from cuerpo import obrero


def test_el_encargo_de_crear_codigo_pide_llaves_por_partes():
    """El encargo de crear un .py tiene que pedir las llaves de mentira POR PARTES.

    Si el obrero escribe las llaves de golpe, el JSON de su respuesta se corta a medio
    camino y el trabajo se descarta. La regla vive en el propio encargo: hay que
    comprobar que el texto que devuelve _prompt_obrero la lleva dentro.
    """
    texto = obrero._prompt_obrero(
        "material",
        "Crear el archivo nuevo cuerpo/x.py",
        "crear",
    )
    assert isinstance(texto, str), "el encargo tiene que ser texto"
    assert "forma de llave" in texto, (
        "el encargo de crear codigo no habla de la forma de llave: "
        "el obrero volvera a escribir las llaves de golpe"
    )
    assert "partes" in texto.lower(), (
        "el encargo de crear codigo no pide armar las llaves por partes: "
        "el JSON se cortara a medio camino"
    )


if __name__ == "__main__":
    test_el_encargo_de_crear_codigo_pide_llaves_por_partes()
    print("OK: el escritor no escribe llaves de golpe")
