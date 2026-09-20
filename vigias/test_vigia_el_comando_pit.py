# -*- coding: utf-8 -*-
"""VIGIA: el subcomando `pit` tiene que existir en ingeniero.py.

Julio, 2026-09-20.

El paso 3 del metodo (mapa de IA contra programacion) se ejecuta con
`python ingeniero.py pit <proyecto>`. Ese subcomando es el que arranca el bucle
del capataz (cuerpo/capataz.py::bucle) y sin el, el pit no arranca solo y todo
el paso 3 se queda en el papel.

Esta vigia abre ingeniero.py y afirma dos cosas sobre su TEXTO:

  1. que nombra el subcomando `pit` (la rama `cmd == "pit"`),
  2. que nombra la funcion `bucle` (la que llama el capataz).

No ejecuta ingeniero.py: solo mira su texto. Es una vigia de contrato, no de
comportamiento. Si alguien renombra el subcomando o deja de llamar a `bucle`,
esta vigia se pone roja y avisa.
"""

import os
import re


# La ruta de ingeniero.py se calcula desde este archivo: la vigia vive en
# <raiz>/vigias/ y el mando en <raiz>/ingeniero.py. Asi no depende de donde se
# corra pytest.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
INGENIERO = os.path.join(RAIZ, "ingeniero.py")


# El mensaje de fallo, en espanol y con el porque. Sin ese subcomando el pit no
# arranca solo y todo el paso 3 se queda en el papel.
MENSAJE_SIN_PIT = (
    "FALLO: ingeniero.py no tiene el subcomando 'pit'. "
    "Sin ese subcomando el pit no arranca solo y todo el paso 3 se queda en el papel. "
    "Se esperaba encontrar en ingeniero.py una rama del tipo: "
    "if cmd == \"pit\" ... que llame a cuerpo.capataz.bucle."
)

MENSAJE_SIN_BUCLE = (
    "FALLO: ingeniero.py no nombra la funcion 'bucle'. "
    "Sin ese subcomando el pit no arranca solo y todo el paso 3 se queda en el papel. "
    "Se esperaba encontrar en ingeniero.py una llamada del tipo: "
    "from cuerpo import capataz as _cap ... _cap.bucle(...)."
)


def _leer_ingeniero():
    """Devuelve el texto de ingeniero.py, o None si no se puede leer."""
    if not os.path.isfile(INGENIERO):
        return None
    with open(INGENIERO, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def test_ingeniero_py_existe():
    """Sin ingeniero.py no hay mando unico: la vigia no puede opinar de nada."""
    assert os.path.isfile(INGENIERO), (
        "FALLO: no se encuentra ingeniero.py en %s. "
        "Sin ese subcomando el pit no arranca solo y todo el paso 3 se queda en el papel."
        % INGENIERO
    )


def test_ingeniero_nombra_el_subcomando_pit():
    """ingeniero.py tiene que nombrar el subcomando `pit`.

    Se busca la rama del despachador: `cmd == "pit"` (o con comillas simples).
    No vale que la palabra 'pit' aparezca suelta en un comentario: tiene que
    estar como comparacion del comando.
    """
    texto = _leer_ingeniero()
    assert texto is not None, MENSAJE_SIN_PIT

    # La rama real del despachador: cmd == "pit"  o  cmd == 'pit'
    patron = re.compile(r'cmd\s*==\s*["\']pit["\']')
    assert patron.search(texto), MENSAJE_SIN_PIT


def test_ingeniero_nombra_la_funcion_bucle():
    """ingeniero.py tiene que nombrar la funcion `bucle`.

    El subcomando `pit` delega en cuerpo.capataz.bucle. Si el mando deja de
    nombrar `bucle`, el pit no arranca solo y el paso 3 se queda en el papel.
    """
    texto = _leer_ingeniero()
    assert texto is not None, MENSAJE_SIN_BUCLE

    # La llamada real: _cap.bucle(...)  o  capataz.bucle(...)  o  bucle(...)
    patron = re.compile(r'\bbucle\s*\(')
    assert patron.search(texto), MENSAJE_SIN_BUCLE


def test_el_subcomando_pit_llama_a_bucle():
    """Las dos cosas juntas: el subcomando `pit` y la funcion `bucle`.

    Esta es la afirmacion fuerte: no basta con que cada nombre aparezca por
    separado en cualquier parte del archivo. Tiene que haber una rama
    `cmd == "pit"` que llame a `bucle`. Si no, el pit no arranca solo y todo el
    paso 3 se queda en el papel.
    """
    texto = _leer_ingeniero()
    assert texto is not None, MENSAJE_SIN_PIT

    # Se busca la rama del pit y, dentro de su bloque, la llamada a bucle.
    # El bloque del pit es corto (una o dos lineas): se mira desde la rama
    # hasta la siguiente rama `if cmd ==` o hasta 400 caracteres, lo que llegue
    # antes. Asi no se confunde con otras ramas del despachador.
    patron_rama = re.compile(r'cmd\s*==\s*["\']pit["\']')
    m = patron_rama.search(texto)
    assert m, MENSAJE_SIN_PIT

    desde = m.end()
    resto = texto[desde:desde + 400]
    # Se corta en la siguiente rama del despachador, si la hay.
    siguiente = re.search(r'\n\s*if\s+cmd\s*==', resto)
    if siguiente:
        resto = resto[:siguiente.start()]

    assert re.search(r'\bbucle\s*\(', resto), (
        "FALLO: la rama del subcomando 'pit' en ingeniero.py no llama a 'bucle'. "
        "Sin ese subcomando el pit no arranca solo y todo el paso 3 se queda en el papel. "
        "Se esperaba algo como: from cuerpo import capataz as _cap ... return _cap.bucle(...)."
    )
