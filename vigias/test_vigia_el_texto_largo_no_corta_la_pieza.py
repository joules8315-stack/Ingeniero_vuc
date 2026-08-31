# -*- coding: utf-8 -*-
"""VIGIA — UN TEXTO LARGO DENTRO DE UNA PIEZA NO LA PARTE POR LA MITAD.

FALLO REAL, cazado el 2026-08-31 usando la propia herramienta reparada ese dia:

  Se pidio la pieza `_prompt_obrero` por su nombre y llego de 2 renglones, cuando mide 40.
  Motivo: esa pieza es casi toda un TEXTO LARGO entre comillas triples, y los renglones de ese
  texto empiezan en la columna cero. La regla decia "un renglon en columna cero termina la
  pieza", asi que la corto en el primer renglon del texto.

  Es el MISMO dano que se venia a reparar: entregar la pieza partida. Solo que ahora por otro
  motivo. Por eso se mide aparte.

LO QUE SE MIDE
  1. Una pieza que lleva dentro un texto largo pegado al margen llega ENTERA.
  2. La pieza siguiente NO se cuela dentro.
  3. Y sobre el codigo de verdad: las piezas que son casi todo texto llegan enteras.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from cerebro import piezas   # noqa: E402

# Una pieza con un texto largo pegado al margen, igual que los encargos de verdad.
CON_TEXTO_LARGO = '''# -*- coding: utf-8 -*-
"""Cabecera."""


def antes():
    return 1


def con_texto(algo):
    """Esta es la que se parte."""
    return f"""Hola, esto es un encargo largo.

REGLAS:
1. La primera regla, pegada al margen.
2. La segunda regla, tambien pegada al margen.

===== MATERIAL =====
{algo}
===== FIN ====="""


def despues():
    return "fin"
'''


@pytest.fixture
def archivo(tmp_path):
    p = tmp_path / "con_texto.py"
    p.write_text(CON_TEXTO_LARGO, encoding="utf-8")
    return str(p)


def test_la_pieza_con_texto_largo_llega_entera(archivo):
    """El fallo exacto: llegaba de 2 renglones cuando mide 12."""
    r = piezas.funcion_completa(archivo, "con_texto")
    assert r, "no encontro la pieza"
    t = r["texto"]
    assert "FIN =====" in t, (
        "la pieza llego CORTADA: el texto largo de dentro, al estar pegado al margen, se tomo "
        "por el final de la pieza. Es el mismo dano de entregar la pieza partida")
    assert r["hasta"] - r["desde"] >= 10, \
        "la pieza llego de %d renglones y mide mas de 10" % (r["hasta"] - r["desde"] + 1)


def test_no_se_cuela_la_pieza_siguiente(archivo):
    """Pasarse de largo es tan malo como quedarse corto: entonces se toca lo que no toca."""
    r = piezas.funcion_completa(archivo, "con_texto")
    assert "def despues" not in r["texto"], "se trajo tambien la pieza siguiente"
    assert "def antes" not in r["texto"], "se trajo tambien la pieza anterior"


def test_sobre_el_codigo_de_verdad_el_encargo_del_obrero_llega_entero():
    """El caso que lo destapo, sobre el archivo real."""
    ruta = os.path.join(AQUI, "cuerpo", "obrero.py")
    r = piezas.funcion_completa(ruta, "_prompt_obrero")
    assert r, "no encuentra el encargo del obrero"
    assert r["hasta"] - r["desde"] >= 20, (
        "el encargo del obrero llego de %d renglones. Mide mas de 20: esta llegando partido, "
        "y con un pedazo asi el equipo no puede aprobar nada"
        % (r["hasta"] - r["desde"] + 1))
    assert "FIN DEL MATERIAL" in r["texto"], "llego cortado antes del final"
