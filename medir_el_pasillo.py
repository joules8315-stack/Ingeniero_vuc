# -*- coding: utf-8 -*-
"""MIDE el pasillo de verdad: que sale de armar_encargo y que le llega al cerebro.
Reproduce el caso real del 2026-09-09 (7.575 mandadas, 35.845 llegadas). Temporal."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
sys.path.insert(0, AQUI)

import asignador  # noqa: E402

TOPE = asignador.TOPE_LETRAS
objetivo_real = "x" * 7575          # lo que Julio mando (medido, f0d6ada)
material_real = "y" * 34460         # el paquete medido (ULTIMO_TRABAJO_DEL_EQUIPO.json)

enc = asignador.armar_encargo({"objetivo": objetivo_real, "prueba": "resolver"},
                              material=material_real)

print("TOPE_LETRAS declarado ................ %d" % TOPE)
print("objetivo que entra ................... %d" % len(objetivo_real))
print("material que entra ................... %d" % len(material_real))
print("ENCARGO que sale de armar_encargo .... %d" % len(enc))
print("  -> cumple el tope? ................. %s" % (len(enc) <= TOPE))
print("  -> se pasa por ..................... %d letras" % max(0, len(enc) - TOPE))

print("")
print("AHORA lo que de verdad se le manda al cerebro (trabajar usa _prompt_obrero):")
try:
    from cuerpo import obrero
    prompt = obrero._prompt_obrero(enc, objetivo_real, "reparar")
    print("PROMPT que llega al cerebro ........... %d" % len(prompt))
    print("  -> aguanta el gratis mas pequeno (19042)? %s" % (len(prompt) <= 19042))
    print("  -> factor de inflado desde el encargo: x%.2f" % (len(prompt) / max(1, len(enc))))
    print("  -> factor de inflado desde lo mandado: x%.2f" % (len(prompt) / len(objetivo_real)))
except Exception as e:
    print("no se pudo medir _prompt_obrero:", str(e)[:200])
