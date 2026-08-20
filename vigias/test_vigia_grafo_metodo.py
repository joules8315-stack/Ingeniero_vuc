# -*- coding: utf-8 -*-
"""VIGIA 17 — EL GRAFO DE LA FORMA DE TRABAJO (Julio, 2026-08-20).

  "indexa toda la forma de trabajo, crea el grafo que te lo recuerde siempre... para que
   siempre sigas la misma ruta. Asi mismo como debes buscar la informacion, como preguntar,
   cuando hacerlo."

El grafo de las otras capas mapea el CODIGO. Este mapea el METODO: los 8 pasos, que exige cada
uno, que prohibe, su candado y de que documento de Julio sale.

Lo que se vigila aqui es lo que lo haria inutil:
  · que un paso se quede SIN CANDADO (entonces se salta, y eso ya paso)
  · que no sepa en que paso estamos (entonces no recuerda nada util)
  · que los documentos del metodo dejen de estar indexados (entonces no se pueden citar)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import pytest
from cerebro import protocolo as pr


def test_los_ocho_pasos_estan_y_en_orden():
    assert len(pr.PASOS) == 8
    assert [p["n"] for p in pr.PASOS] == list(range(1, 9))


def test_NINGUN_paso_se_queda_sin_candado():
    """Un paso sin candado es un paso que se salta. Es la leccion del 2026-08-20."""
    sin = [p["nombre"] for p in pr.PASOS if not pr.tiene_candado(p)]
    assert not sin, "estos pasos no tienen candado y se van a saltar: %s" % sin


def test_cada_paso_dice_que_exige_y_que_prohibe():
    for p in pr.PASOS:
        assert p["exige"], "el paso %d no dice que exige" % p["n"]
        assert p["prohibe"], "el paso %d no dice que esta prohibido" % p["n"]
        assert p["comando"], "el paso %d no dice como se hace" % p["n"]
        assert p["fuente"], "el paso %d no dice de que documento de Julio sale" % p["n"]


def test_sabe_en_que_paso_estamos():
    p = pr.paso_actual()
    assert p and 1 <= p["n"] <= 8
    txt = pr.ahora()
    assert "PASO" in txt and "PROHIBIDO" in txt


# ─── los tres errores del 2026-08-20 tienen su paso ───────────────────────────
def test_el_paso_de_la_causa_raiz_prohibe_reparar_lo_inferido():
    """El error que arranco todo: iba a indexar el MVP sin saber donde estaba lento."""
    p = [x for x in pr.PASOS if x["n"] == 3][0]
    junto = " ".join(p["prohibe"]).lower()
    assert "inferido" in junto
    assert "antes de localizar" in junto


def test_el_paso_de_preguntar_prohibe_preguntar_lo_ya_escrito():
    p = [x for x in pr.PASOS if x["n"] == 4][0]
    assert any("ya escribio" in x.lower() for x in p["prohibe"])
    assert "22" in p["fuente"], "no cita la seccion del protocolo de Julio de donde sale"


def test_el_paso_de_la_prueba_prohibe_autovalidarse():
    p = [x for x in pr.PASOS if x["n"] == 7][0]
    junto = " ".join(p["prohibe"]).lower()
    assert "verde" in junto and "su propia prueba" in junto


# ─── el norte y las leyes duras ───────────────────────────────────────────────
def test_el_norte_manda_sobre_los_pasos():
    junto = " ".join(a + " " + b for a, b in pr.NORTE).lower()
    assert "consolid" in junto, "falta el norte: consolidar a una sola version"
    assert "no asumir" in junto or "suposicion" in junto


def test_estan_las_leyes_duras_de_julio():
    junto = " ".join(a + " " + b for a, b in pr.LEYES_DURAS).lower()
    for debe in ("simple", "asumir", "repita", "duplicar"):
        assert debe in junto, "falta la ley dura sobre '%s'" % debe


# ─── el indice del metodo ─────────────────────────────────────────────────────
def test_los_documentos_del_metodo_estan_indexados():
    fichas = pr.indexar()
    assert len(fichas) >= 8, "se indexaron muy pocos documentos: %d" % len(fichas)
    proyectos = {f["proyecto"] for f in fichas}
    assert "dmm" in proyectos or "foto_informe" in proyectos


def test_se_puede_consultar_el_metodo_y_citarlo():
    """Poder citar archivo:linea es lo que separa 'aplicar la ley' de 'opinar'."""
    r = pr.buscar_en_el_metodo("antes de preguntar agotar las fuentes")
    assert r, "no encuentra la regla de agotar las fuentes"
    assert ":" in r[0]["donde"], "no dice el documento y la linea, no se puede citar"
