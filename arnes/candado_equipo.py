# -*- coding: utf-8 -*-
"""arnes/candado_equipo.py — NO SE ESCRIBE CODIGO A SOLAS. SIEMPRE EL EQUIPO.

Julio, 2026-08-21, despues de tener que repetirlo otra vez:
  "pon candado de modo que siempre tengas que trabajar con equipo, y vigias para el arnes, que
   te frene cuando no lo hagas."
  "pon candado para que siempre actues con equipo, modo ingeniero y economico, sin excusa."
  "por no trabajar en equipo ya has gastado 19."

EL AGUJERO QUE TAPA: la regla estaba escrita, en la memoria y en el protocolo, y aun asi se
escribio a solas un guardia entero, tres vigias y cuatro reparaciones. Escrito no es cumplido.
Julio lo pago de su bolsillo. Una regla que depende de que yo me acuerde NO es una regla.

LO QUE EXIGE: para tocar CODIGO tiene que haber un veredicto del equipo RECIENTE que cubra ese
archivo. Uno genera, OTRO distinto audita (4 ojos: nadie se aprueba a si mismo).

  cd C:\Ingeniero_VUC; python ingeniero.py equipo <proyecto> "<la tarea>"

LO QUE NO ESTORBA (o el candado se vuelve un muro y se acaba apagando, que es peor):
  · los documentos .md          — escribir la ley no es programar
  · archivo nuevo que no existe — crear no es reescribir
  · el propio arnes             — si el candado se rompe, hay que poder arreglarlo
  · si NO hay ningun cerebro    — no se deja a Julio atrapado por una cuota agotada; se deja
                                  pasar y queda APUNTADO, para que se vea que se paso sin equipo

INVIOLABLE no es que no haya salida: es que la salida deje rastro. Cada vez que se escribe codigo
sin equipo queda en memoria/SIN_EQUIPO.log, y una vigia lo cuenta.
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

VEREDICTO = os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
SIN_EQUIPO = os.path.join(AQUI, "memoria", "SIN_EQUIPO.log")
VIGENCIA_MIN = 90          # un veredicto vale hora y media: lo que dura una tanda de trabajo
CODIGO = (".py", ".js", ".html", ".ts", ".jsx", ".tsx", ".css", ".sql")


def _ruta_veredicto():
    return os.environ.get("INGENIERO_VEREDICTO_TEST") or VEREDICTO


def _ruta_sin_equipo():
    return os.environ.get("INGENIERO_SIN_EQUIPO_TEST") or SIN_EQUIPO


def guardar_veredicto(tarea, archivos, obrero, auditor, veredicto):
    """Lo llama `ingeniero.py equipo` cuando el equipo termina. Es la llave."""
    d = {"cuando": time.time(), "tarea": tarea, "archivos": list(archivos or []),
         "obrero": obrero, "auditor": auditor, "veredicto": veredicto}
    os.makedirs(os.path.dirname(_ruta_veredicto()), exist_ok=True)
    json.dump(d, open(_ruta_veredicto(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def veredicto_vigente():
    """El veredicto del equipo si sigue fresco, o None."""
    try:
        d = json.load(open(_ruta_veredicto(), encoding="utf-8"))
    except Exception:
        return None
    if (time.time() - float(d.get("cuando", 0))) > VIGENCIA_MIN * 60:
        return None
    return d


def cubre(d, fp):
    """¿El veredicto habla de ESTE archivo? Un veredicto sobre otra cosa no vale de llave."""
    if not d:
        return False
    base = os.path.basename(fp).lower()
    for a in d.get("archivos", []):
        if os.path.basename(str(a)).lower() == base:
            return True
    return False


def _hay_cerebros():
    try:
        from cuerpo import obrero
        return bool(obrero.quienes_hay())
    except Exception:
        return False


def _apuntar_sin_equipo(fp, por_que):
    try:
        os.makedirs(os.path.dirname(_ruta_sin_equipo()), exist_ok=True)
        with open(_ruta_sin_equipo(), "a", encoding="utf-8") as f:
            f.write("%s  %s  (%s)\n" % (time.strftime("%Y-%m-%d %H:%M"), fp[:120], por_que))
    except Exception:
        pass


MENSAJE = (
    "BLOQUEADO: NO SE ESCRIBE CODIGO A SOLAS\n\n"
    "  {fp}\n\n"
    "  Julio tuvo que repetirlo tres veces y le costo dinero. Uno GENERA, otro distinto AUDITA;\n"
    "  yo dirijo y leo el veredicto. Escribirlo yo mismo gasta lo caro para hacer lo barato.\n\n"
    "  Que hacer:\n"
    "     cd C:\Ingeniero_VUC; python ingeniero.py equipo <proyecto> \"<la tarea>\"\n\n"
    "  Eso deja el veredicto, y con el veredicto este archivo se abre. Los documentos .md,\n"
    "  los archivos nuevos y el propio arnes se pueden tocar siempre.\n")


def main():
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = str((data.get("tool_input") or {}).get("file_path") or "")
    if not fp:
        return 0
    if os.path.splitext(fp)[1].lower() not in CODIGO:
        return 0                                    # documentos: libres
    if not os.path.exists(fp):
        return 0                                    # crear no es reescribir
    rel = fp.replace("\\", "/").lower()
    if "/arnes/" in rel:
        return 0                                    # hay que poder arreglar el propio candado
    if not _hay_cerebros():
        _apuntar_sin_equipo(fp, "no habia ningun cerebro disponible")
        return 0                                    # nunca dejar a Julio atrapado
    d = veredicto_vigente()
    if cubre(d, fp):
        return 0                                    # el equipo ya lo miro: adelante
    sys.stderr.write(MENSAJE.format(fp=fp))
    return 2


if __name__ == "__main__":
    sys.exit(main())
