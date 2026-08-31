#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_buzon.py — EL BUZON DE CLINE: no se trabaje sin leer lo que dejaron.

Julio, 2026-08-31: "cuando trabaje contigo, debes estar mirando el buzon... crea un mecanismo que
te active cuando claude este trabajando, legislalo, pon candado y crea vigia, no debe depender de
que te acuerdes."

EL FALLO MEDIDO: el canal (canal.py) deja los mensajes de Claude para Cline en disco, pero Cline no
los veia salvo que Julio le dijera "mira el buzon". Eso dependia de que Cline se acordara, y ya
esta escrito en la memoria de fallos que "depender de que la IA se acuerde" NO funciona.

LA CURA: este candado hace FISICO ver el buzon. Se engancha a UserPromptSubmit (cuando arranca un
turno) y a Stop (cuando termina). Si hay un mensaje de otro agente PARA CLINE sin leer, BLOQUEA y
lo muestra. No se puede trabajar sin verlo. Claude NO se bloquea a si mismo por los mensajes que el
envio a Cline.

Anti-bucle (como todos los candados): TOPE_BLOQUEOS seguidos y salida por autorizacion de Julio.
"""
import glob
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDEJA = os.path.join(AQUI, "memoria", "canal")
CONTADOR = os.path.join(AQUI, "memoria", ".buzon_bloqueos")
TOPE_BLOQUEOS = 2

def _quien():
    return (os.environ.get("INGENIERO_QUIEN", "") or "desconocido").strip() or "desconocido"


def _companero_activo():
    """Nombre del companero ACTIVO si ya existe la pieza (arnes/companero.py, en construccion).

    Si aun no existe (o falla), devuelve '' y el candado NO depende de ella: se cubre solo con
    quien corre. Nunca se rompe por una pieza que todavia no esta.
    """
    try:
        import companero  # mismo arnes
        return str(companero.activo() or "").strip().lower()
    except Exception:
        return ""


def _destinos():
    """A quien le pueden escribir y debe mirar el buzon.

    Ya NO es una lista clavada a mano con "cline": sale de quien corre ahora y del companero
    activo (si la pieza ya existe). Asi, el dia que Julio cambie de companero, el buzon lo sigue
    sin reescribir nada a mano.
    """
    destinos = {"*", "todos", "todas", " todos los"}
    yo = _quien()
    if yo and yo != "desconocido":
        destinos.add(yo)
    activo = _companero_activo()
    if activo and activo != "desconocido":
        destinos.add(activo)
    # Alias historicos para no romper los mensajes viejos que ya estan en la bandeja.
    destinos.update(("cline", "4ojos"))
    return destinos

def _bandeja():
    """Donde estan los recados. Se resuelve cada vez, no al importar, para que las pruebas la
    desvien y no toquen la bandeja de verdad.

    FALTABA: esta funcion se llamaba pero nadie la habia escrito, asi que mensajes_pendientes()
    se caia en silencio y el candado devolvia 'no hay nada' SIEMPRE. Un candado que se cae y
    contesta que todo esta bien es peor que no tenerlo. Cazado el 2026-08-31.
    """
    return os.environ.get("INGENIERO_BUZON_BANDEJA", "").strip() or BANDEJA


def mensajes_pendientes():
    """Mensajes PARa el agente activo (o para todos) SIN leer, que vienen de OTRO agente.

    Son los encargos/pedidos que la otra IA le dejo y que quien corre todavia no vio. Un mensaje
    que ya se marco leido, o que viene del propio agente, no cuenta. Devuelve (pendientes, unico):
      - pendientes: lista de mensajes de otros que aun no se vieron
      - unico:      el remitente, si TODOS los mensajes (sin filtrar por 'de propio') salieron de
                    un mismo emisor; si no, None. Se usa para deducir quien corre cuando no hay
                    identidad (fix del fallo 1 de Claude).
    """
    bn = _bandeja()
    todos = []
    if os.path.isdir(bn):
        for ruta in sorted(glob.glob(os.path.join(bn, "*.json"))):
            try:
                m = json.load(open(ruta, encoding="utf-8"))
            except Exception:
                continue
            if m.get("leido"):
                continue
            todos.append(m)
    # deducir si todo vino de un mismo emisor (para el caso 'sin identidad')
    emisores = {str(m.get("de", "")).strip() for m in todos}
    unico = emisores.pop() if len(emisores) == 1 else None

    yo = _quien()
    dest = _destinos()
    out = []
    for m in todos:
        para = str(m.get("para", "")).strip()
        if para not in dest:
            continue                       # no va dirigido a quien mira el buzon
        de = str(m.get("de", "")).strip()
        if de == yo:
            continue                       # lo mande yo mismo: no me bloquea
        out.append(m)
    return out, unico


def _ruta_contador():
    """La cuenta de frenadas. Se resuelve cada vez para que las pruebas la desvien y no toquen
    la memoria de verdad; si no, una prueba deja el contador al tope y el candado deja de frenar
    de verdad sin que nadie se entere."""
    return os.environ.get("INGENIERO_BUZON_CONTADOR", "").strip() or CONTADOR


def _cuantas_veces_ya_freno():
    try:
        with open(_ruta_contador(), encoding="utf-8") as f:
            return int((f.read() or "0").strip() or 0)
    except Exception:
        return 0


def _apuntar_frenada(n):
    try:
        ruta = _ruta_contador()
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(str(n))
    except Exception:
        pass


def main():
    """Frena si hay un recado SIN CONTESTAR de la otra IA. Y solo si es de verdad de otra IA.

    EL FALLO QUE ESTO CIERRA (medido el 2026-08-31): a Claude se le bloqueaba ensenandole SUS
    PROPIOS mensajes. Sabia quien corre solo por una variable de entorno que nadie pone, asi que
    quien corre era 'desconocido' y la excepcion de "no me bloqueo por lo que yo mande" nunca se
    aplicaba. Ahora, si no consta quien corre y TODOS los recados sin leer vienen del mismo
    remitente, se entiende que quien corre es ese mismo y NO se bloquea.

    Y ante la duda se AVISA, no se frena: parar el trabajo de todos es peor que un aviso.
    """
    try:
        import autorizacion
        if autorizacion.autorizada():
            return 0                       # la llave de Julio manda
    except Exception:
        pass

    try:
        pendientes, unico = mensajes_pendientes()
    except Exception:
        return 0                           # este candado nunca puede tumbar el trabajo

    if not pendientes:
        _apuntar_frenada(0)
        return 0

    yo = _quien()
    if yo == "desconocido" and unico:
        # No consta quien corre, pero todos los recados sin leer los envio el mismo. Ese mismo no
        # puede estar pidiendose cuentas a si mismo: se avisa y se deja pasar.
        sys.stderr.write("\nAVISO (buzon): hay %d recado(s) en la bandeja, todos enviados por "
                         "'%s'. No se frena porque no consta que sean para quien trabaja ahora.\n"
                         % (len(pendientes), unico))
        return 0

    veces = _cuantas_veces_ya_freno()
    if veces >= TOPE_BLOQUEOS:
        # ANTI-BUCLE: ya se aviso dos veces. Un candado que frena para siempre se acaba apagando.
        sys.stderr.write("\nAVISO (buzon, ya no frena mas): siguen %d recado(s) sin contestar.\n"
                         % len(pendientes))
        return 0

    _apuntar_frenada(veces + 1)
    sys.stderr.write(
        "\nNO SE PUEDE TRABAJAR — HAY RECADOS SIN CONTESTAR EN EL BUZON:\n\n"
        + "\n".join("  - de %s (%s): %s" % (m.get("de", "?"), m.get("cuando", "?"),
                                            str(m.get("texto", ""))[:110].replace("\n", " "))
                    for m in pendientes[:6])
        + "\n\n  Leelos y contesta antes de seguir:\n"
          "     cd C:\\Ingeniero_VUC; python arnes/canal.py leer\n"
          "  y contesta con:  python arnes/canal.py enviar <a quien> \"<tu respuesta>\"\n")
    try:
        import candados_medicion
        candados_medicion.cazado("buzon")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())


