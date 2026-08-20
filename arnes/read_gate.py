#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/read_gate.py — EL CANDADO DE LECTURA. La pieza que no existia en ningun lado.

El arnes de DMM (`arnes/edit_gate.py`) frena EDITAR. Nadie frena LEER.
Y el dinero se va leyendo: `app.py` son 10.818 lineas. Cada vez que una IA lo abre entero,
Julio paga por 10.818 lineas para usar 40.

Este candado es un hook PreToolUse de Claude Code. Cuando la IA va a leer un archivo grande:
  1) mira si hay un PAQUETE MINIMO vigente para el trabajo de hoy;
  2) si el archivo NO esta en el paquete y es grande -> BLOQUEA y le dice como pedirlo bien.

No estorba: lo chico se lee libre, y con paquete vigente se lee lo del paquete.
Estilo copiado de `arnes/edit_gate.py` de DMM (Julio, 2026-07-23): un recordatorio se ignora,
solo un candado que FRENA se cumple.
"""
import json, os, sys, glob, time, re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AQUI_ARNES = os.path.join(AQUI, "arnes")
PAQUETES = os.path.join(AQUI, "memoria", "paquetes")
CFG = os.path.join(AQUI, "arnes", "lectura.config")

DEF = {"tope_lineas": "300", "vigencia_horas": "8", "libres": ".md,.config,.json,.txt"}


def cfg():
    d = dict(DEF)
    try:
        for ln in open(CFG, encoding="utf-8").read().splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                d[k.strip()] = v.strip()
    except Exception:
        pass
    return d


def paquete_vigente(horas):
    """El paquete mas nuevo, si no esta rancio. Devuelve (ruta, texto) o (None, '')."""
    try:
        ps = sorted(glob.glob(os.path.join(PAQUETES, "*.md")), key=os.path.getmtime, reverse=True)
    except Exception:
        return None, ""
    if not ps:
        return None, ""
    p = ps[0]
    if (time.time() - os.path.getmtime(p)) > float(horas) * 3600:
        return None, ""
    try:
        return p, open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return None, ""


def lineas_de(ruta):
    try:
        with open(ruta, "rb") as f:
            return f.read().count(b"\n") + 1
    except Exception:
        return 0


def main():
    # INTERRUPTOR DE EMERGENCIA: INGENIERO_OFF=1 aparta el candado.
    # Ningun candado debe poder dejar a Julio atrapado sin salida.
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input") or {}
    fp = str(ti.get("file_path") or "")
    if not fp or not os.path.exists(fp):
        return 0

    # ── CONTEXTO PERDIDO: no se sigue a ciegas ────────────────────────────────
    # Si venimos de una compactacion, TODO esta bloqueado hasta leer AL_VOLVER.md.
    # Y el propio acto de leerlo es lo que desbloquea: no hay atajo.
    try:
        sys.path.insert(0, os.path.join(AQUI_ARNES))
        import candado_contexto as _cc
        if _cc.hay_marca():
            if os.path.normcase(os.path.abspath(fp)) == os.path.normcase(os.path.abspath(_cc.AL_VOLVER)):
                _cc.quitar_marca()
                return 0          # justo lo que habia que hacer: adelante
            sys.stderr.write(_cc.aviso())
            return 2
    except Exception:
        pass

    c = cfg()
    # Leer un pedazo declarado (offset+limit) SIEMPRE se permite: eso es justo lo que se quiere.
    if ti.get("offset") or ti.get("limit"):
        return 0
    if os.path.splitext(fp)[1].lower() in [x.strip() for x in c["libres"].split(",")]:
        return 0

    n = lineas_de(fp)
    if n <= int(c["tope_lineas"]):
        return 0   # lo chico se lee libre: bloquearlo seria estorbar

    ruta_pk, txt = paquete_vigente(c["vigencia_horas"])
    base = os.path.basename(fp)
    # OJO: no vale que el nombre aparezca "de pasada" en un comentario del paquete.
    # Solo vale si el paquete lo DECLARA como pieza o trozo (fallo real detectado 2026-08-20:
    # trozos.py nombra "app.py de Foto Informe" en su docstring y eso abria la puerta a leer
    # las 10.818 lineas enteras).
    declarados = set()
    for m in re.finditer(r"^### `([^`]+?)`", txt or "", re.M):
        declarados.add(m.group(1).split(":")[0].split("/")[-1].strip())
    if base in declarados:
        return 0   # el paquete SI lo declara: adelante

    sys.stderr.write(
        "BLOQUEADO POR EL CANDADO DE LECTURA (Ingeniero VUC)\n"
        f"  Ibas a leer ENTERO: {base}  ({n:,} lineas)\n"
        + (f"  Paquete vigente: {os.path.basename(ruta_pk)} — y ese archivo NO esta en el.\n"
           if ruta_pk else "  No hay paquete minimo vigente para este trabajo.\n")
        + "\n  Haz UNA de estas tres, ninguna cuesta caro:\n"
          "  1) Pide el paquete del asunto (esto es lo normal):\n"
          '       cd C:\Ingeniero_VUC; python -m cerebro.router <proyecto> "<el problema en tus palabras>"\n'
          "  2) Lee solo el pedazo que necesitas, con su direccion exacta:\n"
          "       Read(file_path=..., offset=<linea>, limit=<cuantas>)\n"
          "  3) Si de verdad hace falta el archivo entero, justificalo:\n"
          "       NECESITO_LEER: archivo / motivo / decide / riesgo\n"
          "\n  Regla: leer de mas se PIDE, no se hace.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
