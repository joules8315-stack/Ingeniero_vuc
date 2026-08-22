# -*- coding: utf-8 -*-
"""vigias/test_vigia_modo_ingeniero_siempre.py — SIEMPRE MODO INGENIERO.

Julio, 2026-08-21: "Haz pruebas, que siempre estes modo ingeniero."

Vigila que el modo ingeniero este SIEMPRE activo:
  1. Los hooks de modo_ingeniero estan puestos en el settings de Claude.
  2. No esta apagado por la variable INGENIERO_OFF.
  3. Hay un candado / modo que bloquea si no es ingeniero.

Si esta vigia se pone roja, es que alguien apago el modo ingeniero: hay que arreglarlo antes
de seguir, no se trabaja sin el.
"""
import sys, os, json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
SETTINGS = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")


def _settings():
    try:
        return json.load(open(SETTINGS, encoding="utf-8"))
    except Exception:
        return {}


def test_hooks_de_modo_ingeniero_puestos():
    """Los hooks del modo ingeniero deben estar en el settings de Claude."""
    s = json.dumps(_settings())
    assert "modo_ingeniero.py" in s, "faltan los hooks de modo_ingeniero en settings.json"


def test_no_apagado_por_variable():
    """INGENIERO_OFF no debe estar activo (si lo esta, el modo se apaga)."""
    assert not os.environ.get("INGENIERO_OFF", "").strip(), \
        "INGENIERO_OFF esta puesto: el modo ingeniero esta apagado"


def test_hay_algo_que_bloquea_sin_modo_ingeniero():
    """Debe haber un candado o el modo ingeniero enganchado para no escribir sin el."""
    s = json.dumps(_settings())
    assert ("modo_ingeniero" in s) or ("candado_ingeniero" in s), \
        "no hay nada que fuerce el modo ingeniero en settings.json"
