# -*- coding: utf-8 -*-
"""HABILIDAD — MEDIR AL EQUIPO. Sin gastar ni una llamada a ninguna IA.

Julio, 2026-09-05: "crea las putas skills, habilidades, justo para que hagan lo
repetitivo, sin necesidad de usar IA".

Esto es lo que el 5 de septiembre se hizo A MANO con seis ordenes de terminal para
saber si los cerebros gratis sirven o no. Es una cuenta, no un juicio: por eso lo
hace un programita y no un cerebro.

Contesta, con el registro que ya existe en disco:
  - quien ESCRIBE de verdad y quien solo REVISA
  - que trabajo fue real y que trabajo fue de practica
  - cuanto de lo aprobado llego DE VERDAD al codigo

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/medir_al_equipo.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRABAJOS = os.path.join(AQUI, "memoria", "TRABAJOS_DEL_EQUIPO.log")
APLICADO = os.path.join(AQUI, "memoria", "APLICACIONES.log")


def _lineas(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8", errors="ignore") as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]


def _trozos(linea):
    """Una linea del registro: fecha | escribio X | reviso Y | VEREDICTO | archivos"""
    partes = [p.strip() for p in linea.split("|")]
    while len(partes) < 5:
        partes.append("")
    return partes


def _de_practica(archivos):
    """Practica = toca archivos que NO existen en el disco. No se adivina: se comprueba."""
    nombres = [a.strip() for a in (archivos or "").split(",") if a.strip()]
    if not nombres:
        return False
    for n in nombres:
        for base in (AQUI, os.path.join(AQUI, "cuerpo"), os.path.join(AQUI, "arnes"),
                     os.path.join(AQUI, "cerebro"), os.path.join(AQUI, "vigias"),
                     os.path.join(AQUI, "skills")):
            if os.path.exists(os.path.join(base, n)):
                return False
    return True


def _quien(campo, prefijo):
    """De 'escribio deepseek' saca 'deepseek'."""
    campo = (campo or "").strip()
    if campo.startswith(prefijo):
        return campo[len(prefijo):].strip() or "(nadie)"
    return campo or "(nadie)"


def medir():
    escribio_real, escribio_practica, reviso_real, veredictos = {}, {}, {}, {}
    lineas = _lineas(TRABAJOS)
    for ln in lineas:
        p = _trozos(ln)
        quien_e = _quien(p[1], "escribio")
        quien_r = _quien(p[2], "reviso")
        vered = p[3] or "(sin veredicto)"
        if _de_practica(p[4]):
            escribio_practica[quien_e] = escribio_practica.get(quien_e, 0) + 1
            continue
        escribio_real[quien_e] = escribio_real.get(quien_e, 0) + 1
        clave = "%s -> %s" % (quien_r, vered)
        reviso_real[clave] = reviso_real.get(clave, 0) + 1
        veredictos[vered] = veredictos.get(vered, 0) + 1

    aplic = _lineas(APLICADO)
    # Lo que cae en carpeta temporal son las pruebas de las vigias: no cuenta como codigo real.
    reales = [a for a in aplic if "Temp" not in a and "temp" not in a]
    return {
        "total": len(lineas),
        "escribio_real": escribio_real,
        "escribio_practica": escribio_practica,
        "reviso_real": reviso_real,
        "veredictos": veredictos,
        "aplicaciones_todas": len(aplic),
        "aplicaciones_reales": reales,
        "aplicadas_ok": [a for a in reales if "| OK |" in a],
    }


def _tabla(titulo, d):
    L = ["", titulo]
    if not d:
        L.append("  (nada)")
        return L
    for k, v in sorted(d.items(), key=lambda x: -x[1]):
        L.append("  %-40s %d" % (k, v))
    return L


def informe(r=None):
    r = r or medir()
    real = sum(r["escribio_real"].values())
    practica = sum(r["escribio_practica"].values())
    L = ["MEDIDA DEL EQUIPO — del registro, sin gastar ninguna llamada",
         "=" * 64,
         "  trabajos apuntados : %d" % r["total"],
         "  trabajo REAL       : %d" % real,
         "  practica (archivos que no existen) : %d" % practica]
    L += _tabla("QUIEN ESCRIBIO en trabajo REAL:", r["escribio_real"])
    L += _tabla("QUIEN ENSAYO en archivos de practica:", r["escribio_practica"])
    L += _tabla("VEREDICTOS del trabajo real:", r["veredictos"])
    L += _tabla("REVISOR -> VEREDICTO (trabajo real):", r["reviso_real"])
    L += ["", "LO QUE LLEGO DE VERDAD AL CODIGO:",
          "  aplicaciones apuntadas : %d" % r["aplicaciones_todas"],
          "  sobre codigo de verdad : %d" % len(r["aplicaciones_reales"]),
          "  de esas, salieron bien : %d" % len(r["aplicadas_ok"])]
    for a in r["aplicadas_ok"][-8:]:
        L.append("    " + a[:110])
    if real and not r["aplicaciones_reales"]:
        L += ["", "AVISO: hay trabajo real aprobado y NADA llego al codigo."]
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe() + "\n")
