# -*- coding: utf-8 -*-
"""VIGIA — EL ROUTER INCLUYE LOS CONTRATOS NUEVOS (fix 2026-08-24).

El equipo (Cline y Claude) no podia construir un modulo nuevo porque el router solo metia en el
paquete los contratos ligados a flujos existentes; un contrato recien legislado no entraba, el
equipo no veia el material y (correctamente) no inventaba. Ahora el router tambien incluye los
contratos que HABLAN del problema. Esta vigia comprueba que un contrato nuevo entra al paquete.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)


def test_contrato_nuevo_entra_al_paquete():
    from cerebro import grafo, router
    if "dmm" not in grafo.proyectos():
        import pytest
        pytest.skip("dmm no esta")
    grafo.cargar("dmm", forzar=True)  # que el indice vea el archivo nuevo
    pk = router.armar(
        "dmm",
        "crear el modulo cuerpo/negocio.py segun CONTRATO_INTELIGENCIA_NEGOCIO roi ltv cac embudo forecast")
    leyes = [f["id"] for f in pk["leyes"]]
    assert any("INTELIGENCIA_NEGOCIO" in i for i in leyes), \
        "el contrato nuevo no entro al paquete: el equipo no lo va a ver"
