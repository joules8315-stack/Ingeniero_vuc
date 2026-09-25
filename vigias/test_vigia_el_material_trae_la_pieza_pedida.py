import pytest


# Fallo del 2026-09-25, expediente 173: se pregunto tres veces por una funcion
# sin mandarla nunca, y se pago cada intento. Este vigia nace rojo a proposito:
# la funcion falta_en_el_material todavia no existe en cuerpo/obrero.py.
# El import va DENTRO de cada prueba (la casa lo obliga) para que pytest
# pueda recoger el archivo aunque la funcion todavia no exista.


ENCARGO_CON_ARCHIVO_Y_FUNCION = (
    "Revisa el archivo cuerpo/obrero.py y dentro la funcion _prompt_obrero."
)

MATERIAL_COMPLETO = (
    "En cuerpo/obrero.py esta la pieza pedida.\n"
    "def _prompt_obrero(...):\n"
    "    ...\n"
)

MATERIAL_SOLO_NOMBRE_EN_LISTA = (
    "Piezas del proyecto:\n"
    "- cuerpo/obrero.py\n"
    "- cuerpo/ingeniero.py\n"
)

MATERIAL_SIN_ESE_ARCHIVO = (
    "Piezas del proyecto:\n"
    "- cuerpo/ingeniero.py\n"
    "- cuerpo/revisor.py\n"
)

ENCARGO_SIN_ARCHIVO = "Hay que mejorar un aviso para que se entienda mejor."

ENCARGO_PUNTO_PY_SUELTO = "Revisa el punto py y dime que ves."


def test_uno_material_trae_archivo_y_funcion_lista_vacia():
    from cuerpo.obrero import falta_en_el_material

    resultado = falta_en_el_material(MATERIAL_COMPLETO, ENCARGO_CON_ARCHIVO_Y_FUNCION)
    assert resultado == []


def test_dos_material_solo_nombra_archivo_en_lista_falta_la_funcion():
    from cuerpo.obrero import falta_en_el_material

    resultado = falta_en_el_material(
        MATERIAL_SOLO_NOMBRE_EN_LISTA, ENCARGO_CON_ARCHIVO_Y_FUNCION
    )
    assert len(resultado) == 1
    assert any("_prompt_obrero" in frase for frase in resultado)


def test_tres_material_no_menciona_el_archivo():
    from cuerpo.obrero import falta_en_el_material

    resultado = falta_en_el_material(
        MATERIAL_SIN_ESE_ARCHIVO, ENCARGO_CON_ARCHIVO_Y_FUNCION
    )
    assert len(resultado) >= 1
    assert any("cuerpo/obrero.py" in frase for frase in resultado)


def test_cuatro_encargo_sin_archivo_lista_vacia():
    from cuerpo.obrero import falta_en_el_material

    resultado = falta_en_el_material(MATERIAL_COMPLETO, ENCARGO_SIN_ARCHIVO)
    assert resultado == []


def test_cinco_encargo_dice_punto_py_suelto_lista_vacia():
    from cuerpo.obrero import falta_en_el_material

    resultado = falta_en_el_material(MATERIAL_COMPLETO, ENCARGO_PUNTO_PY_SUELTO)
    assert resultado == []
