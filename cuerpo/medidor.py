# -*- coding: utf-8 -*-
"""cuerpo/medidor.py — MIDE SI EL PAQUETE ACERTO (Julio, 2026-08-20).

  "1) Medir el acierto  2) Aprender de los aciertos y errores  3) Que el router se corrija solo"

NO es el medidor de tokens de DMM (`cuerpo/medidor.py` de Asesor Marketing, julio 2026), que
mide el GASTO. Ese ya existe y mide otra cosa. Este mide el ACIERTO: ¿el paquete traia lo que
hacia falta, o se quedo corto?

POR QUE ES LA PIEZA QUE FALTABA: hasta hoy se podia decir "ahorra el 99%" porque se conto, pero
NO se podia decir "acierta el 90%" porque nunca se midio. Y el 2026-08-20 se descubrio que
fallaba —traia el motor y no la pantalla— y lo cazaron Qwen y Gemini, no las 26 vigias verdes.
Sin medir, todo lo demas es fe.

COMO SE SABE SI ACERTO, SIN MOLESTAR A JULIO (señales que deja el propio trabajo):
  · el obrero pidio NECESITO_LEER          -> el paquete se quedo CORTO
  · el obrero contesto NO_ENCONTRADO       -> el paquete se quedo CORTO
  · el obrero pregunto PREGUNTA_REQUERIDA  -> faltaba una decision, no material (no cuenta)
  · el juez APROBO                         -> el paquete SIRVIO
  · el juez dijo que se invento algo       -> sospechoso: quiza faltaba material
  · Julio marco la prueba humana HECHA     -> **el unico acierto que vale de verdad** (Ley 5)

Todo queda en `memoria/MEDICIONES.json`, que sobrevive a cerrar la sesion.
"""
import os, sys, json, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
RUTA = os.path.join(AQUI, "memoria", "MEDICIONES.json")


def _ruta():
    """La de verdad, o una de prueba. Cada comprobacion usa su copia (ley 23)."""
    return os.environ.get("INGENIERO_MEDICIONES_TEST") or RUTA


def _leer():
    try:
        return json.load(open(_ruta(), encoding="utf-8"))
    except Exception:
        return []


def _guardar(d):
    os.makedirs(os.path.dirname(_ruta()), exist_ok=True)
    json.dump(d, open(_ruta(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def apuntar_paquete(pk, texto):
    """Se llama al armar un paquete. Guarda QUE trajo, para poder juzgarlo despues."""
    ms = _leer()
    m = {
        "id": len(ms) + 1,
        "cuando": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "proyecto": pk.get("apodo"),
        "problema": pk.get("problema"),
        "flujos": [f for f, _ in pk.get("flujos", [])],
        "piezas": [f["id"] for f in pk.get("codigo", [])],
        "trozos": [t["direccion"] for t in pk.get("trozos", [])],
        "leyes": [f["id"] for f in pk.get("leyes", [])],
        "vigias": [f["id"] for f in pk.get("vigias", [])],
        "lineas_paquete": len(texto.splitlines()),
        "lineas_proyecto": pk.get("total_proyecto", 0),
        "veredicto": "SIN_JUZGAR",
        "por_que": "",
        "falto": [],
        "prueba_humana": "PENDIENTE",
    }
    m["ahorro"] = round(100 - m["lineas_paquete"] * 100 / max(1, m["lineas_proyecto"]), 1)
    ms.append(m)
    _guardar(ms)
    return m


def _ultimo_de(proyecto, problema):
    for m in reversed(_leer()):
        if m["proyecto"] == proyecto and m["problema"] == problema:
            return m
    return None


def juzgar(proyecto, problema, resultado):
    """Se llama tras el trabajo cruzado. Deduce si el paquete SIRVIO, sin preguntarle a Julio."""
    ms = _leer()
    m = None
    for x in reversed(ms):
        if x["proyecto"] == proyecto and x["problema"] == problema:
            m = x
            break
    if not m:
        return None

    p = (resultado or {}).get("propuesta") or {}
    j = (resultado or {}).get("juez_dice") or {}
    crudo = json.dumps(resultado, ensure_ascii=False).upper()

    falto, veredicto, por_que = [], "SIN_JUZGAR", ""

    if "NECESITO_LEER" in crudo:
        veredicto, por_que = "CORTO", "el obrero tuvo que pedir mas material"
        falto = [str(x) for x in (p.get("preguntas") or [])][:3]
    elif str(p.get("diagnostico", "")).strip().upper() == "NO_ENCONTRADO":
        veredicto, por_que = "CORTO", "el obrero no encontro en el paquete con que responder"
        falto = [str(x) for x in (p.get("preguntas") or [])][:3]
    elif j.get("invento_algo"):
        veredicto, por_que = "SOSPECHOSO", "el obrero se invento cosas: quiza faltaba material"
        falto = [str(x) for x in (j.get("que_invento") or [])][:3]
    elif (j.get("veredicto") or "").upper() == "APROBADO":
        veredicto, por_que = "SIRVIO", "el juez aprobo la reparacion hecha con este paquete"
    elif (j.get("veredicto") or "").upper() == "RECHAZADO":
        veredicto, por_que = "NO_CONCLUYENTE", "rechazada, pero por la reparacion, no por el material"
    elif p.get("preguntas"):
        veredicto, por_que = "FALTO_DECISION", "no falto material: falto que Julio decidiera algo"

    m["veredicto"], m["por_que"], m["falto"] = veredicto, por_que, falto
    _guardar(ms)
    return m


def marcar_prueba_humana(proyecto, problema, resultado="HECHA"):
    """El unico acierto que vale de verdad (Ley 5). SOLO lo pone Julio, nunca una IA."""
    ms = _leer()
    for x in reversed(ms):
        if x["proyecto"] == proyecto and x["problema"] == problema:
            x["prueba_humana"] = resultado
            _guardar(ms)
            return x
    return None


def lo_que_falto(proyecto=None, k=8):
    """Lo que el router deberia haber traido y no trajo. Es la comida del auto-ajuste."""
    out = []
    for m in _leer():
        if proyecto and m["proyecto"] != proyecto:
            continue
        if m["veredicto"] in ("CORTO", "SOSPECHOSO") and m["falto"]:
            out.append({"proyecto": m["proyecto"], "flujos": m["flujos"], "falto": m["falto"]})
    return out[-k:]


def resumen(proyecto=None):
    ms = [m for m in _leer() if not proyecto or m["proyecto"] == proyecto]
    if not ms:
        return {"total": 0}
    juzgados = [m for m in ms if m["veredicto"] not in ("SIN_JUZGAR", "FALTO_DECISION")]
    sirvieron = [m for m in juzgados if m["veredicto"] == "SIRVIO"]
    cortos = [m for m in juzgados if m["veredicto"] == "CORTO"]
    humanas = [m for m in ms if m["prueba_humana"] == "HECHA"]
    return {
        "total": len(ms),
        "juzgados": len(juzgados),
        "acierto": round(len(sirvieron) * 100 / len(juzgados), 1) if juzgados else None,
        "cortos": len(cortos),
        "ahorro_medio": round(sum(m["ahorro"] for m in ms) / len(ms), 1),
        "probados_por_julio": len(humanas),
    }


def texto(proyecto=None):
    r = resumen(proyecto)
    if not r["total"]:
        return ("MEDIDOR DE ACIERTO: todavia no hay ninguna medicion.\n"
                "  Se llena solo al usar `python ingeniero.py trabaja` y `cruzado`.")
    L = ["MEDIDOR DE ACIERTO (memoria/MEDICIONES.json)"]
    L.append(f"  paquetes armados : {r['total']}")
    L.append(f"  ahorro medio     : {r['ahorro_medio']}%   <- esto ya se sabia")
    if r["juzgados"]:
        L.append(f"  ACIERTO          : {r['acierto']}%  ({r['juzgados']} juzgados, "
                 f"{r['cortos']} se quedaron cortos)   <- esto es lo que faltaba")
    else:
        L.append("  ACIERTO          : sin datos todavia (hace falta usar `cruzado`)")
    L.append(f"  probados por Julio: {r['probados_por_julio']}   <- el unico que vale de verdad")
    falt = lo_que_falto(proyecto)
    if falt:
        L.append("  LO QUE EL ROUTER NO TRAJO Y HACIA FALTA:")
        for f in falt[-4:]:
            L.append(f"    - flujo {','.join(f['flujos'][:2])}: {'; '.join(f['falto'])[:100]}")
    return "\n".join(L)
