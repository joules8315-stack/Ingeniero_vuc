# -*- coding: utf-8 -*-
"""VIGIA — EL BUZON NO BLOQUEA A NINGUNA IA POR SUS PROPIOS MENSAJES.

Encargo de Claude para Continue (2026-08-31, tercera tarea, URGENTE porque BLOQUEA el trabajo).
Julio: "legisla, pon candado y pon vigia, reparalo".

EL FALLO MEDIDO:
  arnes/candado_buzon.py sabe a quien bloquea por la variable de entorno INGENIERO_QUIEN, que
  nadie pone. Sin ella quien corre es "desconocido", asi que la excepcion "no bloquearse por lo
  que uno mismo envio" NUNCA se aplica, y lista los recados que uno mismo mando como si fueran
  de otro.

LO QUE VIGILA (cura de Claude):
  1. Sin identidad (sin INGENIERO_QUIEN) un UNICO remitente con recados sin leer no puede
     bloquearse a si mismo: se DEDUCE quien corre y NO frena. Ante la duda AVISA, no bloquea
     (parar el trabajo de todos es peor que un aviso).
  2. Con identidad conocida, nadie se bloquea con los recados que el mismo envio.
  3. El candado consulta al companero ACTIVO (no una lista a mano con "cline" clavado).
  4. NO afloja el freno de verdad: un recado de OTRO agente (el companero) sin contestar SIGUE
     bloqueando igual de fuerte.
"""
import io
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import autorizacion  # noqa: E402
import candado_buzon as cb  # noqa: E402


def _sin_autorizacion(monkeypatch):
    monkeypatch.setattr(autorizacion, "autorizada", lambda: False)


def _bandeja(tmp_path, *mensajes):
    b = str(tmp_path / "bandeja")
    os.makedirs(b, exist_ok=True)
    for i, m in enumerate(mensajes):
        json.dump(m, open(os.path.join(b, "m%d.json" % i), "w", encoding="utf-8"))
    return b


def _setup(monkeypatch, tmp_path, *mensajes):
    _sin_autorizacion(monkeypatch)
    b = _bandeja(tmp_path, *mensajes)
    monkeypatch.setattr(cb, "BANDEJA", b)
    monkeypatch.setenv("INGENIERO_BUZON_CONTADOR", str(tmp_path / "cont"))
    monkeypatch.delenv("INGENIERO_OFF", raising=False)


def test_sin_identidad_no_bloquea_por_lo_que_uno_mismo_envio(tmp_path, monkeypatch):
    """FALLO 1: sin INGENIERO_QUIEN todo es 'desconocido'. Un unico remitente con recados suyos
    sin leer NO puede bloquearse a si mismo: se deduce y no frena (a lo sumo avisa)."""
    _setup(monkeypatch, tmp_path,
           {"de": "desconocido", "para": "desconocido", "texto": "yo mando", "leido": False},
           {"de": "desconocido", "para": "desconocido", "texto": "yo mando 2", "leido": False})
    monkeypatch.delenv("INGENIERO_QUIEN", raising=False)   # nadie pone la variable
    assert cb.main() == 0, (
        "sin identidad, un unico remitente esta bloqueandose por lo que el mando. "
        "Tiene que deducirlo y no frenar.")


def test_con_identidad_no_se_bloquea_por_sus_propios_mensajes(tmp_path, monkeypatch):
    """Con identidad conocida no se bloquea por recados que uno mismo envio (aunque el destino
    este como 'desconocido')."""
    _setup(monkeypatch, tmp_path,
           {"de": "continue", "para": "desconocido", "texto": "yo mando", "leido": False})
    monkeypatch.setenv("INGENIERO_QUIEN", "continue")
    assert cb.main() == 0, (
        "continue se bloqueo por un recado que el mismo envio hacia 'desconocido'.")


def test_sigue_frenando_a_un_recado_de_verdad(tmp_path, monkeypatch):
    """NO aflojar lo que protege: un recado del companero (otro agente) sin contestar sigue
    bloqueando igual de fuerte."""
    _setup(monkeypatch, tmp_path,
           {"de": "claude", "para": "continue", "texto": "recado del companero", "leido": False})
    monkeypatch.setenv("INGENIERO_QUIEN", "continue")
    assert cb.main() == 2, (
        "aflojo el freno: un recado de otro agente (claude) para continue sin ver debe bloquear.")


def test_consulta_al_companero_activo_no_lleva_nombre_clavado():
    """FALLO 2: no lleva la lista de companeros a mano con 'cline'. Consulta al companero activo
    (en arnes/companero.py), el unico sitio donde vive esa respuesta."""
    txt = io.open(os.path.join(AQUI, "arnes", "candado_buzon.py"),
                  encoding="utf-8", errors="ignore").read()
    assert "companero" in txt.lower() or "activo" in txt.lower(), (
        "candado_buzon no consulta al companero activo: depende de un nombre clavado")
