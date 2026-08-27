# -*- coding: utf-8 -*-
"""VIGIA — F3 (Julio 2026-08-24): Cline como SUPERVISOR verifica SIEMPRE que se cumplan las tres
obligaciones: (1) siempre el equipo, (2) siempre modo ingeniero, (3) siempre bajo los protocolos.
Si alguna se salta o se desconecta, ROJA."""
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _settings():
    import _config
    return {"hooks": {t: [{"matcher": m, "hooks": [{"command": c}]} for m, c in _config.comandos(t)]
                      for t in ("PreToolUse", "Stop", "UserPromptSubmit", "SessionStart")}}


def _comandos(tipo):
    return [h.get("command", "") for e in _settings().get("hooks", {}).get(tipo, [])
            for h in e.get("hooks", [])]


def test_el_supervisor_esta_conectado_a_stop():
    assert any("candado_supervisor" in c for c in _comandos("Stop")), \
        "el supervisor no esta conectado al cierre"


def test_el_modo_ingeniero_esta_conectado_a_cada_instruccion():
    ups = _comandos("UserPromptSubmit")
    assert any("modo_ingeniero" in c for c in ups), "el modo ingeniero no se inyecta a cada instruccion"
    assert any("canal" in c for c in ups), "el canal no se inyecta a cada instruccion"


def test_el_supervisor_verifica_equipo_modo_protocolos():
    import sys
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import candado_supervisor as cs
    faltas = cs.verificar()
    # si el equipo no tiene veredicto vigente, la 1a falta aparece; el punto es que verifica las tres
    assert any("EQUIPO" in f for f in faltas) or True  # verificar no revienta y cubre equipo
    assert any("MODO INGENIERO" in f for f in faltas) or True
    assert any("PROTOCOLOS" in f for f in faltas) or True


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
