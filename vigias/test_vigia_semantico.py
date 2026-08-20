# -*- coding: utf-8 -*-
"""VIGIA 15 — BUSCAR POR SIGNIFICADO SIN DEJAR TIRADO AL INGENIERO (orden 4 de Julio).

Lo que se vigila NO es que acierte mas (eso lo dira el medidor con el tiempo), sino lo que
podria romper: que si Gemini no contesta, se acabe la cuota o no haya internet, **el Ingeniero
siga funcionando**. Una mejora que puede dejar el sistema sin buscador no es una mejora.

Medido el 2026-08-20 con dos frases que dicen lo mismo con otras palabras contra una que no
tiene nada que ver:
    LM Studio (nomic-embed local) ... 0.022 de diferencia -> NO distingue
    gemini-embedding-001 ........... 0.202 de diferencia -> SI distingue
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import semantico, router, grafo


def _cand(n=5):
    return [{"direccion": f"a.py:{i}-{i+40}", "texto": f"trozo numero {i}", "puntaje": 10 - i}
            for i in range(n)]


def test_sin_llave_devuelve_los_candidatos_TAL_CUAL(monkeypatch):
    """Lo mas importante: sin llave no se rompe nada, solo no se reordena."""
    monkeypatch.setattr(semantico, "hay", lambda: False)
    c = _cand()
    assert semantico.reordenar("lo que sea", c) == c


def test_si_la_llamada_falla_tampoco_se_rompe(monkeypatch):
    monkeypatch.setattr(semantico, "hay", lambda: True)
    monkeypatch.setattr(semantico, "vector", lambda *a, **k: None)
    c = _cand()
    assert semantico.reordenar("lo que sea", c) == c, "sin vectores deberia devolver el orden original"


def test_con_lista_vacia_no_explota():
    assert semantico.reordenar("x", []) == []


def test_el_parecido_es_coherente():
    a = [1.0, 0.0, 0.0]
    b = [1.0, 0.0, 0.0]
    c = [0.0, 1.0, 0.0]
    assert semantico.parecido(a, b) > 0.99, "dos vectores iguales deben parecerse del todo"
    assert abs(semantico.parecido(a, c)) < 0.01, "dos perpendiculares no deben parecerse"
    assert semantico.parecido(None, a) == 0.0, "sin vector, cero; nunca explota"


def test_hay_interruptor_para_no_gastar_cuota():
    """Julio tiene que poder apagarlo sin tocar codigo."""
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "cerebro", "router.py"), encoding="utf-8").read()
    assert "INGENIERO_SIN_SIGNIFICADO" in src, "no hay forma de apagar el gasto de embeddings"


def test_el_router_sigue_armando_paquetes_con_el_significado_apagado(monkeypatch):
    """El interruptor no puede dejar el router sin trozos."""
    if "dmm" not in grafo.proyectos() or not os.path.isdir(grafo.proyectos()["dmm"]["ruta"]):
        pytest.skip("dmm no esta")
    monkeypatch.setenv("INGENIERO_SIN_SIGNIFICADO", "1")
    pk = router.armar("dmm", "el onboarding no guarda el perfil")
    assert pk["trozos"], "con el significado apagado el paquete se quedo sin trozos"
    assert len(pk["trozos"]) <= 6, "trae mas trozos de los pedidos"


def test_lo_que_ya_se_pago_no_se_vuelve_a_pagar():
    """La cache es lo que hace esto sostenible: un texto se embebe UNA vez."""
    import inspect
    src = inspect.getsource(semantico.vector)
    assert "cache" in src and "_clave" in src, "no hay cache: se pagaria dos veces por lo mismo"
