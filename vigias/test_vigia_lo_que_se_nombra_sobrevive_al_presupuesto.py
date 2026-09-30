# -*- coding: utf-8 -*-
"""VIGIA — LO QUE EL PROBLEMA NOMBRA SOBREVIVE AL PRESUPUESTO.

NACE ROJA A PROPOSITO (2026-09-29). La pieza que vigila todavia no existe:

    cerebro/router.py::asegurar_trozo_nombrado(pedazos, pieza, desde, hasta, texto, nombre)

Se escribe en la ronda siguiente. Esta prueba se entrega hoy para que la roja se lea
de un vistazo y para que, cuando la pieza entre, estas comprobaciones se pongan verdes.

PROMESA DE SABOTAJEO: cuando el arreglo entre, quien revise quita la pieza de
cerebro/router.py y comprueba que estas comprobaciones vuelven a rojo. Si siguen
verdes con la pieza quitada, esta vigia no protege nada.

EL CASO DE JULIO (medido en vivo el 2026-09-29 sobre el proyecto de verdad):
  - el problema nombraba la funcion processPhoto, que vive en el renglon 2381;
  - el pedazo 2369-2408 la contenia, con puntaje 19.32;
  - el presupuesto reparte de mayor a menor y tiro ese pedazo por ser grande;
  - el paquete entregado se quedo con 1217-1256, 1185-1224 y 1345-1384;
  - lo que el problema NOMBRA no llego.

La pieza nueva garantiza que lo nombrado sobreviva: si ya hay un pedazo de la MISMA
pieza que contiene esos renglones, le sube el puntaje a 99.0 y le pone la marca; si
no lo hay, agrega al principio un pedazo nuevo con puntaje 99.0 y la marca.

Sin IA, sin red, sin lanzar procesos, sin abrir ningun archivo del proyecto y sin
escribir nada en ninguna parte. Siempre el mismo resultado.
"""
import os
import sys

# Arranque: meter en la ruta de busqueda la carpeta que esta un nivel arriba de
# la carpeta vigias, para poder importar cerebro.router.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cerebro import router  # noqa: E402


# ---------------------------------------------------------------------------
# PRIMER ASSERT: la pieza todavia no esta escrita. La roja de hoy se lee aqui.
# ---------------------------------------------------------------------------
assert hasattr(router, "asegurar_trozo_nombrado"), (
    "FALTA LA PIEZA: cerebro/router.py::asegurar_trozo_nombrado todavia no existe. "
    "Esta vigia nace ROJA a proposito (2026-09-29). La pieza se escribe en la ronda "
    "siguiente y, cuando entre, estas comprobaciones se ponen verdes. Si alguien "
    "quita la pieza y esto sigue verde, la vigia no protege nada."
)


# ---------------------------------------------------------------------------
# Datos de los casos. Todo hecho a mano, sin tocar nada del proyecto.
# ---------------------------------------------------------------------------
PIEZA = "cuerpo/obrero.py"
OTRA_PIEZA = "cerebro/router.py"
DESDE = 2381
HASTA = 2381
TEXTO = "def processPhoto(...): ..."
NOMBRE = "processPhoto"


# ---------------------------------------------------------------------------
# Caso 1: LISTA VACIA.
# ---------------------------------------------------------------------------
def test_lista_vacia_trae_el_pedazo_nombrado():
    salida = router.asegurar_trozo_nombrado([], PIEZA, DESDE, HASTA, TEXTO, NOMBRE)
    assert isinstance(salida, list), "debe devolver una lista"
    assert len(salida) == 1, "con lista vacia debe traer UN pedazo"
    t = salida[0]
    assert t.get("pieza") == PIEZA
    assert t.get("desde") == DESDE
    assert t.get("hasta") == HASTA
    assert t.get("texto") == TEXTO
    assert t.get("puntaje") == 99.0
    assert t.get("_completo") == NOMBRE


# ---------------------------------------------------------------------------
# Caso 2: YA HAY UNO QUE LO CONTIENE, Y ES EL CASO DE JULIO.
# ---------------------------------------------------------------------------
def test_ya_hay_uno_que_lo_contiene_y_es_el_caso_de_julio():
    pedazo = {
        "pieza": PIEZA,
        "desde": 2369,
        "hasta": 2408,
        "texto": "...",
        "puntaje": 19.32,
    }
    salida = router.asegurar_trozo_nombrado(
        [pedazo], PIEZA, DESDE, HASTA, TEXTO, NOMBRE
    )
    assert isinstance(salida, list)
    assert len(salida) == 1, "no se agrega ningun pedazo nuevo"
    t = salida[0]
    assert t is pedazo, "debe ser el mismo pedazo de antes"
    assert t.get("pieza") == PIEZA
    assert t.get("desde") == 2369
    assert t.get("hasta") == 2408
    assert t.get("puntaje") == 99.0, "se le sube el puntaje a 99.0"
    assert t.get("_completo") == NOMBRE, "se le pone la marca con el nombre"


# ---------------------------------------------------------------------------
# Caso 3: EL QUE CONTIENE ES DE OTRA PIEZA.
# ---------------------------------------------------------------------------
def test_el_que_contiene_es_de_otra_pieza_no_cuenta():
    ajeno = {
        "pieza": OTRA_PIEZA,
        "desde": 2369,
        "hasta": 2408,
        "texto": "...",
        "puntaje": 19.32,
    }
    salida = router.asegurar_trozo_nombrado(
        [ajeno], PIEZA, DESDE, HASTA, TEXTO, NOMBRE
    )
    assert isinstance(salida, list)
    assert len(salida) == 2, "debe traer DOS pedazos: el ajeno y el nombrado"
    primero = salida[0]
    assert primero.get("pieza") == PIEZA
    assert primero.get("desde") == DESDE
    assert primero.get("hasta") == HASTA
    assert primero.get("texto") == TEXTO
    assert primero.get("puntaje") == 99.0
    assert primero.get("_completo") == NOMBRE
    assert salida[1] is ajeno, "el ajeno se queda tal cual"


# ---------------------------------------------------------------------------
# Caso 4: SOLO SE SOLAPA A MEDIAS.
# ---------------------------------------------------------------------------
def test_solo_se_solapa_a_medias_no_lo_contiene():
    vecino = {
        "pieza": PIEZA,
        "desde": 2350,
        "hasta": 2375,
        "texto": "...",
        "puntaje": 12.76,
    }
    salida = router.asegurar_trozo_nombrado(
        [vecino], PIEZA, DESDE, HASTA, TEXTO, NOMBRE
    )
    assert isinstance(salida, list)
    assert len(salida) == 2, "como no lo contiene, se agrega el nombrado"
    primero = salida[0]
    assert primero.get("pieza") == PIEZA
    assert primero.get("desde") == DESDE
    assert primero.get("hasta") == HASTA
    assert primero.get("texto") == TEXTO
    assert primero.get("puntaje") == 99.0
    assert primero.get("_completo") == NOMBRE
    assert salida[1] is vecino, "el vecino se queda tal cual"


# ---------------------------------------------------------------------------
# Caso 5: NO REVIENTA CON BASURA.
# ---------------------------------------------------------------------------
def test_no_revienta_con_basura():
    salida = router.asegurar_trozo_nombrado(
        None, PIEZA, DESDE, HASTA, TEXTO, NOMBRE
    )
    assert isinstance(salida, list), "debe devolver una lista aunque le llegue nada"
    assert len(salida) >= 1, "al menos trae el pedazo nombrado"
    t = salida[0]
    assert t.get("pieza") == PIEZA
    assert t.get("desde") == DESDE
    assert t.get("hasta") == HASTA
    assert t.get("texto") == TEXTO
    assert t.get("puntaje") == 99.0
    assert t.get("_completo") == NOMBRE
