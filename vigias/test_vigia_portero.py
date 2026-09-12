# -*- coding: utf-8 -*-
"""VIGIA de arnes/portero.py — EL PORTERO decide con programa, sin gastar un cerebro.

Esta vigia es una prueba de INTEGRACION real, no unitaria con datos hermeetizados:
el portero ahora REUSA arnes/reparto.py (la fuente unica de la verdad), asi que aqui
se planta el reparto y los fallos en archivos temporales con las funciones REALES de
arnes.reparto (asignar, supervisar) y se comprueba que el portero decide de verdad.

Vigia verde NO es prueba (Ley 5): la prueba es que Julio vea que una cuenta no llega a
ningun cerebro en vivo. Esta vigia solo comprueba que el portero responde con lo real.
"""
import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

import arnes.reparto as reparto
import arnes.portero as p


@pytest.fixture
def temporales(tmp_path, monkeypatch):
    """Apunta reparto y fallos a archivos temporales, ya creados y vacios.

    Devuelve (ruta_reparto, ruta_fallos) para que cada prueba pueda plantarlos.
    """
    ruta_reparto = str(tmp_path / "REPARTO_IA.json")
    monkeypatch.setattr(reparto, "RUTA", ruta_reparto)
    with open(ruta_reparto, "w", encoding="utf-8") as f:
        json.dump([], f)

    ruta_fallos = str(tmp_path / "FALLOS.json")
    monkeypatch.setattr(p, "FALLOS_RUTA", ruta_fallos)
    with open(ruta_fallos, "w", encoding="utf-8") as f:
        json.dump([], f)
    return ruta_reparto, ruta_fallos


def test_tarea_viva_devuelve_dueno_y_no_lo_pisa(temporales):
    """Una tarea recien asignada -> ya_tiene_dueno con quien y estado reales."""
    tarea = "reparar el diccionario"
    ok, _ = reparto.asignar("claude", tarea)
    assert ok, "no dejo asignar la tarea"
    r = p.decidir("ingeniero", tarea)
    assert r["decision"] == "ya_tiene_dueno"
    assert r["quien_la_tiene"] == "claude"
    assert r["estado"] == "asignada"


def test_estado_correcta_no_cuenta_como_viva(temporales):
    """Una tarea supervisada correcta ya no es viva: se puede pedir de nuevo."""
    tarea = "reparar el diccionario"
    # Con su guardian nombrado (2026-09-12): desde que la ley "una opinion no es prueba" tiene
    # quien la haga cumplir, una tarea sin guardian nombrado no se cierra. Lo que esta prueba
    # comprueba es otra cosa (que una correcta deja de estar viva), y sigue igual.
    reparto.asignar("claude", tarea, vigia="vigias/test_vigia_diccionario_de_julio.py")
    estado, _ = reparto.supervisar("claude", tarea, True)  # la cierra como correcta
    assert estado == "correcta"
    r = p.decidir("ingeniero", tarea)
    assert r["decision"] != "ya_tiene_dueno"


def test_no_confunde_por_parecido(temporales):
    """Una tarea parecida pero distinta no se confunde con la que esta viva."""
    reparto.asignar("claude", "reparar el diccionario envenenado")
    r = p.decidir("ingeniero", "reparar el diccionario envenenado ahora")
    assert r["decision"] != "ya_tiene_dueno"


def test_encargo_con_texto_decidido_es_cuenta(temporales):
    """Una tarea que trae el texto viejo y el nuevo decididos -> cuenta (programa)."""
    tarea = {"TEXTO_VIEJO": "linea vieja", "TEXTO_NUEVO": "linea nueva"}
    r = p.decidir("ingeniero", tarea)
    assert r["decision"] == "cuenta"
    assert "programa" in r["motivo"]


def test_tarea_abierta_sin_dueno_es_juicio(temporales):
    """Una tarea totalmente nueva, sin dueno ni fallos -> juicio."""
    r = p.decidir("ingeniero", "una tarea totalmente nueva sin decidir")
    assert r["decision"] == "juicio"


def test_pieza_con_fallo_curado_se_avisa(temporales, tmp_path):
    """Si la pieza que toca la tarea tiene un fallo curado por un vigia que existe -> ya_curado."""
    pieza = "cerebro/piezas.py"
    curador = tmp_path / "un_vigia_curador.py"
    curador.write_text("contenido", encoding="utf-8")
    ruta_reparto, ruta_fallos = temporales
    with open(ruta_fallos, "w", encoding="utf-8") as f:
        json.dump([{"piezas": [pieza], "quien_lo_caza": str(curador)}], f)
    tarea = {"piezas": [pieza]}
    r = p.decidir("ingeniero", tarea)
    assert r["decision"] == "ya_curado"
    assert pieza in r["piezas"]


def test_no_se_pudo_leer_reparto_no_bloquea(temporales):
    """Si no existe el archivo de reparto -> no_se_sabe con NO BLOQUEAR (jamas bloquea)."""
    ruta_reparto, _ = temporales
    os.remove(ruta_reparto)
    r = p.decidir("ingeniero", "cualquier tarea")
    assert r["decision"] == "no_se_sabe"
    assert "NO BLOQUEAR" in r["motivo"]


def test_no_se_pudo_leer_fallos_no_bloquea(temporales):
    """Si el reparto esta pero no se pudo leer los fallos -> no_se_sabe, NO BLOQUEAR."""
    _, ruta_fallos = temporales
    os.remove(ruta_fallos)
    r = p.decidir("ingeniero", "cualquier tarea sin dueno")
    assert r["decision"] == "no_se_sabe"
    assert "NO BLOQUEAR" in r["motivo"]
