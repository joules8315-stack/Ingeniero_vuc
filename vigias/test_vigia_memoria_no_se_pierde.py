# -*- coding: utf-8 -*-
"""VIGIA 20 — LA MEMORIA DE ERRORES NO SE PIERDE NUNCA (2026-08-21).

Lo que paso: mientras se aislaban las comprobaciones para que no se pisaran, **una escribio su
copia vacia encima de la memoria real y se perdieron 27 de los 32 errores aprendidos**. Se
recuperaron del guardado anterior, pero el susto fue real: la memoria de errores es lo unico que
impide repetir lo ya vivido, y estuvo a un guardado de desaparecer.

Se detecto por una cifra que BAJO sin explicacion: "errores que avisan: 8" paso a 5. Un numero
que baja solo, sin que nadie borre nada a proposito, siempre es un fallo.

Lo que se vigila aqui:
  · que la memoria nunca quede vacia ni encoja de golpe
  · que ninguna comprobacion escriba en la memoria de verdad
  · que los errores mas valiosos (los que ya avisan) sigan ahi
"""
import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import pytest
from cuerpo import fallos

MINIMO = 25          # ya se habian aprendido mas de 30; si baja de aqui, algo se perdio


def _reales():
    """Los errores de verdad, sin desvios de prueba."""
    ruta = os.path.join(AQUI, "memoria", "FALLOS.json")
    try:
        return json.load(open(ruta, encoding="utf-8"))
    except Exception:
        return []


def test_la_memoria_de_errores_no_esta_vacia():
    fs = _reales()
    assert fs, "LA MEMORIA DE ERRORES ESTA VACIA: se ha perdido todo lo aprendido"


def test_no_ha_encogido_de_golpe():
    """El aviso que dio la alarma: una cifra que baja sola siempre es un fallo."""
    fs = _reales()
    assert len(fs) >= MINIMO, (
        "la memoria tiene %d errores y deberia tener al menos %d: se perdio lo aprendido"
        % (len(fs), MINIMO))


def test_siguen_los_errores_que_YA_AVISAN():
    """Los que llevan disparador son los mas valiosos: son los que frenan antes de repetir."""
    con = [f for f in _reales() if f.get("disparador")]
    assert len(con) >= 5, "quedan solo %d errores que avisen antes: se perdieron" % len(con)


def test_siguen_los_errores_mas_repetidos():
    """El de escribir codigo desde la terminal se cometio SEIS veces: no puede desaparecer."""
    texto = " ".join((f["que_paso"] + f["no_volver_a"]).lower() for f in _reales())
    for debe in ("terminal", "paquete", "asum"):
        assert debe in texto, "falta el error sobre '%s': la memoria esta incompleta" % debe


def test_ninguna_comprobacion_escribe_en_la_memoria_real():
    """La causa del susto: una comprobacion escribio su copia encima de la de verdad."""
    ruta_real = os.path.join(AQUI, "memoria", "FALLOS.json")
    carpeta = os.path.join(AQUI, "vigias")
    culpables = []
    for f in os.listdir(carpeta):
        if not f.endswith(".py"):
            continue
        txt = open(os.path.join(carpeta, f), encoding="utf-8", errors="ignore").read()
        if "fallos.apuntar(" in txt or "fallos.sembrar(" in txt:
            # tiene que desviar la ruta antes de escribir
            if "INGENIERO_FALLOS_TEST" not in txt and "monkeypatch.setattr(fallos" not in txt:
                culpables.append(f)
    assert not culpables, (
        "estas comprobaciones escriben en la memoria REAL y pueden borrarla: %s" % culpables)


def test_se_puede_desviar_la_memoria_para_probar():
    """Sin desvio, cualquier prueba pisa la memoria de verdad."""
    import inspect
    assert "INGENIERO_FALLOS_TEST" in inspect.getsource(fallos), \
        "no hay forma de que una prueba use su propia copia"
