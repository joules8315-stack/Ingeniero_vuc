# -*- coding: utf-8 -*-
"""VIGIA — PRUEBA REAL ANTES DE PEDIRLE A JULIO (bloque B2, legislacion 2026-08-24).

Julio, 2026-08-24: "siempre haz pruebas manuales internas reales con playwright, antes de decirme
que me pida que yo realice pruebas fisicas reales, primero debe asegurarse que se cumple el
objetivo que trace... verifique si en realidad se logro el resultado, o fue una autovalidacion."

Comprueba que el candado `arnes/candado_prueba_real.py` MUERDE: sin evidencia fresca, verde y con
equipo, NO se le puede pedir a Julio que pruebe. Y que una autovalidacion no abre la puerta.
"""
import os
import sys
import json
import time
import subprocess

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest
import candado_prueba_real as pr


def _correr_pedir(tmp_path, env_extra=None):
    env = dict(os.environ)
    env["INGENIERO_PRUEBAS_TEST"] = str(tmp_path)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(
        [sys.executable, os.path.join(AQUI, "arnes", "candado_prueba_real.py"),
         "pedir", "dmm", "el objetivo se cumple"],
        capture_output=True, text=True, env=env, timeout=120)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


def test_sin_evidencia_bloquea_pedir(tmp_path, monkeypatch):
    """No se le pide a Julio que pruebe si NO hay prueba real hecha."""
    monkeypatch.setenv("INGENIERO_PRUEBAS_TEST", str(tmp_path))
    code, txt = _correr_pedir(tmp_path)
    assert code == 2, "dejo pedirle a Julio sin ninguna prueba real"
    assert "NO SE LE PIDE A JULIO" in txt


def test_con_evidencia_fresca_verde_y_con_equipo_deja_pedir(tmp_path, monkeypatch):
    """Con prueba real, con equipo y en verde, recien ahi se puede pedir."""
    monkeypatch.setenv("INGENIERO_PRUEBAS_TEST", str(tmp_path))
    pr.marcar("dmm", "el objetivo se cumple", con_equipo=True, resultado="OK")
    assert pr.hay_prueba_real("dmm", "el objetivo se cumple") is not None
    code, txt = _correr_pedir(tmp_path)
    assert code == 0, "bloqueo aunque hay prueba real fresca, verde y con equipo"


def test_autovalidacion_no_abre_la_puerta(tmp_path, monkeypatch):
    """Una prueba hecha a solas (sin veredicto del equipo) NO es prueba (Julio, 2026-08-24)."""
    monkeypatch.setenv("INGENIERO_PRUEBAS_TEST", str(tmp_path))
    pr.marcar("dmm", "el objetivo se cumple", con_equipo=False, resultado="OK")
    assert pr.hay_prueba_real("dmm", "el objetivo se cumple") is None, \
        "la autovalidacion no debe valer como prueba"
    code, _ = _correr_pedir(tmp_path)
    assert code == 2, "dejo pedir con una prueba que fue autovalidacion"


def test_prueba_en_rojo_no_abre_la_puerta(tmp_path, monkeypatch):
    """Si la prueba real fallo (no OK), tampoco se le pide a Julio."""
    monkeypatch.setenv("INGENIERO_PRUEBAS_TEST", str(tmp_path))
    pr.marcar("dmm", "el objetivo se cumple", con_equipo=True, resultado="ROJO")
    assert pr.hay_prueba_real("dmm", "el objetivo se cumple") is None
    code, _ = _correr_pedir(tmp_path)
    assert code == 2


def test_prueba_vieja_ya_no_vale(tmp_path, monkeypatch):
    """La evidencia caduca: una prueba de hace un mes no sirve para pedir hoy."""
    monkeypatch.setenv("INGENIERO_PRUEBAS_TEST", str(tmp_path))
    d = pr.marcar("dmm", "el objetivo se cumple", con_equipo=True, resultado="OK")
    d["cuando"] = time.time() - 30 * 24 * 3600
    json.dump(d, open(os.path.join(str(tmp_path), "dmm__el_objetivo_se_cumple.json"),
                      "w", encoding="utf-8"), ensure_ascii=False)
    assert pr.hay_prueba_real("dmm", "el objetivo se cumple") is None
    code, _ = _correr_pedir(tmp_path)
    assert code == 2


def test_la_marca_guarda_si_fue_con_equipo():
    """La evidencia debe dejar escrito si fue con el equipo o autovalidacion."""
    r = pr.marcar("dmm", "el objetivo se cumple", con_equipo=True)
    assert r["con_equipo"] is True
    assert "con_equipo" in r
