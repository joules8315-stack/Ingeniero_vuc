"""Vigia: el pit mira la prueba antes de dar por hecho que una tarea esta terminada.

El 2026-09-20 el pit dio por terminadas tres tareas solo porque se guardaron,
sin mirar ni una vez si la prueba de cada tarea estaba verde. Una de ellas dejo
en la historia una prueba que no podia estar verde nunca.

Dar por hecho lo que no se ha comprobado es lo contrario de A-7.

Esta vigia nace ROJA: exige que capataz.la_tarea_esta_terminada consulte de
verdad los pasos de la prueba (comprobar_pasos) antes de responder que una
tarea esta terminada.
"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARNES = os.path.join(RAIZ, "arnes")
for _ruta in (RAIZ, ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from cuerpo import capataz


def test_el_pit_mira_la_prueba_antes_de_dar_por_hecho(monkeypatch):
    """Sin mirar la prueba, el pit da por hecho lo que no ha comprobado."""
    llamadas = []

    def comprobar_pasos_falso(orden):
        llamadas.append(orden)
        return ""

    monkeypatch.setattr(capataz, "comprobar_pasos", comprobar_pasos_falso)

    orden = {"id": 7}
    resultado = capataz.la_tarea_esta_terminada(orden)

    assert isinstance(resultado, dict), (
        "la_tarea_esta_terminada debe devolver un diccionario"
    )
    assert resultado.get("ok") is True, (
        "sin mirar la prueba el pit da por hecho lo que no ha comprobado"
    )
    assert len(llamadas) == 1, (
        "sin mirar la prueba el pit da por hecho lo que no ha comprobado"
    )


def test_una_tarea_con_prueba_roja_no_esta_terminada(monkeypatch):
    """Una tarea cuya prueba esta roja no esta terminada por mucho que se haya guardado."""
    llamadas = []

    def comprobar_pasos_falso(orden):
        llamadas.append(orden)
        return "vigia_verde"

    monkeypatch.setattr(capataz, "comprobar_pasos", comprobar_pasos_falso)

    orden = {"id": 7}
    resultado = capataz.la_tarea_esta_terminada(orden)

    assert isinstance(resultado, dict), (
        "la_tarea_esta_terminada debe devolver un diccionario"
    )
    assert resultado.get("ok") is False, (
        "una tarea cuya prueba esta roja no esta terminada por mucho que se haya guardado"
    )
    assert resultado.get("paso") == "vigia_verde", (
        "una tarea cuya prueba esta roja no esta terminada por mucho que se haya guardado"
    )
    razon = resultado.get("razon")
    assert isinstance(razon, str) and razon.strip() != "", (
        "una tarea cuya prueba esta roja no esta terminada por mucho que se haya guardado"
    )
