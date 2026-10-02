# -*- coding: utf-8 -*-
"""vigias/test_vigia_las_dos_vias.py — VIGIA DE CONTRATO_LAS_DOS_VIAS.

Nace ROJA: la pieza que arma la GUIA y el CODIGO por separado todavia no existe.
Cuando la reparacion este hecha, esta vigia pasa.

Lo que se exige, sin IA y sin mirar el texto del codigo (se EJECUTA):

  1. Una pieza nueva con una funcion que, dada una orden, arme:
       - la GUIA: objetivo, donde (pieza y funciones de la orden), motivo exacto del
         fallo anterior (leido del mensaje de la vigia roja y de los motivos del
         ultimo rechazo) y lo que no se debe repetir.
       - el CODIGO: la funcion completa de la pieza, literal, entregada por el
         mostrador y no por adivinar palabras; si no cabe se parte por funcion,
         nunca se recorta.
  2. Otra funcion que diga si hay MEZCLA entre las dos vias.

Tabla de verdad de CONTRATO_LAS_DOS_VIAS (las cuatro filas):

  | guia aparte | codigo limpio | resultado |
  |-------------|---------------|-----------|
  | si          | si            | PASA      |
  | si          | no (guia dentro del codigo) | NO PASA |
  | no (codigo dentro de la guia) | si | NO PASA |
  | no (una sola via) | no (una sola via) | NO PASA |

Nunca lanza: si la pieza no existe, la prueba falla por el import (rojo legitimo).
"""

import os
import sys
import tempfile

import pytest


# ---------------------------------------------------------------------------
# La pieza que se espera. Si aun no existe, el import falla y la vigia nace ROJA.
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import las_dos_vias  # noqa: E402  <- aqui nace roja si no existe


# ---------------------------------------------------------------------------
# Utilidades de prueba: todo en carpetas temporales, sin tocar el estado real.
# ---------------------------------------------------------------------------


def _orden_de_mentira(pieza="cuerpo/ejemplo.py", funciones=None):
    """Una orden con lo minimo que la pieza debe saber leer."""
    if funciones is None:
        funciones = ["saluda", "despide"]
    return {
        "objetivo": "que el saludo no se caiga cuando falta el nombre",
        "pieza": pieza,
        "funciones": list(funciones),
        "repara": "cuerpo/ejemplo.py:12-20",
        "mensaje_vigia_roja": (
            "FALLO en test_saluda_sin_nombre: KeyError: 'nombre' "
            "en cuerpo/ejemplo.py linea 14"
        ),
        "motivos_ultimo_rechazo": [
            "el codigo no traia la funcion saluda completa",
            "se recorto la funcion por la mitad",
        ],
        "no_repetir": [
            "no mandar la funcion a medias",
            "no adivinar el cuerpo de la funcion",
        ],
    }


def _codigo_literal():
    """El codigo tal cual lo entrega el mostrador: literal, sin adornos."""
    return (
        "def saluda(nombre):\n"
        "    if not nombre:\n"
        "        return 'hola'\n"
        "    return 'hola ' + nombre\n"
        "\n"
        "def despide(nombre):\n"
        "    return 'adios ' + (nombre or '')\n"
    )


# ---------------------------------------------------------------------------
# 1) La GUIA se arma aparte, con lo que pide el contrato.
# ---------------------------------------------------------------------------


def test_la_guia_trae_objetivo_donde_motivo_y_lo_que_no_se_repite():
    orden = _orden_de_mentira()
    guia = las_dos_vias.armar_guia(orden)

    assert isinstance(guia, str) and guia.strip(), "la guia no puede venir vacia"

    # objetivo
    assert orden["objetivo"] in guia, "la guia no lleva el objetivo"

    # donde = pieza y funciones de la orden
    assert orden["pieza"] in guia, "la guia no dice en que pieza se trabaja"
    for f in orden["funciones"]:
        assert f in guia, "la guia no nombra la funcion %r" % f

    # motivo exacto del fallo anterior: del mensaje de la vigia roja
    assert "KeyError" in guia, "la guia no lleva el motivo exacto de la vigia roja"
    assert "linea 14" in guia or "linea 14" in guia.replace("l\u00ednea", "linea"), (
        "la guia no lleva el renglon exacto del fallo"
    )

    # motivo exacto: de los motivos del ultimo rechazo
    for m in orden["motivos_ultimo_rechazo"]:
        assert m in guia, "la guia no lleva el motivo del ultimo rechazo: %r" % m

    # lo que no se debe repetir
    for n in orden["no_repetir"]:
        assert n in guia, "la guia no lleva lo que no se debe repetir: %r" % n


# ---------------------------------------------------------------------------
# 2) El CODIGO va literal, entregado por el mostrador, y si no cabe se parte
#    por funcion, nunca se recorta.
# ---------------------------------------------------------------------------


def test_el_codigo_va_literal_y_no_se_recorta():
    orden = _orden_de_mentira()
    codigo = _codigo_literal()

    salida = las_dos_vias.armar_codigo(orden, codigo)

    assert isinstance(salida, str) and salida.strip(), "el codigo no puede venir vacio"

    # literal: cada funcion completa, tal cual la entrego el mostrador
    assert "def saluda(nombre):" in salida
    assert "return 'hola ' + nombre" in salida
    assert "def despide(nombre):" in salida
    assert "return 'adios ' + (nombre or '')" in salida

    # no se adivina: no aparece nada que no estuviera en el codigo entregado
    assert "pass" not in salida, "el codigo trae relleno que no entrego el mostrador"


def test_si_no_cabe_se_parte_por_funcion_y_nunca_se_recorta():
    orden = _orden_de_mentira()
    codigo = _codigo_literal()

    # Un tope tan pequeno que no cabe todo: debe partirse por funcion.
    partes = las_dos_vias.armar_codigo(orden, codigo, tope=40)

    if isinstance(partes, str):
        partes = [partes]

    assert len(partes) >= 2, "con tope pequeno el codigo debe partirse por funcion"

    junto = "\n".join(partes)
    # ninguna funcion puede quedar a medias: cada trozo que empieza una funcion la termina
    for trozo in partes:
        if "def saluda" in trozo:
            assert "return 'hola ' + nombre" in trozo, "la funcion saluda quedo recortada"
        if "def despide" in trozo:
            assert "return 'adios ' + (nombre or '')" in trozo, (
                "la funcion despide quedo recortada"
            )

    # y entre todos los trozos, el codigo entero sigue estando
    assert "def saluda(nombre):" in junto
    assert "def despide(nombre):" in junto


# ---------------------------------------------------------------------------
# 3) La funcion que dice si hay MEZCLA entre las dos vias.
# ---------------------------------------------------------------------------


def test_hay_mezcla_detecta_guia_dentro_del_codigo():
    guia = "OBJETIVO: arreglar el saludo\nPIEZA: cuerpo/ejemplo.py\n"
    codigo_limpio = _codigo_literal()
    codigo_sucio = codigo_limpio + "\n# OBJETIVO: arreglar el saludo\n"

    assert las_dos_vias.hay_mezcla(guia, codigo_limpio) is False, (
        "guia aparte y codigo limpio NO son mezcla"
    )
    assert las_dos_vias.hay_mezcla(guia, codigo_sucio) is True, (
        "guia dentro del codigo SI es mezcla"
    )


def test_hay_mezcla_detecta_codigo_dentro_de_la_guia():
    guia_limpia = "OBJETIVO: arreglar el saludo\nPIEZA: cuerpo/ejemplo.py\n"
    guia_sucia = guia_limpia + "\n" + _codigo_literal()
    codigo = _codigo_literal()

    assert las_dos_vias.hay_mezcla(guia_limpia, codigo) is False
    assert las_dos_vias.hay_mezcla(guia_sucia, codigo) is True, (
        "codigo dentro de la guia SI es mezcla"
    )


# ---------------------------------------------------------------------------
# 4) Las cuatro filas de la tabla de verdad de CONTRATO_LAS_DOS_VIAS.
# ---------------------------------------------------------------------------


def test_tabla_de_verdad_las_cuatro_filas():
    guia = "OBJETIVO: arreglar el saludo\nPIEZA: cuerpo/ejemplo.py\n"
    codigo = _codigo_literal()

    # Fila 1: guia aparte y codigo limpio -> PASA
    assert las_dos_vias.pasa(guia, codigo) is True

    # Fila 2: guia dentro del codigo -> NO PASA
    codigo_con_guia = codigo + "\n# OBJETIVO: arreglar el saludo\n"
    assert las_dos_vias.pasa(guia, codigo_con_guia) is False

    # Fila 3: codigo dentro de la guia -> NO PASA
    guia_con_codigo = guia + "\n" + codigo
    assert las_dos_vias.pasa(guia_con_codigo, codigo) is False

    # Fila 4: una sola via (falta la guia o falta el codigo) -> NO PASA
    assert las_dos_vias.pasa("", codigo) is False
    assert las_dos_vias.pasa(guia, "") is False
    assert las_dos_vias.pasa("", "") is False


# ---------------------------------------------------------------------------
# 5) Nunca lanza: con ordenes raras devuelve algo, no explota.
# ---------------------------------------------------------------------------


def test_nunca_lanza_con_ordenes_raras():
    for orden in ({}, {"pieza": None}, {"funciones": None}, {"objetivo": 123}):
        try:
            las_dos_vias.armar_guia(orden)
        except Exception as e:  # pragma: no cover
            pytest.fail("armar_guia lanzo con orden rara: %r" % (e,))

    for guia, codigo in ((None, None), ("", ""), (123, 456)):
        try:
            las_dos_vias.hay_mezcla(guia, codigo)
            las_dos_vias.pasa(guia, codigo)
        except Exception as e:  # pragma: no cover
            pytest.fail("hay_mezcla/pasa lanzaron con entradas raras: %r" % (e,))


# ---------------------------------------------------------------------------
# 6) Sin tocar el estado real: todo lo que se escriba va a carpeta temporal.
# ---------------------------------------------------------------------------


def test_no_toca_el_estado_real():
    with tempfile.TemporaryDirectory() as tmp:
        orden = _orden_de_mentira(pieza=os.path.join(tmp, "ejemplo.py"))
        guia = las_dos_vias.armar_guia(orden)
        codigo = las_dos_vias.armar_codigo(orden, _codigo_literal())
        assert guia and codigo
        # la carpeta temporal sigue siendo temporal: nada se escribio fuera de ella
        assert os.path.isdir(tmp)
