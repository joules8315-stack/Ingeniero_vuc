# -*- coding: utf-8 -*-
"""VIGIA 6 — EL RELEVO DE CUOTAS (orden critica de Julio, 2026-08-20).

  "gaste los token gratis de Qwen y despues los de gemini, cuando se repongan los de Qwen
   continue con el, esto es critico."

Lo critico no es cambiar de cerebro cuando uno se agota: eso es facil. Lo critico es VOLVER
al primero cuando repone. Si nadie lleva la cuenta, el sistema se queda pegado al segundo
para siempre y se desperdicia el gratis que ya volvio.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import cuotas


@pytest.fixture(autouse=True)
def _limpio(tmp_path, monkeypatch):
    """Cada prueba con su propio archivo de cuotas: no se toca el real de Julio."""
    monkeypatch.setattr(cuotas, "RUTA", str(tmp_path / "CUOTAS.json"))
    yield


def test_el_orden_es_el_de_julio():
    assert cuotas.ORDEN[0] == "groq", "el primero SIEMPRE es Qwen (Groq)"
    assert cuotas.ORDEN[1] == "gemini", "el segundo es Gemini"


def test_al_agotarse_qwen_pasa_a_gemini():
    assert cuotas.turno() == "groq"
    cuotas.dormir("groq", "429 rate limit exceeded")
    assert cuotas.turno() == "gemini", "con Qwen agotado le toca a Gemini"


def test_cuando_qwen_repone_SE_VUELVE_A_EL():
    """La parte critica. Si esto falla, Julio se queda gastando el segundo cerebro de gusto."""
    cuotas.dormir("groq", "429 rate limit exceeded")
    assert cuotas.turno() == "gemini"
    # se simula que paso la siesta
    d = cuotas._leer()
    d["dormidos"]["groq"]["hasta"] = time.time() - 1
    cuotas._guardar(d)
    assert cuotas.turno() == "groq", "Qwen repuso y NO se volvio a el: se desperdicia el gratis"


def test_si_los_dos_se_agotan_queda_el_local():
    cuotas.dormir("groq", "429 quota")
    cuotas.dormir("gemini", "429 quota")
    assert cuotas.turno() == "local", "con los dos de nube agotados debe quedar LM Studio"


def test_distingue_agote_de_fallo_normal():
    """Solo se releva por CUOTA. Un error de codigo no debe hacer dormir a un cerebro sano."""
    assert cuotas.es_agote("429 Too Many Requests")
    assert cuotas.es_agote("RESOURCE_EXHAUSTED: quota exceeded")
    assert not cuotas.es_agote("KeyError: 'mensaje'")
    assert not cuotas.es_agote("connection refused")


def test_el_tope_por_dia_duerme_mas_que_el_del_minuto():
    assert cuotas.SIESTA["dia"] > cuotas.SIESTA["minuto"]


def test_el_estado_sobrevive_a_cerrar_la_sesion():
    cuotas.dormir("groq", "429 rate limit")
    assert os.path.exists(cuotas.RUTA), "las cuotas deben quedar en disco, no en memoria"
    assert cuotas.turno() == "gemini"
