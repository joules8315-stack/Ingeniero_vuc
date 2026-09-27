"""Vigia: la puerta gratis tambien se cuenta.

Julio se quedo sin presupuesto el 2026-09-27 sin ningun aviso. El recibo de la
puerta gratis devuelve cost 0, y el apunte anotaba cero siempre, asi que el
gasto de 663 llamadas quedo invisible. Medido ese dia: una pregunta de 6 letras
consume 10.683 unidades de entrada.

Esta vigia nace ROJA a proposito: exige dos piezas que HOY NO EXISTEN en
cuerpo/bigpickle.py.

  1) unidades_de_la_salida(salida) -> dict con las unidades que el propio
     recibo declara. En cada linea con type == 'step_finish' el recibo trae
     part.tokens con las claves total, input y output. Con recibo vacio o sin
     tokens devuelve ceros y no revienta.

  2) _anotar(..., unidades=0) -> argumento nuevo opcional que escribe en la
     linea del registro la forma unidades=12720.

La reparacion va en la ronda siguiente. Aqui solo se escribe la vigia.

Reglas de esta prueba:
  - NUNCA escribe en el registro de verdad ni en la memoria de verdad.
  - Todo lo que toca vive en tmp_path.
  - Determinista y sin red.
"""

from __future__ import annotations

import json

import pytest

from cuerpo import bigpickle


# ---------------------------------------------------------------------------
# Utilidades de la prueba
# ---------------------------------------------------------------------------


def _recibo_de_dos_lineas() -> str:
    """Recibo minimo: una linea de texto y una de step_finish con cost 0.

    El coste es 0 (puerta gratis) pero el recibo SI declara las unidades:
    total 12720, input 10683, output 1.
    """
    linea_texto = json.dumps({"type": "text", "part": {"text": "ok"}})
    linea_fin = json.dumps(
        {
            "type": "step_finish",
            "part": {
                "cost": 0,
                "tokens": {"total": 12720, "input": 10683, "output": 1},
            },
        }
    )
    return linea_texto + "\n" + linea_fin + "\n"


def _leer_ultima_linea(ruta) -> str:
    """Devuelve la ultima linea no vacia del registro temporal."""
    texto = ruta.read_text(encoding="utf-8")
    lineas = [ln for ln in texto.splitlines() if ln.strip()]
    assert lineas, "el registro temporal quedo vacio: _anotar no escribio nada"
    return lineas[-1]


# ---------------------------------------------------------------------------
# Pieza 1: unidades_de_la_salida
# ---------------------------------------------------------------------------


def test_unidades_de_la_salida_lee_el_total_aunque_el_costo_sea_cero():
    """La puerta gratis devuelve cost 0, pero el recibo declara 12720 unidades."""
    salida = _recibo_de_dos_lineas()

    unidades = bigpickle.unidades_de_la_salida(salida)

    assert isinstance(unidades, dict), (
        "unidades_de_la_salida debe devolver un diccionario con total, input y output"
    )
    assert unidades.get("total") == 12720, (
        "el recibo declara total 12720; el costo 0 no puede tapar las unidades"
    )
    assert unidades.get("input") == 10683, "el recibo declara input 10683"
    assert unidades.get("output") == 1, "el recibo declara output 1"


def test_unidades_de_la_salida_con_recibo_vacio_devuelve_ceros():
    """Recibo vacio: ceros y sin reventar."""
    unidades = bigpickle.unidades_de_la_salida("")

    assert isinstance(unidades, dict)
    assert unidades.get("total") == 0
    assert unidades.get("input") == 0
    assert unidades.get("output") == 0


def test_unidades_de_la_salida_sin_tokens_devuelve_ceros():
    """step_finish sin part.tokens: ceros y sin reventar."""
    linea = json.dumps({"type": "step_finish", "part": {"cost": 0}})

    unidades = bigpickle.unidades_de_la_salida(linea + "\n")

    assert isinstance(unidades, dict)
    assert unidades.get("total") == 0
    assert unidades.get("input") == 0
    assert unidades.get("output") == 0


def test_unidades_de_la_salida_suma_varios_step_finish():
    """Dos step_finish: las unidades se suman, no se pisan."""
    uno = json.dumps(
        {
            "type": "step_finish",
            "part": {"cost": 0, "tokens": {"total": 100, "input": 90, "output": 10}},
        }
    )
    dos = json.dumps(
        {
            "type": "step_finish",
            "part": {"cost": 0, "tokens": {"total": 200, "input": 180, "output": 20}},
        }
    )

    unidades = bigpickle.unidades_de_la_salida(uno + "\n" + dos + "\n")

    assert unidades.get("total") == 300
    assert unidades.get("input") == 270
    assert unidades.get("output") == 30


def test_unidades_de_la_salida_ignora_lineas_rotas():
    """Lineas que no son JSON valido se ignoran sin reventar."""
    salida = "esto no es json\n" + _recibo_de_dos_lineas()

    unidades = bigpickle.unidades_de_la_salida(salida)

    assert unidades.get("total") == 12720


# ---------------------------------------------------------------------------
# Pieza 2: _anotar acepta unidades y las escribe
# ---------------------------------------------------------------------------


def test_anotar_escribe_las_unidades_en_la_linea(tmp_path, monkeypatch):
    """_anotar(..., unidades=12720) deja 'unidades=12720' en la linea.

    El registro va a un archivo temporal: NUNCA se toca el de verdad.
    """
    ruta_temporal = tmp_path / "BIGPICKLE.log"
    monkeypatch.setattr(bigpickle, "RUTA_LOG", ruta_temporal)

    bigpickle._anotar(
        segundos=1.5,
        costo=0.0,
        ok=True,
        nota="puerta gratis",
        tamano=0,
        unidades=12720,
    )

    linea = _leer_ultima_linea(ruta_temporal)
    assert "unidades=12720" in linea, (
        "la linea del registro debe llevar la forma unidades=12720; "
        f"linea escrita: {linea!r}"
    )


def test_anotar_sin_unidades_usa_cero_por_defecto(tmp_path, monkeypatch):
    """El argumento unidades es opcional y vale 0 por defecto."""
    ruta_temporal = tmp_path / "BIGPICKLE.log"
    monkeypatch.setattr(bigpickle, "RUTA_LOG", ruta_temporal)

    bigpickle._anotar(segundos=0.5, costo=0.0, ok=True, nota="sin unidades")

    linea = _leer_ultima_linea(ruta_temporal)
    assert "unidades=0" in linea, (
        "sin pasar unidades, la linea debe llevar unidades=0; "
        f"linea escrita: {linea!r}"
    )


def test_anotar_sigue_escribiendo_lo_de_antes(tmp_path, monkeypatch):
    """El argumento nuevo no rompe lo que ya se anotaba."""
    ruta_temporal = tmp_path / "BIGPICKLE.log"
    monkeypatch.setattr(bigpickle, "RUTA_LOG", ruta_temporal)

    bigpickle._anotar(
        segundos=2.0,
        costo=0.0,
        ok=True,
        nota="puerta gratis",
        tamano=0,
        unidades=12720,
    )

    linea = _leer_ultima_linea(ruta_temporal)
    assert "segundos=2.000" in linea
    assert "costo=0.000000" in linea
    assert "ok=True" in linea
    assert "nota=puerta gratis" in linea
    assert "unidades=12720" in linea


def test_anotar_no_toca_el_registro_de_verdad(tmp_path, monkeypatch):
    """La prueba escribe SOLO en tmp_path, nunca en el registro real."""
    ruta_temporal = tmp_path / "BIGPICKLE.log"
    monkeypatch.setattr(bigpickle, "RUTA_LOG", ruta_temporal)

    bigpickle._anotar(segundos=0.1, costo=0.0, ok=True, nota="aislado", unidades=1)

    assert ruta_temporal.exists(), "el registro temporal debe existir"
    assert ruta_temporal.parent == tmp_path


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
