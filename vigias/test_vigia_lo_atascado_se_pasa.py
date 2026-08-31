# -*- coding: utf-8 -*-
"""VIGIA — EL FOCO, LA TAREA QUE SE ASIGNA, Y LO ATASCADO QUE SE PASA.

Legisla tres ordenes de Julio del 2026-08-31 (CONTRATO_TRABAJO_CON_CLINE.md, puntos 0, 1 y 3):

  · "no vas a reparar a hacer pruebas del ingeniero reparando el MVP, seguimos afinando el
     ingeniero"                                                          -> el FOCO
  · "asignale tarea a cline"                                             -> se ASIGNA, no se ofrece
  · "asignale tarea a cline, esa que no has podido resolver y despues la supervisas"
                                                                          -> lo ATASCADO se pasa

No se mide que este escrito en el contrato (eso seria medir la promesa). Se mide sobre el
REPARTO DE VERDAD: a que proyecto van las tareas, si tienen dueno unico, y si lo que se atasco
cambio de manos dejando dicho por que.
"""
import io
import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

import reparto   # noqa: E402

LEY = os.path.join(AQUI, "CONTRATO_TRABAJO_CON_CLINE.md")

# Lo que NO se toca mientras el foco sea la herramienta.
PROYECTOS_DE_JULIO = ("foto_informe", "app_web", "dmm", "asesor marketing", "mvp")


def _tareas():
    if not os.path.exists(reparto.RUTA):
        return []
    with io.open(reparto.RUTA, encoding="utf-8") as f:
        return json.load(f)


def _ley():
    with io.open(LEY, encoding="utf-8") as f:
        return f.read()


def test_la_ley_recoge_las_tres_ordenes():
    t = _ley()
    assert "EL FOCO" in t, "no esta legislado el foco: se afina la herramienta, no el producto"
    assert "SE ASIGNA, NO SE OFRECE" in t, "no esta legislado que la tarea se asigna, no se ofrece"
    assert "SE LE PASA AL OTRO" in t, "no esta legislado que lo atascado se le pasa al otro"


def test_el_foco_se_respeta_en_el_reparto_de_verdad():
    """No vale decirlo: ninguna tarea viva puede ir contra el foco."""
    fuera = []
    for t in _tareas():
        if t.get("estado") not in ("asignada", "entregada", "a_corregir"):
            continue
        texto = (str(t.get("tarea", "")) + " " + " ".join(str(p) for p in t.get("piezas", []))).lower()
        for prohibido in PROYECTOS_DE_JULIO:
            if prohibido in texto:
                fuera.append(str(t.get("tarea", ""))[:70])
                break
    assert not fuera, (
        "hay tarea(s) vivas que tocan un proyecto de Julio en vez de la herramienta, y el foco "
        "dice que ahora se afina la herramienta: %s" % fuera[:3])


def test_cada_tarea_viva_tiene_un_solo_dueno():
    """Se ASIGNA. Dos duenos es trabajo pagado dos veces y un choque al guardar."""
    vistos = {}
    repetidas = []
    for t in _tareas():
        if t.get("estado") not in ("asignada", "entregada", "a_corregir"):
            continue
        tarea = str(t.get("tarea", ""))
        if tarea in vistos and vistos[tarea] != t.get("quien"):
            repetidas.append(tarea[:70])
        vistos[tarea] = t.get("quien")
    assert not repetidas, "hay tareas con dos duenos: %s" % repetidas[:3]


def test_lo_atascado_cambia_de_manos_y_queda_dicho_por_que():
    """Lo que uno no puede cerrar se le pasa al otro, y se apunta el motivo. Si no, se pierde."""
    pasadas = []
    for t in _tareas():
        for linea in (t.get("historial") or []):
            if "pasada de" in str(linea):
                pasadas.append((str(t.get("tarea", ""))[:50], str(linea)))
    if not pasadas:
        pytest.skip("todavia no se ha atascado ninguna tarea, no hay nada que medir")
    for tarea, linea in pasadas:
        assert len(linea) > 40, (
            "la tarea '%s' cambio de manos sin decir por que. Pasarla sin el motivo es tirarle "
            "el problema al otro, no repartir" % tarea)


def test_la_ley_exige_pasarla_CON_el_material():
    """Pasar una tarea sin el material es tirarsela encima. Eso ya se legislo."""
    t = _ley()
    assert "con todo el material" in t.lower(), \
        "la ley no exige pasar la tarea CON el material: el otro empezaria de cero"
    assert "quien la pasa la supervisa" in t.lower(), \
        "la ley no dice que quien pasa la tarea es quien la supervisa"
