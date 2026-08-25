# -*- coding: utf-8 -*-
"""VIGIA — F4 (Julio 2026-08-24): la comunicacion entre agentes (Claude, Cline, DeepSeek) es fluida
y MANDATORIA. El canal entrega a cada agente los mensajes de los otros; el candado de comunicacion
bloquea si hay pendientes sin responder. Comprueba que candado_comunicacion esta conectado y muerde."""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def test_candado_comunicacion_esta_conectado_a_stop():
    s = json.load(open(os.path.join(AQUI, ".claude", "settings.json"), encoding="utf-8"))
    stop = s.get("hooks", {}).get("Stop", [])
    cmds = [h.get("command", "") for e in stop for h in e.get("hooks", [])]
    assert any("candado_comunicacion" in c for c in cmds), "candado_comunicacion no esta en el hook Stop"


def test_el_canal_entrega_a_claude_el_mensaje_de_cline(tmp_path):
    """Cline deja mensaje a claude -> el hook del canal se lo inyecta a claude en su proxima instruccion."""
    b = str(tmp_path / "bandeja")
    old = (os.environ.get("INGENIERO_CANAL_TEST"), os.environ.get("INGENIERO_QUIEN"))
    os.environ["INGENIERO_CANAL_TEST"] = b
    os.environ["INGENIERO_QUIEN"] = "cline"
    try:
        import canal
        canal.enviar("claude", "PENDIENTE: verifica el candado de comunicacion", de="cline")
    finally:
        os.environ.pop("INGENIERO_CANAL_TEST", None); os.environ.pop("INGENIERO_QUIEN", None)
    # ahora claude despierta: el hook del canal se lo muestra
    env2 = dict(os.environ)
    env2["INGENIERO_CANAL_TEST"] = b
    env2["INGENIERO_QUIEN"] = "claude"
    r = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "canal.py")],
                       capture_output=True, text=True, env=env2)
    salida = (r.stdout or "") + (r.stderr or "")
    assert "CANAL INTERNO" in salida, "el canal no entrego el mensaje a claude"
    assert "verifica el candado de comunicacion" in salida, "claude no recibio el texto del mensaje"


def test_candado_comunicacion_bloquea_con_pendientes(tmp_path, monkeypatch):
    import candado_comunicacion as cc
    b = str(tmp_path / "bandeja")
    os.makedirs(b, exist_ok=True)
    monkeypatch.setattr(cc, "BANDEJA", b)
    # un mensaje dirigido a 'desconocido' (quien cuando no hay INGENIERO_QUIEN) sin responder
    json.dump({"de": "cline", "para": "desconocido", "texto": "responde esto", "leido": False,
               "respondido": False},
              open(os.path.join(b, "m.json"), "w", encoding="utf-8"))
    monkeypatch.delenv("INGENIERO_OFF", raising=False)
    rc = cc.main()
    assert rc == 2, "candado_comunicacion no bloqueo con mensajes pendientes"


def test_candado_comunicacion_no_bloquea_sin_pendientes(tmp_path, monkeypatch):
    import candado_comunicacion as cc
    b = str(tmp_path / "bandeja2")
    os.makedirs(b, exist_ok=True)
    monkeypatch.setattr(cc, "BANDEJA", b)
    monkeypatch.delenv("INGENIERO_OFF", raising=False)
    monkeypatch.setenv("INGENIERO_COMUNICACION_CONTADOR", str(tmp_path / "cont"))
    assert cc.main() == 0, "sin pendientes no debe bloquear"


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
