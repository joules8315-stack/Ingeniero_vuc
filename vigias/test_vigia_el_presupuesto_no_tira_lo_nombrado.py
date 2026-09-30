# -*- coding: utf-8 -*-
"""Vigia: el reparto del presupuesto NO puede tirar lo que el problema NOMBRA.

NACE ROJA A PROPOSITO (2026-09-29).

Julio lo dijo asi hoy: "el fallo importante, que es, que no encuentra la pieza
por funsion, no se ha reparado". Es la ultima capa: el pedazo que trae lo que el
problema NOMBRA ya llega marcado y con prioridad, y aun asi el reparto del
presupuesto lo TIRA por ser grande, y en su lugar mete pedazos que nadie pidio.

Medido en vivo hoy 2026-09-29 sobre el proyecto de verdad. Los pedazos que llegan
al reparto, con su puntaje y su tamano en letras, son:

    1217-1256  puntaje 99.0   tamano  6.393  MARCADO captureDesktopPhoto
    1185-1224  puntaje 21.55  tamano  9.023  sin marca
    2369-2408  puntaje 99.0   tamano 14.652  MARCADO processPhoto
    1345-1384  puntaje 12.76  tamano  2.842  sin marca

El tope del reparto son 19.000 letras. La cuenta medida: entra el primero marcado
y quedan 12.607; el segundo marcado mide 14.652 y NO cabe, asi que se tira; y
despues si caben dos pedazos SIN marca de 9.023 y 2.842. Lo entregado fue
1217-1256, 1185-1224 y 1345-1384. O sea que se tiro lo pedido para meter lo que
nadie pidio.

LO QUE VA A CAMBIAR EN LA RONDA SIGUIENTE (para que esta prueba lo mida):
  - los pedazos MARCADOS no se tiran nunca, aunque no quepan;
  - los que no estan marcados siguen entrando solo si caben, igual que hoy;
  - la lista devuelta sigue quedando ordenada de mayor a menor puntaje, como hoy.

Sin IA, sin red, sin lanzar procesos. Determinista.
"""

import os
import sys

# Arranque: meter en la ruta de busqueda la carpeta que esta un nivel arriba de
# la carpeta vigias, a partir de la ruta de este mismo archivo de prueba.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cerebro.router import recortar_por_presupuesto  # noqa: E402


# ---------------------------------------------------------------------------
# Utilidades de montaje: pedazos de mentira hechos a mano.
# ---------------------------------------------------------------------------

def _texto_de(tamano):
    """Fabrica un texto que mide EXACTAMENTE `tamano` letras."""
    return "x" * tamano


def _pedazo(texto, puntaje, marca=None):
    """Arma un pedazo de mentira con su texto, su puntaje y, si toca, su marca.

    La marca de lo nombrado se llama, exactamente, `_completo` y trae dentro el
    nombre que el problema nombro. La otra marca igual de fuerte se llama
    `_nombrado` y se usa para los archivos que el problema nombra.
    """
    pedazo = {"texto": texto, "puntaje": puntaje}
    if marca is not None:
        pedazo["_completo"] = marca
    return pedazo


def _tamanos(pedazos):
    """Devuelve la lista de tamanos de texto de los pedazos, en orden."""
    return [len(p["texto"]) for p in pedazos]


def _puntajes(pedazos):
    """Devuelve la lista de puntajes de los pedazos, en orden."""
    return [p["puntaje"] for p in pedazos]


def _esta_ordenado_de_mayor_a_menor(pedazos):
    """True si los puntajes van de mayor a menor (no creciente)."""
    puntajes = _puntajes(pedazos)
    return all(puntajes[i] >= puntajes[i + 1] for i in range(len(puntajes) - 1))


# ---------------------------------------------------------------------------
# CASO 1 — EL CASO MEDIDO DE JULIO. NACE ROJO.
# ---------------------------------------------------------------------------

def test_caso_medido_de_julio_no_tira_lo_nombrado():
    """Los DOS pedazos marcados tienen que sobrevivir al reparto con tope 19000.

    Hoy solo sobrevive el primero (6.393 letras) y el segundo marcado
    (processPhoto, 14.652 letras) se tira para meter dos pedazos SIN marca.
    Por eso esta prueba nace roja.
    """
    pedazos = [
        _pedazo(_texto_de(6393), 99.0, marca="captureDesktopPhoto"),
        _pedazo(_texto_de(9023), 21.55),
        _pedazo(_texto_de(14652), 99.0, marca="processPhoto"),
        _pedazo(_texto_de(2842), 12.76),
    ]

    devueltos = recortar_por_presupuesto(pedazos, 19000)

    tamanos = _tamanos(devueltos)
    assert 6393 in tamanos, (
        "El reparto tiro el pedazo marcado captureDesktopPhoto (6.393 letras). "
        "Hoy se tira lo que el problema nombra para meter lo que nadie pidio, "
        "y por eso la vuelta se pierde entera."
    )
    assert 14652 in tamanos, (
        "El reparto tiro el pedazo marcado processPhoto (14.652 letras) porque "
        "no cabia, y en su lugar metio pedazos SIN marca (9.023 y 2.842). "
        "Hoy se tira lo que el problema nombra para meter lo que nadie pidio, "
        "y por eso la vuelta se pierde entera."
    )
    assert _esta_ordenado_de_mayor_a_menor(devueltos), (
        "La lista devuelta tiene que quedar ordenada de mayor a menor puntaje."
    )


# ---------------------------------------------------------------------------
# CASO 2 — LOS QUE NO ESTAN MARCADOS SIGUEN CABIENDO CUANDO HAY SITIO.
# Ya esta verde hoy; tiene que seguir verde.
# ---------------------------------------------------------------------------

def test_sin_marca_caben_cuando_hay_sitio():
    """Un marcado pequeno y dos sin marca pequenos: con tope de sobra, entran los tres."""
    pedazos = [
        _pedazo(_texto_de(1000), 90.0, marca="funcionPedida"),
        _pedazo(_texto_de(800), 50.0),
        _pedazo(_texto_de(600), 30.0),
    ]

    devueltos = recortar_por_presupuesto(pedazos, 10000)

    tamanos = _tamanos(devueltos)
    assert 1000 in tamanos, "El pedazo marcado pequeno tiene que entrar."
    assert 800 in tamanos, "El pedazo sin marca de 800 tiene que entrar: hay sitio."
    assert 600 in tamanos, "El pedazo sin marca de 600 tiene que entrar: hay sitio."
    assert _esta_ordenado_de_mayor_a_menor(devueltos), (
        "La lista devuelta tiene que quedar ordenada de mayor a menor puntaje."
    )


# ---------------------------------------------------------------------------
# CASO 3 — LOS QUE NO ESTAN MARCADOS NO SE CUELAN CUANDO NO HAY SITIO.
# Ya esta verde hoy; tiene que seguir verde.
# ---------------------------------------------------------------------------

def test_sin_marca_no_se_cuelan_cuando_no_hay_sitio():
    """Un marcado cuyo texto ya llena el tope el solo: los sin marca no entran."""
    pedazos = [
        _pedazo(_texto_de(5000), 90.0, marca="funcionPedida"),
        _pedazo(_texto_de(3000), 50.0),
        _pedazo(_texto_de(2000), 30.0),
    ]

    devueltos = recortar_por_presupuesto(pedazos, 5000)

    tamanos = _tamanos(devueltos)
    assert 5000 in tamanos, "El pedazo marcado tiene que entrar."
    assert 3000 not in tamanos, (
        "El pedazo sin marca de 3000 no cabe: no se puede colar."
    )
    assert 2000 not in tamanos, (
        "El pedazo sin marca de 2000 no cabe: no se puede colar."
    )
    assert _esta_ordenado_de_mayor_a_menor(devueltos), (
        "La lista devuelta tiene que quedar ordenada de mayor a menor puntaje."
    )


# ---------------------------------------------------------------------------
# CASO 4 — SIN NINGUN MARCADO SE PORTA COMO HOY.
# Ya esta verde hoy; tiene que seguir verde.
# ---------------------------------------------------------------------------

def test_sin_ningun_marcado_se_porta_como_hoy():
    """Tres sin marca donde el de mayor puntaje ya pasa del tope el solo: entra ese."""
    pedazos = [
        _pedazo(_texto_de(9000), 90.0),
        _pedazo(_texto_de(3000), 50.0),
        _pedazo(_texto_de(2000), 30.0),
    ]

    devueltos = recortar_por_presupuesto(pedazos, 5000)

    tamanos = _tamanos(devueltos)
    assert 9000 in tamanos, (
        "El de mayor puntaje se queda siempre aunque el solo pase del tope."
    )
    assert 3000 not in tamanos, "El de 3000 no cabe despues del de 9000."
    assert 2000 not in tamanos, "El de 2000 no cabe despues del de 9000."
    assert _esta_ordenado_de_mayor_a_menor(devueltos), (
        "La lista devuelta tiene que quedar ordenada de mayor a menor puntaje."
    )
