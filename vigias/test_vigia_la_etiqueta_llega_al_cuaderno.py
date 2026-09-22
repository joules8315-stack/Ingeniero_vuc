"""Vigia: la etiqueta de la tarea llega al cuaderno.

Comprueba que cada llamada a una IA queda anotada con la tarea del pit
que la pidio (plan v4 P3-7).
"""

import json
import types

from cuerpo import capataz, cuaderno


def _leer_lineas(ruta):
    """Lee el archivo jsonl y devuelve las lineas no vacias ya parseadas."""
    with open(ruta, "r", encoding="utf-8") as f:
        crudas = f.readlines()
    salida = []
    for linea in crudas:
        if not linea.strip():
            continue
        salida.append(json.loads(linea))
    return salida


def test_etiqueta_llega_al_cuaderno(monkeypatch, tmp_path):
    """Con INGENIERO_ETIQUETA puesta, la linea trae la etiqueta limpia."""
    ruta = tmp_path / "c.jsonl"
    monkeypatch.setenv("INGENIERO_CUADERNO_TEST", str(ruta))
    monkeypatch.setenv("INGENIERO_ETIQUETA", " P3-7 ")

    cuaderno.apuntar("deepseek", resultado=cuaderno.OK)

    lineas = _leer_lineas(ruta)
    assert len(lineas) == 1
    assert lineas[0]["etiqueta"] == "P3-7"


def test_sin_etiqueta_no_hay_campo(monkeypatch, tmp_path):
    """Sin INGENIERO_ETIQUETA, la linea no trae el campo etiqueta."""
    ruta = tmp_path / "c.jsonl"
    monkeypatch.setenv("INGENIERO_CUADERNO_TEST", str(ruta))
    monkeypatch.delenv("INGENIERO_ETIQUETA", raising=False)

    cuaderno.apuntar("deepseek", resultado=cuaderno.OK)

    lineas = _leer_lineas(ruta)
    assert len(lineas) == 1
    assert "etiqueta" not in lineas[0]


def test_etiqueta_larga_se_corta_a_80(monkeypatch, tmp_path):
    """Una etiqueta de 200 letras se guarda cortada a 80."""
    ruta = tmp_path / "c.jsonl"
    monkeypatch.setenv("INGENIERO_CUADERNO_TEST", str(ruta))
    monkeypatch.setenv("INGENIERO_ETIQUETA", "a" * 200)

    cuaderno.apuntar("deepseek", resultado=cuaderno.OK)

    lineas = _leer_lineas(ruta)
    assert len(lineas) == 1
    assert lineas[0]["etiqueta"] == "a" * 80


def test_capataz_pasa_la_etiqueta_al_equipo(monkeypatch):
    """lanzar_al_equipo pasa INGENIERO_ETIQUETA con el id de la orden."""
    guardado = {}

    def falso_run(*args, **kwargs):
        guardado["env"] = kwargs.get("env")
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")

    class PopenFalso:
        def __init__(self, comando, **kw):
            guardado["env"] = kw.get("env")
            self.pid = 1
            self.returncode = 0

        def poll(self):
            return 0

        def kill(self):
            pass

        def wait(self, timeout=None):
            return 0

    monkeypatch.setattr(capataz.subprocess, "run", falso_run)
    monkeypatch.setattr(capataz.subprocess, "Popen", PopenFalso)

    from cuerpo import vigilante
    monkeypatch.setattr(vigilante, "esperar", lambda *a, **k: "termino")

    capataz.lanzar_al_equipo(
        "ingeniero", {"id": "P9", "encargo": "x", "pieza": "y"}
    )

    assert guardado["env"]["INGENIERO_ETIQUETA"] == "P9"
