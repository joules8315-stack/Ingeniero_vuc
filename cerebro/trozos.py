# -*- coding: utf-8 -*-
"""cerebro/trozos.py — CAPA 3 del cerebro: los TROZOS (el "chunk").

Aqui esta la economia de verdad. Una pieza puede tener 10.818 lineas (app.py de Foto Informe).
Nadie necesita esas 10.818: necesita 40. Esta capa corta la pieza en trozos y sabe cual trozo
responde al problema, con su LINEA EXACTA.

Mejora sobre `cuerpo/indice.py` de DMM (de donde viene la idea): alli el trozo se corta por
caracteres y se devuelve como `archivo#3`, que no le sirve a nadie para ir a mirar. Aqui el
trozo se corta por LINEAS y se devuelve como `archivo:340-380`, que es una direccion real.

Sin llaves, sin internet, sin costo: cuenta palabras (la misma idea de BolsaDePalabras de DMM).
"""
import re, math
from collections import Counter, defaultdict

TAM = 40          # lineas por trozo
SOLAPE = 8        # lineas repetidas entre trozo y trozo (para no cortar una funcion en seco)
RUIDO = {"the", "and", "for", "que", "con", "por", "los", "las", "del", "una", "self",
         "import", "from", "return", "def", "class", "if", "else", "not", "none", "true", "false"}


def _palabras(txt):
    return [w for w in re.findall(r"[a-záéíóúñ_]{3,}", txt.lower()) if w not in RUIDO]


def cortar(texto, tam=TAM, solape=SOLAPE):
    """Parte en trozos con solape. Devuelve [{desde, hasta, texto}] con lineas 1-indexadas."""
    lineas = texto.splitlines()
    if not lineas:
        return []
    out, i = [], 0
    paso = max(1, tam - solape)
    while i < len(lineas):
        bloque = lineas[i:i + tam]
        out.append({"desde": i + 1, "hasta": min(i + tam, len(lineas)), "texto": "\n".join(bloque)})
        if i + tam >= len(lineas):
            break
        i += paso
    return out


def _leer(abs_path):
    try:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


class Buscador:
    """Indexa los trozos de unas piezas y trae los k que responden al problema.
    Usa TF-IDF simple: premia la palabra rara (la que de verdad distingue) y castiga la comun."""

    def __init__(self, fichas):
        self.trozos = []
        for f in fichas:
            txt = _leer(f["abs"])
            if not txt:
                continue
            for t in cortar(txt):
                self.trozos.append({
                    "pieza": f["id"], "abs": f["abs"], "rol": f["rol"],
                    "desde": t["desde"], "hasta": t["hasta"], "texto": t["texto"],
                    "bolsa": Counter(_palabras(t["texto"])),
                })
        # cuantos trozos contienen cada palabra (para saber cuales son raras)
        self.docs = len(self.trozos) or 1
        self.en_cuantos = defaultdict(int)
        for t in self.trozos:
            for w in t["bolsa"]:
                self.en_cuantos[w] += 1

    def buscar(self, consulta, k=6, solo_piezas=None, exigir=None):
        """exigir = palabras del ASUNTO (el flujo). Si se pasan, el trozo que no hable del
        asunto se descarta aunque comparta palabras sueltas. Sin esto, buscar "no persiste la
        plantilla al cambiar de SESION" traia el login (por la palabra sesion). Caso real."""
        q = _palabras(consulta)
        if not q:
            return []
        res = []
        for t in self.trozos:
            if solo_piezas and t["pieza"] not in solo_piezas:
                continue
            if exigir and not any(e.lower() in t["texto"].lower() for e in exigir):
                continue
            p = 0.0
            for w in q:
                c = t["bolsa"].get(w, 0)
                if c:
                    idf = math.log(self.docs / (1 + self.en_cuantos[w]))
                    p += (1 + math.log(c)) * max(idf, 0.1)
            if p > 0:
                res.append((p, t))
        res.sort(key=lambda x: -x[0])
        vistos, out = set(), []
        for p, t in res:
            # no traer dos trozos pegados de la misma pieza: aburre y encarece
            clave = (t["pieza"], t["desde"] // 100)
            if clave in vistos:
                continue
            vistos.add(clave)
            out.append({"pieza": t["pieza"], "desde": t["desde"], "hasta": t["hasta"],
                        "puntaje": round(p, 2), "texto": t["texto"], "rol": t["rol"],
                        "direccion": f"{t['pieza']}:{t['desde']}-{t['hasta']}"})
            if len(out) >= k:
                break
        return out
