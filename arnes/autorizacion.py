# -*- coding: utf-8 -*-
"""arnes/autorizacion.py — APAGAR LOS CANDADOS SOLO JULIO, CON SU LLAVE SECRETA.

Julio, 2026-08-24: "que solo pueda quitarlos yo, por medio de comando, en ps, y debe ser con
previa autorizacion."
Julio, 2026-08-26: "SOLO YO AUTORIZO." Antes bastaba correr `autorizar-off` y la autorizacion se
escribia sola: CUALQUIER IA podia autorizarse a si misma. Ahora `autorizar-off` exige la LLAVE
SECRETA de Julio. Sin la llave correcta, REFUSA y no abre. La llave vive FUERA del repo, en el
perfil de Julio (`~/.ingeniero_julio_llave`), que el crea a mano; ninguna IA la conoce.

Antes bastaba prender la variable INGENIERO_OFF=1 y los candados se apagaban en silencio
(cualquiera podia). Ahora NO: el unico camino es un comando con la llave de Julio que deja una
AUTORIZACION ESCRITA, con fecha. Los candados solo se abren si esa autorizacion existe y es
reciente (24h). Si no, bloquean y dejan constancia.

Como apaga Julio (en PowerShell, una sola vez, dura 24h):
    1) una vez, crear su llave fuera del repo:
         Set-Content $env:USERPROFILE\.ingeniero_julio_llave '<su secreto>'
    2) cuando lo necesite:
         python ingeniero.py autorizar-off "<motivo>" "<su secreto>"
"""
import os
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(AQUI, "memoria", ".autorizacion_off")
VIGENCIA_H = 24

# Llave de prueba SOLO para las vigias; NUNCA se usa en produccion.
SECRETO_TEST = "ing-julio-prueba-2026"


def _marca():
    return os.environ.get("INGENIERO_AUTORIZACION_TEST") or MARCA


def _ruta_secreto():
    """La llave de Julio: fuera del repo. Solo en pruebas se apunta a un temporal."""
    t = os.environ.get("INGENIERO_LLAVE_JULIO_TEST")
    if t:
        return t
    return os.path.join(os.path.expanduser("~"), ".ingeniero_julio_llave")


def _secreto_esperado():
    try:
        with open(_ruta_secreto(), encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def sembrar_secreto_test(tmp_dir):
    """PARA VIGIAS: escribe la llave de prueba en un temporal y la apunta. Devuelve el secreto."""
    ruta = os.path.join(str(tmp_dir), ".llave_julio_test")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(SECRETO_TEST)
    os.environ["INGENIERO_LLAVE_JULIO_TEST"] = ruta
    return SECRETO_TEST


def autorizar(motivo, llave=""):
    """Solo Julio autoriza: exige SU llave secreta. Sin la llave correcta, REFUSA y no abre.

    Devuelve {"ok": ruta} si autorizo, o {"_error": motivo} si se denego o falta la llave.
    """
    esperada = _secreto_esperado()
    if not esperada:
        return {"_error": "NO AUTORIZADO: falta la llave de Julio. Solo Julio la crea, fuera del "
                          "repo (~/.ingeniero_julio_llave); sin ella nadie puede apagar."}
    if not llave or llave.strip() != esperada:
        return {"_error": "AUTORIZACION DENEGADA: la llave no coincide. SOLO Julio autoriza."}
    os.makedirs(os.path.dirname(_marca()), exist_ok=True)
    with open(_marca(), "w", encoding="utf-8") as f:
        f.write("%s | %s" % (time.strftime("%Y-%m-%d %H:%M"), (motivo or "").strip()))
    return {"ok": _marca()}


def autorizada():
    """¿Hay autorizacion escrita, vigente y reciente de Julio para apagar los candados?"""
    try:
        if time.time() - os.path.getmtime(_marca()) <= VIGENCIA_H * 3600:
            return True
    except OSError:
        pass
    return False


def estado():
    try:
        if autorizada():
            return "candados APAGADOS por autorizacion de Julio (vigente 24h)"
    except Exception:
        pass
    return "candados ACTIVOS (no hay autorizacion vigente de Julio)"

