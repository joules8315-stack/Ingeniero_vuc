# -*- coding: utf-8 -*-
"""Vigia de texto: el comando equipo aplica la propuesta ENTERA, no un solo trozo.

Julio, 2026-09-21: cuando el equipo aprueba un arreglo que toca VARIOS trozos del mismo
archivo, el comando `equipo` de ingeniero.py tiene que aplicar la propuesta completa.

Si sigue llamando a `aplicador.aplicar_cambio`, ese aplicador solo sabe aplicar UN trozo:
el resto de los trozos del mismo arreglo se quedan fuera, y el equipo paga una ronda nueva
por cada trozo que falto. Es decir: se paga varias veces el mismo arreglo.

Esta vigia es de TEXTO: abre ingeniero.py y comprueba, con assert, dos cosas del comando
equipo:

  1. que YA NO aparece la llamada `_ok, _msg = aplicador.aplicar_cambio(prop, raiz=_raiz)`
  2. que SI aparece la llamada `_ok, _msg = aplicador.aplicar_propuesta(prop, raiz=_raiz)`

No toca ningun otro archivo.
"""

import os


AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
INGENIERO = os.path.join(RAIZ, "ingeniero.py")

# Los dos textos exactos que se buscan en ingeniero.py.
# El viejo: aplica UN solo trozo (aplicar_cambio).
# El nuevo: aplica la propuesta ENTERA (aplicar_propuesta).
TEXTO_VIEJO = "_ok, _msg = aplicador.aplicar_cambio(prop, raiz=_raiz)"
TEXTO_NUEVO = "_ok, _msg = aplicador.aplicar_propuesta(prop, raiz=_raiz)"


def _leer_ingeniero():
    """Devuelve el texto completo de ingeniero.py."""
    with open(INGENIERO, encoding="utf-8") as f:
        return f.read()


def test_el_equipo_ya_no_aplica_un_solo_trozo():
    """El comando equipo NO debe seguir llamando a aplicar_cambio.

    aplicar_cambio solo sabe aplicar UN trozo. Si el arreglo aprobado toca varios trozos
del mismo archivo, los demas se quedan fuera y el equipo tiene que pagar una ronda nueva
por cada trozo que falto. Por eso este texto tiene que haber desaparecido.
    """
    texto = _leer_ingeniero()
    assert TEXTO_VIEJO not in texto, (
        "El comando equipo de ingeniero.py todavia llama a "
        "aplicador.aplicar_cambio, que solo sabe aplicar UN trozo. "
        "Con eso, un arreglo que toca varios trozos del mismo archivo se aplica a medias "
        "y el equipo paga una ronda nueva por cada trozo que falto. "
        "Falta el texto: %r" % TEXTO_VIEJO
    )


def test_el_equipo_aplica_la_propuesta_entera():
    """El comando equipo SI debe llamar a aplicar_propuesta.

    aplicar_propuesta aplica la propuesta ENTERA: todos los trozos del mismo arreglo de
una sola vez. Sin esto, el equipo paga una ronda por cada trozo de un mismo arreglo.
    """
    texto = _leer_ingeniero()
    assert TEXTO_NUEVO in texto, (
        "El comando equipo de ingeniero.py NO llama a "
        "aplicador.aplicar_propuesta. Sin esa llamada, el equipo solo aplica un trozo "
        "y paga una ronda nueva por cada trozo que falto del mismo arreglo. "
        "Falta el texto: %r" % TEXTO_NUEVO
    )


if __name__ == "__main__":
    test_el_equipo_ya_no_aplica_un_solo_trozo()
    test_el_equipo_aplica_la_propuesta_entera()
    print("Vigia verde: el comando equipo aplica la propuesta entera, no un solo trozo.")
