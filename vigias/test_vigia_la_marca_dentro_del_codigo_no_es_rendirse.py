import os
import sys


# REGLA OBLIGATORIA DE ESCRITURA: la marca NUNCA se escribe entera y seguida.
# Se arma juntando trozos con el signo de sumar, igual que esta casa hace con las llaves de mentira.
MARCA = "NO" + "_" + "ENCONTRADO"


# Los cuatro nombres de campo que hoy recorre quien llama a _trae_no_encontrado.
CAMPOS = ("archivo", "codigo", "texto_viejo", "texto_nuevo")


# ---------------------------------------------------------------------------
# ARRANQUE: meter en la ruta de busqueda la carpeta que esta un nivel arriba de
# la carpeta vigias, para poder importar cuerpo/obrero.py. Se hace DENTRO de
# cada caso, nunca arriba del archivo.
# ---------------------------------------------------------------------------
def _raiz():
    """La carpeta que esta un nivel arriba de la carpeta vigias."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(aqui)


def _trae(propuesta, campos=CAMPOS):
    """Importa cuerpo/obrero.py DENTRO del caso y llama a _trae_no_encontrado."""
    raiz = _raiz()
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    from cuerpo import obrero
    return obrero._trae_no_encontrado(propuesta, campos)


# ---------------------------------------------------------------------------
# AYUDANTES: propuestas de mentira, armadas aqui mismo. Sin disco, sin red.
# ---------------------------------------------------------------------------
def _codigo_largo_sin_marca():
    """Un archivo de codigo de mentira de unos quince renglones, sin la marca."""
    return (
        "# Modulo de mentira para la prueba.\n"
        "# Explica lo que hace y no usa la marca por ningun lado.\n"
        "\n"
        "import os\n"
        "\n"
        "\n"
        "def sumar(a, b):\n"
        "    return a + b\n"
        "\n"
        "\n"
        "def restar(a, b):\n"
        "    return a - b\n"
        "\n"
        "\n"
        "def main():\n"
        "    print(sumar(1, 2))\n"
        "    print(restar(3, 1))\n"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )


def _codigo_largo_con_marca():
    """Un archivo de codigo de mentira de unos quince renglones que USA la marca como valor."""
    return (
        "# Modulo de mentira para la prueba.\n"
        "# Explica lo que hace y en medio devuelve la marca como valor legitimo.\n"
        "\n"
        "import os\n"
        "\n"
        "\n"
        "def sumar(a, b):\n"
        "    return a + b\n"
        "\n"
        "\n"
        "def buscar(nombre):\n"
        "    if not nombre:\n"
        "        return \"" + MARCA + "\"\n"
        "    return nombre\n"
        "\n"
        "\n"
        "def main():\n"
        "    print(sumar(1, 2))\n"
        "    print(buscar(''))\n"
        "\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )


def _propuesta(archivo="", codigo="", texto_viejo="", texto_nuevo=""):
    return {
        "archivo": archivo,
        "codigo": codigo,
        "texto_viejo": texto_viejo,
        "texto_nuevo": texto_nuevo,
    }


# ---------------------------------------------------------------------------
# CASO 1 — NACE ROJO: un archivo de codigo largo que usa la marca SI PASA.
# ---------------------------------------------------------------------------
def test_caso_1_codigo_largo_con_marca_si_pasa():
    propuesta = _propuesta(
        archivo="modulo/de/mentira.py",
        texto_nuevo=_codigo_largo_con_marca(),
    )
    resultado = _trae(propuesta)
    assert resultado is False, (
        "Por esto se perdio una ronda entera hoy: un archivo de codigo largo que usa la marca "
        "como valor legitimo fue rechazado como si el cerebro se hubiera rendido. "
        "La marca dentro de codigo es CONTENIDO, no rendicion."
    )


# ---------------------------------------------------------------------------
# CASO 2 — VERDE HOY: la marca sola sigue siendo rendirse.
# ---------------------------------------------------------------------------
def test_caso_2_marca_sola_sigue_siendo_rendirse():
    propuesta = _propuesta(texto_nuevo=MARCA)
    assert _trae(propuesta) is True


# ---------------------------------------------------------------------------
# CASO 3 — VERDE HOY: la marca con espacios alrededor tambien.
# ---------------------------------------------------------------------------
def test_caso_3_marca_con_espacios_alrededor_tambien():
    propuesta = _propuesta(texto_nuevo="  \n\n" + MARCA + "\n\n  ")
    assert _trae(propuesta) is True


# ---------------------------------------------------------------------------
# CASO 4 — VERDE HOY: la marca al principio con una excusa detras tambien.
# Este es el caso que impide aflojarlo de mas.
# ---------------------------------------------------------------------------
def test_caso_4_marca_al_principio_con_excusa_detras_tambien():
    propuesta = _propuesta(
        texto_nuevo=MARCA + ": no se encontro el archivo pedido",
    )
    assert _trae(propuesta) is True


# ---------------------------------------------------------------------------
# CASO 5 — VERDE HOY: una respuesta corta con la marca escondida tambien.
# Con tres renglones o menos no hay codigo de verdad que valga.
# ---------------------------------------------------------------------------
def test_caso_5_respuesta_corta_con_marca_escondida_tambien():
    propuesta = _propuesta(
        texto_nuevo="no pude hacerlo\n" + MARCA + "\n",
    )
    assert _trae(propuesta) is True


# ---------------------------------------------------------------------------
# CASO 6 — VERDE HOY: en la ruta cualquier aparicion es rendirse.
# ---------------------------------------------------------------------------
def test_caso_6_en_la_ruta_cualquier_aparicion_es_rendirse():
    propuesta = _propuesta(
        archivo=MARCA,
        texto_nuevo=_codigo_largo_sin_marca(),
    )
    assert _trae(propuesta) is True


# ---------------------------------------------------------------------------
# CASO 7 — VERDE HOY: no revienta, y sin marca contesta que NO.
# ---------------------------------------------------------------------------
def test_caso_7_no_revienta_y_sin_marca_contesta_que_no():
    # 7a) propuesta normal de quince renglones sin la marca en ninguna parte.
    propuesta_normal = _propuesta(
        archivo="modulo/de/mentira.py",
        codigo=_codigo_largo_sin_marca(),
        texto_viejo="def sumar(a, b):\n    return a + b\n",
        texto_nuevo=_codigo_largo_sin_marca(),
    )
    assert _trae(propuesta_normal) is False

    # 7b) diccionario vacio.
    assert _trae({}) is False

    # 7c) diccionario donde los campos traen numeros en vez de textos.
    propuesta_numeros = {
        "archivo": 123,
        "codigo": 456,
        "texto_viejo": 789,
        "texto_nuevo": 0,
    }
    assert _trae(propuesta_numeros) is False

    # 7d) diccionario donde los campos traen nada.
    propuesta_nada = {
        "archivo": None,
        "codigo": None,
        "texto_viejo": None,
        "texto_nuevo": None,
    }
    assert _trae(propuesta_nada) is False
