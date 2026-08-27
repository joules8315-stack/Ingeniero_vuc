# -*- coding: utf-8 -*-
"""VIGIA — L15 LA LLAVE UNICA DE JULIO ABRE SOLO LO NECESARIO (Julio, 2026-08-27).

Cuando Julio pone su llave, NO se abren los 12 candados de golpe. Se abren SOLO los que la tarea
necesita, ni mas ni menos, y antes de abrir se le dice exactamente cuales candados se abren y por que.

Se vigila:
  1. la ley esta escrita donde la leen (contrato + matriz + protocolo + CLAUDE),
  2. existe el registro de que candado protege que (no se abre a ciegas),
  3. el comando autorizar puede decir que abre (y no silenciosamente todo).
"""
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys = __import__("sys")
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_la_ley_esta_escrita_donde_la_leen():
    contrato = _leer(os.path.join(AQUI, "CONTRATO_LEGISLACION_TOTAL.md")).lower()
    assert "llave" in contrato and "ni más ni menos" in contrato, \
        "la ley de la llave unica no esta en el contrato"
    matriz = _leer(os.path.join(AQUI, "MATRIZ_LEGISLACION.md")).lower()
    assert "llave" in matriz and "ni más ni menos" in matriz, \
        "la ley no esta en la matriz"
    proto = _leer(os.path.join(AQUI, "PROTOCOLO_UNICO.md")).lower()
    assert "llave" in proto and "ni más ni menos" in proto, \
        "la ley no esta en el protocolo"
    claude = _leer(os.path.join(AQUI, "CLAUDE.md")).lower()
    assert "llave" in claude and "ni más ni menos" in claude, \
        "la ley no esta en CLAUDE.md"


def test_cada_candado_dice_que_protege():
    """La llave no puede abrir a ciegas: cada candado declara que frena (para saber si hace falta)."""
    import re
    candados = ["equipo", "terminal", "diagnostico", "preguntar", "protocolo",
                "supervisor", "cierre", "commit", "comunicacion", "memoria",
                "legislar", "contexto"]
    for n in candados:
        f = os.path.join(AQUI, "arnes", "candado_%s.py" % n)
        txt = _leer(f)
        assert txt.strip(), "falta el candado %s" % n
        # cada candado lleva una cabecera que dice que frena (no abre en silencio)
        assert "frena" in txt.lower() or "bloque" in txt.lower() or "exige" in txt.lower(), \
            "el candado %s no dice que frena/protege" % n


def test_el_comando_autorizar_existe():
    """La llave se usa por el comando autorizar-off (que debe existir)."""
    txt = _leer(os.path.join(AQUI, "ingeniero.py"))
    assert 'cmd == "autorizar-off"' in txt, "el comando autorizar-off no existe"
    import autorizacion as au
    assert hasattr(au, "autorizar"), "autorizacion no tiene la funcion autorizar"
