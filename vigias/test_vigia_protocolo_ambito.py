# -*- coding: utf-8 -*-
"""VIGIA — F1 (Julio 2026-08-24): el protocolo aplica a TODO tipo de trabajo (Ingeniero, MVP, DMM),
no solo al MVP. Si vuelve a quedar "para el MVP", ROJA."""
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_el_protocolo_aplica_a_todo_tipo_de_trabajo():
    t = open(os.path.join(AQUI, "PROTOCOLO_UNICO.md"), encoding="utf-8").read().lower()
    assert "aplica siempre" in t or "todo tipo de trabajo" in t, "el protocolo no declara su ambito"
    assert "no es \"para el mvp\"" in t or "no es para el mvp" in t or "no es 'para el mvp'" in t, \
        "el protocolo no deja claro que no es solo del MVP"


def test_menciona_los_proyectos_a_los_que_aplica():
    t = open(os.path.join(AQUI, "PROTOCOLO_UNICO.md"), encoding="utf-8").read().lower()
    for proy in ("ingeniero", "mvp", "dmm"):
        assert proy in t, "el protocolo no menciona a %s" % proy


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
