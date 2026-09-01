# -*- coding: utf-8 -*-
"""VIGIA — EL BALANCE DEL TRABAJO: CUANTO HACE EL EQUIPO Y CUANTO HACE JULIO (2026-09-02).

  "Nada cuenta cuanto hago yo y cuanto hace el equipo. Por eso te enteras cuando ya se gasto."

LO QUE PASO, MEDIDO: `cuerpo/medidor.py` mide el ACIERTO del paquete, no cuanto trabaja cada
quien. No existia ninguna cuenta de cuantas cosas hizo el equipo y cuantas hizo Julio a mano, ni
cuanto gasto se lleva la tanda. Se enteraba cuando ya estaba gastado.

QUE SE VIGILA AQUI:
  · que el balance cuente cuantos trabajos llevan veredicto del equipo (equipo)
  · que cuente cuantos se hicieron fuera del equipo / a mano (a_mano)
  · que cuente las rondas del equipo (TRABAJOS_DEL_EQUIPO.log)
  · que lea el gasto de la tanda (GASTO.json)
  · que lo diga en palabras simples, para que Julio lo vea sin preguntar
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "cuerpo"))
import pytest


@pytest.fixture(autouse=True)
def _cuadernos_aparte(tmp_path, monkeypatch):
    bal = tmp_path / "BALANCE.log"
    bal.write_text("equipo | a.py\n"
                   "equipo | b.py\n"
                   "a_mano | c.py\n"
                   "equipo | d.py\n"
                   "a_mano | e.md\n", encoding="utf-8")
    eq = tmp_path / "TRABAJOS_DEL_EQUIPO.log"
    eq.write_text("2026-09-02 10:00  ronda 1\n"
                  "2026-09-02 11:00  ronda 2\n"
                  "2026-09-02 12:00  ronda 3\n", encoding="utf-8")
    gas = tmp_path / "GASTO.json"
    gas.write_text(json.dumps({"contador": 7}), encoding="utf-8")
    monkeypatch.setenv("INGENIERO_BALANCE_BALANCE", str(bal))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(eq))
    monkeypatch.setenv("INGENIERO_BALANCE_GASTO", str(gas))
    yield


def _balance():
    from cuerpo import balance
    return balance


def test_cuenta_cuanto_hizo_el_equipo_y_cuanto_a_mano():
    """El corazon: el reparto equipo/a_mano sale de verdad de los registros, no de la memoria."""
    r = _balance().reparto()
    assert r["equipo"] == 3, "no conto los trabajos del equipo"
    assert r["a_mano"] == 2, "no conto los trabajos a mano"


def test_cuenta_las_rondas_del_equipo():
    r = _balance().reparto()
    assert r["rondas_equipo"] == 3, "no conto las rondas del equipo"


def test_lee_el_gasto_de_la_tanda():
    r = _balance().reparto()
    assert r["gasto_tanda"] == 7, "no leyo el gasto de la tanda"


def test_lo_dice_en_palabras_simples():
    """Para Julio, sin jerga: que se vea la division de un vistazo."""
    t = _balance().texto()
    assert "3" in t and "2" in t, "el balance no dice cuanto hizo cada quien"
    assert "equipo" in t.lower() and "a mano" in t.lower(), "no habla del reparto en simple"


def test_sin_cuadernos_no_se_inventa():
    """Si no hay registros, el balance no inventa numeros: dice que no hay datos."""
    import cuerpo.balance as b
    import os as _o
    import tempfile as _tf
    d = _tf.mkdtemp()
    vacio = os.path.join(d, "BALANCE_vacio.log")
    open(vacio, "w", encoding="utf-8").write("")
    _b = dict(_o.environ)
    _b["INGENIERO_BALANCE_BALANCE"] = vacio
    _b["INGENIERO_BALANCE_EQUIPO"] = os.path.join(d, "eq_vacio.log")
    _b["INGENIERO_BALANCE_GASTO"] = os.path.join(d, "gas_vacio.json")
    old = dict(_o.environ)
    try:
        _o.environ.clear(); _o.environ.update(_b)
        r = b.reparto()
        assert r["equipo"] == 0 and r["a_mano"] == 0, "invento numeros sin registros"
    finally:
        _o.environ.clear(); _o.environ.update(old)
