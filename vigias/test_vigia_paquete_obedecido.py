# -*- coding: utf-8 -*-
"""VIGIA — EL EQUIPO USA LA MEMORIA DEL PAQUETE, NO INVENTA (Julio, 2026-08-24).

Julio: "que usen la memoria indexada, los paquetes, para que no vuelvan a rechazar trabajo o
hacer lo que se les de la gana."

El freno `obrero._validar_en_paquete` comprueba que todo archivo que el modelo nombra este
DECLARADO en el paquete. Si inventa uno, se marca y no se deja pasar. Esta vigia comprueba que el
freno muerde de verdad:
  · deja pasar lo que SI esta en el paquete,
  · marca lo que el modelo invento,
  · y la orden al modelo dice que use SOLO la memoria del paquete.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "cuerpo"))
from cuerpo import obrero  # noqa: E402

PAQUETE = (
    "# PAQUETE MINIMO\n"
    "### `web/servidor.py` — 100 lineas\n"
    "### `web/pantalla.py` — 50 lineas\n"
    "### `cuerpo/perfil.py` — 30 lineas\n"
)


def test_deja_pasar_lo_que_si_esta_en_el_paquete():
    assert obrero._validar_en_paquete(PAQUETE, {"archivo": "web/servidor.py"}) == []
    assert obrero._validar_en_paquete(PAQUETE, {"archivo": "cuerpo/perfil.py"}) == []


def test_marca_lo_que_el_modelo_invento():
    r = obrero._validar_en_paquete(PAQUETE, {"archivo": "web/inventado.py"})
    assert "inventado.py" in r, "no marco un archivo que no esta en el paquete"


def test_marca_archivos_que_nombra_en_el_cambio():
    r = obrero._validar_en_paquete(PAQUETE, {"cambio": "tocar cuerpo/otro.py y web/servidor.py"})
    assert "otro.py" in r, "no marco el archivo inventado en el cambio"
    assert "servidor.py" not in r, "marco un archivo que SI estaba declarado"


def test_la_orden_dice_usar_solo_la_memoria_del_paquete():
    txt = open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8").read()
    assert "SOLO con la memoria del PAQUETE" in txt, "la orden no dice usar solo el paquete"
    assert "NECESITO_LEER" in txt, "falta como pedir material que no esta"


def test_el_freno_esta_conectado_al_trabajo():
    txt = open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8").read()
    assert "_validar_en_paquete" in txt, "el freno no esta en el obrero"
    assert "_fuera_del_paquete" in txt, "el freno no marca lo inventado en el trabajo"
