"""Candado de la puerta trasera (Julio, 2026-09-29).

Julio lo dijo asi: "cual puerta trasera abriste? Buscala". Se buscaron y eran dos,
las dos usadas por mi. Julio las confirmo y ordeno: "pon un candado que ni por el
putas se pueda abrir".

Puerta uno: un documento que vive dentro de un proyecto de Julio se puede escribir
a solas, sin que el equipo lo revise. Apuntada 189 veces hoy en memoria/SIN_EQUIPO.log
con el sello "DEJO PASAR: documento libre", dos de ellas a las 16:20 y a las 16:36.

Puerta dos: en vez de usar el comando, se importa una pieza por dentro y se ejecuta
su funcion, que hace lo mismo pero sin pasar por el portero, sin dejar rastro. Usada
unas quince veces hoy.

Este candado NO se puede apagar: no lee variables de entorno, no tiene banderas de
apagado, no tiene lista de permitidos, ni de excepciones, ni lista blanca. La unica
excepcion es reparar el propio arnes, y su motivo queda escrito aqui abajo.

La pieza es NUEVA y todavia no la llama nadie: engancharla donde pasan las demas va
en otra ronda, con su propia prueba.
"""

import os
import re


# ---------------------------------------------------------------------------
# Apunte del ultimo freno. Se guarda en memoria del modulo, no en disco, porque
# la pieza todavia no la llama nadie y no debe tocar nada del proyecto.
# ---------------------------------------------------------------------------
_ULTIMA_ANOTACION = None


# ---------------------------------------------------------------------------
# Palabras que marcan el veredicto del equipo. Se escriben aqui, en el codigo,
# porque son la unica llave que vale: la de Julio, con su motivo.
# ---------------------------------------------------------------------------
_PALABRA_APROBADO = "APROBADO"
_PALABRA_EQUIPO = "EQUIPO"


# ---------------------------------------------------------------------------
# Nombre de la carpeta del arnes. Es la UNICA excepcion que existe, y el motivo
# queda escrito aqui: si el candado se rompe, hay que poder arreglarlo. No hay
# ninguna otra excepcion, ni se anade despues.
# ---------------------------------------------------------------------------
_CARPETA_ARNES = "arnes"


def _quien_intenta():
    """Devuelve quien corre el programa, o 'desconocido' si no consta.

    Se toma de quien corre el programa. Si no consta, se escribe 'desconocido'
    en vez de inventar un nombre.
    """
    try:
        import getpass
        nombre = getpass.getuser()
        if nombre:
            return nombre
    except Exception:
        pass
    try:
        nombre = os.environ.get("USER") or os.environ.get("USERNAME")
        if nombre:
            return nombre
    except Exception:
        pass
    return "desconocido"


def _apuntar_freno(motivo, detalle=None):
    """Deja apuntado el intento de abrir la puerta trasera.

    El apunte es un diccionario y entre sus claves esta 'identidad', que dice
    quien intento la llamada. Se puede leer con ultima_anotacion().
    """
    global _ULTIMA_ANOTACION
    apunte = {
        "identidad": _quien_intenta(),
        "motivo": motivo,
    }
    if detalle is not None:
        apunte["detalle"] = detalle
    _ULTIMA_ANOTACION = apunte
    return apunte


def _leer_texto(ruta):
    """Lee el texto de un archivo. Devuelve None si no se puede leer.

    Nunca revienta: ante la duda se frena.
    """
    if ruta is None:
        return None
    if not isinstance(ruta, str):
        return None
    if not ruta.strip():
        return None
    try:
        if not os.path.isfile(ruta):
            return None
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def _vive_en_proyecto_de_julio(ruta):
    """Decide si la ruta vive dentro de un proyecto de Julio.

    Un documento vive dentro de un proyecto de Julio cuando esta dentro de una
    carpeta que no es la del propio arnes y que tiene pinta de proyecto: lleva
    un archivo de proyecto (PROYECTO.md, README.md, pyproject.toml, setup.py,
    .git, etc.) en su arbol de carpetas. Ante la duda se frena.
    """
    if ruta is None or not isinstance(ruta, str) or not ruta.strip():
        return False
    try:
        ruta_abs = os.path.abspath(ruta)
    except Exception:
        return False
    carpeta = os.path.dirname(ruta_abs)
    if not carpeta:
        return False
    # El propio arnes queda fuera de esta regla, por el motivo de abajo.
    partes = carpeta.replace("\\", "/").split("/")
    if _CARPETA_ARNES in partes:
        return False
    # Se sube por el arbol buscando marcas de proyecto de Julio.
    marcas = (
        "PROYECTO.md",
        "PROYECTO_SIN_VEREDICTO.md",
        "README.md",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "ingeniero.py",
    )
    actual = carpeta
    for _ in range(12):
        try:
            if not actual or actual == os.path.dirname(actual):
                break
            for marca in marcas:
                if os.path.exists(os.path.join(actual, marca)):
                    return True
            if os.path.isdir(os.path.join(actual, ".git")):
                return True
            actual = os.path.dirname(actual)
        except Exception:
            break
    return False


def _trae_veredicto_del_equipo(texto):
    """Decide si un texto trae veredicto del equipo.

    Un documento trae veredicto cuando su texto lleva escrita la palabra
    APROBADO junto con la palabra EQUIPO. Si no lleva las dos, no trae
    veredicto.
    """
    if texto is None or not isinstance(texto, str):
        return False
    tiene_aprobado = _PALABRA_APROBADO in texto
    tiene_equipo = _PALABRA_EQUIPO in texto
    return bool(tiene_aprobado and tiene_equipo)


def documento_de_proyecto_puede_pasar(ruta):
    """Devuelve False si el documento vive en un proyecto de Julio y no trae
    veredicto del equipo; True solo cuando si lo trae.

    Un documento trae veredicto cuando su texto lleva escrita la palabra
    APROBADO junto con la palabra EQUIPO. Si no lleva las dos, no trae
    veredicto.

    El unico sitio que queda fuera de esta regla es el propio arnes, por el
    motivo escrito arriba: si el candado se rompe, hay que poder arreglarlo.

    Nunca revienta: si la ruta no existe, esta vacia, es None o no se puede
    leer, devuelve False, porque ante la duda se frena.
    """
    if ruta is None or not isinstance(ruta, str) or not ruta.strip():
        return False
    try:
        if not os.path.isfile(ruta):
            return False
    except Exception:
        return False
    texto = _leer_texto(ruta)
    if texto is None:
        return False
    if _trae_veredicto_del_equipo(texto):
        return True
    if _vive_en_proyecto_de_julio(ruta):
        return False
    # Fuera de un proyecto de Julio no hay puerta que cerrar.
    return True


def _texto_importa_y_ejecuta_por_dentro(texto):
    """Decide si un texto de python importa una pieza y ademas ejecuta una
    funcion llamada registrar o cerrar sobre esa pieza.

    Se reconoce asi: en el texto aparece un import, y aparece una llamada que
    termina en punto seguido de registrar y un parentesis, o punto seguido de
    cerrar y un parentesis.
    """
    if texto is None or not isinstance(texto, str):
        return False
    if not re.search(r"^\s*(?:from\s+\S+\s+)?import\s+", texto, re.MULTILINE):
        return False
    if re.search(r"\.\s*registrar\s*\(", texto):
        return True
    if re.search(r"\.\s*cerrar\s*\(", texto):
        return True
    return False


def llamada_por_terminal_puede_pasar(comando, cwd):
    """Devuelve False cuando el archivo de python del comando, LEYENDO SU
    TEXTO, importa otra pieza y ademas ejecuta una funcion llamada registrar o
    una funcion llamada cerrar sobre esa pieza. Eso es entrar por dentro, y se
    frena.

    NO se ejecuta nada: solo se lee el texto del archivo. Prohibido lanzar
    procesos.

    Si no se puede leer el archivo, o el comando no trae un archivo de python,
    devuelve False, porque ante la duda se frena.

    Cada vez que frena, deja APUNTADO el intento, y ese apunte se puede leer
    con ultima_anotacion().
    """
    if not isinstance(comando, (list, tuple)) or len(comando) < 2:
        _apuntar_freno("comando sin archivo de python", detalle=repr(comando))
        return False
    programa = comando[0]
    archivo = comando[1]
    if not isinstance(archivo, str) or not archivo.strip():
        _apuntar_freno("comando sin archivo de python", detalle=repr(comando))
        return False
    if not archivo.endswith(".py"):
        _apuntar_freno("el comando no trae un archivo de python", detalle=archivo)
        return False
    ruta = archivo
    if not os.path.isabs(ruta):
        base = cwd if isinstance(cwd, str) and cwd.strip() else os.getcwd()
        ruta = os.path.join(base, ruta)
    texto = _leer_texto(ruta)
    if texto is None:
        _apuntar_freno("no se pudo leer el archivo del comando", detalle=ruta)
        return False
    if _texto_importa_y_ejecuta_por_dentro(texto):
        _apuntar_freno(
            "entra por dentro: importa una pieza y ejecuta registrar o cerrar",
            detalle={"programa": programa, "archivo": ruta},
        )
        return False
    return True


def reparar_archivo_del_arnes_puede_pasar(ruta):
    """Devuelve True solo si esa ruta es un archivo que YA EXISTE y que vive en
    una carpeta llamada arnes. Para cualquier otra ruta devuelve False.

    Esta es la UNICA excepcion que existe, y el motivo queda escrito dentro de
    la pieza: si el candado se rompe, hay que poder arreglarlo. No hay ninguna
    otra excepcion, ni se anade despues.
    """
    if ruta is None or not isinstance(ruta, str) or not ruta.strip():
        return False
    try:
        if not os.path.isfile(ruta):
            return False
        ruta_abs = os.path.abspath(ruta)
    except Exception:
        return False
    carpeta = os.path.dirname(ruta_abs)
    partes = carpeta.replace("\\", "/").split("/")
    return _CARPETA_ARNES in partes


def ultima_anotacion():
    """Devuelve el apunte del ultimo freno, o None si todavia no hubo ninguno.

    El apunte es un diccionario y entre sus claves esta, escrita asi, la clave
    identidad, que dice quien intento la llamada. Se toma de quien corre el
    programa, y si no consta se escribe 'desconocido' en vez de inventar un
    nombre.
    """
    return _ULTIMA_ANOTACION
