# -*- coding: utf-8 -*-
"""VIGIA 25 — DEEPSEEK ESTA EN EL EQUIPO DE VERDAD, NO DE ADORNO.

Julio, 2026-08-21, y hubo que repetirlo:
  "trabaja de la mano con deepseek, que si tu eres las manos el supervisa, y si el es las manos
   tu supervisas, eso como norma inquebrantable."
  "no es openrouter, es deepseek."
  "si, ese es, canal de 4 ojos, ahora agregalo al equipo."

LO QUE PASO: se construyo la puerta de OTRA empresa (OpenRouter) para traer a DeepSeek por ahi,
y DeepSeek nunca llego a existir: no estaba en la fila, ni tenia apodo, ni tenia llave. Un
cerebro que esta escrito en un comentario pero no en la fila es un cerebro de adorno. Ya paso lo
mismo antes con los cerebros que se anadian y NUNCA entraban (ley de `quienes_hay`).

LO QUE SE VIGILA AQUI:
  · que DeepSeek este en la fila y tenga apodo (si no, no lo ve nadie)
  · que su puerta sea la SUYA (api.deepseek.com), no la de un intermediario
  · que lea SU llave propia (DEEPSEEK_API_KEY)
  · que SIN llave no entre en la fila y no estorbe
  · que CON llave entre de verdad
  · que quedarse SIN SALDO se trate como agotarse, no como fallo de codigo: es de pago, y
    reintentar en balde le cuesta dinero a Julio
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from cuerpo import cuotas, obrero


def test_esta_en_la_fila_y_tiene_nombre():
    assert "deepseek" in cuotas.ORDEN, "DeepSeek no esta en la fila: no le tocaria nunca"
    assert cuotas.APODO.get("deepseek"), "DeepSeek no tiene apodo: no se le ve en 'cuotas'"


def test_va_el_ultimo_porque_es_el_unico_de_pago():
    """Los gratis primero. Julio: 'tu debes ser el ultimo recurso'."""
    gratis = [q for q in cuotas.ORDEN if q != "deepseek"]
    assert cuotas.ORDEN.index("deepseek") > max(cuotas.ORDEN.index(q) for q in gratis), \
        "DeepSeek es de PAGO y va delante de los gratis: eso le cuesta dinero a Julio"


def _lo_que_hace_de_verdad(nombre_funcion):
    """Lo que la funcion HACE, sin comentarios ni explicaciones.

    Se mira el arbol del codigo, no el texto (lo impuso DeepSeek auditando esta misma vigia).
    Leer el texto a pelo daba dos fallos: se ponia ROJA por el comentario que cita a Julio
    diciendo "no es openrouter, es deepseek", y podia ponerse VERDE con un texto disfrazado.
    Devuelve (los textos que usa, los nombres que usa).
    """
    import ast
    arbol = ast.parse(open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8").read())
    fn = next((n for n in ast.walk(arbol)
               if isinstance(n, ast.FunctionDef) and n.name == nombre_funcion), None)
    assert fn is not None, "NO_ENCONTRADO: la funcion %s no existe" % nombre_funcion
    # La explicacion se quita POR SU SITIO (es la primera frase suelta de la funcion), no
    # comparando su texto: al pedirla ya viene recolocada y nunca coincide letra por letra.
    pasos = list(fn.body)
    if (pasos and isinstance(pasos[0], ast.Expr)
            and isinstance(pasos[0].value, ast.Constant)
            and isinstance(pasos[0].value.value, str)):
        pasos = pasos[1:]
    textos, nombres = [], []
    for paso in pasos:
        for n in ast.walk(paso):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                textos.append(n.value)
            elif isinstance(n, ast.Name):
                nombres.append(n.id)
            elif isinstance(n, ast.Attribute):
                nombres.append(n.attr)
    return textos, nombres


def test_tiene_su_propia_puerta_y_no_la_del_intermediario():
    assert hasattr(obrero, "_deepseek_directo"), "no existe la puerta propia de DeepSeek"
    textos, nombres = _lo_que_hace_de_verdad("_deepseek_directo")
    todo = " ".join(textos + nombres).lower()
    assert any("api.deepseek.com" in t for t in textos), \
        "la puerta de DeepSeek no apunta a la casa de DeepSeek"
    assert "openrouter" not in todo, \
        "la puerta de DeepSeek pasa por el intermediario; Julio dijo que NO es openrouter"
    assert "DEEPSEEK_API_KEY" in textos + nombres, \
        "la puerta no lee la llave propia de DeepSeek"


def test_su_modelo_esta_configurado():
    vel = obrero._velocidad()
    assert vel.get("modelo_deepseek"), "sin modelo configurado, DeepSeek se queda fuera de la fila"


def test_sin_llave_no_entra_y_no_estorba(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    assert "deepseek" not in obrero.quienes_hay(), \
        "sin llave DeepSeek entra igual: fallara en cada encargo y estorbara a los demas"


def test_con_llave_entra_de_verdad(monkeypatch):
    """El fallo de los 'cerebros de adorno': declarado pero nunca en la fila."""
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-de-mentira-para-la-prueba")
    assert "deepseek" in obrero.quienes_hay(), \
        "con llave y con modelo, DeepSeek sigue sin entrar en la fila: es de adorno"


def test_sin_llave_la_puerta_avisa_claro(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    try:
        obrero._deepseek_directo("hola", 0.2, "deepseek-chat")
    except Exception as e:
        assert "llave" in str(e).lower(), "el aviso de que falta la llave no se entiende"
    else:
        raise AssertionError("sin llave la puerta deberia avisar, no seguir adelante")


@pytest.fixture
def equipo_de_mentira(tmp_path, monkeypatch):
    """Un equipo de pega para ver A QUIEN SE LE PREGUNTA DE VERDAD, sin salir a internet.

    Lo impuso DeepSeek auditando esta vigia: "eso SOLO se prueba ejecutando con un espia, no
    mirando el codigo". Mirar el codigo dice lo que parece; el espia dice lo que pasa.

    Se usan dos Gemini como los gratis (dos, para que se les pregunte A LA VEZ, que es el camino
    donde estaba el peligro) y DeepSeek como el de pago.
    """
    monkeypatch.setattr(cuotas, "RUTA", str(tmp_path / "CUOTAS.json"))
    registro = []
    manda = {"un_gratis_contesta": False}

    def _gemini_de_pega(prompt, temperatura, modelo):
        registro.append("gratis")
        if manda["un_gratis_contesta"]:
            return "lo resuelvo yo, que soy gratis"
        raise RuntimeError("429 quota")

    def _deepseek_de_pega(prompt, temperatura, modelo):
        registro.append("deepseek")
        return "contesto el de pago"

    monkeypatch.setattr(obrero, "quienes_hay", lambda: ["gemini", "gemini2", "deepseek"])
    monkeypatch.setattr(obrero, "_gemini_directo", _gemini_de_pega)
    monkeypatch.setattr(obrero, "_deepseek_directo", _deepseek_de_pega)
    return registro, manda


def test_si_un_gratis_contesta_al_de_PAGO_NO_SE_LE_LLAMA(equipo_de_mentira):
    """LA PRUEBA QUE CUIDA EL DINERO DE JULIO.

    A los cerebros se les pregunta A TODOS A LA VEZ, porque "son todos gratis, preguntar no
    cuesta". Con uno de pago dentro eso seria una llamada pagada en CADA pregunta, aunque
    contestase antes uno gratis. Si esta vigia se pone roja, a Julio le estan cobrando de mas.
    """
    registro, manda = equipo_de_mentira
    manda["un_gratis_contesta"] = True
    txt, quien, _ = obrero._preguntar_con_relevo("una pregunta cualquiera", 0.2)
    assert txt, "no contesto nadie"
    assert quien != "deepseek", "contesto el de pago habiendo uno gratis que podia"
    assert "deepseek" not in registro, \
        "se le pregunto al de PAGO aunque un gratis contesto: eso le cuesta dinero a Julio"


def test_al_de_pago_solo_cuando_NINGUN_gratis_pudo_y_UNA_sola_vez(equipo_de_mentira):
    """Y cuando de verdad no queda nadie gratis, entra el de pago: una sola vez, y el ultimo."""
    registro, manda = equipo_de_mentira
    manda["un_gratis_contesta"] = False
    txt, quien, avisos = obrero._preguntar_con_relevo("una pregunta cualquiera", 0.2)
    assert quien == "deepseek", "se agotaron todos los gratis y el de pago no entro al rescate"
    assert txt, "el de pago no devolvio nada"
    assert registro.count("deepseek") == 1, \
        "se llamo al de pago %d veces: cada una cuesta dinero" % registro.count("deepseek")
    assert registro[-1] == "deepseek", "al de pago se le pregunto antes de agotar los gratis"
    assert any("SE PAGA" in a for a in avisos), \
        "no se avisa de que contesto el de pago: Julio tiene que enterarse de cuando gasta"


def test_la_llamada_al_de_pago_tiene_tope_de_tiempo():
    """DeepSeek: "si se cuelga, Julio paga igual". La de pago va con tope, como todas."""
    import ast
    arbol = ast.parse(open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8").read())
    fn = next((n for n in ast.walk(arbol)
               if isinstance(n, ast.FunctionDef) and n.name == "_ultimo_recurso"), None)
    assert fn is not None, "NO_ENCONTRADO: no existe el ultimo recurso del cerebro de pago"
    usados = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name)}
    assert "_con_tope" in usados, \
        "la llamada al cerebro de pago no lleva tope de tiempo: si se cuelga, Julio paga igual"


def test_quedarse_sin_saldo_es_agotarse_no_un_fallo():
    """Es el UNICO de pago. Si se queda sin saldo y no se le manda a dormir, se le reintenta
    una y otra vez en balde. Un cerebro de pago mal tratado sale mas caro que no tenerlo."""
    for texto in ("Insufficient Balance",
                  "402 Client Error: Payment Required",
                  "insufficient_quota"):
        assert cuotas.es_agote(texto), \
            "quedarse sin saldo (%r) no se reconoce como agotado: se reintentara gastando" % texto
