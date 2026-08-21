# -*- coding: utf-8 -*-
"""VIGIA 27 — SOLO CODIGO A LA NUBE, NUNCA DATOS DE CLIENTES (Julio, 2026-08-21).

Julio lo decidio con los terminos de Google delante. En el plan GRATIS de Gemini, Google dice
que usa lo que se le manda para mejorar sus productos y que **personas** pueden leerlo ("human
reviewers may read, annotate, and process your API input and output"). No se puede desactivar en
el plan gratis; sus propios terminos avisan: "Do not submit sensitive, confidential, or personal
information to the Unpaid Services". Comprobado en ai.google.dev/gemini-api/terms.

POR QUE IMPORTA MAS DE LO QUE PARECE: Julio no vende programas, vende informes a empresas. El
telefono de un cliente suyo no es un dato suyo: es de su cliente. Soltarlo no es un descuido
tecnico, es un problema con quien le paga.

DONDE SE TAPA: en el UNICO sitio por donde sale todo, no en cada sitio que llama. Si depende de
acordarse en veinte sitios, un dia no se acuerda en uno.

LO QUE NO SE TAPA: codigo, nombres de archivo, numeros de linea, fechas, versiones y mensajes de
error. Si se tapara eso, el cerebro no podria reparar nada y el candado acabaria apagado.
"""
import inspect
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import privacidad, obrero


# ─── TAPA LO QUE ES DE UN CLIENTE ─────────────────────────────────────────────
@pytest.mark.parametrize("texto,marca", [
    ("Llamar a Maria Perez al 600123456 manana", "<TELEFONO>"),
    ("El cliente escribio desde maria.perez@empresa.es", "<CORREO>"),
    ("DNI 12345678Z del titular", "<DOCUMENTO>"),
    ("pago con la 4111 1111 1111 1111", "<TARJETA>"),
    ("GROQ_API_KEY=gsk_loquesea123", "<CLAVE>"),
])
def test_tapa_los_datos_de_cliente(texto, marca):
    limpio, n = privacidad.limpiar(texto)
    assert n >= 1, "no tapo nada en: %s" % texto
    assert marca in limpio, "no lo marco como %s: %s" % (marca, limpio)


def test_el_dato_original_DESAPARECE():
    """Lo que importa no es que ponga la marca, sino que el dato ya no este."""
    limpio, _ = privacidad.limpiar("Maria Perez, 600123456, maria@empresa.es")
    assert "600123456" not in limpio
    assert "maria@empresa.es" not in limpio


# ─── NO ESTORBA AL TRABAJO ────────────────────────────────────────────────────
@pytest.mark.parametrize("texto", [
    "app_web.html lineas 792-844",
    "el fallo salta en app.py:12392",
    "version 3.5.1 del 2026-08-21",
    "def guardar_informe(usuario_id, plantilla):",
    "HTTP Error 404: Not Found",
    "el color de fondo es #ff8800",
])
def test_no_toca_el_codigo(texto):
    """Si tapa cosas del codigo, el cerebro no puede reparar y el candado se acaba apagando."""
    limpio, n = privacidad.limpiar(texto)
    assert n == 0, "tapo algo que era del codigo: %r -> %r" % (texto, limpio)
    assert limpio == texto


# ─── ENGANCHADO DE VERDAD, Y EN UN SOLO SITIO ─────────────────────────────────
def test_esta_enganchado_donde_sale_todo():
    src = inspect.getsource(obrero._preguntar_con_relevo)
    assert "privacidad" in src, "la ley esta escrita pero no enganchada: no tapa nada"
    assert "prompt_nube" in src


def test_a_la_nube_va_el_encargo_LIMPIO():
    """El fallo que casi se cuela: se tapaba arriba y por otro camino salia sin tapar."""
    src = inspect.getsource(obrero._preguntar_con_relevo)
    codigo = [l for l in src.splitlines() if not l.strip().startswith("#")]
    for l in codigo:
        for puerta in ("_gemini_directo(", "_openrouter_directo(", "_preguntar_groq("):
            if puerta in l and "def " not in l:
                assert "prompt_nube" in l, (
                    "sale a la nube SIN limpiar por aqui: %s" % l.strip())


def test_al_cerebro_de_tu_PC_va_entero():
    """Ahi no sale nada del ordenador: taparlo solo empeoraria su respuesta."""
    src = inspect.getsource(obrero._preguntar_con_relevo)
    for l in src.splitlines():
        if "preguntar_local(" in l and "def " not in l:
            assert "prompt_nube" not in l, "al de casa se le manda recortado sin necesidad"


def test_no_hay_dos_caminos_para_hablar_con_la_nube():
    """Un camino duplicado es un agujero esperando su turno: ya paso hoy."""
    src = inspect.getsource(obrero._preguntar_con_relevo)
    codigo = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert codigo.count("_gemini_directo(") <= 1, "hay dos caminos hacia Gemini"
    assert codigo.count("_preguntar_groq(") <= 1, "hay dos caminos hacia Groq"
