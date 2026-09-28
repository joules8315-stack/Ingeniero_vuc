# -*- coding: utf-8 -*-
"""Instalador de las reglas de Codex.

Para que sirve
---------------
Codex lee sus reglas en un archivo llamado AGENTS.md que vive dentro de su
carpeta personal (la carpeta .codex del usuario del sistema). En este proyecto
las reglas buenas se escriben en config/codex/reglas_codex.md. Este programa
copia el documento del proyecto encima del archivo que lee Codex, y antes de
pisarlo guarda una copia de lo que habia en memoria/rescate, con la fecha en
el nombre para que no se pise una copia con otra.

Orden de uso
------------
1. Se lee el documento fuente del proyecto (config/codex/reglas_codex.md).
   Si no existe, no se hace nada y se dice claro: no se inventa contenido.
2. Si el destino (la carpeta .codex del usuario, archivo AGENTS.md) ya existe,
   se guarda una copia en memoria/rescate con la fecha en el nombre.
   Si no existe, se dice y se sigue.
3. Se escribe el destino con el contenido del documento fuente, en utf-8.
4. Se devuelve un resumen en palabras simples, listo para leer.

Como se ejecuta
---------------
    python arnes/instalar_reglas_codex.py

No pide llaves, no usa red, no llama a ninguna IA y no corre pruebas.
Si algo falla, no revienta: devuelve el motivo en una frase.
"""

import os
import shutil
import sys
from datetime import date


# Ruta del documento fuente, relativa a la raiz del proyecto.
RUTA_FUENTE_RELATIVA = os.path.join("config", "codex", "reglas_codex.md")

# Carpeta de rescate, relativa a la raiz del proyecto.
RUTA_RESCATE_RELATIVA = os.path.join("memoria", "rescate")

# Nombre del archivo que lee Codex dentro de su carpeta personal.
NOMBRE_DESTINO = "AGENTS.md"

# Nombre de la carpeta personal de Codex dentro de la carpeta del usuario.
NOMBRE_CARPETA_CODEX = ".codex"


def _raiz_del_proyecto():
    """Devuelve la carpeta raiz del proyecto.

    Se calcula a partir de la ubicacion de este archivo: este archivo vive en
    <raiz>/arnes/instalar_reglas_codex.py, asi que la raiz es la carpeta de
    arriba de 'arnes'.
    """
    carpeta_de_este_archivo = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(carpeta_de_este_archivo)


def _carpeta_codex_del_usuario():
    """Devuelve la carpeta .codex del usuario del sistema.

    Se averigua a partir de la carpeta del usuario (HOME en Linux/Mac,
    USERPROFILE en Windows). Nunca se escribe a mano la ruta de un usuario
    concreto.
    """
    carpeta_usuario = os.path.expanduser("~")
    return os.path.join(carpeta_usuario, NOMBRE_CARPETA_CODEX)


def _leer_texto(ruta):
    """Lee un archivo de texto en utf-8 y devuelve su contenido."""
    with open(ruta, "r", encoding="utf-8") as manejador:
        return manejador.read()


def _escribir_texto(ruta, contenido):
    """Escribe un archivo de texto en utf-8, creando la carpeta si hace falta."""
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as manejador:
        manejador.write(contenido)


def _nombre_copia_con_fecha(nombre_original):
    """Arma el nombre de la copia de seguridad con la fecha de hoy.

    Ejemplo: AGENTS.md -> AGENTS.md.2026-09-28.bak
    """
    hoy = date.today().isoformat()
    return nombre_original + "." + hoy + ".bak"


def instalar_reglas_codex():
    """Hace el trabajo completo y devuelve un resumen en palabras simples.

    Devuelve un diccionario con estas claves:
      - 'ok': True si se instalo, False si algo impidio hacerlo.
      - 'mensaje': frase en palabras simples, lista para leer.
      - 'fuente': ruta del documento del proyecto (o None).
      - 'destino': ruta del archivo que lee Codex (o None).
      - 'copia': ruta de la copia de seguridad (o None si no habia nada).
    """
    raiz = _raiz_del_proyecto()
    ruta_fuente = os.path.join(raiz, RUTA_FUENTE_RELATIVA)
    carpeta_rescate = os.path.join(raiz, RUTA_RESCATE_RELATIVA)
    carpeta_codex = _carpeta_codex_del_usuario()
    ruta_destino = os.path.join(carpeta_codex, NOMBRE_DESTINO)

    # Paso 1: leer el documento fuente del proyecto.
    if not os.path.isfile(ruta_fuente):
        return {
            "ok": False,
            "mensaje": (
                "No se instalo nada: no existe el documento de reglas del "
                "proyecto en " + ruta_fuente + ". No se inventa contenido "
                "ni se escribe un archivo vacio."
            ),
            "fuente": ruta_fuente,
            "destino": ruta_destino,
            "copia": None,
        }

    try:
        contenido = _leer_texto(ruta_fuente)
    except OSError as error:
        return {
            "ok": False,
            "mensaje": (
                "No se pudo leer el documento de reglas del proyecto en "
                + ruta_fuente + ". Motivo: " + str(error)
            ),
            "fuente": ruta_fuente,
            "destino": ruta_destino,
            "copia": None,
        }

    # Paso 2: guardar copia de lo que hay hoy en el destino, si existe.
    ruta_copia = None
    if os.path.isfile(ruta_destino):
        try:
            if not os.path.isdir(carpeta_rescate):
                os.makedirs(carpeta_rescate, exist_ok=True)
            nombre_copia = _nombre_copia_con_fecha(NOMBRE_DESTINO)
            ruta_copia = os.path.join(carpeta_rescate, nombre_copia)
            shutil.copyfile(ruta_destino, ruta_copia)
        except OSError as error:
            return {
                "ok": False,
                "mensaje": (
                    "No se instalo nada: no se pudo guardar la copia de "
                    "seguridad de " + ruta_destino + ". Motivo: " + str(error)
                ),
                "fuente": ruta_fuente,
                "destino": ruta_destino,
                "copia": None,
            }

    # Paso 3: escribir el destino con el contenido del documento fuente.
    try:
        _escribir_texto(ruta_destino, contenido)
    except OSError as error:
        return {
            "ok": False,
            "mensaje": (
                "No se pudo escribir el archivo de reglas de Codex en "
                + ruta_destino + ". Motivo: " + str(error)
            ),
            "fuente": ruta_fuente,
            "destino": ruta_destino,
            "copia": ruta_copia,
        }

    # Paso 4: armar el resumen en palabras simples.
    partes = []
    partes.append("Listo. Las reglas de Codex quedaron instaladas.")
    partes.append("Se copio de: " + ruta_fuente)
    partes.append("Se copio a: " + ruta_destino)
    if ruta_copia is not None:
        partes.append(
            "Antes de pisarlo se guardo una copia de lo que habia en: "
            + ruta_copia
        )
    else:
        partes.append(
            "No habia nada antes en el destino, asi que no hubo copia de "
            "seguridad que guardar."
        )
    partes.append(
        "Codex ya puede leer las reglas nuevas, incluido el apartado de que "
        "no espera nunca."
    )

    return {
        "ok": True,
        "mensaje": " ".join(partes),
        "fuente": ruta_fuente,
        "destino": ruta_destino,
        "copia": ruta_copia,
    }


def main():
    """Punto de entrada cuando el archivo se ejecuta directamente."""
    try:
        resultado = instalar_reglas_codex()
    except Exception as error:  # noqa: BLE001 - no reventar en la cara de Julio
        print("No se pudo instalar las reglas de Codex. Motivo: " + str(error))
        return 1

    print(resultado["mensaje"])
    return 0 if resultado["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
