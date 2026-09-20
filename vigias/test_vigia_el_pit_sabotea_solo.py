"""VIGIA: EL PIT SABOTEA SOLO.

Despues de cada cambio, alguien corre a mano el sabotaje por programa para
comprobar que la vigia de verdad protege. Eso es mecanico y lo tiene que hacer
el pit solo (orden A-39 punto 2 de Julio, del 2026-09-20).

Esta vigia nace ROJA porque cuerpo/capataz.py todavia no sabe hacerlo: no
existe sabotear_la_orden. Cuando exista, esta vigia comprobara que:

  1. Con un sabotaje que sale bien (codigo 0), la orden se aprueba (ok=True) y
     se corrio UNA sola vez, mencionando tanto la vigia como el sabotaje.
  2. Con un sabotaje que sale mal (codigo 1), la orden NO se aprueba (ok=False)
     y trae una razon de texto no vacia.
  3. Con una orden VACIA, sin sabotaje ninguno, no se aprueba ni se suspende:
     ok=None, porque no hay nada que correr.

Sin correr el sabotaje nadie sabe si la vigia de verdad protege, y la prueba
puede estar verde por la razon equivocada.
"""

import os
import sys


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARNES = os.path.join(RAIZ, 'arnes')
for carpeta in (RAIZ, ARNES):
    if carpeta not in sys.path:
        sys.path.insert(0, carpeta)

from cuerpo import capataz  # noqa: E402


def test_con_sabotaje_que_sale_bien_la_orden_se_aprueba(monkeypatch):
    """Si el sabotaje sale bien, la orden se aprueba y se corrio una sola vez."""
    llamadas = []

    def correr_orden_del_sistema_falso(palabras):
        llamadas.append(list(palabras))
        return 0

    monkeypatch.setattr(
        capataz,
        'correr_orden_del_sistema',
        correr_orden_del_sistema_falso,
        raising=False,
    )

    orden = {
        'vigia': 'vigias/loquesea.py',
        'sabotaje': 'memoria/sabotajes/loquesea.json',
    }
    resultado = capataz.sabotear_la_orden(orden)

    assert isinstance(resultado, dict), (
        'sabotear_la_orden tiene que devolver un diccionario, y devolvio: '
        + repr(resultado)
    )
    assert resultado.get('ok') is True, (
        'Con un sabotaje que sale bien (codigo 0), la orden tiene que quedar '
        'aprobada (ok=True). Sin correr el sabotaje nadie sabe si la vigia de '
        'verdad protege, y la prueba puede estar verde por la razon equivocada. '
        'Devolvio: ' + repr(resultado)
    )
    assert len(llamadas) == 1, (
        'El sabotaje se tiene que correr UNA sola vez por orden. Se corrio '
        + str(len(llamadas)) + ' veces. Sin correr el sabotaje nadie sabe si '
        'la vigia de verdad protege, y la prueba puede estar verde por la '
        'razon equivocada.'
    )
    palabras = llamadas[0]
    texto = ' '.join(str(p) for p in palabras)
    assert 'vigias/loquesea.py' in texto, (
        'La llamada al sabotaje tiene que mencionar la vigia '
        'vigias/loquesea.py. Sin correr el sabotaje nadie sabe si la vigia de '
        'verdad protege, y la prueba puede estar verde por la razon equivocada. '
        'Se paso: ' + repr(palabras)
    )
    assert 'memoria/sabotajes/loquesea.json' in texto, (
        'La llamada al sabotaje tiene que mencionar el sabotaje '
        'memoria/sabotajes/loquesea.json. Sin correr el sabotaje nadie sabe si '
        'la vigia de verdad protege, y la prueba puede estar verde por la '
        'razon equivocada. Se paso: ' + repr(palabras)
    )


def test_con_sabotaje_que_sale_mal_la_orden_no_se_aprueba(monkeypatch):
    """Si el sabotaje sale mal, la orden no se aprueba y trae una razon."""
    llamadas = []

    def correr_orden_del_sistema_falso(palabras):
        llamadas.append(list(palabras))
        return 1

    monkeypatch.setattr(
        capataz,
        'correr_orden_del_sistema',
        correr_orden_del_sistema_falso,
        raising=False,
    )

    orden = {
        'vigia': 'vigias/loquesea.py',
        'sabotaje': 'memoria/sabotajes/loquesea.json',
    }
    resultado = capataz.sabotear_la_orden(orden)

    assert isinstance(resultado, dict), (
        'sabotear_la_orden tiene que devolver un diccionario, y devolvio: '
        + repr(resultado)
    )
    assert resultado.get('ok') is False, (
        'Con un sabotaje que sale mal (codigo 1), la orden NO se puede aprobar: '
        'ok tiene que ser False. Devolvio: ' + repr(resultado)
    )
    razon = resultado.get('razon')
    assert isinstance(razon, str) and razon.strip() != '', (
        'Cuando el sabotaje sale mal, la orden tiene que traer una razon de '
        'texto no vacia para que se sepa por que no se aprueba. Devolvio: '
        + repr(resultado)
    )


def test_orden_sin_sabotaje_no_se_aprueba_ni_se_suspende():
    """Una orden sin lista de sabotaje no se aprueba ni se suspende: ok=None."""
    resultado = capataz.sabotear_la_orden({})

    assert isinstance(resultado, dict), (
        'sabotear_la_orden tiene que devolver un diccionario, y devolvio: '
        + repr(resultado)
    )
    assert resultado.get('ok') is None, (
        'Una orden sin lista de sabotaje no se aprueba ni se suspende: '
        'simplemente no hay nada que correr, asi que ok tiene que ser None. '
        'Devolvio: ' + repr(resultado)
    )
