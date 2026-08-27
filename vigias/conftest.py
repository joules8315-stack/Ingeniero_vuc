# -*- coding: utf-8 -*-
"""conftest.py — NINGUNA COMPROBACION TOCA EL ESTADO DE VERDAD (ley 23, 2026-08-21).

LEY 23: "una comprobacion que falla a veces es peor que ninguna". Ya se curo dos veces por lo
mismo —la memoria de errores y el registro de apagones— y volvio a pasar por un tercer sitio: la
marca de "hilo perdido" era un archivo COMPARTIDO. Una comprobacion la ponia y otra, corriendo a
la vez, se la encontraba puesta: el candado de edicion bloqueaba un contrato que debe poder
escribirse siempre. Sola, verde; en tanda, roja. Rojo falso, y un rojo falso ensena a ignorar los
rojos, que es exactamente como se cuela un rojo de verdad.

La cura no es arreglar el sitio numero tres: es que NINGUNA comprobacion vea nunca el estado real.
Cada prueba trabaja sobre su propia copia, y la copia se va con ella. Vale tambien para los
programas que la prueba lanza aparte, porque heredan estas variables.
"""
import os
import sys
import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


@pytest.fixture(autouse=True)
def _nada_toca_lo_real(tmp_path, monkeypatch):
    """Cada prueba, con su propia copia. Se hereda a los programas que la prueba lance."""
    monkeypatch.setenv("INGENIERO_CONTEXTO_TEST", str(tmp_path / ".contexto_perdido"))
    # El contador de bloqueos del protocolo: tras 2 bloqueos seguidos se abre una valvula de
    # escape para no atascar a Julio. Era compartido, asi que un bloqueo DE VERDAD dejaba la
    # valvula ya abierta y la comprobacion salia roja sin que nada estuviera roto (cuarto sitio
    # con este mismo patron, 2026-08-21).
    monkeypatch.setenv("INGENIERO_CONTADOR_TEST", str(tmp_path / ".protocolo_bloqueos"))
    # La AUTORIZACION de Julio (su llave) tambien es estado REAL: si la tiene puesta (24h), los
    # candados abren de verdad y las vigias que prueban que el candado MUERDE se pondrian rojas en
    # falso (creyendo que el candado fallo cuando en realidad la llave abrio, que es su trabajo).
    # Ley 23 + L15 (2026-08-27): ninguna comprobacion ve el estado real. Cada vigia apunta la
    # autorizacion a su propia copia que no existe, asi prueba que el candado muerde SIN llave,
    # y la llave real de Julio deja de causar rojos falsos. La llave real sigue abriendo (no se toca).
    monkeypatch.setenv("INGENIERO_AUTORIZACION_TEST", str(tmp_path / ".aut_julio_no_existe"))
    yield
