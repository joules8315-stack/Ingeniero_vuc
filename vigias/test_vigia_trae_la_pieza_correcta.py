# -*- coding: utf-8 -*-
"""VIGIA 2 — TRAE LA PIEZA CORRECTA, NO CUALQUIERA.

Ahorrar tokens trayendo basura no es ahorrar: es fallar barato.
Cada caso dice que pieza TIENE que venir y cual NO debe venir.
Los casos salen de fallos REALES vistos el 2026-08-20 (el login colandose en un problema
de plantilla, por la palabra "sesion").
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import router, grafo

CASOS = [
    ("dmm", "el onboarding asesorado no guarda el perfil de la empresa",
     ["cuerpo/perfil.py"], ["cuerpo/precios.py", "cuerpo/whatsapp.py"]),
    ("dmm", "la lista de precios no reemplaza a la anterior",
     ["cuerpo/precios.py"], ["cuerpo/perfil.py"]),
]


def _hay(apodo):
    prs = grafo.proyectos()
    return apodo in prs and os.path.isdir(prs[apodo]["ruta"])


@pytest.mark.parametrize("apodo,problema,deben,no_deben", CASOS)
def test_trae_lo_que_debe(apodo, problema, deben, no_deben):
    if not _hay(apodo):
        pytest.skip(f"{apodo} no esta en esta maquina")
    pk = router.armar(apodo, problema)
    traidas = {f["id"] for f in pk["codigo"]}
    for d in deben:
        assert d in traidas, f"'{problema}' NO trajo {d}. Trajo: {sorted(traidas)}"


@pytest.mark.parametrize("apodo,problema,deben,no_deben", CASOS)
def test_no_trae_lo_ajeno(apodo, problema, deben, no_deben):
    if not _hay(apodo):
        pytest.skip(f"{apodo} no esta en esta maquina")
    pk = router.armar(apodo, problema)
    traidas = {f["id"] for f in pk["codigo"]}
    for n in no_deben:
        assert n not in traidas, f"'{problema}' trajo {n}, que no tiene nada que ver"


@pytest.mark.parametrize("apodo,problema,deben,no_deben", CASOS)
def test_trae_la_ley_de_ese_asunto(apodo, problema, deben, no_deben):
    """Debe traer el contrato DUENO del asunto, no el mapa general que nombra todo."""
    if not _hay(apodo):
        pytest.skip(f"{apodo} no esta en esta maquina")
    pk = router.armar(apodo, problema)
    leyes = " ".join(f["id"].upper() for f in pk["leyes"])
    assert "CONTRATO" in leyes, f"'{problema}' no trajo ningun contrato"
