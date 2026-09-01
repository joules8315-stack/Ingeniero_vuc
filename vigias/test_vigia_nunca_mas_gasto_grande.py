# -*- coding: utf-8 -*-
"""VIGIA — EL CANDADO DEL GASTO QUE NUNCA SE PUSO (Julio, 2026-09-02).

  "legisla fuerte, nunca mas, nunca mas vuelves a hacer gasto grande"
  "el cierre del gasto que iba a impedirme esto nunca se puso. Lo deje escrito y sin aplicar."

LO QUE PASO, MEDIDO: el contrato CONTRATO_NUNCA_MAS_GASTO_GRANDE.md pedia un candado
`arnes/candado_gasto.py` y su vigia. Ni uno ni otro existian. La ley estaba escrita y sin aplicar,
exactamente lo que Julio midio. Este candado no recuerda el gasto: lo cuenta y lo FRENA.

QUE SE VIGILA AQUI (de verdad, no de palabra):
  · que avise a mitad del tope de la tanda
  · que avise al 80% del tope
  · que FRENE al llegar al tope (no es un recordatorio: frena)
  · que tres rechazos seguidos paren y avisen (no se insiste una cuarta vez)
  · que deje rastro en el libro de gasto para que Julio lo mire sin preguntar
"""
import importlib
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest


@pytest.fixture(autouse=True)
def _cuaderno_aparte(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_GASTO_TEST", str(tmp_path / "GASTO.json"))
    yield


def _gasto(tmp_path, monkeypatch, tope):
    import candado_gasto as g
    monkeypatch.setenv("INGENIERO_TOPE_ACCIONES", str(tope))
    return g


# ─── AVISA ANTES DE LLEGAR ────────────────────────────────────────────────────
def test_avisa_a_la_mitad_del_tope(tmp_path, monkeypatch):
    """A mitad del tope se le dice a Julio cuanto se lleva, no al final (ley 2)."""
    g = _gasto(tmp_path, monkeypatch, tope=10)
    est, msg = None, ""
    for _ in range(5):
        est, msg = g.contar(1)          # la sexta accion cruza la mitad
    est, msg = g.contar(1)
    assert est == "aviso_mitad", "no aviso a mitad del tope"


def test_avisa_al_80_del_tope(tmp_path, monkeypatch):
    g = _gasto(tmp_path, monkeypatch, tope=10)
    est = ""
    for _ in range(8):
        est, _ = g.contar(1)            # la octava cruza el 80%
    assert est == "aviso_80", "no aviso cuando ya casi se llego al tope"


# ─── FRENA DE VERDAD ──────────────────────────────────────────────────────────
def test_frena_al_llegar_al_tope(tmp_path, monkeypatch):
    """El nucleo: llegar al tope BLOQUEA, no es un recordatorio (ley 1)."""
    g = _gasto(tmp_path, monkeypatch, tope=5)
    est = ""
    for _ in range(5):
        est, _ = g.contar(1)
    assert est == "freno", "no freno al llegar al tope: gastar es a escondidas"


def test_main_devuelve_2_cuando_frena(tmp_path, monkeypatch):
    """El hook: al llegar al tope la salida tiene que ser 2 (frena de verdad)."""
    g = _gasto(tmp_path, monkeypatch, tope=2)
    import io
    g.contar(1)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"acciones": 1})))
    assert g.main() == 2, "el hook no freno al llegar al tope"


# ─── TRES RECHAZOS SEGUIDOS Y SE PARA ─────────────────────────────────────────
def test_tres_rechazos_seguidos_paran(tmp_path, monkeypatch):
    """Tres rechazos seguidos no son mala suerte: el encargo esta mal. Se para (ley 3)."""
    g = _gasto(tmp_path, monkeypatch, tope=100)
    assert g.rechazo(True) is False
    assert g.rechazo(True) is False
    assert g.rechazo(True) is True, "tres rechazos seguidos deberian parar"


def test_un_aprobado_entre_medio_borra_la_cuenta_de_rechazos(tmp_path, monkeypatch):
    """Si algo sale bien entre rechazos, no es una racha de rechazos: se reanuda."""
    g = _gasto(tmp_path, monkeypatch, tope=100)
    g.rechazo(True)
    g.rechazo(True)
    g.rechazo(False)                    # un aprobado corta la racha
    assert g.rechazo(True) is False, "el aprobado no corto la racha de rechazos"


# ─── DEJA RASTRO ──────────────────────────────────────────────────────────────
def test_deja_rastro_para_julio(tmp_path, monkeypatch):
    """Julio lo mira, no tiene que preguntar (ley 3 de NUNCA_A_SOLAS)."""
    g = _gasto(tmp_path, monkeypatch, tope=10)
    g.contar(1)
    ruta = os.environ["INGENIERO_GASTO_TEST"]
    assert os.path.exists(ruta), "no dejo el cuaderno de gasto"
    datos = json.load(open(ruta, encoding="utf-8"))
    assert datos.get("contador", 0) >= 1, "no conto la accion"
