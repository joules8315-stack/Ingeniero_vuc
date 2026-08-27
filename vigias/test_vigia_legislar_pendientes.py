# -*- coding: utf-8 -*-
"""VIGIA — F5 / punto a de Julio: TODA instruccion se legisla, con candado (2026-08-24).

"todo lo que yo escriba debe ser legislado, todo, absolutamente todo... la orden es clara, siempre."

Comprueba que el candado de legislacion muerde de verdad: apuntar una instruccion la deja pendiente
y bloquea; legislarla (o marcarla) la libera; y nunca deja a Julio atrapado (antibucle + salida).
"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import candado_legislar as cl  # noqa: E402


def _ledger_aparte(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_LEGISLAR_TEST", str(tmp_path / "leg.json"))


def test_apuntar_deja_pendiente(tmp_path, monkeypatch):
    _ledger_aparte(tmp_path, monkeypatch)
    cl.apuntar("Legisla que el equipo sea cline, deepseek y claude")
    assert len(cl.pendientes()) == 1, "apuntar no dejo la instruccion pendiente"


def test_legislar_la_libera(tmp_path, monkeypatch):
    _ledger_aparte(tmp_path, monkeypatch)
    t = "Toda instruccion se legisla con candado"
    cl.apuntar(t)
    assert len(cl.pendientes()) == 1
    ok = cl.marcar(t, "legislado", "contrato + tabla + matriz + vigia")
    assert ok and not cl.pendientes(), "legislar no libero la instruccion"


def test_ya_existe_la_libera_con_motivo(tmp_path, monkeypatch):
    _ledger_aparte(tmp_path, monkeypatch)
    t = "Reutilizar lo que ya existe"
    cl.apuntar(t)
    assert cl.marcar(t, "ya_existe", "ya esta en CONTRATO_LEGISLACION_TOTAL L5")
    assert not cl.pendientes()


def test_hook_bloquea_con_pendientes_y_abre_sin(tmp_path, monkeypatch):
    _ledger_aparte(tmp_path, monkeypatch)
    # sin pendientes -> no bloquea
    env = dict(os.environ)
    env["INGENIERO_LEGISLAR_TEST"] = str(tmp_path / "leg.json")
    r = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_legislar.py")],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, "sin pendientes no debe bloquear"
    # con pendientes -> bloquea
    cl.apuntar("Algo sin legislar todavia")
    r2 = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_legislar.py")],
                        capture_output=True, text=True, env=env)
    assert r2.returncode == 2, "con pendientes debe bloquear"
    assert "SIN LEGISLAR" in r2.stderr


def test_esta_conectado_al_candado_de_cierre():
    txt = open(os.path.join(AQUI, "arnes", "candado_cierre.py"), encoding="utf-8").read()
    assert "candado_legislar" in txt, "el candado de legislar no esta conectado al cierre"


def test_no_deja_a_julio_atrapado(tmp_path, monkeypatch):
    """El candado tiene salida: SOLO Julio la abre con su autorizacion (autorizar-off)."""
    _ledger_aparte(tmp_path, monkeypatch)
    cl.apuntar("x")
    import autorizacion as aut
    marca = str(tmp_path / "aut_off")
    os.environ["INGENIERO_AUTORIZACION_TEST"] = marca
    secreto = aut.sembrar_secreto_test(tmp_path)
    try:
        aut.autorizar("prueba: salida de emergencia", secreto)
        env = dict(os.environ)
        env["INGENIERO_LEGISLAR_TEST"] = str(tmp_path / "leg.json")
        env["INGENIERO_AUTORIZACION_TEST"] = marca
        r = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_legislar.py")],
                           capture_output=True, text=True, env=env)
        assert r.returncode == 0, "la autorizacion de Julio no abrio el candado (encerrado)"
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
