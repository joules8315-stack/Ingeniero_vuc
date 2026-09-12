import os
import sys

# Añadir rutas al sys.path para poder importar los módulos del proyecto
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import asignador
from cuerpo import obrero


def _sobre(objetivo: str, material: str):
    """Construye el encargo y el sobre final.

    1. Llama a ``asignador.armar_encargo`` con un diccionario que contiene el
       objetivo y la prueba "resolver", pasando también el material.
    2. Con el texto devuelto (el encargo) llama a ``obrero._prompt_obrero``
       indicando que la tarea es "reparar".
    3. Devuelve una tupla ``(encargo, sobre)``.
    """
    encargo = asignador.armar_encargo({"objetivo": objetivo, "prueba": "resolver"}, material=material)
    sobre = obrero._prompt_obrero(encargo, objetivo, "reparar")
    return encargo, sobre


def test_el_objetivo_viaja_UNA_sola_vez():
    """Comprueba que el objetivo (marcado) aparece solo una vez en el sobre.
    Con el código actual el objetivo se duplica, por lo que este test debe fallar.
    """
    marca = "ZMARCADELOBJETIVOZ"
    objetivo = f"Este es el objetivo con la marca {marca} dentro."
    material = "material corto"
    _, sobre = _sobre(objetivo, material)
    assert sobre.count(marca) == 1, "El objetivo aparece más de una vez en el sobre."


def test_quitar_la_copia_devuelve_groq_al_trabajo():
    """Comprueba que el sobre resultante cabe dentro del límite de 19042 caracteres.
    Con el código actual el sobre supera ese límite, por lo que este test debe fallar.
    """
    # objetivo de 7575 letras
    objetivo = "a" * 7575
    # material de 34460 letras
    material = "b" * 34460
    _, sobre = _sobre(objetivo, material)
    assert len(sobre) <= 19042, "El sobre sigue siendo demasiado grande."


def test_el_objetivo_SIGUE_ESTANDO_no_vale_con_borrarlo():
    """Asegura que la marca del objetivo sigue presente en el sobre.
    Este test debe pasar porque la marca no debe eliminarse.
    """
    marca = "ZMARCADELOBJETIVOZ"
    objetivo = f"Objetivo con marca {marca} para la prueba."
    material = "material cualquiera"
    _, sobre = _sobre(objetivo, material)
    assert marca in sobre, "La marca del objetivo desapareció del sobre."
