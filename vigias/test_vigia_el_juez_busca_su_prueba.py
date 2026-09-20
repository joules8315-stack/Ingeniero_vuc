# -*- coding: utf-8 -*-
# test_vigia_el_juez_busca_su_prueba.py
#
# PARA QUE SIRVE:
# La funcion juzgar_con_vecinas (arnes/juez_de_la_prueba.py) recibe la raiz, la ruta
# relativa del archivo que se cambia (con barras normales), el texto viejo y el texto
# nuevo. Ella sola busca cual es la prueba que cubre ese archivo y devuelve un
# diccionario con al menos ok, prueba y razon.
#
# Esta vigia comprueba tres cosas, con una raiz de mentira armada con tmp_path:
#   1. Si el texto nuevo arregla de verdad (suma en vez de resta), ok es True y la
#      entrada prueba nombra al archivo test_vigia_pieza.py.
#   2. Si el texto nuevo NO arregla nada (multiplicacion en vez de suma), ok es False.
#   3. Si ninguna prueba nombra al archivo, no hay manera de comprobarlo corriendo
#      nada: ok es None (ni True ni False) y la razon lo explica.
#
# Sin esto habria que pagarle a una IA para saber algo que se puede correr gratis.

import sys
from pathlib import Path

import pytest

# Se importa desde la carpeta arnes igual que lo hace
# vigias/test_vigia_el_juez_de_la_prueba.py: se agrega la raiz del proyecto al camino
# de busqueda y se importa el modulo por su nombre.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from arnes.juez_de_la_prueba import juzgar_con_vecinas  # noqa: E402


# ---------------------------------------------------------------------------
# Textos de la pieza de mentira
# ---------------------------------------------------------------------------

PIEZA_QUE_RESTA = '''# -*- coding: utf-8 -*-

def suma(a, b):
    return a - b
'''

PIEZA_QUE_SUMA = '''# -*- coding: utf-8 -*-

def suma(a, b):
    return a + b
'''

PIEZA_QUE_MULTIPLICA = '''# -*- coding: utf-8 -*-

def suma(a, b):
    return a * b
'''

# La prueba de mentira: agrega la carpeta de arriba al camino de busqueda, importa
# pieza y comprueba que suma(2, 3) da 5. Nace ROJA porque pieza.suma resta, y ademas
# NOMBRA a pieza, que es como juzgar_con_vecinas la encuentra.
PRUEBA_DE_MENTIRA = '''# -*- coding: utf-8 -*-

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import pieza


def test_suma_da_cinco():
    assert pieza.suma(2, 3) == 5
'''

# Un archivo que ninguna prueba nombra: no hay manera de comprobarlo corriendo nada.
NADIE_ME_MIRA = '''# -*- coding: utf-8 -*-

def cualquier_cosa(a, b):
    return a + b
'''


# ---------------------------------------------------------------------------
# Utilidad: arma la raiz de mentira con tmp_path
# ---------------------------------------------------------------------------

def _armar_raiz(tmp_path):
    """Crea la raiz de mentira: pieza.py que resta y vigias/test_vigia_pieza.py."""
    raiz = tmp_path / "raiz"
    raiz.mkdir()

    (raiz / "pieza.py").write_text(PIEZA_QUE_RESTA, encoding="utf-8")

    carpeta_vigias = raiz / "vigias"
    carpeta_vigias.mkdir()
    (carpeta_vigias / "test_vigia_pieza.py").write_text(
        PRUEBA_DE_MENTIRA, encoding="utf-8"
    )

    return raiz


# ---------------------------------------------------------------------------
# PRUEBA 1: el texto nuevo arregla de verdad -> ok True y prueba nombra la vigia
# ---------------------------------------------------------------------------

def test_con_el_arreglo_bueno_ok_es_verdadero_y_la_prueba_aparece(tmp_path):
    raiz = _armar_raiz(tmp_path)

    resultado = juzgar_con_vecinas(
        str(raiz),
        "pieza.py",
        PIEZA_QUE_RESTA,
        PIEZA_QUE_SUMA,
    )

    assert isinstance(resultado, dict), (
        "juzgar_con_vecinas tiene que devolver un diccionario con ok, prueba y razon; "
        "sin eso hay que pagarle a una IA para saber algo que se puede correr gratis"
    )

    assert resultado.get("ok") is True, (
        "con el texto nuevo que devuelve la suma, la prueba de mentira pasa de roja a "
        "verde: ok tiene que ser verdadero. Si no, hay que pagarle a una IA para saber "
        "algo que se puede correr gratis"
    )

    prueba = resultado.get("prueba")
    assert prueba, (
        "ok verdadero sin decir CUAL prueba lo demuestra no sirve: la entrada prueba "
        "tiene que nombrar al archivo que se corrio"
    )

    assert "test_vigia_pieza.py" in str(prueba), (
        "la entrada prueba tiene que nombrar al archivo test_vigia_pieza.py, que es la "
        "prueba que cubre a pieza.py; sin eso hay que pagarle a una IA para saber algo "
        "que se puede correr gratis"
    )


# ---------------------------------------------------------------------------
# PRUEBA 2: el texto nuevo NO arregla nada -> ok False
# ---------------------------------------------------------------------------

def test_con_el_arreglo_malo_ok_es_falso(tmp_path):
    raiz = _armar_raiz(tmp_path)

    resultado = juzgar_con_vecinas(
        str(raiz),
        "pieza.py",
        PIEZA_QUE_RESTA,
        PIEZA_QUE_MULTIPLICA,
    )

    assert isinstance(resultado, dict), (
        "juzgar_con_vecinas tiene que devolver un diccionario con ok, prueba y razon; "
        "sin eso hay que pagarle a una IA para saber algo que se puede correr gratis"
    )

    assert resultado.get("ok") is False, (
        "con el texto nuevo que devuelve la multiplicacion, suma(2, 3) da 6 y no 5: la "
        "prueba sigue roja, asi que ok tiene que ser falso. Si no, hay que pagarle a una "
        "IA para saber algo que se puede correr gratis"
    )


# ---------------------------------------------------------------------------
# PRUEBA 3: ninguna prueba nombra al archivo -> ok es None y la razon lo explica
# ---------------------------------------------------------------------------

def test_sin_prueba_que_lo_nombre_ok_es_nada_y_la_razon_lo_explica(tmp_path):
    raiz = _armar_raiz(tmp_path)

    (raiz / "nadie_me_mira.py").write_text(NADIE_ME_MIRA, encoding="utf-8")

    resultado = juzgar_con_vecinas(
        str(raiz),
        "nadie_me_mira.py",
        "def cualquier_cosa(a, b):\n    return a + b\n",
        "def cualquier_cosa(a, b):\n    return a - b\n",
    )

    assert isinstance(resultado, dict), (
        "juzgar_con_vecinas tiene que devolver un diccionario con ok, prueba y razon; "
        "sin eso hay que pagarle a una IA para saber algo que se puede correr gratis"
    )

    assert resultado.get("ok") is None, (
        "si ninguna prueba nombra a nadie_me_mira.py, no hay manera de comprobarlo "
        "corriendo nada: ok NO puede ser ni verdadero ni falso, tiene que ser nada "
        "(None). Si no, hay que pagarle a una IA para saber algo que se puede correr "
        "gratis"
    )

    razon = resultado.get("razon")
    assert razon, (
        "cuando ok es nada, la razon tiene que explicar por que no se pudo comprobar; "
        "sin eso hay que pagarle a una IA para saber algo que se puede correr gratis"
    )

    assert isinstance(razon, str) and razon.strip(), (
        "la razon tiene que ser un texto en castellano que explique que ninguna prueba "
        "nombra al archivo y por eso no se puede comprobar corriendo nada"
    )
