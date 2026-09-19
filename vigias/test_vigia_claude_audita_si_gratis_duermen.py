import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from cuerpo import obrero, cuotas


def test_existe_la_puerta_de_claude():
    assert hasattr(obrero, '_claude_directo') is True


def test_si_todas_las_gratis_duermen_audita_claude(monkeypatch):
    """A-32: si todas las gratis duermen, revisa Big Pickle; Claude no revisa."""
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(cuotas, 'desperto', lambda q: False)
    llamadas = []
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda prompt: llamadas.append(1) or json.dumps({'veredicto': 'APROBADO', 'fallos': []}),
        raising=False,
    )
    from cuerpo import bigpickle as _bp
    bp = []
    monkeypatch.setattr(_bp, 'preguntar', lambda prompt, *a, **k: bp.append(1) or (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), []))
    auditoria, quien, avisos = obrero.auditar('', {'archivo': 'x.py'}, evitar='deepseek')
    assert quien == 'bigpickle'
    assert auditoria['veredicto'] == 'APROBADO'
    assert len(bp) == 1
    assert llamadas == []


def test_si_una_gratis_esta_despierta_claude_no_audita(monkeypatch):
    """A-32: si una gratis esta despierta, no revisa ni Claude ni Big Pickle."""
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(cuotas, 'desperto', lambda q: q == 'gemini4')
    llamadas = []
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda prompt: llamadas.append(1) or json.dumps({'veredicto': 'APROBADO', 'fallos': []}),
        raising=False,
    )
    from cuerpo import bigpickle as _bp
    bp = []
    monkeypatch.setattr(_bp, 'preguntar', lambda prompt, *a, **k: bp.append(1) or (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), []))
    auditoria, quien, avisos = obrero.auditar('', {'archivo': 'x.py'}, evitar='deepseek')
    assert bp == []
    assert llamadas == []
    assert quien not in ('claude', 'bigpickle')


def test_claude_no_audita_lo_que_escribio_claude(monkeypatch):
    """A-32: si el que escribio es Big Pickle, no revisa Big Pickle ni Claude."""
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(cuotas, 'desperto', lambda q: False)
    llamadas = []
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda prompt: llamadas.append(1) or json.dumps({'veredicto': 'APROBADO', 'fallos': []}),
        raising=False,
    )
    from cuerpo import bigpickle as _bp
    bp = []
    monkeypatch.setattr(_bp, 'preguntar', lambda prompt, *a, **k: bp.append(1) or (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), []))
    auditoria, quien, avisos = obrero.auditar('', {'archivo': 'x.py'}, evitar='bigpickle')
    assert bp == []
    assert llamadas == []
    assert quien != 'bigpickle'
