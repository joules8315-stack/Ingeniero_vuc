# -*- coding: utf-8 -*-
"""
inventario.py -- PASO 1 del Ingeniero VUC: el MAPA.
Barre TODOS los proyectos de Julio y clasifica cada pieza por ROL.
No imprime contenido: solo cuenta, clasifica y detecta duplicados.
Salida: MAPA_INGENIERO.json (para maquinas) + MAPA_INGENIERO.md (para Julio).
"""
import os, json, hashlib, re
from collections import defaultdict

# LAS RAICES SALEN DE proyectos.config, no de aqui.
# Antes estaban quemadas en este archivo y en proyectos.config a la vez: dos listas que se
# contradecian (Ley 6, no repetidera). Ahora hay UNA sola libreta de direcciones.
def _raices():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = [(base, "Ingeniero VUC (esta herramienta)")]
    cfg = os.path.join(base, "proyectos.config")
    if os.path.exists(cfg):
        for ln in open(cfg, encoding="utf-8", errors="ignore").read().splitlines():
            ln = ln.strip()
            if not ln or ln.startswith("#") or "=" not in ln:
                continue
            apodo, resto = ln.split("=", 1)
            ruta = resto.split("|")[0].strip()
            if os.path.abspath(ruta) != os.path.abspath(base):
                out.append((ruta, apodo.strip()))
    return out

RAICES = _raices()
EXCLUIR_DIR = {"__pycache__", ".git", "node_modules", "LM Studio", ".venv", "venv",
               "site-packages", ".pytest_cache", "dist", "build", ".mypy_cache", ".venv", "Lib", "Scripts", "artifacts", "Microsoft", "docs_build"}
EXCLUIR_EXT = {".pyc", ".exe", ".dll", ".zip", ".png", ".jpg", ".jpeg", ".gif",
               ".ico", ".pdf", ".docx", ".xlsx", ".log", ".dat", ".bin", ".so"}

def rol(ruta, nombre):
    n = nombre.lower()
    r = ruta.lower().replace("\\", "/")
    if n.startswith("test_vigia") or "/vigias/" in r and n.endswith(".py"): return "VIGIA"
    if n.startswith("contrato") or n.startswith("contratos"):               return "CONTRATO"
    if "matriz" in n or "tabla_de_verdad" in n or "tabla de verdad" in n:   return "MATRIZ/TABLA_VERDAD"
    if "/arnes/" in r or n in ("sellar.sh", "edit_gate.py", "pre-push"):    return "ARNES/CANDADO"
    if n.startswith("protocolo") or n.startswith("mapa_") or n.startswith("plan_"): return "PROTOCOLO/MAPA"
    if "/cuerpo/" in r and n.endswith(".py"):                               return "CUERPO (modulo)"
    if "skill" in n:                                                        return "SKILL"
    if "helper" in n or "util" in n:                                        return "HELPER"
    if n.endswith((".bat", ".ps1", ".sh")):                                 return "LANZADOR/SCRIPT"
    if n.endswith(".md"):                                                   return "DOC"
    if n.endswith(".py"):                                                   return "CODIGO"
    if n.endswith((".html", ".css", ".js")):                                return "WEB"
    if n.endswith((".json", ".sql", ".txt", ".yaml", ".yml", ".config", ".env", ".example")): return "DATO/CONFIG"
    return "OTRO"

def lineas_y_hash(p):
    try:
        with open(p, "rb") as f: b = f.read()
        return b.count(b"\n") + 1, hashlib.md5(b).hexdigest()
    except Exception:
        return 0, ""

def resumen(p, ext):
    """Primera linea util: docstring, titulo md o primer comentario. Max 160 chars."""
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read(4000)
    except Exception:
        return ""
    if ext == ".md":
        for ln in txt.splitlines():
            if ln.startswith("#"): return ln.lstrip("# ").strip()[:160]
    m = re.search(r'"""(.+?)"""', txt, re.S)
    if m: return " ".join(m.group(1).split())[:160]
    for ln in txt.splitlines():
        s = ln.strip()
        if s.startswith("#") and len(s) > 3: return s.lstrip("# ").strip()[:160]
    return ""

def apis(p):
    """Funciones y clases publicas de un .py (la 'boca' del modulo)."""
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f: txt = f.read()
    except Exception:
        return []
    return [m for m in re.findall(r"^(?:def|class)\s+([A-Za-z_]\w*)", txt, re.M) if not m.startswith("_")][:25]

piezas, por_rol, por_proyecto = [], defaultdict(int), defaultdict(int)
hashes = defaultdict(list); nombres = defaultdict(list)

for raiz, etiqueta in RAICES:
    if not os.path.isdir(raiz):
        continue
    from cerebro.piezas import es_nombre_reservado as _reservado, barrer_reservados as _barrer
    _barrer(raiz)
    for dp, dns, fns in os.walk(raiz):
        dns[:] = [d for d in dns if d not in EXCLUIR_DIR]
        dns[:] = [d for d in dns if not _reservado(d)]
        for fn in fns:
            if _reservado(fn): continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXCLUIR_EXT: continue
            full = os.path.join(dp, fn)
            try:
                if os.path.getsize(full) > 3_000_000: continue
            except Exception:
                continue
            ln, h = lineas_y_hash(full)
            r = rol(full, fn)
            pieza = {
                "proyecto": etiqueta,
                "ruta": os.path.relpath(full, raiz).replace("\\", "/"),
                "ruta_abs": full,
                "rol": r,
                "lineas": ln,
                "resumen": resumen(full, ext),
                "api": apis(full) if ext == ".py" else [],
                "md5": h,
            }
            piezas.append(pieza)
            por_rol[r] += 1
            por_proyecto[etiqueta] += 1
            if h: hashes[h].append(f"{etiqueta}::{pieza['ruta']}")
            nombres[fn].append(f"{etiqueta}::{pieza['ruta']}")

dup_identicos = {h: v for h, v in hashes.items() if len(v) > 1}
dup_nombre = {n: v for n, v in nombres.items() if len(v) > 1}

salida = {
    "generado_por": "Ingeniero VUC / mapa/inventario.py",
    "total_piezas": len(piezas),
    "total_lineas": sum(p["lineas"] for p in piezas),
    "por_proyecto": dict(por_proyecto),
    "por_rol": dict(por_rol),
    "duplicados_identicos": {h: v for h, v in list(dup_identicos.items())},
    "duplicados_por_nombre": dup_nombre,
    "piezas": piezas,
}
base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "MAPA_INGENIERO.json"), "w", encoding="utf-8") as f:
    json.dump(salida, f, ensure_ascii=False, indent=1)

# Regenerar el mapa legible para Julio: el compilador ya existe y convierte el json en md.
compilar = os.path.join(base, "compilar_mapa.py")
if os.path.exists(compilar):
    import subprocess, sys
    subprocess.run([sys.executable, compilar], cwd=base, check=True)

print("PIEZAS:", len(piezas), "| LINEAS:", salida["total_lineas"])
print("\n-- POR PROYECTO --")
for k, v in sorted(por_proyecto.items(), key=lambda x: -x[1]): print(f"  {v:5}  {k}")
print("\n-- POR ROL --")
for k, v in sorted(por_rol.items(), key=lambda x: -x[1]): print(f"  {v:5}  {k}")
print("\n-- COPIAS IDENTICAS (mismo contenido, 2+ lugares):", len(dup_identicos))
print("-- MISMO NOMBRE EN 2+ LUGARES:", len(dup_nombre))
