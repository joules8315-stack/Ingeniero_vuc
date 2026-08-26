# -*- coding: utf-8 -*-
"""arnes/medir_precision.py — MIDE la PRECISION (acierto) REAL de cada cerebro, EN TERRENO.

Julio, 2026-08-25: medir la precision "en terreno, con la tarea real", para usar a los que sirven
y poner a descansar a los que no, y crear despues la regla de las tareas especificas. La vigia es
la que los hace precisos: este numero decide a quien se le confia la tarea y con que control.

TAREA DE CAMPO: ANALISIS DEL DMM (proponer campanas). Se le da a cada modelo los datos REALES de
SolarDemo (metricas_reales.json) y el perfil de marca (perfil_datos.json), y se le pide proponer
3 campanas. Se puntua con COMPROBACIONES OBJETIVAS y verificables (grounded, no opinion):
  1. usa_datos        -> menciona el canal real (Facebook) o las ventas/alcance dados.
  2. detecta_problema -> ve que todas las campanas dan 0 ventas (el fallo real de los datos).
  3. canales_marca    -> propone canales de la marca (Instagram/WhatsApp), no solo repetir Facebook.
  4. medible          -> alinea con 'medir contra ventas' (posicionamiento de DMM).
Sin inventar datos: se puntua si RESPONDE CON lo dado, no si inventa cifras.

Resultado en memoria/PRECISION.json: aciertos/4 por modelo para esta tarea. Los que saquen bajo
no se usan para esta tarea (se ponen a descansar) y se registra la regla de asignacion.
"""
import json
import os
import re
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

from cuerpo import obrero   # noqa: E402

RUTA = os.path.join(AQUI, "memoria", "PRECISION.json")

# La tarea de campo: analisis de campanas de SolarDemo con datos reales.
PROMPT_TAREA = (
    "Eres el gerente de marketing con IA de una empresa que SI vende, no el que promete; "
    "valoras honestidad y resultados medidos contra ventas, y trabajas con Instagram, "
    "Facebook y WhatsApp. Tienes los datos REALES de la ultima semana de SolarDemo: "
    "3 campanas, todas de 'Facebook Marketplace'. "
    "Campana 1: alcance 728, clics 68, interacciones 356, ventas 0. "
    "Campana 2: alcance 11, clics 11, interacciones 0, ventas 0. "
    "Campana 3: alcance 37, clics 37, interacciones 5, ventas 0. "
    "Propon 3 campanas para la proxima semana, cada una con: nombre, canal, objetivo y una "
    "linea que justifique la decision usando los datos. NO inventes datos que no estan."
)

# (clave, regex que detecta que SI cumplio esa comprobacion)
CHECKS = [
    ("usa_datos",        r"facebook|alcance|clics|728|ventas"),
    ("detecta_problema", r"0 ventas|sin ventas|no vend|no ha vendido|no esta vendiendo|todas.*0"),
    ("canales_marca",    r"instagram|whatsapp"),
    ("medible",          r"medir|contra ventas|ventas"),
]


def _preguntar(quien, modelo):
    if quien.startswith("gemini"):
        return obrero._gemini_directo(PROMPT_TAREA, 0.2, modelo)
    if quien.startswith("deepseek"):
        return obrero._deepseek_directo(PROMPT_TAREA, 0.2, modelo)
    if quien == "local":
        return obrero.preguntar_local(PROMPT_TAREA, 0.2)
    return obrero.prestar_cerebro()[0]._preguntar_groq(PROMPT_TAREA, modelo, 0.2)


def evaluar(texto):
    """Devuelve (aciertos, detalle) de las 4 comprobaciones objetivas."""
    aciertos = 0
    detalle = {}
    for clave, pat in CHECKS:
        ok = bool(re.search(pat, (texto or ""), re.I | re.S))
        detalle[clave] = ok
        aciertos += int(ok)
    return aciertos, detalle


def main():
    vel = obrero._velocidad()
    blancos = sys.argv[1:] or ["groq", "groq20b", "qwen", "gemini", "gemini2",
                               "gemini3", "deepseek", "local"]
    modelos = {
        "groq": vel.get("modelo_groq"), "groq20b": vel.get("modelo_groq20b"),
        "qwen": "qwen/qwen3.6-27b",
        "gemini": vel.get("modelo_gemini"), "gemini2": vel.get("modelo_gemini2"),
        "gemini3": vel.get("modelo_gemini3"),
        "deepseek": vel.get("modelo_deepseek"), "local": None,
    }
    datos = {}
    print("=== PRECISION EN TERRENO: tarea de analisis de campanas (SolarDemo) ===", flush=True)
    print("Comprobaciones: usa_datos | detecta_problema | canales_marca | medible\n", flush=True)
    for quien in blancos:
        if quien not in modelos:
            print("  desconocido: %s" % quien, flush=True)
            continue
        t0 = time.time()
        try:
            txt = _preguntar(quien, modelos[quien])
        except Exception as e:
            txt = "[FALLO %s]" % e
        aciertos, detalle = evaluar(txt)
        ok = "  ".join("%s:%s" % (k, "SI" if v else "no") for k, v in detalle.items())
        datos[quien] = {"aciertos": aciertos, "total": len(CHECKS),
                        "porcentaje": round(100.0 * aciertos / len(CHECKS), 1),
                        "detalle": detalle, "t": round(time.time() - t0, 1)}
        print("  %-9s %d/4  %s" % (quien, aciertos, ok), flush=True)
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(datos, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nGuardado en " + RUTA + "  (acierto real por modelo en la tarea de analisis de campanas).")
    print("Regla sugerida: los con >=3/4 se usan para analisis; los de menos se ponen a descansar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
