# -*- coding: utf-8 -*-
"""VIGIA — CONTESTAR UN RECADO LO DEJA CERRADO.

FALLO REAL, 2026-08-31: el candado de comunicacion exige que no queden recados SIN RESPONDER, y
mira una marca `respondido` dentro de cada recado. Pero NADIE pone esa marca: `canal.enviar` no
la toca y no existe ninguna otra forma de ponerla.

Resultado medido ese dia: se contestaron los recados atrasados por el canal, y el candado siguio
bloqueando con los MISMOS recados. No habia forma honrada de satisfacerlo.

Y esa leccion ya estaba pagada, escrita en la propia memoria de fallos:
  "no hacer un candado sin una forma honrada de satisfacerlo: empuja a saltarselo, y eso es peor
   que no tenerlo"

Un candado que no se puede satisfacer se acaba apagando. Y apagado no protege nada.

LO QUE SE MIDE
  1. Contestarle a alguien deja cerrados los recados que esa persona te habia dejado.
  2. No se cierran los recados de OTROS: contestarle a uno no borra lo que debe a los demas.
  3. El recado se marca como contestado, con quien y cuando, para que quede rastro.
"""
import io
import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

import canal   # noqa: E402


@pytest.fixture
def buzon(monkeypatch, tmp_path):
    """Un buzon de mentira: una prueba jamas toca el de verdad."""
    monkeypatch.setenv("INGENIERO_CANAL_TEST", str(tmp_path))
    monkeypatch.setenv("INGENIERO_QUIEN", "claude")
    return tmp_path


def _recados_de(carpeta, de_quien):
    salen = []
    for nombre in sorted(os.listdir(str(carpeta))):
        if not nombre.endswith(".json"):
            continue
        try:
            with io.open(os.path.join(str(carpeta), nombre), encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue
        if str(d.get("de", "")).lower() == de_quien:
            salen.append(d)
    return salen


def test_existe_la_forma_de_cerrar_un_recado():
    """Sin esto, el candado no se puede satisfacer y se acaba apagando."""
    assert hasattr(canal, "cerrar_recados_de"), (
        "no existe ninguna forma de dejar cerrado un recado ya contestado. El candado de "
        "comunicacion exige que no queden recados sin responder, pero nadie puede marcarlos: "
        "es un candado sin salida honrada, y esos se acaban apagando")


def test_contestar_cierra_los_recados_de_esa_persona(buzon):
    canal.enviar("claude", "oye, una duda", de="continue")
    assert not any(r.get("respondido") for r in _recados_de(buzon, "continue")), \
        "el recado nacio ya marcado como contestado: entonces no mide nada"

    canal.enviar("continue", "te contesto: es asi", de="claude")

    quedan = [r for r in _recados_de(buzon, "continue") if not r.get("respondido")]
    assert not quedan, (
        "se le contesto y sus recados siguen contando como sin responder. Asi el candado bloquea "
        "para siempre con los mismos recados, que es lo que paso el 2026-08-31")


def test_no_cierra_los_recados_de_los_demas(buzon):
    """Contestarle a uno no puede borrar lo que se le debe a otro."""
    canal.enviar("claude", "lo mio", de="continue")
    canal.enviar("claude", "y lo mio", de="otro")

    canal.enviar("continue", "te contesto a ti", de="claude")

    del_otro = [r for r in _recados_de(buzon, "otro") if not r.get("respondido")]
    assert del_otro, (
        "al contestarle a uno se dieron por cerrados TAMBIEN los recados de otro. Asi se pierden "
        "cosas que Julio o la otra IA estan esperando")


def test_queda_rastro_de_quien_contesto_y_cuando(buzon):
    """La memoria no olvida: si algo se cierra, se sabe quien lo cerro."""
    canal.enviar("claude", "una pregunta", de="continue")
    canal.enviar("continue", "contestado", de="claude")

    cerrados = [r for r in _recados_de(buzon, "continue") if r.get("respondido")]
    assert cerrados, "no se cerro ninguno"
    r = cerrados[0]
    assert str(r.get("respondido_por", "")).lower() == "claude", \
        "no se apunto QUIEN contesto el recado"
    assert r.get("respondido_cuando"), \
        "no se apunto CUANDO se contesto: sin fecha no hay rastro que valga"
