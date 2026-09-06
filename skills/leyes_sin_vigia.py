# -*- coding: utf-8 -*-
"""HABILIDAD — QUE LEYES SON SOLO PAPEL. Sin gastar ni una llamada a ninguna IA.

Julio, 2026-09-06. Criterio que la justifica: al contarlo por primera vez el 6 de
septiembre salieron **13 leyes de 24 sin ninguna vigia que las nombre**. Mas de la
mitad de las leyes de la casa no las vigila nadie: son papel.

Una ley sin vigia depende de que la IA se acuerde. Y ya esta medido que acordarse
no funciona: "avisar no detiene a quien ya decidio".

Es cruzar dos listas de nombres: una cuenta, no un juicio.

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/leyes_sin_vigia.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIGIAS = os.path.join(AQUI, "vigias")


def _leyes():
    return sorted(n for n in os.listdir(AQUI)
                  if n.startswith("CONTRATO_") and n.endswith(".md"))


def _texto_de_las_vigias():
    """Todo lo que dicen las vigias, junto. Se lee una vez y se busca dentro."""
    trozos = []
    for carpeta in (VIGIAS,):
        if not os.path.isdir(carpeta):
            continue
        for n in os.listdir(carpeta):
            if not n.endswith(".py"):
                continue
            try:
                with open(os.path.join(carpeta, n), encoding="utf-8", errors="ignore") as f:
                    trozos.append(f.read())
            except Exception:
                pass
    return "\n".join(trozos)


def revisar():
    texto = _texto_de_las_vigias()
    con, sin = [], []
    for ley in _leyes():
        nombre = ley[:-3]                      # sin el .md
        corto = nombre.replace("CONTRATO_", "")
        (con if (nombre in texto or corto in texto) else sin).append(ley)
    return {"todas": _leyes(), "con_vigia": con, "sin_vigia": sin}


def informe(r=None):
    r = r or revisar()
    total, sin = len(r["todas"]), len(r["sin_vigia"])
    pct = (sin * 100.0 / total) if total else 0
    L = ["LEYES SIN VIGIA — cuales son solo papel", "=" * 52,
         "  leyes escritas        : %d" % total,
         "  leyes con vigia       : %d" % len(r["con_vigia"]),
         "  leyes SIN vigia       : %d   (%.0f %%)" % (sin, pct),
         ""]
    if r["sin_vigia"]:
        L.append("SOLO PAPEL — nadie comprueba que se cumplan:")
        for n in r["sin_vigia"]:
            L.append("   " + n)
        L += ["",
              "Una ley sin vigia depende de que la IA se acuerde.",
              "Ya esta medido que acordarse no funciona: avisar no detiene",
              "a quien ya decidio. Cada una de estas necesita su vigia."]
    else:
        L.append("Todas las leyes tienen quien las vigile.")
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe() + "\n")
