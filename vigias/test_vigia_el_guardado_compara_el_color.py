# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_guardado_compara_el_color.py

VIGIA QUE VIGILA LA REPARACION R25-el-guardado-compara-el-color-no-exige-verde.

QUE VIGILA:
  Que la decision de guardar compare el color de las vigias vecinas CON EL COLOR
  QUE TENIAN ANTES del cambio, y frene SOLO si el cambio EMPEORA algo.

  Una vigia que YA estaba roja antes del cambio, y que el cambio no toca, NO puede
  frenar el guardado. Hoy (2026-10-01) el guardia frena en cuanto encuentra una roja
  ya guardada en el vecindario, y como hay 54 rojas repartidas por el proyecto,
  cualquier trabajo correcto queda frenado por culpa de rojas ajenas.

COMO NACE:
  ROJA por un assert que falla, no por un error de sintaxis ni por un nombre que
  no existe. Cuando la reparacion este hecha, esta vigia pasa a verde sin tocarla.

COMO SE PRUEBA SIN TOCAR EL PROYECTO DE VERDAD:
  Se llama a la funcion pura `rojas_que_frenan` de arnes/guardia_de_guardado.py,
  que es la que decide que rojas frenan. Se le pasa:
    - rojas_ahora:        las rojas que hay ahora (una de ellas ya estaba roja antes)
    - guardadas:          las que ya estan en git (todas)
    - declaradas:         las que una orden declara que esperan arreglo (ninguna)
    - conocidas_de_antes: las que YA estaban rojas antes del cambio (la ajena)
  Y se exige que la roja ajena NO aparezca en la lista de las que frenan.

  Si la reparacion no esta hecha, `rojas_que_frenan` devuelve la roja ajena y el
  assert falla: la vigia nace ROJA, como manda el metodo de Julio.

NO TOCA LA MEMORIA DE VERDAD:
  No escribe en memoria/ ni en .rojas_conocidas.json. Solo llama a una funcion pura
  con listas en memoria. Nada de estado compartido.
"""
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# Localizar la raiz del proyecto y el modulo del guardia sin depender del cwd.
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


def _cargar_rojas_que_frenan():
    """Trae la funcion pura que decide que rojas frenan el guardado.

    Si el modulo no se puede importar, la vigia falla con un mensaje claro
    (no con un ImportError crudo), para que se vea que el problema es del
    guardia y no de la vigia.
    """
    try:
        from arnes import guardia_de_guardado
    except Exception as e:  # pragma: no cover - solo si el arnes se rompe
        pytest.fail(
            "No se pudo importar arnes/guardia_de_guardado.py: %r. "
            "La vigia necesita esa funcion pura para decidir que rojas frenan." % (e,)
        )
    fn = getattr(guardia_de_guardado, "rojas_que_frenan", None)
    if fn is None:
        pytest.fail(
            "arnes/guardia_de_guardado.py no expone `rojas_que_frenan`. "
            "Sin esa funcion no se puede vigilar que el guardado compare el color."
        )
    return fn


# ---------------------------------------------------------------------------
# LA VIGIA
# ---------------------------------------------------------------------------
def test_una_roja_de_antes_ajena_al_cambio_no_frena_el_guardado():
    """Una vigia roja que YA estaba roja antes, y que el cambio no toca, no frena.

    Escenario (el caso real medido el 2026-09-28: 54 rojas repartidas por el
    proyecto):
      - `vigias/test_vieja_roja.py` ya estaba roja ANTES del cambio.
      - El trabajo que se va a guardar NO la toca.
      - El guardia debe comparar el color de antes con el de ahora y ver que
        NO empeoro: la roja ajena no puede frenar.

    Hoy el guardia frena con cualquier roja ya guardada en el vecindario, asi
    que este assert FALLA: la vigia nace ROJA.
    """
    rojas_que_frenan = _cargar_rojas_que_frenan()

    roja_ajena = "vigias/test_vieja_roja.py"
    roja_del_cambio = "vigias/test_lo_que_toco_el_cambio.py"

    rojas_ahora = [roja_ajena, roja_del_cambio]
    guardadas = [roja_ajena, roja_del_cambio]   # las dos ya estan en git
    declaradas = []                              # ninguna orden las declara esperando
    conocidas_de_antes = [roja_ajena]            # la ajena YA estaba roja antes

    frenan = rojas_que_frenan(
        rojas_ahora, guardadas, declaradas, conocidas_de_antes
    )

    assert roja_ajena not in frenan, (
        "El guardado NO compara el color de antes: la vigia %r ya estaba roja "
        "antes del cambio y el cambio no la toca, pero el guardia la cuenta "
        "como roja que frena. Con 54 rojas repartidas por el proyecto, cualquier "
        "trabajo correcto queda frenado por rojas ajenas. "
        "Frenan ahora: %r" % (roja_ajena, frenan)
    )


def test_una_roja_nueva_del_cambio_si_frena_el_guardado():
    """Contraprueba: si el cambio EMPEORA algo, el guardado SI tiene que frenar.

    Esta parte NO es la que nace roja: es la que impide que la reparacion se
    haga trampa (por ejemplo, dejando de frenar siempre). Una roja que el
    cambio introduce de verdad tiene que seguir frenando.
    """
    rojas_que_frenan = _cargar_rojas_que_frenan()

    roja_nueva = "vigias/test_lo_que_toco_el_cambio.py"

    rojas_ahora = [roja_nueva]
    guardadas = [roja_nueva]        # ya esta en git
    declaradas = []                  # ninguna orden la declara esperando
    conocidas_de_antes = []          # NO estaba roja antes: el cambio la rompio

    frenan = rojas_que_frenan(
        rojas_ahora, guardadas, declaradas, conocidas_de_antes
    )

    assert roja_nueva in frenan, (
        "El guardado dejo de frenar cuando el cambio EMPEORA algo: la vigia %r "
        "no estaba roja antes y ahora si, y el guardia la deja pasar. "
        "Frenan ahora: %r" % (roja_nueva, frenan)
    )


def test_una_roja_declarada_por_su_orden_no_frena_el_guardado():
    """Contraprueba: una roja que su orden declara esperando arreglo no frena.

    Esto ya funciona hoy; se deja aqui para que la reparacion no lo rompa al
    tocar la comparacion de colores.
    """
    rojas_que_frenan = _cargar_rojas_que_frenan()

    roja_declarada = "vigias/test_espera_su_arreglo.py"

    rojas_ahora = [roja_declarada]
    guardadas = [roja_declarada]
    declaradas = [roja_declarada]    # su orden la declara esperando
    conocidas_de_antes = []

    frenan = rojas_que_frenan(
        rojas_ahora, guardadas, declaradas, conocidas_de_antes
    )

    assert roja_declarada not in frenan, (
        "Una roja declarada por su orden como esperando arreglo no puede frenar "
        "el guardado. Frenan ahora: %r" % (frenan,)
    )


def test_una_roja_nueva_sin_guardar_no_frena_el_guardado():
    """Contraprueba: una roja que aun no esta en git es nueva y no frena.

    Esto ya funciona hoy; se deja aqui para que la reparacion no lo rompa.
    """
    rojas_que_frenan = _cargar_rojas_que_frenan()

    roja_nueva_sin_guardar = "vigias/test_recien_escrita.py"

    rojas_ahora = [roja_nueva_sin_guardar]
    guardadas = []                   # todavia no esta en git
    declaradas = []
    conocidas_de_antes = []

    frenan = rojas_que_frenan(
        rojas_ahora, guardadas, declaradas, conocidas_de_antes
    )

    assert roja_nueva_sin_guardar not in frenan, (
        "Una roja que aun no esta guardada es nueva y no puede frenar el "
        "guardado. Frenan ahora: %r" % (frenan,)
    )
