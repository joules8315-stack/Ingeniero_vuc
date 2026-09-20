# -*- coding: utf-8 -*-
"""vigias/test_vigia_una_prueba_no_escribe_en_la_memoria.py — VIGIA

Que vigila (fallo real del 2026-09-20):

    Una vigia que corria el cruzado con cerebros de mentira dejo un apunte de mentira en la
    memoria de fallos DE VERDAD. Ese apunte enveneno la memoria y puso ROJA otra vigia
    distinta, que no tenia nada que ver con la prueba.

La cura ya esta puesta en cuerpo/cruzado.py: si el entorno trae la senal de que hay una
prueba corriendo (PYTEST_CURRENT_TEST), el cruzado NO apunta nada en la memoria de fallos.

Esta vigia sujeta esa cura para que nadie la quite: corre el cruzado con cerebros de mentira
y con un apuntar falso que solo llena una lista en memoria, y exige que esa lista quede VACIA.
Si alguien quita el candado de cruzado.py, esta vigia se pone roja.

NO VOLVER A: dejar que una prueba escriba en la memoria de verdad.
"""
import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARNES = os.path.join(RAIZ, "arnes")
for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cuerpo import cruzado, obrero  # noqa: E402
from arnes import juez_de_la_prueba  # noqa: E402


def test_una_prueba_no_escribe_en_la_memoria(monkeypatch):
    """Una prueba NUNCA puede escribir en la memoria de fallos de verdad."""

    # 1) Cerebros de mentira: nadie llama a ninguna IA de verdad.
    def disponible_falso():
        return (True, "cerebro de mentira")

    monkeypatch.setattr(obrero, "disponible", disponible_falso)

    def _preguntar_con_relevo_falso(pedido, *args, **kwargs):
        pedido = pedido or ""
        if "VIGILANTE" in pedido:
            cuerpo = {
                "archivo_vigia": "vigias/test_de_mentira.py",
                "no_vale_si": "nada",
                "prueba": "def test_de_mentira():\n    assert True\n",
            }
        elif "JUEZ" in pedido:
            cuerpo = {
                "veredicto": "APROBADO",
                "invento_algo": False,
                "fallos": [],
                "que_le_falta": "",
                "resumen_para_el_jefe": "mentira de prueba",
            }
        else:
            cuerpo = {
                "archivo": "a.py",
                "diagnostico": "mentira de prueba",
                "texto_viejo": "x = 1\n",
                "texto_nuevo": "x = 2\n",
            }
        return (json.dumps(cuerpo, ensure_ascii=False), "cerebro de mentira", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", _preguntar_con_relevo_falso)

    # 2) El juez de la prueba tambien es de mentira: no toca el disco.
    def juzgar_con_vecinas_falso(*args, **kwargs):
        return {"ok": True, "razon": "mentira de prueba"}

    monkeypatch.setattr(juez_de_la_prueba, "juzgar_con_vecinas", juzgar_con_vecinas_falso)

    # 3) El apuntar de verdad se sustituye por uno que solo llena una lista.
    apuntes = []

    def apuntar_falso(*args, **kwargs):
        apuntes.append((args, kwargs))
        return None

    monkeypatch.setattr(cruzado.fallos, "apuntar", apuntar_falso)

    # 4) Se corre el cruzado entero con cerebros de mentira.
    cruzado.resolver("paquete de mentira", "problema de mentira", rondas=1)

    # 5) La lista tiene que quedar VACIA: la prueba no escribe en la memoria de verdad.
    assert apuntes == [], (
        "Una prueba NUNCA puede escribir en la memoria de fallos de verdad: la envenena "
        "y pone rojas a otras vigias que no tienen nada que ver."
    )
