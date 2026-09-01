# -*- coding: utf-8 -*-
"""VIGIA 25 — EL CEREBRO QUE CONTESTA ES EL QUE PEDI (2026-08-21).

COMO SE DESCUBRIO: se pidio un modelo inventado, "pepito-grillo-9000", y contesto tan tranquilo
(en italiano). O sea que el Ingeniero creia estar eligiendo cerebro y SIEMPRE le contestaba el
mismo. Todas las medidas de velocidad hechas asi eran mentira: se dio por bueno que Kimi K2 y K3
funcionaban en 7 segundos, y ni siquiera estan en la llave de Julio. Se le llego a decir a Julio
que ya tenia Kimi. Era falso.

LA CAUSA: la puerta comoda del cerebro prestado hacia dos cosas a escondidas. A Gemini le quitaba
el modelo pedido y usaba el suyo fijo; y si el modelo no existia, en vez de avisar caia CALLANDO
en otro proveedor. **Un error tapado es peor que un error**: hace decidir sobre datos falsos.

LO QUE COSTO: los dos modelos fijos de Gemini (2.0-flash, y de respaldo 1.5-flash) llevaban
MUERTOS, 404 los dos. Por eso Gemini fallaba 4 de cada 7 veces, el trabajo no acababa en el
cerebro gratis sino en la IA cara, y lo pagaba Julio. Es el fallo que mas dinero le ha costado.
"""
import inspect
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import obrero, cuotas


def test_se_llama_a_cada_cerebro_directo():
    """EL NUCLEO: nada de puertas comodas que cambien el cerebro por detras."""
    src = inspect.getsource(obrero._preguntar_con_relevo)
    assert "_gemini_directo" in src, "Gemini vuelve a ir por la puerta que ignora el modelo"
    assert "_preguntar_groq" in src, "Groq vuelve a ir por la puerta que puede cambiar de cerebro"
    codigo = " ".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert "forzar=" not in codigo, (
        "volvio la puerta comoda: si el modelo no existe cae callando en otro cerebro y contesta "
        "como si nada, que es justo lo que hizo perder el dinero")


def test_un_modelo_que_no_existe_da_ERROR_no_respuesta():
    """Si un modelo inventado contesta, todas las medidas valen cero."""
    c, _ = obrero.prestar_cerebro()
    if not c or not os.environ.get("GROQ_API_KEY", "").strip():
        pytest.skip("sin llave de Groq")
    with pytest.raises(Exception):
        c._preguntar_groq("Di LISTO.", "pepito-grillo-9000", 0.1)


def test_el_modelo_de_gemini_configurado_esta_VIVO():
    """Los que habia puestos llevaban muertos y nadie se entero: fallaba en silencio."""
    if not os.environ.get("GEMINI_API_KEY", "").strip():
        pytest.skip("sin llave de Gemini")
    m = obrero._velocidad().get("modelo_gemini")
    assert m, "no hay modelo de Gemini configurado"
    # Se distingue MUERTO de OCUPADO. Un modelo retirado da 404 siempre: eso es el fallo que se
    # vigila (los dos que habia puestos llevaban meses muertos y nadie se entero). Un 503 es que
    # el servicio esta saturado un momento; eso no es culpa del Ingeniero y no puede pintar un
    # rojo falso, que ensena a ignorar los rojos. Se reintenta y, si sigue saturado, se dice.
    ultimo = None
    for _ in range(3):
        try:
            txt = obrero._gemini_directo("Di solo LISTO.", 0.1, m)
            assert (txt or "").strip(), "el modelo de Gemini configurado contesta vacio"
            return
        except Exception as e:
            ultimo = str(e)
            if "404" in ultimo:
                raise AssertionError(
                    "el modelo de Gemini configurado (%s) esta MUERTO: da 404" % m)
    pytest.skip("Gemini saturado ahora mismo (%s): no es un fallo del Ingeniero" % ultimo[:60])


def test_el_modelo_de_groq_configurado_esta_VIVO():
    if not os.environ.get("GROQ_API_KEY", "").strip():
        pytest.skip("sin llave de Groq")
    c, _ = obrero.prestar_cerebro()
    m = obrero._velocidad().get("modelo_groq")
    try:
        respuesta = c._preguntar_groq("Di solo LISTO.", m, 0.1)
    except Exception as e:
        numero = getattr(e, "code", None) or getattr(e, "status_code", None)
        texto = str(e).lower()
        if numero in (429, 503) or "429" in texto or "503" in texto or "too many requests" in texto or "service unavailable" in texto:
            pytest.skip("cuota del dia agotada o servidor no disponible: no es fallo del modelo")
        raise
    assert (respuesta or "").strip(), \
        "el modelo de Groq configurado no contesta"


def test_cada_cerebro_de_la_fila_tiene_modelo_configurado():
    """Se llegaron a meter Kimi y Llama en la fila sin comprobarlos: dan 404 en su llave.
    Un cerebro apuntado que no existe hace perder el turno y frena el trabajo.
    Se comprueba lo que importa —que cada uno tenga con que contestar— y no una lista cerrada,
    porque la lista tiene que poder crecer: Julio quiere muchos cerebros gratis, no tres."""
    vel = obrero._velocidad()
    for quien in cuotas.ORDEN:
        if quien == "local":
            continue          # el de casa no lleva modelo: lo elige LM Studio
        assert vel.get("modelo_" + quien), (
            "'%s' esta en la fila pero no tiene modelo configurado: perdera el turno siempre"
            % quien)


def test_el_auditor_nunca_es_el_mismo_que_genero():
    """Cuatro ojos de verdad: nadie se aprueba a si mismo."""
    src = inspect.getsource(obrero.trabajar)
    assert "evitar=quien_gen" in src, "el que genera podria auditarse a si mismo"
