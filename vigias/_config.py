# -*- coding: utf-8 -*-
"""Helper de vigias: leer la config de hooks EFECTIVA de Claude.

Julio, 2026-08-27: se pidio autorizacion DOS veces para lo mismo porque el arnes estaba
duplicado en DOS settings activos a la vez (el de usuario ~/.claude/settings.json y el del
proyecto .claude/settings.json). La fuente canonica es el USUARIO (el arnes del Ingeniero
vigila todos los proyectos). El proyecto solo tiene lo suyo (candados de cierre).

Estas funciones devuelven la config COMBINADA (usuario + proyecto) para que las vigias
comprueben que un candado SIGA conectado viva donde viva, sin asumir una sola capa.
"""
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def leer_capas():
    """Devuelve lista de dicts de settings: [usuario, proyecto] (los que existan)."""
    capas = []
    usr = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")
    if os.path.exists(usr):
        try:
            capas.append(json.load(open(usr, encoding="utf-8")))
        except Exception:
            pass
    proy = os.path.join(AQUI, ".claude", "settings.json")
    if os.path.exists(proy):
        try:
            capas.append(json.load(open(proy, encoding="utf-8")))
        except Exception:
            pass
    return capas


def comandos(tipo):
    """Todos los comandos de hooks del tipo dado (PreToolUse/Stop/UserPromptSubmit...), en
    cualquier capa. Devuelve (matcher, comando) por cada hook."""
    out = []
    for s in leer_capas():
        for e in s.get("hooks", {}).get(tipo, []):
            m = e.get("matcher", "")
            for h in e.get("hooks", []):
                out.append((m, h.get("command", "")))
    return out


def comandos_de(tipo, nombre):
    """True si un candado (nombre) aparece conectado en el tipo de hook, en cualquier capa."""
    return any(nombre in c for _, c in comandos(tipo))
