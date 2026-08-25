# -*- coding: utf-8 -*-
"""VIGIA — el mando no se muere por un caracter que la consola no sepa mostrar.

FALLO REAL (2026-08-25, reproducido). Se lanzo al equipo sobre Foto Informe. El equipo CONTESTO.
Y el mando murio al IMPRIMIR la respuesta:

    UnicodeEncodeError: 'charmap' codec can't encode character '\\u202f' in position 1178

La consola de Windows usa cp1252 y la respuesta traia un espacio fino (u202f), que ahi no existe.

DOS DANOS, y el segundo es el caro:
  1. Un traceback de Python en la cara de Julio. Ya esta apuntado como fallo desde antes.
  2. SE PERDIO EL TRABAJO. La llave del equipo se guarda DESPUES de imprimir, asi que al morir
     en el print no se guardo nada y hubo que pagar la llamada otra vez. Un caracter invisible
     costo el trabajo entero.

LA REGLA: mostrar es lo ULTIMO que puede tumbar un trabajo ya hecho. Si un caracter no se puede
dibujar, se dibuja como se pueda, pero no se tira lo que costo.

ESTA VIGIA NACE ROJA.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# El caracter exacto que lo mato, mas otros que tampoco caben en cp1252.
RAROS = "espacio fino:  flecha:→ comilla:“ emoji:✅"


def test_escribir_en_cp1252_no_mata_al_mando():
    """Se fuerza la consola a cp1252 (la de Julio) y se le pide escribir esos caracteres.

    Se corre en un proceso APARTE a proposito: es la unica forma de reproducir la consola de
    verdad. Y se llama al mando, no a un print suelto, porque lo que hay que probar es que el
    MANDO aguanta.
    """
    entorno = dict(os.environ)
    entorno["PYTHONIOENCODING"] = "cp1252"
    entorno["INGENIERO_TEXTO_RARO_TEST"] = RAROS

    r = subprocess.run(
        [sys.executable, "-c",
         "import sys, os; sys.path.insert(0, r'%s'); import ingeniero; "
         "print(os.environ['INGENIERO_TEXTO_RARO_TEST'])" % AQUI],
        capture_output=True, text=True, env=entorno, cwd=AQUI)

    assert "UnicodeEncodeError" not in (r.stderr or ""), (
        "el mando SE MUERE al escribir un caracter que la consola no sabe mostrar. Eso tira un "
        "traceback a la cara de Julio y, peor, pierde el trabajo ya hecho: la llave del equipo "
        "se guarda DESPUES de imprimir. Un caracter invisible cuesta la llamada entera.\n"
        "  salida de error: %s" % (r.stderr or "")[-400:])
    assert r.returncode == 0, (
        "el mando termino con error al escribir caracteres raros: %s" % (r.stderr or "")[-300:])
