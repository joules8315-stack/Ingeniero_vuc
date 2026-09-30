import os
import sys

# La carpeta vigias esta un nivel por debajo de la raiz del proyecto.
# Se mete la raiz en la ruta de busqueda para poder importar cuerpo.obrero.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from cuerpo import obrero


# ---------------------------------------------------------------------------
# Textos de mentira, armados juntando renglones de una lista.
# No se usa texto de triple comilla que lleve dentro otras comillas.
# ---------------------------------------------------------------------------

def _texto_con_etiquetas_pegadas():
    """Encargo cuyo unico codigo pegado inserta un diccionario con etiquetas.

    Las etiquetas son pieza, abs y rol, entre comillas dobles. Ninguna de
    ellas es una funcion que el encargo vaya a tocar: son etiquetas.
    """
    renglones = [
        "OBJETIVO: dejar listo el recorte del material.",
        "El encargo pega este trozo literal de codigo:",
        '    datos = {"pieza": valor, "abs": otro, "rol": tercero}',
        "y con eso basta.",
    ]
    return "\n".join(renglones)


def _texto_que_nombra_la_funcion_armar():
    """Encargo en palabras corrientes, sin comillas ni diccionarios."""
    renglones = [
        "OBJETIVO: hay que arreglar la funcion armar.",
        "La funcion armar es la que deja el paquete listo.",
        "No se toca nada mas.",
    ]
    return "\n".join(renglones)


def _texto_que_nombra_una_raya_baja():
    """Encargo que nombra una palabra que empieza por raya baja."""
    renglones = [
        "OBJETIVO: revisar el recorte del material.",
        "Hay que mirar _recortar_material antes de seguir.",
    ]
    return "\n".join(renglones)


def _texto_normal():
    """Encargo normal, sin nombres de funcion conocidos."""
    renglones = [
        "OBJETIVO: dejar el paquete listo para la ronda.",
        "No hay nada mas que hacer.",
    ]
    return "\n".join(renglones)


# ---------------------------------------------------------------------------
# Caso 1: EL CASO MEDIDO. Nace ROJO a proposito.
# ---------------------------------------------------------------------------

def test_la_etiqueta_pegada_no_es_una_funcion():
    """Una etiqueta entre comillas no puede contarse como funcion nombrada.

    Hoy la funcion cuenta toda palabra que aparezca en la coleccion de
    conocidos, sin mirar COMO se usa. Por eso pieza y rol, que son etiquetas
    de un diccionario pegado como material, se toman por funciones y la ronda
    se frena antes de empezar pidiendo material que no hace falta.
    """
    texto = _texto_con_etiquetas_pegadas()
    conocidas = {"rol", "pieza", "armar"}
    devueltas = obrero._nombres_de_funcion_del_texto(texto, conocidas=conocidas)
    assert "rol" not in devueltas, (
        "Hoy una etiqueta pegada como material se toma por una funcion y frena "
        "la ronda antes de empezar: 'rol' es una etiqueta de un diccionario, "
        "no una funcion que el encargo vaya a tocar. Eso tumbo dos rondas ya "
        "aprobadas hoy."
    )
    assert "pieza" not in devueltas, (
        "Hoy una etiqueta pegada como material se toma por una funcion y frena "
        "la ronda antes de empezar: 'pieza' es una etiqueta de un diccionario, "
        "no una funcion que el encargo vaya a tocar. Eso tumbo dos rondas ya "
        "aprobadas hoy."
    )


# ---------------------------------------------------------------------------
# Caso 2: lo que hoy funciona y no puede cambiar.
# ---------------------------------------------------------------------------

def test_la_funcion_nombrada_en_palabras_corrientes_si_se_cuenta():
    """Un nombre de funcion dicho en palabras corrientes si se cuenta."""
    texto = _texto_que_nombra_la_funcion_armar()
    conocidas = {"rol", "pieza", "armar"}
    devueltas = obrero._nombres_de_funcion_del_texto(texto, conocidas=conocidas)
    assert "armar" in devueltas, (
        "El texto pide arreglar la funcion armar en palabras corrientes y sin "
        "comillas: la lista devuelta tiene que traer 'armar'."
    )


# ---------------------------------------------------------------------------
# Caso 3: lo que hoy funciona y no puede cambiar.
# ---------------------------------------------------------------------------

def test_la_palabra_con_raya_baja_si_se_cuenta_sin_conocidas():
    """Una palabra que empieza por raya baja se cuenta aunque no haya conocidas."""
    texto = _texto_que_nombra_una_raya_baja()
    devueltas = obrero._nombres_de_funcion_del_texto(texto)
    assert "_recortar_material" in devueltas, (
        "El texto nombra _recortar_material y no se le pasa coleccion de "
        "conocidos: la lista devuelta tiene que traerla."
    )


# ---------------------------------------------------------------------------
# Caso 4: no revienta.
# ---------------------------------------------------------------------------

def test_texto_vacio_y_conocidas_en_nada_no_revientan():
    """Texto vacio y conocidas en None devuelven lista sin lanzar error."""
    vacio = obrero._nombres_de_funcion_del_texto("")
    assert isinstance(vacio, list), "Con texto vacio tiene que devolver una lista."
    assert vacio == [], "Con texto vacio la lista tiene que venir sin nombres."

    normal = obrero._nombres_de_funcion_del_texto(_texto_normal(), conocidas=None)
    assert isinstance(normal, list), "Con conocidas en None tiene que devolver una lista."
    assert "rol" not in normal, "Sin conocidas no puede aparecer 'rol'."
    assert "pieza" not in normal, "Sin conocidas no puede aparecer 'pieza'."
    assert "armar" not in normal, "Sin conocidas no puede aparecer 'armar'."
