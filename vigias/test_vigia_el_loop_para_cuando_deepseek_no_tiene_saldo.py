"""Vigia: el loop no debe pararse por dolares, pero SI debe avisar cuando DeepSeek
se queda sin saldo (HTTP 402 Insufficient Balance).

Vigila dos piezas de cuerpo/capataz.py:
  - deepseek_sin_saldo(): True solo si DeepSeek esta dormido por falta de SALDO.
  - bucle(): no debe devolver TOPE por gasto, y debe devolver SIN SALDO cuando
    DeepSeek esta dormido por saldo.

Aisla la memoria de cuotas en una carpeta temporal cambiando cuotas.RUTA con
monkeypatch, para no tocar la memoria de verdad.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import cuotas  # noqa: E402
from cuerpo import capataz  # noqa: E402


# ---------------------------------------------------------------------------
# Aislamiento de la memoria de cuotas
# ---------------------------------------------------------------------------

def _aislar_cuotas(tmp_path, monkeypatch):
    """Apunta cuotas.RUTA a un archivo temporal para no tocar la memoria real."""
    ruta = tmp_path / 'CUOTAS.json'
    monkeypatch.setattr(cuotas, 'RUTA', str(ruta), raising=False)
    return ruta


# ---------------------------------------------------------------------------
# (1) Sin nadie dormido, deepseek_sin_saldo() es False
# ---------------------------------------------------------------------------

def test_sin_nadie_dormido_no_hay_saldo_agotado(tmp_path, monkeypatch):
    _aislar_cuotas(tmp_path, monkeypatch)
    assert capataz.deepseek_sin_saldo() is False


# ---------------------------------------------------------------------------
# (2) DeepSeek dormido por 'HTTP 402 Insufficient Balance' -> True
# ---------------------------------------------------------------------------

def test_deepseek_dormido_por_saldo_es_true(tmp_path, monkeypatch):
    _aislar_cuotas(tmp_path, monkeypatch)
    cuotas.dormir('deepseek', 'HTTP 402 Insufficient Balance')
    assert capataz.deepseek_sin_saldo() is True


# ---------------------------------------------------------------------------
# (3) DeepSeek dormido por cuota (429) NO es falta de saldo
# ---------------------------------------------------------------------------

def test_deepseek_dormido_por_cuota_no_es_saldo(tmp_path, monkeypatch):
    _aislar_cuotas(tmp_path, monkeypatch)
    cuotas.dormir('deepseek', '429 rate limit')
    assert capataz.deepseek_sin_saldo() is False


# ---------------------------------------------------------------------------
# (4) Otro motor dormido por saldo NO cuenta como DeepSeek sin saldo
# ---------------------------------------------------------------------------

def test_otro_motor_dormido_por_saldo_no_cuenta(tmp_path, monkeypatch):
    _aislar_cuotas(tmp_path, monkeypatch)
    cuotas.dormir('bigpickle', 'HTTP 402 Insufficient Balance')
    assert capataz.deepseek_sin_saldo() is False


# ---------------------------------------------------------------------------
# (5) El bucle NO para por dolares (no aparece TOPE)
# ---------------------------------------------------------------------------

def test_bucle_no_para_por_dolares(tmp_path, monkeypatch):
    _aislar_cuotas(tmp_path, monkeypatch)
    monkeypatch.setattr(capataz, 'gastado_del_mes', lambda *a, **k: 50.0, raising=False)
    monkeypatch.setattr(capataz, 'listas_para_correr', lambda *a, **k: [], raising=False)
    monkeypatch.setattr(capataz, 'leer_lista', lambda *a, **k: [], raising=False)
    resultado = capataz.bucle('ingeniero', aviso=lambda *a: None)
    assert 'TOPE' not in str(resultado)


# ---------------------------------------------------------------------------
# (6) Con DeepSeek dormido por saldo, el bucle avisa SIN SALDO
# ---------------------------------------------------------------------------

def test_bucle_avisa_sin_saldo(tmp_path, monkeypatch):
    _aislar_cuotas(tmp_path, monkeypatch)
    cuotas.dormir('deepseek', 'HTTP 402 Insufficient Balance')
    monkeypatch.setattr(capataz, 'gastado_del_mes', lambda *a, **k: 0.0, raising=False)
    monkeypatch.setattr(capataz, 'listas_para_correr', lambda *a, **k: [], raising=False)
    monkeypatch.setattr(capataz, 'leer_lista', lambda *a, **k: [], raising=False)
    resultado = capataz.bucle('ingeniero', aviso=lambda *a: None)
    assert 'SIN SALDO' in str(resultado)
