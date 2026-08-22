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
    """Se comprueba lo que la ley QUIERE, no un puesto fijo en la fila.

    El 2026-08-21 se anadio un cuarto cerebro gratis (gpt-oss-20b: Groq reparte cupo POR MODELO,
    asi que cada modelo mas es cupo gratis de mas). Eso NO contradice la ley de Julio —usar hasta
    el final lo gratis y no tocar lo caro—, pero si movia de sitio a Gemini. Julio, ese mismo dia:
    "tu debes ser el ultimo recurso, cuando se agoten los modelos gratis, o sea nunca, porque
    existen cientos". Atar la ley a un puesto fijo impedia anadir cerebros, que es justo lo que
    la ley pide. Lo que NO se afloja: primero Groq y el de casa el ultimo de los gratis.

    El 2026-08-21 Julio ordeno meter a DeepSeek, que SE PAGA ("es una orden implementa el puto
    deepseek"). Eso no afloja la ley: la precisa. Lo de pago puede estar en la fila, pero DETRAS
    de todo lo gratis y sin entrar nunca en la pregunta a la vez. Por eso "el ultimo" deja de
    medirse sobre la fila entera y se mide sobre LOS GRATIS, que es lo que la ley protegia.
    """
    gratis = [q for q in cuotas.ORDEN if q not in cuotas.DE_PAGO]
    pago = [q for q in cuotas.ORDEN if q in cuotas.DE_PAGO]
    assert cuotas.ORDEN[0] == "groq", "el primero SIEMPRE es Qwen (Groq)"
    assert "gemini" in cuotas.ORDEN, "Gemini tiene que seguir en la fila"
    assert gratis[-1] == "local", "el de tu PC es el ultimo GRATIS: se usa cuando no queda nube"
    assert gratis.index("gemini") < gratis.index("local"), "Gemini va antes que el de casa"
    assert len(gratis) >= 3, "se perdieron cerebros gratis de la fila"
    # lo de pago, SIEMPRE detras de todo lo gratis
    sitio = {q: i for i, q in enumerate(cuotas.ORDEN)}
    for p in pago:
        for g in gratis:
            assert sitio[p] > sitio[g], \
                "%s se paga y va por delante de %s, que es gratis" % (p, g)


def _el_siguiente_gratis(dormidos):
    for q in dormidos:
        cuotas.dormir(q, "429 rate limit exceeded")
    return cuotas.turno()


def test_al_agotarse_uno_pasa_al_siguiente_GRATIS():
    assert cuotas.turno() == "groq"
    siguiente = _el_siguiente_gratis(["groq"])
    assert siguiente in cuotas.ORDEN and siguiente != "groq", \
        "con el primero agotado no paso a ningun otro cerebro gratis"
    assert siguiente != "local", "salto al de casa teniendo nube libre: se desperdicia lo gratis"


def test_cuando_repone_SE_VUELVE_A_EL():
    """La parte critica. Si esto falla, Julio se queda gastando el segundo cerebro de gusto."""
    cuotas.dormir("groq", "429 rate limit exceeded")
    assert cuotas.turno() != "groq"
    # se simula que paso la siesta
    d = cuotas._leer()
    d["dormidos"]["groq"]["hasta"] = time.time() - 1
    cuotas._guardar(d)
    assert cuotas.turno() == "groq", "Qwen repuso y NO se volvio a el: se desperdicia el gratis"


def test_si_se_agota_toda_la_nube_queda_el_local():
    for q in cuotas.ORDEN:
        if q != "local":
            cuotas.dormir(q, "429 quota")
    assert cuotas.turno() == "local", "con toda la nube agotada debe quedar LM Studio"


GRATIS = ("groq", "gemini", "local")          # las tres puertas sin coste


def test_lo_que_cuesta_DINERO_esta_declarado():
    """Julio: 'tu debes ser el ultimo recurso, cuando se agoten los modelos gratis'.

    Antes esto prohibia que hubiera NINGUNO de pago en la fila. El 2026-08-21 Julio ordeno meter
    a DeepSeek, que se paga. La ley no se afloja, se aprieta donde importa: lo que protege su
    dinero no es que no exista lo de pago, es que lo de pago este DECLARADO y no se pueda colar
    ninguno de tapadillo. Un cerebro de pago sin declarar entraria en la pregunta a la vez que
    los gratis y le cobraria a Julio en cada pregunta."""
    for q in cuotas.ORDEN:
        if any(q.startswith(p) for p in GRATIS):
            continue
        assert q in cuotas.DE_PAGO, \
            ("entro en la fila '%s', que no va por ninguna puerta gratis y NO esta declarado "
             "como de pago: se le cobraria a Julio sin que nadie lo sepa" % q)


def test_hay_cerebros_de_sobra_para_los_CUATRO_OJOS():
    """Con uno solo, el que propone se aprueba a si mismo. Paso de verdad el 2026-08-21: con Groq
    agotado y el de casa fallando, quedaba UN cerebro y la auditoria se quedo sin hacer."""
    assert len(cuotas.ORDEN) >= 4, (
        "quedan %d cerebros: si se agota uno no hay segundo par de ojos" % len(cuotas.ORDEN))


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
    assert cuotas.turno() != "groq", "se olvido que estaba agotado al releerlo del disco"
