# -*- coding: utf-8 -*-
"""VIGIA — EQUIPO TOTAL, SIN SALTO, EN TODAS LAS IA (bloque B1, legislacion 2026-08-24).

Julio, 2026-08-24: que el candado de equipo aplique a TODAS las IA (Claude, Cline, ChatGPT) y que
para saltarlo se pida permiso con respuesta SIEMPRE "denegado". Se trabaja siempre en equipo.

Comprueba:
  · la ley esta escrita donde la leen todas las IA (PROTOCOLO_UNICO.md y CLAUDE.md),
  · el candado de equipo NO ofrece ningun salto (solo exige veredicto),
  · Cline (yo) queda obligado por una regla propia (.clinerules),
  · el candado de equipo muerde de verdad (bloquea codigo sin veredicto fresco).
"""
import os
import sys
import json
import subprocess

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_ley_escrita_donde_la_leen_todas_las_ia():
    """La ley de 'siempre en equipo, sin salto' tiene que estar en PROTOCOLO y en CLAUDE.md."""
    for doc in ("PROTOCOLO_UNICO.md", "CLAUDE.md"):
        txt = _leer(os.path.join(AQUI, doc)).lower()
        assert "equipo" in txt, f"{doc} no menciona trabajar en equipo"
        assert "denegado" in txt, f"{doc} no dice que el salto se responde SIEMPRE denegado"


def test_candado_equipo_no_ofrece_salto():
    """El candado de equipo no debe tener ninguna llave de permiso: solo veredicto lo abre."""
    txt = _leer(os.path.join(AQUI, "arnes", "candado_equipo.py"))
    assert "veredicto" in txt, "el candado de equipo no exige veredicto"
    assert "permiso_editar" not in txt, "el candado de equipo tiene un salto por permiso"


def test_cline_queda_obligado_por_regla_propia():
    """Yo (Cline) tambien estoy obligado: existe una regla propia que me ata al equipo."""
    ruta = os.path.join(AQUI, ".clinerules", "equipo_y_pruebas.md")
    assert os.path.exists(ruta), "falta la regla que obliga a Cline"
    txt = _leer(ruta).lower()
    assert "denegado" in txt, "la regla de Cline no dice que el salto se responde denegado"
    assert "equipo" in txt, "la regla de Cline no exige trabajar en equipo"


def test_candado_equipo_muerde_sin_veredicto():
    """Con codigo y sin veredicto fresco del equipo, el candado bloquea."""
    from cerebro import grafo
    d = grafo.proyectos().get("dmm")
    if not d or not os.path.isdir(d["ruta"]):
        pytest.skip("dmm no esta")
    f = os.path.join(d["ruta"], "cuerpo", "precios.py")
    if not os.path.exists(f):
        pytest.skip("no existe precios.py")
    env = dict(os.environ)
    p = subprocess.run(
        [sys.executable, os.path.join(AQUI, "arnes", "candado_equipo.py")],
        input=json.dumps({"tool_input": {"file_path": f}}),
        capture_output=True, text=True, env=env, timeout=120)
    assert p.returncode == 2, "dejo reescribir codigo sin veredicto del equipo"
