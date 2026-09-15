#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/canal.py — EL CANAL INTERNO AI-AI (con disparador).

Permite que Claude, Cline (identidad "4ojos" en este canal) y ChatGPT se dejen mensajes en disco, y que el
DISPARADOR (hook UserPromptSubmit) se los inyecte a quien despierte. Asi no hace falta
copiar y pegar texto de una ventana a otra: la IA que se despierta recibe los mensajes
que le dejaron las otras.

    python arnes/canal.py enviar <para> "<texto>"   -> deja un mensaje en la bandeja
    python arnes/canal.py leer                        -> saca los pendientes (uso interno del hook)

IDENTIDAD: cada IA se firma con la variable de entorno INGENIERO_QUIEN (claude, cline
[alias 4ojos], chatgpt). Si no esta, firma como "desconocido". Leer SOLO muestra y marca como leidos los
mensajes dirigidos a quien lee (o a "*" / "todos"); los ajenos NO se tocan (fix tras la
auditoria de Claude: antes 'se comia' los mensajes de los demas).

REGLAS DEL CANAL (Ley 6, no repetidera; nunca inventar):
  - el texto del mensaje es el del autor, tal cual. No se reescribe, no se adorna.
  - un mensaje se marca LEIDO solo si es de quien lee, para no robarlo al destinatario real.
  - si no hay mensajes, el hook no devuelve nada (silencioso, no estorba).
"""
import os, sys, json, glob, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDEJA = os.path.join(AQUI, "memoria", "canal")


def _bandeja():
    return os.environ.get("INGENIERO_CANAL_TEST") or BANDEJA


def _quien():
    return (os.environ.get("INGENIERO_QUIEN", "") or "desconocido").strip() or "desconocido"


def enviar(para, texto, de=None):
    de = de or _quien()
    os.makedirs(_bandeja(), exist_ok=True)
    ruta = os.path.join(_bandeja(), "%s.json" % int(time.time() * 1000))
    json.dump({"de": de, "para": para, "texto": texto,
               "cuando": time.strftime("%Y-%m-%d %H:%M"), "leido": False},
              open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    _llamar(para, texto)          # el llamado: que la otra IA 'sienta' que le escribieron
    try:
        cerrar_recados_de(para, de or _quien())
    except Exception:
        pass
    return ruta


def cerrar_recados_de(quien, por_quien):
    """Cierra los recados que 'quien' dejo, marcandolos como respondidos por 'por_quien'."""
    cerrados = 0
    if not os.path.isdir(_bandeja()):
        return cerrados
    for ruta in glob.glob(os.path.join(_bandeja(), "*.json")):
        try:
            with open(ruta, encoding="utf-8") as f:
                m = json.load(f)
            if str(m.get("de", "")).strip().lower() != quien.strip().lower():
                continue
            if m.get("respondido"):
                continue
            m["respondido"] = True
            m["respondido_por"] = por_quien
            m["respondido_cuando"] = time.strftime("%Y-%m-%d %H:%M")
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(m, f, ensure_ascii=False, indent=1)
            cerrados += 1
        except Exception:
            continue
    return cerrados


def _llamar(para, texto):
    """Deja la MARCA del llamado sin abrir ninguna ventana.

    APAGADO DE RAIZ (Julio, 2026-08-27): antes se lanzaba `llamar.py` como subproceso, y aunque el
    toast (aviso visual) estaba apagado, el subproceso abria una ventana de PowerShell cada vez que
    alguien dejaba un mensaje. Ahora se escribe la marca DIRECTAMENTE (sin subproceso, sin ventana):
    la marca (memoria/canal/llamados/<para>.txt) es lo que la IA lee para enterarse del llamado. El
    aviso visual (toast) solo sale si INGENIERO_LLAMAR_TOAST=1, y en ese caso si se lanza.
    """
    try:
        import sys as _sys
        _sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import llamar as _ll
        _ll.marcar(para, texto)          # la marca SIEMPRE se escribe (el llamado no se pierde)
        if os.environ.get("INGENIERO_LLAMAR_TOAST", "").strip() == "1":
            _ll._toast(para, texto)      # el aviso visual solo si Julio lo pide
    except Exception:
        pass


def leer(para=None, marcar=True):
    """Los mensajes pendientes PARA ESTA IA (o los de "*"/"todos"). Los ajenos no se tocan
    ni se marcan leidos, para no robarselos al destinatario real (fix 4ojos tras la auditoria
    de Claude: antes leer 'se comia' los mensajes de todos).
    Fallo 2026-09-15: se marcaba leido al leerlo, antes de entregarlo, y se perdia.
    Con marcar=False no escribe nada; solo devuelve, con su ruta, para entregar despues."""
    para = para or _quien()
    salida = []
    if not os.path.isdir(_bandeja()):
        return salida
    for ruta in sorted(glob.glob(os.path.join(_bandeja(), "*.json"))):
        try:
            m = json.load(open(ruta, encoding="utf-8"))
        except Exception:
            continue
        destino = str(m.get("para", "")).strip()
        if destino not in (para, "*", "todos", "todas", "todos los"):
            continue                      # no es tuyo: ni se muestra ni se marca leido
        if m.get("leido"):
            continue
        m["ruta"] = ruta
        salida.append(m)
        if marcar:
            try:
                m["leido"] = True
                json.dump(m, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            except Exception:
                pass
    return salida


# Fallo 2026-09-15: el recado se marcaba leido al leerlo, antes de entregarlo, y se perdia.
def marcar_leidos(rutas):
    """Marca leido=True en cada ruta y lo guarda. Nunca lanza. Devuelve cuantas marco."""
    marcados = 0
    for ruta in rutas:
        try:
            m = json.load(open(ruta, encoding="utf-8"))
            m["leido"] = True
            json.dump(m, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            marcados += 1
        except Exception:
            continue
    return marcados


def texto_leer(para=None):
    msgs = leer(para)
    if not msgs:
        return ""
    L = ["CANAL INTERNO — mensajes que te dejaron mientras no estabas:"]
    for m in msgs:
        L.append("  • de %s (%s): %s" % (m.get("de", "?"), m.get("cuando", "?"), m.get("texto", "")))
    L.append("")
    L.append("LOOP: si este mensaje te pide actuar, al terminar responde por el canal con:")
    L.append("  python arnes/canal.py enviar <destino> \"<tu resumen o veredicto>\"")
    L.append("Asi la otra IA recibe tu respuesta en su proxima instruccion y el ciclo sigue.")
    return "\n".join(L)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "leer"
    if q == "enviar" and len(sys.argv) >= 4:
        ruta = enviar(sys.argv[2], " ".join(sys.argv[3:]))
        print("CANAL: mensaje a '%s' guardado en %s" % (sys.argv[2], ruta))
        sys.exit(0)
    # uso del hook: si hay mensajes, salida en formato que Claude inyecta como contexto.
    txt = texto_leer()
    if txt:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                  "additionalContext": txt}},
                         ensure_ascii=False))
    # si no hay, no se imprime nada: hook silencioso, no estorba.
