"""Vigia del CONTRATO_MENOS_IA_MAS_PROGRAMA.md.

Esta vigia no ejecuta ninguna habilidad. Solo hace cuentas sobre los archivos
de la carpeta skills/ y sobre el texto de cada uno. Tres pruebas:

  1. Ninguna habilidad IMPORTA un cerebro. Se mira con una expresion regular
     que casa solo con lineas de import o from que traigan cerebro, obrero,
     openai, google.generativeai o anthropic. Nombrar un cerebro en un texto
     o guardarlo como dato NO cuenta: eso seria una alarma que grita en falso.
  2. Las seis habilidades que la Regla 2 del contrato nombra siguen existiendo
     como archivo: cazar_el_humo, medir_al_equipo, via_unica,
     falta_en_el_material, frenos_con_culpable y orden_o_texto_pegado.
  3. Hay al menos tantas habilidades como esas seis. Un candado sobre una
     carpeta vacia siempre esta verde y no prueba nada.

Por que importa: una habilidad que llama a una IA deja de ser gratis, deja de
dar siempre el mismo resultado y se puede agotar. Es una cuenta, no un juicio.
"""

from __future__ import annotations

import re
from pathlib import Path


# --- Rutas ---------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_SKILLS = RAIZ / "skills"


# --- Las seis habilidades que nombra la Regla 2 del contrato --------------

HABILIDADES_DE_LA_REGLA_2 = (
    "cazar_el_humo",
    "medir_al_equipo",
    "via_unica",
    "falta_en_el_material",
    "frenos_con_culpable",
    "orden_o_texto_pegado",
)

MINIMO_DE_HABILIDADES = len(HABILIDADES_DE_LA_REGLA_2)


# --- La expresion regular que caza un IMPORT de cerebro ------------------
#
# Solo casa con lineas de import o from que traigan uno de los nombres
# prohibidos. No casa con menciones en comentarios, docstrings ni datos:
# para eso haria falta que la linea empiece por import o from.
#
# Nombres prohibidos: cerebro, obrero, openai, google.generativeai, anthropic.

NOMBRES_DE_CEREBRO = (
    r"cerebro",
    r"obrero",
    r"openai",
    r"google\.generativeai",
    r"anthropic",
)

# AGUJERO CAZADO SABOTEANDO, EL MISMO DIA QUE NACIO (2026-09-12).
#
# La primera version solo miraba DE DONDE se importa, no QUE se importa. Se le metio a proposito
# un "from cuerpo import cerebro" en una habilidad y LA VIGIA SIGUIO VERDE: el nombre prohibido
# iba al final y se le escapaba. Eso es un VERDE DE MENTIRA, justo lo que esta casa persigue, y
# no se habria visto nunca si no se llega a sabotear.
#
# LECCION: una vigia que nace verde no ha probado nada. Se le rompe lo que vigila a proposito y
# TIENE que ponerse roja; si no, no sirve.
#
# Ahora se mira la LINEA ENTERA de import: empieza por from o por import Y trae un nombre
# prohibido, este donde este. Sigue sin casar con comentarios ni con textos, porque la linea
# tiene que empezar por from o por import.
PATRON_IMPORT_DE_CEREBRO = re.compile(
    r"^[ \t]*(?:from|import)\b[^\n#]*\b(?:" + "|".join(NOMBRES_DE_CEREBRO) + r")\b",
    re.MULTILINE,
)


# --- Utilidades ----------------------------------------------------------

def _archivos_de_habilidades() -> list[Path]:
    """Devuelve los .py de la carpeta skills/, ordenados y sin duplicados."""
    if not CARPETA_SKILLS.is_dir():
        return []
    return sorted(p for p in CARPETA_SKILLS.glob("*.py") if p.is_file())


def _leer_texto(ruta: Path) -> str:
    """Lee un archivo como texto, sin reventar si tiene bytes raros."""
    try:
        return ruta.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _lineas_de_import_de_cerebro(texto: str) -> list[str]:
    """Devuelve las lineas del texto que son un import de cerebro."""
    return [m.group(0).strip() for m in PATRON_IMPORT_DE_CEREBRO.finditer(texto)]


# --- Prueba 1: ninguna habilidad importa un cerebro ----------------------

def test_ninguna_habilidad_importa_un_cerebro() -> None:
    """Ninguna habilidad de skills/ puede IMPORTAR un cerebro.

    Se mira con una expresion regular que casa solo con lineas de import o
    from que traigan cerebro, obrero, openai, google.generativeai o anthropic.
    Nombrar un cerebro en un texto o guardarlo como dato NO cuenta.

    Por que importa: una habilidad que llama a una IA deja de ser gratis,
    deja de dar siempre el mismo resultado y se puede agotar.
    """
    culpables: list[str] = []
    for ruta in _archivos_de_habilidades():
        texto = _leer_texto(ruta)
        for linea in _lineas_de_import_de_cerebro(texto):
            culpables.append(f"{ruta.name}: {linea}")

    assert not culpables, (
        "Estas habilidades IMPORTAN un cerebro, y no deben:\n  "
        + "\n  ".join(culpables)
        + "\n\nUna habilidad que llama a una IA deja de ser gratis, deja de dar "
        "siempre el mismo resultado y se puede agotar. "
        "Nombrar un cerebro en un texto o guardarlo como dato no es importar: "
        "eso no cuenta y no se senala aqui."
    )


# --- Prueba 2: las seis habilidades de la Regla 2 existen --------------

def test_las_seis_habilidades_de_la_regla_2_existen() -> None:
    """Las seis habilidades que nombra la Regla 2 siguen existiendo como archivo.

    Son cazar_el_humo, medir_al_equipo, via_unica, falta_en_el_material,
    frenos_con_culpable y orden_o_texto_pegado. Cada una salio de algo que
    costo tiempo o dinero de verdad.
    """
    faltan: list[str] = []
    for nombre in HABILIDADES_DE_LA_REGLA_2:
        ruta = CARPETA_SKILLS / f"{nombre}.py"
        if not ruta.is_file():
            faltan.append(f"{nombre}.py")

    assert not faltan, (
        "Faltan habilidades que la Regla 2 del contrato nombra:\n  "
        + "\n  ".join(faltan)
        + "\n\nCada una salio de algo que costo tiempo o dinero de verdad. "
        "Si desaparecen, el contrato queda sin lo que prometia."
    )


# --- Prueba 3: hay al menos tantas habilidades como las seis ------------

def test_hay_al_menos_tantas_habilidades_como_las_seis() -> None:
    """Hay al menos tantas habilidades como las seis de la Regla 2.

    Por que importa: un candado sobre una carpeta vacia siempre esta verde
    y no prueba nada.
    """
    archivos = _archivos_de_habilidades()
    cuantas = len(archivos)

    assert cuantas >= MINIMO_DE_HABILIDADES, (
        f"Solo hay {cuantas} habilidades en skills/, y hacen falta al menos "
        f"{MINIMO_DE_HABILIDADES}.\n\nUn candado sobre una carpeta vacia "
        "siempre esta verde y no prueba nada."
    )


# --- Permite correrlo a mano sin pytest ---------------------------------

if __name__ == "__main__":
    test_ninguna_habilidad_importa_un_cerebro()
    test_las_seis_habilidades_de_la_regla_2_existen()
    test_hay_al_menos_tantas_habilidades_como_las_seis()
    print("Vigia MENOS_IA_MAS_PROGRAMA: las tres pruebas pasan.")
