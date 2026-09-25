"""VIGIA: el guardado no muere por la bateria completa de vigias.

NACE ROJA: la reparacion aun no esta.

Hoy vecinas._vecinas_por_stem devuelve None en cuanto un archivo de codigo
cambiado no aparece en ninguna vigia. Y None significa correr las 245 vigias
enteras con tope de 15 minutos, por lo que el guardado muere por tiempo y el
trabajo ya aprobado se deshace. Medido 82 veces en memoria/FALLOS.json id 69.
"""

import os
import sys
import tempfile


AQUI = os.path.dirname(os.path.abspath(__file__))
ARNES = os.path.join(os.path.dirname(AQUI), "arnes")
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import vecinas  # noqa: E402


def test_un_archivo_sin_vigia_no_manda_correr_las_245():
    with tempfile.TemporaryDirectory() as raiz:
        carpeta_vigias = os.path.join(raiz, "vigias")
        os.makedirs(carpeta_vigias)
        vigia = "test_vigia_de_prueba.py"
        with open(os.path.join(carpeta_vigias, vigia), "w", encoding="utf-8") as f:
            f.write("# vigila pieza_conocida\n")

        cambiados = ["pieza_conocida.py", "pieza_sin_vigia.py"]
        vigias = [vigia]

        resultado = vecinas._vecinas_por_stem(cambiados, raiz, vigias)

        assert resultado is not None, (
            "_vecinas_por_stem devolvio None: eso manda correr las 245 vigias "
            "enteras con tope de 15 minutos y el guardado muere por tiempo"
        )
        assert isinstance(resultado, list), (
            "_vecinas_por_stem debe devolver una lista, no %r" % (type(resultado),)
        )
        assert vigia in resultado, (
            "la vigia de pieza_conocida debe venir en el resultado: %r" % (resultado,)
        )
