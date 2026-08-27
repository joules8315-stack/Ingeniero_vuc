# -*- coding: utf-8 -*-
"""Vigía — EL CANDADO DE ESCRITURA ESTÁ CONECTADO Y NO SE APAGA EN SILENCIO (Julio, 2026-08-24).

Julio: "que claude utilice el equipo... y que no lo puedan desactivar, sino que me pidan autorizacion
previa." Esta vigía comprueba que:
  1. El candado de escritura está CONECTADO a las ediciones (settings.json) — si lo desconectan, ROJA.
  2. Prender INGENIERO_OFF solo NO apaga los candados: hace falta la autorización escrita de Julio.
"""
import json
import os
import sys
import subprocess

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _settings():
    """La config combinada (usuario + proyecto) reconstruida para los que la consumen."""
    import _config
    return {"hooks": {t: [{"matcher": m, "hooks": [{"command": c}]} for m, c in _config.comandos(t)]
                      for t in ("PreToolUse", "Stop", "UserPromptSubmit", "SessionStart")}}


def _comandos_escritura():
    """Los comandos de hook de escritura que deben correr los candados (en cualquier capa)."""
    import _config
    cmds = [c for m, c in _config.comandos("PreToolUse")
            if any(t in m.lower() for t in ("write", "edit"))]
    return cmds


def test_el_candado_de_escritura_esta_conectado_a_la_edicion():
    cmds = _comandos_escritura()
    assert cmds, "no hay hook de escritura/edicion en settings (usuario o proyecto)"
    assert any("candado_equipo" in c for c in cmds), "falta el candado de equipo en la escritura"
    assert any("edit_gate_universal" in c for c in cmds), "falta el candado de edicion en la escritura"


def test_el_arnes_NO_esta_duplicado():
    """Julio, 2026-08-27: se pedian autorizacion dos veces para lo mismo porque el arnes vivia en
    DOS settings a la vez (usuario y proyecto) y ademas habia 3 edit_gate distintos en el usuario.
    La fuente canonica es el USUARIO; el proyecto NO debe repetir el arnes. Esta vigia muerde si la
    MISMA funcion corre en el MISMO (evento, matcher) dos veces (en cualquier capa). Un candado en
    varios matchers distintos (ej: candado_terminal en Bash, Grep, Glob) NO es duplicacion: son
    herramientas distintas.
    """
    import _config
    capas = _config.leer_capas()
    assert len(capas) >= 1, "no hay ningun settings"
    arnes = ["read_gate", "candado_terminal", "candado_equipo", "edit_gate_universal",
             "candado_memoria", "candado_protocolo", "candado_diagnostico", "candado_preguntar",
             "guard_pasado", "candado_cierre", "candado_contexto", "modo_ingeniero"]
    donde = {}
    for capa in capas:
        for t in ("PreToolUse", "Stop", "UserPromptSubmit", "SessionStart",
                  "PreCompact", "PostCompact"):
            for e in capa.get("hooks", {}).get(t, []):
                m = e.get("matcher", "")
                for h in e.get("hooks", []):
                    c = h.get("command", "")
                    for nombre in arnes:
                        if nombre + ".py" in c:
                            clave = (t, m, nombre)
                            donde.setdefault(clave, 0)
                            donde[clave] += 1
    duplicados = {k: v for k, v in donde.items() if v > 1}
    assert not duplicados, (
        "el arnes pide la misma funcion dos veces en el mismo lugar (se pide autorizacion dos "
        "veces): " + ", ".join(f"{k}->{v}" for k, v in duplicados.items())
        + ". La misma funcion en el mismo evento/matcher debe correr UNA sola vez.")


def test_la_terminal_esta_conectada_al_candado():
    """LA RENDIJA (Julio, 2026-08-27): la terminal no estaba conectada a NINGUN candado.

    Escribir codigo por la terminal (echo, heredoc, Set-Content) se saltaba el candado de equipo,
    que solo se disparaba en la herramienta de editar. Y leer por terminal tampoco pasaba por el
    candado del paquete minimo. Esta vigia comprueba que candado_terminal SIGA conectado a la
    terminal y a las busquedas (en usuario o proyecto): si se desconecta, ROJA.
    """
    import _config
    pre = _config.comandos("PreToolUse")
    matchers = " ".join(m.lower() for m, _ in pre)
    # la terminal y las busquedas tienen que pasar por candado_terminal
    assert any("bash" in m.lower() for m, _ in pre), \
        "la terminal (Bash) no esta conectada a ningun candado"
    assert any("candado_terminal" in c for _, c in pre), \
        "candado_terminal no esta conectado a ninguna herramienta: la terminal es una rendija"
    assert any("grep" in m.lower() or "glob" in m.lower() for m, _ in pre), \
        "las busquedas (grep/glob) no pasan por candado_terminal"


def test_ingeniero_off_solo_no_apaga_los_candados(tmp_path):
    """Prender INGENIERO_OFF sin la autorizacion escrita de Julio NO apaga (Julio, 2026-08-24)."""
    from cerebro import grafo
    d = grafo.proyectos().get("dmm")
    if not d or not os.path.isdir(d["ruta"]):
        import pytest
        pytest.skip("dmm no esta")
    f = os.path.join(d["ruta"], "cuerpo", "precios.py")
    if not os.path.exists(f):
        import pytest
        pytest.skip("no existe precios.py")
    import autorizacion as aut
    marca = str(tmp_path / "aut_off")
    env = dict(os.environ)
    env["INGENIERO_AUTORIZACION_TEST"] = marca
    env["INGENIERO_OFF"] = "1"
    os.environ["INGENIERO_AUTORIZACION_TEST"] = marca   # para que autorizar() escriba en el temporal
    secreto = aut.sembrar_secreto_test(tmp_path)
    try:
        p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "edit_gate_universal.py")],
                           input=json.dumps({"tool_input": {"file_path": f}}),
                           capture_output=True, text=True, env=env, timeout=120)
        assert p.returncode == 2, "INGENIERO_OFF apago los candados sin autorizacion de Julio"
        # con autorizacion si apaga
        aut.autorizar("prueba", secreto)
        p2 = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "edit_gate_universal.py")],
                            input=json.dumps({"tool_input": {"file_path": f}}),
                            capture_output=True, text=True, env=env, timeout=120)
        assert p2.returncode == 0, "la autorizacion de Julio no abrio el candado"
    finally:
        os.environ.pop("INGENIERO_AUTORIZACION_TEST", None)
        os.environ.pop("INGENIERO_LLAVE_JULIO_TEST", None)


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
