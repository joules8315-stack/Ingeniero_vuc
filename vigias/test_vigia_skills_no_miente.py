# -*- coding: utf-8 -*-
"""VIGIA 7 — EL BUSCADOR DE HABILIDADES NO MIENTE (orden 4 de Julio).

Decirle a Julio "eso ya lo escribiste" sobre algo que nunca escribio es tan grave como
inventarse un archivo: lo manda a buscar humo y le hace perder el tiempo.

Casos sacados de fallos REALES del 2026-08-20:
  · "telegram" traia trozos de metricas_reales.py (por la palabra "canal")
  · "generar un codigo QR" traia 4 trozos cualesquiera (porque "qr" tiene 2 letras y se
    descartaba, dejando la busqueda sin nada que exigir)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import skills
from cerebro import grafo


def _hay_proyectos():
    return any(os.path.isdir(p["ruta"]) for p in grafo.proyectos().values())


def test_lo_que_si_existe_lo_encuentra():
    """docx SI esta en los proyectos de Julio y python-docx SI esta instalada."""
    if not _hay_proyectos():
        pytest.skip("no hay proyectos en esta maquina")
    r = skills.buscar("rellenar una plantilla docx de Word")
    assert r["librerias"], "no vio la libreria python-docx"
    assert any(x["libreria"] == "python-docx" for x in r["librerias"])


def test_lo_que_no_existe_NO_lo_inventa():
    """Julio nunca hizo nada de codigos QR: no puede decirle que ya lo escribio."""
    if not _hay_proyectos():
        pytest.skip("no hay proyectos en esta maquina")
    r = skills.buscar("generar un codigo QR")
    assert not r["en_proyectos"], \
        f"dijo que Julio ya lo escribio, y no es cierto: {r['en_proyectos']}"
    assert r["librerias"], "deberia proponer la libreria qrcode en vez de inventar"


def test_cuando_no_hay_nada_lo_dice_claro():
    r = skills.buscar("zzzqqq xyzzy habilidad que no existe en ningun lado")
    txt = skills.informe(r)
    assert "NO_ENCONTRADO" in txt or not r["en_proyectos"]


def test_avisa_si_la_libreria_falta_por_instalar():
    r = skills.buscar("generar un codigo QR")
    for lib in r["librerias"]:
        if not lib["instalada"]:
            assert any("pip install" in c for c in r["faltan"]), "no dijo como instalarla"


def test_no_crea_si_ya_existe(tmp_path, monkeypatch):
    """Ley 6: antes de crear, se busca. Si ya hay algo que sirve, NO se crea otra cosa."""
    monkeypatch.setattr(skills, "SKILLS", str(tmp_path))
    r = skills.crear("leer_word", "leer archivos docx de Word")
    assert "_error" in r and "no repetidera" in r["_error"].lower(), \
        "creo una habilidad nueva cuando python-docx ya hace eso"
