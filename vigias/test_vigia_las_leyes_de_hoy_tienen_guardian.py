# -*- coding: utf-8 -*-
"""VIGIA — LAS DOS LEYES QUE FALLARON HOY, CON QUIEN LAS HAGA CUMPLIR.

MEDIDO EL 2026-09-12 con skills/leyes_sin_vigia.py (una de las habilidades dormidas, usada por
fin): de 56 leyes escritas, 35 NO TIENEN QUIEN LAS COMPRUEBE. El 62 por ciento son solo papel, y
dependen de que una IA se acuerde. Ya esta medido que acordarse no funciona.

Aqui se les pone guardian a las DOS que fallaron el mismo dia. Una la escribio Claude horas antes
y tampoco tenia guardian: se cayo en lo mismo que denuncia.

LEY 1 — UNA OPINION NO ES PRUEBA (CONTRATO_UNA_OPINION_NO_ES_PRUEBA.md)
  Lo que paso: el auditor del equipo APROBO dos veces codigo que estaba roto, y la vigia salio
  roja entera. Un visto bueno es una opinion; el hecho es el guardian.
  Donde se cuela: una tarea SIN GUARDIAN NOMBRADO se puede cerrar igual, y eso es cerrar por
  opinion, porque no hay nada que mirar.

LEY 2 — SIN GUARDAR NO HAY TRABAJO (CONTRATO_SIN_GUARDAR_NO_HAY_TRABAJO.md)
  Lo que paso: opencode llevaba CINCO HORAS de trabajo sin guardar, y sus siete horas y media
  parado solo se supieron mirando la hora de su ultimo guardado.
  Lo que falta: poder MIRARLO sin preguntarle a nadie. Es una cuenta.

COMO SE PRUEBA: se EJECUTA el camino real contra un reparto de mentira. No se busca ninguna
palabra dentro de ningun archivo, no se llama a ningun cerebro, y sale lo mismo las mil veces.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

import reparto  # noqa: E402


@pytest.fixture(autouse=True)
def _reparto_de_mentira(tmp_path, monkeypatch):
    """Nunca se toca el reparto de verdad de Julio."""
    monkeypatch.setattr(reparto, "RUTA", str(tmp_path / "REPARTO_DE_PRUEBA.json"))
    yield


def test_NO_se_cierra_una_tarea_SIN_GUARDIAN_NOMBRADO():
    """UNA OPINION NO ES PRUEBA: sin guardian que nombrar, cerrar es cerrar por opinion."""
    reparto.asignar("alguien", "una tarea sin guardian")
    reparto.entregada("alguien", "una tarea sin guardian")
    estado, _ = reparto.supervisar("alguien", "una tarea sin guardian", True)
    assert estado != "correcta", (
        "SE CERRO UNA TAREA SIN NINGUN GUARDIAN NOMBRADO, solo porque quien supervisa dijo que "
        "estaba verde. Eso es cerrar por OPINION, y hoy el auditor aprobo DOS VECES codigo roto")


def test_CON_guardian_nombrado_y_verde_SI_se_cierra():
    """El candado no puede ser un muro: con su guardian nombrado y verde, se cierra."""
    reparto.asignar("alguien", "una tarea con guardian", vigia="vigias/test_algo.py")
    reparto.entregada("alguien", "una tarea con guardian")
    estado, _ = reparto.supervisar("alguien", "una tarea con guardian", True)
    assert estado == "correcta", "con guardian nombrado y verde tampoco deja cerrar: es un muro"


def test_con_guardian_pero_ROJO_no_se_cierra():
    reparto.asignar("alguien", "otra tarea", vigia="vigias/test_algo.py")
    reparto.entregada("alguien", "otra tarea")
    estado, _ = reparto.supervisar("alguien", "otra tarea", False)
    assert estado == "a_corregir", "con el guardian rojo la dio por buena: %s" % estado


def test_SE_PUEDE_MIRAR_quien_lleva_tiempo_sin_guardar():
    """SIN GUARDAR NO HAY TRABAJO: que se sepa sin preguntarle a nadie. Es una cuenta."""
    assert hasattr(reparto, "horas_sin_guardar"), (
        "NO HAY FORMA DE MIRAR SI ALGUIEN LLEVA TIEMPO SIN GUARDAR. Hoy costo cinco horas de "
        "trabajo de opencode, y sus siete horas y media parado solo se supieron a ojo. Hace "
        "falta horas_sin_guardar(raiz) que lo diga contando, no preguntando")
    h = reparto.horas_sin_guardar(AQUI)
    assert h is None or (isinstance(h, float) and h >= 0), (
        "devolvio algo que nadie sabe leer: %r" % (h,))
