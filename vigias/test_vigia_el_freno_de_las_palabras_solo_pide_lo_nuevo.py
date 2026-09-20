# -*- coding: utf-8 -*-
"""VIGIA — EL FRENO DE LAS PALABRAS SOLO PIDE LO NUEVO.

La cuenta 4 del revisor (arnes/revisor_de_programa.py) mira las palabras con guion bajo del
encargo y avisa con "NO HACE LO QUE SE PIDIO" cuando una de esas palabras no aparece ni en el
texto viejo ni en el nuevo. Esa cuenta tiene un filo: si el encargo nombra algo que YA ESTA en
el archivo, eso es CONTEXTO y no se pide traerlo. Frenarlo seria una frenada en falso, y una
frenada en falso ensena a ignorar todos los frenos.

Esta vigia fija las dos caras:

  PRUEBA 1 — el encargo habla de una funcion que YA ESTA en el archivo (despide_bien).
             Como ya esta, es contexto: NINGUN fallo puede decir "NO HACE LO QUE SE PIDIO".

  PRUEBA 2 — el encargo pide una llamada a una palabra que NO esta ni en el archivo ni en el
             cambio (cuenta_nueva). Eso si es trabajo que falta: TIENE que salir un fallo con
             "NO HACE LO QUE SE PIDIO" que nombre esa palabra.

Se importa el revisor desde la carpeta arnes, igual que lo hace
vigias/test_vigia_revisor_de_programa.py.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


# El archivo de verdad que se escribe en disco. Tiene DOS funciones: saluda_fuerte y
# despide_bien. La linea que se cambia vive DENTRO de saluda_fuerte.
ARCHIVO_DE_VERDAD = (
    "def saluda_fuerte(nombre):\n"
    "    return 'Hola, ' + nombre\n"
    "\n"
    "\n"
    "def despide_bien(nombre):\n"
    "    return 'Adios, ' + nombre\n"
)

LINEA_VIEJA = "    return 'Hola, ' + nombre\n"
LINEA_NUEVA = "    return 'Hola fuerte, ' + nombre\n"


FRASE_QUE_FRENA = "NO HACE LO QUE SE PIDIO"


def _revisor():
    """El revisor de programa, importado desde arnes como en la vigia del revisor."""
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija.")
    return revisor_de_programa


def _escribir_archivo(tmp_path):
    """Escribe el archivo de verdad en disco y devuelve su ruta."""
    archivo = tmp_path / "ejemplo_dos_funciones.py"
    archivo.write_text(ARCHIVO_DE_VERDAD, encoding="utf-8")
    return archivo


def _propuesta(archivo):
    """La propuesta de las dos pruebas: cambia una linea dentro de saluda_fuerte."""
    return {
        "archivo": str(archivo),
        "funcion": "saluda_fuerte",
        "texto_viejo": LINEA_VIEJA,
        "texto_nuevo": LINEA_NUEVA,
    }


def test_lo_que_ya_esta_en_el_archivo_es_contexto_y_no_se_pide(tmp_path):
    """PRUEBA 1: el encargo nombra despide_bien, que YA ESTA en el archivo.

    Como despide_bien ya esta, es contexto y no se pide traerlo. Ningun fallo puede decir
    "NO HACE LO QUE SE PIDIO": seria una frenada en falso sobre trabajo bueno.
    """
    r = _revisor()
    archivo = _escribir_archivo(tmp_path)
    propuesta = _propuesta(archivo)
    tarea = (
        "Dentro de saluda_fuerte hay que mirar lo que hace despide_bien y dejarlo como esta."
    )

    fallos = r.revisar(propuesta, tarea)

    culpables = [f for f in fallos if FRASE_QUE_FRENA in str(f)]
    assert not culpables, (
        "SE PERDIO EL CONTEXTO: el encargo nombraba despide_bien, que YA ESTA en el archivo, "
        "y el revisor lo trato como trabajo que falta. Una palabra que ya vive en el archivo "
        "es contexto, no una peticion. Fallos devueltos: " + str(fallos))


def test_lo_que_no_esta_en_ningun_lado_si_se_pide(tmp_path):
    """PRUEBA 2: el encargo pide una llamada a cuenta_nueva, que NO esta en ningun lado.

    cuenta_nueva no aparece ni en el archivo ni en el cambio. Eso si es trabajo que falta:
    tiene que salir un fallo con "NO HACE LO QUE SE PIDIO" que nombre esa palabra.
    """
    r = _revisor()
    archivo = _escribir_archivo(tmp_path)
    propuesta = _propuesta(archivo)
    tarea = "Hay que agregar una llamada a cuenta_nueva dentro de saluda_fuerte."

    fallos = r.revisar(propuesta, tarea)

    con_frase = [f for f in fallos if FRASE_QUE_FRENA in str(f)]
    assert con_frase, (
        "SE PERDIO EL FRENO: el encargo pedia una llamada a cuenta_nueva, que no esta ni en "
        "el archivo ni en el cambio, y el revisor no dijo nada. Un trabajo que falta tiene "
        "que salir. Fallos devueltos: " + str(fallos))

    nombra = [f for f in con_frase if "cuenta_nueva" in str(f)]
    assert nombra, (
        "SE PERDIO EL NOMBRE: el revisor freno, pero no dijo QUE palabra falta. El fallo tiene "
        "que nombrar cuenta_nueva para que se sepa que trabajo se quedo sin hacer. Fallos "
        "devueltos: " + str(fallos))
