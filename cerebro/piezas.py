# -*- coding: utf-8 -*-
"""cerebro/piezas.py — CAPA 2 del cerebro: las PIEZAS (un nodo por archivo).

Una PIEZA es la ficha de un archivo: que es, cuanto pesa, que boca tiene (funciones publicas)
y de quien depende. La ficha NO contiene el archivo: contiene lo justo para decidir si vale
la pena abrirlo. Esa es toda la economia del sistema.

Origen: la logica de resumen/API viene de `mapa/inventario.py` y del `cuerpo/indice.py` de DMM.
"""
import os, re, hashlib

EXCLUIR_DIR = {"__pycache__", ".git", "node_modules", "LM Studio", ".venv", "venv",
               "site-packages", ".pytest_cache", "dist", "build", ".mypy_cache",
               "Lib", "Scripts", "artifacts", "Microsoft", ".memoria_ingeniero"}
EXCLUIR_EXT = {".pyc", ".exe", ".dll", ".zip", ".png", ".jpg", ".jpeg", ".gif", ".ico",
               ".pdf", ".docx", ".xlsx", ".log", ".dat", ".bin", ".so", ".lnk"}
TOPE_BYTES = 3_000_000


def rol(rel, nombre):
    """El ROL manda: dice como se trata la pieza y en que capa entra."""
    n, r = nombre.lower(), rel.lower().replace("\\", "/")
    if n.startswith("test_vigia") or (r.startswith("vigias/") and n.endswith(".py")): return "VIGIA"
    if n.startswith("contrato"):                                    return "CONTRATO"
    if "matriz" in n or "verdad" in n:                              return "MATRIZ"
    if r.startswith("arnes/") or n in ("sellar.sh", "edit_gate.py", "pre-push", "read_gate.py"): return "ARNES"
    if n.startswith(("protocolo", "mapa_", "plan_", "estado_")):    return "PROTOCOLO"
    if r.startswith("cuerpo/") and n.endswith(".py"):               return "CUERPO"
    if r.startswith("cerebro/") and n.endswith(".py"):              return "CEREBRO"
    if "skill" in n:                                                return "SKILL"
    if n.endswith((".html", ".css", ".js")):                        return "WEB"
    if n.endswith((".bat", ".ps1", ".sh")):                         return "LANZADOR"
    if n.endswith(".md"):                                           return "DOC"
    if n.endswith(".py"):                                           return "CODIGO"
    return "DATO"


def _leer(ruta_abs, tope=None):
    try:
        with open(ruta_abs, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(tope) if tope else f.read()
    except Exception:
        return ""


def resumen(ruta_abs, ext):
    """Una linea que diga QUE es. Docstring, titulo del .md o primer comentario."""
    txt = _leer(ruta_abs, 4000)
    if ext == ".md":
        for ln in txt.splitlines():
            if ln.startswith("#"):
                return ln.lstrip("# ").strip()[:180]
    m = re.search(r'"""(.+?)"""', txt, re.S)
    if m:
        return " ".join(m.group(1).split())[:180]
    for ln in txt.splitlines():
        s = ln.strip()
        if s.startswith("#") and len(s) > 4:
            return s.lstrip("# ").strip()[:180]
    return ""


def api(ruta_abs):
    """La BOCA de un modulo: sus funciones y clases publicas, con la linea donde viven.
    Con esto la IA sabe QUE puede llamar sin abrir el archivo."""
    out = []
    for i, ln in enumerate(_leer(ruta_abs).splitlines(), 1):
        m = re.match(r"^(def|class)\s+([A-Za-z_]\w*)", ln)
        if m and not m.group(2).startswith("_"):
            out.append({"nombre": m.group(2), "tipo": m.group(1), "linea": i})
    return out


def imports(ruta_abs):
    """De quien depende esta pieza (modulos locales del proyecto)."""
    txt = _leer(ruta_abs)
    mods = set()
    for m in re.finditer(r"^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", txt, re.M):
        mods.add((m.group(1) or m.group(2)).split(".")[0] if False else (m.group(1) or m.group(2)))
    return sorted(mods)


def escanear(raiz):
    """Devuelve la lista de FICHAS del proyecto. No devuelve contenido: devuelve fichas."""
    raiz = os.path.abspath(raiz)
    fichas = []
    for dp, dns, fns in os.walk(raiz):
        dns[:] = [d for d in dns if d not in EXCLUIR_DIR]
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXCLUIR_EXT:
                continue
            full = os.path.join(dp, fn)
            try:
                if os.path.getsize(full) > TOPE_BYTES:
                    continue
            except Exception:
                continue
            rel = os.path.relpath(full, raiz).replace("\\", "/")
            try:
                with open(full, "rb") as f:
                    b = f.read()
            except Exception:
                continue
            fichas.append({
                "id": rel,
                "abs": full,
                "rol": rol(rel, fn),
                "lineas": b.count(b"\n") + 1,
                "bytes": len(b),
                "resumen": resumen(full, ext),
                "api": api(full) if ext == ".py" else [],
                "importa": imports(full) if ext == ".py" else [],
                "md5": hashlib.md5(b).hexdigest(),
            })
    return fichas
