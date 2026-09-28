import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo import obrero


# ---------------------------------------------------------------------------
# Material de prueba armado AQUI, juntando renglones de una lista.
# NO se usa texto de triple comilla que lleve dentro mas triples comillas:
# eso cerraria el texto y el archivo no compilaria.
# Los renglones de relleno son comentarios normales, sin ninguna comilla triple.
# ---------------------------------------------------------------------------

# La funcion pedida por el encargo. Su declaracion tiene que sobrevivir al recorte.
DECLARACION_PEDIDA = "def _funcion_que_el_encargo_pide(paquete, tarea):"

# Relleno largo: renglones de comentario normales, sin comillas triples.
RELLENO = [
    "# relleno 01: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 02: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 03: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 04: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 05: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 06: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 07: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 08: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 09: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 10: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 11: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 12: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 13: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 14: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 15: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 16: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 17: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 18: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 19: linea de comentario para engordar el trozo y forzar el recorte",
    "# relleno 20: linea de comentario para engordar el trozo y forzar el recorte",
]


def _material_de_prueba():
    """Arma el paquete de prueba juntando renglones de una lista.

    Estructura: cabecera, LA LEY QUE MANDA, LOS TROZOS (varios del MISMO archivo,
    con el trozo que trae la declaracion pedida AL FINAL) y A QUIEN PUEDE DANAR.
    """
    lineas = []
    lineas.append("# PAQUETE DE PRUEBA")
    lineas.append("")
    lineas.append("## 1. LA LEY QUE MANDA AQUI")
    lineas.append("- CONTRATO_DE_PRUEBA: la ley que manda en este paquete de prueba.")
    lineas.append("")
    lineas.append("## 3. LOS TROZOS EXACTOS")
    # Primer trozo del archivo pedido: NO trae la declaracion pedida.
    lineas.append("### `cuerpo/obrero.py:1-40`  (relevancia 99.0)")
    lineas.append("def _otra_funcion_cualquiera(paquete):")
    lineas.append("    return paquete")
    lineas.extend(RELLENO)
    # Segundo trozo del MISMO archivo: tampoco trae la declaracion pedida.
    lineas.append("### `cuerpo/obrero.py:41-80`  (relevancia 98.0)")
    lineas.append("def _funcion_de_relleno(paquete):")
    lineas.append("    return paquete")
    lineas.extend(RELLENO)
    # Tercer trozo del MISMO archivo: AQUI va la declaracion pedida, AL FINAL.
    lineas.append("### `cuerpo/obrero.py:81-120`  (relevancia 97.0)")
    lineas.append(DECLARACION_PEDIDA)
    lineas.append("    return paquete")
    lineas.extend(RELLENO)
    lineas.append("")
    lineas.append("## 5. A QUIEN PUEDE DANAR TOCAR ESTO")
    lineas.append("- cuerpo/obrero.py — lo importa desde arnes/asignador.py")
    lineas.append("- cuerpo/obrero.py — lo importa desde arnes/revisor_de_programa.py")
    lineas.append("")
    return "\n".join(lineas)


def _tope_medido(material):
    """Tope que obliga a recortar de verdad, medido sobre el propio material.

    Se queda con la mitad del material: es MENOR que el material entero (recorta)
    y MAYOR que lo que la funcion esta obligada a conservar (ley + a quien puede
    danar + el trozo con la declaracion pedida), asi que la vigia puede ponerse
    verde sin romper el tope ni la ley.
    """
    return max(900, len(material) // 2)


def test_el_recorte_no_se_come_la_funcion_pedida():
    """Caso 1: con varios trozos del mismo archivo y el trozo con la declaracion
    pedida AL FINAL, y un tope que obliga a recortar, el texto que sale sigue
    trayendo la declaracion de esa funcion."""
    material = _material_de_prueba()
    tope = _tope_medido(material)
    salida = obrero._filtrar_paquete(
        material, archivo="cuerpo/obrero.py", tope=tope, funciones=["_funcion_que_el_encargo_pide"]
    )
    assert DECLARACION_PEDIDA in salida, (
        "el recorte se comio el trozo con la declaracion pedida: "
        "el que escribe recibe el archivo nombrado pero sin la funcion"
    )


def test_el_recorte_conserva_la_ley_y_a_quien_puede_danar():
    """Caso 2: en ese mismo caso, el texto que sale sigue trayendo la ley que
    manda y la seccion de a quien puede danar."""
    material = _material_de_prueba()
    tope = _tope_medido(material)
    salida = obrero._filtrar_paquete(
        material, archivo="cuerpo/obrero.py", tope=tope, funciones=["_funcion_que_el_encargo_pide"]
    )
    assert "LA LEY QUE MANDA" in salida, "el recorte se comio la ley que manda"
    assert "A QUIEN PUEDE DANAR" in salida, "el recorte se comio la seccion de a quien puede danar"


def test_sin_funcion_pedida_se_comporta_como_hoy():
    """Caso 3: sin pasarle ninguna funcion, se comporta como hoy y no revienta."""
    material = _material_de_prueba()
    tope = _tope_medido(material)
    salida = obrero._filtrar_paquete(material, archivo="cuerpo/obrero.py", tope=tope)
    assert isinstance(salida, str)
    assert salida.strip() != ""
    assert "LA LEY QUE MANDA" in salida
    assert "A QUIEN PUEDE DANAR" in salida
