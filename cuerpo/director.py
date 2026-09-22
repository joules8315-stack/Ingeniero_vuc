"""cuerpo/director.py -- Orden de Julio A-48 del 2026-09-22.

Con esto Codex (o Claude) dirige el loop sin escribir archivos a mano:
el programa escribe. Solo biblioteca estandar de Python (json, os,
subprocess, sys). Todas las rutas son relativas a la raiz que se pasa
como primer argumento.

Cuatro funciones publicas:

  - estado(raiz)          -> texto con el parte del dia.
  - orden_nueva(raiz, t)  -> (True/False, motivo).
  - reintentar(raiz, id)  -> (True/False, motivo).
  - hecha(raiz, id)       -> (True/False, motivo).

Ninguna lanza: todo error se devuelve como (False, motivo) y estado
devuelve el texto del error.
"""

import json
import os
import subprocess
import sys


# ----------------------------------------------------------------------
# Rutas y utilidades internas
# ----------------------------------------------------------------------


def _ruta_memoria(raiz):
    return os.path.join(raiz, 'memoria')


def _ruta_ordenes(raiz):
    return os.path.join(_ruta_memoria(raiz), 'ORDENES.json')


def _ruta_expedientes(raiz):
    return os.path.join(_ruta_memoria(raiz), 'EXPEDIENTES')


def _ruta_huellas(raiz):
    return os.path.join(_ruta_memoria(raiz), 'HUELLAS_QUE_FALLARON.jsonl')


def _ruta_rescate(raiz):
    return os.path.join(_ruta_memoria(raiz), 'rescate')


def _leer_ordenes(raiz):
    """Devuelve la lista de ordenes. Si el JSON trae un dict, usa su
    clave 'ordenes'. Si no existe el archivo, devuelve lista vacia."""
    ruta = _ruta_ordenes(raiz)
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    if isinstance(datos, dict):
        datos = datos.get('ordenes', [])
    if not isinstance(datos, list):
        return []
    return datos


def _guardar_ordenes(raiz, ordenes):
    """Escritura atomica: archivo .tmp y os.replace."""
    ruta = _ruta_ordenes(raiz)
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    tmp = ruta + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(ordenes, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ruta)


def _buscar_orden(ordenes, id_orden):
    for o in ordenes:
        if isinstance(o, dict) and o.get('id') == id_orden:
            return o
    return None


def _texto_no_vacio(valor):
    return isinstance(valor, str) and valor.strip() != ''


def _cortar(linea, tope=400):
    linea = linea.rstrip('\n').rstrip('\r')
    if len(linea) > tope:
        return linea[:tope]
    return linea


# ----------------------------------------------------------------------
# 1) estado
# ----------------------------------------------------------------------


def estado(raiz):
    """Devuelve el parte del dia como texto.

    - Cuenta de cada estado (una linea 'pendiente: N' por estado).
    - Las 8 primeras ordenes pendientes o corriendo (id y titulo).
    - De los 5 archivos mas nuevos de raiz/memoria/EXPEDIENTES (si la
      carpeta existe): id de la orden, tipo y las lineas de su salida
      que contienen VEREDICTO, fallo, resumen, GUARDIA o NO SE
      (cada una cortada a 400 letras).

    Si algo falla, devuelve el texto del error.
    """
    try:
        ordenes = _leer_ordenes(raiz)
    except Exception as e:
        return 'ERROR leyendo ordenes: %s' % e

    lineas = []

    # --- cuenta por estado ---
    cuenta = {}
    for o in ordenes:
        if not isinstance(o, dict):
            continue
        est = o.get('estado', '') or ''
        cuenta[est] = cuenta.get(est, 0) + 1
    if cuenta:
        for est in sorted(cuenta.keys()):
            lineas.append('%s: %d' % (est, cuenta[est]))
    else:
        lineas.append('(sin ordenes)')

    # --- 8 primeras pendientes o corriendo ---
    lineas.append('')
    lineas.append('-- pendientes o corriendo (max 8) --')
    mostradas = 0
    for o in ordenes:
        if not isinstance(o, dict):
            continue
        est = o.get('estado', '')
        if est in ('pendiente', 'corriendo'):
            lineas.append('%s | %s' % (o.get('id', '?'), o.get('titulo', '')))
            mostradas += 1
            if mostradas >= 8:
                break
    if mostradas == 0:
        lineas.append('(ninguna)')

    # --- expedientes mas nuevos ---
    carpeta = _ruta_expedientes(raiz)
    if os.path.isdir(carpeta):
        try:
            nombres = os.listdir(carpeta)
        except Exception as e:
            lineas.append('')
            lineas.append('ERROR leyendo EXPEDIENTES: %s' % e)
            return '\n'.join(lineas)

        archivos = []
        for nombre in nombres:
            ruta = os.path.join(carpeta, nombre)
            if os.path.isfile(ruta):
                try:
                    mtime = os.path.getmtime(ruta)
                except Exception:
                    mtime = 0
                archivos.append((mtime, ruta))
        archivos.sort(key=lambda par: par[0], reverse=True)
        archivos = archivos[:5]

        lineas.append('')
        lineas.append('-- expedientes mas nuevos (max 5) --')
        if not archivos:
            lineas.append('(ninguno)')
        for _mtime, ruta in archivos:
            lineas.append('')
            lineas.append('== %s ==' % os.path.basename(ruta))
            try:
                with open(ruta, 'r', encoding='utf-8', errors='replace') as f:
                    contenido = f.read()
            except Exception as e:
                lineas.append('ERROR leyendo %s: %s' % (os.path.basename(ruta), e))
                continue

            try:
                datos = json.loads(contenido)
            except Exception:
                datos = None

            if isinstance(datos, dict):
                id_orden = datos.get('id', datos.get('orden', ''))
                tipo = datos.get('tipo', '')
                salida = datos.get('salida', '')
                if not isinstance(salida, str):
                    salida = json.dumps(salida, ensure_ascii=False)
            else:
                id_orden = ''
                tipo = ''
                salida = contenido

            lineas.append('id: %s' % id_orden)
            lineas.append('tipo: %s' % tipo)
            claves = ('VEREDICTO', 'fallo', 'resumen', 'GUARDIA', 'NO SE')
            for linea in salida.splitlines():
                if any(clave in linea for clave in claves):
                    lineas.append(_cortar(linea))

    return '\n'.join(lineas)


# ----------------------------------------------------------------------
# 2) orden_nueva
# ----------------------------------------------------------------------


def orden_nueva(raiz, texto):
    """Anade una orden nueva al principio de la lista.

    El texto debe ser un JSON con un dict que traiga id, titulo, pieza,
    encargo y vigia no vacios, y cuyo id no exista ya.

    Devuelve (True, motivo) o (False, motivo).
    """
    try:
        datos = json.loads(texto)
    except Exception as e:
        return (False, 'el texto no es JSON valido: %s' % e)

    if not isinstance(datos, dict):
        return (False, 'el JSON tiene que ser un objeto con id, titulo, pieza, encargo y vigia')

    for campo in ('id', 'titulo', 'pieza', 'encargo', 'vigia'):
        if not _texto_no_vacio(datos.get(campo)):
            return (False, 'falta %s o esta vacio' % campo)

    try:
        ordenes = _leer_ordenes(raiz)
    except Exception as e:
        return (False, 'no se pudieron leer las ordenes: %s' % e)

    if _buscar_orden(ordenes, datos['id']) is not None:
        return (False, 'ya existe una orden con id %s' % datos['id'])

    nueva = dict(datos)
    nueva.setdefault('depende', [])
    nueva.setdefault('modo', 'IA')
    nueva.setdefault('estado', 'pendiente')
    nueva.setdefault('paso_fallido', '')
    nueva.setdefault('fallos_seguidos', 0)
    nueva.setdefault('nota', '')
    nueva.setdefault('prueba_real', '')
    nueva.setdefault('comando', '')

    ordenes.insert(0, nueva)

    try:
        _guardar_ordenes(raiz, ordenes)
    except Exception as e:
        return (False, 'no se pudo guardar: %s' % e)

    return (True, 'orden %s creada y puesta la primera' % nueva['id'])


def orden_corta(raiz, id, pieza, vigia, que_hacer):
    """Crea una orden corta a partir de que_hacer.

    El encargo es que_hacer. Detras, por cada palabra de que_hacer que sea
    el nombre de una funcion o clase definida en raiz/pieza (si existe), el
    texto 'def NOMBRE(...): (linea N)' con la linea exacta copiada del
    archivo y su numero. Detras, 'No toques ningun otro archivo.'.

    Si la pieza no existe, crear es True.

    Luego da de alta la orden con orden_nueva(raiz, json.dumps({...})) con
    titulo = que_hacer cortado a 90 letras, y devuelve lo mismo que
    orden_nueva.
    """
    crear = not os.path.isfile(os.path.join(raiz, pieza))

    lineas = [que_hacer]

    if not crear:
        try:
            with open(os.path.join(raiz, pieza), 'r', encoding='utf-8', errors='replace') as f:
                contenido = f.read()
        except Exception:
            contenido = ''

        if contenido:
            palabras = que_hacer.split()
            for numero, linea in enumerate(contenido.splitlines(), 1):
                limpia = linea.strip()
                if limpia.startswith('def ') or limpia.startswith('class '):
                    resto = limpia[4:] if limpia.startswith('def ') else limpia[6:]
                    nombre = ''
                    for c in resto:
                        if c.isalnum() or c == '_':
                            nombre += c
                        else:
                            break
                    if nombre and nombre in palabras:
                        lineas.append('%s (linea %d)' % (limpia, numero))

    lineas.append('No toques ningun otro archivo.')
    encargo = '\n'.join(lineas)

    datos = {
        'id': id,
        'titulo': que_hacer[:90],
        'pieza': pieza,
        'encargo': encargo,
        'vigia': vigia,
        'crear': crear,
    }

    return orden_nueva(raiz, json.dumps(datos))


# ----------------------------------------------------------------------
# 3) reintentar
# ----------------------------------------------------------------------


def reintentar(raiz, id):
    """Pone la orden en pendiente, fallos_seguidos 0 y paso_fallido ''.

    Ademas quita de HUELLAS_QUE_FALLARON.jsonl las lineas cuyo JSON
    tiene ese id, guardando antes una copia en
    raiz/memoria/rescate/HUELLAS.antes_<id>.

    Devuelve (True, motivo) o (False, motivo).
    """
    try:
        ordenes = _leer_ordenes(raiz)
    except Exception as e:
        return (False, 'no se pudieron leer las ordenes: %s' % e)

    orden = _buscar_orden(ordenes, id)
    if orden is None:
        return (False, 'no existe la orden %s' % id)

    orden['estado'] = 'pendiente'
    orden['fallos_seguidos'] = 0
    orden['paso_fallido'] = ''

    try:
        _guardar_ordenes(raiz, ordenes)
    except Exception as e:
        return (False, 'no se pudo guardar: %s' % e)

    # --- limpiar huellas ---
    ruta_huellas = _ruta_huellas(raiz)
    if os.path.exists(ruta_huellas):
        try:
            with open(ruta_huellas, 'r', encoding='utf-8', errors='replace') as f:
                lineas = f.readlines()
        except Exception as e:
            return (False, 'no se pudieron leer las huellas: %s' % e)

        # copia de rescate
        try:
            carpeta_rescate = _ruta_rescate(raiz)
            os.makedirs(carpeta_rescate, exist_ok=True)
            ruta_copia = os.path.join(carpeta_rescate, 'HUELLAS.antes_%s' % id)
            with open(ruta_copia, 'w', encoding='utf-8') as f:
                f.writelines(lineas)
        except Exception as e:
            return (False, 'no se pudo guardar la copia de rescate: %s' % e)

        conservadas = []
        for linea in lineas:
            texto = linea.strip()
            if texto == '':
                conservadas.append(linea)
                continue
            try:
                registro = json.loads(texto)
            except Exception:
                conservadas.append(linea)
                continue
            if isinstance(registro, dict) and registro.get('id') == id:
                continue
            conservadas.append(linea)

        try:
            tmp = ruta_huellas + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                f.writelines(conservadas)
            os.replace(tmp, ruta_huellas)
        except Exception as e:
            return (False, 'no se pudieron reescribir las huellas: %s' % e)

    return (True, 'orden %s puesta en pendiente y huellas limpiadas' % id)


# ----------------------------------------------------------------------
# 4) hecha
# ----------------------------------------------------------------------


def hecha(raiz, id):
    """Corre el vigia de la orden con pytest.

    Si pytest sale con 0, pone la orden en hecha y guarda.
    Si no, devuelve (False, las ultimas 15 lineas de la salida) y no
    toca la orden.
    """
    try:
        ordenes = _leer_ordenes(raiz)
    except Exception as e:
        return (False, 'no se pudieron leer las ordenes: %s' % e)

    orden = _buscar_orden(ordenes, id)
    if orden is None:
        return (False, 'no existe la orden %s' % id)

    vigia = orden.get('vigia', '')
    if not _texto_no_vacio(vigia):
        return (False, 'la orden %s no tiene vigia' % id)

    comando = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', vigia]

    try:
        resultado = subprocess.run(
            comando,
            cwd=raiz,
            timeout=600,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
        )
    except subprocess.TimeoutExpired:
        return (False, 'el vigia tardo mas de 600 segundos')
    except Exception as e:
        return (False, 'no se pudo correr el vigia: %s' % e)

    if resultado.returncode == 0:
        orden['estado'] = 'hecha'
        try:
            _guardar_ordenes(raiz, ordenes)
        except Exception as e:
            return (False, 'el vigia paso pero no se pudo guardar: %s' % e)
        return (True, 'orden %s marcada como hecha' % id)

    salida = (resultado.stdout or '') + (resultado.stderr or '')
    ultimas = salida.splitlines()[-15:]
    return (False, '\n'.join(ultimas))


def depende(raiz, id, lista_ids):
    """Pone depende = lista_ids (lista de textos; vacia vale) en esa orden.

    Guarda con escritura atomica como las demas y devuelve (True, motivo)
    o (False, motivo) si no existe la orden.
    """
    try:
        ordenes = _leer_ordenes(raiz)
    except Exception as e:
        return (False, 'no se pudieron leer las ordenes: %s' % e)

    orden = _buscar_orden(ordenes, id)
    if orden is None:
        return (False, 'no existe la orden %s' % id)

    orden['depende'] = lista_ids

    try:
        _guardar_ordenes(raiz, ordenes)
    except Exception as e:
        return (False, 'no se pudo guardar: %s' % e)

    return (True, 'orden %s: depende = %s' % (id, lista_ids))


def archivar(raiz, id, motivo):
    """Pone estado archivada y nota = motivo en esa orden.

    Devuelve (True, motivo) o (False, motivo) si no existe la orden.
    """
    try:
        ordenes = _leer_ordenes(raiz)
    except Exception as e:
        return (False, 'no se pudieron leer las ordenes: %s' % e)

    orden = _buscar_orden(ordenes, id)
    if orden is None:
        return (False, 'no existe la orden %s' % id)

    orden['estado'] = 'archivada'
    orden['nota'] = motivo

    try:
        _guardar_ordenes(raiz, ordenes)
    except Exception as e:
        return (False, 'no se pudo guardar: %s' % e)

    return (True, 'orden %s archivada' % id)
