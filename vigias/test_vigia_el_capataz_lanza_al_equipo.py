# -*- coding: utf-8 -*-
"""Vigia de lanzar_al_equipo (cuerpo/capataz.py).

Prueba que el capataz arma bien el comando del equipo, que pasa el tope de
segundos y el entorno, y que traduce la salida a guardado/codigo/salida.
Nunca llama al equipo de verdad: se reemplaza subprocess.run por una funcion
falsa que apunta lo que recibe y devuelve lo que le digamos.
"""

import os
import subprocess
import sys
import types

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo import capataz


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


def _ultima_llamada(falsa):
    assert falsa.llamadas, "subprocess.run no fue llamado"
    return falsa.llamadas[-1]


def test_el_comando_lleva_lo_que_tiene_que_llevar(monkeypatch):
    """El comando lleva interprete, ingeniero.py, equipo, proyecto, encargo,
    --escribe deepseek y --revisa bigpickle, y NO lleva --crear."""
    falsa = _falsa_run(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(capataz.subprocess, "run", falsa)

    capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE))

    llamada = _ultima_llamada(falsa)
    comando = llamada["args"][0]

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
    falsa = _falsa_run(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(capataz.subprocess, "run", falsa)

    orden = dict(ORDEN_BASE)
    orden["crear"] = True
    capataz.lanzar_al_equipo("dmm", orden)

    comando = _ultima_llamada(falsa)["args"][0]
    assert comando[-1] == "--crear"


def test_pasa_timeout_y_entorno_utf8(monkeypatch):
    """Se pasa timeout igual al tope pedido y env con PYTHONIOENCODING utf-8."""
    falsa = _falsa_run(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(capataz.subprocess, "run", falsa)

    capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE), tope_segundos=42)

    kwargs = _ultima_llamada(falsa)["kwargs"]
    assert kwargs["timeout"] == 42
    assert kwargs["env"]["PYTHONIOENCODING"] == "utf-8"


def test_si_stdout_trae_guardado_al_momento_devuelve_guardado_true(monkeypatch):
    """Si la salida trae GUARDADO AL MOMENTO, guardado es True con codigo y salida."""
    falsa = _falsa_run(
        returncode=0,
        stdout="todo bien\nGUARDADO AL MOMENTO\n",
        stderr="",
    )
    monkeypatch.setattr(capataz.subprocess, "run", falsa)

    resultado = capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE))

    assert resultado["guardado"] is True
    assert resultado["codigo"] == 0
    assert "GUARDADO AL MOMENTO" in resultado["salida"]


def test_si_no_trae_guardado_al_momento_guardado_es_false(monkeypatch):
    """Si la salida no trae GUARDADO AL MOMENTO, guardado es False."""
    falsa = _falsa_run(
        returncode=1,
        stdout="EL EQUIPO NO APROBO\n",
        stderr="",
    )
    monkeypatch.setattr(capataz.subprocess, "run", falsa)

    resultado = capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE))

    assert resultado["guardado"] is False
    assert resultado["codigo"] == 1
    assert "EL EQUIPO NO APROBO" in resultado["salida"]


def test_si_se_agota_el_tiempo_devuelve_tope_de_tiempo(monkeypatch):
    """Si subprocess.run lanza TimeoutExpired, guardado False, codigo None y
    salida que empieza por TOPE DE TIEMPO."""
    excepcion = subprocess.TimeoutExpired(cmd="x", timeout=7)
    falsa = _falsa_run(excepcion=excepcion)
    monkeypatch.setattr(capataz.subprocess, "run", falsa)

    resultado = capataz.lanzar_al_equipo("dmm", dict(ORDEN_BASE), tope_segundos=7)

    assert resultado["guardado"] is False
    assert resultado["codigo"] is None
    assert resultado["salida"].startswith("TOPE DE TIEMPO")
