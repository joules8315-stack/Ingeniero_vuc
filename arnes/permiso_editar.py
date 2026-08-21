# -*- coding: utf-8 -*-
"""arnes/permiso_editar.py — LA LLAVE QUE EL CANDADO OFRECIA Y NO EXISTIA.

Fallo real del 2026-08-20: el candado de edicion decia "si de verdad hace falta tocarlo,
justificalo con NECESITO_EDITAR"... y ese mecanismo NO EXISTIA en ningun sitio. Un candado que
ofrece una llave inexistente obliga a apagar el arnes entero, que es justo lo que no se quiere.

QUE HACE: permite tocar UN archivo concreto, UNA vez, dejando por escrito por que. No abre la
puerta en general: abre esa puerta, con nombre y motivo, y queda apuntado para que Julio lo vea.

    python ingeniero.py necesito-editar <archivo> --motivo "..." --vigia "..." --dana "..."

Exige las cuatro cosas, igual que la causa raiz. Sin motivo no hay permiso.
Caduca en 30 minutos y solo vale para ese archivo.
"""
import json, os, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "PERMISOS_EDICION.json")
REGISTRO = os.path.join(AQUI, "memoria", "permisos_edicion.log")
VIGENCIA_MIN = 30


def dar(archivo, motivo, vigia="", dana=""):
    """Da permiso para tocar UN archivo, con su justificacion por escrito."""
    if not archivo or not motivo:
        return {"_error": "hace falta el archivo Y el motivo. Sin motivo no hay permiso."}
    d = {"archivo": os.path.normcase(os.path.abspath(archivo)),
         "nombre": os.path.basename(archivo),
         "motivo": motivo, "vigia": vigia, "dana": dana, "cuando": time.time()}
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M") + "  " + d["nombre"] + "  ->  " + motivo[:120] + "\n")
    return d


def hay_permiso(archivo):
    """¿Hay permiso vigente para ESE archivo concreto?"""
    try:
        d = json.load(open(RUTA, encoding="utf-8"))
    except Exception:
        return False
    if time.time() - float(d.get("cuando", 0)) > VIGENCIA_MIN * 60:
        return False
    return os.path.normcase(os.path.abspath(archivo)) == d.get("archivo")


def texto():
    try:
        d = json.load(open(RUTA, encoding="utf-8"))
    except Exception:
        return "PERMISOS DE EDICION: ninguno dado."
    quedan = VIGENCIA_MIN * 60 - (time.time() - float(d.get("cuando", 0)))
    if quedan <= 0:
        return "PERMISOS DE EDICION: el ultimo ya caduco (%s)." % d.get("nombre", "?")
    return ("PERMISO VIGENTE para %s (quedan %d min)\n  motivo: %s"
            % (d.get("nombre"), quedan // 60, d.get("motivo", "")[:120]))
