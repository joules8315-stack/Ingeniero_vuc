"""Vigia A-38 punto 4: si Big Pickle esta caido, revisa otra IA.

La ley del 2026-09-19 (orden de Julio A-38 punto 4) manda que si Big Pickle
no contesta, el relevo revise con solo lo que necesita. Nunca Claude y nunca
quien escribio. Esta vigia nace ROJA porque hoy obrero.auditar deja SIN_AUDITAR
cuando Big Pickle cae.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import obrero, cuotas  # noqa: E402
from cuerpo import bigpickle as _bp  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _big_pickle_sin_marca(monkeypatch):
    # cada prueba empieza sin la marca de Big Pickle caido (orden 101, 2026-09-21)
    monkeypatch.setattr(obrero.auditar, '_bp_caido', False, raising=False)
    # Grok tambien cae en estas pruebas, que miden el relevo de hoy; nunca se llama a una IA de verdad (orden 99, 2026-09-21)
    from cuerpo import grok as _grok
    monkeypatch.setattr(_grok, 'preguntar', lambda *a, **k: ('', ['Grok no contesto (prueba)']))


def test_si_bigpickle_cae_revisa_otro_y_avisa_a38(monkeypatch):
    """A-38: Big Pickle cae, el relevo revisa y el aviso menciona A-38."""
    monkeypatch.setattr(_bp, 'preguntar', lambda prompt, *a, **k: ('', ['timeout']))

    guardado = {}

    def falsa(prompt, *a, **k):
        guardado['kwargs'] = dict(k)
        guardado['args'] = a
        return (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), 'groq', [])

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', falsa)
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda p: (_ for _ in ()).throw(AssertionError('Claude no revisa')),
        raising=False,
    )

    auditoria, quien, avisos = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek'
    )

    assert quien == 'groq', 'deberia revisar el relevo groq, reviso: ' + repr(quien)
    assert auditoria['veredicto'] == 'APROBADO', 'veredicto inesperado: ' + repr(auditoria)
    assert guardado.get('kwargs', {}).get('evitar') == 'deepseek', (
        'el relevo no recibio evitar=deepseek: ' + repr(guardado.get('kwargs'))
    )
    texto_avisos = ' '.join(str(a) for a in (avisos or []))
    assert 'A-38' in texto_avisos, 'ningun aviso menciona A-38: ' + repr(avisos)


def test_si_bigpickle_cae_y_el_relevo_calla_queda_sin_auditar(monkeypatch):
    """A-38: si Big Pickle cae y el relevo tampoco contesta, SIN_AUDITAR y no Claude."""
    monkeypatch.setattr(_bp, 'preguntar', lambda prompt, *a, **k: ('', ['timeout']))
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda p: (_ for _ in ()).throw(AssertionError('Claude no revisa')),
        raising=False,
    )

    auditoria, quien, avisos = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek'
    )

    assert auditoria['veredicto'] == 'SIN_AUDITAR', (
        'deberia quedar SIN_AUDITAR: ' + repr(auditoria)
    )
    assert quien != 'claude', 'Claude no puede revisar: ' + repr(quien)


def test_si_bigpickle_contesta_el_relevo_no_se_llama(monkeypatch):
    """A-38: si Big Pickle contesta, revisa Big Pickle y el relevo nunca se llama."""
    bp = []
    monkeypatch.setattr(
        _bp,
        'preguntar',
        lambda prompt, *a, **k: bp.append(1)
        or (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), []),
    )

    relevo = []

    def falsa(*a, **k):
        relevo.append(1)
        return (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), 'groq', [])

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', falsa)
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda p: (_ for _ in ()).throw(AssertionError('Claude no revisa')),
        raising=False,
    )

    auditoria, quien, avisos = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek'
    )

    assert quien == 'bigpickle', 'deberia revisar bigpickle, reviso: ' + repr(quien)
    assert auditoria['veredicto'] == 'APROBADO', 'veredicto inesperado: ' + repr(auditoria)
    assert len(bp) == 1, 'Big Pickle deberia haber sido preguntado una vez: ' + repr(bp)
    assert relevo == [], 'el relevo no deberia llamarse si Big Pickle contesta: ' + repr(relevo)


if __name__ == "__main__":
    import inspect

    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                sig = inspect.signature(_f)
                if 'monkeypatch' in sig.parameters:
                    import pytest

                    class _MP:
                        def setattr(self, obj, nombre, valor, raising=True):
                            setattr(obj, nombre, valor)

                    _f(_MP())
                else:
                    _f()
                print("  VERDE  " + _n)
            except Exception as e:
                fails += 1
                print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
