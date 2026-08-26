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
    """Solo veredicto del equipo (o autorizacion de Julio) abren el candado. NINGUNA otra puerta.

    Julio, 2026-08-26: la salida de emergencia NECESITO_EDITAR / permiso_editar se volvio la
    ENTRADA PRINCIPAL — todas las IA se salieron por ahi y trabajaron a solas. Quedo cerrada de
    raiz. Un candado de equipo que deja a un agente escribirse el permiso a si mismo no es candado.
    """
    eq = _leer(os.path.join(AQUI, "arnes", "candado_equipo.py"))
    assert "veredicto" in eq, "el candado de equipo no exige veredicto"
    for nombre in ("candado_equipo.py", "edit_gate_universal.py"):
        txt = _leer(os.path.join(AQUI, "arnes", nombre))
        assert "hay_permiso" not in txt, (
            "%s NO debe honrar permisos de edicion (NECESITO_EDITAR): se volvio la entrada "
            "principal para trabajar a solas (Julio, 2026-08-26)" % nombre)
        assert "import permiso_editar" not in txt, (
            "%s no debe importar permiso_editar: la puerta quedo cerrada de raiz" % nombre)


def test_la_llave_retirada_jamas_abre():
    """permiso_editar quedo RETIRADO: hay_permiso siempre responde False, nada abre."""
    import permiso_editar
    assert permiso_editar.hay_permiso(r"C:\cualquier\archivo.py") is False, \
        "la llave retirada (permiso_editar) volvio a abrir: se queda cerrada SIEMPRE"


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
