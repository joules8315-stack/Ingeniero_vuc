# -*- coding: utf-8 -*-
"""vigias/test_vigia_copista.py — Pruebas para arnes/copista.py.

Verifica que el copista aplica un cambio solo cuando debe, y que se detiene
sin tocar nada cuando no es seguro. Tambien comprueba que el copista nunca
llama a una IA.
"""
import os
import sys

# Se anade la raiz del proyecto al camino de busqueda para poder importar el copista.
# La carpeta 'vigias' y la carpeta 'arnes' estan al mismo nivel.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

# Se importa el copista. Si esto falla, todas las pruebas fallaran y se sabra
# que el problema es que no se encuentra el archivo del copista.
from arnes import copista


def _crear_archivo(tmp_path, nombre, contenido):
    """Crea un archivo temporal con el contenido dado y devuelve su ruta."""
    ruta = tmp_path / nombre
    ruta.write_text(contenido, encoding="utf-8")
    return str(ruta)


def _encargo_con_bloques(archivo, texto_viejo, texto_nuevo):
    """Construye un encargo con las etiquetas y los dos bloques de texto."""
    return f"""archivo: {archivo}
funcion: mi_funcion
TEXTO_VIEJO
{texto_viejo}
TEXTO_NUEVO
{texto_nuevo}
"""


def test_aplica_cuando_el_texto_esta_una_sola_vez(tmp_path):
    """Prueba que el copista aplica el cambio si el texto viejo aparece una sola vez."""
    nombre_archivo = "archivo_prueba.txt"
    texto_viejo = "linea_original"
    texto_nuevo = "linea_cambiada"
    ruta_archivo = _crear_archivo(tmp_path, nombre_archivo, texto_viejo)
    encargo = _encargo_con_bloques(nombre_archivo, texto_viejo, texto_nuevo)

    # Se llama al copista con la raiz del proyecto para que encuentre el archivo.
    ok, mensaje = copista.copiar(encargo, raiz=str(tmp_path))

    # El copista debe decir que todo fue bien.
    assert ok, f"El copista no aplico el cambio cuando debia. Mensaje: {mensaje}"

    # Se relee el archivo para comprobar que el cambio se hizo.
    contenido = open(ruta_archivo, encoding="utf-8").read()
    assert texto_nuevo in contenido, "El texto nuevo no aparece en el archivo despues de copiar."
    assert texto_viejo not in contenido, "El texto viejo sigue en el archivo despues de copiar."


def test_frena_si_el_texto_no_esta(tmp_path):
    """Prueba que el copista se detiene si el texto viejo no existe en el archivo."""
    nombre_archivo = "archivo_prueba.txt"
    contenido_original = "linea_original"
    texto_viejo = "texto_que_no_existe"
    texto_nuevo = "linea_cambiada"
    ruta_archivo = _crear_archivo(tmp_path, nombre_archivo, contenido_original)
    encargo = _encargo_con_bloques(nombre_archivo, texto_viejo, texto_nuevo)

    # Se llama al copista.
    ok, mensaje = copista.copiar(encargo, raiz=str(tmp_path))

    # El copista debe decir que no pudo aplicar el cambio.
    assert not ok, "El copista aplico un cambio cuando el texto viejo no estaba. Deberia haberse detenido."
    assert "no esta" in mensaje, f"El mensaje de error no dice que el texto no esta. Mensaje: {mensaje}"

    # Se comprueba que el archivo no ha cambiado nada.
    contenido_despues = open(ruta_archivo, encoding="utf-8").read()
    assert contenido_despues == contenido_original, "El archivo fue modificado cuando no debia. Debe quedar exactamente igual."


def test_frena_si_el_texto_esta_dos_veces(tmp_path):
    """Prueba que el copista se detiene si el texto viejo aparece dos veces."""
    nombre_archivo = "archivo_prueba.txt"
    linea_repetida = "linea_repetida"
    contenido_original = f"{linea_repetida}\n{linea_repetida}\n"
    texto_viejo = linea_repetida
    texto_nuevo = "linea_cambiada"
    ruta_archivo = _crear_archivo(tmp_path, nombre_archivo, contenido_original)
    encargo = _encargo_con_bloques(nombre_archivo, texto_viejo, texto_nuevo)

    # Se llama al copista.
    ok, mensaje = copista.copiar(encargo, raiz=str(tmp_path))

    # El copista debe decir que no pudo aplicar el cambio.
    assert not ok, "El copista aplico un cambio cuando el texto viejo estaba dos veces. Deberia haberse detenido."
    assert "2" in mensaje, f"El mensaje de error no dice cuantas veces aparece el texto. Mensaje: {mensaje}"

    # Se comprueba que el archivo no ha cambiado nada.
    contenido_despues = open(ruta_archivo, encoding="utf-8").read()
    assert contenido_despues == contenido_original, "El archivo fue modificado cuando no debia. Debe quedar exactamente igual."


def test_no_es_su_trabajo_si_no_hay_bloques(tmp_path):
    """Prueba que el copista se detiene si el encargo no trae los dos bloques de texto."""
    # Un encargo normal, sin las etiquetas TEXTO_VIEJO ni TEXTO_NUEVO.
    encargo = "archivo: algo.py\nfuncion: hacer_algo\nEste es un encargo normal."

    # Se llama al copista. No hace falta raiz porque no deberia tocar nada.
    ok, mensaje = copista.copiar(encargo)

    # El copista debe decir que no es su trabajo.
    assert not ok, "El copista intento trabajar con un encargo que no era suyo. Deberia haberse detenido."
    assert "NO ES TRABAJO DEL COPISTA" in mensaje, f"El mensaje de error no dice que no es su trabajo. Mensaje: {mensaje}"


def test_frena_si_el_archivo_no_existe(tmp_path):
    """Prueba que el copista se detiene si el archivo indicado no existe."""
    nombre_archivo = "archivo_que_no_existe.txt"
    texto_viejo = "linea_original"
    texto_nuevo = "linea_cambiada"
    encargo = _encargo_con_bloques(nombre_archivo, texto_viejo, texto_nuevo)

    # Se llama al copista con una raiz que no contiene el archivo.
    ok, mensaje = copista.copiar(encargo, raiz=str(tmp_path))

    # El copista debe decir que no pudo aplicar el cambio.
    assert not ok, "El copista intento trabajar con un archivo que no existe. Deberia haberse detenido."
    assert "no esta" in mensaje, f"El mensaje de error no dice que el archivo no esta. Mensaje: {mensaje}"


def test_el_copista_no_llama_a_ninguna_ia():
    """Prueba que el archivo del copista no importa ninguna IA ni libreria de red."""
    ruta_copista = os.path.join(RAIZ, "arnes", "copista.py")
    with open(ruta_copista, encoding="utf-8") as f:
        lineas = f.readlines()

    # Palabras que delatan una llamada a una IA o a la red.
    palabras_prohibidas = ["cerebro", "openai", "gemini", "deepseek", "groq", "requests", "urllib"]

    # Solo se miran las lineas que empiezan por 'import' o por 'from'.
    for linea in lineas:
        linea_limpia = linea.strip().lower()
        if linea_limpia.startswith("import") or linea_limpia.startswith("from"):
            for palabra in palabras_prohibidas:
                assert palabra not in linea_limpia, f"El copista importa '{palabra}', lo que significa que podria llamar a una IA o a la red. Linea: {linea.strip()}"
