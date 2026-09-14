# -*- coding: utf-8 -*-
"""VIGIA 10 — LA VIA CANONICA SE COMPRUEBA LO PRIMERO (orden de Julio, 2026-08-20).

  "que todas las rutas, ramas, vias canonicas, siempre se cumplan, que sea lo primero que
   verifique el ingeniero, que este trabajando donde debe, no en una version equivoca,
   y que guarde alli sus commit"

FALLO REAL que la motiva (mismo dia): el Ingeniero tenia declarado Foto Informe en
`C:\\MVP\\Foto_informe--main`, rama main, ultimo commit del 28 de MAYO, 57 archivos... habiendo
en `C:\\Users\\USER\\dev\\Foto_info_repo\\Foto_informe--main` la version del 23 de JULIO con 253.
Todas las pruebas del router se hicieron contra una copia dos meses vieja. Reparar ahi habria
sido arreglar algo que nadie usa.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest
import via_canonica
from cerebro import grafo


def test_todo_proyecto_declara_ruta_Y_rama():
    """Sin rama declarada no hay forma de saber si se esta guardando donde se debe."""
    for apodo, d in grafo.proyectos().items():
        assert d.get("ruta"), f"{apodo} no declara ruta"
        assert d.get("rama"), f"{apodo} no declara RAMA canonica: los commits pueden acabar en cualquier lado"


def test_la_rama_declarada_es_la_rama_real():
    for apodo, d in grafo.proyectos().items():
        if not os.path.isdir(d["ruta"]):
            continue
        real = via_canonica.rama_de(d["ruta"])
        if real == "SIN-GIT":
            continue
        assert real == d["rama"], (
            f"{apodo}: declara '{d['rama']}' pero esta en '{real}'. "
            f"Guardar commits en la rama equivocada es perder el trabajo.")


def test_ninguna_via_declarada_es_mas_vieja_que_su_gemela():
    """El corazon de la ley: si hay copias, la declarada tiene que ser la BUENA."""
    malas = []
    for apodo, d in grafo.proyectos().items():
        estado, avisos = via_canonica.revisar(apodo, d["ruta"], d.get("rama", ""))
        if estado == "BLOQUEO":
            malas.append((apodo, avisos))
    assert not malas, "hay proyectos apuntando a la version equivocada:\n" + \
        "\n".join(f"  {a}: {'; '.join(v)}" for a, v in malas)


def test_el_ingeniero_guarda_en_su_rama_canonica():
    """Que el propio Ingeniero cumpla la ley que impone a los demas."""
    real = via_canonica.rama_de(AQUI)
    declarada = grafo.proyectos().get("ingeniero", {}).get("rama", "")
    assert real == declarada, f"el Ingeniero esta en '{real}' y declara '{declarada}'"


def test_es_lo_primero_en_el_mando():
    """No basta con que exista: tiene que correr ANTES que nada."""
    src = open(os.path.join(AQUI, "ingeniero.py"), encoding="utf-8").read()
    assert "_via_ok" in src, "el mando no comprueba la via canonica"
    assert "TOCAN_PROYECTO" in src, "no esta declarado que comandos tocan un proyecto"
    i_check = src.index("if not _via_ok(")
    i_arranca = src.index('if cmd == "arranca"')
    assert i_check < i_arranca, "la comprobacion de via NO va antes que los comandos"


def test_el_sellado_exige_la_rama_canonica():
    """Los commits se guardan donde mandan, no donde toque."""
    s = open(os.path.join(AQUI, "sellar.sh"), encoding="utf-8").read()
    assert "RAMA_OK" in s and "BLOQUEADO" in s, "sellar.sh no protege la rama canonica"


# EL BUCLE DE LOS CANDADOS (Julio, 2026-09-13): los candados escriben sus propios cuadernos
# (memoria/CANDADOS_MEDICION.json, memoria/GASTO.log y demas) CADA VEZ que actuan. Ese archivo
# de mediciones reescrito deja el git siempre "sucio", y la via canonica grita "hay cambios SIN
# GUARDAR" a cada rato aunque no haya trabajo de Julio sin guardar. Es lo que Julio siente como
# "me pide permiso a cada rato" y lo que hace perder minutos en cada cierre.

def test_los_cuadernos_de_los_candados_NO_son_trabajo_sin_guardar(monkeypatch):
    """Si lo unico sucio son los cuadernos que los candados reescriben solos, NO es trabajo
    sin guardar: la via canonica no debe gritar."""
    def _falso(ruta, *args):
        if 'status' in args:
            return (" M memoria/CANDADOS_MEDICION.json\n"
                    " M memoria/GASTO.log\n"
                    " M memoria/GUARDIA.log\n")
        return ""
    monkeypatch.setattr(via_canonica, "_git", _falso)
    assert via_canonica.hay_cambios_sin_guardar("C:/x") is False, (
        "los cuadernos de los candados hicieron gritar 'hay cambios SIN GUARDAR'. Es un bucle: "
        "el candado se ensucia solo al medir. Solo el trabajo de verdad debe contar.")


def test_el_codigo_real_SI_es_trabajo_sin_guardar(monkeypatch):
    """NO se afloja: codigo real sucio tiene que seguir gritando igual de fuerte."""
    def _falso(ruta, *args):
        if 'status' in args:
            return " M cuerpo/obrero.py\n"
        return ""
    monkeypatch.setattr(via_canonica, "_git", _falso)
    assert via_canonica.hay_cambios_sin_guardar("C:/x") is True, (
        "hay codigo real sin guardar y la via canonica no grita: se aflojo el candado, y eso "
        "esta prohibido. Solo los cuadernos de los candados deben ignorarse.")
