# -*- coding: utf-8 -*-
"""Vigia: bigpickle descansa tras dos fallos seguidos.

Vigila dos funciones de cuerpo/cuotas.py:
  · bigpickle_fallo()  — apunta un fallo de bigpickle.
  · bigpickle_acierto() — borra la cuenta de fallos de bigpickle.

Reglas que se comprueban:
  1) Un solo fallo NO lo manda a dormir: sigue despierto.
  2) Dos fallos seguidos SI lo mandan a dormir, y la marca dura ~1800 s.
  3) Un acierto en medio borra la cuenta: fallo, acierto, fallo -> despierto.

La memoria de cuotas se aisla cambiando cuotas.RUTA a un archivo en tmp_path, para no
tocar memoria/CUOTAS.json de la casa real.
"""
import time

from cuerpo import cuotas


QUIEN = "bigpickle"


def _aislar(monkeypatch, tmp_path):
    """Apunta cuotas.RUTA a un archivo temporal y devuelve la ruta usada."""
    ruta = tmp_path / "CUOTAS.json"
    monkeypatch.setattr(cuotas, "RUTA", str(ruta))
    return ruta


def test_un_solo_fallo_deja_a_bigpickle_despierto(monkeypatch, tmp_path):
    """Tras UN solo fallo, bigpickle sigue despierto."""
    _aislar(monkeypatch, tmp_path)

    cuotas.bigpickle_fallo()

    assert cuotas.desperto(QUIEN) is True


def test_dos_fallos_seguidos_mandan_a_bigpickle_a_dormir(monkeypatch, tmp_path):
    """Tras DOS fallos seguidos, bigpickle duerme ~1800 s desde ahora."""
    _aislar(monkeypatch, tmp_path)

    cuotas.bigpickle_fallo()
    cuotas.bigpickle_fallo()

    assert cuotas.desperto(QUIEN) is False

    ahora = time.time()
    hasta = cuotas._leer()["dormidos"][QUIEN]["hasta"]
    assert 1790 <= (hasta - ahora) <= 1810


def test_acierto_borra_la_cuenta_y_bigpickle_sigue_despierto(monkeypatch, tmp_path):
    """Fallo, acierto y fallo: el acierto borra la cuenta, bigpickle sigue despierto."""
    _aislar(monkeypatch, tmp_path)

    cuotas.bigpickle_fallo()
    cuotas.bigpickle_acierto()
    cuotas.bigpickle_fallo()

    assert cuotas.desperto(QUIEN) is True
