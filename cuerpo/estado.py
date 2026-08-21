# -*- coding: utf-8 -*-
"""cuerpo/estado.py — LA MEMORIA DEL TRABAJO (para que Julio no repita).

El estado NO vive en el chat. Si vive en el chat, al cerrarse se pierde y Julio tiene que
volver a contar todo. Vive aqui, en disco, y sobrevive a que se cierre la sesion, se acabe
el saldo o se cambie de IA.
"""
import os, json, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "ESTADO.json")

VACIO = {
    "proyecto": "", "problema": "", "flujos": [], "paquete": "",
    "decision_pendiente": "", "vigias_antes": "", "vigias_despues": "",
    "prueba_humana": "PENDIENTE", "ultimo_sello": "", "historial": [],
}


def _ruta():
    """La de verdad, o una de prueba.

    Las comprobaciones escribian en el estado REAL, y cuando dos corridas coincidian se pisaban
    entre ellas: salian rojas sin que nada estuviera roto, y el guardia de cierre no dejaba
    terminar por un susto falso (fallo real 2026-08-21). Ahora cada prueba usa su copia.
    """
    return os.environ.get("INGENIERO_ESTADO_TEST") or RUTA


def leer():
    try:
        d = json.load(open(_ruta(), encoding="utf-8"))
        for k, v in VACIO.items():
            d.setdefault(k, v)
        return d
    except Exception:
        return dict(VACIO)


def guardar(d):
    os.makedirs(os.path.dirname(_ruta()), exist_ok=True)
    json.dump(d, open(_ruta(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def apuntar(**cambios):
    d = leer()
    hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    for k, v in cambios.items():
        if k in d and d[k] != v:
            d["historial"].append({"cuando": hoy, "campo": k, "de": str(d[k])[:60], "a": str(v)[:60]})
        d[k] = v
    d["historial"] = d["historial"][-60:]
    return guardar(d)


def respondida(texto_pregunta=None):
    """Marca una pregunta como YA CONTESTADA por Julio.

    Hacia falta (fallo real 2026-08-20): el candado de cierre no dejaba terminar por preguntas
    que ya estaban respondidas, y no habia forma legitima de cerrarlas salvo apagar el candado
    entero. Un candado sin forma honrada de satisfacerlo empuja a saltarselo, y eso es peor
    que no tenerlo.

    Sin argumento las cierra todas. Con argumento, solo la que coincida.
    """
    d = leer()
    actual = d.get("decision_pendiente", "")
    if not actual:
        return d
    if not texto_pregunta:
        return apuntar(decision_pendiente="")
    quedan = [p.strip() for p in actual.split("|")
              if p.strip() and texto_pregunta.lower() not in p.lower()]
    return apuntar(decision_pendiente=" | ".join(quedan))


def texto():
    d = leer()
    L = ["ESTADO DEL TRABAJO (memoria/ESTADO.json)"]
    L.append(f"  proyecto            : {d['proyecto'] or '(ninguno)'}")
    L.append(f"  problema            : {d['problema'] or '(ninguno)'}")
    L.append(f"  flujos              : {', '.join(d['flujos']) or '-'}")
    L.append(f"  paquete vigente     : {os.path.basename(d['paquete']) if d['paquete'] else '(ninguno)'}")
    L.append(f"  vigias antes/despues: {d['vigias_antes'] or '?'} / {d['vigias_despues'] or '?'}")
    L.append(f"  PRUEBA HUMANA       : {d['prueba_humana']}   <- solo Julio la pone en HECHA")
    if d["decision_pendiente"]:
        L.append(f"  *** PREGUNTA PENDIENTE PARA JULIO: {d['decision_pendiente']}")
    return "\n".join(L)
