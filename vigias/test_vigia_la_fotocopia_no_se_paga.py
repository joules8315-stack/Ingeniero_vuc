# -*- coding: utf-8 -*-
"""VIGIA — LA FOTOCOPIA NO SE PAGA. Si el texto ya viene decidido, lo aplica un PROGRAMA.

LEY: CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md (Julio, 2026-09-08). Julio lo repitio varias veces:
"quedo que lo que se podia hacer con programa, se hacia, asi salia gratis. Que pasa, otra vez
lo tengo que repetir?". Y al pillarlo: "legisla bien esa mierda, ponle candado, vigia, y mira
que se cumpla, que no se te olvide en la puta vida".

LO MEDIDO ESE DIA, el mismo cambio de las dos maneras:
    con el equipo de IA .... 4 rondas y NO entro (se comio las comillas, no encontro el texto
                             por una raya larga, y en dos rondas se autoauditio)
    con el programa ........ 1 segundo, entro a la primera, coste CERO

Y arnes/copista.py, hecho JUSTO para esto, llevaba meses dormido porque ESTABA ROTO: al
lanzarlo como dice su propia documentacion reventaba al arrancar. Construido, probado, dormido
y averiado.

ESTA VIGIA COMPRUEBA LAS TRES COSAS:
  1. que el copista ARRANCA solo, como lo lanzaria cualquiera, sin saber ponerle el camino;
  2. que el candado FRENA un encargo que ya trae el texto viejo y el nuevo exactos;
  3. que el candado DEJA PASAR un encargo de juicio de verdad. Un candado que frena lo legitimo
     ensena a ignorarlos todos, y eso es peor que no tenerlo.
"""
import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

COPISTA = os.path.join(AQUI, "arnes", "copista.py")

UNA_FOTOCOPIA = "\n".join([
    "en cuerpo/ejemplo.py hay que cambiar una linea.",
    "TEXTO VIEJO EXACTO:",
    "    hid = hipotesis.registrar(h)",
    "TEXTO NUEVO EXACTO:",
    "    hid = definir_test(e, h, m)",
])

UN_JUICIO = "\n".join([
    "en cuerpo/ejemplo.py la pantalla va lenta al abrirse y no sabemos por que.",
    "Hay que averiguar que la esta frenando y proponer como arreglarlo sin romper vecinos.",
])


def test_el_copista_arranca_solo_sin_que_le_pongan_el_camino():
    """Se lanza como lo lanzaria cualquiera. Si revienta al arrancar, esta dormido para siempre."""
    if not os.path.exists(COPISTA):
        pytest.skip("no esta el copista en esta maquina: no se falsea un verde")
    limpio = dict(os.environ)
    limpio.pop("PYTHONPATH", None)          # como lo lanzaria alguien que no sabe del tema
    r = subprocess.run([sys.executable, COPISTA], cwd=AQUI, env=limpio,
                       capture_output=True, text=True, timeout=120)
    salida = (r.stdout or "") + (r.stderr or "")
    assert "No module named" not in salida, (
        "EL COPISTA REVIENTA AL ARRANCAR: %s. Por eso lleva meses dormido: nadie lo uso nunca "
        "porque al primer intento se rompe. Una pieza no esta terminada hasta que se ha USADO "
        "una vez de verdad." % salida.strip()[:160])


def _candado():
    try:
        import candado_terminal
    except ImportError:
        pytest.fail("NO EXISTE arnes/candado_terminal.py, que es donde vive este freno")
    if not hasattr(candado_terminal, "es_una_fotocopia"):
        pytest.fail(
            "EL CANDADO NO SABE DISTINGUIR UNA FOTOCOPIA. Falta es_una_fotocopia(texto): sin "
            "eso, la ley de que la fotocopia no se paga es papel, y Julio va a tener que "
            "repetirlo otra vez.")
    return candado_terminal


def test_frena_la_fotocopia():
    """Un encargo que ya trae el texto de antes y el de despues es una fotocopia: no se paga."""
    c = _candado()
    assert c.es_una_fotocopia(UNA_FOTOCOPIA), (
        "NO CAZO LA FOTOCOPIA. Ese encargo ya trae el texto viejo y el nuevo exactos: no hay "
        "nada que pensar, solo que copiar. Mandarlo a una IA es pagar por una fotocopiadora.")


def test_deja_pasar_el_trabajo_de_juicio():
    """Averiguar POR QUE algo falla es juicio: eso si es trabajo de cerebro y tiene que pasar."""
    c = _candado()
    assert not c.es_una_fotocopia(UN_JUICIO), (
        "FRENO EN FALSO un encargo de juicio de verdad. Un candado que frena lo legitimo es "
        "PEOR que no tenerlo, porque ensena a ignorarlos todos.")
