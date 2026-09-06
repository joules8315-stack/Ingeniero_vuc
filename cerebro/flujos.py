# -*- coding: utf-8 -*-
"""cerebro/flujos.py — CAPA 1 del cerebro: los FLUJOS (los asuntos del proyecto).

Un FLUJO es un asunto del negocio: "precios", "onboarding", "plantilla", "roles".
Existe porque los hilos literales no alcanzan: `CONTRATO_PERFIL_Y_MULTIEMPRESA.md`
manda sobre `cuerpo/perfil.py` aunque NUNCA escriba ese nombre de archivo.
El flujo los junta por ASUNTO.

Dos vias, y la de Julio siempre gana:
  1) DECLARADA — `flujos.config` en la carpeta del proyecto (lo que Julio dice).
  2) DEDUCIDA  — del nombre de las piezas (cuando nadie declaro nada).
"""
import os, re

RUIDO = {"py", "md", "test", "vigia", "contrato", "contratos", "cuerpo", "web", "de", "del",
         "la", "el", "los", "las", "y", "e", "en", "un", "una", "por", "con", "para", "sh",
         "html", "json", "txt", "auto", "maestro", "mvp", "mvp2", "dmm", "app", "main",
         "que", "solo", "se", "no", "si", "lo", "su", "sus", "mas", "ya", "esta", "estan", "son",
         "hay", "sin", "sobre", "cuando", "porque", "todo", "toda", "cada", "este", "esta", "ese",
         "esa", "muy", "tambien", "pero", "como", "donde", "quien", "cual", "algo", "otro", "otra",
         "hacer", "ser", "tiene", "puede"}


def _tokens(pid):
    base = os.path.splitext(pid.split("/")[-1])[0].lower()
    base = re.sub(r"^test_vigia_|^contratos?_", "", base)
    return [t for t in re.split(r"[_\-\.]+", base) if t and t not in RUIDO and len(t) > 2]


def declarados(raiz):
    """Lee flujos.config del proyecto:  F3 plantilla = plantilla, docx, tabla"""
    ruta = os.path.join(raiz, "flujos.config")
    out = {}
    if not os.path.exists(ruta):
        return out
    for ln in open(ruta, encoding="utf-8", errors="ignore").read().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "=" not in ln:
            continue
        nombre, claves = ln.split("=", 1)
        out[nombre.strip()] = [c.strip().lower() for c in claves.split(",") if c.strip()]
    return out


def detectar(fichas, raiz=None):
    """Devuelve {nombre_flujo: {claves, piezas, declarado}}. El nucleo de cada flujo es
    un modulo del cuerpo; a su alrededor se pegan su contrato, sus vigias y su web."""
    flujos = {}

    # 1) Los que Julio declaro mandan.
    if raiz:
        for nombre, claves in declarados(raiz).items():
            flujos[nombre] = {"claves": claves, "piezas": [], "declarado": True}

    # 2) Los deducidos: un flujo por cada modulo del cuerpo/codigo nucleo.
    for f in fichas:
        if f["rol"] in ("CUERPO", "CEREBRO"):
            base = os.path.splitext(f["id"].split("/")[-1])[0].lower()
            if base in ("__init__", "config"):
                continue
            if not any(base in fl["claves"] for fl in flujos.values()):
                flujos.setdefault(base, {"claves": [base], "piezas": [], "declarado": False})

    # 2b) Flujos que NO tienen modulo propio pero SI tienen ley y vigias.
    #     Caso real: "onboarding" no es un cuerpo/onboarding.py, pero tiene 2 contratos y 6 vigias.
    #     Sin esto, el asunto mas importante del proyecto quedaba invisible para el router.
    from collections import Counter
    cuenta = Counter()
    for f in fichas:
        if f["rol"] in ("CONTRATO", "VIGIA", "MATRIZ", "WEB", "CODIGO"):
            for t in _tokens(f["id"]):
                cuenta[t] += 1
    for tok, n in cuenta.items():
        if n >= 3 and not any(tok in fl["claves"] for fl in flujos.values()):
            flujos[tok] = {"claves": [tok], "piezas": [], "declarado": False}

    # 3) Repartir TODAS las piezas entre los flujos, por asunto.
    for f in fichas:
        toks = set(_tokens(f["id"]))
        if not toks:
            continue
        for nombre, fl in flujos.items():
            if toks & set(fl["claves"]):
                fl["piezas"].append(f["id"])

    for fl in flujos.values():
        fl["piezas"] = sorted(set(fl["piezas"]))
    return flujos


def buscar(flujos, consulta):
    """Del texto del problema saca los flujos que tocan. Devuelve [(nombre, puntaje)]."""
    q = set(re.split(r"[^\wáéíóúñ]+", consulta.lower())) - RUIDO
    hits = []
    for nombre, fl in flujos.items():
        p = 0
        for clave in fl["claves"]:
            if clave in q:
                p += 3
            elif any(clave in w or w in clave for w in q if len(w) > 3):
                p += 1
        if fl["declarado"] and p:
            p += 2
        if nombre.lower() in consulta.lower():
            p += 3
        if p:
            hits.append((nombre, p))
    return sorted(hits, key=lambda x: -x[1])
