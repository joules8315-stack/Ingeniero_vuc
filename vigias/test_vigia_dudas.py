# -*- coding: utf-8 -*-
"""VIGIA 13 — BUSCAR PRIMERO, PREGUNTAR DESPUES... PERO SIN MENTIR (Ley 16).

  Julio: "primero busque en los repositorios la respuesta, solo cuando no la halle, pregunte;
   siempre debe hacerlas, aun mas si pierde el contexto"

El peligro de esta pieza no es preguntar de mas: es dar por RESUELTA una duda que nadie ha
contestado. Si eso pasa, se asume — y asumir es justo lo que Julio prohibio.

DOS COSAS QUE SE APRENDIERON PROBANDO ESTO (2026-08-20):

1. **El juez del cerebro NO es un adorno: es imprescindible.** Se intento probar el sistema sin
   el (`juzgar=False`) y salieron falsos positivos a mansalva: "cuantos empleados tiene la
   empresa" traia un fallo del onboarding, y "que dia prefiere para publicar" traia el contrato
   de flujo. Contar palabras nunca sabra si un texto RESPONDE una pregunta.

2. **Pero una vigia no puede depender de una llamada a un cerebro.** Un cerebro no contesta
   siempre igual: un dia aprobo un contrato que no venia al caso y la vigia se puso roja sin que
   el codigo hubiera cambiado. Una vigia inestable no vale para nada.

La salida a las dos cosas: se prueba el sistema COMPLETO, pero con un juez de mentira que
contesta siempre lo mismo. Asi se comprueba la logica de verdad, sin depender de nadie.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import dudas, estado
from cerebro import grafo


def _hay(a):
    p = grafo.proyectos()
    return a in p and os.path.isdir(p[a]["ruta"])


@pytest.fixture(autouse=True)
def _registro_aparte(tmp_path, monkeypatch):
    """Cada prueba con SU registro. Antes escribian preguntas de mentira en el registro de
    verdad, y despues el guardia de cierre las tomaba por preguntas reales sin hacer y no
    dejaba terminar (fallo real 2026-08-21)."""
    monkeypatch.setenv("INGENIERO_ESTADO_TEST", str(tmp_path / "ESTADO.json"))
    yield


@pytest.fixture
def juez_severo(monkeypatch):
    """Juez de mentira: dice que NINGUN candidato responde. Es el caso 'no esta escrito'."""
    monkeypatch.setattr(dudas, "_responde_de_verdad", lambda duda, cand: [])


@pytest.fixture
def juez_permisivo(monkeypatch):
    """Juez de mentira: dice que el primero SI responde. Es el caso 'si esta escrito'."""
    monkeypatch.setattr(dudas, "_responde_de_verdad", lambda duda, cand: cand[:1])


# ─── lo que NO esta escrito se pregunta ────────────────────────────────────────
@pytest.mark.parametrize("duda", [
    "de que color quiere Julio el boton de aprobar",
    "cuantos empleados tiene la empresa de Julio",
    "que dia de la semana prefiere Julio para publicar",
])
def test_si_el_juez_dice_que_nada_responde_SE_PREGUNTA(duda, juez_severo):
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    r = dudas.resolver(duda, "dmm")
    assert r["hay_que_preguntar"], f"'{duda}': el juez dijo que nada responde y aun asi no pregunto"
    assert not r["hallado"]


def test_lo_que_SI_responde_no_molesta_a_julio(juez_permisivo):
    # se busca en 'ingeniero', que es donde esta escrito el relevo de cuotas. Buscarlo en dmm
    # no devolvia ni un candidato, el juez ni se llamaba, y la prueba no probaba nada.
    if not _hay("ingeniero"):
        pytest.skip("ingeniero no esta")
    r = dudas.resolver("relevo de cuotas entre los cerebros gratis", "ingeniero")
    assert not r["hay_que_preguntar"], "el juez aprobo una fuente y aun asi iba a preguntar"


# ─── el juez es imprescindible y tiene que llamarse ────────────────────────────
def test_el_juez_se_llama_de_verdad():
    """Sin este filtro, contar palabras da falsos positivos: probado el 2026-08-20."""
    import inspect
    src = inspect.getsource(dudas.resolver)
    assert "_responde_de_verdad" in src, "no se llama al juez que separa 'responde' de 'se parece'"


def test_sin_cerebro_el_juez_elige_el_lado_seguro(monkeypatch):
    """Sin cerebro no se puede saber si algo responde -> se PREGUNTA a Julio. Nunca se supone."""
    from cuerpo import obrero
    monkeypatch.setattr(obrero, "quienes_hay", lambda: [])
    assert dudas._responde_de_verdad("lo que sea", [{"fuente": "X", "donde": "y", "texto": "z"}]) == []


def test_si_el_juez_falla_tampoco_se_da_nada_por_bueno(monkeypatch):
    from cuerpo import obrero
    monkeypatch.setattr(obrero, "quienes_hay", lambda: ["groq"])
    monkeypatch.setattr(obrero, "_preguntar_con_relevo",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("se cayo")))
    assert dudas._responde_de_verdad("x", [{"fuente": "X", "donde": "y", "texto": "z"}]) == []


# ─── la pregunta se formula bien y no se pierde ────────────────────────────────
def test_la_pregunta_dice_donde_se_busco(juez_severo):
    """Preguntar sin decir donde se busco parece pereza; diciendolo, es un informe."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    d = "de que color quiere Julio el boton de aprobar"
    txt = dudas.formular(d, dudas.resolver(d, "dmm"))
    assert "PREGUNTA_REQUERIDA" in txt
    assert "busque" in txt.lower(), "no dice que ya se busco antes de preguntar"


def test_la_pregunta_queda_apuntada_para_que_no_se_olvide(juez_severo):
    """Si no se apunta, se pierde. El candado de cierre la exige antes de terminar el turno."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    antes = estado.leer().get("decision_pendiente", "")
    try:
        estado.apuntar(decision_pendiente="")
        dudas.apuntar_pregunta("de que color quiere Julio el boton de aprobar", "dmm")
        assert estado.leer().get("decision_pendiente"), "la pregunta no quedo apuntada"
    finally:
        estado.apuntar(decision_pendiente=antes)


def test_si_esta_resuelta_no_se_apunta_pregunta(juez_permisivo):
    """No se molesta a Julio con algo que ya estaba escrito."""
    if not _hay("ingeniero"):
        pytest.skip("ingeniero no esta")
    antes = estado.leer().get("decision_pendiente", "")
    try:
        estado.apuntar(decision_pendiente="")
        dudas.apuntar_pregunta("relevo de cuotas entre los cerebros gratis", "ingeniero")
        assert not estado.leer().get("decision_pendiente"), \
            "apunto una pregunta para Julio de algo que ya estaba respondido"
    finally:
        estado.apuntar(decision_pendiente=antes)
