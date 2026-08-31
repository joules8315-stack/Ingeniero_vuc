# -*- coding: utf-8 -*-
"""VIGIA — una vuelta YA PAGADA no se pierde cuando el revisor contesta roto.

ENCARGO de Claude a Cline (2026-08-31): en cuerpo/obrero.py, en trabajar(), al revisor
(auditor) se le pregunta UNA sola vez. Si contesta algo ilegible (o no contesta), se tira la
propuesta buena del obrero — la vuelta ya pagada. Medido: paso DOS veces hoy.

La cura YA EXISTE en cuerpo/cruzado.py, en resolver(): reintenta 2 veces cuando el juez
devuelve algo ilegible (puesto desde el 2026-08-27). Esa cura nunca llego a obrero.trabajar().
Esta vigia comprueba que llego.

NACE ROJA: hoy el revisor roto no se vuelve a preguntar, y el informe miente poniendo '?'.
No llama a ningun cerebro: se le da de comer al relevo un caso de mentira. Determinista.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

import cuerpo.obrero as obrero  # noqa: E402

_PROPUESTA = ('{"diagnostico":"algo esta mal","archivo":"cuerpo/obrero.py",'
              '"cambio":"cambiar esto","codigo":"x = 1","confianza":"media"}')
_RESPUESTA_BUENA = '{"veredicto":"APROBADO","invento_algo":false,"fallos":[]}'


def test_el_revisor_roto_no_tira_la_vuelta_pagada(monkeypatch):
    """El revisor contesta ROTO la 1ra vez; se le vuelve a preguntar y la propuesta no se pierde."""
    monkeypatch.setattr(obrero, "prestar_cerebro", lambda: (object(), None))
    monkeypatch.setattr(obrero, "quienes_hay", lambda: True)
    veces = {"revisor": 0}

    def _falso_relevo(prompt, *a, **k):
        if "Eres el OBRERO" in str(prompt):
            return (_PROPUESTA, "deepseek", [])
        veces["revisor"] += 1                       # es el revisor (auditor)
        if veces["revisor"] == 1:
            return ("", "gemini2", ["el revisor contesto roto"])   # ilegible: no se entiende
        return (_RESPUESTA_BUENA, "gemini3", [])    # se le pidio de nuevo: contesta bien

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", _falso_relevo)

    r = obrero.trabajar("un paquete de texto cualquiera", "una tarea cualquiera")
    assert veces["revisor"] >= 2, (
        "al revisor se le pregunto UNA sola vez y contesto roto: se perdio la vuelta YA PAGADA "
        "del obrero. La cura de cruzado.py (reintentar) no llego a obrero.trabajar().")
    assert r.get("auditoria", {}).get("veredicto") == "APROBADO", (
        "aunque el revisor contesto roto la 1ra vez, no se le volvio a preguntar: la propuesta "
        "buena del obrero se tiro, y esa vuelta ya estaba pagada.")


def test_el_informe_dice_que_el_revisor_contesto_roto(monkeypatch):
    """Si ni reintentando queda revisor, el informe lo dice claro; no miente con '?'."""
    monkeypatch.setattr(obrero, "prestar_cerebro", lambda: (object(), None))
    monkeypatch.setattr(obrero, "quienes_hay", lambda: True)

    def _falso_relevo(prompt, *a, **k):
        if "Eres el OBRERO" in str(prompt):
            return (_PROPUESTA, "deepseek", [])
        return ("", "gemini2", ["el revisor contesto roto"])   # nunca contesta bien

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", _falso_relevo)

    r = obrero.trabajar("un paquete de texto", "una tarea")
    resumen = (r.get("auditoria", {}).get("resumen_para_el_jefe") or "")
    assert "roto" in resumen.lower(), (
        "el informe no dice que el revisor contesto roto: miente poniendo '?'. Debe decirlo "
        "claro, para que se sepa que la vuelta se perdio por el revisor, no por el trabajo.")
