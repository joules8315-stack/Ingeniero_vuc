#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_prueba_real.py — ANTES DE PEDIRLE A JULIO QUE PRUEBE, PROBAR DE VERDAD.

Julio, 2026-08-24: "que siempre haga pruebas manuales internas reales con playwright, antes de
decirme que me pida que yo realice pruebas fisicas reales, primero debe asegurarse que se cumple
el objetivo que trace, esto evita que yo pierda el tiempo."

EL AGUJERO QUE TAPA: la regla antigua era "una vigia verde NO es prueba" y "Julio prueba con sus
ojos". Eso dejaba a Julio probando TODO a mano, incluso lo que una maquina puede comprobar sola,
y a veces el objetivo ni siquiera se habia cumplido: Julio abria la app y estaba rota. El tiempo
de Julio no se gasta en lo que una prueba real automatica puede demostrar antes.

LO QUE EXIGE (bloque B2 de la legislacion 2026-08-24): antes de pedirle a Julio que pruebe con
sus ojos, tiene que haber EVIDENCIA de una PRUEBA REAL que:
  · se hizo CON EL EQUIPO (veredicto, no autovalidacion),
  · toca la pantalla de verdad (Playwright), no un simulacro,
  · y demuestra que el objetivo se cumple.
Sin esa evidencia, NO se le pide a Julio: se corre la prueba real primero.

    python arnes/candado_prueba_real.py marcar <proyecto> "<objetivo>" --archivo <ruta> --detalle "..."
    python arnes/candado_prueba_real.py pedir  <proyecto> "<objetivo>"

marcar  -> deja la evidencia de que la prueba real corrio, con el equipo, y dio bien.
pedir   -> el candado: SI no hay evidencia fresca, verde y con equipo, BLOQUEA (no se le pide).

La evidencia guarda si se hizo con el equipo (veredicto) o fue autovalidacion. Una autovalidacion
NO abre la puerta: Julio, 2026-08-24, "verifique si en realidad se logro el resultado, o fue una
autovalidacion."
"""
import json
import os
import sys
import time
import glob

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRUEBAS = os.path.join(AQUI, "memoria", "pruebas_real")
VIGENCIA_HORAS = 72   # una prueba real vale tres dias de trabajo


def _ruta_pruebas():
    """La de verdad, o una de prueba. Cada comprobacion usa su copia (ley 23)."""
    return os.environ.get("INGENIERO_PRUEBAS_TEST") or PRUEBAS


def marcar(proyecto, objetivo, herramienta="playwright", resultado="OK",
           con_equipo=True, archivo="", detalle=""):
    """Deja la evidencia de que se corrio una prueba real y dio bien.

    con_equipo=True  -> hubo veredicto del equipo (no autovalidacion).
    resultado="OK"   -> la prueba corrio y el objetivo se cumplio.
    """
    if not proyecto or not objetivo:
        return {"_error": "hace falta el proyecto Y el objetivo. Sin eso no hay evidencia."}
    os.makedirs(_ruta_pruebas(), exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in objetivo.lower())[:50]
    ruta = os.path.join(_ruta_pruebas(), "%s__%s.json" % (proyecto, slug))
    d = {"proyecto": proyecto, "objetivo": objetivo, "cuando": time.time(),
         "resultado": resultado, "herramienta": herramienta,
         "con_equipo": bool(con_equipo), "archivo": archivo, "detalle": detalle}
    json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def _ultima(proyecto):
    try:
        ps = sorted(glob.glob(os.path.join(_ruta_pruebas(), "%s__*.json" % (proyecto or ""))),
                    key=os.path.getmtime, reverse=True)
    except Exception:
        return None
    if not ps:
        return None
    try:
        return json.load(open(ps[0], encoding="utf-8"))
    except Exception:
        return None


def hay_prueba_real(proyecto, objetivo, max_horas=VIGENCIA_HORAS):
    """¿Hay evidencia fresca, verde y CON EQUIPO de una prueba real para este asunto?

    Devuelve el dict de la evidencia si vale; None si no hay nada que valga. Solo cuenta:
      · resultado OK (verde),
      · con_equipo (no autovalidacion),
      · reciente (menos de max_horas),
      · que hable del mismo objetivo (coincide la palabra clave de fondo).
    """
    d = _ultima(proyecto or "")
    if not d:
        return None
    if d.get("resultado") != "OK":
        return None
    if not d.get("con_equipo"):
        return None
    if time.time() - float(d.get("cuando", 0)) > float(max_horas) * 3600:
        return None
    return d


MENSAJE = (
    "BLOQUEADO: NO SE LE PIDE A JULIO QUE PRUEBE TODAVIA\n\n"
    "  Ibas a pedirle a Julio que pruebe con sus ojos, pero no hay EVIDENCIA de una\n"
    "  PRUEBA REAL (hecha con el equipo, con Playwright) que demuestre que el objetivo\n"
    "  se cumple.\n\n"
    "  Julio, 2026-08-24: 'siempre haz pruebas reales internas antes de decirme que me\n"
    "  pida que yo realice pruebas fisicas; primero asegurate de que se cumple el objetivo\n"
    "  que trace. Esto evita que yo pierda el tiempo.'\n\n"
    "  Que hacer ANTES de pedirle a Julio:\n"
    "    1) Con el EQUIPO, corre la prueba real interna (Playwright) que toca la pantalla\n"
    "       de verdad y comprueba que el objetivo se cumple.\n"
    "    2) Deja la evidencia (con su veredicto de equipo):\n"
    "       cd C:\\Ingeniero_VUC; python arnes/candado_prueba_real.py marcar <proyecto> \"<objetivo>\" --archivo <ruta> --detalle \"que se vio y que paso\"\n"
    "    3) Recien ahi pedirle a Julio que pruebe con sus ojos.\n"
    "\n  El tiempo de Julio no se gasta en lo que una maquina puede comprobar sola.\n")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    cmd = args[0]
    if cmd == "marcar":
        if len(args) < 3:
            print("NO_ENCONTRADO: hace falta <proyecto> \"<objetivo>\"")
            return 1
        proyecto = args[1]
        partes = []
        for a in args[2:]:
            if a.startswith("--"):
                break
            partes.append(a)
        objetivo = " ".join(partes)
        archivo, detalle, con_equipo = "", "", True
        if "--archivo" in args:
            i = args.index("--archivo")
            archivo = args[i + 1] if len(args) > i + 1 else ""
        if "--detalle" in args:
            i = args.index("--detalle")
            detalle = " ".join(args[i + 1:])
        if "--sin-equipo" in args:
            con_equipo = False
        r = marcar(proyecto, objetivo, archivo=archivo, detalle=detalle, con_equipo=con_equipo)
        if "_error" in r:
            print(r["_error"])
            return 1
        print("PRUEBA REAL marcada como OK para '%s' (objetivo: %s)" % (proyecto, objetivo[:80]))
        print("  con el equipo: %s   herramienta: %s" % ("SI" if con_equipo else "NO (autovalidacion)",
                                                         r["herramienta"]))
        if detalle:
            print("  detalle: %s" % detalle[:160])
        return 0
    if cmd == "pedir":
        if len(args) < 3:
            print("NO_ENCONTRADO: hace falta <proyecto> \"<objetivo>\"")
            return 1
        proyecto, objetivo = args[1], " ".join(args[2:])
        if hay_prueba_real(proyecto, objetivo):
            print("OK: hay evidencia fresca, verde y con equipo. Ya se puede pedirle a Julio que pruebe.")
            return 0
        sys.stderr.write(MENSAJE)
        # MEDICION (Julio, 2026-08-25): freno pedirle a Julio que pruebe sin evidencia real.
        try:
            import candados_medicion
            candados_medicion.cazado("prueba_real")
        except Exception:
            pass
        return 2
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
