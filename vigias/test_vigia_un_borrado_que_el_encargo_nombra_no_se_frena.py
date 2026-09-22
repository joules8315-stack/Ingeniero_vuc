# -*- coding: utf-8 -*-
"""VIGIA — UN BORRADO QUE EL ENCARGO NOMBRA NO SE FRENA.

El revisor de programa (arnes/revisor_de_programa.py) tiene una cuenta que avisa cuando un
cambio se lleva por delante una funcion o una clase que ya estaba: el aviso lleva la palabra
DESAPARECE. Esa cuenta es un aviso, no una condena: si el encargo PIDE ese borrado, el aviso
no debe salir; si el encargo NO lo pide, el aviso tiene que seguir saliendo para que nadie
pierda codigo en silencio.

Esta vigia fija las dos caras con la misma propuesta:

  1. tarea que NOMBRA el cambio (la funcion vieja se cambia por nueva) -> ningun texto de la
     lista que devuelve revisar contiene 'DESAPARECE'.
  2. tarea que NO nombra el borrado (solo cambia el return) -> algun texto de la lista
     contiene 'DESAPARECE'.

Se carga el revisor igual que las demas vigias: metiendo la raiz y la carpeta arnes en
sys.path e importando revisor_de_programa.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


# La propuesta es la misma en las dos pruebas: se borra la funcion vieja y se pone la nueva.
# El texto viejo y el nuevo son archivos enteros que se dejan leer, que es cuando el revisor
# puede comparar las piezas de antes y de despues.
PROPUESTA = {
    "archivo": "m.py",
    "texto_viejo": "def vieja():\n    return 1\n",
    "texto_nuevo": "def nueva():\n    return 1\n",
}


def _revisor():
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija.")
    return revisor_de_programa


def test_un_borrado_que_el_encargo_nombra_no_se_frena():
    """Si la tarea dice que la funcion vieja se cambia por nueva, el borrado esta pedido:
    el revisor no debe sacar el aviso DESAPARECE."""
    r = _revisor()
    tarea = "En m.py la funcion vieja se cambia por nueva"
    fallos = r.revisar(PROPUESTA, tarea=tarea)
    assert not any("DESAPARECE" in str(f) for f in fallos), (
        "SE FRENO UN BORRADO QUE EL ENCARGO NOMBRA: la tarea pedia cambiar la funcion vieja "
        "por la nueva y el revisor saco el aviso DESAPARECE. Dijo: " + str(fallos))


def test_un_borrado_que_el_encargo_no_nombra_sigue_frenando():
    """Si la tarea no pide el borrado (solo cambia el return), el aviso DESAPARECE tiene que
    seguir saliendo: el codigo no puede perderse en silencio."""
    r = _revisor()
    tarea = "En m.py cambia el return"
    fallos = r.revisar(PROPUESTA, tarea=tarea)
    assert any("DESAPARECE" in str(f) for f in fallos), (
        "NO SE FRENO UN BORRADO QUE EL ENCARGO NO NOMBRA: la tarea solo pedia cambiar el "
        "return y el revisor dejo pasar la desaparicion de la funcion vieja sin avisar. "
        "Dijo: " + str(fallos))
