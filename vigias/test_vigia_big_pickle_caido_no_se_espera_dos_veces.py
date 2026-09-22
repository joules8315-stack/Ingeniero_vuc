"""Vigia: si Big Pickle esta caido, no se le espera dos veces.

Julio, 2026-09-21. Cuando el auditor pedido es 'bigpickle' y Big Pickle no contesta
(timeout), obrero.auditar NO debe volver a llamar a bigpickle.preguntar en la misma
ronda: ya se sabe que esta caido y se pasa al relevo. Pero si Big Pickle SI contesta
bien, cada llamada a obrero.auditar debe volver a preguntarle, porque no fallo.

Se vigila la funcion auditar de cuerpo/obrero.py con auditor='bigpickle'.
"""

from cuerpo import obrero
from cuerpo import bigpickle
from cuerpo import grok


PROPUESTA = {'archivo': 'x.py'}


def _claude_prohibido(*args, **kwargs):
    """Si alguien llama a Claude, la vigia revienta: Claude no debe usarse aqui."""
    raise AssertionError('no se debe llamar a Claude en esta vigia')


def _preparar(monkeypatch, respuestas):
    """Deja el terreno listo: cuenta llamadas a bigpickle.preguntar y devuelve
    las respuestas de la lista, una por llamada. Devuelve el contador."""
    llamadas = {'n': 0}

    def _preguntar_falso(prompt):
        i = llamadas['n']
        llamadas['n'] += 1
        if i < len(respuestas):
            return respuestas[i]
        return respuestas[-1]

    monkeypatch.setattr(bigpickle, 'preguntar', _preguntar_falso)
    monkeypatch.setattr(grok, 'preguntar', lambda *a, **k: ('', ['grok falso en la vigia']))
    monkeypatch.setattr(obrero, '_claude_directo', _claude_prohibido)
    monkeypatch.setattr(obrero.auditar, '_bp_caido', False, raising=False)

    def _relevo_falso(prompt, temperatura, evitar=None, primero=None, pesado=False,
                      clase='', vuelta=0):
        return ('{"veredicto": "APROBADO", "resumen_para_el_jefe": "ok"}',
                'groq', [])

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', _relevo_falso)
    return llamadas


def test_big_pickle_caido_no_se_espera_dos_veces(monkeypatch):
    """Si Big Pickle no contesta (timeout), dos llamadas seguidas solo le preguntan UNA vez."""
    llamadas = _preparar(monkeypatch, [
        ('', ['Big Pickle no contesto en 300s (timeout)']),
    ])

    auditoria1, quien1, avisos1 = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')
    auditoria2, quien2, avisos2 = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')

    assert llamadas['n'] == 1, (
        'bigpickle.preguntar se llamo %d veces; con Big Pickle caido debe llamarse UNA sola vez'
        % llamadas['n'])
    assert isinstance(auditoria1, dict)
    assert isinstance(auditoria2, dict)


def test_big_pickle_vivo_si_se_le_pregunta_cada_vez(monkeypatch):
    """Si Big Pickle contesta bien, dos llamadas seguidas le preguntan DOS veces."""
    llamadas = _preparar(monkeypatch, [
        ('{"veredicto": "APROBADO", "resumen_para_el_jefe": "ok"}', []),
        ('{"veredicto": "APROBADO", "resumen_para_el_jefe": "ok"}', []),
    ])

    auditoria1, quien1, avisos1 = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')
    auditoria2, quien2, avisos2 = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')

    assert llamadas['n'] == 2, (
        'bigpickle.preguntar se llamo %d veces; si Big Pickle contesta bien debe llamarse DOS veces'
        % llamadas['n'])
    assert isinstance(auditoria1, dict)
    assert isinstance(auditoria2, dict)
