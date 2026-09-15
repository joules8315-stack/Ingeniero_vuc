import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'arnes'))
import canal

RUTA_PROGRAMITA = os.path.join(RAIZ, '.opencode', 'plugins', 'canal_buzon.js')


def test_leer_sin_marcar_no_marca(monkeypatch, tmp_path):
    monkeypatch.setenv('INGENIERO_CANAL_TEST', str(tmp_path))
    canal.enviar('opencode', 'hola', de='claude')
    msgs = canal.leer('opencode', marcar=False)
    assert len(msgs) == 1
    msgs2 = canal.leer('opencode', marcar=False)
    assert len(msgs2) == 1


def test_marcar_despues_de_entregar(monkeypatch, tmp_path):
    monkeypatch.setenv('INGENIERO_CANAL_TEST', str(tmp_path))
    canal.enviar('opencode', 'hola', de='claude')
    msgs = canal.leer('opencode', marcar=False)
    assert len(msgs) == 1
    canal.marcar_leidos([m['ruta'] for m in msgs])
    msgs2 = canal.leer('opencode', marcar=False)
    assert len(msgs2) == 0


def test_el_programita_usa_marca_prt_y_no_lee_sin_sesion():
    assert os.path.exists(RUTA_PROGRAMITA), 'no existe el programita: ' + RUTA_PROGRAMITA
    with open(RUTA_PROGRAMITA, 'r', encoding='utf-8') as f:
        texto = f.read()
    assert 'prt_' in texto
    assert 'canal-' + chr(34) not in texto
    assert 'canal-' + 'Date' not in texto
    assert '--sin-marcar' in texto


def test_el_programita_marca_solo_despues_de_entregar():
    assert os.path.exists(RUTA_PROGRAMITA), 'no existe el programita: ' + RUTA_PROGRAMITA
    with open(RUTA_PROGRAMITA, 'r', encoding='utf-8') as f:
        texto = f.read()
    assert chr(34) + 'marcar' + chr(34) in texto
