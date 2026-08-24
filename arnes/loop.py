#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/loop.py — EL BUCLE AUTOMATICO AI-AI (Julio, 2026-08-24).

Que Claude y Cline se comuniquen en AUTOMATICO, sin que Julio intervenga.

El canal (canal.py) deja mensajes en disco pero es PASIVO: solo entrega cuando la otra IA
despierta. Para que sea automatico hace falta un VIGILANTE que procese el encargo en segundo
plano con el EQUIPO (los cerebros) y le devuelva el resultado al otro. Eso es este bucle.

    python arnes/loop.py iniciar <proyecto> "<problema>" --para claude --de cline
    python arnes/loop.py paso                 -> un ciclo: si hay encargo, lo procesa
    python arnes/loop.py bucle                -> se queda vigilando (en segundo plano)
    python arnes/loop.py parar                -> frena el bucle (marca PARAR)
    python arnes/loop.py estado               -> que hay ahora

SEGURIDAD (nada puede quemar plata ni dar vueltas para siempre):
  · RONDAS_MAX por encargo (tope duro). Al llegar, el encargo se da por terminado.
  · archivo PARAR que corta el ciclo de una vez.
  · el encargo lo procesa `subagentes` (el equipo), nunca a ciegas.
  · cada paso queda en memoria/canal/loop.log.
"""
import os
import sys
import json
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDEJA = os.path.join(AQUI, "memoria", "canal")
ENCARGO = os.path.join(BANDEJA, ".encargo.json")
PARAR = os.path.join(BANDEJA, ".parar")
LOG = os.path.join(BANDEJA, "loop.log")
RONDAS_MAX = 5          # tope duro de vueltas por encargo


def _ruta_de(nombre):
    base = os.environ.get("INGENIERO_LOOP_TEST_DIR")
    if base:
        return os.path.join(base, os.path.basename(nombre))
    return nombre


def _log(msg):
    try:
        os.makedirs(os.path.dirname(_ruta_de(LOG)), exist_ok=True)
        with open(_ruta_de(LOG), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M") + "  " + str(msg)[:300] + "\n")
    except Exception:
        pass


def iniciar(proyecto, problema, para="claude", de="cline", rondas_max=RONDAS_MAX):
    """Deja el encargo para que el bucle lo procese y le devuelva el resultado a `para`."""
    e = {"proyecto": proyecto, "problema": problema, "para": para, "de": de,
         "rondas_max": int(rondas_max), "vuelta": 0,
         "cuando": time.strftime("%Y-%m-%d %H:%M")}
    os.makedirs(os.path.dirname(_ruta_de(ENCARGO)), exist_ok=True)
    json.dump(e, open(_ruta_de(ENCARGO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if os.path.exists(_ruta_de(PARAR)):
        os.remove(_ruta_de(PARAR))
    _log("ENCARGO iniciado por %s para %s: %s" % (de, para, problema[:80]))
    return e


def parar():
    os.makedirs(os.path.dirname(_ruta_de(PARAR)), exist_ok=True)
    open(_ruta_de(PARAR), "w", encoding="utf-8").write(time.strftime("%Y-%m-%d %H:%M"))
    _log("BUCLE PARADO por orden de parar")
    return True


def _encargo():
    try:
        return json.load(open(_ruta_de(ENCARGO), encoding="utf-8"))
    except Exception:
        return None


def _procesar(e):
    """Manda el encargo al EQUIPO (subagentes) y devuelve el veredicto corto."""
    sys.path.insert(0, AQUI)
    from cuerpo import subagentes
    r = subagentes.lanzar(e["proyecto"], e["problema"])     # espera; usa los cerebros
    return subagentes.veredicto(r)


def paso(procesar=True):
    """Un ciclo del bucle. Devuelve un texto corto de que paso."""
    e = _encargo()
    if not e:
        return "sin encargo"
    if os.path.exists(_ruta_de(PARAR)):
        _log("frenado por PARAR (habia encargo pendiente)")
        return "parado"
    vuelta = int(e.get("vuelta", 0))
    if vuelta >= int(e.get("rondas_max", RONDAS_MAX)):
        _log("tope de vueltas alcanzado (%d): encargo terminado" % vuelta)
        try:
            os.remove(_ruta_de(ENCARGO))
        except Exception:
            pass
        return "tope"
    if not procesar:
        return "listo_para_procesar"
    # MARCA DE CORRIENDO: que no se doble un paso por dos disparos a la vez.
    corriendo = _ruta_de(ENCARGO) + ".corriendo"
    if os.path.exists(corriendo):
        return "ya_corriendo"
    try:
        open(corriendo, "w", encoding="utf-8").write(str(time.time()))
        veredicto = _procesar(e)
        try:
            import canal  # noqa: E402  (mismo arnes)
            canal.enviar(e["para"], "[LOOP r%d] %s" % (vuelta + 1, veredicto)[:600], de="loop")
        except Exception as ex:
            _log("no se pudo responder por el canal: %s" % str(ex)[:100])
        e["vuelta"] = vuelta + 1
        json.dump(e, open(_ruta_de(ENCARGO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        _log("ronda %d procesada para %s (%s)" % (vuelta + 1, e["para"], e["problema"][:60]))
        return "procesado ronda %d" % (vuelta + 1)
    except Exception as ex:
        _log("ronda %d FALLO: %s" % (vuelta + 1, str(ex)[:120]))
        return "fallo: " + str(ex)[:120]
    finally:
        try:
            if os.path.exists(corriendo):
                os.remove(corriendo)
        except Exception:
            pass


def estado():
    e = _encargo()
    if not e:
        return "SIN ENCARGO. El bucle espera. `python arnes/loop.py iniciar ...`"
    parado = "SI" if os.path.exists(_ruta_de(PARAR)) else "no"
    L = ["ENCARGO: %s -> %s (proyecto %s)" % (e["de"], e["para"], e["proyecto"])]
    L.append("  problema  : %s" % e["problema"][:120])
    L.append("  vuelta    : %s/%s   PARAR: %s" % (e["vuelta"], e["rondas_max"], parado))
    return "\n".join(L)


def bucle(intervalo=10):
    """Se queda vigilando (correrlo aparte, en segundo plano)."""
    _log("BUCLE encendido (intervalo %ss)" % intervalo)
    while True:
        r = paso()
        if r == "tope":
            _log("bucle termina por tope")
            break
        time.sleep(intervalo)
    return 0


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "estado"
    if q == "iniciar" and len(sys.argv) >= 3:
        args = sys.argv[2:]
        para, de = "claude", "cline"
        corte = len(args)
        for flag in ("--para", "--de"):
            if flag in args:
                i = args.index(flag)
                val = args[i + 1] if len(args) > i + 1 else ""
                if flag == "--para":
                    para = val
                else:
                    de = val
                corte = min(corte, i)
        proyecto = args[0]
        problema = " ".join(args[1:corte]) if corte > 1 else ""
        print(json.dumps(iniciar(proyecto, problema, para=para, de=de), ensure_ascii=False))
        sys.exit(0)
    if q == "parar":
        parar()
        print("BUCLE PARADO.")
        sys.exit(0)
    if q == "bucle":
        sys.exit(bucle())
    if q == "paso":
        print(paso())
        sys.exit(0)
    if q == "estado":
        print(estado())
        sys.exit(0)
    print(__doc__)
    sys.exit(1)

