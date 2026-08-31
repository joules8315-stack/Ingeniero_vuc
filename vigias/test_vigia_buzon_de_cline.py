# -*- coding: utf-8 -*-
"""VIGIA — EL BUZON DE CLINE: no se trabaja sin ver lo que dejaron (Julio, 2026-08-31).

Julio: "cuando trabaje contigo, debes estar mirando el buzon... crea un mecanismo que te active
cuando claude este trabajando... no debe depender de que te acuerdes."

EL FALLO: el canal deja los mensajes de Claude para Cline, pero Cline no los veia salvo que Julio
le dijera "mira el buzon". Dependia de que Cline se acordara, y eso ya esta apuntado como algo que
NO funciona.

LA CURA: candado_buzon enganchado a UserPromptSubmit y Stop. Si hay un mensaje de otro agente PARA
CLINE sin leer, bloquea y lo muestra. No se puede trabajar sin verlo.

No llama a ningun cerebro: se le da de comer un canal de mentira. Determinista.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import autorizacion  # noqa: E402
import candado_buzon as cb  # noqa: E402


def _sin_autorizacion(monkeypatch):
    """La autorizacion de Julio NO esta puesta (solo el la pone); el candado tiene que morder."""
    monkeypatch.setattr(autorizacion, "autorizada", lambda: False)


def _bandeja_con(tmp_path, mensaje):
    b = str(tmp_path / "bandeja")
    os.makedirs(b, exist_ok=True)
    json.dump(mensaje, open(os.path.join(b, "m.json"), "w", encoding="utf-8"))
    return b


def test_bloquea_con_mensaje_de_claude_para_cline(tmp_path, monkeypatch):
    """Claude le dejo a Cline un encargo sin leer -> Cline no puede trabajar sin verlo."""
    _sin_autorizacion(monkeypatch)
    b = _bandeja_con(tmp_path, {"de": "claude", "para": "cline", "texto": "encargo pendiente",
                                "cuando": "2026-08-31", "leido": False})
    monkeypatch.setattr(cb, "BANDEJA", b)
    monkeypatch.setenv("INGENIERO_BUZON_CONTADOR", str(tmp_path / "cont"))
    monkeypatch.setenv("INGENIERO_QUIEN", "cline")
    monkeypatch.delenv("INGENIERO_OFF", raising=False)
    assert cb.main() == 2, (
        "candado_buzon no bloqueo con un mensaje de claude para cline sin leer. Sin bloqueo, "
        "Cline vuelve a trabajar sin ver los encargos y Julio tiene que avisarle a mano.")


def test_no_bloquea_sin_mensajes(tmp_path, monkeypatch):
    """Si no hay nada en el buzon, no estorba: un candado que bloquea siempre se acaba apagando."""
    _sin_autorizacion(monkeypatch)
    b = str(tmp_path / "vacia")
    os.makedirs(b, exist_ok=True)
    monkeypatch.setattr(cb, "BANDEJA", b)
    monkeypatch.setenv("INGENIERO_BUZON_CONTADOR", str(tmp_path / "cont"))
    monkeypatch.setenv("INGENIERO_QUIEN", "cline")
    monkeypatch.delenv("INGENIERO_OFF", raising=False)
    assert cb.main() == 0, "bloqueo sin mensajes pendientes: un candado que siempre grita se apaga"


def test_no_bloquea_a_claude_por_sus_propios_mensajes(tmp_path, monkeypatch):
    """Claude no se bloquea por los mensajes que el mismo le manda a Cline."""
    _sin_autorizacion(monkeypatch)
    b = _bandeja_con(tmp_path, {"de": "claude", "para": "cline", "texto": "encargo", "leido": False})
    monkeypatch.setattr(cb, "BANDEJA", b)
    monkeypatch.setenv("INGENIERO_BUZON_CONTADOR", str(tmp_path / "cont"))
    monkeypatch.setenv("INGENIERO_QUIEN", "claude")
    monkeypatch.delenv("INGENIERO_OFF", raising=False)
    assert cb.main() == 0, (
        "claude se bloqueo por mensajes que el mismo envio a cline: eso romperia el flujo")


def test_esta_enchufado_a_userprompt_y_stop():
    """Escrito no es cumplido. Tiene que estar en la puerta por donde arranca y termina el turno."""
    import _config
    assert _config.comandos_de("UserPromptSubmit", "candado_buzon"), (
        "candado_buzon no esta en UserPromptSubmit: sin eso no arranca el turno mirando el buzon, "
        "y Julio vuelve a tener que avisarle a Cline a mano")
    assert _config.comandos_de("Stop", "candado_buzon"), (
        "candado_buzon no esta en Stop: sin eso Cline puede terminar sin haberse asegurado de que "
        "no quedo un encargo sin ver")
