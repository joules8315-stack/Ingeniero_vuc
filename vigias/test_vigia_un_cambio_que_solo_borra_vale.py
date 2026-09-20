# -*- coding: utf-8 -*-
"""VIGIA — UN CAMBIO QUE SOLO BORRA VALE.

La frase que se vigila es: "La propuesta no trae texto nuevo."

EL AGUJERO QUE ESTA VIGIA TAPA: arnes/revisor_de_programa.py devuelve esa frase en cuanto
el texto nuevo viene vacio. Pero un BORRADO LEGITIMO tambien trae el texto nuevo vacio: se
quita una funcion que sobra y no se pone nada en su lugar. Si esa frase saliera ahi, el
revisor estaria frenando trabajo bueno, y un candado que frena lo legitimo ensena a ignorar
todos los candados (leccion de las frenadas en falso del 2026-09-08).

DOS PRUEBAS:
  1. Borrado legitimo: hay texto viejo (la funcion sobra_esto) y el texto nuevo es vacio.
     NINGUN fallo puede traer la frase.
  2. Nada que borrar: el texto viejo tambien es vacio. Ahi SI tiene que salir la frase.

Se importa igual que vigias/test_vigia_revisor_de_programa.py: metiendo la raiz del proyecto
y la carpeta arnes en sys.path, y luego importando revisor_de_programa a secas.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

FRASE = "La propuesta no trae texto nuevo"


# El archivo de verdad que se escribe en disco. Dos funciones: una que se queda (suma_dos) y
# otra que sobra (sobra_esto). El texto viejo de la propuesta es EXACTAMENTE el de sobra_esto
# tal como esta en el archivo, para que el revisor lo pueda localizar y sustituir.
CODIGO_DEL_ARCHIVO = (
    "def suma_dos(a, b):\n"
    "    return a + b\n"
    "\n"
    "\n"
    "def sobra_esto(x):\n"
    "    return x * 2\n"
)

TEXTO_VIEJO_SOBRA_ESTO = (
    "def sobra_esto(x):\n"
    "    return x * 2\n"
)


def _revisor():
    """Importa el revisor de programa igual que lo hace la vigia hermana."""
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija.")
    return revisor_de_programa


def test_un_cambio_que_solo_borra_vale(tmp_path):
    """PRUEBA 1: borrado legitimo. Quitar sobra_esto es trabajo bueno y no se puede frenar."""
    r = _revisor()
    archivo = tmp_path / "ejemplo.py"
    archivo.write_text(CODIGO_DEL_ARCHIVO, encoding="utf-8")

    propuesta = {
        "archivo": str(archivo),
        "funcion": "sobra_esto",
        "texto_viejo": TEXTO_VIEJO_SOBRA_ESTO,
        "texto_nuevo": "",
    }
    fallos = r.revisar(propuesta, tarea="quitar la funcion sobra_esto, que ya no se usa")

    assert not any(FRASE in str(f) for f in fallos), (
        "SE RECHAZO UN BORRADO BUENO: la propuesta quita la funcion sobra_esto y no pone nada "
        "en su lugar, que es un borrado legitimo. El revisor no puede contestar con la frase "
        "'%s'. Dijo: %s" % (FRASE, fallos))


def test_sin_texto_viejo_ni_nuevo_si_avisa(tmp_path):
    """PRUEBA 2: no hay nada que borrar ni nada que poner. Ahi SI tiene que avisar."""
    r = _revisor()
    archivo = tmp_path / "ejemplo.py"
    archivo.write_text(CODIGO_DEL_ARCHIVO, encoding="utf-8")

    propuesta = {
        "archivo": str(archivo),
        "funcion": "sobra_esto",
        "texto_viejo": "",
        "texto_nuevo": "",
    }
    fallos = r.revisar(propuesta, tarea="quitar la funcion sobra_esto, que ya no se usa")

    assert any(FRASE in str(f) for f in fallos), (
        "NO AVISO CUANDO NO HABIA NADA QUE HACER: con el texto viejo y el texto nuevo vacios "
        "la propuesta no trae nada que aplicar, y el revisor tiene que decirlo con la frase "
        "'%s'. Dijo: %s" % (FRASE, fallos))
