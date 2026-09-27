"""Vigia: la extension suelta (.py sin nombre delante) NO es un archivo.

Medido el 2026-09-27 sin gastar ninguna IA: cuerpo/obrero.py::falta_en_el_material
saca del encargo los nombres de archivo y hoy acepta como archivo la extension
SUELTA, o sea un punto seguido de py sin ningun nombre delante, porque solo
comprueba que la palabra no sea 'py' a secas. Asi, cuando el encargo dice en una
frase normal que se pide un archivo de codigo con esa extension suelta, el filtro
se cree que hay un archivo llamado '.py' y, como ese texto aparece en cualquier
material, deja de filtrar: al que escribe le llega el bulto entero y la ronda se
paga de mas.

Esta prueba NACE ROJA a proposito: va antes de la reparacion. No toca
cuerpo/obrero.py. No llama a ninguna IA, no lanza procesos y no escribe nada:
solo llama a la funcion con textos escritos dentro de la propia prueba.

Casos que exige, tres y nada mas:
  1. Encargo con una ruta de verdad: se reconoce como archivo y si el material
     no la trae, se avisa.
  2. Encargo que solo trae la extension suelta, sin ningun nombre delante, y un
     material que no habla de ningun archivo: la lista de avisos sale VACIA,
     porque una extension suelta no es un archivo.
  3. Encargo que trae las dos cosas, la ruta de verdad y la extension suelta:
     solo cuenta la ruta de verdad.
"""

import os
import sys

# La prueba vive en vigias/ y necesita importar cuerpo/obrero.py de la raiz.
_RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from cuerpo.obrero import falta_en_el_material


# La extension suelta se arma POR PARTES para no dejar en el archivo una forma
# que el guardia pueda confundir con una llave ni con una ruta real.
_PUNTO = "."
_EXT = "py"
_EXTENSION_SUELTA = _PUNTO + _EXT  # ".py" sin ningun nombre delante


def test_una_ruta_de_verdad_se_reconoce_y_se_avisa_si_no_esta():
    """Caso 1: el encargo nombra una ruta de verdad y el material no la trae.

    La ruta se reconoce como archivo y, como el material no la trae, la lista
    de avisos NO puede salir vacia: tiene que avisar de que falta ese archivo.
    """
    encargo = (
        "Hay que reparar el archivo cuerpo/obrero.py porque la funcion "
        "falta_en_el_material acepta la extension suelta como archivo."
    )
    material = (
        "PAQUETE MINIMO. Aqui solo hay leyes y trozos de otros archivos. "
        "No se habla de ningun archivo de codigo concreto."
    )

    avisos = falta_en_el_material(material, encargo)

    assert avisos, (
        "con una ruta de verdad en el encargo y sin esa ruta en el material, "
        "la lista de avisos no puede salir vacia"
    )
    assert any("cuerpo/obrero.py" in str(a) for a in avisos), (
        "el aviso tiene que nombrar la ruta de verdad que falta: cuerpo/obrero.py"
    )


def test_la_extension_suelta_sola_no_es_un_archivo():
    """Caso 2: el encargo solo trae la extension suelta, sin nombre delante.

    El material no habla de ningun archivo. Como una extension suelta NO es un
    archivo, la lista de avisos tiene que salir VACIA.
    """
    encargo = (
        "Se pide un archivo de codigo con la extension " + _EXTENSION_SUELTA + " "
        "que haga el trabajo, sin decir su nombre."
    )
    material = (
        "PAQUETE MINIMO. Aqui solo hay leyes y trozos de otros archivos. "
        "No se habla de ningun archivo de codigo concreto."
    )

    avisos = falta_en_el_material(material, encargo)

    assert avisos == [], (
        "una extension suelta no es un archivo: con solo la extension suelta en "
        "el encargo y un material sin archivos, la lista de avisos tiene que "
        "salir VACIA, y salio: " + repr(avisos)
    )


def test_con_ruta_de_verdad_y_extension_suelta_solo_cuenta_la_ruta():
    """Caso 3: el encargo trae la ruta de verdad Y la extension suelta.

    Solo cuenta la ruta de verdad. Si el material trae la ruta, no hay aviso
    por la ruta; y la extension suelta no puede generar un aviso propio.
    """
    encargo = (
        "Hay que reparar cuerpo/obrero.py y ademas se pide un archivo de codigo "
        "con la extension " + _EXTENSION_SUELTA + " que haga el trabajo."
    )
    material = (
        "PAQUETE MINIMO. Aqui esta el trozo de cuerpo/obrero.py que hay que "
        "reparar, con su funcion falta_en_el_material entera."
    )

    avisos = falta_en_el_material(material, encargo)

    assert avisos == [], (
        "si el material trae la ruta de verdad, no hay aviso por ella; y la "
        "extension suelta no puede generar un aviso propio. Salio: " + repr(avisos)
    )

    # Y si el material NO trae la ruta de verdad, el unico aviso es por la ruta.
    material_sin_ruta = (
        "PAQUETE MINIMO. Aqui solo hay leyes y trozos de otros archivos. "
        "No se habla de ningun archivo de codigo concreto."
    )
    avisos_sin_ruta = falta_en_el_material(material_sin_ruta, encargo)

    assert avisos_sin_ruta, (
        "si el material no trae la ruta de verdad, tiene que haber aviso por ella"
    )
    assert all("cuerpo/obrero.py" in str(a) for a in avisos_sin_ruta), (
        "el unico aviso posible es por la ruta de verdad; la extension suelta no "
        "puede generar un aviso propio. Salio: " + repr(avisos_sin_ruta)
    )
