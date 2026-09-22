# -*- coding: utf-8 -*-
"""VIGIA — EL REVISOR MIRA CADA TROZO, NO SOLO EL PRIMERO.

La funcion revisar(propuesta, tarea) de arnes/revisor_de_programa.py recibe una propuesta que
puede traer una lista 'cambios' con varios trozos. Esta vigia comprueba, sin gastar ni una IA,
que el revisor mira TODOS los trozos y no solo el primero:

  1. Con trozos validos (el texto viejo existe y los nombres del texto nuevo existen), ningun
     texto de la lista que devuelve revisar contiene 'NO EXISTE'.
  2. Si un trozo trae un texto viejo que NO esta en el archivo, algun texto contiene
     'EL TEXTO VIEJO NO ESTA'.
  3. Si un trozo trae en el texto nuevo un nombre que no existe (re sin importar), algun texto
     contiene 'NO EXISTE'.

Se carga el modulo como lo hace vigias/test_vigia_revisor_de_programa.py: metiendo la raiz y
la carpeta arnes en sys.path e importando revisor_de_programa.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


SALTO = "\n"


def _revisor():
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija.")
    return revisor_de_programa


def _escribir_m(tmp_path):
    """Escribe m.py con las lineas exactas que pide la tarea y devuelve su ruta."""
    ruta = tmp_path / "m.py"
    ruta.write_text(
        "import os" + SALTO +
        SALTO +
        "def a():" + SALTO +
        "    return 1" + SALTO +
        SALTO +
        "def b():" + SALTO +
        "    return 2" + SALTO,
        encoding="utf-8",
    )
    return ruta


def _propuesta_valida(ruta):
    """La propuesta del caso (1): dos trozos, los dos con texto viejo existente y nombres
    del texto nuevo que si existen (os esta importado en m.py)."""
    return {
        "archivo": str(ruta),
        "texto_viejo": "",
        "texto_nuevo": "",
        "cambios": [
            {
                "texto_viejo": "def a():" + SALTO + "    return 1" + SALTO,
                "texto_nuevo": "def a():" + SALTO + "    return os.sep" + SALTO,
            },
            {
                "texto_viejo": "def b():" + SALTO + "    return 2" + SALTO,
                "texto_nuevo": "def b():" + SALTO + "    return 3" + SALTO,
            },
        ],
    }


def test_trozos_validos_no_dicen_no_existe(tmp_path):
    """(1) Con los dos trozos validos, ningun texto de la lista contiene 'NO EXISTE'."""
    r = _revisor()
    ruta = _escribir_m(tmp_path)
    propuesta = _propuesta_valida(ruta)

    fallos = r.revisar(propuesta, tarea="en m.py cambia a y b")

    assert not any("NO EXISTE" in str(f) for f in fallos), (
        "Con trozos validos el revisor no debe decir 'NO EXISTE'. Dijo: " + str(fallos))


def test_trozo_con_texto_viejo_que_no_esta(tmp_path):
    """(2) Si el segundo trozo trae un texto viejo que no esta en el archivo, se avisa."""
    r = _revisor()
    ruta = _escribir_m(tmp_path)
    propuesta = _propuesta_valida(ruta)
    propuesta["cambios"][1] = {
        "texto_viejo": "def c():" + SALTO + "    return 9" + SALTO,
        "texto_nuevo": "def c():" + SALTO + "    return 3" + SALTO,
    }

    fallos = r.revisar(propuesta, tarea="en m.py cambia a y b")

    assert any("EL TEXTO VIEJO NO ESTA" in str(f) for f in fallos), (
        "El revisor debe avisar 'EL TEXTO VIEJO NO ESTA' cuando un trozo trae un texto viejo "
        "que no aparece en el archivo. Dijo: " + str(fallos))


def test_trozo_con_nombre_que_no_existe(tmp_path):
    """(3) Si el primer trozo usa 're' sin importarlo, se avisa con 'NO EXISTE'."""
    r = _revisor()
    ruta = _escribir_m(tmp_path)
    propuesta = _propuesta_valida(ruta)
    propuesta["cambios"][0] = {
        "texto_viejo": "def a():" + SALTO + "    return 1" + SALTO,
        "texto_nuevo": "def a():" + SALTO + "    return re.sub" + SALTO,
    }

    fallos = r.revisar(propuesta, tarea="en m.py cambia a y b")

    assert any("NO EXISTE" in str(f) for f in fallos), (
        "El revisor debe avisar 'NO EXISTE' cuando un trozo usa un nombre que no esta "
        "importado ni definido. Dijo: " + str(fallos))
