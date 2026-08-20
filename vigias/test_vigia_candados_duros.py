# -*- coding: utf-8 -*-
"""VIGIA 12 — LOS CANDADOS DUROS MUERDEN (Julio, 2026-08-20).

  "Como hacemos para que lo que no se garantiza ahora, sea una garantia?"

La respuesta fue: convertir cada promesa en una comprobacion que BLOQUEA. Aqui se comprueba
que esos candados muerden de verdad y —igual de importante— que **no dejan a Julio atrapado**.

Un candado que no bloquea da falsa seguridad. Uno que bloquea siempre es peor que el problema.
"""
import os, sys, json, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest


def _correr(script, payload, entorno=None):
    env = dict(os.environ)
    if entorno:
        env.update(entorno)
    p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", script)],
                       input=json.dumps(payload), capture_output=True, text=True,
                       env=env, timeout=300)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


# ─── candado de EDICION universal ───────────────────────────────────────────────
def test_edicion_bloquea_codigo_no_declarado():
    from cerebro import grafo
    d = grafo.proyectos().get("dmm")
    if not d or not os.path.isdir(d["ruta"]):
        pytest.skip("dmm no esta")
    f = os.path.join(d["ruta"], "cuerpo", "precios.py")
    if not os.path.exists(f):
        pytest.skip("no existe precios.py")
    code, _ = _correr("edit_gate_universal.py", {"tool_input": {"file_path": f}})
    assert code == 2, "dejo reescribir codigo que no esta en ningun paquete"


def test_edicion_deja_los_documentos_y_las_vigias():
    """Los contratos deben poder escribirse siempre, y las vigias son test-first."""
    from cerebro import grafo
    d = grafo.proyectos().get("dmm")
    if not d or not os.path.isdir(d["ruta"]):
        pytest.skip("dmm no esta")
    for rel in ("CONTRATO_PRECIOS.md", os.path.join("vigias", "test_vigia_plantilla.py")):
        f = os.path.join(d["ruta"], rel)
        if not os.path.exists(f):
            continue
        code, _ = _correr("edit_gate_universal.py", {"tool_input": {"file_path": f}})
        assert code == 0, f"estorba: bloqueo {rel}, que debe poder editarse siempre"


def test_el_interruptor_de_emergencia_apaga_los_candados():
    """Ningun candado puede dejar a Julio sin poder trabajar."""
    from cerebro import grafo
    d = grafo.proyectos().get("dmm")
    if not d or not os.path.isdir(d["ruta"]):
        pytest.skip("dmm no esta")
    f = os.path.join(d["ruta"], "cuerpo", "precios.py")
    if not os.path.exists(f):
        pytest.skip("no existe precios.py")
    code, _ = _correr("edit_gate_universal.py", {"tool_input": {"file_path": f}},
                      {"INGENIERO_OFF": "1"})
    assert code == 0, "el interruptor de emergencia no apaga el candado de edicion"


# ─── candado de CONTEXTO PERDIDO ────────────────────────────────────────────────
def test_contexto_perdido_bloquea_y_solo_lo_abre_al_volver():
    import candado_contexto as cc
    cc.quitar_marca()
    try:
        cc.poner_marca("prueba")
        assert cc.hay_marca()
        # cualquier lectura queda bloqueada
        code, txt = _correr("read_gate.py", {"tool_input": {
            "file_path": os.path.join(AQUI, "cerebro", "router.py")}})
        assert code == 2, "con el contexto perdido dejo seguir a ciegas"
        assert "NO SE SIGUE A CIEGAS" in txt
        # leer AL_VOLVER.md es lo unico que desbloquea
        open(cc.AL_VOLVER, "a", encoding="utf-8").close()
        code, _ = _correr("read_gate.py", {"tool_input": {"file_path": cc.AL_VOLVER}})
        assert code == 0, "no dejo leer el archivo que sirve para recuperar el hilo"
        assert not cc.hay_marca(), "leer AL_VOLVER.md no quito la marca"
    finally:
        cc.quitar_marca()


# ─── candado de CIERRE ──────────────────────────────────────────────────────────
def test_cierre_bloquea_si_hay_pregunta_sin_hacer():
    from cuerpo import estado
    antes = estado.leer().get("decision_pendiente", "")
    cont = os.path.join(AQUI, "memoria", ".cierres_bloqueados")
    try:
        if os.path.exists(cont):
            os.remove(cont)
        estado.apuntar(decision_pendiente="PRUEBA: una pregunta para Julio")
        code, txt = _correr("candado_cierre.py", {})
        assert code == 2, "dejo terminar dejando una pregunta de Julio sin hacer"
        assert "PREGUNTA" in txt.upper()
    finally:
        estado.apuntar(decision_pendiente=antes)
        if os.path.exists(cont):
            os.remove(cont)


def test_cierre_NO_deja_a_julio_atrapado():
    """Lo mas importante de un candado que bloquea: que tenga salida."""
    from cuerpo import estado
    antes = estado.leer().get("decision_pendiente", "")
    cont = os.path.join(AQUI, "memoria", ".cierres_bloqueados")
    try:
        if os.path.exists(cont):
            os.remove(cont)
        estado.apuntar(decision_pendiente="PRUEBA: bucle")
        salidas = [_correr("candado_cierre.py", {})[0] for _ in range(3)]
        assert 0 in salidas, f"bloqueo las 3 veces seguidas: deja a Julio atrapado ({salidas})"
        assert salidas.count(2) <= 2, "bloquea mas veces seguidas de las declaradas"
    finally:
        estado.apuntar(decision_pendiente=antes)
        if os.path.exists(cont):
            os.remove(cont)


def test_todos_los_candados_tienen_interruptor():
    for s in ("read_gate.py", "edit_gate_universal.py", "candado_cierre.py",
              "candado_contexto.py", "modo_ingeniero.py"):
        txt = open(os.path.join(AQUI, "arnes", s), encoding="utf-8").read()
        assert "INGENIERO_OFF" in txt, f"{s} no tiene interruptor de emergencia"
