import os
import subprocess

from cuerpo import capataz
from arnes import recoger_los_pedazos
from arnes import guardia_de_guardado


TEXTO_NUEVO = '''def pieza_nueva():
    return 1
'''


class ResultadoFalso:
    def __init__(self, returncode):
        self.returncode = returncode
        self.stdout = ''
        self.stderr = ''


def _run_falso(palabras, **kwargs):
    """Nunca corre nada: devuelve el codigo segun lo que se le pide."""
    if isinstance(palabras, (list, tuple)):
        texto = ' '.join(str(p) for p in palabras)
    else:
        texto = str(palabras)
    if 'pytest' in texto:
        return ResultadoFalso(1)
    if 'git' in texto and 'cat-file' in texto:
        return ResultadoFalso(1)
    return ResultadoFalso(0)


def _preparar(tmp_path, monkeypatch):
    raiz = tmp_path
    pieza = raiz / 'pieza.py'
    pieza.write_text(TEXTO_NUEVO, encoding='utf-8')
    memoria = raiz / 'memoria' / 'trabajos_sin_revisar'
    memoria.mkdir(parents=True, exist_ok=True)

    def recoger_falso(raiz_arg, nombre):
        return {'ok': True, 'destino': 'pieza.py', 'razon': 'x'}

    monkeypatch.setattr(recoger_los_pedazos, 'recoger', recoger_falso)
    monkeypatch.setattr(subprocess, 'run', _run_falso)
    monkeypatch.setattr(guardia_de_guardado, '_vigias', lambda raiz_arg: (True, 'x'))
    return raiz


def test_la_pieza_nueva_ya_no_esta_en_su_sitio(tmp_path, monkeypatch):
    raiz = _preparar(tmp_path, monkeypatch)
    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    capataz.recoger_lo_frenado(orden, str(raiz))
    assert not (raiz / 'pieza.py').exists(), 'la pieza nueva se quedo en su sitio'


def test_la_pieza_nueva_queda_apartada_como_rojo(tmp_path, monkeypatch):
    raiz = _preparar(tmp_path, monkeypatch)
    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    capataz.recoger_lo_frenado(orden, str(raiz))
    carpeta = raiz / 'memoria' / 'trabajos_sin_revisar'
    candidatos = [
        n for n in os.listdir(str(carpeta))
        if n.startswith('pieza.py') and n.endswith('.ROJO')
    ]
    assert candidatos, 'no hay ningun archivo pieza.py*.ROJO en trabajos_sin_revisar'
    with open(str(carpeta / candidatos[0]), encoding='utf-8') as f:
        contenido = f.read()
    assert contenido == TEXTO_NUEVO, 'el archivo apartado no lleva el texto NUEVO dentro'
