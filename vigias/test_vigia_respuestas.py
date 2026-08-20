# -*- coding: utf-8 -*-
"""VIGIA 16 — ¿LA RESPUESTA SIRVIO? (Julio, 2026-08-20).

  "No solo que se respondio, despues falta evaluar si fue correcta la respuesta,
   de lo contrario de nada sirve"

Es el error de siempre con otra cara: dar por buena una respuesta solo porque existe es lo
mismo que dar por probada una reparacion solo porque la vigia esta verde.

LA SEÑAL OBJETIVA, la que Julio lleva repitiendo desde el primer dia:
**si tiene que repetir la instruccion, la respuesta NO sirvio.**

Lo que se vigila aqui: que nada nazca dandose por bueno, y que la repeticion se detecte sola.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import respuestas


@pytest.fixture(autouse=True)
def _limpio(tmp_path, monkeypatch):
    monkeypatch.setattr(respuestas, "RUTA", str(tmp_path / "RESPUESTAS.json"))
    yield


def test_una_respuesta_NACE_sin_evaluar():
    """Lo mas importante: nada se da por bueno solo por existir."""
    r = respuestas.apuntar("que color quieres", "azul")
    assert r["evaluacion"] == "PENDIENTE", "nacio dandose por buena"


def test_si_julio_lo_repite_la_anterior_queda_NO_SIRVIO():
    """El corazon: repetirse es la prueba objetiva de que la respuesta no sirvio."""
    respuestas.apuntar("que medidor querias para el paquete", "el de acierto")
    n = respuestas.apuntar("que medidor querias exactamente para el paquete", "te repito: acierto")
    assert n["repitio_a"], "no detecto que Julio estaba repitiendo lo mismo"
    anterior = respuestas._leer()[0]
    assert anterior["evaluacion"] == "NO_SIRVIO", anterior


def test_dos_preguntas_distintas_NO_cuentan_como_repeticion():
    """Si todo pareciera repeticion, el numero no valdria para nada."""
    respuestas.apuntar("de que color el boton de aprobar", "verde")
    n = respuestas.apuntar("cuantos empleados tiene la empresa", "quince")
    assert not n["repitio_a"], f"conto como repeticion algo que no lo es: {n['repitio_a']}"


def test_solo_julio_puede_decir_que_una_respuesta_sirvio():
    respuestas.apuntar("una pregunta cualquiera del sistema", "una respuesta")
    r = respuestas.resumen()
    assert r["sirvieron"] == 0, "se dio por buena sin que Julio lo dijera"
    respuestas.evaluar("una pregunta cualquiera del sistema", "SIRVIO")
    assert respuestas.resumen()["sirvieron"] == 1


def test_el_contador_de_repeticiones_es_el_termometro():
    respuestas.apuntar("como se guarda el perfil de la empresa", "asi")
    respuestas.apuntar("como se guarda el perfil de la empresa otra vez", "que te lo repito")
    assert respuestas.resumen()["veces_que_julio_repitio"] == 1


def test_sin_datos_no_se_inventa_un_porcentaje():
    assert "todavia no" in respuestas.texto().lower()


# ─── ACLARAR no es NO_SIRVIO (Julio, 2026-08-20) ────────────────────────────────
def test_aclarar_NO_cuenta_como_respuesta_equivocada():
    """Julio: 'no lo marques como una respuesta que no sirvio, sino como una que debe ser
    aclarada, que es muy diferente; se trata solo de argumentar de manera diferente'.

    Si se confunden, el sistema aprende mal: daria por erroneo el CONTENIDO cuando lo que
    fallo fue la FORMA, y se acabaria cambiando algo que ya estaba bien."""
    respuestas.apuntar("una explicacion correcta pero enrevesada", "la respuesta buena")
    respuestas.evaluar("una explicacion correcta pero enrevesada", "ACLARAR")
    r = respuestas.resumen()
    assert r["equivocadas"] == 0, "conto como equivocada una que solo habia que explicar mejor"
    assert r["hubo_que_aclarar"] == 1
    assert r["acierto"] == 100.0, "el CONTENIDO era correcto: el acierto no puede bajar"


def test_se_mide_aparte_cuando_el_ingeniero_se_explica_mal():
    """Es un problema distinto y se arregla distinto: uno cambia la respuesta, otro la explicacion."""
    respuestas.apuntar("algo que se explico fatal pero era correcto", "x")
    respuestas.evaluar("algo que se explico fatal pero era correcto", "ACLARAR")
    assert respuestas.resumen()["me_explique_mal"] == 100.0


def test_una_respuesta_equivocada_SI_baja_el_acierto():
    """La otra mitad: lo que de verdad estaba mal tiene que notarse."""
    respuestas.apuntar("primera cosa bien contestada del todo", "a")
    respuestas.evaluar("primera cosa bien contestada del todo", "SIRVIO")
    respuestas.apuntar("segunda cosa contestada al reves", "b")
    respuestas.evaluar("segunda cosa contestada al reves", "NO_SIRVIO")
    r = respuestas.resumen()
    assert r["equivocadas"] == 1 and r["acierto"] == 50.0, r
