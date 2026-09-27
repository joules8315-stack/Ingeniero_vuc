# -*- coding: utf-8 -*-
"""VIGIA: a nadie se le espera mas de lo medido.

De que fallo nace (numeros medidos el 2026-09-27 sobre memoria/CUADERNO_DE_LLAMADAS.jsonl):

  - Big Pickle dio 163 respuestas buenas. La mas lenta tardo 314 segundos.
    162 de las 163 llegaron antes de 300 segundos.
  - grok47 dio 27 respuestas buenas y TODAS llegaron antes de 240 segundos.

Sin embargo hoy se le puede esperar a un cerebro su propio record por 1.5, es decir
hasta 471 segundos o mas, y el tope por defecto de Big Pickle es 600 segundos.

Esperar 600 segundos para ganar una respuesta de cada 163 es lo que hace que una
orden tarde 90 minutos.

Lo que esta vigia exige: que exista un techo maximo de espera de 300 segundos
que nadie pueda pasar, sin cambiar nada mas.

Esta vigia NACE ROJA: hoy el techo no existe y estos casos fallan.
"""

import json
import os
import sys

import pytest


# La raiz del repo se calcula subiendo dos niveles desde este archivo.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import cuotas  # noqa: E402
from cuerpo import bigpickle  # noqa: E402
from cuerpo import cuaderno  # noqa: E402


TOPE = 300


class _CerebroDeMentira(object):
    """Cerebro minimo para las pruebas: solo lo que cuotas necesita leer."""

    def __init__(self, nombre, record_seg):
        self.nombre = nombre
        self.record_seg = record_seg


def _gasto_con(monkeypatch, cerebro):
    """Sustituye cuotas._leer por algo que devuelve un gasto con un cerebro dentro."""

    def _leer_falso(*args, **kwargs):
        return {"gasto": {cerebro.nombre: cerebro}}

    monkeypatch.setattr(cuotas, "_leer", _leer_falso, raising=False)


def test_a_un_cerebro_lentisimo_no_se_le_esperan_mas_de_300(monkeypatch):
    """Un cerebro con record de 1000 s no puede hacer esperar mas de 300 s.

    Si se le espera su record por 1.5, serian 1500 segundos. Eso es esperar de mas:
    con 300 s ya se cubre a 162 de las 163 respuestas buenas de Big Pickle.
    """
    cerebro = _CerebroDeMentira("lentisimo", 1000)
    _gasto_con(monkeypatch, cerebro)

    espera = cuotas.cuanto_esperarle(cerebro)

    assert espera <= TOPE, (
        "A un cerebro con record de 1000 s se le esta esperando %r segundos. "
        "Eso es esperar de mas: el techo tiene que ser 300 s como mucho. "
        "Con 300 s ya llegan 162 de las 163 respuestas buenas de Big Pickle; "
        "esperar mas solo alarga la orden sin ganar casi nada." % (espera,)
    )


def test_a_un_cerebro_normal_no_se_le_cambia_la_espera(monkeypatch):
    """Un cerebro normal (record 100 s) sigue esperando 150 s: su record por 1.5.

    El techo de 300 s no debe tocar a los cerebros normales.
    """
    cerebro = _CerebroDeMentira("normal", 100)
    _gasto_con(monkeypatch, cerebro)

    espera = cuotas.cuanto_esperarle(cerebro)

    assert espera == 150, (
        "A un cerebro normal con record de 100 s se le espera %r segundos, "
        "y deberia ser 150 (su record por el margen de 1.5). "
        "El techo de 300 s no debe cambiar la espera de los cerebros normales." % (espera,)
    )


def test_la_espera_minima_sigue_siendo_60(monkeypatch):
    """Un cerebro con record de 10 s sigue teniendo una espera minima de 60 s."""
    cerebro = _CerebroDeMentira("rapido", 10)
    _gasto_con(monkeypatch, cerebro)

    espera = cuotas.cuanto_esperarle(cerebro)

    assert espera == 60, (
        "A un cerebro con record de 10 s se le espera %r segundos, "
        "y la espera minima tiene que seguir siendo 60 s." % (espera,)
    )


def test_a_big_pickle_tampoco_se_le_esperan_mas_de_300(monkeypatch, tmp_path):
    """Big Pickle tampoco puede pasar de 300 s de espera.

    Se escribe un cuaderno de mentira con varias lineas JSON de quien bigpickle,
    resultado ok, segundos 500 y tamano 1000, y se comprueba que la espera
    calculada para un tamano de 1000 no pasa de 300 s.
    """
    cuaderno_falso = tmp_path / "CUADERNO_DE_LLAMADAS.jsonl"
    lineas = []
    for i in range(5):
        lineas.append(json.dumps({
            "quien": "bigpickle",
            "resultado": "ok",
            "segundos": 500,
            "tamano": 1000,
            "n": i,
        }))
    cuaderno_falso.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    monkeypatch.setattr(cuaderno, "_ruta", lambda *a, **k: str(cuaderno_falso), raising=False)

    espera = cuotas.espera_de_bigpickle(1000)

    assert espera <= TOPE, (
        "A Big Pickle, con un tamano de 1000, se le esta esperando %r segundos. "
        "Eso es esperar de mas: el techo tiene que ser 300 s como mucho. "
        "Su record medido es 314 s y 162 de sus 163 respuestas buenas llegaron "
        "antes de 300 s; esperar mas solo hace que una orden tarde 90 minutos." % (espera,)
    )


def test_el_tope_por_defecto_de_big_pickle_tampoco_pasa_de_300():
    """El tope por defecto de Big Pickle no puede pasar de 300 s.

    Hoy vale 600 s: eso es esperar de mas para ganar una respuesta de cada 163.
    """
    tope = bigpickle.TIMEOUT_POR_DEFECTO

    assert tope <= TOPE, (
        "El tope por defecto de Big Pickle es %r segundos, y no puede pasar de 300. "
        "Esperar 600 s para ganar una respuesta de cada 163 es lo que hace que "
        "una orden tarde 90 minutos." % (tope,)
    )
