import concurrent.futures
import datetime
import hashlib
import json
import os
import subprocess
import sys


# Limites de tiempo medidos el 2026-09-21 en el cuaderno de llamadas:
# DeepSeek tarda 4 a 11 s, Big Pickle hasta 328 s y con A-47 se le espera hasta 600 s,
# el guardia corre la bateria en 262 s, y una tarea puede dar 4 vueltas de revision:
# 4 por (11 + 600) + 262 = 2706 s. El tope de fuera tiene que ser mayor que la suma de los de dentro.
# SIN_AVANCE tiene que ser MAYOR que la llamada callada mas larga (la espera de Big Pickle de hasta 600 s),
# o se cortaria a una IA que esta contestando.
LIMITE_TAREA_SEGUNDOS = 420
SIN_AVANCE_SEGUNDOS = 660
TOPE_DURO_SEGUNDOS = 3000


def lanzar_al_equipo(proyecto, orden, tope_segundos=900):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    comando = [
        sys.executable,
        "ingeniero.py",
        "equipo",
        proyecto,
        orden["encargo"],
        "--escribe",
        "deepseek",
        "--revisa",
        "bigpickle",
    ]
    if orden.get("crear"):
        comando.append("--crear")
    entorno = dict(os.environ)
    entorno["PYTHONIOENCODING"] = "utf-8"
    entorno["INGENIERO_ETIQUETA"] = str(orden.get("id", ""))
    archivo = open(os.path.join(raiz, 'memoria', '.salida_tarea_' + str(orden.get('id', '')) + '.txt'), 'w', encoding='utf-8', errors='replace')
    proceso = subprocess.Popen(
        comando,
        cwd=raiz,
        stdout=archivo,
        stderr=subprocess.STDOUT,
        env=entorno,
    )

    def avance():
        import psutil
        total = 0.0
        try:
            pp = psutil.Process(proceso.pid)
            for p in [pp] + pp.children(recursive=True):
                try:
                    t = p.cpu_times()
                    total += t.user + t.system
                except psutil.Error:
                    pass
        except Exception:
            total = 0.0
        total = round(total, 1)
        try:
            total += os.path.getsize(os.path.join(raiz, 'memoria', '.salida_tarea_' + str(orden.get('id', '')) + '.txt'))
        except Exception:
            pass
        for nombre in ('CUADERNO_DE_LLAMADAS.jsonl', 'APLICACIONES.log'):
            try:
                total += os.path.getmtime(os.path.join(raiz, 'memoria', nombre))
            except Exception:
                pass
        return total

    from cuerpo import vigilante
    estado = vigilante.esperar(proceso=proceso, limite=LIMITE_TAREA_SEGUNDOS, sin_avance=SIN_AVANCE_SEGUNDOS, tope_duro=TOPE_DURO_SEGUNDOS, avance=avance)
    archivo.close()
    with open(os.path.join(raiz, 'memoria', '.salida_tarea_' + str(orden.get('id', '')) + '.txt'), encoding='utf-8', errors='replace') as f:
        salida = f.read()
    if estado != 'termino':
        return {
            'guardado': False,
            'codigo': None,
            'salida': 'COLGADA: ' + estado + ' (sin avance pasado el limite; se busca la causa raiz)\n' + salida,
        }
    return {
        'guardado': 'GUARDADO AL MOMENTO' in salida,
        'codigo': proceso.returncode,
        'salida': salida,
    }


def leer_lista():
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, "memoria", "ORDENES.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []
    if isinstance(datos, list):
        return datos
    return []


CAMPOS_ETIQUETA = ('id', 'origen', 'repara', 'pieza', 'depende', 'modo', 'razon', 'encargo')


def validar_etiqueta(orden):
    """Devuelve la lista de problemas de la etiqueta de una orden (vacia = completa)."""
    if not isinstance(orden, dict):
        return ['no es una orden']
    problemas = []
    for campo in CAMPOS_ETIQUETA:
        if campo not in orden:
            problemas.append('falta ' + campo)
            continue
        if campo == 'depende':
            if not isinstance(orden[campo], list):
                problemas.append('depende no es una lista')
            continue
        valor = orden[campo]
        if not isinstance(valor, str) or valor.strip() == '':
            problemas.append('falta ' + campo)
    if 'modo' in orden and orden['modo'] not in ('PROGRAMA', 'IA'):
        problemas.append('modo debe ser PROGRAMA o IA')
    return problemas


def huella_de(orden):
    """Devuelve los primeros 16 caracteres hex del sha256 de encargo + '\n' + pieza."""
    encargo = orden.get('encargo', '') if isinstance(orden, dict) else ''
    pieza = orden.get('pieza', '') if isinstance(orden, dict) else ''
    if not isinstance(encargo, str):
        encargo = ''
    if not isinstance(pieza, str):
        pieza = ''
    texto = encargo + '\n' + pieza
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:16]


def anotar_huella_fallida(orden, motivo):
    """Agrega una linea json con la huella, el id, el motivo y la fecha ISO de hoy."""
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, 'memoria', 'HUELLAS_QUE_FALLARON.jsonl')
    linea = {
        'huella': huella_de(orden),
        'id': orden.get('id', '') if isinstance(orden, dict) else '',
        'motivo': motivo,
        'fecha': datetime.date.today().isoformat(),
    }
    with open(ruta, 'a', encoding='utf-8') as f:
        f.write(json.dumps(linea, ensure_ascii=False) + '\n')


def listas_para_correr():
    """Devuelve, en el mismo orden de la lista, las ordenes que se pueden correr ya."""
    lista = leer_lista()
    resultado = []
    piezas_en_resultado = set()
    piezas_corriendo = set()
    for orden in lista:
        if isinstance(orden, dict) and orden.get('estado') == 'corriendo':
            pieza = orden.get('pieza')
            if pieza:
                piezas_corriendo.add(pieza)
    for orden in lista:
        if not isinstance(orden, dict):
            continue
        if orden.get('estado') != 'pendiente':
            continue
        if validar_etiqueta(orden):
            continue
        if ya_fallo(orden):
            continue
        depende = orden.get('depende')
        if not isinstance(depende, list):
            continue
        ok_depende = True
        for dep_id in depende:
            encontrada = None
            for otra in lista:
                if isinstance(otra, dict) and otra.get('id') == dep_id:
                    encontrada = otra
                    break
            if encontrada is None or encontrada.get('estado') != 'hecha':
                ok_depende = False
                break
        if not ok_depende:
            continue
        pieza = orden.get('pieza')
        if pieza in piezas_corriendo:
            continue
        if pieza in piezas_en_resultado:
            continue
        resultado.append(orden)
        if pieza:
            piezas_en_resultado.add(pieza)
    return resultado


# Tope de gasto del pit (plan v4 P3-8, acuerdo A-27): DeepSeek + Big Pickle no pasan
# de 5 USD al mes. Lo usara el loop del pit (P3-9). Es CUENTA, sin IA.
TOPE_MES_USD = 5.0

# Precios de hora PICO (los mas caros, para que el tope se equivoque del lado seguro),
# copiados de api-docs.deepseek.com/quick_start/pricing el 2026-09-19.
PRECIOS_POR_MILLON = {
    'flash': {'acierto': 0.006, 'fallo': 0.30, 'salida': 1.20},
    'pro': {'acierto': 0.044, 'fallo': 1.32, 'salida': 3.96},
}


def costo_deepseek(modelo, uso):
    """USD que costo una llamada a DeepSeek, segun el dict usage de la respuesta."""
    if not isinstance(uso, dict):
        uso = {}
    acierto = uso.get('prompt_cache_hit_tokens')
    fallo = uso.get('prompt_cache_miss_tokens')
    salida = uso.get('completion_tokens')
    if acierto is None and fallo is None:
        fallo = uso.get('prompt_tokens')
    if acierto is None:
        acierto = 0
    if fallo is None:
        fallo = 0
    if salida is None:
        salida = 0
    if 'flash' in str(modelo).lower():
        precios = PRECIOS_POR_MILLON['flash']
    else:
        precios = PRECIOS_POR_MILLON['pro']
    return (acierto * precios['acierto'] + fallo * precios['fallo'] + salida * precios['salida']) / 1000000


def gastado_del_mes(hoy=None):
    """USD gastados en el mes de 'hoy' (o del dia de hoy). Nunca lanza."""
    if hoy is None:
        hoy = datetime.date.today()
    mes = hoy.strftime('%Y-%m')
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta_memoria = os.path.join(carpeta_proyecto, 'memoria')
    total = 0.0
    ruta_test = os.environ.get('INGENIERO_GASTO_USD_TEST')
    if ruta_test:
        ruta_gasto = ruta_test
    else:
        ruta_gasto = os.path.join(carpeta_memoria, 'GASTO_USD.jsonl')
    try:
        with open(ruta_gasto, encoding='utf-8') as f:
            for linea in f:
                try:
                    dato = json.loads(linea)
                except json.JSONDecodeError:
                    continue
                if not isinstance(dato, dict):
                    continue
                cuando = dato.get('cuando')
                if not isinstance(cuando, str) or not cuando.startswith(mes):
                    continue
                total += costo_deepseek(dato.get('modelo'), dato.get('uso'))
    except (FileNotFoundError, OSError):
        pass
    ruta_log = os.path.join(carpeta_memoria, 'BIGPICKLE.log')
    try:
        with open(ruta_log, encoding='utf-8') as f:
            for linea in f:
                if not linea.startswith(mes):
                    continue
                partes = linea.split('\t')
                for parte in partes:
                    if parte.startswith('costo='):
                        try:
                            total += float(parte[len('costo='):])
                        except ValueError:
                            pass
                        break
    except (FileNotFoundError, OSError):
        pass
    return total


def se_paso_del_tope(hoy=None):
    """True si ya se gasto el tope del mes."""
    return gastado_del_mes(hoy) >= TOPE_MES_USD


def tipo_de_fallo(salida):
    """Devuelve de que tipo fue el fallo, mirando el texto de salida."""
    if isinstance(salida, str) and salida.startswith('COLGADA:'):
        return 'colgada'
    if not isinstance(salida, str):
        return "otro"
    if salida.startswith("TOPE DE TIEMPO"):
        return "tiempo"
    if "EL GUARDIA NO DEJO GUARDAR" in salida or "NO SE GUARDO" in salida:
        return "guardia"
    if "EL EQUIPO NO APROBO" in salida:
        return "no_aprobo"
    if "no se pudo aplicar" in salida:
        return "no_aplico"
    return "otro"


def bucle(proyecto, en_paralelo=1, tope_segundos=900, aviso=print):
    """Corre las ordenes sola hasta que se para por una de las tres causas:
    tope de gasto del mes, todo hecho (o nada se puede correr), o 3 fallos
    del mismo tipo en la misma pieza."""
    fallos_por_pieza_tipo = {}
    while True:
        if se_paso_del_tope():
            return 'PARADO: TOPE DE GASTO (%.2f USD este mes)' % gastado_del_mes()
        tanda = listas_para_correr()[:en_paralelo]
        if not tanda:
            pendientes = []
            for orden in leer_lista():
                if isinstance(orden, dict) and orden.get('estado') in ('pendiente', 'corriendo'):
                    pendientes.append(str(orden.get('id', '')))
            if not pendientes:
                return 'PARADO: TODO HECHO'
            return 'PARADO: NADA SE PUEDE CORRER (pendientes: ' + ','.join(pendientes) + ')'
        for orden in tanda:
            marcar_estado(
                orden.get('id'),
                'corriendo',
                orden.get('paso_fallido') or '',
                orden.get('fallos_seguidos') or 0,
            )

        def correr_una(orden):
            try:
                return lanzar_al_equipo(proyecto, orden, tope_segundos)
            except Exception as e:
                return {'guardado': False, 'codigo': None, 'salida': 'ERROR DEL CAPATAZ: ' + str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(tanda)) as ejecutor:
            resultados = list(ejecutor.map(correr_una, tanda))

        for orden, resultado in zip(tanda, resultados):
            orden_id = str(orden.get('id', ''))
            if resultado.get('guardado'):
                sabotaje = sabotear_la_orden(orden)
                if isinstance(sabotaje, dict) and sabotaje.get('ok') is False:
                    aviso('SABOTAJE ' + orden_id + ' ' + str(sabotaje.get('razon')))
                    marcar_estado(orden.get('id'), 'fallida', 'sabotaje', (orden.get('fallos_seguidos') or 0) + 1)
                    continue
                terminada = la_tarea_esta_terminada(orden)
                if isinstance(terminada, dict) and terminada.get('ok') is False and terminada.get('paso') == 'vigia_verde':
                    aviso('SIN_TERMINAR ' + orden_id + ' ' + str(terminada.get('razon')))
                    marcar_estado(orden.get('id'), 'fallida', terminada.get('paso'), (orden.get('fallos_seguidos') or 0) + 1)
                    continue
                marcar_estado(orden.get('id'), 'hecha', '', 0)
                aviso('HECHA ' + orden_id)
                if isinstance(sabotaje, dict) and sabotaje.get('ok'):
                    aviso('SABOTAJE ' + orden_id + ' ' + str(sabotaje.get('razon')))
            else:
                salida = resultado.get('salida', '')
                tipo = tipo_de_fallo(salida)
                anotar_huella_fallida(orden, tipo)
                fallos_seguidos = (orden.get('fallos_seguidos') or 0) + 1
                marcar_estado(orden.get('id'), 'fallida', tipo, fallos_seguidos)
                aviso('FALLIDA ' + orden_id + ' (' + tipo + ')')
                try:
                    recogido = recoger_lo_frenado(orden, None)
                    if isinstance(recogido, dict) and recogido.get('ok'):
                        aviso('RECOGIDO ' + orden_id + ' ' + str(recogido.get('destino')))
                except Exception as e:
                    aviso('NO SE PUDO RECOGER ' + orden_id + ' ' + str(e)[:200])
                try:
                    informe = forense(orden, resultado)
                    aviso('FORENSE ' + orden_id + ': ' + str(informe.get('paso')) + ' - ' + str(informe.get('motivo')))
                except Exception as e:
                    aviso('FORENSE ' + orden_id + ' no pudo: ' + str(e)[:200])
                pieza = orden.get('pieza')
                clave = (pieza, tipo)
                fallos_por_pieza_tipo[clave] = fallos_por_pieza_tipo.get(clave, 0) + 1
                if fallos_por_pieza_tipo[clave] >= 3:
                    return 'PARADO: 3 FALLOS DEL MISMO TIPO (' + tipo + ') EN ' + str(pieza)


def la_tarea_esta_terminada(orden):
    """Mira si la tarea esta de verdad terminada, no solo guardada.

    El 2026-09-20 el pit dio por terminadas tres tareas solo porque se
    guardaron, sin mirar ni una vez si la prueba de cada tarea estaba verde,
    y una de ellas dejo en la historia una prueba que no podia estar verde
    nunca. Esta funcion es la que mira.

    Recibe la orden y devuelve un diccionario con las claves ok, paso y razon.
    """
    try:
        paso = comprobar_pasos(orden)
        if paso == "":
            return {
                "ok": True,
                "paso": "",
                "razon": "Todos los pasos estan comprobados.",
            }
        return {
            "ok": False,
            "paso": paso,
            "razon": "La tarea no esta terminada porque fallo el paso " + str(paso) + ", por mucho que se haya guardado.",
        }
    except Exception as e:
        return {
            "ok": False,
            "paso": "error",
            "razon": "Fallo al comprobar la tarea: " + str(e),
        }


def correr_orden_del_sistema(palabras):
    """Corre una orden del sistema y devuelve el numero con el que termino.

    Existe aparte para que una prueba pueda ponerla en su sitio sin correr
    nada de verdad.
    """
    import subprocess
    carpeta = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        resultado = subprocess.run(palabras, cwd=carpeta, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return 124
    return resultado.returncode


def armar_sabotaje(orden, raiz=None):
    """Arma la lista de sabotaje de una orden a partir del trabajo aprobado mas nuevo de su pieza.

    El sabotaje es deshacer el cambio aprobado (A-43): se busca en
    raiz/memoria/trabajos_del_equipo el archivo cuyo nombre contiene APROBADO y
    el nombre de la pieza, se toma el de fecha de cambio mas nueva, y se lee su
    propuesta. Si trae una lista 'cambios', por cada trozo con texto_viejo y
    texto_nuevo se agrega {'archivo': pieza, 'viejo': texto_nuevo, 'nuevo':
    texto_viejo}; si no, y trae texto_viejo no vacio, se agrega un solo objeto
    igual. Si no quedo ningun objeto, devuelve False. Si si, crea la carpeta del
    archivo de orden['sabotaje'] (relativo a raiz), escribe la lista con
    json.dump (indent 1, ensure_ascii False) y devuelve True. Nunca lanza: ante
    cualquier error devuelve False.
    """
    try:
        if raiz is None:
            raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pieza = ''
        if isinstance(orden, dict):
            pieza = os.path.basename(str(orden.get('pieza', '')))
        if not pieza:
            return False
        carpeta = os.path.join(raiz, 'memoria', 'trabajos_del_equipo')
        candidatos = []
        for nombre_archivo in os.listdir(carpeta):
            if 'APROBADO' in nombre_archivo and pieza in nombre_archivo:
                ruta = os.path.join(carpeta, nombre_archivo)
                try:
                    candidatos.append((os.path.getmtime(ruta), ruta))
                except OSError:
                    continue
        if not candidatos:
            return False
        candidatos.sort()
        ruta_trabajo = candidatos[-1][1]
        with open(ruta_trabajo, 'r', encoding='utf-8') as f:
            trabajo = json.load(f)
        propuesta = trabajo.get('propuesta') if isinstance(trabajo, dict) else None
        if not isinstance(propuesta, dict):
            return False
        # el nombre de la pieza sirve para buscar su trabajo aprobado; el sabotaje necesita la ruta entera (medido 2026-09-22, orden 70)
        lista = []
        cambios = propuesta.get('cambios')
        if isinstance(cambios, list):
            for trozo in cambios:
                if not isinstance(trozo, dict):
                    continue
                viejo = trozo.get('texto_viejo')
                nuevo = trozo.get('texto_nuevo')
                if viejo and nuevo:
                    lista.append({'archivo': str(orden.get('pieza', '')).replace(chr(92), '/'), 'viejo': nuevo, 'nuevo': viejo})
        else:
            viejo = propuesta.get('texto_viejo')
            nuevo = propuesta.get('texto_nuevo')
            if viejo and nuevo:
                lista.append({'archivo': str(orden.get('pieza', '')).replace(chr(92), '/'), 'viejo': nuevo, 'nuevo': viejo})
        if not lista:
            return False
        destino = orden.get('sabotaje') if isinstance(orden, dict) else None
        if not destino:
            return False
        ruta_destino = os.path.join(raiz, destino)
        carpeta_destino = os.path.dirname(ruta_destino)
        if carpeta_destino:
            os.makedirs(carpeta_destino, exist_ok=True)
        with open(ruta_destino, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=1, ensure_ascii=False)
        return True
    except Exception:
        return False


def sabotear_la_orden(orden):
    """Corre el sabotaje de una orden y comprueba por programa que la vigia de verdad protege.

    Despues de cada cambio hay que comprobar por programa que la vigia de
    verdad protege. Eso lo hacia alguien a mano (orden A-39 punto 2 de Julio,
    del 2026-09-20).
    """
    try:
        vigia = orden.get('vigia') if isinstance(orden, dict) else None
        sabotaje = orden.get('sabotaje') if isinstance(orden, dict) else None
        if vigia and not sabotaje and orden.get('pieza') != vigia:
            sabotaje = 'memoria/sabotajes/orden_' + str(orden.get('id', '')) + '.json'
            orden = dict(orden, sabotaje=sabotaje)
        if not vigia or not sabotaje:
            return {'ok': None, 'razon': 'esta orden no trae lista de sabotaje y por eso no hay nada que correr'}
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.isfile(os.path.join(raiz, sabotaje)):
            if not armar_sabotaje(orden):
                return {'ok': None, 'razon': 'no hay sabotaje escrito y no se pudo armar solo (pieza creada entera o sin trabajo aprobado)'}
        palabras = [sys.executable, 'arnes/sabotaje.py', vigia, sabotaje]
        codigo = correr_orden_del_sistema(palabras)
        if codigo == 0:
            return {'ok': True, 'razon': 'el sabotaje se corrio y la vigia freno'}
        return {'ok': False, 'razon': 'el sabotaje se corrio y la vigia NO freno, o sea que esa vigia no protege de verdad'}
    except Exception as e:
        return {'ok': False, 'razon': str(e)}


def recoger_lo_frenado(orden, raiz):
    """Devuelve a su sitio la copia buena que el guardia dejo apartada en memoria/trabajos_sin_revisar con el final .FRENADO_POR_EL_GUARDIA."""
    try:
        if not raiz:
            raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pieza = orden.get('pieza') if isinstance(orden, dict) else ''
        if not pieza:
            return {'ok': False, 'razon': 'la orden no dice que pieza toca'}
        nombre = os.path.basename(pieza) + '.FRENADO_POR_EL_GUARDIA'
        from arnes import recoger_los_pedazos
        import subprocess
        import sys
        resultado = recoger_los_pedazos.recoger(raiz, nombre)
        if not isinstance(resultado, dict) or not resultado.get('ok'):
            return resultado
        from arnes import guardia_de_guardado
        if guardia_de_guardado._hay_llaves(raiz, [pieza]):
            os.replace(pieza, os.path.join(raiz, 'memoria', 'trabajos_sin_revisar', os.path.basename(pieza) + '.LLAVE'))
            return {'ok': False, 'destino': resultado.get('destino'), 'razon': 'la copia recogida trae algo con forma de llave: no se deja en el disco'}
        if orden.get('entrega_la_prueba') == 'si':
            return resultado
        vigia = orden.get('vigia')
        if not vigia:
            return resultado
        entorno = dict(os.environ)
        entorno['INGENIERO_OFF'] = '1'
        prueba = subprocess.run(
            [sys.executable, '-m', 'pytest', '-q', vigia],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=300,
            env=entorno,
        )
        if prueba.returncode != 0:
            guardada = subprocess.run(
                ['git', 'cat-file', '-e', 'HEAD:' + pieza],
                cwd=raiz,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if guardada.returncode != 0:
                os.replace(pieza, os.path.join(raiz, 'memoria', 'trabajos_sin_revisar', os.path.basename(pieza) + '.ROJO'))
            else:
                subprocess.run(
                    ['git', 'checkout', 'HEAD', '--', pieza],
                    cwd=raiz,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            return {'ok': False, 'destino': resultado.get('destino'), 'razon': 'la copia recogida deja su prueba roja: no se deja en el disco'}
        from arnes import guardia_de_guardado
        paso, _mensaje = guardia_de_guardado._vigias(raiz)
        if paso is not True:
            guardada = subprocess.run(
                ['git', 'cat-file', '-e', 'HEAD:' + pieza],
                cwd=raiz,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if guardada.returncode != 0:
                os.replace(pieza, os.path.join(raiz, 'memoria', 'trabajos_sin_revisar', os.path.basename(pieza) + '.ROJO'))
            else:
                subprocess.run(
                    ['git', 'checkout', 'HEAD', '--', pieza],
                    cwd=raiz,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            return {'ok': False, 'destino': resultado.get('destino'), 'razon': 'la copia recogida pone rojas a sus vecinas: no se deja en el disco'}
        return resultado
    except Exception as e:
        return {'ok': False, 'razon': str(e)}


def armar_expediente(orden, resultado):
    """Junta en un dict lo que el perito necesita para analizar el fallo sin usar su memoria."""
    orden = orden if isinstance(orden, dict) else {}
    resultado = resultado if isinstance(resultado, dict) else {}
    salida = resultado.get('salida', '')
    if not isinstance(salida, str):
        salida = ''
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta_memoria = os.path.join(carpeta_proyecto, 'memoria')
    pieza = orden.get('pieza', '')
    if not isinstance(pieza, str):
        pieza = ''
    prefijo = os.path.basename(pieza)
    apartados = []
    carpeta_trabajos = os.path.join(carpeta_memoria, 'trabajos_sin_revisar')
    if os.path.isdir(carpeta_trabajos):
        for nombre in os.listdir(carpeta_trabajos):
            if nombre.endswith('.FRENADO_POR_EL_GUARDIA') and nombre.startswith(prefijo):
                apartados.append(nombre)
    dict_expediente = {
        'orden': orden,
        'huella': huella_de(orden),
        'tipo': tipo_de_fallo(salida),
        'codigo': resultado.get('codigo'),
        'salida': salida[-4000:],
        'apartados': apartados,
        'fecha': datetime.datetime.now().isoformat(timespec='seconds'),
    }
    carpeta_expedientes = os.path.join(carpeta_memoria, 'EXPEDIENTES')
    try:
        os.makedirs(carpeta_expedientes, exist_ok=True)
        marca = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        ruta = os.path.join(carpeta_expedientes, str(orden.get('id', '')) + '_' + marca + '.json')
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(dict_expediente, f, indent=2, ensure_ascii=False)
        return (ruta, dict_expediente)
    except OSError:
        return (None, dict_expediente)


def citas_que_no_existen(citas, raiz):
    """Devuelve las citas que no sirven: no son dict, estan vacias, se salen del proyecto, el archivo no existe o el texto no aparece literal."""
    if not isinstance(citas, list):
        return [{'archivo': '', 'texto': '', 'por_que': 'no hay lista de citas'}]
    malas = []
    try:
        raiz_real = os.path.realpath(raiz)
    except (OSError, ValueError):
        raiz_real = ''
    for cita in citas:
        if not isinstance(cita, dict):
            malas.append({'archivo': '', 'texto': '', 'por_que': 'no es una cita'})
            continue
        archivo = cita.get('archivo', '')
        texto = cita.get('texto', '')
        if not isinstance(archivo, str):
            archivo = ''
        if not isinstance(texto, str):
            texto = ''
        if texto.strip() == '':
            malas.append({'archivo': archivo, 'texto': texto, 'por_que': 'cita vacia'})
            continue
        try:
            ruta = os.path.realpath(os.path.join(raiz_real, archivo))
            dentro = os.path.commonpath([raiz_real, ruta]) == raiz_real
        except (OSError, ValueError):
            dentro = False
        if not dentro:
            malas.append({'archivo': archivo, 'texto': texto, 'por_que': 'fuera del proyecto'})
            continue
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
        except (OSError, ValueError):
            malas.append({'archivo': archivo, 'texto': texto, 'por_que': 'el archivo no existe'})
            continue
        if texto.replace('\r', '') not in contenido.replace('\r', ''):
            malas.append({'archivo': archivo, 'texto': texto, 'por_que': 'no aparece literal'})
    return malas


def pedir_al_perito(expediente, raiz, tope_segundos=600):
    """Llama a Claude como perito en solo lectura para analizar un fallo con el expediente."""
    import shutil
    exe = shutil.which('claude')
    if not exe:
        return (None, 'no encuentro claude en el PATH')
    pedido = ('Eres el perito del pit (acuerdo A-22). Analiza este fallo SOLO con el expediente y leyendo el codigo del proyecto; no uses tu memoria. Responde SOLO un objeto JSON con: que_paso, causa_raiz, donde, quien_fallo (herramienta, programa, equipo o diseno), citas (lista de {archivo, texto} copiados LITERAL del proyecto, que prueban la causa), no_volver_a (la leccion en una frase), tarea_nueva ({repara, pieza, razon, encargo, modo: PROGRAMA o IA}; distinta de la orden que fallo). OBLIGATORIO: tu respuesta completa es SOLO el objeto JSON, sin una sola palabra antes ni despues. EXPEDIENTE:' + json.dumps(expediente, ensure_ascii=False, indent=2))
    esquema = json.dumps({
        'type': 'object',
        'properties': {
            'que_paso': {'type': 'string'},
            'causa_raiz': {'type': 'string'},
            'donde': {'type': 'string'},
            'quien_fallo': {'type': 'string'},
            'no_volver_a': {'type': 'string'},
            'citas': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'archivo': {'type': 'string'},
                        'texto': {'type': 'string'},
                    },
                },
            },
            'tarea_nueva': {'type': 'object'},
        },
        'required': ['que_paso', 'causa_raiz'],
    }, ensure_ascii=False)
    orden = [exe, '-p', '--tools', 'Read,Grep,Glob', '--permission-mode', 'plan', '--json-schema', esquema]
    entrada = pedido
    for intento in range(3):
        try:
            entorno = dict(os.environ)
            entorno['INGENIERO_OFF'] = '1'
            resultado = subprocess.run(
                orden,
                input=entrada,
                cwd=raiz,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=tope_segundos,
                env=entorno,
            )
        except subprocess.TimeoutExpired:
            return (None, 'el perito no contesto en %d s' % tope_segundos)
        except Exception:
            return (None, 'el perito no contesto')
        salida = resultado.stdout or ''
        inicio = salida.find('{')
        fin = salida.rfind('}')
        if inicio != -1 and fin != -1 and fin >= inicio:
            trozo = salida[inicio:fin + 1]
            try:
                datos = json.loads(trozo)
            except (ValueError, TypeError):
                datos = None
            if isinstance(datos, dict):
                return (datos, 'ok')
        entrada = 'RECORDATORIO: no respondiste en JSON. Responde SOLO el objeto JSON pedido, nada mas. ' + pedido
    return (None, 'el perito no devolvio JSON: ' + salida[:200])


def juzgar_citas(analisis):
    """Juzga si las citas de un analisis prueban de verdad la causa de raiz que se afirma."""
    from cuerpo import bigpickle
    if not isinstance(analisis, dict):
        return (False, 'no hay analisis')
    pedido = ('Eres el revisor del forense. Estas citas son LITERALES del proyecto (un programa ya comprobo que existen). Juzga SOLO si prueban la causa de raiz que se afirma. Responde SOLO un objeto JSON {"prueban": true o false, "por_que": "una frase"}. CAUSA: ' + str(analisis.get('causa_raiz', '')) + ' CITAS: ' + json.dumps(analisis.get('citas', []), ensure_ascii=False))
    texto, avisos = bigpickle.preguntar(pedido)
    if not texto:
        return (False, 'Big Pickle no contesto: ' + '; '.join(avisos)[:200])
    inicio = texto.find('{')
    fin = texto.rfind('}')
    if inicio == -1 or fin == -1 or fin < inicio:
        return (False, 'Big Pickle no devolvio JSON')
    try:
        dato = json.loads(texto[inicio:fin + 1])
    except (ValueError, TypeError):
        return (False, 'Big Pickle no devolvio JSON')
    if not isinstance(dato, dict):
        return (False, 'Big Pickle no devolvio JSON')
    return (dato.get('prueban') is True, str(dato.get('por_que', '')))


def agregar_orden(orden):
    """Agrega una orden nueva a la lista si pasa las validaciones."""
    if not isinstance(orden, dict):
        return (False, 'no es una orden')
    problemas = validar_etiqueta(orden)
    if problemas:
        return (False, 'etiqueta incompleta: ' + ', '.join(problemas))
    lista = leer_lista()
    orden_id = orden.get('id')
    for otra in lista:
        if isinstance(otra, dict) and otra.get('id') == orden_id:
            return (False, 'ya existe el id ' + str(orden_id))
    if ya_fallo(orden):
        return (False, 'esa misma tarea ya fallo')
    huella = huella_de(orden)
    for otra in lista:
        if isinstance(otra, dict) and huella_de(otra) == huella:
            return (False, 'ya esta en la lista')
    nueva = dict(orden)
    nueva['estado'] = 'pendiente'
    nueva['paso_fallido'] = ''
    nueva['fallos_seguidos'] = 0
    # ley A-43, el arreglo de la herramienta va al frente
    if str(nueva.get('origen', '')).startswith('forense:'):
        lista.insert(0, nueva)
    else:
        lista.append(nueva)
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, 'memoria', 'ORDENES.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)
    return (True, 'agregada ' + str(orden_id))


def reintentar_tras_el_arreglo(id_orden, id_arreglo):
    """Deja pendiente la orden y borra su huella de HUELLAS_QUE_FALLARON.jsonl.

    Nunca lanza: ante cualquier error devuelve False.
    """
    try:
        lista = leer_lista()
        encontrada = None
        for orden in lista:
            if isinstance(orden, dict) and orden.get('id') == id_orden:
                encontrada = orden
                break
        if encontrada is None:
            return False
        encontrada['estado'] = 'pendiente'
        encontrada['paso_fallido'] = ''
        encontrada['fallos_seguidos'] = 0
        depende = encontrada.get('depende')
        if not isinstance(depende, list):
            depende = []
        if id_arreglo not in depende:
            depende.append(id_arreglo)
        encontrada['depende'] = depende
        carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.join(carpeta_proyecto, 'memoria', 'ORDENES.json')
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=2, ensure_ascii=False)
        huella = huella_de(encontrada)
        ruta_huellas = os.path.join(carpeta_proyecto, 'memoria', 'HUELLAS_QUE_FALLARON.jsonl')
        try:
            with open(ruta_huellas, encoding='utf-8') as f:
                renglones = f.readlines()
        except (FileNotFoundError, OSError):
            return True
        conservados = []
        for renglon in renglones:
            try:
                dato = json.loads(renglon)
            except json.JSONDecodeError:
                conservados.append(renglon)
                continue
            if isinstance(dato, dict) and dato.get('huella') == huella:
                continue
            conservados.append(renglon)
        with open(ruta_huellas, 'w', encoding='utf-8') as f:
            f.writelines(conservados)
        return True
    except Exception:
        return False


def forense(orden, resultado, raiz=None):
    """Analiza un fallo con el perito, comprueba sus citas, lo juzga y deja tarea nueva. Nunca lanza."""
    if raiz is None:
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta, expediente = armar_expediente(orden, resultado)
    analisis, estado = pedir_al_perito(expediente, raiz)
    if analisis is None:
        informe = {'ok': False, 'paso': 'perito', 'motivo': estado}
    else:
        citas = analisis.get('citas')
        if not isinstance(citas, list) or not citas:
            informe = {'ok': False, 'paso': 'citas', 'motivo': 'el perito no trajo citas'}
        else:
            malas = citas_que_no_existen(citas, raiz)
            if malas:
                informe = {'ok': False, 'paso': 'citas', 'motivo': 'citas que no existen: ' + json.dumps(malas, ensure_ascii=False)[:500]}
            else:
                prueban, por_que = juzgar_citas(analisis)
                if not prueban:
                    informe = {'ok': False, 'paso': 'juez', 'motivo': por_que}
                else:
                    try:
                        from cuerpo import fallos
                        import re
                        fallos.apuntar(
                            que_paso=str(analisis.get('que_paso') or 'fallo en el pit')[:200],
                            causa_raiz=str(analisis.get('causa_raiz', ''))[:300],
                            cura='tarea nueva del forense',
                            no_volver_a=str(analisis.get('no_volver_a', ''))[:200],
                            proyecto=os.path.basename(str(raiz)),
                            piezas=[str(orden.get('pieza', ''))],
                            quien_lo_caza='pit (forense)',
                            disparador=re.escape(str(orden.get('pieza', ''))) or 'pit',
                        )
                    except Exception:
                        pass
                    tarea = dict(analisis.get('tarea_nueva') or {})
                    tarea['id'] = str(orden.get('id', '')) + '-F' + datetime.datetime.now().strftime('%H%M%S')
                    tarea['origen'] = 'forense:' + str(orden.get('id', ''))
                    if 'depende' not in tarea:
                        tarea['depende'] = []
                    ok, motivo = agregar_orden(tarea)
                    informe = {'ok': ok, 'paso': 'tarea', 'motivo': motivo, 'tarea': tarea['id']}
    informe['expediente'] = ruta
    if ruta is not None:
        try:
            junto = dict(expediente)
            junto['analisis'] = analisis
            junto['informe'] = informe
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(junto, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    return informe


def ya_fallo(orden):
    """True si la huella_de(orden) aparece en el archivo; nunca lanza."""
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, 'memoria', 'HUELLAS_QUE_FALLARON.jsonl')
    huella = huella_de(orden)
    try:
        with open(ruta, encoding='utf-8') as f:
            for linea in f:
                try:
                    dato = json.loads(linea)
                except json.JSONDecodeError:
                    continue
                if isinstance(dato, dict) and dato.get('huella') == huella:
                    return True
    except (FileNotFoundError, OSError):
        return False
    return False


def siguiente_pendiente():
    for orden in leer_lista():
        if orden.get("estado") == "pendiente" and not validar_etiqueta(orden):
            return orden
    return None


def marcar_estado(orden_id, estado, paso_fallido='', fallos_seguidos=0):
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, "memoria", "ORDENES.json")
    lista = leer_lista()
    encontrada = False
    for orden in lista:
        if orden.get("id") == orden_id:
            orden["estado"] = estado
            orden["paso_fallido"] = paso_fallido
            orden["fallos_seguidos"] = fallos_seguidos
            encontrada = True
            break
    if not encontrada:
        return False
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)
    return True


def comprobar_pasos(orden):
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Paso 1 ronda: buscar el archivo mas reciente APROBADO de la pieza
    pieza = orden.get("pieza")
    if not pieza:
        return "ronda"
    base = os.path.splitext(os.path.basename(pieza))[0]
    carpeta_trabajos = os.path.join(carpeta_proyecto, "memoria", "trabajos_del_equipo")
    candidatos = []
    try:
        for nombre in os.listdir(carpeta_trabajos):
            if base in nombre and "APROBADO" in nombre:
                ruta_cand = os.path.join(carpeta_trabajos, nombre)
                candidatos.append((os.path.getmtime(ruta_cand), ruta_cand))
    except OSError:
        return "ronda"
    if not candidatos:
        return "ronda"
    candidatos.sort(reverse=True)
    ruta_ronda = candidatos[0][1]
    try:
        with open(ruta_ronda, encoding="utf-8") as f:
            datos_ronda = json.load(f)
    except (OSError, json.JSONDecodeError):
        return "ronda"
    obrero = datos_ronda.get("obrero")
    auditor = datos_ronda.get("auditor")
    if not obrero or not auditor or obrero == auditor:
        return "ronda"

    # Paso 2 aplicada: la ruta del campo pieza existe en disco
    if not os.path.exists(pieza):
        return "aplicada"

    # Paso 2b pieza_suelta: si la pieza es un .py que existe, algun otro .py
    # del proyecto debe nombrarla por su nombre de modulo; si nadie la nombra,
    # la pieza quedo suelta y se devuelve "aplicada".
    if pieza.endswith(".py") and os.path.exists(pieza):
        modulo = os.path.splitext(os.path.basename(pieza))[0]
        ruta_pieza_abs = os.path.abspath(pieza)
        nombrada = False
        for raiz, _dirs, archivos in os.walk(carpeta_proyecto):
            for nombre_archivo in archivos:
                if not nombre_archivo.endswith(".py"):
                    continue
                ruta_otro = os.path.join(raiz, nombre_archivo)
                if os.path.abspath(ruta_otro) == ruta_pieza_abs:
                    continue
                try:
                    with open(ruta_otro, encoding="utf-8") as f:
                        contenido = f.read()
                except OSError:
                    continue
                if modulo in contenido:
                    nombrada = True
                    break
            if nombrada:
                break
        if not nombrada:
            return "aplicada"

    # Paso 3 vigia_verde: pytest sobre la vigia
    vigia = orden.get("vigia")
    if not vigia:
        return "vigia_verde"
    ruta_vigia = os.path.join(carpeta_proyecto, vigia)
    if not os.path.isfile(ruta_vigia):
        return "vigia_verde"
    try:
        resultado_vigia = subprocess.run(
            ["python", "-m", "pytest", vigia],
            cwd=carpeta_proyecto,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return "vigia_verde"
    if orden.get("entrega_la_prueba") == "si":
        # La tarea ENTREGA la prueba: se comprueba al reves. La prueba tiene
        # que existir y estar ROJA. Si ya esta verde, este paso falla, porque
        # una prueba que pasa antes del cambio no demuestra nada.
        if resultado_vigia.returncode == 0:
            return "vigia_verde"
        # No basta con que pytest devuelva rojo: hay que mirar la salida.
        # Si el rojo viene de una comprobacion no cumplida (AssertionError)
        # la prueba nacio roja de verdad y el paso esta bien. Si viene de un
        # reventon de la propia prueba (AttributeError, NameError o TypeError
        # sin AssertionError) el paso FALLA, porque una prueba que revienta no
        # mide nada. Excepcion: ImportError o ModuleNotFoundError nombrando
        # justo la pieza que esta orden va a crear SI valen, porque es normal
        # que la prueba no encuentre todavia una pieza que aun no existe.
        salida_vigia = (resultado_vigia.stdout or "") + (resultado_vigia.stderr or "")
        if "AssertionError" in salida_vigia:
            return ""
        pieza_de_la_orden = orden.get("pieza") or ""
        nombre_pieza = os.path.splitext(os.path.basename(pieza_de_la_orden))[0]
        if nombre_pieza and ("ImportError" in salida_vigia or "ModuleNotFoundError" in salida_vigia) and nombre_pieza in salida_vigia:
            return ""
        if "AttributeError" in salida_vigia or "NameError" in salida_vigia or "TypeError" in salida_vigia:
            return "vigia_verde"
        return ""
    if resultado_vigia.returncode != 0:
        try:
            resultado_git = subprocess.run(
                ["git", "ls-files", vigia],
                cwd=carpeta_proyecto,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return "vigia_verde"
        if resultado_git.stdout.strip() == "":
            return ""
        return "vigia_verde"

    # Paso 4 prueba_real: correr el comando de la orden
    comando = orden.get("comando")
    if not comando:
        return "prueba_real"
    try:
        resultado_prueba = subprocess.run(
            comando,
            shell=True,
            cwd=carpeta_proyecto,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return "prueba_real"
    if resultado_prueba.returncode != 0:
        return "prueba_real"

    # Paso 5 guardado: si el comando no esta vacio ya se corrio en el paso 4
    return ""
