# -*- coding: utf-8 -*-
"""VIGIA — la precision de los cerebros se mide EN TERRENO y queda guardada.

Julio, 2026-08-25: "de nada sirve tener una cantidad grande de contexto, si es impreciso... los
hacemos precisos justamente con los VIGIAS... siempre midiendo su verdadera capacidad... para crear
despues la regla de las tareas especificas que se le van a asignar."

`medir_capacidad` mide si el modelo RESPONDE (cuanto aguanta). `medir_precision` mide si ACIERTA
en una tarea real de analisis (proponer campanas con los datos reales de SolarDemo), con
comprobaciones objetivas y verificables. El resultado vive en memoria/PRECISION.json y decide a
quien se le confia cada tarea y a quien se pone a descansar.

Comprueba:
  · existe la herramienta de precision y tiene las 4 comprobaciones objetivas,
  · la medicion queda guardada (memoria/PRECISION.json) con los modelos evaluados,
  · la medicion es EN TERRENO (usa la tarea de analisis real, no solo un banco sintetico).
"""
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_existe_la_herramienta_de_precision():
    txt = _leer(os.path.join(AQUI, "arnes", "medir_precision.py"))
    assert txt, "falta arnes/medir_precision.py"
    assert "medir_capacidad" not in txt, "medir_precision no debe medir capacidad (esa es otra)"


def test_tiene_las_comprobaciones_objetivas_de_la_tarea():
    txt = _leer(os.path.join(AQUI, "arnes", "medir_precision.py"))
    for c in ("usa_datos", "detecta_problema", "canales_marca", "medible"):
        assert c in txt, f"medir_precision no comprueba '{c}'"
    assert "SolarDemo" in txt, "la tarea de campo debe usar los datos reales (no inventar)"


def test_la_medicion_queda_guardada():
    ruta = os.path.join(AQUI, "memoria", "PRECISION.json")
    assert os.path.exists(ruta), "falta memoria/PRECISION.json (medir_precision no se ha corrido)"
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except Exception as e:
        assert False, "PRECISION.json no es json: %s" % e
    assert d, "PRECISION.json esta vacio"
    # Debe tener al menos los modelos gratuitos principales.
    for m in ("groq", "gemini2", "qwen"):
        assert m in d, f"PRECISION.json no evaluo a {m}"
