# -*- coding: utf-8 -*-
"""Vigia: cada orden del taller tiene SU PROPIA copia de la carpeta.

Que vigila
----------
Que exista `arnes/copia_de_la_orden.py` con dos funciones:

  - copia_para(orden_id, raiz, correr_uno=None)
      Devuelve un diccionario con 'ok', 'carpeta' y 'motivo'.
      El mismo orden_id pedido dos veces devuelve LA MISMA carpeta.
      Dos orden_id distintos devuelven carpetas DISTINTAS.

  - soltar_copia(copia, correr_uno=None)
      Devuelve True si solto la carpeta, False si no habia nada que soltar.
      Llamarla dos veces es seguro: la segunda no hace nada.

Por que
-------
Medido el 2026-09-21 y escrito en
`vigias/test_vigia_el_pit_corre_una_tarea_a_la_vez.py`: con dos tareas a la
vez, las dos comparten la misma carpeta de trabajo, y el guardia de una ve
el trabajo A MEDIAS de la otra. Entonces da por bueno, o por malo, lo que no
le toca.

Esa misma vigia dice cuando se puede volver a dos tareas: SOLO cuando cada
tarea trabaje en su propia copia. Hoy 2026-09-29 se intento subir el
paralelo sin eso y esa vigia lo freno con razon. Asi que la copia propia va
PRIMERO.

Estado de esta vigia
--------------------
NACE ROJA A PROPOSITO: la pieza `arnes/copia_de_la_orden.py` todavia no
existe y se escribe en otra ronda. El primer assert lo dice con un mensaje
claro para que la roja se lea de un vistazo.

Reglas de esta prueba
---------------------
  - Solo libreria estandar: os, sys, types.
  - Sin IA, sin red, sin lanzar procesos de verdad.
  - Nada escrito fuera de la carpeta temporal que da pytest.
  - Resultado siempre igual: no depende del reloj ni del azar.
"""

import os
import sys
import types


# ---------------------------------------------------------------------------
# ARRANQUE: meter en sys.path la raiz del proyecto y la carpeta arnes
# ---------------------------------------------------------------------------
# Este archivo vive en <raiz>/vigias/test_vigia_....py
# La raiz del proyecto es la carpeta que esta un nivel arriba de 'vigias'.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
_ARNES = os.path.join(_RAIZ, "arnes")

for _ruta in (_RAIZ, _ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# ---------------------------------------------------------------------------
# FALSO DE correr_uno: no lanza ningun programa de verdad
# ---------------------------------------------------------------------------
def _correr_uno_falso(*args, **kwargs):
    """Devuelve un objeto con returncode 0, stdout vacio y stderr vacio.

    Se usa en lugar del programa que crea la carpeta de verdad, para que la
    prueba no lance procesos ni toque nada fuera de la carpeta temporal.
    """
    return types.SimpleNamespace(returncode=0, stdout="", stderr="")


# ---------------------------------------------------------------------------
# CASO 1: DOS ORDENES DISTINTAS, DOS CARPETAS DISTINTAS
# ---------------------------------------------------------------------------
def test_dos_ordenes_distintas_dos_carpetas_distintas(tmp_path):
    # Primero de todo: la pieza tiene que existir. Si no, la roja se lee
    # de un vistazo y no sale un error feo de importacion.
    try:
        from arnes import copia_de_la_orden
    except ImportError:
        copia_de_la_orden = None

    assert copia_de_la_orden is not None, (
        "arnes/copia_de_la_orden.py todavia no esta escrita: "
        "la pieza que da a cada orden su propia carpeta se escribe en otra "
        "ronda. Esta vigia nace roja a proposito."
    )

    raiz = str(tmp_path)
    copia_a = copia_de_la_orden.copia_para(
        "orden-alfa", raiz, correr_uno=_correr_uno_falso
    )
    copia_b = copia_de_la_orden.copia_para(
        "orden-beta", raiz, correr_uno=_correr_uno_falso
    )

    assert copia_a.get("ok") is True, (
        "copia_para('orden-alfa') no dio ok: %r" % (copia_a,)
    )
    assert copia_b.get("ok") is True, (
        "copia_para('orden-beta') no dio ok: %r" % (copia_b,)
    )

    carpeta_a = copia_a.get("carpeta")
    carpeta_b = copia_b.get("carpeta")

    assert carpeta_a, "copia_para('orden-alfa') no devolvio carpeta"
    assert carpeta_b, "copia_para('orden-beta') no devolvio carpeta"
    assert carpeta_a != carpeta_b, (
        "dos ordenes distintas comparten la misma carpeta (%r): "
        "cada tarea del taller tiene que trabajar en SU PROPIA copia"
        % (carpeta_a,)
    )


# ---------------------------------------------------------------------------
# CASO 2: LA MISMA ORDEN, LA MISMA CARPETA
# ---------------------------------------------------------------------------
def test_la_misma_orden_la_misma_carpeta(tmp_path):
    try:
        from arnes import copia_de_la_orden
    except ImportError:
        copia_de_la_orden = None

    assert copia_de_la_orden is not None, (
        "arnes/copia_de_la_orden.py todavia no esta escrita: "
        "la pieza que da a cada orden su propia carpeta se escribe en otra "
        "ronda. Esta vigia nace roja a proposito."
    )

    raiz = str(tmp_path)
    primera = copia_de_la_orden.copia_para(
        "orden-gamma", raiz, correr_uno=_correr_uno_falso
    )
    segunda = copia_de_la_orden.copia_para(
        "orden-gamma", raiz, correr_uno=_correr_uno_falso
    )

    assert primera.get("ok") is True, (
        "la primera copia_para('orden-gamma') no dio ok: %r" % (primera,)
    )
    assert segunda.get("ok") is True, (
        "la segunda copia_para('orden-gamma') no dio ok: %r" % (segunda,)
    )

    assert primera.get("carpeta") == segunda.get("carpeta"), (
        "la misma orden pidio su copia dos veces y devolvio carpetas "
        "distintas (%r y %r): el mismo orden_id tiene que dar LA MISMA "
        "carpeta" % (primera.get("carpeta"), segunda.get("carpeta"))
    )


# ---------------------------------------------------------------------------
# CASO 3: SOLTARLA DOS VECES NO REVIENTA
# ---------------------------------------------------------------------------
def test_soltarla_dos_veces_no_revienta(tmp_path):
    try:
        from arnes import copia_de_la_orden
    except ImportError:
        copia_de_la_orden = None

    assert copia_de_la_orden is not None, (
        "arnes/copia_de_la_orden.py todavia no esta escrita: "
        "la pieza que da a cada orden su propia carpeta se escribe en otra "
        "ronda. Esta vigia nace roja a proposito."
    )

    raiz = str(tmp_path)
    copia = copia_de_la_orden.copia_para(
        "orden-delta", raiz, correr_uno=_correr_uno_falso
    )
    assert copia.get("ok") is True, (
        "copia_para('orden-delta') no dio ok: %r" % (copia,)
    )

    primera = copia_de_la_orden.soltar_copia(
        copia, correr_uno=_correr_uno_falso
    )
    assert primera is True, (
        "soltar_copia la primera vez devolvio %r y tenia que devolver True"
        % (primera,)
    )

    segunda = copia_de_la_orden.soltar_copia(
        copia, correr_uno=_correr_uno_falso
    )
    assert segunda is False, (
        "soltar_copia la segunda vez devolvio %r y tenia que devolver False "
        "sin reventar" % (segunda,)
    )


if __name__ == "__main__":
    # Prueba de humo: solo comprueba que el archivo se importa y que el
    # primer assert salta con el mensaje claro mientras la pieza no exista.
    import tempfile

    with tempfile.TemporaryDirectory() as _tmp:
        class _TmpPath(object):
            def __str__(self):
                return _tmp

        try:
            test_dos_ordenes_distintas_dos_carpetas_distintas(_TmpPath())
            test_la_misma_orden_la_misma_carpeta(_TmpPath())
            test_soltarla_dos_veces_no_revienta(_TmpPath())
            print("OK: cada orden tiene su propia copia")
        except AssertionError as error:
            print("ROJA: %s" % (error,))
