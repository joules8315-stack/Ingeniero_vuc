# -*- coding: utf-8 -*-
"""VIGIA — EL EQUIPO NO SE CAE POR LA CAJA (fallo real 2026-08-24).

El comando 'equipo' pasaba la CAJA (dict del paquete) a `trabajar`, que espera el TEXTO.
Se pagaba a DeepSeek, contestaba bien, y justo al comprobar que no invento archivos se caia
(TypeError: expected string or bytes-like object). Reparado: se pasa el texto y `trabajar`
normaliza la caja por si acaso. Esta vigia atrapa que no vuelva a pasar.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cuerpo import obrero  # noqa: E402


def _caja():
    """Un paquete en forma de CAJA (dict), como el que mandaba el comando 'equipo'."""
    return {"apodo": "dmm", "problema": "p", "flujos": [], "raiz": "x", "leyes": [],
            "codigo": [], "trozos": [], "vigias": [], "dana": [], "total_proyecto": 10}


def test_no_cae_cuando_le_mandan_la_caja():
    """El freno recibe la caja y NO debe tirar TypeError (la normaliza a texto)."""
    r = obrero._validar_en_paquete(_caja(), {"archivo": "web/servidor.py"})
    assert isinstance(r, list), "el freno se cayo con la caja"


def test_trabajar_normaliza_la_caja():
    txt = open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8").read()
    assert "isinstance(paquete, str)" in txt, "trabajar no normaliza la caja a texto"


def test_el_comando_equipo_pasa_el_texto():
    txt = open(os.path.join(AQUI, "ingeniero.py"), encoding="utf-8").read()
    assert "a_texto(paq)" in txt, "el comando equipo sigue pasando la caja, no el texto"
