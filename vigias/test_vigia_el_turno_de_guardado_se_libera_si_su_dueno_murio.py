# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_turno_de_guardado_se_libera_si_su_dueno_murio.py

VIGIA: EL TURNO DE GUARDADO SE LIBERA SI SU DUENO MURIO.

Vigila arnes/candado_equipo.py::fila_de_commits(raiz, espera=2400), que es un
administrador de contexto (se usa con `with`).

Que se prueba, con assert y de verdad (ejecutando, no leyendo):

  1) Si el turno existe recien escrito con el numero 999999 (un proceso que NO
existe), el `with` entra en menos de 3 segundos: el candado reconoce que el dueno
murio y libera el turno.

  2) Si el turno existe con el numero del PROPIO proceso de la prueba
(os.getpid(), que esta vivo), el `with` con espera=2 lanza TimeoutError: el
candado NO libera el turno de un dueno vivo.

  3) Al salir del `with` el archivo del turno ya no existe: el candado limpia.

La ruta del turno se calcula igual que en la funcion vigilada:

    os.path.join(tempfile.gettempdir(),
                 'ingeniero_fila_' +
                 hashlib.sha1(os.path.abspath(str(raiz)).lower()
                              .encode('utf-8')).hexdigest()[:12] +
                 '.lock')

con raiz = str(tmp_path).

Cada prueba borra el archivo del turno al final, para no dejar basura en el
temporal ni ensuciar a las demas vigias.
"""

import hashlib
import os
import sys
import tempfile
import time

import pytest


# --- La carpeta arnes tiene que estar en sys.path para poder importar candado_equipo ---
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_DEL_PROYECTO = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ_DEL_PROYECTO, "arnes")
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import candado_equipo  # noqa: E402


# --- El numero de un proceso que no existe (para simular un dueno muerto) ---
PID_MUERTO = 999999


def _ruta_del_turno(raiz):
    """Calcula la ruta del turno EXACTAMENTE igual que fila_de_commits."""
    clave = hashlib.sha1(
        os.path.abspath(str(raiz)).lower().encode("utf-8")
    ).hexdigest()[:12]
    return os.path.join(
        tempfile.gettempdir(), "ingeniero_fila_" + clave + ".lock"
    )


def _escribir_turno(ruta, pid):
    """Deja el turno escrito con el numero de proceso que se le diga."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(str(pid))


def _borrar_turno(ruta):
    """Borra el archivo del turno si existe. Nunca revienta."""
    try:
        os.remove(ruta)
    except OSError:
        pass


def test_el_turno_de_un_dueno_muerto_se_libera(tmp_path):
    """(1) Turno con pid 999999 (proceso que no existe): el with entra rapido."""
    raiz = str(tmp_path)
    ruta = _ruta_del_turno(raiz)
    _borrar_turno(ruta)
    try:
        _escribir_turno(ruta, PID_MUERTO)
        assert os.path.exists(ruta), "el turno de prueba no llego a escribirse"

        inicio = time.time()
        with candado_equipo.fila_de_commits(raiz, espera=3):
            paso = time.time() - inicio
            # Entro: el candado reconocio que el dueno murio y libero el turno.
            assert paso < 3, (
                "el candado no libero el turno de un dueno muerto: "
                "tardo %.2f s (espera=3)" % paso
            )
    finally:
        _borrar_turno(ruta)


def test_el_turno_de_un_dueno_vivo_no_se_libera(tmp_path):
    """(2) Turno con el pid de ESTE proceso (vivo): el with lanza TimeoutError."""
    raiz = str(tmp_path)
    ruta = _ruta_del_turno(raiz)
    _borrar_turno(ruta)
    try:
        _escribir_turno(ruta, os.getpid())
        assert os.path.exists(ruta), "el turno de prueba no llego a escribirse"

        with pytest.raises(TimeoutError):
            with candado_equipo.fila_de_commits(raiz, espera=2):
                # No deberia llegar aqui: el dueno esta vivo.
                pass
    finally:
        _borrar_turno(ruta)


def test_al_salir_del_with_el_turno_ya_no_existe(tmp_path):
    """(3) Al salir del with, el archivo del turno ya no esta."""
    raiz = str(tmp_path)
    ruta = _ruta_del_turno(raiz)
    _borrar_turno(ruta)
    try:
        with candado_equipo.fila_de_commits(raiz, espera=3):
            # Dentro del with el turno tiene que existir: lo acaba de tomar.
            assert os.path.exists(ruta), (
                "dentro del with el turno no existe: el candado no lo tomo"
            )
        # Fuera del with el candado tiene que haberlo soltado.
        assert not os.path.exists(ruta), (
            "al salir del with el turno sigue ahi: el candado no lo solto"
        )
    finally:
        _borrar_turno(ruta)
