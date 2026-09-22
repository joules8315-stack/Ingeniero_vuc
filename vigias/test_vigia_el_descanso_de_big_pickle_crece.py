# -*- coding: utf-8 -*-
"""Vigia: el descanso de bigpickle crece cuando vuelve a fallar dos veces seguidas.

Orden de Julio A-46 (2026-09-21): bigpickle, al segundo fallo seguido, duerme 30 min.
Si al despertar vuelve a fallar dos veces seguidas, el descanso crece a 60 min.
Un acierto borra la cuenta de fallos seguidos y el descanso vuelve a 30 min.

Esta vigia comprueba ese crecimiento y ese borrado, aislando la memoria en tmp_path.
"""
import time

from cuerpo import cuotas


import pytest


@pytest.fixture(autouse=True)
def _aislar_memoria(tmp_path, monkeypatch):
    """Aisla la memoria de cuotas en un archivo temporal por prueba."""
    monkeypatch.setattr(cuotas, "RUTA", str(tmp_path / "CUOTAS.json"))


def _despertar():
    """Fuerza que bigpickle ya haya despertado: pone su 'hasta' en el pasado y llama a desperto."""
    d = cuotas._leer()
    d["dormidos"]["bigpickle"]["hasta"] = time.time() - 1
    cuotas._guardar(d)
    cuotas.desperto("bigpickle")


def _dura():
    """Segundos que le quedan de descanso a bigpickle (negativo si ya desperto)."""
    return cuotas._leer()["dormidos"]["bigpickle"]["hasta"] - time.time()


def test_dos_fallos_duermen_30_min():
    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()
    assert cuotas.desperto("bigpickle") is False
    assert 1790 < _dura() < 1810


def test_segundo_ciclo_duerme_60_min():
    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()
    _despertar()
    cuotas.bigpickle_fallo()
    assert cuotas.desperto("bigpickle") is True
    cuotas.bigpickle_fallo()
    assert 3590 < _dura() < 3610


def test_tercer_y_cuarto_ciclo_duermen_60_min():
    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()
    _despertar()
    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()
    assert 3590 < _dura() < 3610

    _despertar()
    cuotas.bigpickle_fallo()
    assert cuotas.desperto("bigpickle") is True
    cuotas.bigpickle_fallo()
    assert 3590 < _dura() < 3610

    _despertar()
    cuotas.bigpickle_fallo()
    assert cuotas.desperto("bigpickle") is True
    cuotas.bigpickle_fallo()
    assert 3590 < _dura() < 3610


def test_acierto_borra_todo_y_vuelve_a_30_min():
    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()
    _despertar()
    cuotas.bigpickle_acierto()
    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()
    assert 1790 < _dura() < 1810
