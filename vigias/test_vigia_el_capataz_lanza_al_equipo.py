# -*- coding: utf-8 -*-
"""Vigia de lanzar_al_equipo (cuerpo/capataz.py).

Prueba que el capataz arma bien el comando del equipo, que pasa el tope de
segundos y el entorno, y que traduce la salida a guardado/codigo/salida.
Nunca llama al equipo de verdad: se falsifican LAS DOS formas de lanzar a la
vez, para que valga hoy (subprocess.run) y cuando lanzar_al_equipo pase a
subprocess.Popen con el vigilante:
  (a) monkeypatch de capataz.subprocess.run con la falsa de hoy;
  (b) monkeypatch de capataz.subprocess.Popen con una clase falsa que apunta
      comando y kw en la misma lista de llamadas;
  (c) monkeypatch de vigilante.esperar (from cuerpo import vigilante) que
      devuelve 'termino', salvo en la prueba del tiempo agotado, donde
      devuelve 'tope_duro'.

Texto de ayuda de arriba: vale para las dos formas de lanzar mientras entra la
orden 95 (2026-09-22).
"""

import os
import subprocess
import sys
import types

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo import capataz
from cuerpo import vigilante


ORDEN_BASE = {
    "id": "P1",
    "encargo": "arregla algo",
    "pieza": "cuerpo/x.py",
}


def _falsa_run(returncode=0, stdout="", stderr="", excepcion=None):
    """Devuelve una funcion falsa para subprocess.run que apunta args y kwargs."""
    llamadas = []

    def falsa(*args, **kwargs):
        llamadas.append({"args": args, "kwargs": kwargs})
        if excepcion is not None:
            raise excepcion
        return types.SimpleNamespace(
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    falsa.llamadas = llamadas
    return falsa


def _falsa_popen(returncode=0, stdout="", stderr="", excepcion=None):
    """Devuelve una clase falsa para subprocess.Popen que apunta comando y kw
    en la misma lista de llamadas que la falsa de run."""
    llamadas = []

    class FalsaPopen:
        def __init__(self, comando, **kw):
            llamadas.append({"args": (comando,), "kwargs": kw})
            self.pid = 1
            self.returncode = returncode
            if excepcion is not None:
                raise excepcion
            salida = kw.get("stdout")
            if salida is not None and hasattr(salida, "write"):
                salida.write(stdout)
                salida.flush()

        def poll(self):
            return 0

        def kill(self):
            return None

        def wait(self, timeout=None):
            return 0

    FalsaPopen.llamadas = llamadas
    return FalsaPopen


def _falsa_esperar(resultado="termino"):
    """Devuelve una funcion falsa para vigilante.esperar."""
    llamadas = []

    def falsa(*args, **kwargs):
        llamadas.append({"args": args, "kwargs": kwargs})
        return resultado

    falsa.llamadas = llamadas
    return falsa


def _montar(monkeypatch, returncode=0, stdout="", stderr="", excepcion=None,
            esperar="termino"):
    """Falsifica las dos formas de lanzar y el vigilante a la vez."""
    falsa_run = _falsa_run(returncode=returncode, stdout=stdout, stderr=stderr,
                           excepcion=excepcion)
    # el Popen falso no lanza el tiempo agotado; con el vigilante eso lo dice esperar (medido 2026-09-22)
    falsa_popen = _falsa_popen(returncode=returncode, stdout=stdout, stderr=stderr)
    falsa_esperar = _falsa_esperar(esperar)
    monkeypatch.setattr(capataz.subprocess, "run", falsa_run)
    monkeypatch.setattr(capataz.subprocess, "Popen", falsa_popen)
    monkeypatch.setattr(vigilante, "esperar", falsa_esperar)
    return falsa_run, falsa_popen, falsa_esperar


def _ultima_llamada(falsa):
    assert falsa.llamadas, "no se lanzo nada (ni run ni Popen)"
    return falsa.llamadas[-1]


def _comando_de_la_ultima(falsa_run, falsa_popen):
    """Devuelve el comando de la ultima llamada, venga de run o de Popen."""
    if falsa_run.llamadas:
        return falsa_run.llamadas[-1]["args"][0]
    if falsa_popen.llamadas:
        return falsa_popen.llamadas[-1]["args"][0]
    raise AssertionError("no se lanzo nada (ni run ni Popen)")


def test_el_comando_lleva_lo_que_tiene_que_llevar(monkeypatch):
    """El comando lleva interprete, ingeniero.py, equipo, proyecto, encargo,
    --escribe deepseek y --revisa bigpickle, y NO lleva --crear."""
    falsa_run, falsa_popen, _ = _montar(monkeypatch)

    capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE))

    comando = _comando_de_la_ultima(falsa_run, falsa_popen)

    assert comando[0] == sys.executable
    assert comando[1] == "ingeniero.py"
    assert comando[2] == "equipo"
    assert comando[3] == "dmm"
    assert comando[4] == "arregla algo"
    assert "--escribe" in comando
    assert comando[comando.index("--escribe") + 1] == "deepseek"
    assert "--revisa" in comando
    assert comando[comando.index("--revisa") + 1] == "bigpickle"
    assert "--crear" not in comando


def test_con_crear_el_comando_termina_en_crear(monkeypatch):
    """Si la orden trae crear=True, el comando acaba en --crear."""
    falsa_run, falsa_popen, _ = _montar(monkeypatch)

    orden = dict(ORDEN_BASE)
    orden["crear"] = True
    capataz.lanzar_al_equipo("dmm", orden)

    comando = _comando_de_la_ultima(falsa_run, falsa_popen)
    assert comando[-1] == "--crear"


def test_pasa_timeout_y_entorno_utf8(monkeypatch):
    """Se pasa env con PYTHONIOENCODING utf-8 siempre, y timeout igual al tope
    pedido solo si la llamada fue a run (si 'timeout' esta en kwargs)."""
    falsa_run, falsa_popen, _ = _montar(monkeypatch)

    capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE), tope_segundos=42)

    if falsa_run.llamadas:
        kwargs = falsa_run.llamadas[-1]["kwargs"]
    else:
        kwargs = falsa_popen.llamadas[-1]["kwargs"]
    assert kwargs["env"]["PYTHONIOENCODING"] == "utf-8"
    if "timeout" in kwargs:
        assert kwargs["timeout"] == 42


def test_si_stdout_trae_guardado_al_momento_devuelve_guardado_true(monkeypatch):
    """Si la salida trae GUARDADO AL MOMENTO, guardado es True con codigo y salida."""
    _montar(monkeypatch, returncode=0,
            stdout="todo bien\nGUARDADO AL MOMENTO\n", stderr="")

    resultado = capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE))

    assert resultado["guardado"] is True
    assert resultado["codigo"] == 0
    assert "GUARDADO AL MOMENTO" in resultado["salida"]


def test_si_no_trae_guardado_al_momento_guardado_es_false(monkeypatch):
    """Si la salida no trae GUARDADO AL MOMENTO, guardado es False."""
    _montar(monkeypatch, returncode=0, stdout="EL EQUIPO NO APROBO\n", stderr="")

    resultado = capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE))

    assert resultado["guardado"] is False
    assert resultado["codigo"] == 0
    assert "EL EQUIPO NO APROBO" in resultado["salida"]


def test_si_se_agota_el_tiempo_devuelve_tope_de_tiempo(monkeypatch):
    """Si se agota el tiempo, guardado False, codigo None y salida que empieza
    por 'TOPE DE TIEMPO' o por 'COLGADA:'."""
    excepcion = subprocess.TimeoutExpired(cmd="x", timeout=7)
    _montar(monkeypatch, excepcion=excepcion, esperar="tope_duro")

    resultado = capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE), tope_segundos=7)

    assert resultado["guardado"] is False
    assert resultado["codigo"] is None
    assert (resultado["salida"].startswith("TOPE DE TIEMPO")
            or resultado["salida"].startswith("COLGADA:"))
