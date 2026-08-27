# -*- coding: utf-8 -*-
"""VIGIA — L14 LA DECISION DE REPARAR: ANTES DE REPARAR SE RESPONDEN LAS 5 PREGUNTAS (Julio, 2026-08-27).

Julio: "ya sabes que vas a reparar, donde reparar, porque reparar, cuando vas a reparar y como lo vas
a reparar? si todo es positivo, legisla y repara, sino investiga, responde nuevamente las preguntas
y repara."

La causa raiz (candado_diagnostico) ya exige: archivo (donde), funcion (que), linea (donde exacto),
evidencia (por que / que se midio), cambio (que cambio). El protocolo paso 3 dice "causa raiz, nunca
sintoma". Esta vigia comprueba que la ley este escrita donde la leen y que el candado de decision
exista y exija lo que pide la ley (que / donde / por que).

Se vigila:
  1. la ley esta escrita en contrato + matriz + protocolo + CLAUDE,
  2. el candado de diagnostico exige las piezas de la decision (archivo, funcion, linea, evidencia,
     cambio, alcance),
  3. el protocolo tiene el paso 3 "causa raiz" con su candado,
  4. antes de reparar (comando causa) se declara la causa.
"""
import io
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys = __import__("sys")
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_la_ley_esta_escrita_donde_la_leen():
    contrato = _leer(os.path.join(AQUI, "CONTRATO_LEGISLACION_TOTAL.md")).lower()
    assert "antes de reparar" in contrato, "la ley de la decision de reparar no esta en el contrato"
    matriz = _leer(os.path.join(AQUI, "MATRIZ_LEGISLACION.md")).lower()
    assert "5 preguntas" in matriz or "las 5 preguntas" in matriz, \
        "la ley no esta en la matriz de legislacion"
    proto = _leer(os.path.join(AQUI, "PROTOCOLO_UNICO.md")).lower()
    assert "las 5 preguntas" in proto, "la ley no esta en el protocolo"
    claude = _leer(os.path.join(AQUI, "CLAUDE.md")).lower()
    assert "5 preguntas" in claude, "la ley no esta en CLAUDE.md"


def test_el_candado_de_diagnostico_exige_la_decision_completa():
    """La causa raiz exige las piezas de la decision: donde/que/por que (archivo, funcion, linea,
    evidencia, cambio, alcance). Sin eso es INFERIDO y lo inferido no se repara."""
    import candado_diagnostico as cd
    # declarar sin los campos obligatorios debe fallar
    r = cd.declarar("p", "a.py", "f", "1", "evi", "cambie una cosa", "sintoma", "3 de 10")
    assert "_error" not in r, "declarar una causa completa no debe fallar"
    r = cd.declarar("p", "", "", "", "", "", "", "")  # nada
    assert "_error" in r, "declarar sin nada debe fallar (lo inferido no se repara)"


def test_el_protocolo_tiene_el_paso_3_causa_raiz_con_candado():
    import cerebro.protocolo as pr
    paso3 = next((p for p in pr.PASOS if p.get("n") == 3), None)
    assert paso3, "falta el paso 3 del protocolo (causa raiz)"
    assert "causa" in paso3.get("nombre", "").lower() or "sintoma" in paso3.get("nombre", "").lower(), \
        "el paso 3 no es 'causa raiz'"
    assert paso3.get("candado"), "el paso 3 no tiene candado: es un deseo"
    assert pr.tiene_candado(paso3), "el candado del paso 3 no existe en el disco"


def test_antes_de_reparar_se_declara_la_causa():
    """El comando 'causa' existe y exige los campos de la decision (donde/que/por que)."""
    txt = _leer(os.path.join(AQUI, "ingeniero.py"))
    assert 'cmd == "causa"' in txt, "el comando causa no existe en ingeniero.py"
    for campo in ("--archivo", "--funcion", "--linea", "--evidencia", "--cambio", "--alcance"):
        assert campo in txt, "el comando causa no exige " + campo
