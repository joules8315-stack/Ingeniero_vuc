# -*- coding: utf-8 -*-
"""HABILIDAD — CAZAR EL HUMO. Sin gastar ni una llamada a ninguna IA.

Julio, 2026-09-05. Criterio que la justifica: el 5 de septiembre el equipo entrego
DOS veces seguidas una "reparacion" que solo cambiaba comentarios. El fallo quedaba
intacto y el revisor la aprobo las dos veces diciendo que estaba correcta.

Un cerebro se deja engañar por eso. Un programita no: quita los comentarios, las
cadenas de documentacion y las lineas en blanco de los dos textos, y compara. Si lo
que queda es igual, no se reparo nada. Es comparar texto, no un juicio.

Sirve para dos cosas:
  - mirar lo que acaba de cambiar en el proyecto (lo no guardado)
  - comparar dos textos sueltos, desde otra pieza

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/cazar_el_humo.py
"""
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sin_ruido(texto):
    """Deja solo lo que HACE algo: fuera comentarios, documentacion y lineas vacias."""
    fuera, dentro_doc = [], None
    for linea in (texto or "").splitlines():
        tira = linea.strip()
        if not tira:
            continue
        if dentro_doc:
            if dentro_doc in tira:
                dentro_doc = None
            continue
        abre = re.match(r'^[rubf]*("""|\'\'\')', tira)
        if abre:
            marca = abre.group(1)
            if tira.count(marca) < 2:
                dentro_doc = marca
            continue
        if tira.startswith("#"):
            continue
        fuera.append(tira)
    return "\n".join(fuera)


def es_humo(viejo, nuevo):
    """True si el cambio SOLO toca comentarios: no repara nada."""
    return sin_ruido(viejo) == sin_ruido(nuevo)


def _cambios_sin_guardar(ruta=None):
    """Lo que cambio y aun no se guardo, archivo por archivo: (nombre, quitadas, puestas)."""
    ruta = ruta or AQUI
    try:
        r = subprocess.run(["git", "-C", ruta, "diff", "-U0"], capture_output=True,
                           text=True, encoding="utf-8", errors="ignore", timeout=60)
        texto = r.stdout or ""
    except Exception:
        return []
    salida, actual, menos, mas = [], None, [], []
    for ln in texto.splitlines():
        if ln.startswith("+++ b/"):
            if actual:
                salida.append((actual, "\n".join(menos), "\n".join(mas)))
            actual, menos, mas = ln[6:], [], []
        elif ln.startswith("-") and not ln.startswith("---"):
            menos.append(ln[1:])
        elif ln.startswith("+") and not ln.startswith("+++"):
            mas.append(ln[1:])
    if actual:
        salida.append((actual, "\n".join(menos), "\n".join(mas)))
    return salida


def informe(ruta=None):
    cambios = _cambios_sin_guardar(ruta)
    L = ["CAZAR EL HUMO — lo que cambio y aun no se guarda", "=" * 56]
    if not cambios:
        L.append("  no hay nada cambiado sin guardar")
        return "\n".join(L)
    humos, buenos = [], []
    for nombre, viejo, nuevo in cambios:
        if not nombre.endswith((".py", ".js", ".ts", ".html")):
            continue
        (humos if es_humo(viejo, nuevo) else buenos).append(nombre)
    L.append("  piezas de codigo tocadas : %d" % (len(humos) + len(buenos)))
    L.append("")
    if humos:
        L.append("HUMO — solo se tocaron comentarios, no se reparo nada:")
        for n in humos:
            L.append("   " + n)
    else:
        L.append("Sin humo: todo lo tocado cambia algo que hace.")
    if buenos:
        L.append("")
        L.append("CAMBIO DE VERDAD:")
        for n in buenos:
            L.append("   " + n)
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe() + "\n")
