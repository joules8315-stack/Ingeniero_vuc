import subprocess
import shutil
from cuerpo import grok


class _PopenFalso:
    """Doble de subprocess.Popen que apunta lo que recibe y devuelve un JSON fijo."""

    ultima_orden = None
    ultimo_cwd = None
    ultimo_input = None
    veces_llamado = 0
    lanzar_timeout = False

    def __init__(self, orden, cwd=None, stdin=None, stdout=None, stderr=None, text=None, **kwargs):
        _PopenFalso.ultima_orden = orden
        _PopenFalso.ultimo_cwd = cwd
        _PopenFalso.veces_llamado += 1
        self.returncode = 0

    def communicate(self, input=None, timeout=None):
        _PopenFalso.ultimo_input = input
        if _PopenFalso.lanzar_timeout:
            raise subprocess.TimeoutExpired(cmd='opencode', timeout=timeout)
        texto = (
            '{"type": "text", "part": {"text": "HOLA"}}\n'
            '{"type": "step_finish", "part": {"cost": 0.01}}\n'
        )
        return (texto, '')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def wait(self, timeout=None):
        return 0

    def kill(self):
        return None


def _reset():
    _PopenFalso.ultima_orden = None
    _PopenFalso.ultimo_cwd = None
    _PopenFalso.ultimo_input = None
    _PopenFalso.veces_llamado = 0
    _PopenFalso.lanzar_timeout = False


def _preparar(monkeypatch):
    _reset()
    monkeypatch.setattr(shutil, 'which', lambda nombre: 'opencode')
    monkeypatch.setattr(subprocess, 'Popen', _PopenFalso)


def test_preguntar_devuelve_texto_y_lista(monkeypatch):
    _preparar(monkeypatch)
    texto, avisos = grok.preguntar('hola')
    assert texto == 'HOLA'
    assert avisos == []


def test_la_orden_lleva_modelo_y_formato_y_el_encargo_va_por_input(monkeypatch):
    _preparar(monkeypatch)
    grok.preguntar('hola')
    orden = _PopenFalso.ultima_orden
    assert orden is not None
    if isinstance(orden, str):
        orden_texto = orden
    else:
        orden_texto = ' '.join(str(x) for x in orden)
    assert 'opencode-go/grok-4.7' in orden_texto
    assert '--format' in orden_texto
    assert 'json' in orden_texto
    assert 'hola' not in orden_texto
    assert _PopenFalso.ultimo_input is not None
    assert 'hola' in _PopenFalso.ultimo_input


def test_el_cwd_no_es_la_carpeta_del_proyecto(monkeypatch):
    _preparar(monkeypatch)
    grok.preguntar('hola')
    cwd = _PopenFalso.ultimo_cwd
    assert cwd is not None
    assert 'Ingeniero_VUC' not in str(cwd)


def test_con_llave_de_mentira_no_se_llama_a_popen(monkeypatch):
    _preparar(monkeypatch)
    llave = 's' + 'k' + '-' + ('a' * 24)
    texto, avisos = grok.preguntar('mi clave ' + llave)
    assert texto == ''
    assert _PopenFalso.veces_llamado == 0


def test_si_communicate_lanza_timeout_devuelve_aviso_con_grok(monkeypatch):
    _preparar(monkeypatch)
    _PopenFalso.lanzar_timeout = True
    texto, avisos = grok.preguntar('hola')
    assert texto == ''
    assert any('Grok' in str(a) for a in avisos)
