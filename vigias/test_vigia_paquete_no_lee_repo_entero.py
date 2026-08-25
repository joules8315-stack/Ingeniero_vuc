# -*- coding: utf-8 -*-
"""VIGIA 1 — EL PAQUETE NO PUEDE SER EL REPO ENTERO.

Es la vigia que no existia en ninguna de las 190 del proyecto: ninguna miraba el GASTO.
Si el router empieza a meter archivos enteros, esta se pone ROJA y se nota antes de pagar.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import router, grafo

TOPE = 800          # un paquete mas largo que esto ya no es un paquete
AHORRO_MINIMO = 90  # por ciento


def _casos():
    prs = grafo.proyectos()
    out = []
    if "dmm" in prs and os.path.isdir(prs["dmm"]["ruta"]):
        out += [("dmm", "el onboarding no guarda el perfil de la empresa"),
                ("dmm", "los precios no se actualizan en la web")]
    if "foto_informe" in prs and os.path.isdir(prs["foto_informe"]["ruta"]):
        out += [("foto_informe", "la plantilla no persiste al cambiar de sesion")]
    return out


@pytest.mark.parametrize("apodo,problema", _casos())
def test_el_paquete_cabe_en_un_paquete(apodo, problema):
    txt = router.a_texto(router.armar(apodo, problema))
    n = len(txt.splitlines())
    assert n <= TOPE, f"el paquete de '{problema}' trae {n} lineas (tope {TOPE}): esta releyendo el repo"


@pytest.mark.parametrize("apodo,problema", _casos())
def test_ahorra_de_verdad(apodo, problema):
    pk = router.armar(apodo, problema)
    n = len(router.a_texto(pk).splitlines())
    ahorro = 100 - n * 100 / max(1, pk["total_proyecto"])
    assert ahorro >= AHORRO_MINIMO, f"solo ahorra {ahorro:.1f}% en '{problema}' (minimo {AHORRO_MINIMO}%)"


@pytest.mark.parametrize("apodo,problema", _casos())
def test_ningun_trozo_es_un_archivo_entero(apodo, problema):
    """Un trozo debe ser un PEDAZO. Si un trozo abarca todo el archivo, es leer entero disfrazado."""
    pk = router.armar(apodo, problema)
    fichas = {f["id"]: f for f in pk["fichas"]}
    for t in pk["trozos"]:
        f = fichas.get(t["pieza"])
        if not f or f["lineas"] <= 60:
            continue
        abarca = (t["hasta"] - t["desde"] + 1) / f["lineas"]
        assert abarca < 0.5, f"el trozo {t['direccion']} abarca {abarca:.0%} de {t['pieza']}"
