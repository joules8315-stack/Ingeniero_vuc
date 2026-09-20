# -*- coding: utf-8 -*-
"""VIGIA — UN CAMBIO DENTRO DE UN TEXTO NO FRENA.

Frenada en falso medida el 2026-09-19: cuando el cambio cae DENTRO de un texto entre
comillas triples (un ejemplo de codigo guardado como texto), el revisor lo lee como si
fuera codigo de verdad y grita que usa un nombre que no existe y que desaparece lo que
ya estaba.

Esta vigia tiene DOS pruebas, y las dos hacen falta:

  PRUEBA 1 — el cambio cae DENTRO de un texto entre comillas triples. El revisor NO debe
decir que usa un nombre que no existe, ni que desaparece lo que ya estaba. Si lo dice,
se pierde trabajo legitimo: nadie puede tocar un ejemplo guardado como texto.

  PRUEBA 2 — el cambio cae en CODIGO DE VERDAD y mete un nombre que no se importa en
ninguna parte. El revisor SI debe decir que usa un nombre que no existe. Si no lo dice,
se pierde el freno: el codigo revienta al correr y nadie se entera antes.

Se importa la funcion revisar de arnes/revisor_de_programa.py igual que lo hace
vigias/test_vigia_revisor_de_programa.py: metiendo la carpeta arnes en el sys.path.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


# El archivo de la PRUEBA 1, escrito en disco de verdad con tmp_path.
# Primero una constante con un texto entre comillas triples que dentro trae un ejemplo
# de prueba que importa algo llamado pieza y comprueba una cuenta. Despues una funcion
# normal. El renglon que se cambia vive DENTRO del texto, no en el codigo.
ARCHIVO_CON_EJEMPLO = '''# -*- coding: utf-8 -*-
EJEMPLO_DE_PRUEBA = """
from pieza import sumar

resultado = sumar(2, 3)
assert resultado == 5
"""


def funcion_normal(a, b):
    return a + b
'''

# El renglon del ejemplo que hace la comprobacion, tal como esta dentro del texto.
RENGLON_VIEJO = "assert resultado == 5"
# Ese mismo renglon con otros numeros.
RENGLON_NUEVO = "assert resultado == 7"


# El archivo de la PRUEBA 2, escrito en disco de verdad con tmp_path.
# Una sola funcion normal que devuelve un numero. La propuesta cambia el archivo ENTERO
# para que la funcion use un nombre que no se importa en ninguna parte.
ARCHIVO_DE_CODIGO = '''# -*- coding: utf-8 -*-
def funcion_normal(a, b):
    return a + b
'''

ARCHIVO_DE_CODIGO_CON_NOMBRE_INVENTADO = '''# -*- coding: utf-8 -*-
def funcion_normal(a, b):
    return herramienta_que_no_existe(a, b)
'''


def _revisor():
    """Trae el revisor de arnes/revisor_de_programa.py, igual que la vigia hermana."""
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija.")
    return revisor_de_programa


def _habla_de_nombre_que_no_existe(fallo):
    """Dice si un fallo del revisor acusa de un nombre que no existe."""
    return "NO EXISTE" in str(fallo).upper()


def _habla_de_que_desaparece_lo_que_ya_estaba(fallo):
    """Dice si un fallo del revisor acusa de que desaparece lo que ya estaba.

    El revisor lo dice de varias maneras (regresion, se pierde, desaparece, borra lo que
    ya estaba). Se miran todas para no dejar pasar la frenada en falso por una palabra.
    """
    texto = str(fallo).upper()
    señales = (
        "DESAPARECE",
        "DESAPARECIO",
        "SE PIERDE",
        "SE PERDIO",
        "REGRESION",
        "BORRA LO QUE YA ESTABA",
        "BORRA LO QUE YA",
        "QUITA LO QUE YA ESTABA",
    )
    return any(s in texto for s in señales)


def test_cambio_dentro_de_un_texto_no_frena(tmp_path):
    """PRUEBA 1: el cambio cae DENTRO de un texto entre comillas triples.

    El revisor NO debe gritar que usa un nombre que no existe (pieza, sumar, resultado
    viven dentro del texto, no son codigo) ni que desaparece lo que ya estaba (el renglon
    sigue ahi, solo cambian los numeros).
    """
    r = _revisor()

    archivo = tmp_path / "con_ejemplo.py"
    archivo.write_text(ARCHIVO_CON_EJEMPLO, encoding="utf-8")

    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": RENGLON_VIEJO,
        "texto_nuevo": RENGLON_NUEVO,
    }

    fallos = r.revisar(propuesta, tarea="cambiar los numeros del ejemplo guardado como texto")

    acusan_nombre = [f for f in fallos if _habla_de_nombre_que_no_existe(f)]
    assert not acusan_nombre, (
        "FRENADA EN FALSO: el cambio cae DENTRO de un texto entre comillas triples y el "
        "revisor lo leyo como codigo de verdad. Grito que usa un nombre que no existe. "
        "Si esto falla, se pierde el trabajo legitimo de tocar un ejemplo guardado como "
        "texto: nadie puede cambiar un numero de un ejemplo sin que el revisor lo acuse "
        "de inventarse nombres. Fallos que acusan: " + str(acusan_nombre))

    acusan_desaparicion = [f for f in fallos if _habla_de_que_desaparece_lo_que_ya_estaba(f)]
    assert not acusan_desaparicion, (
        "FRENADA EN FALSO: el cambio cae DENTRO de un texto entre comillas triples y el "
        "revisor grito que desaparece lo que ya estaba. El renglon sigue ahi, solo cambian "
        "los numeros. Si esto falla, se pierde el trabajo legitimo de tocar un ejemplo "
        "guardado como texto: el revisor lo lee como si fuera codigo de verdad. Fallos "
        "que acusan: " + str(acusan_desaparicion))


def test_cambio_en_codigo_de_verdad_si_frena(tmp_path):
    """PRUEBA 2: el cambio cae en CODIGO DE VERDAD y mete un nombre que no se importa.

    Aqui SI tiene que salir un fallo que hable de un nombre que no existe. Si no sale,
    se pierde el freno: el codigo revienta al correr y nadie se entera antes.
    """
    r = _revisor()

    archivo = tmp_path / "codigo_de_verdad.py"
    archivo.write_text(ARCHIVO_DE_CODIGO, encoding="utf-8")

    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": ARCHIVO_DE_CODIGO,
        "texto_nuevo": ARCHIVO_DE_CODIGO_CON_NOMBRE_INVENTADO,
    }

    fallos = r.revisar(propuesta, tarea="cambiar la funcion para que use otra herramienta")

    acusan_nombre = [f for f in fallos if _habla_de_nombre_que_no_existe(f)]
    assert acusan_nombre, (
        "SE PERDIO EL FRENO: el cambio cae en CODIGO DE VERDAD y mete un nombre que no se "
        "importa en ninguna parte, y el revisor NO dijo que usa un nombre que no existe. "
        "Si esto falla, se pierde el freno que caza el fallo real del 2026-09-08 (usar re "
        "sin importarlo): el codigo revienta al correr y nadie se entera antes. Fallos "
        "devueltos: " + str(fallos))
