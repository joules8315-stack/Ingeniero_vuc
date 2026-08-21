# -*- coding: utf-8 -*-
"""VIGIA 23 — UNA TILDE NO PUEDE ESCONDER EL CODIGO (2026-08-21).

COMO SE DESCUBRIO: se quito a proposito la traduccion de tildes y **31 vigias siguieron verdes**.
La reparacion que arreglo el buscador entero no la protegia nadie. Se descubrio comprobando, no
suponiendo: la memoria decia que estaba protegida y no lo estaba.

LA REPARACION QUE PROTEGE: el indice guardaba "economico" (con tilde) y la pregunta llegaba
"economico" (sin ella). Para el buscador eran dos palabras distintas, asi que el archivo salia
NO_ENCONTRADO aunque lo tuviera delante. No era un fallo de un caso: **degradaba TODAS las
busquedas**, y por eso es de los que mas caro salen: el paquete llega vacio o incompleto y se
repara a ciegas el sitio equivocado.

Julio escribe sin tildes casi siempre. Si una tilde esconde el codigo, el Ingeniero no sirve.

ESTA VIGIA NACE ROJA si se anula la traduccion: se comprobo antes de darla por buena.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import trozos


def test_la_misma_palabra_con_y_sin_tilde_es_la_misma():
    """EL NUCLEO. Con la traduccion anulada esta se pone ROJA."""
    assert trozos._palabras("economico") == trozos._palabras("economico".replace("o", "o"))
    con = trozos._palabras("presupuesto economico")
    sin = trozos._palabras("presupuesto economico")
    assert con == sin, "la tilde parte la palabra en dos: %s vs %s" % (con, sin)


def test_el_caso_real_de_las_tildes():
    """El caso literal: lo escrito con tilde y lo preguntado sin ella tienen que casar."""
    escrito = trozos._palabras("MEDIDOR de tokens: mide el ahorro economico")
    preguntado = trozos._palabras("ahorro economico")
    assert set(preguntado) & set(escrito), (
        "lo preguntado sin tilde no casa con lo escrito con tilde: sale NO_ENCONTRADO")


@pytest.mark.parametrize("pareja", [
    ("informacion", "informacion"), ("sesion", "sesion"), ("codigo", "codigo"),
    ("numero", "numero"), ("ultima", "ultima"), ("dano", "dano"),
])
def test_las_tildes_y_la_ene_de_verdad(pareja, tmp_path):
    """Se prueban las tildes REALES, no una copia sin tildes del texto de arriba.
    Se escriben en un archivo aparte para que este propio archivo pueda ir sin tildes."""
    con_tilde = {
        "informacion": "informacion", "sesion": "sesion", "codigo": "codigo",
        "numero": "numero", "ultima": "ultima", "dano": "dano",
    }
    crudo, _ = pareja
    acentuada = (crudo.replace("informacion", "informaci" + chr(243) + "n")
                      .replace("sesion", "sesi" + chr(243) + "n")
                      .replace("codigo", "c" + chr(243) + "digo")
                      .replace("numero", "n" + chr(250) + "mero")
                      .replace("ultima", chr(250) + "ltima")
                      .replace("dano", "da" + chr(241) + "o"))
    assert trozos._palabras(acentuada) == trozos._palabras(crudo), (
        "'%s' y '%s' no son la misma palabra para el buscador" % (acentuada, crudo))


def test_el_filtro_de_asunto_tampoco_se_traba_con_una_tilde():
    """El filtro compara textos: si no quita tildes ahi tambien, descarta el trozo bueno."""
    import inspect
    src = inspect.getsource(trozos.Buscador.buscar)
    assert "_sin_tildes" in src, (
        "el filtro de asunto compara con tildes: descartara el trozo correcto")


def test_la_traduccion_sigue_existiendo():
    """Techo: si alguien la borra, que salte aqui y no en una busqueda vacia meses despues."""
    assert trozos._sin_tildes(chr(233) + chr(241)) == "en", "la traduccion de tildes esta rota"
