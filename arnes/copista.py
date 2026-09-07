# -*- coding: utf-8 -*-
"""arnes/copista.py — Aplica al disco un cambio que YA viene decidido.

POR QUE existe: medido el 2026-09-06, de las 8 rondas pagadas al cerebro de pago,
en 5 el encargo ya llevaba dentro el texto de antes y el de despues exactos: el
cerebro solo los copio. Cinco vueltas pagadas por una fotocopia. Este programa
hace esa fotocopia sin llamar a ningun cerebro, sin decidir nada y sin gastar.

QUE hace: recibe un encargo que trae dos bloques (texto de antes y texto de
despues), comprueba que el texto de antes esta literal y una sola vez en el
archivo indicado, y si es asi aplica el cambio reusando la pieza que ya existe
y que ya sabe comprobar que el archivo no queda roto. Si algo no cuadra, se
FRENA y no toca nada.
"""
import os
import sys


def leer_bloques(encargo):
    """Saca del encargo los bloques marcados: archivo, funcion, texto_viejo y texto_nuevo.

    Devuelve un diccionario con esos cuatro campos, o None si no encuentra los dos
    bloques de texto (texto_viejo y texto_nuevo). Sin los dos, esto no es un encargo
    mecanico y no le toca al copista.
    """
    lineas = encargo.splitlines()
    bloques = {}
    etiqueta_actual = None
    contenido_actual = []

    for linea in lineas:
        # Detectar si la linea es una etiqueta al principio
        if linea.startswith("archivo:"):
            if etiqueta_actual:
                bloques[etiqueta_actual] = "\n".join(contenido_actual).strip()
            etiqueta_actual = "archivo"
            contenido_actual = [linea[len("archivo:"):].strip()]
        elif linea.startswith("funcion:"):
            if etiqueta_actual:
                bloques[etiqueta_actual] = "\n".join(contenido_actual).strip()
            etiqueta_actual = "funcion"
            contenido_actual = [linea[len("funcion:"):].strip()]
        elif linea.startswith("TEXTO_VIEJO"):
            if etiqueta_actual:
                bloques[etiqueta_actual] = "\n".join(contenido_actual).strip()
            etiqueta_actual = "texto_viejo"
            contenido_actual = []
        elif linea.startswith("TEXTO_NUEVO"):
            if etiqueta_actual:
                bloques[etiqueta_actual] = "\n".join(contenido_actual).strip()
            etiqueta_actual = "texto_nuevo"
            contenido_actual = []
        else:
            if etiqueta_actual:
                contenido_actual.append(linea)

    # Guardar el ultimo bloque
    if etiqueta_actual:
        bloques[etiqueta_actual] = "\n".join(contenido_actual).strip()

    # Verificar que esten los dos bloques de texto
    if "texto_viejo" not in bloques or "texto_nuevo" not in bloques:
        return None

    # Asegurar que los campos archivo y funcion existan (aunque sea vacios)
    bloques.setdefault("archivo", "")
    bloques.setdefault("funcion", "")

    return bloques


def comprobar(ruta_archivo, texto_viejo):
    """Cuenta cuantas veces aparece el texto_viejo en el archivo.

    Devuelve una pareja (cuantas_veces, mensaje_en_palabras_simples).
    """
    if not os.path.exists(ruta_archivo):
        return 0, f"El archivo no esta en la ruta: {ruta_archivo}"

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except Exception as e:
        return 0, f"No se pudo leer el archivo: {e}"

    cuantas = contenido.count(texto_viejo)

    if cuantas == 0:
        # Mostrar las primeras 80 letras del texto buscado
        primeras_letras = texto_viejo[:80]
        return 0, f"El texto de antes no esta en el archivo. Se buscaba algo que empezaba asi: '{primeras_letras}'"
    elif cuantas >= 2:
        return cuantas, f"El texto de antes aparece {cuantas} veces. Hay que alargar el texto hasta que sea unico."
    else:
        return 1, "Listo: el texto de antes aparece exactamente una vez."


def copiar(encargo, raiz=None):
    """Funcion principal: aplica el cambio si el texto viejo esta una sola vez.

    Devuelve una pareja (ok, mensaje).
    """
    bloques = leer_bloques(encargo)
    if bloques is None:
        return False, "NO ES TRABAJO DEL COPISTA: el encargo no trae los dos textos"

    archivo = bloques.get("archivo", "")
    funcion = bloques.get("funcion", "")
    texto_viejo = bloques.get("texto_viejo", "")
    texto_nuevo = bloques.get("texto_nuevo", "")

    # Resolver la ruta: si raiz viene y la ruta no es absoluta, se juntan
    ruta_resuelta = archivo
    if raiz and not os.path.isabs(archivo):
        ruta_resuelta = os.path.join(raiz, archivo)

    # Comprobar que el texto viejo esta una sola vez
    cuantas, mensaje = comprobar(ruta_resuelta, texto_viejo)
    if cuantas != 1:
        return False, mensaje

    # Aplicar el cambio reusando la pieza que ya existe
    try:
        from cuerpo.aplicador import aplicar_cambio
        propuesta = {
            "archivo": archivo,  # la ruta tal como venia
            "funcion": funcion,
            "texto_viejo": texto_viejo,
            "texto_nuevo": texto_nuevo,
        }
        ok, msg = aplicar_cambio(propuesta, raiz=raiz)
        return ok, msg
    except Exception as e:
        return False, f"Error al aplicar el cambio: {e}"


if __name__ == "__main__":
    # Bloque de arranque para probar a mano desde la terminal
    if len(sys.argv) < 3:
        print("Uso: python arnes/copista.py <ruta_del_archivo_de_encargo> <carpeta_del_proyecto>")
        sys.exit(1)

    ruta_encargo = sys.argv[1]
    carpeta_proyecto = sys.argv[2]

    try:
        with open(ruta_encargo, "r", encoding="utf-8") as f:
            encargo_texto = f.read()
    except Exception as e:
        print(f"No se pudo leer el archivo de encargo: {e}")
        sys.exit(1)

    ok, mensaje = copiar(encargo_texto, raiz=carpeta_proyecto)
    print(mensaje)
    sys.exit(0 if ok else 1)
