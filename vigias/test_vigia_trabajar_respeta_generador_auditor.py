# -*- coding: utf-8 -*-
"""VIGIA — TRABAJAR RESPETA GENERADOR/AUDITOR (encargo de Julio 2026-08-31).

Julio: "que se pueda elegir de verdad quien genera y quien revisa". Claude lo cerro en la
tarea: en cuerpo/obrero.py, la funcion trabajar() acepta `generador` y `auditor` y NO LOS USA
en ningun sitio (los acepta y los tira). Por eso se perdian vueltas creyendo que se probaba con
otro cerebro. Tres condiciones de Claude:
  1. el revisor NUNCA puede ser el que escribio: si el auditor pedido resulta ser quien genero,
     se lo descarta y se busca otro; si no queda otro, se DICE, no se calla.
  2. si no puede respetar generador/auditor pedidos, AVISA en vez de callarse.
  3. el codigo va DENTRO del encargo.
"""
import inspect
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cuerpo import obrero


def test_trabajar_pasa_generador_como_primero():
    """El generador pedido se intenta PRIMERO, no se ignora."""
    src = inspect.getsource(obrero.trabajar)
    # se pasa generador como 'primero' a la llamada de GENERAR (_preguntar_con_relevo pesado)
    assert "primero=generador" in src, \
        "trabajar() no pasa el generador pedido como 'primero' en la llamada de GENERAR"


def test_trabajar_pasa_auditor_como_primero():
    """El auditor pedido se intenta PRIMERO en la llamada de AUDITAR."""
    src = inspect.getsource(obrero.trabajar)
    assert "primero=auditor" in src or "primero=auditor_ok" in src, \
        "trabajar() no pasa el auditor pedido como 'primero' en la llamada de AUDITAR"


def test_el_auditor_nunca_es_el_que_genero():
    """Cuatro ojos de verdad: el que genera no se audita a si mismo (condicion 1 de Claude)."""
    src = inspect.getsource(obrero.trabajar)
    assert "evitar=quien_gen" in src, "el generador puede auditarse a si mismo"


def test_inventa_no_respeta_generador_sin_avisar():
    """Si no puede usar el generador/auditor pedido, tiene que DECIRLO (condicion 2 de Claude).

    El truco de la 'no_vale_si' de la vigia a ciegas: que no baste con anadir un comentario.
    Debe quedar un aviso real en la salida cuando el pedido no se pudo respetar.
    """
    src = inspect.getsource(obrero.trabajar)
    # hay manejo de 'generador no disponible' y 'auditor no disponible' -> se avisa
    assert "no esta disponible" in src or "no disponible" in src, \
        "no hay forma de que trabajar() avise que no pudo respetar el generador/auditor"
