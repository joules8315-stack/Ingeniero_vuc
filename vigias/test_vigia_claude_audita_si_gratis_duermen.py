import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from cuerpo import obrero, cuotas


def test_existe_la_puerta_de_claude():
    assert hasattr(obrero, '_claude_directo') is True


def test_si_todas_las_gratis_duermen_audita_claude(monkeypatch):
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(cuotas, 'desperto', lambda q: False)
    llamadas = []
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda prompt: llamadas.append(1) or json.dumps({'veredicto': 'APROBADO', 'fallos': []}),
        raising=False,
    )
    auditoria, quien, avisos = obrero.auditar('', {'archivo': 'x.py'}, evitar='deepseek')
    assert quien == 'claude'
    assert auditoria['veredicto'] == 'APROBADO'
    assert len(llamadas) == 1


def test_si_una_gratis_esta_despierta_claude_no_audita(monkeypatch):
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(cuotas, 'desperto', lambda q: q == 'gemini4')
    llamadas = []
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda prompt: llamadas.append(1) or json.dumps({'veredicto': 'APROBADO', 'fallos': []}),
        raising=False,
    )
    auditoria, quien, avisos = obrero.auditar('', {'archivo': 'x.py'}, evitar='deepseek')
    assert llamadas == []
    assert quien != 'claude'


def test_claude_no_audita_lo_que_escribio_claude(monkeypatch):
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', lambda *a, **k: ('', '', []))
    monkeypatch.setattr(cuotas, 'desperto', lambda q: False)
    llamadas = []
    monkeypatch.setattr(
        obrero,
        '_claude_directo',
        lambda prompt: llamadas.append(1) or json.dumps({'veredicto': 'APROBADO', 'fallos': []}),
        raising=False,
    )
    auditoria, quien, avisos = obrero.auditar('', {'archivo': 'x.py'}, evitar='claude')
    assert llamadas == []
    assert quien != 'claude'
