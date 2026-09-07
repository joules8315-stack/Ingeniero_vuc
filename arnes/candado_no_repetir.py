#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_no_repetir.py — NO SE LE REPITE A JULIO LO QUE YA LEYO.

Julio, 2026-09-06: "Esto fue lo que acabamos de hacer, ¿por qué repites todo dos veces?"

Este candado se engancha al terminar la respuesta (igual que candado_protocolo.py).
Guarda en memoria/.ya_le_dije.json la huella md5 de cada frase larga (más de 60 letras)
que ya se le dijo a Julio. Al terminar una respuesta, si más de la mitad de sus frases
largas ya están en ese cuaderno, frena con salida 2 y avisa que eso ya se le contó.

No frena más de dos veces seguidas, para no bloquear el trabajo.
Se apaga con la variable de entorno INGENIERO_OFF=1.
Deja rastro en memoria/.repeticiones.log.
"""
import json, os, sys, hashlib, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
CUADERNO = os.path.join(AQUI, "memoria", ".ya_le_dije.json")
LOG = os.path.join(AQUI, "memoria", ".repeticiones.log")
CONTADOR = os.path.join(AQUI, "memoria", ".no_repetir_bloqueos")
TOPE_BLOQUEOS = 2
LARGA = 60  # letras mínimas para considerar una frase larga


def _contador():
    """El contador de verdad, o uno de prueba (mismo patrón que candado_protocolo)."""
    return os.environ.get("INGENIERO_CONTADOR_TEST") or CONTADOR


def _cuaderno_ruta():
    """La ruta del cuaderno de verdad, o una de prueba (mismo patrón que _contador)."""
    return os.environ.get("INGENIERO_CUADERNO_TEST") or CUADERNO


def _log_ruta():
    """La ruta del rastro de verdad, o una de prueba (mismo patrón que _contador)."""
    return os.environ.get("INGENIERO_LOG_TEST") or LOG


def _leer_cuaderno():
    """Devuelve el conjunto de huellas guardadas."""
    try:
        with open(_cuaderno_ruta(), "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def _escribir_cuaderno(huellas):
    """Guarda el conjunto de huellas en el cuaderno."""
    with open(_cuaderno_ruta(), "w", encoding="utf-8") as f:
        json.dump(sorted(huellas), f, ensure_ascii=False, indent=2)


def _frases_largas(texto):
    """Divide el texto en frases (por punto, signo de cierre, etc.) y devuelve las que tengan más de LARGA letras."""
    import re
    frases = re.split(r'(?<=[.!?])\s+', texto or "")
    return [f.strip() for f in frases if len(f.strip()) > LARGA]


def _huella(frase):
    """Huella md5 de una frase (solo la huella, nunca el texto)."""
    return hashlib.md5(frase.encode("utf-8")).hexdigest()


def _bloqueos_seguidos():
    """Cuántos bloqueos seguidos lleva este candado."""
    try:
        with open(_contador(), "r") as f:
            return int(f.read().strip() or "0")
    except Exception:
        return 0


def _apuntar_bloqueo(valor):
    """Guarda el número de bloqueos seguidos."""
    with open(_contador(), "w") as f:
        f.write(str(valor))


def _registrar(mensaje):
    """Deja rastro en memoria/.repeticiones.log."""
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S") + " " + mensaje + "\n")
    except Exception:
        pass


def salida():
    """Punto de enganche al terminar la respuesta (Stop).

    Lee la respuesta desde stdin (JSON con last_assistant_message), calcula las frases
    largas, y si más de la mitad ya están en el cuaderno, frena con salida 2.
    """
    if os.environ.get("INGENIERO_OFF") == "1":
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ultimo = str(data.get("last_assistant_message") or "")
    if not ultimo:
        return 0
    frases = _frases_largas(ultimo)
    if not frases:
        return 0
    cuaderno = _leer_cuaderno()
    repetidas = [f for f in frases if _huella(f) in cuaderno]
    if len(repetidas) <= len(frases) / 2:
        # No repite: guarda las frases nuevas y resetea el contador
        nuevas = {_huella(f) for f in frases if _huella(f) not in cuaderno}
        if nuevas:
            _escribir_cuaderno(cuaderno | nuevas)
        _apuntar_bloqueo(0)
        return 0
    # Repite: comprobar si ya bloqueó demasiadas veces seguidas
    veces = _bloqueos_seguidos()
    if veces >= TOPE_BLOQUEOS:
        _apuntar_bloqueo(0)
        _registrar("AVISO: se deja pasar para no atascar a Julio, pero repite lo ya contado.")
        sys.stderr.write("AVISO: la respuesta repite lo que ya se le conto a Julio. Se deja pasar para no\n"
                         "  atascar a Julio, pero incumple CONTRATO_NO_REPETIR.md.\n")
        return 0
    _apuntar_bloqueo(veces + 1)
    _registrar("BLOQUEO: respuesta repetida, se frena.")
    sys.stderr.write(
        "NO SE PUEDE TERMINAR: la respuesta repite lo que ya se le conto a Julio.\n"
        "  Julio ya leyo esto y se quejo tres veces el mismo dia. Contesta solo lo nuevo.\n")
    sys.stderr.write("  Las frases que ya se le contaron son:\n")
    for f in repetidas[:3]:
        sys.stderr.write("    - " + f[:100] + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(salida())
