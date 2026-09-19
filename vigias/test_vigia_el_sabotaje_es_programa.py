# -*- coding: utf-8 -*-
"""VIGIA — EL SABOTAJE ES UN PROGRAMA, NO UNA PROMESA.

Se prueba que sabotaje.sabotear() corre la vigia pedida, mira si se pone roja,
si se queda verde o si el texto viejo no aparece, y que SIEMPRE deja los
archivos como estaban.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, 'arnes'))
import sabotaje  # noqa: E402


PIEZA = 'def doble(x):\n    return x * 2\n'
VIGIA = (
    'import sys, os\n'
    'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n'
    'import pieza\n'
    '\n'
    'def test_doble():\n'
    '    assert pieza.doble(2) == 4\n'
)


def _montar(tmp_path):
    """Escribe pieza.py y test_p.py en la raiz temporal."""
    (tmp_path / 'pieza.py').write_text(PIEZA, encoding='utf-8')
    (tmp_path / 'test_p.py').write_text(VIGIA, encoding='utf-8')


def test_sabotaje_rojo_y_restaura(tmp_path):
    """Un sabotaje que rompe la pieza deja la vigia roja y el archivo igual."""
    _montar(tmp_path)
    antes = (tmp_path / 'pieza.py').read_bytes()

    salida = sabotaje.sabotear(
        str(tmp_path),
        'test_p.py',
        [{'archivo': 'pieza.py', 'viejo': 'x * 2', 'nuevo': 'x * 3'}],
    )

    assert salida['ok'] is True
    assert salida['resultados'][0]['estado'] == 'roja'
    assert (tmp_path / 'pieza.py').read_bytes() == antes


def test_sabotaje_no_encontrado(tmp_path):
    """Si el texto viejo no aparece, el estado es no_encontrado y ok False."""
    _montar(tmp_path)
    antes = (tmp_path / 'pieza.py').read_bytes()

    salida = sabotaje.sabotear(
        str(tmp_path),
        'test_p.py',
        [{'archivo': 'pieza.py', 'viejo': 'no existe', 'nuevo': 'x * 3'}],
    )

    assert salida['ok'] is False
    assert salida['resultados'][0]['estado'] == 'no_encontrado'
    assert (tmp_path / 'pieza.py').read_bytes() == antes


def test_sabotaje_verde(tmp_path):
    """Si el cambio no rompe nada, el estado es verde y ok False."""
    _montar(tmp_path)
    antes = (tmp_path / 'pieza.py').read_bytes()

    salida = sabotaje.sabotear(
        str(tmp_path),
        'test_p.py',
        [{'archivo': 'pieza.py', 'viejo': 'def doble', 'nuevo': 'def doble'}],
    )

    assert salida['ok'] is False
    assert salida['resultados'][0]['estado'] == 'verde'
    assert (tmp_path / 'pieza.py').read_bytes() == antes
