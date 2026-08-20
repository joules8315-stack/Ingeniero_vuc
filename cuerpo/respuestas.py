# -*- coding: utf-8 -*-
"""cuerpo/respuestas.py — ¿LA RESPUESTA SIRVIO? (Julio, 2026-08-20).

  "No solo que se respondio, despues falta evaluar si fue correcta la respuesta,
   de lo contrario de nada sirve"

Tiene razon, y es el error de siempre con otra cara: dar por buena una respuesta solo porque
existe es lo mismo que dar por probada una reparacion solo porque la vigia esta verde.

LA SEÑAL OBJETIVA, y la lleva diciendo Julio desde el primer dia:
**si tiene que repetir la instruccion, la respuesta NO sirvio.**
Eso si se puede medir sin opinar: se guarda cada pregunta con su respuesta, y si vuelve a
aparecer una pregunta parecida sobre el mismo asunto, la anterior queda marcada NO_SIRVIO.

Las tres formas de evaluar, de menos a mas fiable:
  1. AUTOMATICA  — la misma pregunta vuelve  -> NO_SIRVIO
  2. POR EL TRABAJO — se hizo lo que se pidio y las vigias quedaron verdes -> SIRVIO (probable)
  3. **DE JULIO** — `python ingeniero.py respuesta-ok / respuesta-mal` -> la unica que zanja (Ley 5)
"""
import os, sys, re, json, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
RUTA = os.path.join(AQUI, "memoria", "RESPUESTAS.json")


def _leer():
    try:
        return json.load(open(RUTA, encoding="utf-8"))
    except Exception:
        return []


def _guardar(d):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _palabras(t):
    from cerebro.trozos import _palabras as p, RUIDO      # misma funcion que el indice
    return {w for w in p(t or "") if w not in RUIDO}


def _parecidas(a, b, minimo=2):
    """Dos preguntas son 'la misma' si comparten al menos N palabras distintivas."""
    return len(_palabras(a) & _palabras(b)) >= minimo


def apuntar(pregunta, respuesta, proyecto=""):
    """Guarda que se pregunto y que contesto Julio. Nace SIN EVALUAR, nunca como buena.

    Si ya habia una pregunta parecida sin evaluar, esa queda marcada NO_SIRVIO: Julio esta
    teniendo que repetirse, que es justo lo que este sistema existe para evitar.
    """
    rs = _leer()
    repetidas = []
    for r in rs:
        if r["evaluacion"] == "PENDIENTE" and _parecidas(r["pregunta"], pregunta):
            r["evaluacion"] = "NO_SIRVIO"
            r["por_que"] = "Julio tuvo que volver a explicar lo mismo"
            repetidas.append(r["pregunta"])
    nueva = {
        "id": len(rs) + 1,
        "cuando": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "proyecto": proyecto,
        "pregunta": pregunta,
        "respuesta": respuesta,
        "evaluacion": "PENDIENTE",
        "por_que": "",
        "repitio_a": repetidas,
    }
    rs.append(nueva)
    _guardar(rs)
    return nueva


def evaluar(texto_pregunta, resultado, por_que=""):
    """resultado: SIRVIO | NO_SIRVIO. Lo pone Julio (o el trabajo, si quedo demostrado)."""
    rs = _leer()
    for r in reversed(rs):
        if texto_pregunta.lower() in r["pregunta"].lower() or _parecidas(r["pregunta"], texto_pregunta):
            r["evaluacion"] = resultado
            r["por_que"] = por_que or ("lo dijo Julio" if resultado else "")
            _guardar(rs)
            return r
    return None


def sin_evaluar():
    return [r for r in _leer() if r["evaluacion"] == "PENDIENTE"]


def resumen():
    rs = _leer()
    if not rs:
        return {"total": 0}
    ev = [r for r in rs if r["evaluacion"] != "PENDIENTE"]
    ok = [r for r in ev if r["evaluacion"] == "SIRVIO"]
    repeticiones = sum(len(r.get("repitio_a", [])) for r in rs)
    return {"total": len(rs), "evaluadas": len(ev),
            "sirvieron": len(ok),
            "acierto": round(len(ok) * 100 / len(ev), 1) if ev else None,
            "veces_que_julio_repitio": repeticiones,
            "pendientes": len(rs) - len(ev)}


def texto():
    r = resumen()
    if not r["total"]:
        return ("RESPUESTAS: todavia no se ha apuntado ninguna.\n"
                "  Se apuntan solas cuando el Ingeniero pregunta y Julio contesta.")
    L = ["¿LAS RESPUESTAS DE JULIO SIRVIERON? (memoria/RESPUESTAS.json)"]
    L.append("  preguntas hechas       : %d" % r["total"])
    if r["evaluadas"]:
        L.append("  respuestas que SIRVIERON: %s%%  (%d de %d evaluadas)"
                 % (r["acierto"], r["sirvieron"], r["evaluadas"]))
    L.append("  VECES QUE JULIO REPITIO : %d   <- si esto sube, el sistema esta fallando"
             % r["veces_que_julio_repitio"])
    if r["pendientes"]:
        L.append("  sin evaluar todavia    : %d" % r["pendientes"])
        for x in sin_evaluar()[-3:]:
            L.append("     - %s" % x["pregunta"][:90])
        L.append("  (evaluarlas: python ingeniero.py respuesta-ok / respuesta-mal \"<la pregunta>\")")
    return "\n".join(L)
