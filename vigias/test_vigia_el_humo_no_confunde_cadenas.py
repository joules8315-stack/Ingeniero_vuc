"""Vigia: el humo no debe confundir cadenas con comentarios.

sin_ruido borra desde cualquier signo numeral hasta el final de la linea. Si ese
numeral esta dentro de unas comillas, no es un comentario: es parte de la cadena.
Esta vigia nace roja y avisa de ese freno en falso.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import revisor_de_programa as r


def test_el_numeral_dentro_de_una_cadena_no_se_borra():
    """Un numeral dentro de comillas es contenido, no comentario."""
    texto = "x.append(" + repr("### a relevancia") + ")"
    limpio = r.sin_ruido(texto)
    assert "relevancia" in limpio, (
        "sin_ruido borro el contenido de una cadena que llevaba numeral: %r" % limpio
    )


def test_un_comentario_de_verdad_si_se_quita():
    """Un numeral fuera de comillas si es un comentario y debe desaparecer."""
    limpio = r.sin_ruido("x = 1  # comentario")
    assert "comentario" not in limpio, (
        "sin_ruido no quito un comentario de verdad: %r" % limpio
    )
    assert "x = 1" in limpio, (
        "sin_ruido se llevo por delante el codigo al quitar el comentario: %r" % limpio
    )


def test_dos_cadenas_que_solo_difieren_en_el_numeral_no_se_confunden():
    """Si el numeral esta dentro de comillas, dos lineas distintas deben seguir distintas."""
    uno = r.sin_ruido("a = " + repr("# uno"))
    dos = r.sin_ruido("a = " + repr("# dos"))
    assert uno != dos, (
        "sin_ruido aplano dos lineas que solo difieren dentro de una cadena con numeral: %r"
        % uno
    )


def test_un_trozo_que_no_se_puede_tokenizar_no_revienta_y_quita_el_comentario():
    """Con codigo roto sin_ruido no debe lanzar, y aun asi debe quitar el comentario."""
    roto = "def f(:\n    x = 1  # c"
    limpio = r.sin_ruido(roto)
    assert "# c" not in limpio, (
        "sin_ruido dejo un comentario en un trozo que no se puede tokenizar: %r" % limpio
    )
    assert "x = 1" in limpio, (
        "sin_ruido perdio el codigo de un trozo que no se puede tokenizar: %r" % limpio
    )
