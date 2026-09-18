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

    A-31 (2026-09-18): la ley Qwen->Gemini->local queda reemplazada por A-9/A-31.
    """
    gratis = [q for q in cuotas.ORDEN if q not in cuotas.DE_PAGO]
    pago = [q for q in cuotas.ORDEN if q in cuotas.DE_PAGO]
    assert cuotas.ORDEN[0] == "groq", "el primero SIEMPRE es Qwen (Groq)"
    assert gratis == ["groq", "gemini4", "gemini2"], \
        "los gratis son groq, gemini4 y gemini2 (A-9/A-31)"
    # lo de pago, SIEMPRE detras de todo lo gratis
    sitio = {q: i for i, q in enumerate(cuotas.ORDEN)}
    for p in pago:
        for g in gratis:
            assert sitio[p] > sitio[g], \
                "%s se paga y va por delante de %s, que es gratis" % (p, g)
    for fuera in ("groq20b", "gemini", "gemini3", "local"):
        assert fuera not in cuotas.ORDEN, \
            "%s salio de la fila por A-31 (2026-09-18)" % fuera


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
    """A-31 (2026-09-18): la local salio de la fila; con toda la nube GRATIS agotada queda DeepSeek. Se conserva el nombre para no perder la pieza."""
    for q in cuotas.ORDEN:
        if q not in cuotas.DE_PAGO:
            cuotas.dormir(q, "429 quota")
    assert cuotas.turno() == "deepseek", "con todas las gratis agotadas queda DeepSeek (A-31)"


# Las puertas SIN COSTE. "router" (OpenRouter) entra el 2026-08-27 y SOLO con los modelos
# terminados en ":free", que es lo unico que se configuro en arnes/velocidad.config. Comprobado
# ese dia preguntando a su API cuales cobran CERO de entrada y de salida. OJO: en OpenRouter
# conviven gratis y de pago bajo la misma llave, asi que si algun dia se configura un modelo SIN
# el ":free", deja de ser gratis y hay que declararlo en DE_PAGO. Lo vigila el test de abajo.
GRATIS = ("groq", "gemini", "local", "router")


def test_ningun_cerebro_de_la_fila_entra_con_capacidad_CERO():
    """FALLO REAL del 2026-08-27: cerebros en la fila que NUNCA se llamaban.

    Es una trampa cerrada: quien no figura en CAPACIDAD entra con cero, `rankear` descarta a todo
    el que no aguante el encargo, asi que nunca se le llama; y como nunca se le llama, nunca mide
    cuanto aguanta. Queda de adorno para siempre.

    Se cazo asi: se anadio OpenRouter, la fila paso de 8 a 11 cerebros, y el equipo SIGUIO
    diciendo "no quedo un segundo cerebro libre para auditar". Los tres router y gemini4 estaban
    en la lista pero invisibles. Un cerebro de adorno es peor que no tenerlo: hace creer a Julio
    que tiene relevo cuando no lo tiene.
    """
    for q in cuotas.ORDEN:
        assert cuotas._capacidad(q) > 0, (
            "'%s' esta en la fila pero su capacidad es CERO: el repartidor lo saltara SIEMPRE y "
            "nunca podra medir cuanto aguanta. Esta de adorno" % q)


def test_en_OpenRouter_solo_entran_los_que_dicen_free():
    """Protege el dinero de Julio en la unica puerta donde gratis y de pago comparten llave.

    En Groq o Gemini la llave manda: o es gratis o no. En OpenRouter NO: con la MISMA llave se
    puede llamar a un modelo gratis (`:free`) o a uno que cobra, y la diferencia son cinco letras
    al final del nombre. Un despiste ahi le cobraria a Julio sin que nadie se entere, y encima
    entraria como si fuera gratis en el relevo.

    Anadido el 2026-08-27, el dia que OpenRouter entro en la fila.
    """
    from pathlib import Path
    cfg = Path(__file__).resolve().parents[1] / "arnes" / "velocidad.config"
    assert cfg.exists(), "falta arnes/velocidad.config: sin el no se sabe que modelos se usan"
    for ln in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if ln.startswith("#") or "=" not in ln:
            continue
        clave, valor = (x.strip() for x in ln.split("=", 1))
        if clave.startswith("modelo_router"):
            assert valor.endswith(":free"), (
                "'%s' esta configurado como '%s', que NO termina en ':free': en OpenRouter eso "
                "SE PAGA, y ademas entraria en el relevo como si fuera gratis" % (clave, valor))


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
