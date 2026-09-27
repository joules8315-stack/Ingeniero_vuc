# -*- coding: utf-8 -*-
"""Memoria de pruebas: apunta el resultado de una corrida y lo reusa si nada cambio.

De que nace
-----------
La misma prueba se corre hasta cuatro veces en un mismo trabajo (el juez de
la prueba, el capataz y el guardia), y cada corrida cuesta minutos. Esta pieza
permite apuntar el resultado de una corrida y reusarlo mientras NADA haya
cambiado, para no repetir la misma corrida.

La huella cambia en cuanto se toca cualquier .py del proyecto
-------------------------------------------------------------
La huella se calcula sobre la lista de objetivos ordenada y sobre el estado
de TODOS los archivos .py que hay dentro de las carpetas ``arnes``, ``cuerpo``
y ``vigias`` de la raiz, mas los .py sueltos en la propia raiz. De cada
archivo entran su ruta relativa con barras normales, su tamano en bytes y su
fecha de modificacion en nanosegundos. Por eso la huella cambia en cuanto se
toca cualquier .py del proyecto: un resultado viejo NUNCA se reusa despues de
un cambio, y por eso reusar no puede dar por bueno algo roto.

Nunca lanza una excepcion hacia fuera
--------------------------------------
Todo va en try except. Ante cualquier duda se responde None o no se guarda
nada. Solo se usa la libreria estandar: os, json, hashlib y time.
"""

import hashlib
import json
import os
import time


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

#: Carpetas de la raiz cuyos .py entran en la huella.
CARPETAS_VIGILADAS = ('arnes', 'cuerpo', 'vigias')

#: Nombre de la carpeta donde vive el archivo de apuntes.
CARPETA_MEMORIA = 'memoria'

#: Nombre del archivo de apuntes.
ARCHIVO_MEMORIA = '.memoria_de_pruebas.json'

#: Cuantos apuntes se conservan como maximo.
MAXIMO_APUNTES = 200


# ---------------------------------------------------------------------------
# Utilidades internas
# ---------------------------------------------------------------------------

def _ruta_memoria(raiz):
    """Devuelve la ruta del archivo de apuntes dentro de la raiz."""
    return os.path.join(raiz, CARPETA_MEMORIA, ARCHIVO_MEMORIA)


def _normalizar(ruta):
    """Convierte una ruta a texto con barras normales."""
    return str(ruta).replace('\\', '/')


def _archivos_py(raiz):
    """Devuelve la lista de rutas absolutas de los .py que entran en la huella.

    Entran los .py que esten dentro de las carpetas arnes, cuerpo y vigias de
    la raiz, mas los .py que esten sueltos en la propia raiz. Las carpetas que
    no existan se saltan. Nunca lanza: ante cualquier duda devuelve lo que
    haya podido reunir.
    """
    encontrados = []

    # .py sueltos en la propia raiz
    try:
        for nombre in os.listdir(raiz):
            try:
                ruta = os.path.join(raiz, nombre)
                if os.path.isfile(ruta) and nombre.endswith('.py'):
                    encontrados.append(ruta)
            except Exception:
                continue
    except Exception:
        pass

    # .py dentro de las carpetas vigiladas
    for carpeta in CARPETAS_VIGILADAS:
        try:
            base = os.path.join(raiz, carpeta)
            if not os.path.isdir(base):
                continue
            for actual, _subcarpetas, archivos in os.walk(base):
                for nombre in archivos:
                    try:
                        if nombre.endswith('.py'):
                            encontrados.append(os.path.join(actual, nombre))
                    except Exception:
                        continue
        except Exception:
            continue

    return encontrados


def _estado_de_archivo(raiz, ruta):
    """Devuelve (ruta_relativa, tamano, mtime_ns) o None si no se puede leer."""
    try:
        datos = os.stat(ruta)
        relativa = os.path.relpath(ruta, raiz)
        return (_normalizar(relativa), int(datos.st_size), int(datos.st_mtime_ns))
    except Exception:
        return None


def _leer_apuntes(raiz):
    """Lee el archivo de apuntes. Devuelve un diccionario o None si no se puede."""
    try:
        ruta = _ruta_memoria(raiz)
        if not os.path.isfile(ruta):
            return None
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        if not isinstance(datos, dict):
            return None
        return datos
    except Exception:
        return None


def _recortar(apuntes):
    """Deja solo los MAXIMO_APUNTES mas nuevos por su campo cuando."""
    try:
        if len(apuntes) <= MAXIMO_APUNTES:
            return apuntes

        def _cuando(item):
            try:
                valor = item[1].get('cuando')
                if valor is None:
                    return float('-inf')
                return float(valor)
            except Exception:
                return float('-inf')

        ordenados = sorted(apuntes.items(), key=_cuando, reverse=True)
        return dict(ordenados[:MAXIMO_APUNTES])
    except Exception:
        return apuntes


# ---------------------------------------------------------------------------
# Funciones publicas
# ---------------------------------------------------------------------------

def huella(raiz, objetivos):
    """Devuelve el sha256 en hexadecimal del estado actual del proyecto.

    Se calcula sobre dos cosas:

    1. la lista de objetivos ordenada;
    2. el estado de todos los archivos .py que haya dentro de las carpetas
       arnes, cuerpo y vigias de la raiz, mas los .py sueltos en la propia
       raiz. De cada archivo entran su ruta relativa con barras normales, su
       tamano en bytes y su fecha de modificacion en nanosegundos, todo
       ordenado por ruta para que el resultado sea siempre el mismo.

    Las carpetas que no existan se saltan. Nunca lanza: ante cualquier duda
    devuelve None.
    """
    try:
        partes = []

        # 1. Objetivos ordenados
        try:
            lista_objetivos = sorted(str(o) for o in objetivos)
        except Exception:
            lista_objetivos = []
        partes.append('OBJETIVOS:' + '|'.join(lista_objetivos))

        # 2. Estado de los .py, ordenado por ruta relativa
        estados = []
        for ruta in _archivos_py(raiz):
            estado = _estado_de_archivo(raiz, ruta)
            if estado is not None:
                estados.append(estado)
        estados.sort(key=lambda e: e[0])

        for relativa, tamano, mtime_ns in estados:
            partes.append('%s|%d|%d' % (relativa, tamano, mtime_ns))

        texto = '\n'.join(partes)
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()
    except Exception:
        return None


def apuntar(raiz, objetivos, paso, detalle):
    """Guarda el resultado de una corrida en memoria/.memoria_de_pruebas.json.

    La clave es la huella de ahora y el valor es un diccionario con:

    - ``paso``: el valor recibido convertido a booleano;
    - ``detalle``: el valor recibido convertido a texto;
    - ``cuando``: ``time.time()``.

    Crea la carpeta memoria si falta. Si el archivo existe y se puede leer,
    conserva los apuntes que ya hubiera; si no se puede leer, empieza de cero.
    Para que no crezca sin fin, si hay mas de 200 apuntes deja solo los 200
    mas nuevos por su campo cuando. Nunca lanza: ante cualquier duda no guarda
    nada y devuelve None.
    """
    try:
        clave = huella(raiz, objetivos)
        if clave is None:
            return None

        apuntes = _leer_apuntes(raiz)
        if apuntes is None:
            apuntes = {}

        try:
            paso_bool = bool(paso)
        except Exception:
            paso_bool = False

        try:
            detalle_texto = str(detalle)
        except Exception:
            detalle_texto = ''

        apuntes[clave] = {
            'paso': paso_bool,
            'detalle': detalle_texto,
            'cuando': time.time(),
        }

        apuntes = _recortar(apuntes)

        carpeta = os.path.join(raiz, CARPETA_MEMORIA)
        try:
            os.makedirs(carpeta, exist_ok=True)
        except Exception:
            return None

        ruta = _ruta_memoria(raiz)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(apuntes, f, ensure_ascii=False, indent=2)

        return None
    except Exception:
        return None


def recordar(raiz, objetivos, ventana_segundos=1800):
    """Devuelve el apunte de la huella de ahora si sigue fresco, o None.

    Devuelve None si el archivo no existe, si no es un diccionario, si no hay
    apunte para la huella de ahora, si el apunte no trae cuando, o si
    ``time.time() - cuando`` es mayor que ``ventana_segundos``.

    En cualquier otro caso devuelve un diccionario con dos claves: ``paso`` y
    ``detalle``. Nunca lanza: ante cualquier duda devuelve None.
    """
    try:
        apuntes = _leer_apuntes(raiz)
        if apuntes is None:
            return None

        clave = huella(raiz, objetivos)
        if clave is None:
            return None

        apunte = apuntes.get(clave)
        if not isinstance(apunte, dict):
            return None

        cuando = apunte.get('cuando')
        if cuando is None:
            return None

        try:
            cuando_num = float(cuando)
        except Exception:
            return None

        try:
            ventana = float(ventana_segundos)
        except Exception:
            return None

        if (time.time() - cuando_num) > ventana:
            return None

        return {
            'paso': bool(apunte.get('paso')),
            'detalle': str(apunte.get('detalle', '')),
        }
    except Exception:
        return None
