# -*- coding: utf-8 -*-
"""VIGIA — LEY L7: LAS PRUEBAS SON REALES, NO AUTOVALIDACION.

Julio, 2026-08-24: "que las pruebas playwright sean reales, no autovalidacion, eso no vale de nada."

Una prueba real ABRE el navegador y comprueba el comportamiento (page.goto, page.click, asserts
sobre lo que se ve). Una autovalidacion solo lee el codigo y dice "parece bien". Comprueba que las
pruebas de la casa son de verdad.
"""
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _archivos_py(raiz):
    salida = []
    for dp, dns, fns in os.walk(raiz):
        for f in fns:
            if f.endswith(".py"):
                salida.append(os.path.join(dp, f))
    return salida


def test_las_pruebas_playwright_abren_navegador_real():
    """Solo las pruebas que de verdad usan el navegador (sync_playwright) deben abrir pagina."""
    pruebas = [p for p in _archivos_py(AQUI)
               if os.path.basename(p).startswith("test_")
               and "sync_playwright" in open(p, encoding="utf-8", errors="ignore").read()]
    assert pruebas, "no hay ninguna prueba que use el navegador real"
    for p in pruebas:
        txt = open(p, encoding="utf-8", errors="ignore").read()
        assert "goto(" in txt or "page.goto" in txt, f"{p} usa playwright pero no abre pagina real"
