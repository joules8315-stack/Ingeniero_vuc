# -*- coding: utf-8 -*-
"""cerebro/enlaces.py — LOS HILOS del cerebro (esto es lo que lo hace tipo Obsidian).

Un enlace dice QUIEN toca a QUIEN. Sin enlaces solo hay una lista de archivos;
con enlaces hay un mapa por el que se puede caminar y traer SOLO el vecindario.

Cuatro clases de hilo, todas sacadas del disco (nunca inventadas):
  IMPORTA  pieza  -> pieza    (el codigo se llama entre si)
  VIGILA   vigia  -> pieza    (que prueba protege que codigo)
  LEGISLA  contrato -> pieza  (que ley manda sobre que codigo)
  CITA     pieza  -> contrato (el codigo dice de que contrato nace)
"""
import os, re
from collections import defaultdict


def _texto(abs_path, tope=200_000):
    try:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(tope)
    except Exception:
        return ""


def tejer(fichas):
    """Devuelve la lista de enlaces {de, a, tipo}. Solo enlaces cuyos DOS extremos existen."""
    ids = {f["id"] for f in fichas}
    por_modulo = {}   # 'cuerpo.indice' / 'indice' -> id real
    for f in fichas:
        if f["id"].endswith(".py"):
            mod = f["id"][:-3].replace("/", ".")
            por_modulo[mod] = f["id"]
            por_modulo[mod.split(".")[-1]] = f["id"]
    contratos = {f["id"]: f for f in fichas if f["rol"] in ("CONTRATO", "MATRIZ", "PROTOCOLO")}

    enlaces = []
    vistos = set()

    def añadir(de, a, tipo):
        if de == a or a not in ids or de not in ids:
            return
        k = (de, a, tipo)
        if k in vistos:
            return
        vistos.add(k)
        enlaces.append({"de": de, "a": a, "tipo": tipo})

    for f in fichas:
        # --- IMPORTA / VIGILA: por los import del archivo ---
        for mod in f.get("importa", []):
            destino = por_modulo.get(mod) or por_modulo.get(mod.split(".")[-1])
            if destino:
                añadir(f["id"], destino, "VIGILA" if f["rol"] == "VIGIA" else "IMPORTA")

        txt = None
        # --- CITA: el codigo/vigia dice "Ver CONTRATO_X" ---
        if f["rol"] in ("CUERPO", "CODIGO", "VIGIA", "WEB", "CEREBRO", "ARNES"):
            txt = _texto(f["abs"])
            for m in re.finditer(r"((?:CONTRATO|MATRIZ|PROTOCOLO)[A-Z0-9_]*\.md)", txt):
                nombre = m.group(1)
                for cid in contratos:
                    if cid.split("/")[-1].upper() == nombre.upper():
                        añadir(f["id"], cid, "CITA")

        # --- LEGISLA: el contrato nombra un archivo de codigo ---
        if f["rol"] in ("CONTRATO", "MATRIZ", "PROTOCOLO", "DOC"):
            txt = _texto(f["abs"])
            for m in re.finditer(r"`?([\w/]+\.(?:py|html|sh|js))`?", txt):
                ref = m.group(1).lstrip("./")
                if ref in ids:
                    añadir(f["id"], ref, "LEGISLA")
                else:
                    base = ref.split("/")[-1]
                    cand = [i for i in ids if i.split("/")[-1] == base]
                    if len(cand) == 1:
                        añadir(f["id"], cand[0], "LEGISLA")

        # --- VIGILA por nombre: test_vigia_precios.py -> cuerpo/precios.py ---
        if f["rol"] == "VIGIA":
            base = f["id"].split("/")[-1][len("test_vigia_"):-3] if f["id"].split("/")[-1].startswith("test_vigia_") else ""
            if base:
                for cand in (f"cuerpo/{base}.py", f"cerebro/{base}.py"):
                    if cand in ids:
                        añadir(f["id"], cand, "VIGILA")

    # --- FUERZA del hilo: cuanto manda de verdad este doc sobre esta pieza.
    # Dos reglas, las mismas que usaria un humano:
    #  1) CASTIGO AL MAPA: un doc que nombra 200 archivos no manda sobre ninguno en particular.
    #     Solo se castiga a partir de 10 (los contratos normales nombran pocas piezas).
    #  2) PREMIO AL DUENO: si el doc se llama CONTRATO_PRECIOS y la pieza es precios.py,
    #     ese es SU contrato. Manda mas que cualquier otro que la mencione de pasada.
    salidas = defaultdict(int)
    for e in enlaces:
        if e["tipo"] in ("LEGISLA", "CITA"):
            salidas[e["de"]] += 1

    def _base(pid):
        return os.path.splitext(pid.split("/")[-1])[0].lower().replace("test_vigia_", "")

    for e in enlaces:
        if e["tipo"] in ("LEGISLA", "CITA"):
            n = salidas[e["de"]]
            f = 1.0 if n <= 10 else round(10.0 / n, 4)
            doc, pieza = _base(e["de"]), _base(e["a"])
            doc_limpio = doc.replace("contrato_", "").replace("contratos_", "")
            if pieza and (pieza in doc_limpio.split("_") or doc_limpio == pieza):
                f += 2.0   # es SU dueno: gana a todos
            e["fuerza"] = round(f, 4)
        else:
            e["fuerza"] = 3.0  # importar y vigilar son hilos DUROS: nunca se descartan
    return enlaces


def indexar(enlaces):
    """Dos diccionarios para caminar el grafo rapido: hacia adelante y hacia atras."""
    sale = defaultdict(list)
    entra = defaultdict(list)
    for e in enlaces:
        sale[e["de"]].append(e)
        entra[e["a"]].append(e)
    return sale, entra
