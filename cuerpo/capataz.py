import concurrent.futures
import datetime
import hashlib
import json
import os
import subprocess
import sys


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
    try:
        resultado = subprocess.run(
            comando,
            cwd=raiz,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=tope_segundos,
            env=entorno,
        )
    except subprocess.TimeoutExpired:
        return {
            "guardado": False,
            "codigo": None,
            "salida": "TOPE DE TIEMPO: " + str(tope_segundos) + " s",
        }
    salida = resultado.stdout + resultado.stderr
    return {
        "guardado": "GUARDADO AL MOMENTO" in salida,
        "codigo": resultado.returncode,
        "salida": salida,
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


def bucle(proyecto, en_paralelo=2, tope_segundos=900, aviso=print):
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
                marcar_estado(orden.get('id'), 'hecha', '', 0)
                aviso('HECHA ' + orden_id)
            else:
                salida = resultado.get('salida', '')
                tipo = tipo_de_fallo(salida)
                anotar_huella_fallida(orden, tipo)
                fallos_seguidos = (orden.get('fallos_seguidos') or 0) + 1
                marcar_estado(orden.get('id'), 'fallida', tipo, fallos_seguidos)
                aviso('FALLIDA ' + orden_id + ' (' + tipo + ')')
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
        return recoger_los_pedazos.recoger(raiz, nombre)
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
    pedido = ('Eres el perito del pit (acuerdo A-22). Analiza este fallo SOLO con el expediente y leyendo el codigo del proyecto; no uses tu memoria. Responde SOLO un objeto JSON con: que_paso, causa_raiz, donde, quien_fallo (herramienta, programa, equipo o diseno), citas (lista de {archivo, texto} copiados LITERAL del proyecto, que prueban la causa), no_volver_a (la leccion en una frase), tarea_nueva ({repara, pieza, razon, encargo, modo: PROGRAMA o IA}; distinta de la orden que fallo). EXPEDIENTE:' + json.dumps(expediente, ensure_ascii=False, indent=2))
    try:
        resultado = subprocess.run(
            [exe, '-p', '--tools', 'Read,Grep,Glob', '--permission-mode', 'plan'],
            input=pedido,
            cwd=raiz,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=tope_segundos,
        )
    except subprocess.TimeoutExpired:
        return (None, 'el perito no contesto en %d s' % tope_segundos)
    except Exception:
        return (None, 'el perito no contesto')
    salida = resultado.stdout or ''
    inicio = salida.find('{')
    fin = salida.rfind('}')
    if inicio == -1 or fin == -1 or fin < inicio:
        return (None, 'el perito no devolvio JSON: ' + salida[:200])
    trozo = salida[inicio:fin + 1]
    try:
        datos = json.loads(trozo)
    except (ValueError, TypeError):
        return (None, 'el perito no devolvio JSON: ' + salida[:200])
    if not isinstance(datos, dict):
        return (None, 'el perito no devolvio JSON: ' + salida[:200])
    return (datos, 'ok')


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
    lista.append(nueva)
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, 'memoria', 'ORDENES.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)
    return (True, 'agregada ' + str(orden_id))


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

    # Paso 3 vigia_verde: pytest sobre la vigia
    vigia = orden.get("vigia")
    if not vigia:
        return "vigia_verde"
    resultado_vigia = subprocess.run(
        ["python", "-m", "pytest", vigia],
        cwd=carpeta_proyecto,
        capture_output=True,
        text=True,
    )
    if resultado_vigia.returncode != 0:
        resultado_git = subprocess.run(
            ["git", "ls-files", vigia],
            cwd=carpeta_proyecto,
            capture_output=True,
            text=True,
        )
        if resultado_git.stdout.strip() == "":
            return ""
        return "vigia_verde"

    # Paso 4 prueba_real: correr el comando de la orden
    comando = orden.get("comando")
    if not comando:
        return "prueba_real"
    resultado_prueba = subprocess.run(
        comando,
        shell=True,
        cwd=carpeta_proyecto,
        capture_output=True,
        text=True,
    )
    if resultado_prueba.returncode != 0:
        return "prueba_real"

    # Paso 5 guardado: si el comando no esta vacio ya se corrio en el paso 4
    return ""
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
        json.dump(lista, f, indent=2)
    return True
