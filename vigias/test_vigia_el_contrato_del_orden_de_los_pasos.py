"""Vigia del contrato: EL ORDEN DE LOS PASOS LO IMPONE EL PROGRAMA.

Metodo de Julio: la vigia se escribe primero y nace ROJA. Una vigia verde no
probo nada. Esta prueba debe fallar por un assert (el contrato aun no existe),
nunca por un error de sintaxis, y pasar cuando el contrato este bien escrito.

Que vigila:
  1. Que existe CONTRATO_EL_ORDEN_DE_LOS_PASOS_LO_IMPONE_EL_PROGRAMA.md
  2. Que contiene las frases exigidas por la tarea.
  3. Que cada archivo con extension que el contrato nombra existe en el proyecto
     o corresponde a una orden abierta en memoria/ORDENES.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Raiz del proyecto: este archivo vive en <raiz>/vigias/, asi que la raiz es
# el padre del directorio que contiene a este archivo.
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent

CONTRATO = RAIZ / "CONTRATO_EL_ORDEN_DE_LOS_PASOS_LO_IMPONE_EL_PROGRAMA.md"
ORDENES = RAIZ / "memoria" / "ORDENES.json"

# Frases que la tarea exige que aparezcan en el contrato.
FRASES_EXIGIDAS = [
    "que cada uno abra el otro",
    "no dependa de tu memoria",
    "depende",
    "PLAN_DE_PASOS.json",
    "CONTRATO_EL_PLAN_SE_SIGUE",
    "camino_sano",
]

# Extensiones que cuentan como "archivo nombrado" por el contrato.
EXTENSIONES = (
    ".py",
    ".md",
    ".json",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".cfg",
    ".ini",
    ".sh",
    ".bat",
    ".ps1",
)

# Patron para extraer rutas/archivos con extension del texto del contrato.
PATRON_ARCHIVO = re.compile(
    r"[A-Za-z0-9_./\\-]+\.(?:py|md|json|txt|yaml|yml|toml|cfg|ini|sh|bat|ps1)"
)


def _leer_contrato() -> str:
    """Devuelve el texto del contrato. Falla con assert si no existe."""
    assert CONTRATO.exists(), (
        f"Falta el contrato: {CONTRATO}. "
        "La vigia nace ROJA a proposito: el contrato aun no existe."
    )
    return CONTRATO.read_text(encoding="utf-8")


def _cargar_ordenes_abiertas() -> set[str]:
    """Devuelve el conjunto de rutas/archivos que aparecen en ORDENES.json.

    Si el archivo no existe o no se puede leer, devuelve conjunto vacio: la
    vigia no debe reventar por eso, solo dejar de tener esa via de escape.
    """
    if not ORDENES.exists():
        return set()
    try:
        datos = json.loads(ORDENES.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()

    encontrados: set[str] = set()

    def _recoger(obj) -> None:
        if isinstance(obj, dict):
            for valor in obj.values():
                _recoger(valor)
        elif isinstance(obj, list):
            for valor in obj:
                _recoger(valor)
        elif isinstance(obj, str):
            encontrados.add(obj)
            # tambien el nombre base, por si la orden guarda solo el archivo
            encontrados.add(Path(obj).name)

    _recoger(datos)
    return encontrados


def _normalizar(ruta: str) -> str:
    """Normaliza separadores para comparar rutas de forma estable."""
    return ruta.replace("\\", "/").strip()


def _archivos_nombrados(texto: str) -> set[str]:
    """Extrae del contrato los archivos con extension que nombra."""
    return {_normalizar(m) for m in PATRON_ARCHIVO.findall(texto)}


def _existe_en_proyecto(ruta: str) -> bool:
    """True si la ruta existe en el proyecto (absoluta o relativa a la raiz)."""
    candidata = Path(ruta)
    if candidata.is_absolute():
        return candidata.exists()
    return (RAIZ / candidata).exists()


def _esta_en_ordenes(ruta: str, ordenes: set[str]) -> bool:
    """True si la ruta (o su nombre base) figura en las ordenes abiertas."""
    normal = _normalizar(ruta)
    base = Path(normal).name
    for entrada in ordenes:
        entrada_norm = _normalizar(entrada)
        if entrada_norm == normal or entrada_norm == base:
            return True
        if entrada_norm.endswith("/" + normal) or entrada_norm.endswith("/" + base):
            return True
    return False


# ---------------------------------------------------------------------------
# PRUEBAS
# ---------------------------------------------------------------------------


def test_el_contrato_del_orden_de_los_pasos_existe() -> None:
    """El contrato tiene que existir. Esta es la prueba que nace ROJA."""
    assert CONTRATO.exists(), (
        f"Falta el contrato: {CONTRATO}. "
        "Sin contrato no hay ley que vigilar: la vigia nace roja a proposito."
    )


def test_el_contrato_contiene_las_frases_exigidas() -> None:
    """El contrato tiene que decir, con estas palabras, lo que la tarea exige."""
    texto = _leer_contrato()
    faltan = [frase for frase in FRASES_EXIGIDAS if frase not in texto]
    assert not faltan, (
        "Al contrato le faltan frases exigidas: " + ", ".join(repr(f) for f in faltan)
    )


def test_cada_archivo_nombrado_existe_o_es_orden_abierta() -> None:
    """Cada archivo con extension que el contrato nombra debe existir o ser orden."""
    texto = _leer_contrato()
    nombrados = _archivos_nombrados(texto)
    ordenes = _cargar_ordenes_abiertas()

    huerfanos = [
        ruta
        for ruta in sorted(nombrados)
        if not _existe_en_proyecto(ruta) and not _esta_en_ordenes(ruta, ordenes)
    ]

    assert not huerfanos, (
        "El contrato nombra archivos que no existen en el proyecto ni figuran "
        "como orden abierta en memoria/ORDENES.json: "
        + ", ".join(huerfanos)
    )


def test_el_contrato_habla_del_plan_de_pasos_y_del_camino_sano() -> None:
    """Refuerzo explicito: el plan de pasos y el camino sano tienen que estar."""
    texto = _leer_contrato()
    assert "PLAN_DE_PASOS.json" in texto, (
        "El contrato debe nombrar PLAN_DE_PASOS.json: el plan vive en un archivo, "
        "no en la memoria de nadie."
    )
    assert "camino_sano" in texto, (
        "El contrato debe nombrar 'camino_sano': el orden lo impone el programa."
    )
    assert "CONTRATO_EL_PLAN_SE_SIGUE" in texto, (
        "El contrato debe nombrar CONTRATO_EL_PLAN_SE_SIGUE: la ley que manda."
    )
