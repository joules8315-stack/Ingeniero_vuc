# -*- coding: utf-8 -*-
"""VIGIA — NO SE LE PIDE A UN CEREBRO QUE JUZGUE TRABAJO YA HECHO Y EN VERDE.

JULIO, 2026-09-09, rompiendo el bucle de un tajo:
"Ese es el punto: esta mal el flujo. Por que se le pide que juzgue algo que ya esta. Eso es
estupido. Debe pasar a EJECUTAR, no que lo juzguen. Lo que debe hacer, a lo sumo, es con un
PROGRAMA verificar que el pedido este bien hecho y lleve lo que se le pidio."

EL BUCLE QUE SE ROMPE, y ocurrio de verdad TRES VECES SEGUIDAS ese dia:
  se manda el trabajo a juzgar
  -> el cerebro, ahogado en relleno, contesta "tiene errores de sintaxis graves"
  -> se comprueba y es FALSO: el archivo compila y sus vigias pasan
  -> se vuelve a mandar
  -> otra vez lo mismo
Cada vuelta costaba dinero y no aportaba NADA. Y encima el veredicto era mentira.

POR QUE ERA ESTUPIDO PEDIRLO: la vigia YA dijo si funciona. Ese es el comparador, y su palabra
vale mas que una opinion. Preguntar despues "¿esto esta bien?" a un cerebro que no puede correr
el codigo es cambiar una medida por una adivinanza.

LO QUE SE HACE EN SU LUGAR: un PROGRAMA comprueba que el pedido este bien hecho. Gratis, al
instante y sin opinar. Mira tres cosas: que diga QUE se queria conseguir, que LLEVE DENTRO lo
que se pidio, y que QUEPA en un cerebro gratis. Si las tres estan, a ejecutar.

LO QUE NO CAMBIA: el equipo sigue siendo obligatorio para ESCRIBIR codigo, que es donde hay
juicio de verdad. Lo que se acaba es pedirle opinion sobre algo ya aplicado y verde.

LEY: CONTRATO_AL_CEREBRO_SOLO_LO_SUYO.md
"""
import os
import re
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _vivo(ruta):
    with open(ruta, encoding="utf-8") as f:
        codigo = f.read()
    codigo = re.sub(r'"""(?:.|\n)*?"""', " ", codigo)
    codigo = re.sub(r"'''(?:.|\n)*?'''", " ", codigo)
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in codigo.splitlines())


def test_juzgar_trabajo_hecho_no_llama_a_ningun_cerebro():
    """Si sigue llamando a un cerebro, el bucle sigue vivo y sigue costando dinero."""
    vivo = _vivo(os.path.join(AQUI, "ingeniero.py"))
    trozo = vivo.split('cmd == "juzga"')[-1].split('cmd == "aplicar-guardado"')[0]
    assert "auditar" not in trozo, (
        "SIGUE PIDIENDOLE A UN CEREBRO QUE JUZGUE ALGO YA HECHO Y VERDE. Eso es el bucle: el "
        "cerebro contesta que hay errores de sintaxis, se comprueba y es falso, se vuelve a "
        "mandar, y otra vez. Cada vuelta cuesta dinero y no aporta nada. La vigia YA dijo si "
        "funciona.")


def test_hay_un_programa_que_comprueba_el_pedido():
    """La pieza que sustituye al cerebro: comprobar, no opinar."""
    import asignador
    assert hasattr(asignador, "pedido_bien_hecho"), (
        "NO HAY QUIEN COMPRUEBE QUE EL PEDIDO ESTA BIEN HECHO. Sin eso, o se le pregunta a un "
        "cerebro (el bucle) o no se comprueba nada.")


def test_caza_un_pedido_sin_objetivo():
    """Sin decir que se queria conseguir, nadie puede hacer el trabajo ni saber si se logro."""
    import asignador
    ok, faltan = asignador.pedido_bien_hecho({"objetivo": "", "material": "def algo(): pass"})
    assert not ok, "dejo pasar un pedido que no dice que se queria conseguir"
    assert faltan, "no dijo QUE le faltaba: callarse no ayuda a arreglarlo"


def test_caza_un_pedido_que_no_lleva_lo_que_se_pidio():
    """Un pedido vacio hace que el cerebro conteste NO_ENCONTRADO habiendo cobrado la vuelta."""
    import asignador
    ok, faltan = asignador.pedido_bien_hecho({"objetivo": "que salga el embudo", "material": ""})
    assert not ok, (
        "DEJO PASAR UN PEDIDO SIN NADA DENTRO. El cerebro contestaria NO_ENCONTRADO y la vuelta "
        "ya estaria pagada.")


def test_caza_un_pedido_que_no_le_cabe_a_nadie():
    """Si no cabe, se les salta a todos en silencio y lo paga el de pago."""
    import asignador
    ok, faltan = asignador.pedido_bien_hecho(
        {"objetivo": "que salga el embudo", "material": "x" * 200000})
    assert not ok, (
        "DEJO PASAR UN PEDIDO QUE NO LE CABE A NADIE. Se les salta a los gratis sin decir nada "
        "y acaba contestando el de pago, que tampoco puede con el.")


def test_deja_pasar_un_pedido_bien_hecho():
    """Comprobar no puede convertirse en estorbar: lo que esta bien, pasa."""
    import asignador
    ok, faltan = asignador.pedido_bien_hecho(
        {"objetivo": "que la pantalla saque el embudo con datos reales",
         "material": "def armar_datos(perfil):\n    return {}\n"})
    assert ok, ("FRENO UN PEDIDO BIEN HECHO: dice que se queria, lleva el codigo dentro y cabe. "
                "Frenar lo bueno ensena a ignorar los frenos. Faltaba: %s" % (faltan,))
