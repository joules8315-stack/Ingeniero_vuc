# -*- coding: utf-8 -*-
"""Vigia nueva: el revisor de programa frena un cambio que deja un .py SIN CARGAR,
pero solo si antes cargaba. Asi no frena en falso archivos que la cuenta ya ve raros.

Nace roja: la comprobacion 'NO CARGA' todavia no existe en arnes/revisor_de_programa.py.
Orden de Julio A-38, tarea E-3.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, 'arnes'))
import revisor_de_programa as r

CV = 'texto' + '_viejo'
CN = 'texto' + '_nuevo'


X_PY = 'import os\n\ndef f():\n    return 1\n'
Y_PY = 'print(sorted([1], key=lambda x: x))\nA = 1\n'
Z_TXT = 'esto no es python\nA = 1\n'


def _escribir(tmp_path, nombre, contenido):
    ruta = tmp_path / nombre
    ruta.write_text(contenido, encoding='utf-8')
    return ruta


def _fallos(ruta, viejo, nuevo, tarea):
    propuesta = {'archivo': str(ruta), CV: viejo, CN: nuevo}
    return r.revisar(propuesta, tarea)


def _alguno_dice_no_carga(fallos):
    return any('NO CARGA' in str(f) for f in fallos)


def test_cambio_que_deja_sin_cargar_frena(tmp_path):
    """(1) x.py cargaba y el cambio lo deja sin cargar: algun fallo dice NO CARGA."""
    ruta = _escribir(tmp_path, 'x.py', X_PY)
    viejo = 'def f():'
    nuevo = '@contextlib.contextmanager\ndef f():'
    fallos = _fallos(ruta, viejo, nuevo, 'cambia f')
    assert _alguno_dice_no_carga(fallos), (
        'el revisor no freno un .py que deja de cargar: ' + repr(fallos))


def test_cambio_que_sigue_cargando_no_frena(tmp_path):
    """(2) mismo archivo, cambio que sigue cargando: ningun fallo dice NO CARGA."""
    ruta = _escribir(tmp_path, 'x.py', X_PY)
    viejo = 'return 1'
    nuevo = 'return 2'
    fallos = _fallos(ruta, viejo, nuevo, 'cambia el retorno')
    assert not _alguno_dice_no_carga(fallos), (
        'el revisor freno en falso un cambio que si carga: ' + repr(fallos))


def test_archivo_que_ya_veia_raro_no_frena(tmp_path):
    """(3) y.py ya no cargaba antes: el cambio no puede dar NO CARGA."""
    ruta = _escribir(tmp_path, 'y.py', Y_PY)
    viejo = 'A = 1'
    nuevo = 'A = 2'
    fallos = _fallos(ruta, viejo, nuevo, 'cambia A')
    assert not _alguno_dice_no_carga(fallos), (
        'el revisor freno en falso un archivo que ya veia raro: ' + repr(fallos))


def test_archivo_que_no_es_py_nunca_da_no_carga(tmp_path):
    """(4) un archivo que no es .py nunca da NO CARGA."""
    ruta = _escribir(tmp_path, 'z.txt', Z_TXT)
    viejo = 'A = 1'
    nuevo = 'A = 2'
    fallos = _fallos(ruta, viejo, nuevo, 'cambia A')
    assert not _alguno_dice_no_carga(fallos), (
        'el revisor dio NO CARGA en un archivo que no es .py: ' + repr(fallos))


if __name__ == '__main__':
    import tempfile
    import pathlib

    _fallos_totales = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith('test_') and callable(_f):
            _dir = pathlib.Path(tempfile.mkdtemp(prefix='vigia_no_carga_'))
            try:
                _f(_dir)
                print('  VERDE  ' + _n)
            except Exception as _e:
                _fallos_totales += 1
                print('  ROJA   ' + _n + ': ' + repr(_e))
    raise SystemExit(1 if _fallos_totales else 0)
