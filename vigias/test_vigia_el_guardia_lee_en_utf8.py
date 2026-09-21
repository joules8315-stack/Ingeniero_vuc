import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
ARNES = os.path.dirname(AQUI)
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import guardia_de_guardado  # noqa: E402
import vecinas  # noqa: E402


class _ResultadoFalso:
    """Lo que devuelve subprocess.run cuando lo cambiamos por un espia."""

    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _es_llamada_a_pytest(args, kwargs):
    """True si esta llamada a subprocess.run es la de pytest.

    OJO: pytest puede venir en args posicionales (la lista de argumentos) o en
    kwargs['args']. Hay que mirar LOS DOS sitios, no solo kwargs, porque si no
    la vigia no ve la llamada y se queda verde mintiendo.
    """
    candidatos = []
    if args:
        candidatos.append(args[0])
    if "args" in kwargs:
        candidatos.append(kwargs["args"])
    for c in candidatos:
        if isinstance(c, (list, tuple)):
            if any(str(x) == "pytest" for x in c):
                return True
        elif isinstance(c, str) and c == "pytest":
            return True
    return False


def test_el_guardia_lee_en_utf8(tmp_path, monkeypatch):
    """Tras _vigias(raiz), la llamada a pytest se hizo con encoding='utf-8' y errors='replace'."""
    (tmp_path / "vigias").mkdir()

    llamadas = []

    def run_falso(*args, **kwargs):
        llamadas.append({"args": args, "kwargs": kwargs})
        return _ResultadoFalso(returncode=0, stdout="1 passed", stderr="")

    monkeypatch.setattr(subprocess, "run", run_falso)
    monkeypatch.setattr(vecinas, "elegir", lambda raiz: ["vigias/test_x.py"])

    paso, mensaje = guardia_de_guardado._vigias(str(tmp_path))
    assert paso is True, "el guardia deberia dejar pasar con '1 passed': %r" % (mensaje,)

    llamadas_pytest = [c for c in llamadas if _es_llamada_a_pytest(c["args"], c["kwargs"])]
    assert llamadas_pytest, (
        "no se encontro ninguna llamada a pytest entre las %d llamadas a subprocess.run"
        % len(llamadas)
    )

    kwargs = llamadas_pytest[0]["kwargs"]
    assert kwargs.get("encoding") == "utf-8", (
        "pytest se llamo sin encoding='utf-8': %r" % (kwargs.get("encoding"),)
    )
    assert kwargs.get("errors") == "replace", (
        "pytest se llamo sin errors='replace': %r" % (kwargs.get("errors"),)
    )
