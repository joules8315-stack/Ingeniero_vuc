import json

from cuerpo import bigpickle
from cuerpo import cuotas
from cuerpo import cuaderno


class ProcesoFalso:
    """Proceso de mentira que imita lo que bigpickle.preguntar espera de Popen."""

    def __init__(self, salida, tiempos):
        self._salida = salida
        self._tiempos = tiempos
        self.returncode = 0
        self.pid = 4242

    def communicate(self, input=None, timeout=None):
        self._tiempos.append(timeout)
        return (self._salida, "")

    def kill(self):
        pass


def _salida_ok(texto):
    """Arma la salida JSON por lineas que bigpickle._parsear_salida sabe leer.

    bigpickle lee la salida de opencode como JSON por lineas y saca el texto
    de los campos de contenido. Se arma una linea con la forma que el parser
    reconoce para que devuelva el texto ok.
    """
    linea = json.dumps({"type": "text", "text": texto})
    return linea + "\n"


def _preparar(monkeypatch, texto="ok"):
    """Deja el enchufe con dobles de prueba y devuelve las listas de control."""
    letras = []
    tiempos = []

    def espera_falsa(letras_recibidas):
        letras.append(letras_recibidas)
        return 777.0

    monkeypatch.setattr(cuotas, "espera_de_bigpickle", espera_falsa)
    monkeypatch.setattr(bigpickle.shutil, "which", lambda nombre: "opencode")

    def popen_falso(*args, **kwargs):
        return ProcesoFalso(_salida_ok(texto), tiempos)

    monkeypatch.setattr(bigpickle.subprocess, "Popen", popen_falso)
    return letras, tiempos


def test_preguntar_usa_la_espera_medida(monkeypatch):
    letras, tiempos = _preparar(monkeypatch)

    bigpickle.preguntar("hola mundo")

    assert tiempos == [777.0]
    assert len(letras) == 1
    # espera_de_bigpickle recibe el numero de letras, no el texto (medido 2026-09-22)
    assert letras[0] == 10


def test_preguntar_respeta_el_timeout_que_le_dan(monkeypatch):
    letras, tiempos = _preparar(monkeypatch)

    bigpickle.preguntar("hola", timeout=50)

    assert tiempos == [50]


def test_el_cuaderno_apunta_el_tamano_del_encargo(monkeypatch):
    letras, tiempos = _preparar(monkeypatch)

    bigpickle.preguntar("hola mundo")

    with open(cuaderno._ruta(), "r", encoding="utf-8") as fh:
        filas = [linea for linea in fh.read().splitlines() if linea.strip()]
    ultima = json.loads(filas[-1])
    assert ultima["tamano"] == 10
