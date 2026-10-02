"""Vigia del contrato: EL INGENIERO ENTIENDE LO QUE JULIO QUIERE.

Metodo de Julio: la vigia se escribe primero y nace ROJA. Una vigia verde no probo nada.

Esta prueba:
  1. Exige que exista CONTRATO_EL_INGENIERO_ENTIENDE_LO_QUE_JULIO_QUIERE.md
  2. Exige que contenga las frases clave de la ley.
  3. Exige que cada archivo con extension que el contrato nombra exista en el proyecto
     o corresponda a una orden abierta en memoria/ORDENES.json.

Nace roja por un assert que falla (el contrato aun no existe), no por error de sintaxis.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
CONTRATO = RAIZ / "CONTRATO_EL_INGENIERO_ENTIENDE_LO_QUE_JULIO_QUIERE.md"
ORDENES = RAIZ / "memoria" / "ORDENES.json"


FRASES_OBLIGATORIAS = [
    "resultado esperado",
    "ontologia",
    "nace conectad",
    "candado",
    "memoria",
    "hora de apuntes",
    "programa antes que IA",
    "CONTRATO_TODO_ENCHUFADO_NADA_DORMIDO",
    "CONTRATO_MENOS_IA_MAS_PROGRAMA",
    "CONTRATO_LOS_CUATRO_OBJETIVOS_ORQUESTADOS",
    "CONTRATO_EL_FABRICANTE_DE_HABILIDADES",
]


PATRON_ARCHIVO = re.compile(r"[A-Za-z0-9_./\\-]+\.(?:py|md|json|txt|yaml|yml|toml|cfg|ini)")


def _leer_contrato() -> str:
    assert CONTRATO.exists(), (
        f"Falta el contrato: {CONTRATO}. "
        "La vigia nace roja porque el contrato aun no existe."
    )
    return CONTRATO.read_text(encoding="utf-8")


def _ordenes_abiertas() -> set[str]:
    """Devuelve el conjunto de rutas/archivos nombrados en ordenes abiertas."""
    if not ORDENES.exists():
        return set()
    try:
        datos = json.loads(ORDENES.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()

    abiertas: set[str] = set()

    def _recoger(valor) -> None:
        if isinstance(valor, str):
            abiertas.add(valor)
            abiertas.add(Path(valor).name)
        elif isinstance(valor, dict):
            for v in valor.values():
                _recoger(v)
        elif isinstance(valor, list):
            for v in valor:
                _recoger(v)

    _recoger(datos)
    return abiertas


def _archivos_nombrados(texto: str) -> set[str]:
    return set(PATRON_ARCHIVO.findall(texto))


def test_existe_el_contrato_del_ingeniero_que_entiende() -> None:
    assert CONTRATO.exists(), (
        f"No existe {CONTRATO.name}. "
        "El contrato que fija la ley del objetivo maximo debe estar escrito."
    )


def test_el_contrato_contiene_las_frases_de_la_ley() -> None:
    texto = _leer_contrato()
    faltan = [frase for frase in FRASES_OBLIGATORIAS if frase not in texto]
    assert not faltan, (
        "Al contrato le faltan frases obligatorias de la ley: " + ", ".join(faltan)
    )


def test_cada_archivo_nombrado_existe_o_es_orden_abierta() -> None:
    texto = _leer_contrato()
    nombrados = _archivos_nombrados(texto)
    assert nombrados, (
        "El contrato no nombra ningun archivo con extension; "
        "debe referenciar los archivos que la ley toca."
    )

    abiertas = _ordenes_abiertas()
    faltantes: list[str] = []
    for nombre in sorted(nombrados):
        candidato = RAIZ / nombre
        if candidato.exists():
            continue
        if nombre in abiertas or Path(nombre).name in abiertas:
            continue
        faltantes.append(nombre)

    assert not faltantes, (
        "El contrato nombra archivos que no existen en el proyecto "
        "ni figuran como orden abierta en memoria/ORDENES.json: "
        + ", ".join(faltantes)
    )
