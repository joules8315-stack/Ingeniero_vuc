# -*- coding: utf-8 -*-
"""vigias/test_vigia_repartidor_por_capacidad.py — REPARTIDOR POR CAPACIDAD Y EFICIENCIA.

Ley de Julio, 2026-08-21: "las tareas se reparten dependiendo de la capacidad de cada uno...
es estupido darle una tarea a una IA que sabes que no va a soportar. Legislar y en ese orden
asignar."

Lo que vigila:
  1. NO se le asigna trabajo a un cerebro que no aguanta el tamano (`rankear` lo salta).
  2. El orden va del MAS eficiente al MENOS (fiabilidad x rapidez).
  3. La capacidad se lee de lo MEDIDO (CAPACIDADES.json / mayor_ok), no de suposiciones.
"""
import sys, os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cuerpo import cuotas  # noqa: E402


def _gasto():
    return {
        "groq":     {"llamadas": 10, "fallos": 0, "record_seg": 1},
        "groq20b":  {"llamadas": 10, "fallos": 0, "record_seg": 0.5},
        "local":    {"llamadas": 10, "fallos": 0, "record_seg": 1},
        "deepseek": {"llamadas": 0,  "fallos": 0},
    }


def test_no_le_da_el_pesado_al_que_no_aguanta(monkeypatch):
    """Un encargo de 30.000 letras NO cae en el local (su limite MEDIDO es 26.000): se salta."""
    monkeypatch.setattr(cuotas, "_leer", lambda: {"gasto": _gasto()})
    monkeypatch.setattr(cuotas, "_medidas", lambda: {})
    r = cuotas.rankear(["groq", "local", "deepseek"], 30000)
    assert "local" not in r          # no aguanta 30.000: se salta, no se le pregunta
    assert "deepseek" in r
    assert "groq" in r


def test_ordena_del_mas_eficiente_al_menos(monkeypatch):
    """groq20b (record 0.5s, sin fallos) debe ir antes que groq (1s) y que deepseek (sin datos)."""
    monkeypatch.setattr(cuotas, "_leer", lambda: {"gasto": _gasto()})
    monkeypatch.setattr(cuotas, "_medidas", lambda: {})
    r = cuotas.rankear(["groq", "groq20b", "deepseek"], 2000)
    assert r[0] == "groq20b"         # el mas rapido y confiable primero
    assert r[-1] == "deepseek"       # sin datos todavia: el ultimo (se prueba si los otros fallan)


def test_capacidad_medida_manda(monkeypatch):
    """La capacidad MEDIDA (CAPACIDADES.json) se usa para decidir, no solo la documentada."""
    monkeypatch.setattr(cuotas, "_leer", lambda: {"gasto": _gasto()})
    monkeypatch.setattr(cuotas, "_medidas", lambda: {"groq": 400000})
    assert "groq" in cuotas.rankear(["groq"], 100000)


def test_capacidad_medida_puede_subir_el_limite_del_local(monkeypatch):
    """El local mide 26.000 hoy; si un dia se mide 40.000, ya entra en un encargo de 30.000."""
    monkeypatch.setattr(cuotas, "_leer", lambda: {"gasto": _gasto()})
    monkeypatch.setattr(cuotas, "_medidas", lambda: {"local": 40000})
    assert "local" in cuotas.rankear(["local"], 30000)
