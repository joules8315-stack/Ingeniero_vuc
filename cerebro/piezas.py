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


def funcion_que_contiene(ruta_abs, desde, hasta):
    """Que funcion contiene el tramo desde-hasta. Devuelve la funcion ENTERA, o None.

    Julio, 2026-09-05. Es la otra mitad de `funcion_completa`: aquella busca por NOMBRE cuando ya
    se sabe el nombre; esta busca por SITIO cuando lo unico que hay es un trozo elegido por
    parecido de palabras, que es lo que entrega el fragmentador.

    Sin esto, el paquete llega con pedazos huerfanos —el trozo empieza a mitad de la funcion y no
    se ve ni el `def`— y el auditor rechaza la ronda diciendo que se usan cosas inventadas.

    Se mira solo la boca del modulo (columna cero), el mismo criterio que usa `funcion_completa`:
    lo anidado no es una pieza que nadie pueda pedir por su nombre.
    """
    try:
        desde = int(desde or 0)
        hasta = int(hasta or 0)
    except Exception:
        return None
    if desde <= 0:
        return None
    lineas = _leer(ruta_abs).splitlines()
    nombre = None
    for i, linea in enumerate(lineas, 1):
        if i > desde:
            break
        if linea[:1] in (" ", "\t"):
            continue
        cruda = linea.rstrip()
        if cruda.startswith("def ") or cruda.startswith("class "):
            corte = cruda.split(None, 1)[1] if " " in cruda else ""
            for sep in ("(", ":"):
                if sep in corte:
                    corte = corte.split(sep, 1)[0]
            nombre = corte.strip() or None
    if not nombre:
        return None                    # el trozo esta antes de la primera funcion: es la cabecera
    hallazgo = funcion_completa(ruta_abs, nombre)
    if not hallazgo:
        return None
    # Se mira donde EMPIEZA el trozo, no donde acaba. Un trozo elegido por parecido de palabras
    # suele arrastrar renglones en blanco del final, y comparando con el final se rechazaba la
    # funcion correcta. Lo cazo la propia vigia el 2026-09-05.
    if hallazgo["hasta"] < desde:
        return None                    # la funcion acaba antes: el trozo cae fuera de ella
    hallazgo["nombre"] = nombre
    return hallazgo


def funcion_completa(ruta_abs, nombre):
    """La pieza ENTERA, buscada POR SU NOMBRE y nunca por un numero de renglon.

    Julio, 2026-08-31, tras repetirlo muchas veces: "que lo busque por funcion y nombre... ya
    que el numero esta constantemente cambiando". Y tenia razon medida: un numero se corre en
    cuanto alguien anade algo mas arriba, y pedir un tramo ("de la 97 a la 136") BORRA la
    funcion entera aunque solo hubiera que cambiar una palabra. El nombre no se mueve.

    Devuelve {"desde", "hasta", "texto"} con el sitio REAL (1-indexado), o None si no esta.
    Nunca inventa: si el nombre no aparece, se contesta que no aparece.

    Se mira solo la boca del modulo (columna cero), el mismo criterio que ya usa api() aqui
    al lado: lo anidado no es una pieza que nadie pueda pedir por su nombre.
    """
    lineas = _leer(ruta_abs).splitlines()
    arranques = ("def " + nombre + "(", "class " + nombre + "(", "class " + nombre + ":")
    desde = hasta = 0
    for i, linea in enumerate(lineas, 1):
        if linea[:1] in (" ", "\t"):
            continue
        if linea.rstrip().startswith(arranques):
            desde = hasta = i
            break
    if not desde:
        return None
    # DENTRO DE UN TEXTO NO SE CORTA (2026-08-31, cazado usando esto mismo). Muchas piezas son
    # casi todo un texto entre comillas triples, y sus renglones van pegados al margen. Con la
    # regla a secas de "columna cero termina la pieza", `_prompt_obrero` llegaba de 2 renglones
    # cuando mide 40: el mismo dano de entregar la pieza partida, por otro camino.
    # Se arranca mirando el propio renglon del def, por si abrio el texto ahi mismo.
    dentro_de_texto = (lineas[desde - 1].count('"""') + lineas[desde - 1].count("'''")) % 2 == 1
    for j in range(desde, len(lineas)):
        linea = lineas[j]
        if not linea.strip():
            continue                    # un renglon en blanco NO corta la funcion
        # EL ORDEN IMPORTA: primero se decide con el estado de ANTES de este renglon. El renglon
        # que CIERRA las comillas suele ir en columna cero; si se actualizara antes de decidir,
        # se cortaria justo antes y la pieza llegaria sin su cierre.
        if len(linea) - len(linea.lstrip()) == 0 and not dentro_de_texto:
            break                       # vuelve a columna cero: aqui ya empieza otra cosa
        hasta = j + 1
        dentro_de_texto = (dentro_de_texto + linea.count('"""') + linea.count("'''")) % 2 == 1
    return {"desde": desde, "hasta": hasta, "texto": "\n".join(lineas[desde - 1:hasta])}


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
    lineas = _leer(ruta_abs).splitlines()
    for i, ln in enumerate(lineas, 1):
        m = re.match(r"^(def|class)\s+([A-Za-z_]\w*)", ln)
        if m and not m.group(2).startswith("_"):
            explicacion = ""
            if i < len(lineas):
                siguiente = lineas[i].strip()
                if siguiente.startswith('"""') or siguiente.startswith("'''"):
                    explicacion = siguiente[3:]
                    if explicacion.endswith('"""') or explicacion.endswith("'''"):
                        explicacion = explicacion[:-3]
                    explicacion = explicacion.strip()
                    punto = explicacion.find('.')
                    if punto != -1:
                        explicacion = explicacion[:punto + 1]
            out.append({"nombre": m.group(2), "tipo": m.group(1), "linea": i, "para_que_sirve": explicacion})
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
