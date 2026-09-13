#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_atento_canal.py — EL QUE MANDA POR EL CANAL A CLAUDE, ESPERA.

Julio, 2026-09-13 (bloque B8): "cuando le des un mensaje por el canal a claude, queda atento
cada 5 minutos, y espera una hora en total."

EL AGUJERO QUE TAPA: se le enviaba un mensaje a Claude por el canal (bandeja AI-AI) y el que lo
enviaba seguia con otra cosa o se iba, sin recoger la respuesta. El mensaje quedaba sin recoger,
la conversacion se acababa, y se repetia lo de siempre: trabajo pedido que nadie recogio, rondas
que se pierden porque el que esperaba no estaba atento. Julio lo dice claro: el que manda, espera.

LO QUE HACE (el freno, no un recordatorio):
  · empezar()       -> deja la MARCA de espera: con que hora se envio el mensaje a Claude.
  · toca_revisar()  -> hay que mirar el canal AHORA (pasaron 5 minutos desde la ultima revision).
  · respondido()    -> llego una respuesta de Claude posterior al envio: se recoge y se termina.
  · vencido()       -> paso la hora total sin respuesta: hay que avisar por el canal y por escrito
                       que la espera se vencio (no abandona sin avisar).
  · estado()        -> un resumen para saber exactamente donde esta la espera.

Uso:
    python arnes/candado_atento_canal.py empezar          <- al enviar mensaje a Claude
    python arnes/candado_atento_canal.py verificar        <- cuando se despierta / cada 5 min

Se prueba con INGENIERO_CANAL_TEST y INGENIERO_ESPERA_TEST apuntando a carpetas de prueba.
"""
import json
import os
import sys
import time
import glob

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDEJA = os.path.join(AQUI, "memoria", "canal")
ESPERAS = os.path.join(AQUI, "memoria", "canal", "esperas")

RITMO_SEG = 5 * 60        # cada 5 minutos
TOTAL_SEG = 60 * 60       # una hora en total


def _bandeja():
    return os.environ.get("INGENIERO_CANAL_TEST") or BANDEJA


def _carpeta_esperas():
    return os.environ.get("INGENIERO_ESPERA_TEST") or ESPERAS


def _quien():
    return (os.environ.get("INGENIERO_QUIEN", "") or "desconocido").strip() or "desconocido"


def _ruta_espera(de):
    return os.path.join(_carpeta_esperas(), "%s.json" % (de or _quien()))


def _ahora():
    return os.environ.get("INGENIERO_ESPERA_AHORA") or time.time() * 1000


def _ms(ahora):
    try:
        return float(ahora)
    except (TypeError, ValueError):
        return time.time() * 1000


def empezar(de=None, enviado_ms=None):
    """Marca que 'de' envió un mensaje a Claude por el canal y queda esperando respuesta.

    Devuelve el dict de la espera recién creada (o {}) si no se pudo escribir.
    """
    de = de or _quien()
    if not de:
        return {}
    d = {"de": de, "enviado_ms": _ms(enviado_ms or _ahora()),
         "ultima_revision_ms": 0, "aviso_vencido": False}
    try:
        os.makedirs(_carpeta_esperas(), exist_ok=True)
        json.dump(d, open(_ruta_espera(de), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except Exception:
        return {}
    return d


def _leer_espera(de):
    de = de or _quien()
    try:
        return json.load(open(_ruta_espera(de), encoding="utf-8"))
    except Exception:
        return {}


def _respondio_claude(de, enviado_ms):
    """¿Hay un mensaje de claude hacia 'de' con timestamp posterior al envio?"""
    if not os.path.isdir(_bandeja()):
        return False
    try:
        enviado = float(enviado_ms)
    except (TypeError, ValueError):
        return False
    for ruta in glob.glob(os.path.join(_bandeja(), "*.json")):
        nombre = os.path.basename(ruta).replace(".json", "")
        try:
            ts = float(nombre)
        except ValueError:
            continue
        if ts <= enviado:
            continue
        try:
            m = json.load(open(ruta, encoding="utf-8"))
        except Exception:
            continue
        orig = str(m.get("de", "")).strip().lower()
        if "claude" not in orig:
            continue
        destino = str(m.get("para", "")).strip()
        if destino.lower() in (de or _quien(), "*", "todos", "todas", "todos los"):
            return True
    return False


def _guardar(d):
    try:
        json.dump(d, open(_ruta_espera(d.get("de")), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    except Exception:
        pass


def revisar(de=None, ahora_ms=None):
    """Registra que en este momento se miró el canal. Colabora con el ritmo de 5 min."""
    d = _leer_espera(de)
    if not d:
        return None
    d["ultima_revision_ms"] = _ms(ahora_ms or _ahora())
    _guardar(d)
    return d


def estado(de=None, ahora_ms=None):
    """Resumen de la espera: donde estamos y que toca ahora.

    Devuelve: en_espera, respondido, vencido, toca_revisar, segundos_esperados,
    segundos_restantes.
    """
    de = de or _quien()
    d = _leer_espera(de)
    if not d:
        return {"en_espera": False, "respondido": False, "vencido": False,
                "toca_revisar": False, "segundos_esperados": 0, "segundos_restantes": 0}
    ahora = _ms(ahora_ms or _ahora())
    enviado = float(d.get("enviado_ms", 0))
    transcurrido_s = (ahora - enviado) / 1000.0
    resto_s = max(0.0, TOTAL_SEG - transcurrido_s)
    ultima = float(d.get("ultima_revision_ms", 0))
    e = {
        "de": de,
        "respondido": _respondio_claude(de, enviado),
        "vencido": transcurrido_s >= TOTAL_SEG,
        "en_espera": transcurrido_s < TOTAL_SEG,
        "toca_revisar": (ahora - ultima) / 1000.0 >= RITMO_SEG,
        "segundos_esperados": int(transcurrido_s),
        "segundos_restantes": int(resto_s),
    }
    if e["respondido"]:
        e["en_espera"] = False
    return e


def aviso_vencido(de=None):
    """Marca el aviso de vencimiento (para no avisar dos veces) y lo devuelve."""
    d = _leer_espera(de)
    if not d or d.get("aviso_vencido"):
        return None
    d["aviso_vencido"] = True
    _guardar(d)
    return {"de": d.get("de"), "tipo": "espera_vencida",
            "texto": "ESPERA VENCIDA: se espero una hora por la respuesta de Claude al canal y no llego. "
                     "Avisar a Julio y al equipo por escrito."}


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    cmd = args[0]
    if cmd == "empezar":
        d = empezar()
        if not d:
            print("NO_ENCONTRADO: no se pudo marcar la espera.")
            return 1
        print("ATENTO: esperando respuesta de Claude desde la marca. Ritmo: cada 5 min. Tope: 1 hora.")
        return 0
    if cmd == "verificar":
        e = estado()
        if not e["en_espera"] and not e["respondido"] and not e["vencido"]:
            print("SIN_ESPERA: no hay mensaje a Claude en espera. Nada que vigilar.")
            return 0
        if e["respondido"]:
            print("RESPUESTA: llego respuesta de Claude por el canal. Recogerla y seguir.")
            return 0
        if e["vencido"]:
            aviso_vencido()
            print("VENCIDA: paso la hora sin respuesta. Hay que avisar a Julio y al equipo.")
            return 2
        if e["toca_revisar"]:
            revisar()
            print("REVISA: toca mirar el canal ya (cada 5 min). Restan %d s." % e["segundos_restantes"])
            return 0
        print("ESPERA: dentro de la ventana, faltan %d s. Volver a mirar en %d s." % (
            e["segundos_restantes"], max(1, RITMO_SEG - (e["segundos_esperados"] % RITMO_SEG))))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())