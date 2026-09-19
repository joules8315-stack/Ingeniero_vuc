"""arnes/vecinas.py — Elige SOLO las vigias de la pieza tocada y sus vecinas.

Acuerdo A-37 de Julio, plan v4 punto 5.

Hoy cada guardado corre TODA la bateria de vigias (DMM ~10 min, y dos veces).
Esta pieza elige SOLO las vigias de la pieza tocada y sus vecinas.

Funcion publica:
    elegir(raiz) -> list | None

    None  = correr toda la carpeta vigias/ (bateria completa)
    list  = rutas (con barras /) de las vigias a correr; puede ser vacia
            si solo cambiaron documentos.

Reglas (en orden):
    1. Si INGENIERO_BATERIA_COMPLETA == '1' -> None.
    2. Archivos cambiados: 'git status --porcelain' en raiz. Preparados,
       sin preparar y nuevos. La ruta es lo que va despues de las 3 primeras
       columnas. En renombres 'a -> b' usar b. Barras /.
    3. Si alguno es conftest.py, pytest.ini, setup.cfg, pyproject.toml,
       o esta dentro de vigias/ y NO empieza por test_ (ayudantes de
       pruebas) -> None.
    4. seleccion = los que esten en vigias/ y empiecen por test_ y terminen
       en .py y existan.
    5. Por cada archivo cambiado de codigo (.py .js .html .css .sh) fuera de
       vigias/: su nombre sin extension (stem). Se agregan todas las
       vigias/test_*.py cuyo texto contenga ese stem como palabra
       (re.search con limites \b). Si un archivo de codigo cambiado no
       aparece en NINGUNA vigia -> None (no hay vecinas conocidas: se corre
       todo, por seguridad).
    6. Devuelve la lista ordenada sin repetidos.

Nunca lanza: ante cualquier error devuelve None.

Bloque __main__:
    python arnes/vecinas.py <raiz>
    imprime una ruta por renglon, o la palabra TODAS si es None,
    o nada si la lista esta vacia.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys


# --- Constantes ---------------------------------------------------------

_VAR_BATERIA_COMPLETA = "INGENIERO_BATERIA_COMPLETA"

# Archivos que, si cambian, obligan a correr toda la bateria.
_ARCHIVOS_QUE_OBLIGAN_TODAS = {
    "conftest.py",
    "pytest.ini",
    "setup.cfg",
    "pyproject.toml",
}

# Extensiones de codigo que disparan busqueda de vecinas.
_EXTENSIONES_CODIGO = (".py", ".js", ".html", ".css", ".sh")

# Carpeta de vigias (relativa a la raiz).
_CARPETA_VIGIAS = "vigias"


# --- Utilidades ---------------------------------------------------------


def _a_barras(ruta: str) -> str:
    """Normaliza separadores a '/'."""
    return ruta.replace("\\", "/")


def _es_vigia_test(nombre: str) -> bool:
    """True si el nombre de archivo es una vigia de prueba."""
    return nombre.startswith("test_") and nombre.endswith(".py")


def _dentro_de_vigias(ruta: str) -> bool:
    """True si la ruta (con barras /) esta dentro de vigias/."""
    return ruta == _CARPETA_VIGIAS or ruta.startswith(_CARPETA_VIGIAS + "/")


def _es_archivo_de_codigo(ruta: str) -> bool:
    """True si la ruta termina en una extension de codigo vigilada."""
    return ruta.endswith(_EXTENSIONES_CODIGO)


def _stem(ruta: str) -> str:
    """Nombre sin extension del ultimo tramo de la ruta."""
    base = ruta.rsplit("/", 1)[-1]
    if "." in base:
        base = base.rsplit(".", 1)[0]
    return base


def _leer_texto(ruta_abs: str) -> str:
    """Lee un archivo de texto; devuelve '' si no se puede."""
    try:
        with open(ruta_abs, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def _contiene_palabra(texto: str, palabra: str) -> bool:
    """True si 'palabra' aparece como palabra completa en 'texto'."""
    if not palabra:
        return False
    try:
        patron = r"\b" + re.escape(palabra) + r"\b"
        return re.search(patron, texto) is not None
    except re.error:
        return False


# --- Git ----------------------------------------------------------------


def _archivos_cambiados(raiz: str) -> list[str]:
    """Devuelve las rutas cambiadas segun 'git status --porcelain'.

    Incluye preparados, sin preparar y nuevos. En renombres 'a -> b' usa b.
    Las rutas van con barras '/'. Lanza si git falla (el llamador captura).
    """
    resultado = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=raiz,
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
        timeout=60,
    )
    if resultado.returncode != 0:
        raise RuntimeError(
            "git status --porcelain fallo con codigo %s" % resultado.returncode
        )

    cambiados: list[str] = []
    for linea in resultado.stdout.splitlines():
        if not linea.strip():
            continue
        # Las 3 primeras columnas son el estado (XY + espacio).
        # La ruta empieza en la columna 3 (indice 3).
        if len(linea) <= 3:
            continue
        resto = linea[3:].strip()
        if not resto:
            continue
        # Renombres: 'a -> b' -> usar b.
        if " -> " in resto:
            resto = resto.split(" -> ", 1)[1].strip()
        # Quitar comillas si git las puso (rutas con espacios raros).
        if len(resto) >= 2 and resto[0] == '"' and resto[-1] == '"':
            resto = resto[1:-1]
        cambiados.append(_a_barras(resto))
    return cambiados


# --- Reglas de seguridad ------------------------------------------------


def _obliga_bateria_completa(cambiados: list[str]) -> bool:
    """True si algun cambio obliga a correr toda la bateria."""
    for ruta in cambiados:
        nombre = ruta.rsplit("/", 1)[-1]
        if nombre in _ARCHIVOS_QUE_OBLIGAN_TODAS:
            return True
        if _dentro_de_vigias(ruta):
            # Dentro de vigias/: solo las test_*.py son vigias normales.
            # Cualquier otro archivo (ayudante de pruebas) obliga a todas.
            if not nombre.startswith("test_"):
                return True
    return False


# --- Seleccion ----------------------------------------------------------


def _vigias_existentes(raiz: str) -> list[str]:
    """Lista de vigias/test_*.py existentes, con barras '/'."""
    carpeta = os.path.join(raiz, _CARPETA_VIGIAS)
    if not os.path.isdir(carpeta):
        return []
    vigias: list[str] = []
    try:
        for nombre in os.listdir(carpeta):
            if not _es_vigia_test(nombre):
                continue
            ruta_abs = os.path.join(carpeta, nombre)
            if os.path.isfile(ruta_abs):
                vigias.append(_CARPETA_VIGIAS + "/" + nombre)
    except OSError:
        return []
    return vigias


def _seleccion_directa(cambiados: list[str], raiz: str) -> list[str]:
    """Vigias cambiadas directamente (paso 4)."""
    seleccion: list[str] = []
    for ruta in cambiados:
        if not _dentro_de_vigias(ruta):
            continue
        nombre = ruta.rsplit("/", 1)[-1]
        if not _es_vigia_test(nombre):
            continue
        ruta_abs = os.path.join(raiz, ruta.replace("/", os.sep))
        if os.path.isfile(ruta_abs):
            seleccion.append(ruta)
    return seleccion


def _vecinas_por_stem(
    cambiados: list[str], raiz: str, vigias: list[str]
) -> list[str] | None:
    """Vigias que mencionan el stem de cada archivo de codigo cambiado.

    Devuelve None si algun archivo de codigo cambiado (fuera de vigias/)
    no aparece en NINGUNA vigia: no hay vecinas conocidas, se corre todo.
    """
    # Cache de textos de vigias para no releer.
    textos: dict[str, str] = {}
    for v in vigias:
        ruta_abs = os.path.join(raiz, v.replace("/", os.sep))
        textos[v] = _leer_texto(ruta_abs)

    vecinas: list[str] = []
    for ruta in cambiados:
        if _dentro_de_vigias(ruta):
            continue
        if not _es_archivo_de_codigo(ruta):
            continue
        stem = _stem(ruta)
        if not stem:
            continue
        encontrada = False
        for v in vigias:
            if _contiene_palabra(textos.get(v, ""), stem):
                vecinas.append(v)
                encontrada = True
        if not encontrada:
            # Archivo de codigo cambiado sin vecinas conocidas:
            # por seguridad, se corre toda la bateria.
            return None
    return vecinas


# --- API publica --------------------------------------------------------


def elegir(raiz: str) -> list[str] | None:
    """Elige las vigias a correr para la pieza tocada y sus vecinas.

    Devuelve None para correr toda la carpeta vigias/, o una lista
    ordenada sin repetidos de rutas (con barras '/') de vigias a correr.
    Nunca lanza: ante cualquier error devuelve None.
    """
    try:
        # (1) Bateria completa forzada por variable de entorno.
        if os.environ.get(_VAR_BATERIA_COMPLETA) == "1":
            return None

        # (2) Archivos cambiados segun git.
        cambiados = _archivos_cambiados(raiz)

        # (3) Cambios que obligan a correr toda la bateria.
        if _obliga_bateria_completa(cambiados):
            return None

        # (4) Vigias cambiadas directamente.
        seleccion = _seleccion_directa(cambiados, raiz)

        # (5) Vecinas por stem de cada archivo de codigo cambiado.
        vigias = _vigias_existentes(raiz)
        vecinas = _vecinas_por_stem(cambiados, raiz, vigias)
        if vecinas is None:
            return None
        seleccion.extend(vecinas)

        # (6) Ordenada sin repetidos.
        return sorted(set(seleccion))
    except Exception:
        # Nunca lanza: ante cualquier error, bateria completa.
        return None


# --- Bloque __main__ ----------------------------------------------------


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write("uso: python arnes/vecinas.py <raiz>\n")
        return 2
    raiz = argv[1]
    resultado = elegir(raiz)
    if resultado is None:
        print("TODAS")
        return 0
    for ruta in resultado:
        print(ruta)
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
