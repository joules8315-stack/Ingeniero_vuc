"""Vigia: el contrato de que TODAS las IA trabajan por el canal.

Metodo de Julio: la vigia se escribe primero y nace ROJA. Una vigia verde
no probo nada. Esta prueba nace roja porque el contrato
CONTRATO_TODAS_LAS_IA_TRABAJAN_POR_EL_CANAL.md todavia no existe; cuando
exista y este bien escrito, pasa.

Lo que vigila:
  1. Que el contrato existe.
  2. Que contiene las palabras/frases exigidas por la ley.
  3. Que cada archivo que el contrato nombra con extension EXISTE en el
     proyecto, o corresponde a una orden abierta en memoria/ORDENES.json.

Leccion del rechazo anterior: el regex de nombres de archivo se comia
'Grok 4.7' y '1.E' de cualquier lista numerada como si fueran archivos
inexistentes. Por eso aqui la extension DEBE empezar por letra.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Raiz del proyecto y rutas clave
# ---------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
CONTRATO = RAIZ / "CONTRATO_TODAS_LAS_IA_TRABAJAN_POR_EL_CANAL.md"
ORDENES = RAIZ / "memoria" / "ORDENES.json"


# ---------------------------------------------------------------------------
# Frases que la ley exige dentro del contrato
# ---------------------------------------------------------------------------

FRASES_EXIGIDAS = [
    "Codex",
    "Big Pickle",
    "Grok 4.7",
    "canal",
    "objetivo",
    "resultado esperado",
    "cuaderno",
    "CONTRATO_ATENTO_AL_CANAL",
]


# ---------------------------------------------------------------------------
# Regex de nombres de archivo con extension.
#
# CLAVE (el fallo que hay que no repetir): la extension tiene que EMPEZAR
# POR LETRA. Asi 'Grok 4.7' NO casa (el '7' no es letra) y '1.E' tampoco
# (el 'E' va precedido de un punto pero el nombre '1' es solo digito y la
# extension 'E' es una sola letra mayuscula suelta; ademas exigimos que el
# nombre base tenga al menos una letra).
#
# Reglas:
#   - nombre base: al menos una letra, luego letras/digitos/._-
#   - extension: empieza por letra, sigue con letras/digitos, 1 a 8 chars
#   - no pegamos a caracteres de palabra por delante (evita 'x.py' dentro
#     de 'foox.py')
# ---------------------------------------------------------------------------

RE_ARCHIVO = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"([A-Za-z][A-Za-z0-9._-]*)"
    r"\."
    r"([A-Za-z][A-Za-z0-9]{0,7})"
    r"(?![A-Za-z0-9_])"
)


# Extensiones que consideramos "archivo del proyecto". Asi evitamos que
# cosas como 'Grok 4.7' o '1.E' (que ya no casan por el regex) o numeros
# de version tipo 'v1.2' se cuelen como archivos.
EXTENSIONES_VALIDAS = {
    "py", "md", "json", "txt", "yml", "yaml", "toml", "cfg", "ini",
    "csv", "tsv", "html", "css", "js", "ts", "sh", "bat", "ps1",
    "sql", "xml", "log", "rst", "env",
}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _leer_contrato() -> str:
    """Lee el contrato. Si no existe, devuelve cadena vacia (la prueba
    fallara en el assert de existencia, que es lo que queremos: nacer roja
    por un assert, no por un error de sintaxis)."""
    if not CONTRATO.exists():
        return ""
    return CONTRATO.read_text(encoding="utf-8", errors="replace")


def _ordenes_abiertas() -> set[str]:
    """Devuelve el conjunto de rutas/archivos que aparecen en ordenes
    abiertas de memoria/ORDENES.json. Si el archivo no existe o no se puede
    leer, devuelve conjunto vacio (no rompemos la prueba por eso)."""
    if not ORDENES.exists():
        return set()
    try:
        datos = json.loads(ORDENES.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return set()

    abiertas: set[str] = set()

    def _recoger(obj) -> None:
        if isinstance(obj, dict):
            # Solo miramos ordenes que no esten cerradas.
            estado = str(obj.get("estado", obj.get("status", ""))).lower()
            cerrada = estado in {"cerrada", "cerrado", "hecha", "hecho", "done", "closed"}
            if not cerrada:
                for clave in ("archivo", "archivos", "ruta", "rutas", "path", "paths"):
                    valor = obj.get(clave)
                    if isinstance(valor, str):
                        abiertas.add(valor)
                    elif isinstance(valor, list):
                        for v in valor:
                            if isinstance(v, str):
                                abiertas.add(v)
            for v in obj.values():
                _recoger(v)
        elif isinstance(obj, list):
            for v in obj:
                _recoger(v)

    _recoger(datos)
    return abiertas


def _normalizar(ruta: str) -> str:
    """Normaliza separadores para comparar rutas de forma robusta."""
    return ruta.replace("\\", "/").strip().lstrip("./")


def _archivos_nombrados(texto: str) -> set[str]:
    """Extrae los nombres de archivo con extension que el contrato nombra.

    Aplica el regex corregido (extension empieza por letra) y filtra por
    extensiones conocidas del proyecto.
    """
    encontrados: set[str] = set()
    for m in RE_ARCHIVO.finditer(texto):
        nombre = m.group(1)
        ext = m.group(2).lower()
        if ext not in EXTENSIONES_VALIDAS:
            continue
        # Descartar cosas que son claramente numeros de version o similares:
        # el nombre base debe tener al menos una letra (ya lo garantiza el
        # regex) y no debe ser solo digitos con puntos.
        if not re.search(r"[A-Za-z]", nombre):
            continue
        encontrados.add(f"{nombre}.{m.group(2)}")
    return encontrados


# ---------------------------------------------------------------------------
# Pruebas
# ---------------------------------------------------------------------------

def test_el_contrato_existe() -> None:
    """El contrato tiene que existir. Esta es la prueba que NACE ROJA:
    mientras el contrato no exista, este assert falla (no es un error de
    sintaxis, es un assert que falla)."""
    assert CONTRATO.exists(), (
        f"Falta el contrato {CONTRATO.name}. La ley manda que en cada trabajo "
        f"se puede pedir ayuda a Codex, Big Pickle y Grok 4.7 (y a las demas IA) "
        f"por el canal, diciendoles el objetivo. Escribe el contrato y esta vigia "
        f"se pondra verde."
    )


def test_el_contrato_contiene_las_frases_exigidas() -> None:
    """El contrato tiene que contener, literalmente, las frases de la ley."""
    texto = _leer_contrato()
    faltan = [frase for frase in FRASES_EXIGIDAS if frase not in texto]
    assert not faltan, (
        f"Al contrato {CONTRATO.name} le faltan estas frases exigidas por la ley: "
        f"{faltan}"
    )


def test_los_archivos_que_nombra_el_contrato_existen_o_son_ordenes_abiertas() -> None:
    """Cada archivo con extension que el contrato nombra tiene que existir en
    el proyecto, o corresponder a una orden abierta en memoria/ORDENES.json.

    El regex exige que la extension empiece por letra, asi que 'Grok 4.7' y
    '1.E' NO se cuelan como archivos inexistentes.
    """
    texto = _leer_contrato()
    nombrados = _archivos_nombrados(texto)
    abiertas = {_normalizar(o) for o in _ordenes_abiertas()}

    faltantes: list[str] = []
    for nombre in sorted(nombrados):
        # 1) Existe en la raiz del proyecto.
        if (RAIZ / nombre).exists():
            continue
        # 2) Existe en algun subdirectorio conocido del proyecto.
        if any(RAIZ.rglob(nombre)):
            continue
        # 3) Corresponde a una orden abierta.
        if _normalizar(nombre) in abiertas:
            continue
        if any(_normalizar(nombre).endswith(a) or a.endswith(_normalizar(nombre)) for a in abiertas):
            continue
        faltantes.append(nombre)

    assert not faltantes, (
        f"El contrato {CONTRATO.name} nombra archivos que no existen en el "
        f"proyecto ni constan como orden abierta en memoria/ORDENES.json: "
        f"{faltantes}"
    )


def test_el_regex_no_se_come_grok_ni_listas_numeradas() -> None:
    """Prueba de la prueba: el regex de nombres de archivo NO debe casar
    'Grok 4.7' ni '1.E' de una lista numerada. Este es el fallo que provoco
    el rechazo anterior; aqui queda clavado para que no vuelva."""
    # 'Grok 4.7' no es un archivo: el '7' no empieza por letra.
    assert _archivos_nombrados("pedir ayuda a Grok 4.7 por el canal") == set()
    # '1.E' de una lista numerada tampoco.
    assert _archivos_nombrados("1.E algo\n2.F otra cosa") == set()
    # Pero un archivo de verdad SI casa.
    assert "cuerpo/codex.py" in _archivos_nombrados("revisar cuerpo/codex.py") or \
           "codex.py" in _archivos_nombrados("revisar cuerpo/codex.py")
    # Y un .md de verdad tambien.
    assert "CONTRATO_ATENTO_AL_CANAL.md" in _archivos_nombrados(
        "ver CONTRATO_ATENTO_AL_CANAL.md"
    )
