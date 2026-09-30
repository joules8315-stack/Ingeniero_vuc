import os
import sys

# La carpeta que esta un nivel arriba de vigias es la raiz del proyecto.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import obrero


# Las tres palabras conocidas del proyecto que se usan en todos los casos.
CONOCIDAS = {"mensajero", "armar", "guardar"}


def _texto(renglones):
    """Arma un texto de mentira juntando renglones de una lista.

    No se usa texto de triple comilla que lleve dentro otras comillas.
    """
    return "\n".join(renglones)


def test_caso_1_dato_pegado_tras_coma_no_es_funcion():
    """Caso medido, NACE ROJO.

    El encargo pega un renglon de codigo donde 'mensajero' es un dato que se
    le pasa a otra funcion, no una funcion que se vaya a tocar. La lista
    devuelta NO puede traer 'mensajero'.
    """
    texto = _texto([
        "Hay que cambiar este renglon del archivo cuerpo/obrero.py:",
        "    return hacer_la_tarea(proyecto, orden, tope, mensajero, False)",
        "Ese renglon es el que hay que reparar.",
    ])
    devueltas = obrero._nombres_de_funcion_del_texto(texto, CONOCIDAS)
    assert "mensajero" not in devueltas, (
        "Un dato dentro de un trozo de codigo pegado se esta tomando por una funcion: "
        "el texto se parte por las comas y eso convierte el dato en una palabra suelta. "
        "Esto freno tres encargos distintos la noche del 2026-09-29."
    )


def test_caso_2_dato_en_firma_pegada_no_es_funcion():
    """Tambien ROJO, la misma causa en una firma pegada.

    El encargo pega una firma donde 'mensajero' es un dato de la firma, no una
    funcion a tocar. La lista devuelta NO puede traer 'mensajero'.
    """
    texto = _texto([
        "La firma que hay que cambiar es esta:",
        "    def hacer_la_tarea(proyecto, orden, tope, mensajero=print):",
        "Hay que dejarla como estaba antes.",
    ])
    devueltas = obrero._nombres_de_funcion_del_texto(texto, CONOCIDAS)
    assert "mensajero" not in devueltas, (
        "Un dato de la firma pegada se esta tomando por una funcion: "
        "el texto se parte por las comas y eso convierte el dato en una palabra suelta. "
        "Esto freno tres encargos distintos la noche del 2026-09-29."
    )


def test_caso_3_funcion_nombrada_en_palabras_corrientes_si_cuenta():
    """Lo que hoy funciona y no puede cambiar.

    El texto dice, en palabras corrientes, que hay que arreglar la funcion
    armar. La lista devuelta TIENE que traer 'armar'.
    """
    texto = _texto([
        "Hay que arreglar la funcion armar, que se queda a medias.",
        "Revisa tambien lo que hace por dentro.",
    ])
    devueltas = obrero._nombres_de_funcion_del_texto(texto, CONOCIDAS)
    assert "armar" in devueltas, (
        "La palabra 'armar' viene justo detras de la palabra funcion y tiene que contar como funcion."
    )


def test_caso_4_funcion_declarada_con_def_si_cuenta():
    """Lo que hoy funciona y no puede cambiar.

    El texto pega un renglon que declara una funcion conocida con 'def'.
    La lista devuelta TIENE que traer 'guardar'.
    """
    texto = _texto([
        "Este es el renglon que declara la funcion:",
        "    def guardar(cosa):",
        "Hay que cambiar lo que hace por dentro.",
    ])
    devueltas = obrero._nombres_de_funcion_del_texto(texto, CONOCIDAS)
    assert "guardar" in devueltas, (
        "La palabra 'guardar' viene justo detras de 'def' y tiene que contar como funcion."
    )


def test_caso_5_palabra_con_raya_baja_sin_conocidas_si_cuenta():
    """Lo que hoy funciona y no puede cambiar.

    El texto nombra una palabra que empieza por raya baja, sin pasarle ninguna
    coleccion de conocidos. La lista devuelta TIENE que traerla.
    """
    texto = _texto([
        "Hay que revisar _prompt_obrero, que se queda corto.",
        "Y tambien _nombres_de_funcion_del_texto.",
    ])
    devueltas = obrero._nombres_de_funcion_del_texto(texto)
    assert "_prompt_obrero" in devueltas, (
        "Una palabra que empieza por raya baja tiene que contar como funcion aunque no se pase coleccion de conocidas."
    )
