# -*- coding: utf-8 -*-
"""VIGIA — LO QUE JULIO DICE SE APUNTA SOLO, SIN QUE NADIE SE ACUERDE.

Julio, 2026-08-31, enfadado y con razon:
  "legisla lo que te dije, porque te digo cosas y no las legislas, esa es una ley y no se cumple"
  "verifica porque no se esta cumpliendo mi orden, que todo lo que yo diga, sin excepcion, debe
   ser legislado"

LA CAUSA RAIZ, MEDIDA ESE DIA:
  El candado `candado_legislar` existe, funciona y esta conectado al candado de cierre: si hay
  instrucciones apuntadas sin legislar, BLOQUEA. Eso funciona.
  Lo que NO existia es quien APUNTA. Las instrucciones solo entraban si alguien llamaba a mano a
  `apuntar()`. O sea: la ley dependia de que la IA se acordara.

  Y esa leccion ya estaba pagada, escrita en la propia memoria de fallos del sistema:
  "La regla estaba escrita en la memoria y en el protocolo, pero escrita no es cumplida: dependia
   de que la IA se acordara."

  Un candado que solo muerde lo que tu mismo le pones en la boca no muerde nada.

LO QUE SE MIDE
  1. Existe una forma de apuntar lo que dice Julio SIN que nadie se acuerde (automatica).
  2. Una orden suya de verdad se reconoce como orden.
  3. Un comentario suyo que no es orden NO se apunta (o el cierre se bloquearia siempre y se
     acabaria apagando el candado, que es peor que no tenerlo).
  4. Esta ENCHUFADA a la puerta por donde entra lo que Julio escribe.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

import candado_legislar as cl   # noqa: E402

ORDENES_DE_VERDAD = [
    "asignale tarea a cline, esa que no has podido resolver y despues la supervisas",
    "no vas a reparar el MVP, seguimos afinando el ingeniero",
    "siempre se cree mapa, que se asigne nombres a todo, y que se use el diccionario",
    "que se elimine esa instruccion y quede buscando por funcion y nombre",
    "no vuelvas a hacer eso de dejar pendiente",
]

NO_SON_ORDENES = [
    "gracias",
    "ok",
    "y eso por que pasa?",
    "no me queda claro, explicate y dime implicaciones?",
    "quien lo esta atendiendo, cline?",
]


def test_existe_quien_apunte_solo():
    """Sin esto, la ley depende de que la IA se acuerde. Y eso ya se probo que no funciona."""
    assert hasattr(cl, "apuntar_lo_que_dijo_julio"), (
        "no existe ninguna forma de apuntar SOLAS las instrucciones de Julio. El candado que "
        "bloquea el cierre existe, pero solo muerde lo que alguien le mete a mano: si nadie se "
        "acuerda, la ley no se cumple. Es lo que Julio lleva denunciando")


def test_reconoce_una_orden_de_verdad():
    for orden in ORDENES_DE_VERDAD:
        assert cl.parece_una_orden(orden), \
            "no reconoce como orden: %r" % orden[:70]


def test_no_apunta_lo_que_no_es_una_orden():
    """Si apunta todo, el cierre se bloquea siempre y se acaba apagando el candado.
    Un candado apagado protege menos que ninguno, porque encima da falsa seguridad."""
    for texto in NO_SON_ORDENES:
        assert not cl.parece_una_orden(texto), \
            "apunta como orden algo que no lo es: %r. Asi el candado se vuelve ruido" % texto[:60]


def test_esta_enchufado_donde_entra_lo_que_julio_escribe():
    """Escrito no es cumplido. Tiene que estar en la puerta por la que pasa lo que el dice."""
    sitios = [os.path.join(AQUI, ".claude", "settings.json"),
              os.path.join(AQUI, ".claude", "settings.local.json")]
    texto = ""
    for s in sitios:
        if os.path.exists(s):
            with open(s, encoding="utf-8", errors="ignore") as f:
                texto += f.read()
    assert "UserPromptSubmit" in texto and "candado_legislar" in texto, (
        "el apuntador no esta enchufado a la puerta por donde entra lo que Julio escribe. "
        "Mientras no lo este, sus instrucciones siguen dependiendo de que alguien se acuerde")
