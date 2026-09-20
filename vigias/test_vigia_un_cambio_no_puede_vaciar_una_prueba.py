"""Vigia: un cambio no puede vaciar el cuerpo de una prueba ya guardada.

El 2026-09-20 un cambio del equipo se comio el cuerpo entero de una prueba
que ya estaba guardada y la dejo con su docstring y nada mas. Una prueba sin
cuerpo PASA SIEMPRE, asi que nadie se entera: el candado sigue en su sitio
pero ya no vigila nada.

Este vigia exige que el revisor de programa frene ese cambio gratis, antes de
aplicarlo. Nace ROJO: mientras el revisor no detecte el cuerpo vaciado, la
primera prueba falla.
"""

import os
import sys

# Raiz del proyecto: dos dirname sobre el abspath de este propio archivo.
_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ARNES = os.path.join(_RAIZ, "arnes")

for _ruta in (_RAIZ, _ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

import revisor_de_programa  # noqa: E402


# Texto de la prueba de mentira: docstring de una linea y dos renglones de
# cuerpo (una asignacion y un assert sobre esa variable).
_CABEZA = 'def test_algo():\n    """Una prueba de mentira."""\n'
_CUERPO_VIEJO = "    numero = 1\n    assert numero == 1\n"
_CUERPO_NUEVO = "    numero = 2\n    assert numero == 2\n"


def _escribir_prueba_de_mentira(tmp_path, cuerpo):
    """Escribe prueba_de_mentira.py en tmp_path y devuelve su ruta."""
    ruta = tmp_path / "prueba_de_mentira.py"
    ruta.write_text(_CABEZA + cuerpo, encoding="utf-8")
    return str(ruta)


def test_un_cambio_no_puede_vaciar_una_prueba(tmp_path):
    """Un cambio que deja la prueba sin cuerpo tiene que frenarse."""
    ruta = _escribir_prueba_de_mentira(tmp_path, _CUERPO_VIEJO)

    propuesta = {
        "archivo": ruta,
        "texto_viejo": _CUERPO_VIEJO,
        "texto_nuevo": "",
    }
    tarea = "cambiar el cuerpo de la prueba"

    resultado = revisor_de_programa.revisar(propuesta, tarea)

    assert isinstance(resultado, list) and resultado, (
        "Un cambio dejo una prueba sin cuerpo y el revisor no dijo nada. "
        "Una prueba sin cuerpo pasa siempre, asi que el candado deja de "
        "vigilar sin que nadie lo note."
    )
    assert any("sin cuerpo" in str(texto) for texto in resultado), (
        "Un cambio dejo una prueba sin cuerpo y el revisor no lo nombro. "
        "Una prueba sin cuerpo pasa siempre, asi que el candado deja de "
        "vigilar sin que nadie lo note."
    )


def test_un_cambio_que_conserva_el_cuerpo_no_se_frena(tmp_path):
    """Un cambio que solo cambia el numero no puede frenarse."""
    ruta = _escribir_prueba_de_mentira(tmp_path, _CUERPO_VIEJO)

    propuesta = {
        "archivo": ruta,
        "texto_viejo": _CUERPO_VIEJO,
        "texto_nuevo": _CUERPO_NUEVO,
    }
    tarea = "cambiar el cuerpo de la prueba"

    resultado = revisor_de_programa.revisar(propuesta, tarea)

    assert not any("sin cuerpo" in str(texto) for texto in resultado), (
        "Se esta frenando un cambio bueno: el cuerpo sigue estando. Eso "
        "quema una vuelta entera sin arreglar nada."
    )
