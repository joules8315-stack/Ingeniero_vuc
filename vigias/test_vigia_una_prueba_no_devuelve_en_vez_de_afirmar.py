# -*- coding: utf-8 -*-
"""vigias/test_vigia_una_prueba_no_devuelve_en_vez_de_afirmar.py

VIGIA de arnes/revisor_de_programa.py.

Dos fallos de la misma familia, vistos el mismo dia:

  1. Una prueba NUEVA en la que una funcion test_ DEVUELVE un valor con return y no tiene
     ningun assert. En pytest eso PASA SIEMPRE: el return se ignora y la prueba no vigila
     nada. El revisor la tiene que FRENAR, y el fallo tiene que explicar por que.

  2. Una prueba NUEVA que, cuando la pieza que vigila no existe, se SALTA (unittest.SkipTest
     o pytest.skip) en vez de fallar. Una prueba saltada tampoco puede ponerse roja: el
     revisor tambien la tiene que FRENAR, y el fallo tiene que decir que mientras la pieza
     no exista hay que fallar con assert.

Y tambien prueba lo contrario, que es lo que evita que el revisor se vuelva un estorbo:

  - Una prueba normal con assert NO se frena.
  - Una prueba que solo hace return sin valor NO se frena.
  - Una prueba que se salta por OTRO motivo (por ejemplo, si falta la carpeta de Codex del
    usuario) NO se frena.

Las importaciones de lo que se prueba van DENTRO de cada prueba. Los archivos de mentira se
montan en una carpeta temporal. No se toca ningun otro archivo.
"""
import os
import tempfile


# ---------------------------------------------------------------------------
# Utilidades de montaje: archivos de mentira en una carpeta temporal.
# ---------------------------------------------------------------------------

def _escribir(ruta, texto):
    """Escribe un archivo de mentira, creando su carpeta si hace falta."""
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta


def _propuesta(ruta, viejo, nuevo):
    """La propuesta tal como la recibe el revisor."""
    return {"archivo": ruta, "viejo": viejo, "nuevo": nuevo}


def _texto_de_fallos(fallos):
    """Todo el texto de los fallos junto, en minusculas, para buscar dentro."""
    return " | ".join(str(f) for f in fallos).lower()


# ---------------------------------------------------------------------------
# CASO 1: una prueba NUEVA que devuelve un valor con return y no tiene assert.
# El revisor la tiene que FRENAR, y el fallo tiene que explicar el por que.
# ---------------------------------------------------------------------------

def test_frena_una_prueba_nueva_que_devuelve_en_vez_de_afirmar():
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_devuelve.py")
        viejo = ""
        nuevo = (
            "def test_algo():\n"
            "    resultado = 1 + 1\n"
            "    return resultado\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert fallos, (
            "El revisor NO freno una prueba nueva que devuelve un valor con return y no "
            "tiene ningun assert. En pytest eso pasa siempre y la prueba no vigila nada."
        )
        texto = _texto_de_fallos(fallos)
        assert "return" in texto or "devuelve" in texto, (
            "El revisor freno, pero el fallo no habla del return que devuelve un valor. "
            "Fallos: %r" % (fallos,)
        )
        assert "assert" in texto, (
            "El fallo tiene que decir que hace falta un assert. Fallos: %r" % (fallos,)
        )
        assert "pytest" in texto or "pasa siempre" in texto or "no vigila" in texto, (
            "El fallo tiene que explicar que en pytest eso pasa siempre y la prueba no "
            "vigila nada. Fallos: %r" % (fallos,)
        )


def test_frena_una_prueba_nueva_que_devuelve_en_vez_de_afirmar_sin_assert_ni_uno():
    """Mismo caso, con una prueba que solo devuelve una constante."""
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_devuelve_constante.py")
        viejo = ""
        nuevo = (
            "def test_otra_cosa():\n"
            "    return True\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert fallos, (
            "El revisor NO freno una prueba nueva que solo hace 'return True' y no tiene "
            "ningun assert."
        )
        texto = _texto_de_fallos(fallos)
        assert "assert" in texto, (
            "El fallo tiene que nombrar el assert que falta. Fallos: %r" % (fallos,)
        )


# ---------------------------------------------------------------------------
# CASO 2: una prueba NUEVA que se SALTA cuando la pieza no existe.
# El revisor la tiene que FRENAR, y el fallo tiene que decir que hay que fallar
# con assert mientras la pieza no exista.
# ---------------------------------------------------------------------------

def test_frena_una_prueba_nueva_que_se_salta_con_skiptest():
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_skiptest.py")
        viejo = ""
        nuevo = (
            "import unittest\n"
            "\n"
            "def test_la_pieza():\n"
            "    try:\n"
            "        import pieza_que_no_existe\n"
            "    except ImportError:\n"
            "        raise unittest.SkipTest('la pieza no existe')\n"
            "    assert pieza_que_no_existe\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert fallos, (
            "El revisor NO freno una prueba nueva que se SALTA con unittest.SkipTest cuando "
            "la pieza que vigila no existe. Una prueba saltada tampoco puede ponerse roja."
        )
        texto = _texto_de_fallos(fallos)
        assert "skip" in texto or "salta" in texto, (
            "El fallo tiene que hablar del salto. Fallos: %r" % (fallos,)
        )
        assert "assert" in texto, (
            "El fallo tiene que decir que hay que fallar con assert mientras la pieza no "
            "exista. Fallos: %r" % (fallos,)
        )


def test_frena_una_prueba_nueva_que_se_salta_con_pytest_skip():
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_pytest_skip.py")
        viejo = ""
        nuevo = (
            "import pytest\n"
            "\n"
            "def test_la_pieza():\n"
            "    try:\n"
            "        import pieza_que_no_existe\n"
            "    except ImportError:\n"
            "        pytest.skip('la pieza no existe')\n"
            "    assert pieza_que_no_existe\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert fallos, (
            "El revisor NO freno una prueba nueva que se SALTA con pytest.skip cuando la "
            "pieza que vigila no existe."
        )
        texto = _texto_de_fallos(fallos)
        assert "skip" in texto or "salta" in texto, (
            "El fallo tiene que hablar del salto. Fallos: %r" % (fallos,)
        )
        assert "assert" in texto, (
            "El fallo tiene que decir que hay que fallar con assert mientras la pieza no "
            "exista. Fallos: %r" % (fallos,)
        )


# ---------------------------------------------------------------------------
# LO CONTRARIO: lo legitimo NO se frena.
# ---------------------------------------------------------------------------

def test_no_frena_una_prueba_normal_con_assert():
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_normal.py")
        viejo = ""
        nuevo = (
            "def test_suma():\n"
            "    resultado = 1 + 1\n"
            "    assert resultado == 2\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert not fallos, (
            "El revisor FRENO una prueba normal con assert. Un candado que frena lo "
            "legitimo ensena a ignorar los frenos. Fallos: %r" % (fallos,)
        )


def test_no_frena_una_prueba_que_solo_hace_return_sin_valor():
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_return_vacio.py")
        viejo = ""
        nuevo = (
            "def test_solo_return():" + "\n"
            + "    return" + "\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert not fallos, (
            "El revisor FRENO una prueba que solo hace 'return' sin valor. Eso no es "
            "devolver un valor: no se puede frenar. Fallos: %r" % (fallos,)
        )


def test_no_frena_una_prueba_que_se_salta_por_otro_motivo():
    """Se salta porque falta la carpeta de Codex del usuario, no porque falte la pieza."""
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_skip_otro_motivo.py")
        viejo = ""
        nuevo = (
            "import os\n"
            "import pytest\n"
            "\n"
            "def test_lo_de_codex():\n"
            "    carpeta = os.path.join(os.path.expanduser('~'), '.codex')\n"
            "    if not os.path.isdir(carpeta):\n"
            "        pytest.skip('no hay carpeta de Codex en este equipo')\n"
            "    assert os.path.isdir(carpeta)\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert not fallos, (
            "El revisor FRENO una prueba que se salta por otro motivo (falta la carpeta de "
            "Codex del usuario). Ese salto no tiene nada que ver con la pieza. "
            "Fallos: %r" % (fallos,)
        )


def test_no_frena_una_prueba_que_se_salta_por_otro_motivo_con_skiptest():
    from arnes import revisor_de_programa

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "test_mentira_skiptest_otro_motivo.py")
        viejo = ""
        nuevo = (
            "import os\n"
            "import unittest\n"
            "\n"
            "def test_lo_de_codex():\n"
            "    carpeta = os.path.join(os.path.expanduser('~'), '.codex')\n"
            "    if not os.path.isdir(carpeta):\n"
            "        raise unittest.SkipTest('no hay carpeta de Codex en este equipo')\n"
            "    assert os.path.isdir(carpeta)\n"
        )
        _escribir(ruta, nuevo)

        fallos = revisor_de_programa.revisar(_propuesta(ruta, viejo, nuevo), "")

        assert not fallos, (
            "El revisor FRENO una prueba que se salta con unittest.SkipTest por otro motivo "
            "(falta la carpeta de Codex del usuario). Fallos: %r" % (fallos,)
        )
