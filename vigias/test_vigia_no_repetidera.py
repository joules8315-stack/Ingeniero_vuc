# -*- coding: utf-8 -*-
"""VIGIA 5 — NO REPETIDERA (Ley 6).

Antecedente real: C:\vigias tenia 52 vigias duplicadas de la carpeta buena. Nadie se dio cuenta
durante meses y las IA reparaban la copia equivocada. Esta vigia mira que no vuelva a pasar.
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import grafo, piezas

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_el_ingeniero_no_tiene_dos_piezas_identicas():
    f = piezas.escanear(AQUI)
    # los __init__.py vacios SON identicos por naturaleza: no es repetidera, es Python.
    codigo = [p for p in f if p["id"].endswith(".py")
              and "memoria/rescate" not in p["id"]
              and not p["id"].endswith("__init__.py")
              and p["bytes"] > 0]
    por_hash = {}
    for p in codigo:
        por_hash.setdefault(p["md5"], []).append(p["id"])
    dup = {h: v for h, v in por_hash.items() if len(v) > 1}
    assert not dup, f"hay piezas identicas duplicadas: {list(dup.values())}"


def test_la_copia_vieja_de_vigias_sigue_desechada():
    assert not os.path.isdir(r"C:\vigias"), \
        "volvio a aparecer C:\vigias. Se desecho el 2026-08-20 (respaldo en memoria/rescate)."


def test_cada_capa_del_cerebro_existe_una_sola_vez():
    """Ley 2: las capas no se eliminan... ni se duplican en otro nombre."""
    # `semantico.py` se declaro el 2026-08-20 (LEY 17): busca por significado, no por letras.
    # Esta vigia se puso ROJA en cuanto la pieza aparecio sin declarar, que es justo su trabajo:
    # que no crezca el cerebro con piezas que nadie legislo.
    # `protocolo.py` se declaro el 2026-08-20 (LEY 20): es el grafo de la FORMA DE TRABAJO
    # (los 8 pasos y sus candados), no del codigo. Esta vigia se puso ROJA en cuanto aparecio
    # sin declarar, que es exactamente su trabajo.
    capas = ["piezas.py", "enlaces.py", "flujos.py", "trozos.py", "grafo.py", "router.py",
             "semantico.py", "protocolo.py"]
    hay = os.listdir(os.path.join(AQUI, "cerebro"))
    for c in capas:
        assert c in hay, f"falta la capa {c} (Ley 2: ninguna capa se elimina)"
    sospechosos = [h for h in hay if h.endswith(".py") and h not in capas + ["__init__.py"]]
    assert not sospechosos, f"piezas de cerebro no declaradas en el contrato: {sospechosos}"
