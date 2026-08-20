#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/edit_gate_universal.py — NO SE TOCA CODIGO A CIEGAS, EN NINGUN PROYECTO.

Julio, 2026-08-20: convertir en GARANTIA lo que hoy solo es una promesa.

QUE FALTABA: el `edit_gate.py` de DMM protege solo DMM. En Foto Informe y en los proyectos que
Julio cree manana, cualquiera puede reescribir codigo sin haber mirado el contexto. Este candado
lo cubre TODO, con la misma regla que ya funciona para leer.

REGLA: para tocar codigo de un proyecto declarado hace falta UNA de estas tres:
  a) un PAQUETE MINIMO vigente que declare ese archivo (lo normal), o
  b) que el archivo sea NUEVO (crear no es reescribir), o
  c) que sea algo que no es codigo: contratos, documentos, vigias.

LO QUE NUNCA BLOQUEA (a proposito, para no estorbar):
  · Los .md — los contratos y documentos deben poder escribirse siempre.
  · Las vigias — son test-first: se escriben ANTES de reparar, no despues.
  · Los archivos nuevos — crear no es pisar el trabajo de nadie.
  · Todo, si `INGENIERO_OFF=1`.

Y ademas respeta el candado de contexto: si se perdio el hilo, no se toca nada hasta recuperarlo.
"""
import json, os, sys, glob, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))
PAQUETES = os.path.join(AQUI, "memoria", "paquetes")

CODIGO = (".py", ".html", ".js", ".css", ".ts", ".jsx", ".tsx")
VIGENCIA_HORAS = 8


def _proyectos():
    try:
        from cerebro import grafo
        return grafo.proyectos()
    except Exception:
        return {}


def _de_que_proyecto(fp):
    """¿Este archivo pertenece a algun proyecto declarado? Devuelve (apodo, ruta) o (None, None)."""
    f = os.path.normcase(os.path.abspath(fp))
    mejor = (None, None, -1)
    for apodo, d in _proyectos().items():
        r = os.path.normcase(os.path.abspath(d["ruta"]))
        if f.startswith(r + os.sep) and len(r) > mejor[2]:
            mejor = (apodo, d["ruta"], len(r))
    return mejor[0], mejor[1]


def _paquete_vigente():
    try:
        ps = sorted(glob.glob(os.path.join(PAQUETES, "*.md")), key=os.path.getmtime, reverse=True)
    except Exception:
        return None, ""
    if not ps:
        return None, ""
    if (time.time() - os.path.getmtime(ps[0])) > VIGENCIA_HORAS * 3600:
        return None, ""
    try:
        return ps[0], open(ps[0], encoding="utf-8", errors="ignore").read()
    except Exception:
        return None, ""


def _declarado_en(txt, fp):
    """Solo vale si el paquete lo DECLARA como pieza (`### `ruta``), no si lo nombra de pasada."""
    import re
    base = os.path.basename(fp)
    for m in re.finditer(r"^### `([^`]+?)`", txt or "", re.M):
        if m.group(1).split(":")[0].split("/")[-1].strip() == base:
            return True
    return False


def main():
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input") or {}
    fp = str(ti.get("file_path") or "")
    if not fp:
        return 0

    # contexto perdido: no se toca nada hasta recuperar el hilo
    try:
        import candado_contexto as _cc
        if _cc.hay_marca():
            sys.stderr.write(_cc.aviso())
            return 2
    except Exception:
        pass

    ext = os.path.splitext(fp)[1].lower()
    if ext not in CODIGO:
        return 0                       # documentos y contratos: libres
    rel = fp.replace("\\", "/").lower()
    if "/vigias/" in rel or os.path.basename(fp).startswith("test_"):
        return 0                       # test-first: la vigia se escribe ANTES
    if not os.path.exists(fp):
        return 0                       # archivo nuevo: crear no es reescribir

    apodo, raiz = _de_que_proyecto(fp)
    if not apodo:
        return 0                       # no es de un proyecto declarado: no es asunto nuestro

    # PUNTO MUERTO (fallo real 2026-08-20): si el propio Ingeniero esta roto, el generador de
    # paquetes no arranca... y este candado exige un paquete para poder arreglarlo. Se bloquea
    # la reparacion de si mismo. Un candado NUNCA puede impedir que se le repare.
    # Cura: si el generador de paquetes no arranca, se deja pasar y se avisa.
    try:
        from cerebro import router as _r        # noqa: F401
    except Exception as e:
        sys.stderr.write("AVISO: el generador de paquetes esta roto (%s).\n"
                         "  Se permite la edicion para poder REPARARLO.\n"
                         "  Corre las vigias en cuanto lo arregles.\n" % str(e)[:100])
        return 0

    ruta_pk, txt = _paquete_vigente()
    if txt and _declarado_en(txt, fp):
        return 0                       # esta en el paquete: adelante

    base = os.path.basename(fp)
    sys.stderr.write(
        "BLOQUEADO POR EL CANDADO DE EDICION (Ingeniero VUC)\n"
        f"  Ibas a reescribir codigo de '{apodo}': {base}\n"
        + (f"  Hay un paquete vigente ({os.path.basename(ruta_pk)}) y ese archivo NO esta en el.\n"
           if ruta_pk else "  No hay ningun paquete minimo vigente.\n")
        + "\n  Tocar codigo sin haber mirado el contexto es como se rompen los vecinos.\n"
          "  Pide el paquete del asunto (trae la ley, las piezas, los trozos y a quien danas):\n"
          f'     cd C:\\Ingeniero_VUC; python ingeniero.py trabaja {apodo} "<el problema>"\n'
          "\n  Si de verdad hace falta tocarlo y no sale en el paquete, justificalo:\n"
          "     NECESITO_EDITAR: archivo / motivo / que vigia lo protege / a quien puede danar\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
