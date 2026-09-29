# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_documento_del_proyecto_no_es_libre.py

VIGIA QUE NACE ROJA A PROPOSITO (2026-09-29).

Julio, con razon: "hijo de puta porque estas escribiendo otra vez a mano". Un documento
que vive dentro de un proyecto suyo se puede escribir a solas, sin que el equipo lo revise,
porque el guardian del equipo lo deja pasar por no ser codigo. Julio ordeno: "pon un candado
que ni por el putas se pueda abrir".

EVIDENCIA: hoy 2026-09-29 quedaron 189 apuntes en memoria/SIN_EQUIPO.log con el sello exacto
"DEJO PASAR: documento libre", dos de ellos documentos metidos dentro del proyecto a las
16:20 y a las 16:36. El renglon que lo deja pasar dice, tal cual:
    _apuntar_frenada(fp, "DEJO PASAR: documento libre")
y despues devuelve cero.

LO QUE SE VIGILA: arnes/candado_equipo.py, su funcion main, que lee la peticion por la
entrada y devuelve DOS cuando frena y CERO cuando deja pasar.

TRES CASOS:
  1. Un documento .md DENTRO de un proyecto de Julio, sin veredicto del equipo, se FRENA
     (debe devolver 2). Hoy devuelve 0: por eso esta prueba nace ROJA.
  2. Un documento .md FUERA de todo proyecto (carpeta temporal) NO se frena (debe devolver 0).
     Ya esta verde hoy y tiene que seguir verde: un borrador no debe frenar a nadie.
  3. Un documento .md DENTRO de la carpeta de memoria de la herramienta NO se frena
     (debe devolver 0). La herramienta escribe sus apuntes sola todo el dia.

NO SE TOCA: solo se crea este archivo de prueba. No se toca el guardian, ni ningun otro
candado, ni ingeniero.py, ni ninguna otra prueba. El arreglo entra en la ronda siguiente.

PROMESA DE SABOTAJE: cuando el arreglo entre, quien revise lo deshace y comprueba que el
primer caso vuelve a rojo.

Sin IA, sin red, sin lanzar procesos. Nada se escribe fuera de la carpeta temporal; en
particular esta prueba NO escribe en la memoria de verdad del proyecto.
"""
import io
import json
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# MONTAJE: se copia el de vigias/test_vigia_equipo_siempre.py
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)              # un nivel arriba de vigias
ARNES = os.path.join(RAIZ, "arnes")

for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import candado_equipo  # noqa: E402  (el guardian que se vigila)


# ---------------------------------------------------------------------------
# LAS TRES PUERTAS DE PRUEBA (nombres EXACTOS, escritos literal)
# ---------------------------------------------------------------------------
PUERTA_VEREDICTO = "INGENIERO_VEREDICTO_TEST"
PUERTA_SIN_EQUIPO = "INGENIERO_SIN_EQUIPO_TEST"
PUERTA_CASA = "INGENIERO_CASA_TEST"


def _peticion(fp):
    """Arma la entrada que el guardian lee por la entrada estandar."""
    return json.dumps({"tool_input": {"file_path": fp}})


def _correr_guardian(monkeypatch, fp):
    """Sustituye la entrada estandar por la peticion y devuelve el codigo del guardian."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(_peticion(fp)))
    return candado_equipo.main()


def _poner_puertas(monkeypatch, tmp_path, con_casa):
    """Pone SIEMPRE las dos puertas de veredicto y apuntes a la carpeta temporal.

    La tercera (casa) solo se pone cuando el caso lo pide. PROHIBIDO inventar nombres,
    PROHIBIDO getattr y PROHIBIDO nombre de reserva: si se pone un nombre que no existe,
    la prueba escribe en el cuaderno de verdad del proyecto.
    """
    monkeypatch.setenv(PUERTA_VEREDICTO, str(tmp_path / "veredicto"))
    monkeypatch.setenv(PUERTA_SIN_EQUIPO, str(tmp_path / "sin_equipo"))
    if con_casa:
        monkeypatch.setenv(PUERTA_CASA, str(tmp_path))
    else:
        monkeypatch.delenv(PUERTA_CASA, raising=False)


# ---------------------------------------------------------------------------
# CASO 1: documento DENTRO de un proyecto de Julio -> SE FRENA (debe devolver 2)
# ---------------------------------------------------------------------------
def test_documento_dentro_del_proyecto_se_frena(monkeypatch, tmp_path):
    """Un .md dentro de una casa, sin veredicto del equipo, tiene que devolver DOS.

    Hoy devuelve CERO porque lo deja pasar como documento libre. Esta prueba nace ROJA.
    """
    _poner_puertas(monkeypatch, tmp_path, con_casa=True)

    # el documento vive DENTRO de la carpeta temporal, que es una casa
    doc = tmp_path / "notas_del_proyecto.md"
    doc.write_text("documento escrito a solas\n", encoding="utf-8")

    codigo = _correr_guardian(monkeypatch, str(doc))

    assert codigo == 2, (
        "El guardian devolvio %r y tenia que devolver 2: hoy devuelve cero porque lo deja "
        "pasar como documento libre. Un documento dentro de un proyecto de Julio no se "
        "escribe a solas: tiene que frenarse sin veredicto del equipo." % (codigo,)
    )


# ---------------------------------------------------------------------------
# CASO 2: documento FUERA de todo proyecto -> NO se frena (debe devolver 0)
# ---------------------------------------------------------------------------
def test_documento_fuera_de_todo_proyecto_no_se_frena(monkeypatch, tmp_path):
    """Un .md en la carpeta temporal, sin casa, tiene que devolver CERO.

    Este caso ya esta verde hoy y tiene que seguir verde: un borrador no debe frenar a nadie.
    """
    _poner_puertas(monkeypatch, tmp_path, con_casa=False)

    doc = tmp_path / "borrador_suelto.md"
    doc.write_text("borrador temporal\n", encoding="utf-8")

    codigo = _correr_guardian(monkeypatch, str(doc))

    assert codigo == 0, (
        "El guardian devolvio %r y tenia que devolver 0: un documento fuera de todo proyecto "
        "es un borrador y no debe frenar a nadie." % (codigo,)
    )


# ---------------------------------------------------------------------------
# CASO 3: apuntes de la propia herramienta -> NO se frenan (debe devolver 0)
# ---------------------------------------------------------------------------
def test_apuntes_de_la_herramienta_no_se_frenan(monkeypatch, tmp_path):
    """Un .md dentro de la carpeta de memoria de la herramienta tiene que devolver CERO.

    La herramienta escribe sus apuntes sola todo el dia; frenarlos la dejaria muerta.
    """
    _poner_puertas(monkeypatch, tmp_path, con_casa=False)

    memoria = RAIZ / "memoria" if hasattr(RAIZ, "__truediv__") else os.path.join(RAIZ, "memoria")
    # la carpeta de memoria de la herramienta, tal cual vive en este proyecto
    memoria = os.path.join(RAIZ, "memoria")
    doc = os.path.join(memoria, "apunte_de_la_herramienta.md")

    codigo = _correr_guardian(monkeypatch, doc)

    assert codigo == 0, (
        "El guardian devolvio %r y tenia que devolver 0: los apuntes de la propia "
        "herramienta no se frenan, o la herramienta queda muerta." % (codigo,)
    )
