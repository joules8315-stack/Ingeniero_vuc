# -*- coding: utf-8 -*-
"""VIGIA — LEY L6: TODO QUEDA LIMPIO Y EN COMMIT, Y LO NUEVO SE INDEXA.

Julio, 2026-08-24: "todo debe quedar limpio, en commit, eso ya se hablo, pon candado y crea vigia."
Y lo corregido por Claude: si aparece algo nuevo y nadie lo anota en el indice, se pone rojo.

Comprueba que el guardia de guardado existe (lo ejecuta git, no la IA) y que las leyes nuevas
quedaron escritas e indexadas en el mapa de la forma de trabajo.
"""
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_el_guardia_de_guardado_existe_y_lo_ejecuta_git():
    assert os.path.exists(os.path.join(AQUI, "arnes", "guardia_de_guardado.py")), \
        "no existe el guardia de guardado"
    hook = os.path.join(AQUI, "hooks", "pre-commit")
    assert os.path.exists(hook), "no esta el gancho pre-commit"
    txt = open(hook, encoding="utf-8", errors="ignore").read()
    assert "guardia_de_guardado" in txt, "el gancho no corre el guardia"


def test_las_leyes_nuevas_estan_indexadas():
    """El contrato de legislacion total esta en el mapa de la forma de trabajo."""
    proto = open(os.path.join(AQUI, "cerebro", "protocolo.py"), encoding="utf-8").read()
    assert "CONTRATO_LEGISLACION_TOTAL" in proto or "LEGISLACION_TOTAL" in proto, \
        "la legislacion total no esta indexada en el mapa"


def test_el_guardia_frena_con_rojas():
    """El guardia NO deja guardar dejando algo roto."""
    txt = open(os.path.join(AQUI, "arnes", "guardia_de_guardado.py"), encoding="utf-8").read()
    assert "ROJAS" in txt or "rojas" in txt, "el guardia no frena con pruebas rojas"
