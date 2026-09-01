# -*- coding: utf-8 -*-
"""VIGIA — NUNCA SIN REVISAR (Claude, 2026-09-02; contrato CONTRATO_NUNCA_SIN_REVISAR.md).

LO QUE PROTEGE: `arnes/candado_equipo.py` -> `guardar_veredicto`. Cuando el veredicto NO es
APROBADO, su lista de archivos se guarda VACIA para que no abra ninguna puerta; se anade el dato
`reviso_a_si_mismo` (verdadero si el que reviso fue el mismo que escribio), y el renglon del
cuaderno lleva dos datos mas al final: si abre puertas y si se reviso a si mismo.

QUE SE VIGILA AQUI (cuatro comprobaciones):
  1) un veredicto SIN_AUDITAR se guarda pero con la lista de archivos VACIA
  2) un veredicto RECHAZADO igual: se guarda con la lista vacia
  3) un veredicto APROBADO SI conserva sus archivos (no se aflojo nada)
  4) reviso_a_si_mismo es verdadero cuando el que reviso es el mismo que escribio, y falso cuando
     son distintos

Se usa la carpeta de mentira que dan las pruebas, nunca la memoria de verdad, para no ensuciar el
rastro real.
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest


@pytest.fixture(autouse=True)
def _todo_aparte(tmp_path, monkeypatch):
    import candado_equipo as ce
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    # el cuaderno de los trabajos se escribe con AQUI; se desvia para no tocar la memoria real
    monkeypatch.setattr(ce, "AQUI", str(tmp_path))
    yield


def _guardar_y_leer(veredicto, obrero, auditor, archivos):
    import candado_equipo as ce
    ce.guardar_veredicto("una tarea", archivos, obrero, auditor, veredicto)
    ruta = os.environ["INGENIERO_VEREDICTO_TEST"]
    return json.load(open(ruta, encoding="utf-8"))


def test_sin_auditar_se_guarda_con_archivos_vacios(tmp_path, monkeypatch):
    """Un SIN_AUDITAR no es aprobacion: se guarda (vale dinero saberlo) pero no abre nada."""
    d = _guardar_y_leer("SIN_AUDITAR", "obrero", "(ninguno)", ["x.py", "y.py"])
    assert d["veredicto"] == "SIN_AUDITAR"
    assert d["archivos"] == [], "un SIN_AUDITAR guardo archivos y abrio puertas"


def test_rechazado_se_guarda_con_archivos_vacios(tmp_path, monkeypatch):
    """Un RECHAZADO tampoco abre: la lista de archivos se guarda vacia."""
    d = _guardar_y_leer("RECHAZADO", "obrero", "revisor", ["x.py"])
    assert d["veredicto"] == "RECHAZADO"
    assert d["archivos"] == [], "un RECHAZADO guardo archivos y abrio puertas"


def test_aprobado_si_conserva_sus_archivos(tmp_path, monkeypatch):
    """El APROBADO debe conservar sus archivos: no se aflojo ni se rompio lo que ya funcionaba."""
    d = _guardar_y_leer("APROBADO", "obrero", "revisor", ["x.py", "y.py"])
    assert d["archivos"] == ["x.py", "y.py"], "el APROBADO perdio sus archivos"


def test_reviso_a_si_mismo_verdadero_si_el_mismo(tmp_path, monkeypatch):
    """Cuando el que reviso es el mismo que escribio, hay que decirlo: se reviso a si mismo."""
    d = _guardar_y_leer("APROBADO", "deepseek", "deepseek", ["x.py"])
    assert d["reviso_a_si_mismo"] is True


def test_reviso_a_si_mismo_falso_si_distintos(tmp_path, monkeypatch):
    """Cuando son dos distintos, NO se reviso a si mismo."""
    d = _guardar_y_leer("APROBADO", "deepseek", "gemini", ["x.py"])
    assert d["reviso_a_si_mismo"] is False


def test_el_renglon_dice_si_abre_puertas(tmp_path, monkeypatch):
    """El cuaderno dice en palabras simples si ese veredicto abre puertas (para Julio, de un
    vistazo). Solo el APROBADO abre."""
    import candado_equipo as ce
    ce.guardar_veredicto("t", ["x.py"], "obrero", "revisor", "RECHAZADO")
    cuaderno = os.path.join(str(tmp_path), "memoria", "TRABAJOS_DEL_EQUIPO.log")
    texto = open(cuaderno, encoding="utf-8").read()
    assert "NO abre puertas" in texto, "el cuaderno no dijo que ese veredicto no abre puertas"
