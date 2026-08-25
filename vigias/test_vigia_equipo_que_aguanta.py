# -*- coding: utf-8 -*-
"""VIGIA — a quien ya no le cupo, no se le vuelve a pedir lo mismo.

Ley: CONTRATO_EQUIPO_QUE_AGUANTA.md (Julio, 2026-08-24).

FALLO REAL QUE LA TRAE: Cline entrego una prueba diciendo que el equipo la habia auditado. Tenia
cinco fallos y uno borraba textos reales de Julio. No fue descuido: los dos obreros gratis
devolvieron 413 Payload Too Large en TODAS las llamadas sobre Foto Informe ese dia, o sea que
NUNCA vieron el codigo. Y se les seguia eligiendo en cada intento.

CAUSA RAIZ (declarada y medida): el techo de cada cerebro SOLO SUBE. `CAPACIDAD` cree la promesa
del proveedor (Groq: 500.000 letras), `_capacidad` se queda con el maximo entre la promesa y lo
medido, y `apuntar_uso` solo apunta tamaño cuando el cerebro ACIERTA. Reventar por tamaño no
enseñaba nada.

ESTA VIGIA NACE ROJA. Se puso a prueba saboteando: quitando la cura, se pone roja.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from cuerpo import cuotas  # noqa: E402


@pytest.fixture(autouse=True)
def _memoria_de_mentira(tmp_path, monkeypatch):
    """NUNCA se escribe en la memoria de verdad desde una comprobacion.

    Leccion ya vivida: una comprobacion escribio su copia vacia encima de la memoria real y se
    perdieron 27 de 32 errores aprendidos.
    """
    monkeypatch.setattr(cuotas, "RUTA", str(tmp_path / "cuotas_de_mentira.json"), raising=False)
    monkeypatch.setattr(cuotas, "_medidas", lambda: {}, raising=False)


def test_existe_la_forma_de_apuntar_que_no_le_cupo():
    """Sin esto, la leccion no se puede aprender: no hay donde apuntarla."""
    assert hasattr(cuotas, "apuntar_no_cupo"), (
        "no hay forma de apuntar que a un cerebro NO le cupo el encargo. Sin eso, el techo solo "
        "sube y se le sigue mandando trabajo que no aguanta (fallo real del 2026-08-24).")


def test_el_techo_BAJA_cuando_no_le_cupo():
    """Es el unico numero que debe poder bajar. Bajarlo ES la leccion."""
    antes = cuotas._capacidad("groq")
    assert antes > 50000, "la prueba no vale: groq deberia empezar con un techo alto"
    cuotas.apuntar_no_cupo("groq", 50000)
    despues = cuotas._capacidad("groq")
    assert despues < antes, (
        "tras reventar por tamaño, el techo NO bajo: se le va a volver a mandar lo mismo. "
        "Julio: 'legislar con datos, no con suposiciones'.")
    assert despues < 50000, (
        "el techo quedo por encima del tamaño que ya reviento: volveria a fallar igual")


def test_ya_no_se_le_elige_para_ese_tamano():
    """La consecuencia que importa: dejar de mandarle lo que no puede."""
    cuotas.apuntar_no_cupo("groq", 50000)
    elegidos = cuotas.rankear(["groq", "deepseek"], 50000)
    assert "groq" not in elegidos, (
        "se le sigue eligiendo para un tamaño con el que YA reviento")
    assert "deepseek" in elegidos, (
        "se saco tambien al que si aguanta: eso deja a Julio sin equipo")


def test_sigue_valiendo_para_lo_que_SI_le_cabe():
    """No se le castiga para siempre: solo se le deja de mandar lo que no aguanta."""
    cuotas.apuntar_no_cupo("groq", 50000)
    assert "groq" in cuotas.rankear(["groq", "deepseek"], 1000), (
        "se le aparto de TODO por un fallo de tamaño. Un encargo pequeño si lo aguanta.")


def test_el_techo_se_queda_con_el_MAS_BAJO():
    """Si revienta dos veces, manda la evidencia mas dura, no la ultima."""
    cuotas.apuntar_no_cupo("groq", 50000)
    cuotas.apuntar_no_cupo("groq", 20000)
    cuotas.apuntar_no_cupo("groq", 90000)
    assert cuotas._capacidad("groq") < 20000, (
        "el techo no se quedo con la evidencia mas dura: un fallo posterior mas grande no puede "
        "borrar lo que ya se sabe que no cabe")


def test_se_reconoce_el_fallo_de_que_no_cupo():
    """Con las frases REALES que devolvieron los cerebros el 2026-08-24, no inventadas."""
    assert hasattr(cuotas, "es_no_cupo"), (
        "no hay forma de reconocer un fallo por tamaño: entonces nunca se apunta el techo y "
        "la cura no sirve de nada")
    reales = [
        "HTTP Error 413: Payload Too Large",
        "HTTP Error 413: Request Entity Too Large",
        "This model's maximum context length is 8192 tokens",
        "request too large for model",
        "payload too large",
    ]
    for msg in reales:
        assert cuotas.es_no_cupo(msg), "no reconoce que NO LE CUPO: %r" % msg
    for msg in ["HTTP Error 429: Too Many Requests", "HTTP Error 503: Service Unavailable",
                "pon GEMINI_API_KEY", "contesto vacio", ""]:
        assert not cuotas.es_no_cupo(msg), (
            "confunde otro fallo con uno de tamaño y le bajaria el techo sin motivo: %r" % msg)


def test_el_obrero_lo_apunta_cuando_pasa():
    """Un candado que nadie llama es teatro. El obrero TIENE que apuntarlo al fallar."""
    codigo = open(os.path.join(AQUI, "cuerpo", "obrero.py"),
                  encoding="utf-8", errors="replace").read()
    assert "apuntar_no_cupo" in codigo, (
        "el obrero nunca apunta que a un cerebro no le cupo: el techo no bajaria jamas y se le "
        "seguiria mandando lo que no aguanta (fallo real del 2026-08-24)")
    assert "es_no_cupo" in codigo, (
        "el obrero no distingue un fallo por tamaño de otro cualquiera")


def test_la_ley_esta_escrita_donde_se_lee():
    ley = os.path.join(AQUI, "CONTRATO_EQUIPO_QUE_AGUANTA.md")
    assert os.path.exists(ley), "falta el contrato escrito de esta ley"
    texto = open(ley, encoding="utf-8", errors="replace").read().lower()
    for palabra in ("no cupo", "sin_auditar", "deepseek", "foto informe"):
        assert palabra in texto, (
            "el contrato ya no dice '%s': la ley se esta vaciando" % palabra)
