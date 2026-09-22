# -*- coding: utf-8 -*-
"""Vigia: a Big Pickle se le espera lo que tarda.

Vigila cuerpo/cuotas.py::espera_de_bigpickle(letras).

Que se vigila, en palabras llanas:
  · Si no hay ninguna fila apuntada, se espera el valor por defecto (600 s).
  · Si hay filas buenas, se usa su record por 1.5.
  · Las filas de OTRO cerebro no cuentan.
  · Las filas con resultado=ERROR no cuentan.
  · Si hay tareas PARECIDAS (entre la mitad y el doble de letras), se usa lo que tardaron
    esas, no el record global.
  · Nunca se espera menos de 60 s.

El cuaderno ya viene aislado por vigias/conftest.py (INGENIERO_CUADERNO_TEST), asi que
estas pruebas no ensucian el cuaderno de verdad.
"""

from cuerpo import cuotas
from cuerpo import cuaderno


# ---------------------------------------------------------------------------
# Ayudantes de la propia vigia
# ---------------------------------------------------------------------------

def _apuntar_bigpickle(tamano, segundos, resultado=None):
    """Apunta una fila BUENA de bigpickle en el cuaderno de pruebas.

    Si no se dice otra cosa, el resultado es cuaderno.OK.
    """
    if resultado is None:
        resultado = cuaderno.OK
    cuaderno.apuntar(
        "bigpickle",
        tamano=tamano,
        clase="auditar",
        resultado=resultado,
        segundos=segundos,
    )


def _apuntar_otro_cerebro(quien, tamano, segundos, resultado=None):
    """Apunta una fila de OTRO cerebro, para probar que no se cuela en la cuenta."""
    if resultado is None:
        resultado = cuaderno.OK
    cuaderno.apuntar(
        quien,
        tamano=tamano,
        clase="auditar",
        resultado=resultado,
        segundos=segundos,
    )


# ---------------------------------------------------------------------------
# (1) Sin ninguna fila: el valor por defecto
# ---------------------------------------------------------------------------

def test_sin_filas_se_espera_el_valor_por_defecto():
    """Sin nada apuntado, espera_de_bigpickle(1000) vale 600."""
    esperado = cuotas.espera_de_bigpickle(1000)
    assert esperado == 600, (
        "sin filas apuntadas se esperaba 600 y salio %r" % (esperado,)
    )


# ---------------------------------------------------------------------------
# (2) Con dos filas buenas: su record por 1.5
# ---------------------------------------------------------------------------

def test_con_dos_filas_buenas_usa_su_record_por_uno_y_medio():
    """Con 100 s y 328 s (tamano 0), espera_de_bigpickle(1000) esta entre 491 y 493.

    328 * 1.5 = 492. El margen [491, 493] admite redondeos.
    """
    _apuntar_bigpickle(tamano=0, segundos=100)
    _apuntar_bigpickle(tamano=0, segundos=328)

    esperado = cuotas.espera_de_bigpickle(1000)
    assert 491 <= esperado <= 493, (
        "con dos filas buenas (100 y 328) se esperaba entre 491 y 493 y salio %r"
        % (esperado,)
    )


# ---------------------------------------------------------------------------
# (3) Filas de otro cerebro y filas con ERROR no cuentan
# ---------------------------------------------------------------------------

def test_filas_de_otro_cerebro_y_filas_con_error_no_cuentan():
    """Solo cuenta la fila buena de bigpickle: 100 s * 1.5 = 150.

    La fila de 'grok' (900 s) es de otro cerebro: no cuenta.
    La fila de bigpickle con resultado=ERROR (900 s) no cuenta.
    """
    _apuntar_otro_cerebro("grok", tamano=0, segundos=900)
    _apuntar_bigpickle(tamano=0, segundos=900, resultado=cuaderno.ERROR)
    _apuntar_bigpickle(tamano=0, segundos=100)

    esperado = cuotas.espera_de_bigpickle(1000)
    assert esperado == 150, (
        "solo la fila buena de bigpickle (100 s) debe contar: se esperaba 150 y salio %r"
        % (esperado,)
    )


# ---------------------------------------------------------------------------
# (4) Tareas parecidas manda; si no las hay, el record de todas
# ---------------------------------------------------------------------------

def test_tareas_parecidas_mandan_y_si_no_las_hay_usa_el_record_de_todas():
    """Cinco filas de tamano 10000 y 100 s, mas una de tamano 0 y 328 s.

    espera_de_bigpickle(12000): hay tareas parecidas (10000 esta entre la mitad y el doble
    de 12000), tardaron 100 s como mucho -> 100 * 1.5 = 150. Margen [149, 151].

    espera_de_bigpickle(1000): NO hay tareas parecidas (10000 no esta entre la mitad y el
    doble de 1000) -> se usa el record de todas, que es 328 -> 328 * 1.5 = 492.
    Margen [491, 493].
    """
    for _ in range(5):
        _apuntar_bigpickle(tamano=10000, segundos=100)
    _apuntar_bigpickle(tamano=0, segundos=328)

    con_parecidas = cuotas.espera_de_bigpickle(12000)
    assert 149 <= con_parecidas <= 151, (
        "con tareas parecidas (10000 letras, 100 s) se esperaba entre 149 y 151 y salio %r"
        % (con_parecidas,)
    )

    sin_parecidas = cuotas.espera_de_bigpickle(1000)
    assert 491 <= sin_parecidas <= 493, (
        "sin tareas parecidas se esperaba el record de todas (492) y salio %r"
        % (sin_parecidas,)
    )


# ---------------------------------------------------------------------------
# (5) Nunca menos de 60 segundos
# ---------------------------------------------------------------------------

def test_nunca_se_espera_menos_de_sesenta_segundos():
    """Cinco filas buenas de tamano 1000 y 5 s: 5 * 1.5 = 7.5, pero el suelo es 60."""
    for _ in range(5):
        _apuntar_bigpickle(tamano=1000, segundos=5)

    esperado = cuotas.espera_de_bigpickle(1000)
    assert esperado == 60, (
        "nunca se espera menos de 60 s: se esperaba 60 y salio %r" % (esperado,)
    )
