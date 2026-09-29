import os
import sys

import pytest


# ---------------------------------------------------------------------------
# ARRANQUE: dejar en sys.path la carpeta de arriba de vigias y la carpeta arnes.
# Se calcula con os.path a partir de la ruta de ESTE archivo de prueba.
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")

for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


RUTA_METODO = os.path.join(ARNES, "metodo.py")


# ---------------------------------------------------------------------------
# ROTULOS que el metodo tiene que exigir. Son los siete del encargo.
# ---------------------------------------------------------------------------
ROTULOS = [
    "PROBLEMA",
    "EVIDENCIA",
    "CAMINO",
    "PUEDE DANAR",
    "VIGIA",
    "NO SE TOCA",
    "MANO",
]


# ---------------------------------------------------------------------------
# ENCARGO COMPLETO de mentira: trae los siete rotulos con algo escrito detras.
# Se arma por partes para no dejar nada con forma de llave en el archivo.
# ---------------------------------------------------------------------------
ENCARGO_COMPLETO = (
    "PROBLEMA: Julio dice que el metodo no puede depender de la memoria de la IA "
    "y que hace falta un programa que obligue a seguirlo."
    "\n"
    "EVIDENCIA: se midio hoy con el registro de caminos y contesto que la ultima "
    "anotacion es del 2026-09-28, o sea que hoy no se apunto ni uno."
    "\n"
    "CAMINO: se comprobo contra el registro de caminos que ya fallaron y este no "
    "repite ninguno de los cuarenta apuntados."
    "\n"
    "PUEDE DANAR: puede danar al ingeniero que lanza la ronda a mano, porque el "
    "freno queda ciego y se saltan pasos del metodo."
    "\n"
    "VIGIA: la prueba es vigias/test_vigia_el_metodo_frena_el_encargo_mal_preparado.py "
    "y prometo sabotearla quitando un rotulo para ver que la lista lo nombra."
    "\n"
    "NO SE TOCA: lo que se queda igual es ingeniero.py y el registro de caminos; "
    "solo se anade la pieza nueva."
    "\n"
    "MANO: la mano mas barata que puede hacerlo es el obrero gratis, porque solo "
    "hay que escribir un archivo nuevo con una funcion."
)


# ---------------------------------------------------------------------------
# AYUDANTE: importa la pieza DENTRO de la prueba, no al cargar el modulo.
# Asi, si la pieza no existe, el fallo se ve como un assert claro y no como
# un error de recoleccion de pytest.
# ---------------------------------------------------------------------------
def _cargar_metodo():
    assert os.path.isfile(RUTA_METODO), (
        "arnes/metodo.py TODAVIA NO ESTA ESCRITA: esta prueba nace ROJA a "
        "proposito. La pieza que vigila se escribe en otra ronda; hoy solo se "
        "entrega esta prueba. Ruta esperada: %s" % RUTA_METODO
    )
    import importlib
    if "metodo" in sys.modules:
        return importlib.reload(sys.modules["metodo"])
    import metodo
    return metodo


# ---------------------------------------------------------------------------
# CASO 1: un encargo vacio le falta todo -> la lista trae siete cosas.
# ---------------------------------------------------------------------------
def test_encargo_vacio_le_falta_todo(tmp_path):
    metodo = _cargar_metodo()
    faltas = metodo.revisar("", str(tmp_path))
    assert isinstance(faltas, list), (
        "revisar() tiene que devolver una LISTA de frases, no %r" % type(faltas)
    )
    assert len(faltas) == 7, (
        "un encargo vacio tiene que devolver SIETE faltas (una por rotulo), "
        "y devolvio %d: %r" % (len(faltas), faltas)
    )


# ---------------------------------------------------------------------------
# CASO 2: un encargo completo pasa -> la lista queda VACIA.
# ---------------------------------------------------------------------------
def test_encargo_completo_pasa(tmp_path):
    metodo = _cargar_metodo()
    faltas = metodo.revisar(ENCARGO_COMPLETO, str(tmp_path))
    assert isinstance(faltas, list), (
        "revisar() tiene que devolver una LISTA de frases, no %r" % type(faltas)
    )
    assert faltas == [], (
        "un encargo con los siete rotulos escritos tiene que devolver lista "
        "VACIA, y devolvio: %r" % (faltas,)
    )


# ---------------------------------------------------------------------------
# CASO 3: si falta una, se nombra esa -> quitamos EVIDENCIA y solo sale esa.
# ---------------------------------------------------------------------------
def test_si_falta_una_se_nombra_esa(tmp_path):
    metodo = _cargar_metodo()
    lineas = ENCARGO_COMPLETO.split("\n")
    sin_evidencia = "\n".join(
        l for l in lineas if not l.strip().startswith("EVIDENCIA")
    )
    assert "EVIDENCIA" not in sin_evidencia, (
        "montaje de la prueba roto: no se consiguio quitar el rotulo EVIDENCIA"
    )
    faltas = metodo.revisar(sin_evidencia, str(tmp_path))
    assert isinstance(faltas, list), (
        "revisar() tiene que devolver una LISTA de frases, no %r" % type(faltas)
    )
    assert len(faltas) == 1, (
        "quitando solo EVIDENCIA tiene que salir EXACTAMENTE una falta, y "
        "salieron %d: %r" % (len(faltas), faltas)
    )
    assert "EVIDENCIA" in faltas[0].upper(), (
        "la unica falta tiene que hablar de la EVIDENCIA, y dijo: %r" % (faltas[0],)
    )


# ---------------------------------------------------------------------------
# CASO 4: lo que devuelve sirve para arreglarlo -> cada frase es util.
# ---------------------------------------------------------------------------
def test_lo_que_devuelve_sirve_para_arreglarlo(tmp_path):
    metodo = _cargar_metodo()
    faltas = metodo.revisar("", str(tmp_path))
    assert isinstance(faltas, list), (
        "revisar() tiene que devolver una LISTA de frases, no %r" % type(faltas)
    )
    assert len(faltas) == 7, (
        "un encargo vacio tiene que devolver SIETE faltas, y devolvio %d: %r"
        % (len(faltas), faltas)
    )
    for i, frase in enumerate(faltas):
        assert isinstance(frase, str), (
            "la falta %d no es texto, es %r" % (i, type(frase))
        )
        assert frase.strip() != "", (
            "la falta %d esta vacia; tiene que decir que falta Y como escribirlo"
            % i
        )
        assert len(frase) > 15, (
            "la falta %d es demasiado corta (%d letras): %r. Tiene que decir "
            "que falta Y como escribirlo, no solo el nombre del rotulo."
            % (i, len(frase), frase)
        )
