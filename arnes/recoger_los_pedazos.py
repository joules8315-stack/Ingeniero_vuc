"""Recoge los pedazos: devuelve a su sitio las copias buenas que el guardia freno.

Cuando el guardia no deja guardar un trabajo ya aprobado, la copia buena se aparta en
memoria/trabajos_sin_revisar con el final .FRENADO_POR_EL_GUARDIA y ahi se queda. Hoy
alguien la devuelve a su sitio a mano decenas de veces por noche. Eso es mecanico y se
programa (orden A-39 de Julio del 2026-09-20).

Esta pieza hace tres cosas:
  1. Lista los pedazos apartados (funcion pedazos).
  2. Averigua de donde venia cada copia (funcion donde_iba).
  3. Devuelve la copia buena a su sitio y marca la copia apartada como recogida
     (funcion recoger), sin borrar nunca nada.
"""

import json
import os
import shutil


# Final que lleva la copia buena cuando el guardia la frena.
SUFIJO_FRENADO = ".FRENADO_POR_EL_GUARDIA"

# Final que se le anade a la copia apartada cuando ya se recogio, para no recogerla dos veces.
SUFIJO_RECOGIDO = ".RECOGIDO"

# Palabra que tiene que llevar dentro el nombre del aprobado.
PALABRA_APROBADO = "APROBADO"


# Carpetas de la memoria donde vive todo esto.
CARPETA_SIN_REVISAR = os.path.join("memoria", "trabajos_sin_revisar")
CARPETA_DEL_EQUIPO = os.path.join("memoria", "trabajos_del_equipo")


def _carpeta_sin_revisar(raiz):
    """Devuelve la ruta de memoria/trabajos_sin_revisar colgando de la raiz."""
    return os.path.join(raiz, CARPETA_SIN_REVISAR)


def _carpeta_del_equipo(raiz):
    """Devuelve la ruta de memoria/trabajos_del_equipo colgando de la raiz."""
    return os.path.join(raiz, CARPETA_DEL_EQUIPO)


def pedazos(raiz):
    """Lista ordenada de los nombres de archivo apartados que acaban en .FRENADO_POR_EL_GUARDIA.

    Mira dentro de memoria/trabajos_sin_revisar. Si la carpeta no existe, devuelve lista
    vacia. Nunca revienta.
    """
    carpeta = _carpeta_sin_revisar(raiz)
    if not os.path.isdir(carpeta):
        return []
    try:
        nombres = os.listdir(carpeta)
    except OSError:
        return []
    apartados = []
    for nombre in nombres:
        if not nombre.endswith(SUFIJO_FRENADO):
            continue
        ruta = os.path.join(carpeta, nombre)
        if os.path.isfile(ruta):
            apartados.append(nombre)
    apartados.sort()
    return apartados


def _nombre_base(nombre):
    """Le quita al nombre de la copia apartada el final .FRENADO_POR_EL_GUARDIA."""
    if nombre.endswith(SUFIJO_FRENADO):
        return nombre[: -len(SUFIJO_FRENADO)]
    return nombre


def _aprobados_que_valen(raiz, nombre_base):
    """Devuelve las rutas de los aprobados del equipo que llevan dentro el nombre base.

    Solo valen los que llevan dentro el nombre base Y la palabra APROBADO. Si la carpeta
    no existe o no hay ninguno, devuelve lista vacia. Nunca revienta.
    """
    carpeta = _carpeta_del_equipo(raiz)
    if not os.path.isdir(carpeta):
        return []
    try:
        nombres = os.listdir(carpeta)
    except OSError:
        return []
    candidatos = []
    for nombre in nombres:
        if nombre_base not in nombre:
            continue
        if PALABRA_APROBADO not in nombre:
            continue
        ruta = os.path.join(carpeta, nombre)
        if os.path.isfile(ruta):
            candidatos.append(ruta)
    return candidatos


def _el_mas_nuevo(rutas):
    """De una lista de rutas devuelve la mas nueva por fecha de modificacion.

    Si no hay ninguna, devuelve None. Nunca revienta.
    """
    mejor = None
    mejor_fecha = None
    for ruta in rutas:
        try:
            fecha = os.path.getmtime(ruta)
        except OSError:
            continue
        if mejor_fecha is None or fecha > mejor_fecha:
            mejor = ruta
            mejor_fecha = fecha
    return mejor


def _archivo_del_aprobado(ruta):
    """Abre el aprobado como JSON y devuelve propuesta.archivo.

    Si no se puede abrir, no es JSON, no hay propuesta o no hay archivo dentro, devuelve
    None. Nunca revienta.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(datos, dict):
        return None
    propuesta = datos.get("propuesta")
    if not isinstance(propuesta, dict):
        return None
    archivo = propuesta.get("archivo")
    if not isinstance(archivo, str) or not archivo:
        return None
    return archivo


def donde_iba(raiz, nombre):
    """Averigua a que ruta pertenecia la copia apartada.

    Le quita al nombre el final .FRENADO_POR_EL_GUARDIA y queda el nombre base. Mira los
    archivos de memoria/trabajos_del_equipo que lleven dentro ese nombre base y tambien
    la palabra APROBADO, se queda con el mas nuevo por fecha de modificacion, lo abre como
    JSON y devuelve el valor de propuesta.archivo. Si no hay carpeta, ni archivos que
    valgan, ni ese valor, devuelve None. Nunca revienta.
    """
    nombre_base = _nombre_base(nombre)
    candidatos = _aprobados_que_valen(raiz, nombre_base)
    if not candidatos:
        return None
    elegido = _el_mas_nuevo(candidatos)
    if elegido is None:
        return None
    return _archivo_del_aprobado(elegido)


def recoger(raiz, nombre):
    """Devuelve la copia buena a su sitio y marca la copia apartada como recogida.

    Devuelve un diccionario con tres claves: ok, destino y razon.

    Primero pregunta a donde_iba. Si no hay destino, devuelve ok en falso, destino en None
    y una razon en espanol diciendo que no consta de donde venia la copia y que por eso no
    se toca nada. Si hay destino, crea las carpetas que falten, copia el contenido de la
    copia apartada encima del archivo de destino y despues le cambia el nombre a la copia
    apartada anadiendole al final .RECOGIDO, para que no se vuelva a recoger dos veces y
    para que NO se borre nada nunca. Devuelve ok en verdadero, el destino y una razon en
    espanol diciendo que la copia buena volvio a su sitio. Si algo falla, devuelve ok en
    falso con la razon del fallo.
    """
    destino = donde_iba(raiz, nombre)
    if not destino:
        return {
            "ok": False,
            "destino": None,
            "razon": (
                "No consta de donde venia la copia apartada '"
                + str(nombre)
                + "', asi que no se toca nada."
            ),
        }

    origen = os.path.join(_carpeta_sin_revisar(raiz), nombre)
    if not os.path.isfile(origen):
        return {
            "ok": False,
            "destino": destino,
            "razon": "No existe la copia apartada '" + str(nombre) + "' en trabajos_sin_revisar.",
        }

    try:
        destino_entero = destino if os.path.isabs(destino) else os.path.join(raiz, destino)
        carpeta_destino = os.path.dirname(destino_entero)
        if carpeta_destino:
            os.makedirs(carpeta_destino, exist_ok=True)
        shutil.copyfile(origen, destino_entero)
        os.replace(origen, origen + SUFIJO_RECOGIDO)
    except OSError as fallo:
        return {
            "ok": False,
            "destino": destino,
            "razon": "Fallo al recoger la copia '" + str(nombre) + "': " + str(fallo),
        }

    return {
        "ok": True,
        "destino": destino,
        "razon": "La copia buena volvio a su sitio: " + str(destino),
    }


def recoger_todos(raiz):
    """Recorre todos los pedazos, llama a recoger con cada uno y devuelve la lista de resultados."""
    resultados = []
    for nombre in pedazos(raiz):
        resultados.append(recoger(raiz, nombre))
    return resultados


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        raiz = sys.argv[1]
    else:
        raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for resultado in recoger_todos(raiz):
        if resultado.get("ok"):
            print("RECOGIDO -> " + str(resultado.get("destino")))
        else:
            print("NO RECOGIDO -> " + str(resultado.get("razon")))
