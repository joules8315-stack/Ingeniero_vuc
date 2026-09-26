import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arnes.guardia_de_guardado import rojas_que_frenan


def test_una_roja_no_guardada_es_nueva_y_no_frena():
    rojas_ahora = ["vigias/test_nueva.py"]
    guardadas = []
    declaradas = []
    conocidas = []
    assert rojas_que_frenan(rojas_ahora, guardadas, declaradas, conocidas) == []


def test_una_roja_guardada_declarada_por_tarea_no_frena():
    rojas_ahora = ["vigias/test_a.py"]
    guardadas = ["vigias/test_a.py"]
    declaradas = ["vigias/test_a.py"]
    conocidas = []
    assert rojas_que_frenan(rojas_ahora, guardadas, declaradas, conocidas) == []


def test_una_roja_guardada_conocida_no_frena():
    rojas_ahora = ["vigias/test_b.py"]
    guardadas = ["vigias/test_b.py"]
    declaradas = []
    conocidas = ["vigias/test_b.py"]
    assert rojas_que_frenan(rojas_ahora, guardadas, declaradas, conocidas) == []


def test_una_roja_guardada_no_declarada_ni_conocida_si_frena():
    rojas_ahora = ["vigias/test_c.py"]
    guardadas = ["vigias/test_c.py"]
    declaradas = []
    conocidas = []
    assert rojas_que_frenan(rojas_ahora, guardadas, declaradas, conocidas) == ["vigias/test_c.py"]


def test_varias_rojas_mezcladas_devuelve_solo_las_que_frenan():
    rojas_ahora = [
        "vigias/test_nueva.py",
        "vigias/test_declarada.py",
        "vigias/test_conocida.py",
        "vigias/test_frena_uno.py",
        "vigias/test_frena_dos.py",
    ]
    guardadas = [
        "vigias/test_declarada.py",
        "vigias/test_conocida.py",
        "vigias/test_frena_uno.py",
        "vigias/test_frena_dos.py",
    ]
    declaradas = ["vigias/test_declarada.py"]
    conocidas = ["vigias/test_conocida.py"]
    resultado = rojas_que_frenan(rojas_ahora, guardadas, declaradas, conocidas)
    assert sorted(resultado) == ["vigias/test_frena_dos.py", "vigias/test_frena_uno.py"]
