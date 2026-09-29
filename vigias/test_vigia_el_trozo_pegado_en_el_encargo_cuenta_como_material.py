import os
import sys

# Arranque: meter en sys.path la carpeta que esta un nivel arriba de la carpeta vigias,
# para poder importar la pieza cuerpo/obrero.py desde la prueba.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_ARRIBA = os.path.dirname(_AQUI)
if _ARRIBA not in sys.path:
    sys.path.insert(0, _ARRIBA)


MATERIAL_INUTIL = "LEYES DEL PROYECTO: no se asume, no se inventa."

# Encargo del CASO 1: nombra el archivo y la funcion y ADEMAS pega el trozo dentro.
ENCARGO_CON_TROZO = (
    "Hay que arreglar cuerpo/saludos.py, funcion dar_saludo.\n"
    "El trozo que hay que cambiar va pegado aqui debajo:\n"
    "\n"
    "def dar_saludo(nombre):\n"
    "    return \"hola \" + nombre\n"
)

# Encargo del CASO 2: nombra el archivo y la funcion pero NO pega el trozo.
ENCARGO_SIN_TROZO = (
    "Hay que arreglar cuerpo/saludos.py, funcion dar_saludo.\n"
    "El trozo no viene pegado en este encargo.\n"
)


def _traer_falta_en_el_material():
    """Importa la pieza dentro de la prueba, sin tocar nada mas."""
    from cuerpo.obrero import falta_en_el_material
    return falta_en_el_material


def test_caso_1_trozo_pegado_en_el_encargo_cuenta_como_material():
    """CASO 1 (nace ROJO): el trozo pegado en el encargo NO debe contar como falta.

    Hoy la funcion mira SOLO el material, ve que no trae ni el archivo ni la funcion,
    y devuelve frases diciendo que falta. Debe devolver lista vacia porque el trozo
    esta pegado dentro del encargo.
    """
    falta_en_el_material = _traer_falta_en_el_material()

    resultado = falta_en_el_material(MATERIAL_INUTIL, ENCARGO_CON_TROZO)

    assert isinstance(resultado, list), (
        "la funcion debe devolver una lista, devolvio: %r" % (resultado,)
    )
    assert resultado == [], (
        "el trozo esta pegado en el encargo y por lo tanto NO falta material; "
        "la funcion devolvio: %r" % (resultado,)
    )


def test_caso_2_sin_trozo_pegado_sigue_avisando_que_falta():
    """CASO 2 (ya verde, debe seguir verde): sin trozo pegado, se sigue avisando.

    Sin este caso, el arreglo podria ser simplemente devolver siempre lista vacia,
    y eso seria peor que el fallo.
    """
    falta_en_el_material = _traer_falta_en_el_material()

    resultado = falta_en_el_material(MATERIAL_INUTIL, ENCARGO_SIN_TROZO)

    assert isinstance(resultado, list), (
        "la funcion debe devolver una lista, devolvio: %r" % (resultado,)
    )
    assert resultado != [], (
        "el encargo nombra cuerpo/saludos.py y dar_saludo y NO pega el trozo; "
        "la funcion debe avisar que falta material, pero devolvio lista vacia"
    )
