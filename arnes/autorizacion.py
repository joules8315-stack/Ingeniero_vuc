# -*- coding: utf-8 -*-
"""arnes/autorizacion.py — APAGAR LOS CANDADOS SOLO JULIO, POR COMANDO Y CON AUTORIZACION.

Julio, 2026-08-24: "que solo pueda quitarlos yo, por medio de comando, en ps, y debe ser con
previa autorizacion."

Antes bastaba prender la variable INGENIERO_OFF=1 y los candados se apagaban en silencio (cualquiera
podia). Ahora NO: el unico camino para apagar es un COMANDO que deja una AUTORIZACION ESCRITA de
Julio, con fecha. Los candados solo se abren si esa autorizacion existe y es reciente (24h). Si no,
bloquean y dejan constancia.

Cómo apaga Julio (en PowerShell, una sola vez, dura 24h):
    cd C:\Ingeniero_VUC; python ingeniero.py autorizar-off "<motivo>"
"""
import os
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(AQUI, "memoria", ".autorizacion_off")
VIGENCIA_H = 24


def _marca():
    return os.environ.get("INGENIERO_AUTORIZACION_TEST") or MARCA


def autorizar(motivo):
    """Lo llama `ingeniero.py autorizar-off <motivo>` (SOLO Julio lo corre). Escribe la autorizacion."""
    os.makedirs(os.path.dirname(_marca()), exist_ok=True)
    with open(_marca(), "w", encoding="utf-8") as f:
        f.write("%s | %s" % (time.strftime("%Y-%m-%d %H:%M"), (motivo or "").strip()))
    return _marca()


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

