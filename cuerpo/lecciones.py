# -*- coding: utf-8 -*-
"""cuerpo/lecciones.py — F8 (punto h): registrar los ACIERTOS y las LECCIONES, fragmentados.

Julio, 2026-08-24 (punto h): "si se comete una equivocación, se registra; si es un acierto también,
debe sufrir el mismo proceso de fragmentación y asociación con una función de cada proyecto. Para
que esté disponible el paquete."

Los ERRORES ya viven en `fallos.py` (memoria/FALLOS.json). Esto registra los ACIERTOS: qué funcionó,
en qué pieza de qué proyecto, para que (como los fallos) queden disponibles como contexto en el
paquete y no se repita a ciegas ni se re-descubra lo que ya se sabe.

Registro: memoria/LECCIONES.json, fragmentado por proyecto -> pieza -> lista de lecciones.
"""
import json
import os
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "LECCIONES.json")


def _ruta():
    return os.environ.get("INGENIERO_LECCIONES_TEST") or RUTA


def _leer():
    try:
        return json.load(open(_ruta(), encoding="utf-8"))
    except Exception:
        return {}


def _guardar(d):
    os.makedirs(os.path.dirname(_ruta()), exist_ok=True)
    json.dump(d, open(_ruta(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def apuntar(proyecto, pieza, leccion):
    """Registra un acierto: qué funcionó en una pieza de un proyecto. Fragmentado por pieza."""
    if not leccion or not leccion.strip():
        return False
    d = _leer()
    d.setdefault(str(proyecto), {}).setdefault(str(pieza), [])
    d[str(proyecto)][str(pieza)].append({
        "leccion": leccion.strip()[:1000], "cuando": time.strftime("%Y-%m-%d %H:%M")})
    _guardar(d)
    return True


def de(proyecto, pieza=""):
    """Las lecciones de un proyecto (o de una pieza concreta). Para el paquete."""
    d = _leer()
    por_proyecto = d.get(str(proyecto), {})
    if not por_proyecto:
        return []
    if pieza:
        return por_proyecto.get(str(pieza), [])
    out = []
    for _p, lecs in por_proyecto.items():
        out.extend(lecs)
    return out


def texto_paquete(proyecto, pieza=""):
    """Bloque legible para el paquete: lo que YA se sabe que funciona aqui."""
    lecs = de(proyecto, pieza)
    if not lecs:
        return ""
    L = ["LO QUE YA FUNCIONA AQUI (aciertos, para no repetir ni re-descubrir):"]
    for l in lecs[-6:]:
        L.append("  - %s (%s)" % (l["leccion"][:200], l["cuando"]))
    return "\n".join(L) + "\n"


def total():
    return sum(len(v) for v in _leer().values() for p, l in v.items())
