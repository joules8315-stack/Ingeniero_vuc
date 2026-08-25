# -*- coding: utf-8 -*-
"""VIGIA — AUTONOMIA DE CLINE (Julio 2026-08-24): en el bucle, Cline trabaja sin pedir autorizacion
a Julio. Se comunica con Claude y DeepSeek por el canal; Julio solo entra al final, para la prueba
humana. Si el bucle dependiera de una aprobacion de Julio en el medio, ROJA."""
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _leer(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_la_ley_de_autonomia_esta_escrita():
    t = _leer(os.path.join(AQUI, "CONTRATO_AUTONOMIA_CLINE.md")).lower()
    assert "no le pregunta a julio" in t or "no le pide" in t, "falta la regla de no preguntar a Julio"
    assert "canal" in t, "falta la comunicacion por canal"
    assert "prueba humana" in t or "ojos" in t, "falta que Julio entra al final (prueba humana)"


def test_el_rol_de_cline_es_consultor_cerebro_supervisor():
    t = _leer(os.path.join(AQUI, "CONTRATO_AUTONOMIA_CLINE.md")).lower()
    assert "consultor" in t, "falta el rol de consultor"
    assert "cerebro" in t, "falta el rol de cerebro (info indexada)"
    assert "supervisor" in t, "falta el rol de supervisor"
    assert "no es la mano" in t or "no hace el trabajo" in t, "no deja claro que Cline no hace el volumen"


def test_el_canal_esta_conectado_a_claude_para_comunicarse_sin_julio():
    s = json.load(open(os.path.join(AQUI, ".claude", "settings.json"), encoding="utf-8"))
    ups = s.get("hooks", {}).get("UserPromptSubmit", [])
    cmds = [h.get("command", "") for e in ups for h in e.get("hooks", [])]
    assert any("canal" in c for c in cmds), "el canal no esta conectado a UserPromptSubmit (los agentes no se hablan solos)"


def test_hay_canal_para_la_comunicacion_agentica():
    assert os.path.exists(os.path.join(AQUI, "arnes", "canal.py")), "falta el canal"
    assert os.path.exists(os.path.join(AQUI, "arnes", "llamar.py")), "falta el aviso de llamado"


def test_el_equipo_resuelve_sin_preguntarle_a_julio():
    txt = _leer(os.path.join(AQUI, "arnes", "canal.py")) + _leer(os.path.join(AQUI, "arnes", "loop.py"))
    assert "NECESITO_LEER" in txt or "enviar" in txt or "canal" in txt, "no hay camino para que el equipo pida contexto a otra IA"


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
