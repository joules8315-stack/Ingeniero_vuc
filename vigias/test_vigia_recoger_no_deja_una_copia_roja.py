import subprocess

from cuerpo import capataz
from arnes import recoger_los_pedazos


class _ResultadoFalso:
    """Objeto minimo que imita lo que devuelve subprocess.run."""

    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _preparar(tmp_path, monkeypatch, orden, returncode_pytest):
    """Deja la pieza en tmp_path, cambia recoger y subprocess.run por dobles.

    Devuelve (raiz, ordenes_guardadas). Cada llamada falsa a subprocess.run
    apunta la orden en la lista para poder mirarla despues.
    """
    pieza = tmp_path / 'pieza.py'
    pieza.write_text('NUEVO\n', encoding='utf-8')
    raiz = str(tmp_path)

    def recoger_falso(raiz_recibida, nombre):
        return {'ok': True, 'destino': 'pieza.py', 'razon': 'x'}

    monkeypatch.setattr(recoger_los_pedazos, 'recoger', recoger_falso)

    ordenes_guardadas = []

    def run_falso(comando, *args, **kwargs):
        ordenes_guardadas.append(comando)
        texto = ' '.join(str(trozo) for trozo in comando) if isinstance(comando, (list, tuple)) else str(comando)
        if 'pytest' in texto:
            return _ResultadoFalso(returncode=returncode_pytest, stdout='', stderr='')
        return _ResultadoFalso(returncode=0, stdout='', stderr='')

    monkeypatch.setattr(subprocess, 'run', run_falso)
    return raiz, ordenes_guardadas


def _contiene(ordenes, *trozos):
    """True si alguna orden guardada contiene todos los trozos pedidos."""
    for orden in ordenes:
        texto = ' '.join(str(trozo) for trozo in orden) if isinstance(orden, (list, tuple)) else str(orden)
        if all(trozo in texto for trozo in trozos):
            return True
    return False


def test_pytest_rojo_devuelve_ok_false_y_guarda_la_orden(tmp_path, monkeypatch):
    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    raiz, ordenes_guardadas = _preparar(tmp_path, monkeypatch, orden, returncode_pytest=1)

    resultado = capataz.recoger_lo_frenado(orden, raiz)

    assert isinstance(resultado, dict)
    assert resultado.get('ok') is False
    assert _contiene(ordenes_guardadas, 'pytest', 'vigias/test_x.py')


def test_pytest_rojo_devuelve_la_pieza_a_lo_guardado(tmp_path, monkeypatch):
    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    raiz, ordenes_guardadas = _preparar(tmp_path, monkeypatch, orden, returncode_pytest=1)

    capataz.recoger_lo_frenado(orden, raiz)

    assert _contiene(ordenes_guardadas, 'git', 'pieza.py')


def test_pytest_verde_devuelve_ok_true(tmp_path, monkeypatch):
    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    raiz, ordenes_guardadas = _preparar(tmp_path, monkeypatch, orden, returncode_pytest=0)

    resultado = capataz.recoger_lo_frenado(orden, raiz)

    assert isinstance(resultado, dict)
    assert resultado.get('ok') is True


def test_entrega_la_prueba_no_llama_a_pytest(tmp_path, monkeypatch):
    orden = {'id': '1', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py', 'entrega_la_prueba': 'si'}
    raiz, ordenes_guardadas = _preparar(tmp_path, monkeypatch, orden, returncode_pytest=1)

    resultado = capataz.recoger_lo_frenado(orden, raiz)

    assert not _contiene(ordenes_guardadas, 'pytest')
    assert isinstance(resultado, dict)
    assert resultado.get('ok') is True
