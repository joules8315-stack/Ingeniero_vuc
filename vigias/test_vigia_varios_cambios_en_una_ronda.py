import os
import sys
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from cuerpo import aplicador


def _escribir(path, contenido):
    path.write_text(contenido, encoding="utf-8")


def _leer(path):
    return path.read_text(encoding="utf-8")


def test_varios_pedazos_en_dos_archivos_se_aplican_todos(tmp_path):
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.py"
    _escribir(f1, "def foo():\n    return 1\n\ndef bar():\n    return 2\n")
    _escribir(f2, "def baz():\n    return 3\n")
    pedazos = [
        {"archivo": str(f1), "funcion": "foo", "texto_viejo": "return 1", "texto_nuevo": "return 10"},
        {"archivo": str(f1), "funcion": "bar", "texto_viejo": "return 2", "texto_nuevo": "return 20"},
        {"archivo": str(f2), "funcion": "baz", "texto_viejo": "return 3", "texto_nuevo": "return 30"},
    ]
    ok, mensaje = aplicador.aplicar_cambios({"cambios": pedazos})
    assert ok is True, mensaje
    assert "return 10" in _leer(f1)
    assert "return 20" in _leer(f1)
    assert "return 30" in _leer(f2)


def test_si_un_pedazo_no_encaja_no_cambia_ningun_archivo(tmp_path):
    f1 = tmp_path / "c.py"
    f2 = tmp_path / "d.py"
    contenido1 = "def alfa():\n    pass\n"
    contenido2 = "def beta():\n    pass\n"
    _escribir(f1, contenido1)
    _escribir(f2, contenido2)
    pedazos = [
        {"archivo": str(f2), "funcion": "beta", "texto_viejo": "pass", "texto_nuevo": "return 2"},
        {"archivo": str(f1), "funcion": "alfa", "texto_viejo": "no_existe", "texto_nuevo": "return 1"},
    ]
    ok, mensaje = aplicador.aplicar_cambios({"cambios": pedazos})
    assert ok is False
    assert "c.py" in mensaje
    assert _leer(f1) == contenido1
    assert _leer(f2) == contenido2


def test_si_un_pedazo_rompe_la_sintaxis_no_cambia_nada(tmp_path):
    f = tmp_path / "e.py"
    original = "def gamma():\n    return 5\n"
    _escribir(f, original)
    pedazos = [
        {"archivo": str(f), "funcion": "gamma", "texto_viejo": "return 5", "texto_nuevo": "def broken(:"},
    ]
    ok, mensaje = aplicador.aplicar_cambios({"cambios": pedazos})
    assert ok is False
    assert _leer(f) == original


def test_un_solo_pedazo_como_hoy_sigue_funcionando(tmp_path):
    f = tmp_path / "f.py"
    _escribir(f, "def delta():\n    return 7\n")
    pedazo = {"archivo": str(f), "funcion": "delta", "texto_viejo": "return 7", "texto_nuevo": "return 70"}
    ok, mensaje = aplicador.aplicar_cambio(pedazo)
    assert ok is True, mensaje
    assert "return 70" in _leer(f)
