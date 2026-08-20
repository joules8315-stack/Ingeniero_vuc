# -*- coding: utf-8 -*-
"""cerebro/grafo.py — EL CEREBRO ARMADO: junta las 4 capas y se acuerda.

Capas:
  0  PROYECTO — a quien atiende
  1  FLUJO    — los asuntos           (flujos.py)
  2  PIEZA    — los archivos          (piezas.py)
  3  TROZO    — los pedazos exactos   (trozos.py)
  +  HILOS    — quien toca a quien    (enlaces.py)

Se guarda en `memoria/grafos/<apodo>.json`. Escanear cuesta segundos; leerlo cuesta nada.
Se refresca solo cuando el proyecto cambia (huella de tamaños y fechas).
"""
import os, json, hashlib
from . import piezas, enlaces, flujos

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(AQUI, "memoria", "grafos")


def proyectos():
    """Lee proyectos.config: la libreta de direcciones del Ingeniero."""
    out = {}
    ruta = os.path.join(AQUI, "proyectos.config")
    if not os.path.exists(ruta):
        return out
    for ln in open(ruta, encoding="utf-8", errors="ignore").read().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or "=" not in ln:
            continue
        apodo, resto = ln.split("=", 1)
        partes = [p.strip() for p in resto.split("|")]
        out[apodo.strip()] = {
            "ruta": partes[0],
            "rama": partes[1] if len(partes) > 1 else "",
            "marca": partes[2] if len(partes) > 2 else "",
        }
    return out


def _huella(raiz):
    """Firma barata del proyecto: si no cambio, no se re-escanea."""
    h = hashlib.md5()
    for dp, dns, fns in os.walk(raiz):
        dns[:] = [d for d in dns if d not in piezas.EXCLUIR_DIR]
        for fn in sorted(fns):
            if os.path.splitext(fn)[1].lower() in piezas.EXCLUIR_EXT:
                continue
            try:
                st = os.stat(os.path.join(dp, fn))
                h.update(f"{fn}{st.st_size}{int(st.st_mtime)}".encode())
            except Exception:
                pass
    return h.hexdigest()


def construir(raiz, apodo="proyecto"):
    fichas = piezas.escanear(raiz)
    hilos = enlaces.tejer(fichas)
    fl = flujos.detectar(fichas, raiz)
    return {
        "apodo": apodo, "raiz": os.path.abspath(raiz), "huella": _huella(raiz),
        "piezas": fichas, "enlaces": hilos, "flujos": fl,
        "resumen": {"piezas": len(fichas), "enlaces": len(hilos), "flujos": len(fl),
                    "lineas": sum(p["lineas"] for p in fichas)},
    }


def cargar(apodo, forzar=False):
    """Trae el cerebro del proyecto. Lo reconstruye SOLO si el proyecto cambio."""
    prs = proyectos()
    if apodo not in prs:
        raise SystemExit(f"NO_ENCONTRADO: el proyecto '{apodo}' no esta en proyectos.config. "
                         f"Declarados: {', '.join(prs) or '(ninguno)'}")
    raiz = prs[apodo]["ruta"]
    if not os.path.isdir(raiz):
        raise SystemExit(f"NO_ENCONTRADO: la ruta de '{apodo}' no existe: {raiz}")
    os.makedirs(MEM, exist_ok=True)
    cache = os.path.join(MEM, f"{apodo}.json")
    if not forzar and os.path.exists(cache):
        try:
            g = json.load(open(cache, encoding="utf-8"))
            if g.get("huella") == _huella(raiz):
                g["_de_cache"] = True
                return g
        except Exception:
            pass
    g = construir(raiz, apodo)
    g["_de_cache"] = False
    json.dump(g, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    return g


# ─── caminar el grafo ────────────────────────────────────────────────────────
def vecinos(g, pieza_id, saltos=1, min_fuerza=1.0):
    """El VECINDARIO de una pieza: lo que la toca y lo que ella toca, hasta N saltos.
    Se corta por FUERZA para no arrastrar el proyecto entero por culpa de un doc general."""
    sale, entra = enlaces.indexar(g["enlaces"])
    frente, visto, out = {pieza_id}, {pieza_id}, []
    for _ in range(saltos):
        nuevo = set()
        for p in frente:
            for e in sale.get(p, []) + entra.get(p, []):
                if e.get("fuerza", 1.0) < min_fuerza:
                    continue
                otro = e["a"] if e["de"] == p else e["de"]
                if otro not in visto:
                    visto.add(otro)
                    nuevo.add(otro)
                    out.append({"pieza": otro, "por": e["tipo"], "fuerza": e.get("fuerza", 1.0),
                                "desde": p})
        frente = nuevo
        if not frente:
            break
    return sorted(out, key=lambda x: -x["fuerza"])


def ficha(g, pieza_id):
    for p in g["piezas"]:
        if p["id"] == pieza_id:
            return p
    return None
