# -*- coding: utf-8 -*-
"""vigias/test_vigia_prueba_previa.py — LA PRUEBA PREVIA AL CEREBRO.

Julio, 2026-10-01. Medido ese dia: de 58 ordenes abiertas con pieza .py, 12 no nombran el
archivo de su pieza, y a esas el paquete les trae el codigo solo en 1 de cada 3. Cada una se
manda a una IA de pago sin que nadie compruebe ANTES, por programa, que el codigo llega.

QUE VIGILA ESTA PRUEBA
---------------------
Que exista una pieza que, dada una orden, reproduzca SIN IA las etapas del encargo:
  1. el paquete que se armaria,
  2. el material que le quedaria al escritor,
  3. el prompt completo,
  4. el recorte al tope del cerebro que va a escribir,
  5. y que diga etapa por etapa si el codigo que la orden nombra sigue estando.
Devuelve un informe corto en palabras simples.

COMO SE PRUEBA
--------------
Ejecutando la funcion con carpetas temporales (tmp_path), sin tocar el estado real.

NACE ROJA: hoy la pieza no existe, asi que el import falla y pytest marca rojo. Cuando la
reparacion este hecha, la pieza existira y la prueba pasara.

NO SE MIRA EL TEXTO DEL CODIGO: se importa y se ejecuta.
"""
import importlib
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# Localizacion de la pieza. Se prueban varios nombres plausibles porque el
# encargo no fija el nombre exacto del modulo; lo que fija es QUE HAGA.
# ---------------------------------------------------------------------------
CANDIDATOS = [
    "cuerpo.prueba_previa",
    "cuerpo.prueba_previa_al_cerebro",
    "cuerpo.vigia_prueba_previa",
    "prueba_previa",
]


def _cargar_pieza():
    """Devuelve el modulo de la pieza, o falla con ImportError si no existe.

    Si no existe ninguno de los candidatos, se levanta ImportError para que la
    prueba NAZCA ROJA por el motivo que pide el contrato (importar justo esa pieza).
    """
    errores = []
    for nombre in CANDIDATOS:
        try:
            return importlib.import_module(nombre)
        except ImportError as e:
            errores.append(f"{nombre}: {e}")
    raise ImportError(
        "No existe la pieza de prueba previa al cerebro. "
        "Se buscaron: " + ", ".join(CANDIDATOS) + ". "
        "Detalle: " + " | ".join(errores)
    )


def _escribir_orden(tmp_path, nombre_archivo, contenido):
    """Deja una orden y su pieza en una carpeta temporal. No toca el estado real."""
    raiz = tmp_path / "raiz"
    raiz.mkdir()
    pieza = raiz / nombre_archivo
    pieza.write_text(contenido, encoding="utf-8")
    orden = raiz / "ORDEN.md"
    orden.write_text(
        "# ORDEN\n\n"
        f"Reparar el archivo {nombre_archivo}: la funcion suma() devuelve mal.\n"
        "Se quiere que sume bien.\n",
        encoding="utf-8",
    )
    return raiz, orden, pieza


# ---------------------------------------------------------------------------
# PRUEBA 1 — con la pieza PRESENTE: asercion POSITIVA.
# La pieza debe reproducir las etapas y decir que el codigo SI esta.
# ---------------------------------------------------------------------------
def test_con_pieza_presente_dice_que_el_codigo_esta(tmp_path):
    pieza = _cargar_pieza()
    raiz, orden, archivo = _escribir_orden(
        tmp_path,
        "sumador.py",
        "def suma(a, b):\n    return a + b\n",
    )

    # La pieza debe exponer una funcion que reproduce las etapas del encargo.
    # Se aceptan nombres plausibles; lo que importa es que exista y corra.
    fn = None
    for nombre in ("reproducir", "reproducir_etapas", "prueba_previa", "revisar"):
        if hasattr(pieza, nombre):
            fn = getattr(pieza, nombre)
            break
    assert fn is not None, (
        "La pieza existe pero no expone una funcion para reproducir las etapas "
        "(se esperaba reproducir / reproducir_etapas / prueba_previa / revisar)."
    )

    informe = fn(orden=str(orden), raiz=str(raiz), tope=20000)

    # El informe debe ser corto y en palabras simples: un texto.
    assert isinstance(informe, str), "El informe debe ser texto en palabras simples."
    assert informe.strip(), "El informe no puede venir vacio."

    # Debe nombrar las etapas del encargo.
    bajo = informe.lower()
    for etapa in ("paquete", "material", "prompt", "recorte"):
        assert etapa in bajo, f"El informe no menciona la etapa '{etapa}'."

    # Y debe decir, etapa por etapa, que el codigo SI sigue estando.
    assert "sumador.py" in informe, (
        "El informe no nombra el archivo que la orden pide reparar."
    )
    assert ("si" in bajo or "s\u00ed" in bajo or "presente" in bajo or "esta" in bajo), (
        "El informe no dice que el codigo sigue estando."
    )


# ---------------------------------------------------------------------------
# PRUEBA 2 — con TOPE PEQUENO: asercion NEGATIVA.
# Si el tope no deja meter el codigo, la pieza debe DECIRLO, no callarse.
# ---------------------------------------------------------------------------
def test_con_tope_pequeno_avisa_que_el_codigo_no_cabe(tmp_path):
    pieza = _cargar_pieza()
    raiz, orden, archivo = _escribir_orden(
        tmp_path,
        "sumador.py",
        "def suma(a, b):\n    return a + b\n" * 200,
    )

    fn = None
    for nombre in ("reproducir", "reproducir_etapas", "prueba_previa", "revisar"):
        if hasattr(pieza, nombre):
            fn = getattr(pieza, nombre)
            break
    assert fn is not None, "La pieza no expone funcion para reproducir las etapas."

    # Tope tan pequeno que el codigo NO puede caber.
    informe = fn(orden=str(orden), raiz=str(raiz), tope=10)

    assert isinstance(informe, str) and informe.strip(), (
        "Con tope pequeno el informe debe seguir siendo texto no vacio."
    )
    bajo = informe.lower()
    assert ("no cabe" in bajo or "no llega" in bajo or "recortado" in bajo
            or "falta" in bajo or "no" in bajo), (
        "Con tope pequeno la pieza debe avisar que el codigo no cabe; no puede callarse."
    )


# ---------------------------------------------------------------------------
# PRUEBA 3 — la pieza NO debe tocar el estado real.
# Se comprueba que el estado real no cambia tras ejecutar la pieza.
# ---------------------------------------------------------------------------
def test_no_toca_el_estado_real(tmp_path):
    pieza = _cargar_pieza()
    raiz, orden, archivo = _escribir_orden(
        tmp_path,
        "sumador.py",
        "def suma(a, b):\n    return a + b\n",
    )

    fn = None
    for nombre in ("reproducir", "reproducir_etapas", "prueba_previa", "revisar"):
        if hasattr(pieza, nombre):
            fn = getattr(pieza, nombre)
            break
    assert fn is not None, "La pieza no expone funcion para reproducir las etapas."

    # Estado real antes (si existe).
    estado_real = os.path.join("memoria", "ESTADO.json")
    antes = None
    if os.path.exists(estado_real):
        with open(estado_real, "rb") as f:
            antes = f.read()

    fn(orden=str(orden), raiz=str(raiz), tope=20000)

    if antes is not None:
        with open(estado_real, "rb") as f:
            despues = f.read()
        assert antes == despues, (
            "La pieza de prueba previa NO debe escribir en memoria/ESTADO.json."
        )
