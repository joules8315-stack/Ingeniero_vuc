"""Vigia: el capataz marca el estado de una orden y lo deja escrito.

Comprueba tres cosas de cuerpo/capataz.py:
  1. marcar_estado cambia estado, paso_fallido y fallos_seguidos de una orden.
  2. marcar_estado limpia paso_fallido y fallos_seguidos cuando se le pide.
  3. marcar_estado devuelve False con una orden que no existe y no toca el archivo.

Nunca toca el ORDENES.json real: cada prueba apunta __file__ a un tmp_path.
"""

import json
import os

import pytest

from cuerpo import capataz


def _preparar(tmp_path, monkeypatch, ordenes):
    """Aisla el modulo en un tmp_path y escribe un ORDENES.json de prueba.

    Devuelve la ruta del ORDENES.json de prueba.
    """
    monkeypatch.setattr(capataz, "__file__", str(tmp_path / "cuerpo" / "capataz.py"))
    carpeta_memoria = tmp_path / "memoria"
    carpeta_memoria.mkdir(parents=True, exist_ok=True)
    ruta = carpeta_memoria / "ORDENES.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(ordenes, f, indent=2, ensure_ascii=False)
    return ruta


def _leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def test_marcar_estado_escribe_estado_paso_y_fallos(tmp_path, monkeypatch):
    """Con una orden 'X1' pendiente, marcar 'hecha' devuelve True y queda escrito."""
    ruta = _preparar(
        tmp_path,
        monkeypatch,
        [{"id": "X1", "estado": "pendiente", "paso_fallido": "", "fallos_seguidos": 0}],
    )

    resultado = capataz.marcar_estado("X1", "hecha", "vigia_verde", 2)

    assert resultado is True
    lista = _leer(ruta)
    orden = [o for o in lista if o.get("id") == "X1"][0]
    assert orden["estado"] == "hecha"
    assert orden["paso_fallido"] == "vigia_verde"
    assert orden["fallos_seguidos"] == 2


def test_marcar_estado_limpia_paso_y_fallos(tmp_path, monkeypatch):
    """Despues de marcar 'hecha', volver a 'pendiente' limpia paso_fallido y fallos."""
    ruta = _preparar(
        tmp_path,
        monkeypatch,
        [{"id": "X1", "estado": "pendiente", "paso_fallido": "", "fallos_seguidos": 0}],
    )

    assert capataz.marcar_estado("X1", "hecha", "vigia_verde", 2) is True
    assert capataz.marcar_estado("X1", "pendiente", "", 0) is True

    lista = _leer(ruta)
    orden = [o for o in lista if o.get("id") == "X1"][0]
    assert orden["estado"] == "pendiente"
    assert orden["paso_fallido"] == ""
    assert orden["fallos_seguidos"] == 0


def test_marcar_estado_con_id_inexistente_no_toca_el_archivo(tmp_path, monkeypatch):
    """Con un id que no existe devuelve False y el archivo queda igual byte a byte."""
    ruta = _preparar(
        tmp_path,
        monkeypatch,
        [{"id": "X1", "estado": "pendiente", "paso_fallido": "", "fallos_seguidos": 0}],
    )
    with open(ruta, "rb") as f:
        antes = f.read()

    resultado = capataz.marcar_estado("NO_EXISTE", "hecha")

    assert resultado is False
    with open(ruta, "rb") as f:
        despues = f.read()
    assert despues == antes
