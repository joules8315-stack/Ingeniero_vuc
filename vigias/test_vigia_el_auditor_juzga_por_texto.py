# -*- coding: utf-8 -*-
"""VIGIA — el auditor juzga la ubicacion POR EL TEXTO, nunca por el numero de linea.

FALLO MEDIDO el 2026-08-28, y costo OCHO rondas de equipo en un solo dia:
  La regla 6 del auditor decia que si el numero de linea y el texto no concuerdan es un error de
  ubicacion y hay que RECHAZAR. El problema es que el numero es la parte FRAGIL:
    · el obrero cuenta sobre el material que le llega y el auditor sobre otro recorte, asi que
      cuentan desde sitios distintos y casi nunca coinciden;
    · en cuanto alguien anade una linea, todos los numeros de abajo se corren.
  El TEXTO en cambio no se confunde: o esta en el material o no esta.

  Rechazos reales de ese dia por esta causa: "dice linea 37 pero es la 39", "declara 97-136 pero
  el codigo solo cubre hasta 51", "las lineas 113-117 no aparecen en los recortes". Ninguno tenia
  que ver con la reparacion pedida. Cada uno fue una ronda de Julio pagada para nada.

ESTA VIGIA NACE ROJA. No llama a ningun cerebro: mira el texto de las instrucciones que se les da.
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
OBRERO = (AQUI / "cuerpo" / "obrero.py").read_text(encoding="utf-8", errors="replace")


def _sin_acentos(t):
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")):
        t = t.replace(a, b)
    return t


def _regla_6():
    """El bloque de la regla 6 dentro de las instrucciones del auditor."""
    i = OBRERO.find("6. COMPRUEBA")
    if i < 0:
        i = OBRERO.find("6. ")
    assert i > 0, "no existe la regla 6 en las instrucciones del auditor"
    fin = OBRERO.find("\nResponde SOLO JSON", i)
    return _sin_acentos(OBRERO[i:fin if fin > i else i + 900].lower())


def test_el_numero_de_linea_NO_es_motivo_de_rechazo():
    """EL FALLO EXACTO: ocho rondas rechazadas por contar, no por reparar."""
    r = _regla_6()
    assert "no es motivo de rechazo" in r, (
        "la regla 6 no dice EXPRESAMENTE que un numero que no cuadra NO basta para rechazar. "
        "Mientras no lo diga, el auditor seguira tumbando reparaciones correctas por contar mal, "
        "y cada una es una ronda de Julio pagada para nada")


def test_la_ubicacion_se_juzga_por_el_TEXTO():
    r = _regla_6()
    assert "por el texto" in r, "la regla 6 no dice que la ubicacion se juzgue por el texto"


def test_se_dice_que_el_numero_es_ORIENTATIVO():
    r = _regla_6()
    assert "orientativo" in r, (
        "no se aclara que el numero es solo orientativo, y sin esa palabra el auditor lo sigue "
        "tratando como una prueba")


def test_se_explica_POR_QUE_el_numero_falla():
    """Sin el porque, el siguiente que lea esto lo 'arregla' y volvemos al punto de partida."""
    r = _regla_6()
    assert "se corre" in r or "se corren" in r, (
        "no se explica que al anadir una linea todos los numeros de abajo se corren. Un candado "
        "sin su razon escrita se deshace en cuanto alguien lo toca")


def test_SI_se_rechaza_cuando_el_texto_NO_esta_en_el_material():
    """No se afloja nada: si el texto no aparece, eso SI es inventar y se rechaza."""
    r = _regla_6()
    assert ("no aparece" in r or "no esta en el material" in r), (
        "ya no se dice cuando SI hay que rechazar por ubicacion. Si el texto no aparece en el "
        "material, el obrero se lo invento, y eso sigue siendo el fallo mas grave")


def test_la_regla_1_sigue_intacta():
    """Rechazar lo inventado es la regla que de verdad protege. No se toca."""
    bajo = _sin_acentos(OBRERO.lower())
    assert "1. invento algo?" in bajo, (
        "desaparecio la regla 1: rechazar lo inventado es el fallo mas grave y no se puede perder "
        "al arreglar la 6")


def test_el_obrero_repara_por_NOMBRE_y_por_texto_viejo_a_nuevo():
    """La mitad que faltaba (Julio, 2026-08-31): el obrero ya no da tramos, da NOMBRE y TEXTO.

    Se actualizo al contrato nuevo y pide MAS, no menos: antes era el texto de una sola linea
    (linea_texto); ahora tiene que dar el NOMBRE de la funcion y el par texto_viejo -> texto_nuevo,
    y esta PROHIBIDO dar numeros de renglon (un tramo borra la funcion entera y se corre solo).
    Ademas trabaja con la funcion COMPLETA, no un pedazo.
    """
    assert "linea_texto" not in OBRERO, (
        "el obrero todavia pide la casilla vieja 'linea_texto'; se reemplazo por funcion + "
        "texto_viejo + texto_nuevo")
    assert '"funcion"' in OBRERO, (
        "el obrero no pide el NOMBRE de la funcion donde esta el cambio: sin nombre, se cae en "
        "numeros de renglon, y esos se corren solos")
    assert '"texto_viejo"' in OBRERO and '"texto_nuevo"' in OBRERO, (
        "el obrero no pide el par texto_viejo -> texto_nuevo: sin eso no queda texto con que "
        "comprobar la ubicacion")
    assert "PROHIBIDO" in OBRERO, (
        "no esta escrito que esta PROHIBIDO dar numeros de renglon: un tramo borra la funcion entera")
    assert '"lineas": "desde-hasta"' not in OBRERO, (
        "el obrero todavia pide tramos de lineas; se elimino esa instruccion")
    assert "COMPLETA" in OBRERO or "completa" in OBRERO, (
        "el obrero no dice que trabaja con la funcion COMPLETA, no un pedazo (Julio, 2026-08-31)")
