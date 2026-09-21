"""Vigia: ni con revisor fijo se aprueba a si mismo.

Julio, 2026-09-20.

La ley dice que quien escribio no puede aprobar su propio trabajo, aunque el
encargo pida ese revisor fijo. Esta vigia comprueba dos cosas:

1. Si el encargo pide como auditor al mismo cerebro que escribio (deepseek),
   el veredicto que sale NO puede ser APROBADO.
2. Si el encargo pide un auditor distinto (gemini4), el veredicto SI puede
   ser APROBADO: el freno nuevo no rompe el caso bueno.

OJO con la firma: obrero.auditar devuelve una TUPLA (auditoria, quien, avisos),
no un dict. Hay que desarmarla antes de mirar el veredicto.
"""

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

from cuerpo import obrero


MATERIAL_DE_PRUEBA = "material de prueba"
PROPUESTA_SENCILLA = "propuesta sencilla"


def _desarmar(resultado):
    """obrero.auditar devuelve (auditoria, quien, avisos). Lo dejamos claro."""
    assert isinstance(resultado, tuple) and len(resultado) == 3, (
        "obrero.auditar debe devolver una tupla (auditoria, quien, avisos); "
        "si cambio la firma, esta vigia tiene que enterarse"
    )
    auditoria, quien, avisos = resultado
    return auditoria, quien, avisos


def _veredicto(auditoria):
    """Saca el veredicto de la auditoria, sea dict o texto JSON."""
    if isinstance(auditoria, dict):
        return auditoria.get("veredicto")
    if isinstance(auditoria, str):
        import json
        try:
            return json.loads(auditoria).get("veredicto")
        except Exception:
            return None
    return None


def test_ni_con_revisor_fijo_se_aprueba_a_si_mismo(monkeypatch):
    """Aunque el encargo pida deepseek como auditor, deepseek no se aprueba."""

    def espia(prompt, temperatura, evitar=None, primero=None, pesado=False,
              clase=None, vuelta=None, **resto):
        # El espia contesta SIEMPRE con deepseek y veredicto APROBADO.
        return ('{"veredicto": "APROBADO", "resumen": "me reviso a mi mismo"}',
                "deepseek", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", espia)

    resultado = obrero.auditar(
        MATERIAL_DE_PRUEBA,
        PROPUESTA_SENCILLA,
        auditor="deepseek",
        evitar="deepseek",
    )
    auditoria, quien, avisos = _desarmar(resultado)

    veredicto = _veredicto(auditoria)
    assert veredicto != "APROBADO", (
        "quien escribio no puede aprobar su propio trabajo aunque el encargo "
        "pidiera ese revisor fijo; salio veredicto=%r con quien=%r"
        % (veredicto, quien)
    )
    assert quien != "deepseek", (
        "si se deja el nombre del que escribio como revisor, el registro del "
        "trabajo seguira diciendo que lo reviso otro; salio quien=%r"
        % (quien,)
    )


def test_un_revisor_distinto_si_aprueba(monkeypatch):
    """Con un revisor distinto al que escribio, el APROBADO si pasa."""

    def espia(prompt, temperatura, evitar=None, primero=None, pesado=False,
              clase=None, vuelta=None, **resto):
        # El espia contesta con gemini4 y veredicto APROBADO.
        return ('{"veredicto": "APROBADO", "resumen": "revisor distinto"}',
                "gemini4", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", espia)

    resultado = obrero.auditar(
        MATERIAL_DE_PRUEBA,
        PROPUESTA_SENCILLA,
        auditor="gemini4",
        evitar="deepseek",
    )
    auditoria, quien, avisos = _desarmar(resultado)

    veredicto = _veredicto(auditoria)
    assert veredicto == "APROBADO", (
        "un revisor distinto al que escribio SI debe poder aprobar; "
        "salio veredicto=%r con quien=%r" % (veredicto, quien)
    )
