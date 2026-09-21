"""Vigia: el candado de cierre tiene que leer la salida de pytest en UTF-8.

CAUSA RAIZ: en Windows, subprocess.run con text=True usa la codificacion por defecto del
sistema (cp1252 o similar). La salida de pytest trae acentos y simbolos; si se decodifica
mal, el candado puede leer basura y confundir un verde con un rojo (o al reves).

Esta vigia NO corre pytest de verdad: pone un espia en subprocess.run que nunca ejecuta
nada, guarda los kwargs de cada llamada y devuelve una salida falsa. Asi se comprueba que
la llamada a pytest lleva encoding='utf-8' y errors='replace'.
"""
import os
import subprocess
import sys

# La carpeta arnes tiene que estar en sys.path para poder importar candado_cierre.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import candado_cierre  # noqa: E402


class _ResultadoFalso:
    """Lo que devuelve el espia: parece un CompletedProcess pero no corrio nada."""

    def __init__(self):
        self.returncode = 0
        self.stdout = "1 passed"
        self.stderr = ""


class _EspiaRun:
    """Espia de subprocess.run: nunca ejecuta, guarda los kwargs de cada llamada."""

    def __init__(self):
        self.llamadas = []

    def __call__(self, *args, **kwargs):
        self.llamadas.append({"args": args, "kwargs": kwargs})
        return _ResultadoFalso()


def _llamada_a_pytest(espia):
    """Devuelve la llamada cuyo comando menciona pytest, o None si no hubo."""
    for llamada in espia.llamadas:
        args = llamada["args"]
        if not args:
            continue
        cmd = args[0]
        if isinstance(cmd, (list, tuple)) and any("pytest" in str(p) for p in cmd):
            return llamada
    return None


def test_el_cierre_lee_en_utf8(tmp_path, monkeypatch):
    # Dentro de una vigia no se corren vigias: se quita la marca para que _vigias_verdes
    # no corte por la guarda de pytest-dentro-de-pytest.
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    # No hay otra corrida en marcha.
    monkeypatch.setattr(candado_cierre, "_ya_hay_otra_corrida", lambda: False)

    # El cerrojo no toca el disco.
    monkeypatch.setattr(candado_cierre, "_poner_cerrojo", lambda: None)
    monkeypatch.setattr(candado_cierre, "_quitar_cerrojo", lambda: None)

    # El espia: subprocess.run nunca corre nada de verdad.
    espia = _EspiaRun()
    monkeypatch.setattr(subprocess, "run", espia)

    # La raiz tiene que tener la carpeta vigias/ o _vigias_verdes corta antes de llamar.
    (tmp_path / "vigias").mkdir()

    verde, detalle = candado_cierre._vigias_verdes(str(tmp_path))

    # El espia devolvio returncode 0, asi que el candado tiene que decir verde.
    assert verde is True, "con returncode 0 el candado tiene que dar verde: " + str(detalle)

    llamada = _llamada_a_pytest(espia)
    assert llamada is not None, "no se llamo a pytest: " + str(espia.llamadas)

    kwargs = llamada["kwargs"]
    assert kwargs.get("encoding") == "utf-8", (
        "la llamada a pytest tiene que llevar encoding='utf-8', "
        "y llevaba: " + repr(kwargs.get("encoding"))
    )
    assert kwargs.get("errors") == "replace", (
        "la llamada a pytest tiene que llevar errors='replace', "
        "y llevaba: " + repr(kwargs.get("errors"))
    )
