# -*- coding: utf-8 -*-
"""VIGIA 4 — CROSS-FLOW: el paquete debe decir A QUIEN SE PUEDE DANAR.

Ley 4 de Julio: "no reparar algo y danar lo otro". Si el paquete no avisa de los vecinos,
la IA repara a ciegas y rompe el de al lado. Eso ya paso en Foto Informe.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import router, grafo


def _hay(a):
    p = grafo.proyectos()
    return a in p and os.path.isdir(p[a]["ruta"])


def test_el_paquete_trae_la_seccion_de_dano():
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    txt = router.a_texto(router.armar("dmm", "el onboarding no guarda el perfil"))
    assert "A QUIEN PUEDE DANAR" in txt


def test_una_pieza_muy_usada_avisa_de_sus_vecinos():
    """cuerpo/perfil.py lo importan 10 modulos. Tocarlo sin avisar es una bomba."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    pk = router.armar("dmm", "el onboarding no guarda el perfil")
    assert pk["dana"], "perfil.py lo usa medio proyecto y el paquete no aviso de ningun vecino"
    piezas = {d[0] for d in pk["dana"]}
    assert any(p.startswith("cuerpo/") for p in piezas), f"vecinos raros: {piezas}"


def test_los_vecinos_existen_de_verdad():
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    g = grafo.cargar("dmm")
    ids = {p["id"] for p in g["piezas"]}
    pk = router.armar("dmm", "el onboarding no guarda el perfil")
    for pieza, por, de in pk["dana"]:
        assert pieza in ids, f"aviso de danar {pieza}, que no existe"
        assert por in ("IMPORTA", "VIGILA"), f"tipo de dano raro: {por}"
