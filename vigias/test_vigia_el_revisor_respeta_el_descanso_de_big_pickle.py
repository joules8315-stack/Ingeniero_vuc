# -*- coding: utf-8 -*-
"""VIGIA: el revisor respeta el descanso de Big Pickle.

Vigila cuerpo/obrero.py::auditar cuando se le pide auditor='bigpickle'.

Lo que se comprueba:
  1. Si cuotas.desperto('bigpickle') devuelve False, bigpickle.preguntar NO se llama
     y la revision la hace grok47 (el relevo de A-45).
  2. Si bigpickle.preguntar devuelve ('', ['timeout']), despues de la llamada
     cuotas._leer()['seguidos']['bigpickle'] vale 1 (se cuenta el fallo).
  3. Si bigpickle.preguntar devuelve el JSON aprobado, la cuenta de seguidos
     de bigpickle queda en 0 (se limpia el contador).

No toca ningun otro archivo: solo lee y monkeypatchea lo necesario.
"""
import json

import pytest

from cuerpo import obrero
from cuerpo import bigpickle
from cuerpo import grok
from cuerpo import cuotas


JSON_APROBADO = '{"veredicto": "APROBADO", "resumen_para_el_jefe": "ok"}'


@pytest.fixture(autouse=True)
def _aislar(monkeypatch, tmp_path):
    """Deja a bigpickle en pie y aisla el cuaderno de cuotas en tmp_path."""
    monkeypatch.setattr(obrero.auditar, '_bp_caido', False, raising=False)
    monkeypatch.setattr(cuotas, 'RUTA', str(tmp_path / 'CUOTAS.json'), raising=False)
    # grok siempre contesta aprobado y sin avisos, para que el relevo sea predecible.
    monkeypatch.setattr(grok, 'preguntar',
                        lambda *a, **k: (JSON_APROBADO, []), raising=False)
    # claude nunca debe entrar: si entra, revienta y la prueba lo nota.
    def _claude_prohibido(*a, **k):
        raise AssertionError('claude no debe revisar en esta vigia')
    monkeypatch.setattr(obrero, '_claude_directo', _claude_prohibido, raising=False)
    yield


def _llamar_auditar():
    """Llama a auditar EXACTAMENTE como pide la tarea."""
    return obrero.auditar('', {'archivo': 'x.py'},
                          auditor='bigpickle', evitar='deepseek')


def test_si_bigpickle_duerme_no_se_le_llama_y_revisa_grok47(monkeypatch):
    """(1) bigpickle dormido: no se le llama y revisa grok47."""
    monkeypatch.setattr(cuotas, 'desperto', lambda quien: False, raising=False)

    llamadas = {'n': 0}

    def _bp_no_llamar(*a, **k):
        llamadas['n'] += 1
        return (JSON_APROBADO, [])

    monkeypatch.setattr(bigpickle, 'preguntar', _bp_no_llamar, raising=False)

    auditoria, quien, avisos = _llamar_auditar()

    assert llamadas['n'] == 0, 'bigpickle.preguntar NO debe llamarse si esta dormido'
    assert quien == 'grok47', 'debe revisar grok47 cuando bigpickle duerme'
    assert isinstance(auditoria, dict)
    assert auditoria.get('veredicto') == 'APROBADO'


def test_fallo_de_bigpickle_suma_uno_en_seguidos(monkeypatch):
    """(2) bigpickle contesta vacio: la cuenta de seguidos sube a 1."""
    monkeypatch.setattr(cuotas, 'desperto', lambda quien: True, raising=False)
    monkeypatch.setattr(bigpickle, 'preguntar',
                        lambda *a, **k: ('', ['timeout']), raising=False)

    _llamar_auditar()

    datos = cuotas._leer()
    seguidos = datos.get('seguidos') or {}
    assert seguidos.get('bigpickle') == 1, \
        'un fallo de bigpickle debe dejar seguidos[bigpickle] en 1'


def test_exito_de_bigpickle_deja_la_cuenta_en_cero(monkeypatch):
    """(3) bigpickle contesta el JSON aprobado: la cuenta queda en 0."""
    monkeypatch.setattr(cuotas, 'desperto', lambda quien: True, raising=False)
    monkeypatch.setattr(bigpickle, 'preguntar',
                        lambda *a, **k: (JSON_APROBADO, []), raising=False)

    auditoria, quien, avisos = _llamar_auditar()

    assert quien == 'bigpickle', 'si bigpickle contesta, debe ser quien revisa'
    assert isinstance(auditoria, dict)
    assert auditoria.get('veredicto') == 'APROBADO'

    datos = cuotas._leer()
    seguidos = datos.get('seguidos') or {}
    assert seguidos.get('bigpickle', 0) == 0, \
        'un exito de bigpickle debe dejar seguidos[bigpickle] en 0'
