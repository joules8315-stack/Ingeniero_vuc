# -*- coding: utf-8 -*-
"""VIGIA — EL TEXTO VIEJO TIENE QUE EXISTIR EN EL ARCHIVO.

Nace de la mitad de los rechazos medidos el 2026-09-19: al que escribe el codigo le llega
solo un PEDAZO del archivo y, cuando le falta, se inventa el resto. Entonces el texto que
dice estar cambiando NO existe tal cual en el archivo. Eso es una CUENTA que sale gratis
(comparar dos cadenas) y hoy se descubre tarde, despues de pagar una revision.

La frase que se vigila es: EL TEXTO VIEJO NO ESTA EN EL ARCHIVO.

PRUEBA 1: archivo real en disco con cuenta_bien; texto_viejo inventado -> SI sale el fallo.
PRUEBA 2: el mismo archivo, texto_viejo que SI esta -> NINGUN fallo con esa frase.
PRUEBA 3: archivo que no existe y texto_viejo vacio (pieza nueva) -> tampoco sale la frase.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

FRASE = "EL TEXTO VIEJO NO ESTA EN EL ARCHIVO"


def _revisor():
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija.")
    return revisor_de_programa


def _escribir_archivo(tmp_path):
    archivo = tmp_path / "pieza.py"
    archivo.write_text(
        "def cuenta_bien(n):\n"
        "    return n + 1\n",
        encoding="utf-8")
    return archivo


def test_texto_viejo_inventado_si_frena(tmp_path):
    """PRUEBA 1: el texto viejo NO esta en el archivo -> tiene que salir el fallo."""
    r = _revisor()
    archivo = _escribir_archivo(tmp_path)
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "def cuenta_mal(n):\n    return n - 1\n",
        "texto_nuevo": "def cuenta_bien(n):\n    return n + 2\n",
    }
    fallos = r.revisar(propuesta, tarea="cambiar cuenta_bien")
    assert any(FRASE in str(f) for f in fallos), (
        "NO FRENO cuando el texto viejo no esta en el archivo. Sin esta cuenta se paga una "
        "revision para descubrir algo que se sabia gratis comparando dos cadenas. Dijo: "
        + str(fallos))


def test_texto_viejo_que_si_esta_no_frena(tmp_path):
    """PRUEBA 2: el texto viejo SI esta en el archivo -> ningun fallo con esa frase."""
    r = _revisor()
    archivo = _escribir_archivo(tmp_path)
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "def cuenta_bien(n):\n    return n + 1\n",
        "texto_nuevo": "def cuenta_bien(n):\n    return n + 2\n",
    }
    fallos = r.revisar(propuesta, tarea="cambiar cuenta_bien")
    assert not any(FRASE in str(f) for f in fallos), (
        "FRENO EN FALSO: el texto viejo SI esta en el archivo y aun asi salio la frase. "
        "Un candado que frena lo legitimo ensena a ignorarlos todos. Dijo: " + str(fallos))


def test_archivo_nuevo_sin_texto_viejo_no_frena(tmp_path):
    """PRUEBA 3: pieza nueva (archivo que no existe, texto viejo vacio) -> no hay contra que comparar."""
    r = _revisor()
    propuesta = {
        "archivo": str(tmp_path / "no_existe_todavia.py"),
        "texto_viejo": "",
        "texto_nuevo": "def cuenta_bien(n):\n    return n + 1\n",
    }
    fallos = r.revisar(propuesta, tarea="crear pieza nueva")
    assert not any(FRASE in str(f) for f in fallos), (
        "FRENO EN FALSO al crear una pieza nueva: no hay archivo ni texto viejo contra que "
        "comparar, asi que esa frase no puede salir. Dijo: " + str(fallos))
