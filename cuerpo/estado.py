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


def leer():
    try:
        d = json.load(open(RUTA, encoding="utf-8"))
        for k, v in VACIO.items():
            d.setdefault(k, v)
        return d
    except Exception:
        return dict(VACIO)


def guardar(d):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
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
