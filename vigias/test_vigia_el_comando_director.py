# -*- coding: utf-8 -*-
"""Vigia del comando `python ingeniero.py director ...` (A-48, 2026-09-22).

Corre el comando DE VERDAD con subprocess.run y comprueba tres cosas:

  1. `director estado` sale con 0 y su salida habla de 'pendientes o corriendo'.
  2. `director nueva 'esto no es json'` sale con 1 y su salida dice 'JSON'.
  3. `director loquesea` sale con 1 y su salida ensena el uso ('director estado').

Solo lee: ninguna prueba cambia la lista de tareas. La prueba 2 manda un texto que NO es
JSON, asi que el director lo rechaza antes de tocar nada; aun asi, si algun dia dejara de
rechazarlo, esta vigia no escribe ni borra nada por su cuenta.

La raiz del proyecto es la carpeta de arriba de `vigias/`, o sea la que contiene
`ingeniero.py`. Se calcula desde la ruta de este mismo archivo, sin numeros a mano.
"""

import os
import subprocess
import sys


# La carpeta de esta vigia es .../vigias; la raiz del proyecto es la de arriba.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
INGENIERO = os.path.join(RAIZ, "ingeniero.py")


def _correr_director(*argumentos):
    """Corre `python ingeniero.py director <argumentos>` desde la raiz del proyecto.

    Devuelve el objeto CompletedProcess. No usa shell: la lista de argumentos va tal cual,
    para que un texto con espacios o comillas no se rompa por el camino.
    """
    return subprocess.run(
        [sys.executable, "ingeniero.py", "director"] + list(argumentos),
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )


def _salida(r):
    """Salida completa (stdout + stderr) para poder buscar dentro sin perder nada."""
    return (r.stdout or "") + (r.stderr or "")


def test_estado_sale_con_cero_y_habla_de_pendientes_o_corriendo():
    """`director estado` es la foto del tablero: debe salir con 0 y decir que hay pendientes."""
    assert os.path.isfile(INGENIERO), "no encuentro ingeniero.py en %s" % RAIZ
    r = _correr_director("estado")
    texto = _salida(r)
    assert r.returncode == 0, (
        "`director estado` deberia salir con 0 y salio con %s. Salida:\n%s"
        % (r.returncode, texto)
    )
    assert "pendientes o corriendo" in texto, (
        "la salida de `director estado` no habla de 'pendientes o corriendo'. Salida:\n%s"
        % texto
    )


def test_nueva_con_texto_que_no_es_json_sale_con_uno_y_dice_json():
    """Una orden que no es JSON se rechaza: sale con 1 y la salida nombra 'JSON'."""
    r = _correr_director("nueva", "esto no es json")
    texto = _salida(r)
    assert r.returncode == 1, (
        "`director nueva 'esto no es json'` deberia salir con 1 y salio con %s. Salida:\n%s"
        % (r.returncode, texto)
    )
    assert "JSON" in texto, (
        "la salida no dice 'JSON' al rechazar una orden que no es JSON. Salida:\n%s" % texto
    )


def test_accion_desconocida_sale_con_uno_y_ensena_el_uso():
    """Una accion que no existe no se inventa: sale con 1 y ensena el uso del comando."""
    r = _correr_director("loquesea")
    texto = _salida(r)
    assert r.returncode == 1, (
        "`director loquesea` deberia salir con 1 y salio con %s. Salida:\n%s"
        % (r.returncode, texto)
    )
    assert "director estado" in texto, (
        "la salida no ensena el uso ('director estado') ante una accion desconocida. Salida:\n%s"
        % texto
    )
