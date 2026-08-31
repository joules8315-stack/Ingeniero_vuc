# -*- coding: utf-8 -*-
"""VIGIA — el obrero repara POR TEXTO y POR NOMBRE, nunca por numero de renglon.

ENCARGO de Claude a Cline (2026-08-31), y es lo que Julio pide desde el principio:
  "Lo que borra todo, que cuenta por lineas, por que no lo reemplazas... si en definitiva no se
   puede buscar por numero, que se elimine esa instruccion y quede buscando por funcion y nombre."

LA MITAD YA ESTA en verde: la busqueda por nombre (piezas.funcion_completa), el repartidor, la ley
y el candado. Falta ESTA mitad: que el propio obrero deje de pedir tramos de lineas en su prompt.

UN TRAMO BORRA LA FUNCION ENTERA (97 a 136 = toda la funcion aunque se cambie una palabra) y los
numeros se corren solos en cuanto alguien anade una linea. El NOMBRE y el TEXTO no se mueven.

NACE ROJA: hoy el obrero todavia pide "lineas": "desde-hasta" y "linea_texto".
No llama a ningun cerebro: mira el texto de las instrucciones que se le dan. Determinista.
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
OBRERO = (AQUI / "cuerpo" / "obrero.py").read_text(encoding="utf-8", errors="replace")


def test_no_pide_tramos_de_lineas():
    """No puede quedar la casilla que pide 'desde-hasta': un tramo borra la funcion entera."""
    assert '"lineas": "desde-hasta"' not in OBRERO, (
        "el obrero todavia pide la casilla 'lineas': 'desde-hasta'. Un tramo (97 a 136) borra la "
        "funcion entera aunque solo hubiera que cambiar una palabra, y los numeros se corren solos.")


def test_no_pide_el_texto_de_UNA_linea():
    """La casilla vieja 'linea_texto' (una sola linea) se reemplaza por el par viejo->nuevo."""
    assert "linea_texto" not in OBRERO, (
        "todavia existe la casilla 'linea_texto' (el texto de una sola linea). Se sustituye por el "
        "par 'texto_viejo' -> 'texto_nuevo'.")


def test_senala_el_sitio_por_NOMBRE():
    """La casilla que dice DONDE esta tiene que ser el nombre de la funcion, no un numero."""
    assert '"funcion"' in OBRERO, (
        "no hay casilla que pida el NOMBRE de la funcion donde esta el cambio. El sitio se senala "
        "por nombre, nunca por numero de renglon.")


def test_da_el_texto_viejo_y_el_nuevo():
    """El cambio se da como 'este texto' -> 'este otro texto', para buscar y reemplazar."""
    assert '"texto_viejo"' in OBRERO, "falta la casilla 'texto_viejo' (el texto que hay AHORA)"
    assert '"texto_nuevo"' in OBRERO, "falta la casilla 'texto_nuevo' (el texto que debe quedar)"


def test_se_conserva_la_frase_copias_el_texto_literal():
    """Otra vigia la exige: sin 'COPIAS el texto literal' no hay texto con que comprobar nada."""
    assert "COPIAS el texto literal" in OBRERO, (
        "desaparecio la frase 'COPIAS el texto literal' que otra vigia exige: hay que conservarla")


def test_la_regla_3_prohibe_los_numeros():
    """Tiene que estar ESCRITO que esta prohibido dar numeros o tramos, con el porque."""
    i = OBRERO.find("3.")
    bloque = OBRERO[i:i + 900].lower() if i > 0 else OBRERO.lower()
    assert "prohibido" in bloque, (
        "la regla 3 no dice EXPRESAMENTE que esta PROHIBIDO dar numeros de renglon o tramos")
    assert "numero" in bloque, "no se menciona el numero de renglon que queda prohibido"


def test_exige_que_el_texto_sea_unico():
    """Si el texto se repite, hay que alargarlo hasta que sea unico: no se toca un sitio equivocado."""
    assert "unico" in OBRERO.lower(), (
        "no se exige que el texto a sustituir sea UNICO en el archivo: si se repite, se alarga "
        "hasta que lo sea. Sin eso, buscar y reemplazar toca el sitio equivocado.")


def test_se_trabaja_con_la_funcion_completa_no_un_pedazo():
    """Julio, 2026-08-31: que busque por funcion, el paquete COMPLETO, no un pedazo.

    La mitad ya esta en verde (piezas.funcion_completa trae la funcion entera). Falta que el obrero
    lo sepa: trabaja con la funcion COMPLETA que le dan, y si el material no la trae entera, la
    pide (NECESITO_LEER) en vez de arreglar a ciegas sobre un pedazo suelto.
    """
    bajo = OBRERO.lower()
    assert "completa" in bajo or "completo" in bajo, (
        "el obrero no dice que trabaja con la funcion/paquete COMPLETO. Un pedazo suelto se repara "
        "mal: falta el contexto de la funcion entera.")
    assert "pedazo" in bajo, (
        "no se avisa que NO se trabaja con un pedazo suelto: sin decirlo, se arregla a ciegas")
    assert "necesito_leer" in bajo, (
        "no se dice que si el material no trae la funcion completa se pide con NECESITO_LEER")
