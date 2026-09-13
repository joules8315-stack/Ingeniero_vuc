"""VIGIA — UN VEREDICTO QUE EL PROGRAMA FRENO NO ABRE PUERTAS NI SE APLICA.

Lo que protege:
  Que la decision final de aplicar un cambio en disco use el veredicto que MANDA.
  Si el revisor de programa (_fallos_mecanicos) freno y guardo
  "RECHAZADO_POR_EL_PROGRAMA", ese veredicto manda sobre el del auditor.
  Un veredicto que el programa rechazo NO se aplica y NO dice LLAVE GUARDADA.

Lo visto el 2026-09-13 en una ronda real:
  arnes/candado_equipo.py::guardar_veredicto llamo al revisor de programa, encontro
  un fallo, cambio el veredicto a "RECHAZADO_POR_EL_PROGRAMA" y lo guardo asi.
  Pero ingeniero.py, comando equipo, IGNORO ese resultado: calculo v_final con el
  veredicto del AUDITOR y con eso APLICO el cambio en disco y dijo "LLAVE GUARDADA".
  Ese dia la salida dijo "EL REVISOR DE PROGRAMA FRENA ... EL CODIGO QUEDA ROTO"
  y a continuacion "APLICADO en disco".

La ley:
  Un veredicto que el programa rechazo no abre puertas ni se aplica.

Estas pruebas nacen ROJAS: la funcion veredicto_para_aplicar todavia no existe en
arnes/candado_equipo.py. Se implementara despues, con el equipo.
"""

import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import candado_equipo


def test_si_el_programa_frena_manda_el_programa():
    res = {"auditoria": {"veredicto": "APROBADO"}}
    guardado = {"veredicto": "RECHAZADO_POR_EL_PROGRAMA"}
    assert candado_equipo.veredicto_para_aplicar(res, guardado) == "RECHAZADO_POR_EL_PROGRAMA", \
        "el auditor aprobo, el programa freno, y se iba a aplicar codigo roto"


def test_sin_guardado_manda_el_auditor():
    assert candado_equipo.veredicto_para_aplicar({"auditoria": {"veredicto": " aprobado "}}, None) == "APROBADO", \
        "sin veredicto del programa, manda el del auditor, en mayusculas y sin espacios"


def test_sin_nada_no_se_inventa_una_aprobacion():
    assert candado_equipo.veredicto_para_aplicar({}, None) == "?", \
        "sin auditoria y sin guardado no se inventa una aprobacion: se devuelve ?"
    assert candado_equipo.veredicto_para_aplicar(None, None) == "?", \
        "sin res y sin guardado no se inventa una aprobacion: se devuelve ?"


def test_el_camino_real_guardar_y_decidir(monkeypatch, tmp_path):
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.setattr(candado_equipo, "AQUI", str(tmp_path))
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos",
                        lambda tarea, archivos=None: ["EL CODIGO QUEDA ROTO en el renglon 8"])
    guardado = candado_equipo.guardar_veredicto(
        "tarea", ["vigias/de_prueba.py"], "deepseek", "gemini4", "APROBADO")
    res = {"auditoria": {"veredicto": "APROBADO"}}
    assert candado_equipo.veredicto_para_aplicar(res, guardado) != "APROBADO", \
        "el revisor de programa freno y la decision final seguia diciendo APROBADO"
