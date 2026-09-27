# -*- coding: utf-8 -*-
"""VIGIA: el paquete trae el archivo nombrado en la frase.

Objetivo (medible): cuando la frase del problema nombra una ruta de archivo que EXISTE en el
proyecto, esa ruta tiene que entrar en el paquete SIEMPRE, sin que influya lo larga que sea la
frase. La comparacion es con la RUTA COMPLETA (con barras normales), no con el nombre suelto,
para que no valga otro archivo que se llame igual.

Medido el 2026-09-27: con una frase LARGA que nombraba una ruta que existe, el paquete no la
traia ni entre las piezas; con la misma peticion CORTA y empezando por la ruta, si la traia.

Esta vigia NACE ROJA a proposito: la prueba va antes de la reparacion. No llama a ninguna IA,
no escribe nada en el proyecto ni en la memoria de verdad: solo llama a armar con el apodo
'ingeniero' y mira lo que devuelve.

Tres casos y nada mas:
  1. frase LARGA que nombra cuerpo/cuotas.py  -> alguna ficha tiene id == 'cuerpo/cuotas.py'
  2. frase CORTA que nombra cuerpo/cuotas.py  -> alguna ficha tiene id == 'cuerpo/cuotas.py'
  3. ruta que NO existe                       -> ninguna ficha la trae y no se inventa nada
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cerebro.router import armar  # noqa: E402


# La ruta que se usa en los casos 1 y 2: codigo normal del proyecto, no un archivo de pruebas.
RUTA_QUE_EXISTE = "cuerpo/cuotas.py"

# Una ruta que NO existe en el proyecto, para el caso 3.
RUTA_QUE_NO_EXISTE = "cuerpo/no_existe_jamas_esta_ruta.py"

# Frase CORTA: empieza por la ruta, como la que SI traia el archivo (medido 2026-09-27).
FRASE_CORTA = RUTA_QUE_EXISTE + " no respeta el orden de relevo de cerebros"

# Frase LARGA: nombra la misma ruta pero enterrada en medio de mucho texto.
# Es la que NO traia el archivo (medido 2026-09-27).
FRASE_LARGA = (
    "Buenos dias, necesito que revises con calma un asunto que lleva dandome vueltas "
    "desde hace varias semanas y que afecta a la forma en que el sistema reparte el trabajo "
    "entre los cerebros disponibles, porque resulta que cuando uno se agota no vuelve a "
    "intentarse aunque ya se haya repuesto, y eso hace que se desperdicie cupo gratis y que "
    "todo acabe recayendo sobre el mismo cerebro de siempre, con el gasto que eso supone y "
    "con el retraso que arrastra para todos los encargos pendientes, asi que te pido por "
    "favor que mires el archivo " + RUTA_QUE_EXISTE + " y me digas que le pasa y como se "
    "arregla, sin tocar nada mas y sin romper a los vecinos que dependen de el, gracias."
)


def _ids_de_fichas(paquete):
    """Devuelve la lista de claves 'id' de las fichas del paquete.

    Cada ficha es un diccionario y su clave 'id' es la RUTA RELATIVA del archivo dentro del
    proyecto, con barras normales. Se normalizan las barras por si el sistema anfitrion usa
    otra cosa, para comparar siempre con la ruta completa.
    """
    fichas = paquete.get("fichas") or []
    ids = []
    for ficha in fichas:
        if isinstance(ficha, dict):
            valor = ficha.get("id")
        else:
            valor = getattr(ficha, "id", None)
        if valor is None:
            continue
        ids.append(str(valor).replace("\\", "/"))
    return ids


def test_caso_1_frase_larga_que_nombra_la_ruta_la_trae():
    """Caso 1: frase LARGA que nombra cuerpo/cuotas.py -> alguna ficha tiene ese id exacto."""
    paquete = armar("ingeniero", FRASE_LARGA)
    ids = _ids_de_fichas(paquete)
    assert RUTA_QUE_EXISTE in ids, (
        "la frase larga nombraba %r y el paquete no trae ninguna ficha con esa ruta; "
        "fichas traidas: %r" % (RUTA_QUE_EXISTE, ids)
    )


def test_caso_2_frase_corta_que_nombra_la_ruta_la_trae():
    """Caso 2: frase CORTA que nombra cuerpo/cuotas.py -> alguna ficha tiene ese id exacto."""
    paquete = armar("ingeniero", FRASE_CORTA)
    ids = _ids_de_fichas(paquete)
    assert RUTA_QUE_EXISTE in ids, (
        "la frase corta nombraba %r y el paquete no trae ninguna ficha con esa ruta; "
        "fichas traidas: %r" % (RUTA_QUE_EXISTE, ids)
    )


def test_caso_3_ruta_que_no_existe_no_se_inventa():
    """Caso 3: ruta que NO existe -> ninguna ficha la trae y no se inventa nada."""
    paquete = armar("ingeniero", "revisa " + RUTA_QUE_NO_EXISTE + " por favor")
    ids = _ids_de_fichas(paquete)
    assert RUTA_QUE_NO_EXISTE not in ids, (
        "la ruta %r no existe en el proyecto y el paquete la trae como ficha: se la invento; "
        "fichas traidas: %r" % (RUTA_QUE_NO_EXISTE, ids)
    )


if __name__ == "__main__":
    sys.exit(pytest.main([os.path.abspath(__file__), "-q"]))
