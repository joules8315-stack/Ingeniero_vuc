import subprocess

from cuerpo import capataz
from arnes import recoger_los_pedazos
from arnes import guardia_de_guardado


ORDEN = {
    'id': '1',
    'pieza': 'pieza.py',
    'vigia': 'vigias/test_x.py',
    'entrega_la_prueba': 'si',
}


def _preparar(monkeypatch, raiz, llaves):
    """Deja el terreno listo: la pieza existe, recoger devuelve ok, subprocess no corre nada
    y _hay_llaves devuelve lo que le digamos."""
    (raiz / 'pieza.py').write_text('x = 1\n', encoding='utf-8')

    def recoger_falso(carpeta, nombre):
        return {'ok': True, 'destino': 'pieza.py', 'razon': 'x'}

    monkeypatch.setattr(recoger_los_pedazos, 'recoger', recoger_falso)

    ordenes = []

    def run_falso(*args, **kwargs):
        ordenes.append((args, kwargs))

        class Resultado:
            returncode = 0
            stdout = ''
            stderr = ''

        return Resultado()

    monkeypatch.setattr(subprocess, 'run', run_falso)

    def hay_llaves_falso(raiz, archivos):
        return llaves

    monkeypatch.setattr(guardia_de_guardado, '_hay_llaves', hay_llaves_falso)

    return ordenes


def test_si_hay_llaves_devuelve_ok_false_y_lo_dice(monkeypatch, tmp_path):
    """Si _hay_llaves devuelve ['pieza.py'], recoger_lo_frenado tiene que devolver ok False
    y su razon tiene que contener la palabra llave."""
    _preparar(monkeypatch, tmp_path, ['pieza.py'])

    resultado = capataz.recoger_lo_frenado(ORDEN, str(tmp_path))

    assert isinstance(resultado, dict), 'recoger_lo_frenado no devolvio un dict'
    assert resultado.get('ok') is False, (
        'con llaves presentes el resultado deberia ser ok False, y vino: ' + repr(resultado))
    razon = str(resultado.get('razon', ''))
    assert 'llave' in razon.lower(), (
        'la razon no nombra la palabra llave: ' + repr(razon))


def test_si_no_hay_llaves_devuelve_ok_true(monkeypatch, tmp_path):
    """Si _hay_llaves devuelve [], el resultado tiene que tener ok True."""
    _preparar(monkeypatch, tmp_path, [])

    resultado = capataz.recoger_lo_frenado(ORDEN, str(tmp_path))

    assert isinstance(resultado, dict), 'recoger_lo_frenado no devolvio un dict'
    assert resultado.get('ok') is True, (
        'sin llaves el resultado deberia ser ok True, y vino: ' + repr(resultado))
