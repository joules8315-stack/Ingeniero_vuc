import os
import sys


# Arranque: meter en sys.path la carpeta que esta un nivel arriba de la carpeta vigias,
# para poder importar el paquete cuerpo desde este archivo de prueba.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)


# Esta prueba NACE ROJA A PROPOSITO (2026-09-29).
#
# Hoy, cuerpo/obrero.py, funcion _preguntar_con_relevo, toma el MINIMO de las capacidades
# de toda la fila y recorta el encargo a ese tope, aunque el cerebro que de verdad va a
# escribir aguante el triple. Medido tres veces el mismo dia: encargos cortados de 45.226 a
# 15.921 letras, de 34.992 a 15.284, y un tercero que ademas recibio el texto de OTRO
# documento. Las tres vueltas murieron (DUDOSO o descartadas por invento).
#
# El arreglo (ronda siguiente) es una pieza NUEVA llamada tope_del_pasillo, que vivira en
# cuerpo/obrero.py. Recibe UNA lista de numeros (las capacidades de los cerebros de la fila)
# y devuelve UN numero: el tope al que se puede recortar. La regla es que devuelva la
# capacidad MAS GRANDE, no la mas pequena, porque el reparto de mas abajo ya sabe mandar el
# trabajo al que aguanta.
#
# En esta ronda NO se toca cuerpo/obrero.py: la prueba tiene que fallar precisamente porque
# tope_del_pasillo todavia no existe, y quien revise tiene que poder comprobarlo de un
# vistazo. Por eso lo primero es un assert claro sobre su existencia.


def test_el_pasillo_no_corta_al_que_escribe():
    """El tope del pasillo debe ser la capacidad MAS GRANDE de la fila, no la mas chica.

    Si esta prueba falla hoy, es porque la pieza tope_del_pasillo todavia no esta escrita
    en cuerpo/obrero.py. Eso es lo esperado en esta ronda: el arreglo entra despues.
    """
    import cuerpo.obrero as obrero

    assert hasattr(obrero, "tope_del_pasillo"), (
        "FALTA LA PIEZA: cuerpo/obrero.py todavia no tiene tope_del_pasillo. "
        "Esta prueba nace roja a proposito (2026-09-29): el arreglo del pasillo entra en "
        "la ronda siguiente y en esta no se toca cuerpo/obrero.py. "
        "Cuando la pieza exista, esta prueba debe pasar en verde."
    )

    # Caso 1: con la fila [5000, 20000, 60000] el tope tiene que ser 60000.
    # Hoy, sin la pieza, esto ni se ejecuta: el assert de arriba ya corta con un mensaje claro.
    assert obrero.tope_del_pasillo([5000, 20000, 60000]) == 60000, (
        "El pasillo debe cortar a la medida del cerebro MAS GRANDE de la fila (60000), "
        "no a la del mas chico (5000): el reparto de mas abajo ya manda el trabajo al que "
        "aguanta, y recortar antes al mas chico tira material para nada."
    )

    # Caso 2: con un solo cerebro en la fila, el tope es su capacidad.
    assert obrero.tope_del_pasillo([12000]) == 12000, (
        "Con un solo cerebro en la fila, el tope del pasillo debe ser su capacidad (12000)."
    )

    # Caso 3: con la fila vacia, el tope es 0, que significa no recortar nada. No puede reventar.
    assert obrero.tope_del_pasillo([]) == 0, (
        "Con la fila vacia, el tope del pasillo debe ser 0 (no recortar nada) y no puede "
        "reventar con un error de Python."
    )
