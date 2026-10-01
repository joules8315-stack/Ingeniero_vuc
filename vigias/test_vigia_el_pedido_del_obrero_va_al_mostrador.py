import os
import pathlib
import pytest

# Importamos el módulo donde se debe definir la función a probar.
# Se asume que el paquete raíz del proyecto está en el PYTHONPATH y que
# "cuerpo" es un paquete importable.
from cuerpo import obrero


def test_funcion_existe():
    """Caso 1: la función debe estar definida en cuerpo.obrero"""
    assert hasattr(obrero, "pedido_del_obrero_al_mostrador"), "La función pedido_del_obrero_al_mostrador no está definida"


def test_pedido_devuelve_pieza_existente(tmp_path):
    """Caso 2: si la propuesta pide una pieza que sí existe, el contenido de la pieza se agrega al material"""
    # Creamos un archivo temporal con contenido conocido.
    contenido_pieza = "ESTA_ES_LA_PIEZA_DE_PRUEBA"
    archivo = tmp_path / "pieza.txt"
    archivo.write_text(contenido_pieza, encoding="utf-8")

    propuesta = {
        "PREGUNTA_REQUERIDA": {
            "ruta": str(archivo),
            # El nombre de la pieza no se usa en la implementación actual, pero se incluye por claridad.
            "pieza": "pieza.txt",
        }
    }
    material_inicial = "MATERIAL_INICIAL"
    resultado = obrero.pedido_del_obrero_al_mostrador(propuesta, material_inicial, str(tmp_path))
    # El material resultante debe contener el contenido de la pieza y ser más largo que el original.
    assert contenido_pieza in resultado
    assert len(resultado) > len(material_inicial)


def test_pedido_sin_pregunta_requerida_no_modifica_material():
    """Caso 3: si la propuesta no contiene PREGUNTA_REQUERIDA, el material se devuelve sin cambios"""
    propuesta = {"alguna_otra_clave": "valor"}
    material = "MATERIAL_INVARIANTE"
    resultado = obrero.pedido_del_obrero_al_mostrador(propuesta, material, "")
    assert resultado == material


def test_pedido_pieza_inexistente_no_modifica_material(tmp_path):
    """Caso 4: si la ruta solicitada no existe, la función no debe alterar el material"""
    ruta_inexistente = tmp_path / "no_existe.txt"
    propuesta = {
        "PREGUNTA_REQUERIDA": {
            "ruta": str(ruta_inexistente),
            "pieza": "no_existe.txt",
        }
    }
    material = "MATERIAL_ORIGINAL"
    resultado = obrero.pedido_del_obrero_al_mostrador(propuesta, material, str(tmp_path))
    assert resultado == material


def test_no_duplica_pieza_al_pedir_dos_veces(tmp_path):
    """Caso 5: la misma pieza solicitada dos veces no debe duplicarse en el material"""
    contenido = "PIEZA_UNICA"
    archivo = tmp_path / "unica.txt"
    archivo.write_text(contenido, encoding="utf-8")
    propuesta = {
        "PREGUNTA_REQUERIDA": {
            "ruta": str(archivo),
            "pieza": "unica.txt",
        }
    }
    material = "BASE"
    # Primera aplicación
    resultado1 = obrero.pedido_del_obrero_al_mostrador(propuesta, material, str(tmp_path))
    # Segunda aplicación sobre el resultado anterior
    resultado2 = obrero.pedido_del_obrero_al_mostrador(propuesta, resultado1, str(tmp_path))
    # La pieza debe aparecer solo una vez.
    assert resultado1.count(contenido) == 1
    assert resultado2 == resultado1
