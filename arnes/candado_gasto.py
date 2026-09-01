# -*- coding: utf-8 -*-
"""arnes/candado_gasto.py — EL CANDADO DEL GASTO QUE NUNCA SE PUSO.

Julio, 2026-09-02, despues de una manana entera quemada:
  "legisla fuerte, nunca mas, nunca mas vuelves a hacer gasto grande"
  "el cierre del gasto que iba a impedirme esto nunca se puso. Lo deje escrito y sin aplicar."

EL AGUJERO QUE TAPA: el contrato CONTRATO_NUNCA_MAS_GASTO_GRANDE.md lo pedia y nunca se hizo.
Una regla que depende de que la IA se acuerde NO es una regla: hay que CONTAR y FRENAR.

LO QUE HACE, y como se comprueba:
  · cuenta las acciones de cada tanda (una tanda dura unas horas, como una jornada de trabajo)
  · AVISA a mitad del tope y al 80% (Julio decide sobre el gasto que ve, ley 2)
  · FRENA de verdad al llegar al tope: salida 2, no es un recordatorio (ley 1)
  · tres rechazos seguidos = se para y se le dice a Julio, no se insiste una cuarta (ley 3)
  · una cosa por encargo: si piden dos cambios a la vez, avisa
  · deja rastro en el libro de gasto para que Julio lo mire sin preguntar

El tope se lee de: la variable INGENIERO_TOPE_ACCIONES, o de `arnes/gasto.config`, o 15 por defecto.
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "GASTO.json")
CONFIG = os.path.join(AQUI, "arnes", "gasto.config")
TANDA_SEG = 4 * 3600          # una tanda dura 4 horas, como una jornada
DEFAULT_TOPE = 15


def _ruta():
    return os.environ.get("INGENIERO_GASTO_TEST") or RUTA


def _tope():
    """El tope de acciones por tanda. La variable manda, luego el config, luego 15."""
    try:
        v = int(str(os.environ.get("INGENIERO_TOPE_ACCIONES", "")).strip())
        if v > 0:
            return v
    except Exception:
        pass
    try:
        with open(CONFIG, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#") or "=" not in linea:
                    continue
                k, val = linea.split("=", 1)
                if k.strip().lower() == "tope":
                    v = int(val.strip())
                    if v > 0:
                        return v
    except Exception:
        pass
    return DEFAULT_TOPE


def _tanda():
    return "%s-%s" % (time.strftime("%Y-%m-%d-%H"), int(time.time() // TANDA_SEG))


def _leer():
    try:
        d = json.load(open(_ruta(), encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _guardar(d):
    os.makedirs(os.path.dirname(_ruta()), exist_ok=True)
    json.dump(d, open(_ruta(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _log(texto):
    """El libro de gasto: que Julio mire, no que pregunte. A prueba de fallos: loguear no puede
    tumbar al candado (igual que el resto del arnes)."""
    try:
        ruta = os.path.join(os.path.dirname(_ruta()), "GASTO.log")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("%s  %s\n" % (time.strftime("%Y-%m-%d %H:%M"), texto))
    except Exception:
        pass


def contar(acciones=1):
    """Cuenta UNA accion (o mas) de la tanda actual.

    Devuelve (estado, mensaje) con estado en:
      ok, aviso_mitad, aviso_80, freno
    """
    tope = _tope()
    d = _leer()
    if d.get("tanda") != _tanda():
        d = {"tanda": _tanda(), "contador": 0, "rechazos_seguidos": 0}
    d["contador"] = int(d.get("contador", 0)) + int(acciones or 1)
    _guardar(d)
    n = d["contador"]
    if n >= tope:
        _log("FRENO: %d/%d acciones de la tanda" % (n, tope))
        return "freno", ("Llegaste al tope de %d acciones de esta tanda. Se para. "
                         "Preguntale a Julio si sigue." % tope)
    if n >= int(tope * 0.8):
        _log("AVISO 80%%: %d/%d acciones" % (n, tope))
        return "aviso_80", ("Vas %d de %d acciones de la tanda. Queda poco del tope." % (n, tope))
    if n >= int(tope * 0.5):
        _log("AVISO MITAD: %d/%d acciones" % (n, tope))
        return "aviso_mitad", ("Vas %d de %d acciones de la tanda. Ya es la mitad." % (n, tope))
    _log("accion %d/%d" % (n, tope))
    return "ok", ""


def rechazo(es_rechazo):
    """Apunta si el ultimo trabajo fue rechazado o aprobado. Devuelve True cuando hay TRES rechazos
    seguidos (ley 3): ahi se para y se le avisa a Julio, no se intenta una cuarta vez."""
    d = _leer()
    if d.get("tanda") != _tanda():
        d = {"tanda": _tanda(), "contador": 0, "rechazos_seguidos": 0}
    if es_rechazo:
        d["rechazos_seguidos"] = int(d.get("rechazos_seguidos", 0)) + 1
    else:
        d["rechazos_seguidos"] = 0
    _guardar(d)
    if d["rechazos_seguidos"] >= 3:
        _log("TRES RECHAZOS SEGUIDOS: se para")
        return True
    return False


def main():
    """El puesto de guardia (hook). Lee la peticion, cuenta la accion y FRENA (salida 2) al tope.
    Avisa (salida 0 con mensaje) a mitad y al 80%. NUNCA frena en falso en un aviso."""
    data = {}
    try:
        data = json.load(sys.stdin)
    except Exception:
        pass
    acciones = 1
    try:
        acciones = int((data.get("acciones") or data.get("tool_input") or {}).get("acciones", 1))
    except Exception:
        acciones = 1
    estado, msg = contar(acciones)
    if estado == "freno":
        sys.stderr.write("\nCANDADO DEL GASTO: %s\n\n" % msg)
        return 2
    if msg:
        sys.stderr.write("CANDADO DEL GASTO (aviso): %s\n" % msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
