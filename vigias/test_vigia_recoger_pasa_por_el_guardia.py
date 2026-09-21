import subprocess

from cuerpo import capataz
from arnes import recoger_los_pedazos
from arnes import guardia_de_guardado


class _ResultadoFalso:
    """Objeto minimo que imita lo que devuelve subprocess.run."""

    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _preparar(monkeypatch, tmp_path, veredicto):
    """Deja el entorno listo: recoger devuelve ok, subprocess.run es falso y el guardia da el veredicto pedido."""
    ordenes_guardadas = []

    def recoger_falso(raiz, nombre):
        return {'ok': True, 'destino': 'pieza.py', 'razon': 'x'}

    def run_falso(*args, **kwargs):
        if args:
            ordenes_guardadas.append(args[0])
        return _ResultadoFalso(returncode=0, stdout='', stderr='')

    def vigias_falso(raiz):
        return veredicto

    monkeypatch.setattr(recoger_los_pedazos, 'recoger', recoger_falso)
    monkeypatch.setattr(subprocess, 'run', run_falso)
    monkeypatch.setattr(guardia_de_guardado, '_vigias', vigias_falso)

    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    raiz = str(tmp_path)
    return orden, raiz, ordenes_guardadas


def test_recoger_lo_frenado_frena_cuando_el_guardia_esta_rojo(monkeypatch, tmp_path):
    orden, raiz, ordenes_guardadas = _preparar(monkeypatch, tmp_path, (False, 'rojas'))
    resultado = capataz.recoger_lo_frenado(orden, raiz)
    assert isinstance(resultado, dict)
    assert resultado.get('ok') is False


def test_recoger_lo_frenado_deja_orden_con_git_y_pieza(monkeypatch, tmp_path):
    orden, raiz, ordenes_guardadas = _preparar(monkeypatch, tmp_path, (False, 'rojas'))
    capataz.recoger_lo_frenado(orden, raiz)
    hay_git_y_pieza = False
    for guardada in ordenes_guardadas:
        if isinstance(guardada, (list, tuple)):
            texto = ' '.join(str(x) for x in guardada)
        else:
            texto = str(guardada)
        if 'git' in texto and 'pieza.py' in texto:
            hay_git_y_pieza = True
            break
    assert hay_git_y_pieza


def test_recoger_lo_frenado_pasa_cuando_el_guardia_esta_verde(monkeypatch, tmp_path):
    orden, raiz, ordenes_guardadas = _preparar(monkeypatch, tmp_path, (True, 'verde'))
    resultado = capataz.recoger_lo_frenado(orden, raiz)
    assert isinstance(resultado, dict)
    assert resultado.get('ok') is True
