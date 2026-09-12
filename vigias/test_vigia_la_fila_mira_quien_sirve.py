# -*- coding: utf-8 -*-
"""VIGIA — LA FILA DE CEREBROS MIRA QUIEN SIRVE, NO SOLO QUIEN ESTA LIBRE.

CAUSA RAIZ MEDIDA EL 2026-09-12, despues de que Julio preguntara por que el equipo fallo cinco
veces seguidas. No fue el equipo. Fueron DOS CEREBROS CONCRETOS:

    quien escribio    aprobado   rechazado   acierto
    gemini4               0          4          0%
    groq                  0          2          0%
    deepseek              5          3         62%

Y NO ES COSA DE UN DIA: gemini4 lleva 1 acierto de 8 en toda su historia, y el sistema le seguia
dando trabajo de escribir. Esperar no lo arregla; manana volveria a elegirlo.

EL PORQUE: cuotas.ORDEN es una lista ESCRITA A MANO. La fila se hace por ese orden y por quien
esta despierto. NADIE mira si el cerebro acierta. Es el mismo fallo que el nombre del companero
escrito a mano y que los numeros de linea escritos a mano: lo que hay que saber se le pregunta a
quien lo sabe, no se congela dentro del codigo.

Y LA CURA YA EXISTIA Y ESTABA DORMIDA: skills/quien_sirve_de_verdad.py mide el acierto real de
cada uno, en trabajo real, sin gastar ni una llamada. Su propia ley lo dice: "antes de mandarle
algo a uno que falla mucho, se mira esta tabla". Nadie la miraba.

LO QUE SE EXIGE:
  1. que la fila PREGUNTE por el acierto (con espia, no por la palabra)
  2. que el orden lo mande el ACIERTO y no la lista escrita a mano: si los datos dicen lo
     contrario que la lista, mandan los datos
  3. que NADIE se quede fuera: el que falla mucho va al final, no se le expulsa, porque el dia
     que los buenos esten agotados sigue siendo mejor que nada
  4. que SIN DATOS la fila quede EXACTAMENTE como estaba: sin informacion no se reordena a
     ciegas, porque adivinar es peor que no tocar nada

LO QUE ESTA VIGIA NO TOCA: la regla de que el de pago va aparte y solo cuando ningun gratis pudo.
Eso se aplica despues, en otro sitio, y sigue igual. Aqui solo se ordena la fila.

COMO SE PRUEBA: se EJECUTA la fila de verdad con los aciertos puestos a mano. No se llama a
ningun cerebro y sale lo mismo las mil veces.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)


def _cuotas():
    from cuerpo import cuotas
    return cuotas


def test_la_fila_PREGUNTA_por_el_acierto(monkeypatch):
    """NACE CONECTADA O NO NACE: con espia, se comprueba que lo pregunta de verdad."""
    c = _cuotas()
    visto = []
    monkeypatch.setattr(c, "acierto_de", lambda quien: visto.append(quien) or None,
                        raising=False)
    monkeypatch.setattr(c, "desperto", lambda quien: True, raising=False)
    c.fila(["groq", "gemini4"])
    assert visto, (
        "LA FILA NO PREGUNTA POR EL ACIERTO DE NADIE: sigue eligiendo por el orden escrito a mano "
        "y por quien esta libre. Es la causa medida de los cinco rechazos, y la pieza que lo "
        "mide (quien_sirve_de_verdad) sigue dormida")


def test_MANDAN_LOS_DATOS_y_no_la_lista_escrita_a_mano(monkeypatch):
    """Si el acierto dice lo contrario que la lista, manda el acierto.

    Se ponen los aciertos AL REVES de como estan en la lista a mano: si la fila sale al reves de
    la lista, es que de verdad esta mirando los datos y no repitiendo el orden de siempre.
    """
    c = _cuotas()
    monkeypatch.setattr(c, "desperto", lambda quien: True, raising=False)
    mano = [q for q in c.ORDEN if q in ("groq", "gemini4")]
    primero_a_mano, segundo_a_mano = mano[0], mano[1]
    aciertos = {primero_a_mano: 0.0, segundo_a_mano: 0.9}
    monkeypatch.setattr(c, "acierto_de", lambda quien: aciertos.get(quien), raising=False)
    orden = c.fila([primero_a_mano, segundo_a_mano])
    assert orden.index(segundo_a_mano) < orden.index(primero_a_mano), (
        "SIGUE MANDANDO LA LISTA ESCRITA A MANO. Con los datos diciendo que uno acierta el 90 por "
        "ciento y el otro el 0, la fila sigue poniendo primero al que falla. Eso es lo que costo "
        "cinco rondas seguidas. Quedo asi: %s" % orden)


def test_al_que_falla_NO_se_le_expulsa(monkeypatch):
    """Va al final, no a la calle: el dia que los buenos esten agotados, mejor que nada."""
    c = _cuotas()
    monkeypatch.setattr(c, "desperto", lambda quien: True, raising=False)
    monkeypatch.setattr(c, "acierto_de",
                        lambda quien: 0.0 if quien == "gemini4" else 0.9, raising=False)
    orden = c.fila(["groq", "gemini4"])
    assert "gemini4" in orden, (
        "EXPULSO al que falla en vez de ponerlo al final. El dia que los que aciertan esten "
        "agotados, uno que falla mucho sigue siendo mejor que quedarse sin nadie")


def test_SIN_DATOS_la_fila_queda_como_estaba(monkeypatch):
    """Sin informacion no se reordena a ciegas: adivinar seria peor que no tocar nada."""
    c = _cuotas()
    monkeypatch.setattr(c, "acierto_de", lambda quien: None, raising=False)
    monkeypatch.setattr(c, "desperto", lambda quien: True, raising=False)
    pedidos = ["groq", "gemini4", "gemini2"]
    orden = c.fila(pedidos)
    esperado = [q for q in c.ORDEN if q in pedidos]
    assert orden == esperado, (
        "sin datos de acierto ha reordenado igual: eso es adivinar. Quedo %s y deberia quedar %s"
        % (orden, esperado))
