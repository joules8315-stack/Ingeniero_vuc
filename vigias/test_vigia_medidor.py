# -*- coding: utf-8 -*-
"""VIGIA 14 — EL MEDIDOR DE ACIERTO (Julio, 2026-08-20).

  "1) Medir el acierto  2) Aprender de los aciertos y errores  3) Que el router se corrija solo"

Por que hace falta: hasta ahora se podia decir "ahorra el 99%" porque se conto, pero NO "acierta
el 90%" porque nunca se midio. Y el paquete FALLABA (traia el motor y no la pantalla): lo cazaron
dos modelos gratis, no las vigias.

Lo que se vigila aqui: que el medidor **no se automiente**. Un medidor que siempre dice "bien"
es peor que no medir, porque da tranquilidad falsa.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import medidor


@pytest.fixture(autouse=True)
def _limpio(tmp_path, monkeypatch):
    """Cada prueba con su propio archivo: no se toca el historial real de Julio."""
    monkeypatch.setattr(medidor, "RUTA", str(tmp_path / "MEDICIONES.json"))
    yield


def _pk(problema="algo", lineas=200, total=20000):
    return ({"apodo": "dmm", "problema": problema, "flujos": [("perfil", 6)],
             "codigo": [{"id": "cuerpo/perfil.py"}], "trozos": [{"direccion": "cuerpo/perfil.py:1-40"}],
             "leyes": [{"id": "CONTRATO_X.md"}], "vigias": [{"id": "vigias/test_x.py"}],
             "total_proyecto": total}, "\n".join(["x"] * lineas))


def test_apunta_el_paquete_con_su_ahorro():
    pk, txt = _pk()
    m = medidor.apuntar_paquete(pk, txt)
    assert m["ahorro"] == 99.0, m["ahorro"]
    assert m["veredicto"] == "SIN_JUZGAR", "no puede nacer dandose por bueno"


def test_si_el_obrero_pidio_mas_material_el_paquete_se_quedo_CORTO():
    """La señal mas importante: el paquete no traia lo necesario."""
    pk, txt = _pk("p1")
    medidor.apuntar_paquete(pk, txt)
    m = medidor.juzgar("dmm", "p1", {"propuesta": {"cambio": "NECESITO_LEER web/servidor.py"}})
    assert m["veredicto"] == "CORTO", m


def test_si_el_obrero_no_encontro_nada_tambien_es_CORTO():
    pk, txt = _pk("p2")
    medidor.apuntar_paquete(pk, txt)
    m = medidor.juzgar("dmm", "p2", {"propuesta": {"diagnostico": "NO_ENCONTRADO",
                                                   "preguntas": ["donde esta el formulario"]}})
    assert m["veredicto"] == "CORTO"
    assert m["falto"], "no apunto QUE falto, que es lo que sirve para corregir el router"


def test_si_el_juez_aprobo_el_paquete_SIRVIO():
    pk, txt = _pk("p3")
    medidor.apuntar_paquete(pk, txt)
    m = medidor.juzgar("dmm", "p3", {"propuesta": {"diagnostico": "falta guardar"},
                                     "juez_dice": {"veredicto": "APROBADO"}})
    assert m["veredicto"] == "SIRVIO"


def test_no_confunde_falta_de_material_con_falta_de_decision():
    """Si falto que Julio decidiera algo, el paquete NO tuvo la culpa."""
    pk, txt = _pk("p4")
    medidor.apuntar_paquete(pk, txt)
    m = medidor.juzgar("dmm", "p4", {"propuesta": {"diagnostico": "ok",
                                                   "preguntas": ["¿de que color el boton?"]}})
    assert m["veredicto"] == "FALTO_DECISION", m["veredicto"]


def test_el_acierto_no_cuenta_los_que_no_son_culpa_del_paquete():
    for i, res in enumerate([
        {"juez_dice": {"veredicto": "APROBADO"}, "propuesta": {"diagnostico": "d"}},
        {"propuesta": {"cambio": "NECESITO_LEER x"}},
        {"propuesta": {"diagnostico": "d", "preguntas": ["¿?"]}},   # falta decision: no cuenta
    ]):
        pk, txt = _pk(f"q{i}")
        medidor.apuntar_paquete(pk, txt)
        medidor.juzgar("dmm", f"q{i}", res)
    r = medidor.resumen("dmm")
    assert r["juzgados"] == 2, f"conto mal: {r}"
    assert r["acierto"] == 50.0, f"acierto mal calculado: {r}"


def test_solo_julio_marca_la_prueba_humana():
    pk, txt = _pk("p5")
    m = medidor.apuntar_paquete(pk, txt)
    assert m["prueba_humana"] == "PENDIENTE", "nacio dandose por probado"
    medidor.juzgar("dmm", "p5", {"juez_dice": {"veredicto": "APROBADO"}, "propuesta": {"diagnostico": "d"}})
    assert medidor._leer()[-1]["prueba_humana"] == "PENDIENTE", \
        "el juez de las IA marco la prueba humana: eso solo lo hace Julio (Ley 5)"
    medidor.marcar_prueba_humana("dmm", "p5")
    assert medidor._leer()[-1]["prueba_humana"] == "HECHA"


def test_dice_QUE_falto_para_que_el_router_se_corrija():
    pk, txt = _pk("p6")
    medidor.apuntar_paquete(pk, txt)
    medidor.juzgar("dmm", "p6", {"propuesta": {"diagnostico": "NO_ENCONTRADO",
                                               "preguntas": ["falta web/servidor.py"]}})
    falt = medidor.lo_que_falto("dmm")
    assert falt and "servidor" in " ".join(falt[-1]["falto"]), falt


def test_sin_mediciones_lo_dice_en_vez_de_inventar_un_numero():
    assert "todavia no hay" in medidor.texto().lower()
