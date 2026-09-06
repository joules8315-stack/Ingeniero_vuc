# -*- coding: utf-8 -*-
"""HABILIDAD — UNA SOLA VIA. Sin gastar ni una llamada a ninguna IA.

Julio, 2026-09-05: "Una sola rama, o via canonica, para ABRIR, TRABAJAR y GUARDAR.
Nunca un duplicado, o via alterna. Si existe mas de una via o rama, unificala."
Ley escrita en CONTRATO_UNA_SOLA_VIA.md.

El aviso que ya existia solo miraba CARPETAS. Por eso una segunda copia de trabajo
del Ingeniero vivio dias sin que nadie la viera. Esto mira las TRES cosas:
  - la carpeta donde se trabaja
  - la rama donde se guarda (y si es la declarada)
  - las copias de trabajo de git, que no se ven al abrir la carpeta
Y ademas dice, de cada rama sobrante, CUANTO trabajo propio tiene: si tiene cero,
retirarla no pierde nada.

Es git y comparar texto: una cuenta, no un juicio.

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/via_unica.py
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(AQUI, "proyectos.config")


def _git(ruta, *args):
    try:
        r = subprocess.run(["git", "-C", ruta] + list(args), capture_output=True,
                           text=True, encoding="utf-8", errors="ignore", timeout=30)
        return (r.stdout or "").strip()
    except Exception:
        return ""


def proyectos():
    """apodo = ruta | rama | marca. Se lee la libreta de direcciones, no se adivina."""
    salida = []
    if not os.path.exists(CONFIG):
        return salida
    with open(CONFIG, encoding="utf-8", errors="ignore") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or "=" not in ln:
                continue
            apodo, resto = ln.split("=", 1)
            partes = [p.strip() for p in resto.split("|")]
            salida.append({
                "apodo": apodo.strip(),
                "ruta": partes[0] if partes else "",
                "rama": partes[1] if len(partes) > 1 else "",
            })
    return salida


def revisar(p):
    """De un proyecto: donde esta, en que rama, que ramas sobran y que copias sobran."""
    ruta, rama_decl = p["ruta"], p["rama"]
    r = {"apodo": p["apodo"], "ruta": ruta, "rama_declarada": rama_decl,
         "existe": os.path.isdir(ruta), "avisos": [], "ramas_sobrantes": [],
         "copias_sobrantes": []}
    if not r["existe"]:
        r["avisos"].append("la carpeta declarada NO existe en el disco")
        return r

    rama = _git(ruta, "rev-parse", "--abbrev-ref", "HEAD")
    r["rama_actual"] = rama or "SIN-GIT"
    if not rama:
        r["avisos"].append("aqui no hay control de versiones")
        return r
    if rama_decl and rama != rama_decl:
        r["avisos"].append("se esta en la rama '%s' y la declarada es '%s'" % (rama, rama_decl))

    canon = rama_decl or rama
    for ln in (_git(ruta, "for-each-ref", "--format=%(refname:short)", "refs/heads/") or "").splitlines():
        otra = ln.strip()
        if not otra or otra == canon:
            continue
        propios = _git(ruta, "rev-list", "--count", "%s..%s" % (canon, otra)) or "?"
        fecha = _git(ruta, "log", "-1", "--format=%cs", otra) or "?"
        r["ramas_sobrantes"].append({"rama": otra, "propios": propios, "fecha": fecha})

    for ln in (_git(ruta, "worktree", "list") or "").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        # OJO: la ruta puede llevar ESPACIOS ("Asesor Marketing"), asi que NO se puede partir
        # la linea por espacios: se compara si empieza por la carpeta buena (fallo real 2026-09-05).
        yo = os.path.normcase(os.path.abspath(ruta)).replace("\\", "/")
        suyo = os.path.normcase(ln).replace("\\", "/")
        if not suyo.startswith(yo):
            r["copias_sobrantes"].append(ln)

    if _git(ruta, "status", "--short"):
        r["avisos"].append("hay cambios sin guardar aqui")
    return r


def informe():
    L = ["UNA SOLA VIA — carpeta, rama y copias de trabajo", "=" * 60]
    limpio = True
    for p in proyectos():
        r = revisar(p)
        L.append("")
        L.append("%s  ->  %s" % (r["apodo"], r["ruta"]))
        L.append("   rama: %s   (declarada: %s)" % (r.get("rama_actual", "?"), r["rama_declarada"] or "-"))
        for a in r["avisos"]:
            L.append("   AVISO: " + a)
            if "sin guardar" not in a:
                limpio = False
        if r["ramas_sobrantes"]:
            limpio = False
            L.append("   RAMAS DE MAS: %d" % len(r["ramas_sobrantes"]))
            for x in sorted(r["ramas_sobrantes"], key=lambda y: -int(y["propios"]) if y["propios"].isdigit() else 0):
                marca = "sin nada propio: retirarla no pierde nada" if x["propios"] == "0" else \
                        "guarda %s cosas que la buena no tiene" % x["propios"]
                L.append("     - %-45s %s   [%s]" % (x["rama"], x["fecha"], marca))
        if r["copias_sobrantes"]:
            limpio = False
            L.append("   COPIAS DE TRABAJO DE MAS: %d" % len(r["copias_sobrantes"]))
            for c in r["copias_sobrantes"]:
                L.append("     - " + c[:100])
        if not r["ramas_sobrantes"] and not r["copias_sobrantes"]:
            L.append("   limpio: una carpeta y una rama")
    L.append("")
    L.append("RESULTADO: " + ("todo en una sola via" if limpio else
                              "HAY MAS DE UNA VIA. Se le enseña a Julio y el decide que se retira."))
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe() + "\n")
