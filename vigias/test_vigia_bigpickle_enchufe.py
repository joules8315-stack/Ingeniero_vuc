import json
import subprocess

import pytest

from cuerpo import bigpickle


class ProcesoFalso:
    """Proceso falso para inyectar en subprocess.Popen sin tocar la red."""

    def __init__(self, *args, **kwargs):
        self.pid = 1
        self.args = args
        self.kwargs = kwargs
        self.returncode = None

    def communicate(self, *args, **kwargs):
        raise subprocess.TimeoutExpired('x', 1)

    def kill(self):
        self.returncode = -9

    def wait(self, *args, **kwargs):
        return self.returncode

    def poll(self):
        return self.returncode


def test_parsear_salida_dos_lineas_json():
    salida = '\n'.join([
        json.dumps({"type": "text", "part": {"text": "hola"}}),
        json.dumps({"type": "step_finish", "part": {"cost": 0.5}}),
    ])
    texto, coste = bigpickle._parsear_salida(salida)
    assert texto == 'hola'
    assert coste == 0.5


def test_trae_llave_detecta_forma_de_llave():
    assert bigpickle._trae_llave('trae <CLAVE>') is True


def test_trae_llave_no_frena_con_marcas_de_llave():
    assert bigpickle._trae_llave('MARCAS_DE_LLAVE = ("API_KEY", "sk-")') is False


def test_preguntar_con_api_key_en_prompt_no_llama(monkeypatch, tmp_path):
    monkeypatch.setattr(bigpickle, 'RUTA_LOG', tmp_path / 'log')
    texto, avisos = bigpickle.preguntar('trae GROQ_API_KEY=gsk_loquesea123')
    assert texto == ''
    assert avisos


def test_preguntar_sin_binario_devuelve_vacio(monkeypatch, tmp_path):
    monkeypatch.setattr(bigpickle, 'RUTA_LOG', tmp_path / 'log')
    monkeypatch.setattr(bigpickle.shutil, 'which', lambda *a, **k: None)
    texto, avisos = bigpickle.preguntar('hola')
    assert texto == ''


def test_preguntar_timeout_no_lanza(monkeypatch, tmp_path):
    monkeypatch.setattr(bigpickle, 'RUTA_LOG', tmp_path / 'log')
    monkeypatch.setattr(bigpickle.subprocess, 'Popen', ProcesoFalso)
    monkeypatch.setattr(bigpickle.subprocess, 'run', lambda *a, **k: None)
    texto, avisos = bigpickle.preguntar('hola', timeout=1)
    assert texto == ''
