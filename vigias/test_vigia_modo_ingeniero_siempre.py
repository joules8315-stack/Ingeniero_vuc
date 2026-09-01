# -*- coding: utf-8 -*-
"""vigias/test_vigia_modo_ingeniero_siempre.py — SIEMPRE MODO INGENIERO.

Julio, 2026-08-21: "Haz pruebas, que siempre estes modo ingeniero."

Vigila que el modo ingeniero este SIEMPRE activo:
  1. Los hooks de modo_ingeniero estan puestos en el settings de Claude.
  2. No esta apagado por la variable INGENIERO_OFF.
  3. Hay un candado / modo que bloquea si no es ingeniero.

Si esta vigia se pone roja, es que alguien apago el modo ingeniero: hay que arreglarlo antes
de seguir, no se trabaja sin el.
"""
import sys, os, json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
SETTINGS = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")


def _settings():
    try:
        return json.load(open(SETTINGS, encoding="utf-8"))
    except Exception:
        return {}


def test_hooks_de_modo_ingeniero_puestos():
    """Los hooks del modo ingeniero deben estar en el settings de Claude."""
    s = json.dumps(_settings())
    assert "modo_ingeniero.py" in s, "faltan los hooks de modo_ingeniero en settings.json"


def test_no_apagado_por_variable():
    """INGENIERO_OFF no debe estar activo (si lo esta, el modo se apaga)."""
    assert not os.environ.get("INGENIERO_OFF", "").strip(), \
        "INGENIERO_OFF esta puesto: el modo ingeniero esta apagado"


def test_hay_algo_que_bloquea_sin_modo_ingeniero():
    """Debe haber un candado o el modo ingeniero enganchado para no escribir sin el."""
    s = json.dumps(_settings())
    assert ("modo_ingeniero" in s) or ("candado_ingeniero" in s), \
        "no hay nada que fuerce el modo ingeniero en settings.json"


# ─── EL MODO INGENIERO ES EL ARNES DE CUALQUIER IA, EN CUALQUIER PROYECTO (Julio, 2026-09-02).
# "Todo lo que trabaje aqui debe estar en modo ingeniero, nada trabaja de manera diferente, y todo
# lo que envie a reparar (MVP, DMM, cualquier aplicacion) debe arrancar por modo ingeniero. No es
# una sugerencia: asi, y solo asi debe trabajar."
CLINERULES_USUARIO = os.path.join(os.path.expanduser("~"), ".clinerules", "modo_ingeniero.md")
PROYECTOS_CFG = os.path.join(AQUI, "proyectos.config")


def _proyectos_registrados():
    """Los proyectos que viven en proyectos.config: (apodo, ruta)."""
    out = []
    try:
        for linea in open(PROYECTOS_CFG, encoding="utf-8"):
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea or "|" not in linea:
                continue
            apodo = linea.split("=", 1)[0].strip()
            ruta = linea.split("=", 1)[1].split("|", 1)[0].strip()
            if apodo and ruta:
                out.append((apodo, ruta))
    except Exception:
        pass
    return out


def test_cline_tiene_modo_ingeniero_a_nivel_usuario():
    """Cline tambien debe estar en modo ingeniero en CUALQUIER proyecto, no solo en Ingeniero_VUC.
    Sin las reglas de usuario, Cline trabaja sin arnes fuera de aqui."""
    assert os.path.exists(CLINERULES_USUARIO), (
        "Cline no tiene modo_ingeniero a nivel usuario (~/.clinerules/modo_ingeniero.md): "
        "fuera de Ingeniero_VUC no trabaja con el arnes")


def test_todos_los_proyectos_registrados_arrancan_por_modo_ingeniero():
    """Todo proyecto registrado debe arrancar por modo ingeniero: bloque en CLAUDE.md + candado de
    lectura + reglas de Cline. Asi, y solo asi se trabaja en ellos."""
    comprobados = 0
    for apodo, ruta in _proyectos_registrados():
        if not os.path.isdir(ruta):
            continue                          # no esta en esta maquina: no se puede comprobar
        comprobados += 1
        md = os.path.join(ruta, "CLAUDE.md")
        texto = open(md, encoding="utf-8").read() if os.path.exists(md) else ""
        assert "INGENIERO_VUC:INICIO" in texto, \
            "%s no tiene el bloque de modo ingeniero en su CLAUDE.md" % apodo
        cr = os.path.join(ruta, ".clinerules", "modo_ingeniero.md")
        assert os.path.exists(cr), \
            "%s no tiene .clinerules/modo_ingeniero.md (Cline sin arnes ahi)" % apodo
    # El candado de lectura (read_gate) es canonico a nivel USUARIO: cubre a todos los proyectos.
    # Si esta en el proyecto TAMBIEN, el arnes se duplica y se pide permiso dos veces (medido el
    # 2026-08-27). Por eso no se exige por proyecto: se exige en el settings de usuario.
    s_usr = json.dumps(_settings())
    assert "read_gate" in s_usr, \
        "el candado de lectura no esta a nivel usuario (~/.claude/settings.json)"
    assert comprobados >= 1, "no se pudo comprobar ningun proyecto registrado"

