import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo import obrero


PROPUESTA_OK = json.dumps({"archivo": "x.py", "texto_viejo": "a", "texto_nuevo": "b"})


def _preparar(monkeypatch, material):
    monkeypatch.setattr(obrero, "_propuesta_cumple", lambda p, c: (True, ""))
    monkeypatch.setattr(obrero, "_validar_en_paquete", lambda *a, **k: [])
    monkeypatch.setattr(obrero, "_filtrar_paquete", lambda paquete, **k: material)
    prompts = []

    def falsa_obrero(prompt, *a, **k):
        prompts.append(prompt)
        return (PROPUESTA_OK, "deepseek", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", falsa_obrero)
    llamadas_auditar = []

    def aud(*a, **k):
        llamadas_auditar.append((a, k))
        return ({"veredicto": "APROBADO"}, "groq", [])

    monkeypatch.setattr(obrero, "auditar", aud)
    return prompts, llamadas_auditar


ENCARGO = (
    "Cambia en cuerpo/obrero.py la funcion _prompt_obrero para que respete "
    "el generador pedido."
)

MATERIAL_SIN_PIEZA = "# PAQUETE\n- cuerpo/otra_cosa.py (10 lineas)\n- cuerpo/y_otra.py (5 lineas)\n"

MATERIAL_CON_PIEZA = (
    "# PAQUETE\n"
    "### cuerpo/obrero.py\n"
    "```\n"
    "def _prompt_obrero(...):\n"
    "    ...\n"
    "```\n"
)


def test_material_sin_pieza_no_llama_a_la_ia(monkeypatch):
    prompts, _ = _preparar(monkeypatch, MATERIAL_SIN_PIEZA)
    resultado = obrero.trabajar(
        ENCARGO, generador="deepseek", auditor="bigpickle"
    )
    assert prompts == []
    texto = json.dumps(resultado, ensure_ascii=False)
    assert "FALTA_MATERIAL" in texto
    assert "NECESITO_LEER" in texto
    assert "cuerpo/obrero.py" in texto


def test_material_con_pieza_si_llama_a_la_ia(monkeypatch):
    prompts, _ = _preparar(monkeypatch, MATERIAL_CON_PIEZA)
    obrero.trabajar(ENCARGO, generador="deepseek", auditor="bigpickle")
    assert len(prompts) >= 1
