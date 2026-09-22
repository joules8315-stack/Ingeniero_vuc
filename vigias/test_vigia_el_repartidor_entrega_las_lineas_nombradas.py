# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_repartidor_entrega_las_lineas_nombradas.py

VIGIA: EL REPARTIDOR ENTREGA LAS LINEAS NOMBRADAS.

Vigila una funcion NUEVA de cerebro/router.py:

    tramos_nombrados(problema) -> [(desde, hasta), ...]

Devuelve la lista de tramos de lineas que el texto del problema nombra. Es la pieza que
faltaba: el repartidor sabia hablar de tramos, pero no tenia forma de pedir POR SU NOMBRE
las lineas que el encargo nombra, y por eso se escribian numeros a mano que se corrian solos
(fallo real: los numeros 87 y 227 dentro de armar()).

Lo que comprueba esta vigia:
  1. una linea suelta se entrega como tramo de un solo renglon;
  2. un rango "de la 351 a la 356" se entrega como (351, 356);
  3. varias lineas sueltas se entregan cada una como su propio tramo;
  4. un texto sin numeros no inventa tramos: devuelve lista vacia;
  5. el propio cerebro/router.py usa tramos_nombrados(problema) dentro del bloque que
     empieza con el comentario LO QUE EL PROBLEMA NOMBRA, ENTRA SU PEDAZO, y ese bloque NO
     define la funcion tramos_nombrados.

No toca ningun otro archivo. Solo lee.
"""
import os

from cerebro import router


AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ROUTER = os.path.join(AQUI, "cerebro", "router.py")


def _texto_router():
    """Devuelve el texto entero de cerebro/router.py, o cadena vacia si no se puede leer."""
    try:
        with open(RUTA_ROUTER, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def test_una_linea_suelta():
    assert router.tramos_nombrados("cambia la linea 1142") == [(1142, 1142)]


def test_un_rango_de_lineas():
    tramos = router.tramos_nombrados("las lineas 351 a 356 y la 634")
    assert (351, 356) in tramos


def test_varias_lineas_sueltas():
    tramos = router.tramos_nombrados("lineas 1142 y 1174")
    assert (1142, 1142) in tramos
    assert (1174, 1174) in tramos


def test_sin_numeros_no_inventa():
    assert router.tramos_nombrados("sin numeros") == []


def test_el_router_usa_la_funcion_en_su_bloque():
    texto = _texto_router()
    assert texto, "no se pudo leer cerebro/router.py"
    marca = "LO QUE EL PROBLEMA NOMBRA, ENTRA SU PEDAZO"
    pos = texto.find(marca)
    assert pos != -1, "no aparece el comentario %r en cerebro/router.py" % marca
    bloque = texto[pos:]
    assert "tramos_nombrados(problema)" in bloque, (
        "el bloque que empieza con %r no llama a tramos_nombrados(problema)" % marca)


if __name__ == "__main__":
    test_una_linea_suelta()
    test_un_rango_de_lineas()
    test_varias_lineas_sueltas()
    test_sin_numeros_no_inventa()
    test_el_router_usa_la_funcion_en_su_bloque()
    print("VIGIA OK: el repartidor entrega las lineas nombradas")
