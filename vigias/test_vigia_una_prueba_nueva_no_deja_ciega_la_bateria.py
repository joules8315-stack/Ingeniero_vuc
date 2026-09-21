# -*- coding: utf-8 -*-
"""vigias/test_vigia_una_prueba_nueva_no_deja_ciega_la_bateria.py

VIGIA de arnes/revisor_de_programa.py.

QUE VIGILA
-----------
Que el revisor FRENE una prueba NUEVA que, arriba del archivo, importa por su nombre
algo que NO existe todavia en la pieza que dice vigilar. Ese fallo no deja roja solo
a esa prueba: revienta la RECOGIDA de pytest y deja CIEGA a toda la bateria. El
revisor tiene que decirlo con esas palabras y tiene que exigir que la importacion
se haga DENTRO de cada prueba.

Y que NO FRENE cuando lo que se importa SI existe en la pieza vigilada.

COMO
----
Se montan los archivos de mentira (la pieza vigilada y la prueba nueva) en una
carpeta temporal. Nunca se toca nada del negocio.

Se usa asi:
    pytest vigias/test_vigia_una_prueba_nueva_no_deja_ciega_la_bateria.py
"""
import os
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from arnes import revisor_de_programa  # noqa: E402


# ---------------------------------------------------------------------------
# Utilidades para montar los archivos de mentira en una carpeta temporal
# ---------------------------------------------------------------------------

def _escribir(ruta, texto):
    """Escribe un archivo de mentira, creando la carpeta si hace falta."""
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta


def _propuesta(ruta_archivo, texto_viejo, texto_nuevo):
    """Arma la propuesta tal como la espera el revisor."""
    return {
        "archivo": ruta_archivo,
        "texto_viejo": texto_viejo,
        "texto_nuevo": texto_nuevo,
    }


def _junta(fallos):
    """Todo el texto de los fallos, en minusculas, para poder buscar dentro."""
    return " | ".join(str(f) for f in fallos).lower()


# ---------------------------------------------------------------------------
# CASO 1 — LA PRUEBA NUEVA IMPORTA ARRIBA UN NOMBRE QUE NO EXISTE
# ---------------------------------------------------------------------------

def test_frena_prueba_nueva_que_importa_arriba_un_nombre_inexistente():
    """Una prueba nueva que arriba hace 'from pieza import nombre_que_no_existe'
    tiene que ser FRENADA por el revisor."""
    with tempfile.TemporaryDirectory() as tmp:
        pieza = _escribir(
            os.path.join(tmp, "pieza_de_mentira.py"),
            "# -*- coding: utf-8 -*-\n"
            "def funcion_que_si_existe():\n"
            "    return 1\n",
        )
        prueba = _escribir(
            os.path.join(tmp, "test_prueba_nueva.py"),
            "# -*- coding: utf-8 -*-\n"
            "from pieza_de_mentira import nombre_que_no_existe\n"
            "\n"
            "def test_algo():\n"
            "    assert nombre_que_no_existe() == 1\n",
        )
        propuesta = _propuesta(prueba, "", open(prueba, encoding="utf-8").read())
        fallos = revisor_de_programa.revisar(propuesta, "crear prueba nueva")
        assert fallos, (
            "El revisor NO freno una prueba nueva que importa arriba un nombre "
            "que no existe en la pieza vigilada. Eso revienta la recogida de pytest "
            "y deja ciega a toda la bateria."
        )
        # La pieza vigilada existe y tiene el nombre bueno; el malo no esta.
        assert os.path.isfile(pieza)


def test_el_fallo_dice_que_deja_ciega_a_toda_la_bateria():
    """El fallo tiene que EXPLICAR que no deja roja solo a esa prueba: para la
    recogida de pytest y deja ciega a toda la bateria."""
    with tempfile.TemporaryDirectory() as tmp:
        _escribir(
            os.path.join(tmp, "pieza_de_mentira.py"),
            "# -*- coding: utf-8 -*-\n"
            "def funcion_que_si_existe():\n"
            "    return 1\n",
        )
        prueba = _escribir(
            os.path.join(tmp, "test_prueba_nueva.py"),
            "# -*- coding: utf-8 -*-\n"
            "from pieza_de_mentira import nombre_que_no_existe\n"
            "\n"
            "def test_algo():\n"
            "    assert nombre_que_no_existe() == 1\n",
        )
        propuesta = _propuesta(prueba, "", open(prueba, encoding="utf-8").read())
        fallos = revisor_de_programa.revisar(propuesta, "crear prueba nueva")
        texto = _junta(fallos)
        assert "recogida" in texto or "bateria" in texto or "ciega" in texto, (
            "El revisor frena, pero NO explica que el fallo para la recogida de pytest "
            "y deja ciega a toda la bateria. Un freno que no dice la causa no se puede "
            "investigar ni reparar. Fallos: %r" % (fallos,)
        )


def test_el_fallo_pide_importar_dentro_de_cada_prueba():
    """El fallo tiene que decir que la importacion se hace DENTRO de cada prueba."""
    with tempfile.TemporaryDirectory() as tmp:
        _escribir(
            os.path.join(tmp, "pieza_de_mentira.py"),
            "# -*- coding: utf-8 -*-\n"
            "def funcion_que_si_existe():\n"
            "    return 1\n",
        )
        prueba = _escribir(
            os.path.join(tmp, "test_prueba_nueva.py"),
            "# -*- coding: utf-8 -*-\n"
            "from pieza_de_mentira import nombre_que_no_existe\n"
            "\n"
            "def test_algo():\n"
            "    assert nombre_que_no_existe() == 1\n",
        )
        propuesta = _propuesta(prueba, "", open(prueba, encoding="utf-8").read())
        fallos = revisor_de_programa.revisar(propuesta, "crear prueba nueva")
        texto = _junta(fallos)
        assert "dentro" in texto and "prueba" in texto, (
            "El revisor frena, pero NO dice que la importacion tiene que hacerse "
            "DENTRO de cada prueba. Fallos: %r" % (fallos,)
        )


# ---------------------------------------------------------------------------
# CASO 2 — LA PRUEBA NUEVA IMPORTA ARRIBA UN NOMBRE QUE SI EXISTE
# ---------------------------------------------------------------------------

def test_no_frena_cuando_lo_importado_si_existe():
    """Si el nombre importado SI existe en la pieza vigilada, el revisor NO frena."""
    with tempfile.TemporaryDirectory() as tmp:
        _escribir(
            os.path.join(tmp, "pieza_de_mentira.py"),
            "# -*- coding: utf-8 -*-\n"
            "def funcion_que_si_existe():\n"
            "    return 1\n",
        )
        prueba = _escribir(
            os.path.join(tmp, "test_prueba_nueva.py"),
            "# -*- coding: utf-8 -*-\n"
            "from pieza_de_mentira import funcion_que_si_existe\n"
            "\n"
            "def test_algo():\n"
            "    assert funcion_que_si_existe() == 1\n",
        )
        propuesta = _propuesta(prueba, "", open(prueba, encoding="utf-8").read())
        fallos = revisor_de_programa.revisar(propuesta, "crear prueba nueva")
        assert not fallos, (
            "El revisor FRENO una prueba nueva que importa un nombre que SI existe "
            "en la pieza vigilada. Un candado que frena lo legitimo ensena a ignorar "
            "todos los candados. Fallos: %r" % (fallos,)
        )


def test_no_frena_cuando_la_importacion_va_dentro_de_la_prueba():
    """Si la importacion se hace DENTRO de la prueba, el revisor NO frena, aunque
    el nombre no exista arriba: dentro de la prueba un fallo deja roja solo a esa
    prueba, no ciega a la bateria."""
    with tempfile.TemporaryDirectory() as tmp:
        _escribir(
            os.path.join(tmp, "pieza_de_mentira.py"),
            "# -*- coding: utf-8 -*-\n"
            "def funcion_que_si_existe():\n"
            "    return 1\n",
        )
        prueba = _escribir(
            os.path.join(tmp, "test_prueba_nueva.py"),
            "# -*- coding: utf-8 -*-\n"
            "def test_algo():\n"
            "    from pieza_de_mentira import funcion_que_si_existe\n"
            "    assert funcion_que_si_existe() == 1\n",
        )
        propuesta = _propuesta(prueba, "", open(prueba, encoding="utf-8").read())
        fallos = revisor_de_programa.revisar(propuesta, "crear prueba nueva")
        assert not fallos, (
            "El revisor FRENO una prueba que importa DENTRO de la prueba. Eso es "
            "justo lo que se pide. Fallos: %r" % (fallos,)
        )


# ---------------------------------------------------------------------------
# CASO 3 — LA CARPETA TEMPORAL NO TOCA NADA DEL NEGOCIO
# ---------------------------------------------------------------------------

def test_los_archivos_de_mentira_viven_en_carpeta_temporal():
    """Los archivos de mentira se montan en una carpeta temporal y no tocan
    ninguna pieza del negocio."""
    with tempfile.TemporaryDirectory() as tmp:
        pieza = _escribir(
            os.path.join(tmp, "pieza_de_mentira.py"),
            "# -*- coding: utf-8 -*-\n"
            "def funcion_que_si_existe():\n"
            "    return 1\n",
        )
        prueba = _escribir(
            os.path.join(tmp, "test_prueba_nueva.py"),
            "# -*- coding: utf-8 -*-\n"
            "from pieza_de_mentira import nombre_que_no_existe\n"
            "\n"
            "def test_algo():\n"
            "    assert nombre_que_no_existe() == 1\n",
        )
        assert os.path.isfile(pieza)
        assert os.path.isfile(prueba)
        assert tmp in pieza
        assert tmp in prueba
        # Nada de lo montado vive dentro de la raiz del negocio.
        assert not pieza.startswith(RAIZ + os.sep)
        assert not prueba.startswith(RAIZ + os.sep)
