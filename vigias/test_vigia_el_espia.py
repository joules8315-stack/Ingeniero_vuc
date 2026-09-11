# -*- coding: utf-8 -*-
"""VIGIA — EL ESPIA: comprobar que una pieza esta enchufada EJECUTANDO, no leyendo.

LEY: CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO.md (Julio, 2026-09-09).

DE DONDE SALE: una vigia comprobaba que al cerebro solo le llegara lo suyo con
`assert "asignador" in ingeniero.py`. Buscaba LA PALABRA en todo el archivo. Como un camino si
lo llamaba, la palabra aparecia y la vigia se ponia VERDE. Pero el otro camino, `resolver`,
mandaba el paquete entero. Medido: se mandaron 7.575 letras y llegaron 35.845, no le cupo a
ningun gratis, contesto el de pago y se juzgo a si mismo. VERDE DE MENTIRA, y asi 21 veces.

QUE ES ESTO: la pieza que hace imposible ese verde falso. Pone un espia dentro de la pieza,
corre el camino DE VERDAD, y dice si la llamaron o no. No hay palabra que colar ni comentario
que engane: o se ejecuto o no se ejecuto.

POR QUE UNA SOLA PARA TODA LA CASA: si cada vigia se escribe su propio espia, en dos dias
vuelven a divergir. Es el mismo fallo con otra cara.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "vigias"))


def _espia():
    try:
        import _espia as mod
    except ImportError:
        pytest.fail(
            "NO EXISTE vigias/_espia.py. Sin el, cada vigia comprueba el enchufe leyendo texto, "
            "y un texto se puede colar sin querer: basta que la palabra aparezca en cualquier "
            "sitio del archivo para que la vigia se ponga verde mintiendo.")
    return mod


class _PiezaDeMentira:
    """Una pieza cualquiera, para probar el espia sin tocar nada de verdad."""

    def __init__(self):
        self.veces = 0

    def trabajar(self, algo):
        self.veces += 1
        return "hecho: " + str(algo)


def test_dice_que_si_cuando_el_camino_la_llama_de_verdad():
    """Lo que tiene que pasar cuando esta bien enchufada."""
    e = _espia()
    pieza = _PiezaDeMentira()
    with e.mirando(pieza, "trabajar") as ojo:
        pieza.trabajar("pan")          # esto es "correr el camino real"
    assert ojo.la_llamaron, (
        "EL ESPIA NO VIO UNA LLAMADA QUE SI OCURRIO. Si no ve lo que pasa delante, no sirve "
        "para nada y ademas daria rojos falsos, que es peor.")
    assert ojo.veces == 1, "conto mal las veces: dijo %s" % ojo.veces


def test_dice_que_no_cuando_nadie_la_llama():
    """Y lo que tiene que pasar cuando esta dormida: es para lo que existe."""
    e = _espia()
    pieza = _PiezaDeMentira()
    with e.mirando(pieza, "trabajar") as ojo:
        pass                            # el camino corre pero NO la usa
    assert not ojo.la_llamaron, (
        "EL ESPIA DIJO QUE LA LLAMARON Y NADIE LA LLAMO. Eso es exactamente el verde de mentira "
        "que esta pieza existe para hacer imposible.")


def test_no_rompe_la_pieza_que_vigila():
    """Vigilar no puede cambiar lo que la pieza hace, ni dejarla tocada despues."""
    e = _espia()
    pieza = _PiezaDeMentira()
    with e.mirando(pieza, "trabajar") as ojo:
        salida = pieza.trabajar("pan")
    assert salida == "hecho: pan", (
        "EL ESPIA CAMBIO LO QUE DEVUELVE LA PIEZA. Un espia que altera lo que vigila hace que "
        "la prueba mida otra cosa distinta de la real.")
    assert pieza.veces == 1, "la pieza no llego a hacer su trabajo de verdad"
    pieza.trabajar("otro")
    assert ojo.veces == 1, (
        "EL ESPIA SIGUE PEGADO DESPUES DE TERMINAR. Se quedaria contando llamadas de otras "
        "pruebas y ensuciaria los resultados de todas.")


def test_tambien_vale_para_una_funcion_suelta_de_un_modulo():
    """Casi todo en esta casa son funciones sueltas, no clases: tiene que valer para eso."""
    e = _espia()
    from cuerpo import cuotas
    with e.mirando(cuotas, "desperto") as ojo:
        cuotas.desperto("groq")
    assert ojo.la_llamaron, (
        "no supo vigilar una funcion suelta de un modulo, que es la forma en que esta escrita "
        "casi toda esta casa")
