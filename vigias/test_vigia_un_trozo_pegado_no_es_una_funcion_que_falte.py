"""VIGIA: un trozo pegado no es una funcion que falte.

Medido el 2026-09-27 con dos llamadas reales y sin gastar ninguna IA:

    cuerpo/obrero.py::falta_en_el_material recibe el material y el encargo y devuelve
    una lista de frases con lo que el encargo nombra y el material no trae. Toma como
    nombre de funcion exigida cualquier palabra del encargo que empiece por raya baja,
    tal cual, sin cortarla donde deja de ser un nombre. Si el encargo trae un trozo
    pegado (por ejemplo ``_anotar(segundos``), la palabra queda pegada al parentesis y
    el filtro busca la declaracion de una funcion llamada ``_anotar`` seguida de
    parentesis y de la palabra ``segundos``, que no puede existir en ningun archivo, y
    devuelve que falta aunque el material traiga la funcion ``_anotar`` de verdad y con
    su codigo. Esto se ve sobre todo cuando la firma de la funcion esta escrita en
    varios renglones.

Esta prueba NACE ROJA a proposito: va antes de la reparacion. En esta ronda NO se toca
cuerpo/obrero.py. La prueba no llama a ninguna IA, no lanza procesos y no escribe nada:
solo llama a la funcion con textos escritos dentro de la propia prueba.

Casos que exige, tres y nada mas:

1. Material con la declaracion de ``_anotar`` repartida en varios renglones y encargo
   que nombra la funcion con su nombre limpio -> lista vacia.
2. Ese mismo material y encargo que trae el nombre pegado a un parentesis y a la
   primera palabra de dentro -> lista vacia, porque la funcion si esta.
3. Ese mismo material y encargo que nombra una funcion con raya baja que de verdad no
   esta -> la lista NO sale vacia y avisa: el aviso de verdad no se afloja.
"""

import os
import sys

# La prueba vive en vigias/ y la funcion vive en cuerpo/obrero.py. Se anade la raiz del
# proyecto al camino de importacion para poder llamarla sin depender de como se lance.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from cuerpo.obrero import falta_en_el_material


# ---------------------------------------------------------------------------
# MATERIAL DE LA PRUEBA
# ---------------------------------------------------------------------------
# La funcion _anotar existe de verdad en el material, pero su firma esta escrita en
# varios renglones: el nombre queda en un renglon y el parentesis con los parametros
# en el siguiente. Ese es justo el caso que dispara el fallo.
MATERIAL_CON_ANOTAR = '''
import time


def _anotar(
    segundos,
    texto,
):
    """Apunta lo que pasa con su hora."""
    with open("bitacora.txt", "a") as f:
        f.write(str(segundos) + " " + str(texto) + "\\n")


def otra_cosa():
    return 1
'''

# Encargo 1: nombra la funcion con su nombre limpio.
ENCARGO_NOMBRE_LIMPIO = "revisa que _anotar este en el material"

# Encargo 2: trae el nombre pegado a un parentesis y a la primera palabra de dentro.
# El nombre de la funcion sigue siendo _anotar, que SI esta en el material.
ENCARGO_TROZO_PEGADO = "revisa que _anotar(segundos, texto) este en el material"

# Encargo 3: nombra una funcion con raya baja que de verdad NO esta en el material.
ENCARGO_FUNCION_QUE_NO_ESTA = "revisa que _no_existe_en_ninguna_parte este en el material"


# ---------------------------------------------------------------------------
# CASO 1: nombre limpio, la funcion esta -> lista vacia
# ---------------------------------------------------------------------------
def test_nombre_limpio_de_funcion_que_si_esta_no_falta():
    faltantes = falta_en_el_material(MATERIAL_CON_ANOTAR, ENCARGO_NOMBRE_LIMPIO)
    assert faltantes == [], (
        "el material trae la funcion _anotar con su codigo y el encargo la nombra "
        "limpia: no puede faltar nada, y salio: " + repr(faltantes)
    )


# ---------------------------------------------------------------------------
# CASO 2: nombre pegado a parentesis y a la primera palabra de dentro -> lista vacia
# ---------------------------------------------------------------------------
def test_trozo_pegado_de_funcion_que_si_esta_no_falta():
    faltantes = falta_en_el_material(MATERIAL_CON_ANOTAR, ENCARGO_TROZO_PEGADO)
    assert faltantes == [], (
        "el encargo trae '_anotar(segundos' pegado, pero la funcion _anotar SI esta "
        "en el material: no puede faltar nada, y salio: " + repr(faltantes)
    )


# ---------------------------------------------------------------------------
# CASO 3: funcion con raya baja que de verdad no esta -> la lista NO sale vacia
# ---------------------------------------------------------------------------
def test_funcion_que_de_verdad_no_esta_si_falta():
    faltantes = falta_en_el_material(MATERIAL_CON_ANOTAR, ENCARGO_FUNCION_QUE_NO_ESTA)
    assert faltantes, (
        "el encargo nombra _no_existe_en_ninguna_parte y esa funcion no esta en el "
        "material: la lista no puede salir vacia"
    )
    assert any("_no_existe_en_ninguna_parte" in frase for frase in faltantes), (
        "el aviso tiene que nombrar la funcion que falta, y salio: " + repr(faltantes)
    )


if __name__ == "__main__":
    test_nombre_limpio_de_funcion_que_si_esta_no_falta()
    test_trozo_pegado_de_funcion_que_si_esta_no_falta()
    test_funcion_que_de_verdad_no_esta_si_falta()
    print("vigia: los tres casos pasaron")
