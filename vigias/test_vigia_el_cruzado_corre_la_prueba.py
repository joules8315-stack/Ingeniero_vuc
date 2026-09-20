# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_cruzado_corre_la_prueba.py — VIGIA (nace ROJA a proposito).

Vigila DOS cosas de cuerpo/cruzado.py, que hoy no hace ninguna:

  1) Que el cruzado CORRA la prueba de verdad, en vez de preguntarle a una IA si la
     reparacion la pasaria.
  2) Que el codigo 2 del juez del cruzado ('NO PASA LA PRUEBA') sea CUENTA, no JUICIO.

MOTIVO (plan v4 P2-5, orden A-39 de Julio):

  El codigo 2 del juez del cruzado ('NO PASA LA PRUEBA') es CUENTA, no JUICIO. Correr la
  prueba es una cuenta que el programa puede hacer solo. Adivinarla con una IA cuesta
  dinero y ademas se equivoca. Por eso el cruzado tiene que EJECUTAR la prueba
  (arnes.juez_de_la_prueba.juzgar_con_vecinas) y no pedirle a un cerebro que adivine si
  la reparacion pasaria.

Este archivo nace ROJO: hoy cuerpo/cruzado.py no menciona juzgar_con_vecinas y le paga
una IA (obrero._preguntar_con_relevo) para que adivine el veredicto del JUEZ.
"""
import os
import sys
import json

# Raiz del proyecto: dos dirname sobre el abspath de este mismo archivo.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")
for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cuerpo import cruzado, obrero   # noqa: E402


RUTA_CRUZADO = os.path.join(RAIZ, "cuerpo", "cruzado.py")


def test_el_cruzado_menciona_juzgar_con_vecinas():
    """PRIMERA prueba: solo texto, sin ejecutar nada.

    Si cuerpo/cruzado.py no menciona juzgar_con_vecinas, es que el cruzado NO corre la
    prueba: le paga a una IA para que adivine si la reparacion la pasaria.
    """
    with open(RUTA_CRUZADO, "r", encoding="utf-8") as f:
        texto = f.read()
    assert "juzgar_con_vecinas" in texto, (
        "El cruzado NO corre la prueba: no menciona juzgar_con_vecinas en cuerpo/cruzado.py. "
        "Por eso le paga a una IA para que adivine si la reparacion pasa la prueba, "
        "cuando correrla es una CUENTA que el programa puede hacer solo."
    )


def test_el_cruzado_no_le_paga_a_una_ia_para_adivinar_el_veredicto(monkeypatch):
    """SEGUNDA prueba: el cruzado corre la prueba y NO le pregunta a una IA por el JUEZ.

    Se falsea obrero.disponible, obrero._preguntar_con_relevo y
    arnes.juez_de_la_prueba.juzgar_con_vecinas. Si el cruzado corre la prueba, la lista
    de pedidos al JUEZ queda VACIA.
    """
    pedidos_al_juez = []
    pedidos_totales = []

    def falso_disponible():
        return (True, "falso")

    def falso_preguntar_con_relevo(pedido, *args, **kwargs):
        pedidos_totales.append(pedido)
        texto = pedido if isinstance(pedido, str) else str(pedido)
        if "VIGILANTE" in texto:
            prueba = {
                "archivo_vigia": "vigias/test_falso.py",
                "prueba": "assert True",
                "no_vale_si": "nada",
            }
            return (json.dumps(prueba, ensure_ascii=False), "falso", [])
        if "JUEZ" in texto:
            pedidos_al_juez.append(texto)
            veredicto = {"veredicto": "APROBADO", "fallos": [], "que_le_falta": ""}
            return (json.dumps(veredicto, ensure_ascii=False), "falso", [])
        reparacion = {
            "archivo": "cuerpo/falso.py",
            "texto_viejo": "viejo",
            "texto_nuevo": "nuevo",
            "diagnostico": "falso",
            "cambio": "falso",
        }
        return (json.dumps(reparacion, ensure_ascii=False), "falso", [])

    def falso_juzgar_con_vecinas(*args, **kwargs):
        return {"ok": True, "razon": "la prueba corre y pasa"}

    monkeypatch.setattr(obrero, "disponible", falso_disponible)
    monkeypatch.setattr(obrero, "_preguntar_con_relevo", falso_preguntar_con_relevo)

    import arnes.juez_de_la_prueba as juez_de_la_prueba
    monkeypatch.setattr(juez_de_la_prueba, "juzgar_con_vecinas", falso_juzgar_con_vecinas)

    cruzado.resolver("paquete de prueba", "problema de prueba", rondas=1)

    assert pedidos_al_juez == [], (
        "Se le pago a una IA para adivinar si la prueba pasa, cuando el programa ya la "
        "habia corrido. El veredicto del JUEZ es CUENTA, no JUICIO: el cruzado debe correr "
        "la prueba con juzgar_con_vecinas y no preguntarle a un cerebro."
    )
