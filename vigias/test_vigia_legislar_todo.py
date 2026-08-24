# -*- coding: utf-8 -*-
"""VIGIA — LEY L5: TODO LO QUE SE HABLA SE LEGISLA, CON CANDADO Y VIGIA.

Julio, 2026-08-24: "legisla, que todo lo que se hable, se legisla, se pone candado y se crea
vigia, que ademas no rompa lo que ya sirve."

Comprueba que cada candado del arnes tiene su vigia que lo protege, y que las leyes estan escritas
donde las leen todas las IA (no son deseos sueltos).
"""
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARNES = os.path.join(AQUI, "arnes")
VIGIAS = os.path.join(AQUI, "vigias")


def _textos_vigias():
    t = []
    for f in os.listdir(VIGIAS):
        if f.endswith(".py"):
            try:
                t.append(open(os.path.join(VIGIAS, f), encoding="utf-8", errors="ignore").read())
            except Exception:
                pass
    return " ".join(t)


def test_todo_candado_tiene_vigia():
    """Cada candado del arnes debe estar referenciado en el CONTENIDO de al menos una vigia."""
    textos = _textos_vigias()
    biblioteca = {"medir_capacidad", "settings_propuesto", "instalar", "llamar", "canal",
                  "supervisor", "permiso_editar", "via_canonica", "velocidad", "respaldos",
                  "candado_diagnostico", "candado_preguntar"}
    faltan = []
    for f in sorted(os.listdir(ARNES)):
        if not f.endswith(".py") or f.startswith("__"):
            continue
        nombre = f[:-3]
        if nombre in biblioteca:
            continue
        if nombre not in textos:
            faltan.append(f)
    assert not faltan, "candados SIN vigia: " + ", ".join(faltan)


def test_las_leyes_estan_escritas_donde_las_leen_todas():
    proto = open(os.path.join(AQUI, "PROTOCOLO_UNICO.md"), encoding="utf-8", errors="ignore").read()
    claude = open(os.path.join(AQUI, "CLAUDE.md"), encoding="utf-8", errors="ignore").read()
    assert "legisla" in proto.lower(), "PROTOCOLO no legisla"
    assert "vigia" in claude.lower(), "CLAUDE.md no exige vigia"


def test_no_se_rompe_lo_que_sirve():
    """Cross-flow: los candados clave compilan."""
    import importlib
    for m in ("read_gate", "edit_gate_universal", "candado_equipo", "candado_prueba_real",
              "candado_terminal"):
        try:
            importlib.import_module(m)
        except Exception as e:
            assert False, f"el candado {m} no importa: {e}"
