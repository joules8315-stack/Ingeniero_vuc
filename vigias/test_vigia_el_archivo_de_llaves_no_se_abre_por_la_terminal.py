"""VIGIA: el archivo de llaves NO se abre por la terminal.

LEY (Julio): las llaves viven SOLO en el archivo de llaves y NUNCA se leen por la
terminal. Ni con cat, ni con type, ni con Get-Content, ni con la ruta completa.

LO MEDIDO EL 2026-09-21: el candado arnes/candado_terminal.py dejaba pasar las cuatro
ordenes de abajo devolviendo 0. Esta vigia nace ROJA y exige que TODAS devuelvan 2.

COMO SE COMPRUEBA: se ejecuta el candado DE VERDAD con subprocess, pasandole por la
entrada el JSON del gancho (hook_event_name=PreToolUse, tool_name=Bash, tool_input.command).
Se pone INGENIERO_OFF vacio en el entorno para que el interruptor no altere la prueba.

Y ademas se comprueba que ordenes normales (dir, git status, python -m pytest vigias)
siguen devolviendo 0, para no frenar en falso.
"""

import json
import os
import subprocess
import sys


# Raiz del proyecto: este archivo vive en <raiz>/vigias/, asi que la raiz es su abuelo.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDADO = os.path.join(RAIZ, "arnes", "candado_terminal.py")


# Las cuatro ordenes que HOY se cuelan y que la ley prohibe.
ORDENES_PROHIBIDAS = [
    "cat .env",
    "type .env",
    "Get-Content .env",
    "Get-Content C:/Ingeniero_VUC/.env",
]

# Ordenes normales que NO se deben frenar.
ORDENES_PERMITIDAS = [
    "dir",
    "git status",
    "python -m pytest vigias",
]


def _entorno_limpio():
    """Entorno con INGENIERO_OFF vacio para que el interruptor no altere la prueba."""
    env = dict(os.environ)
    env["INGENIERO_OFF"] = ""
    return env


def _correr_candado(command):
    """Ejecuta el candado de verdad con la orden dada y devuelve su codigo de salida."""
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }
    entrada = json.dumps(payload).encode("utf-8")
    proc = subprocess.run(
        [sys.executable, CANDADO],
        input=entrada,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=RAIZ,
        env=_entorno_limpio(),
    )
    return proc.returncode


def test_el_candado_existe():
    """Sin el candado no hay nada que vigilar: si falta, la vigia avisa claro."""
    assert os.path.isfile(CANDADO), (
        "No existe el candado que hay que vigilar: %s" % CANDADO
    )


def test_las_cuatro_ordenes_de_llaves_devuelven_2():
    """cat/type/Get-Content sobre el archivo de llaves: TODAS deben devolver 2."""
    fallos = []
    for orden in ORDENES_PROHIBIDAS:
        codigo = _correr_candado(orden)
        if codigo != 2:
            fallos.append("%r devolvio %s (se esperaba 2)" % (orden, codigo))
    assert not fallos, (
        "El archivo de llaves se abre por la terminal. La ley dice que NUNCA. "
        "Ordenes que se colaron: " + "; ".join(fallos)
    )


def test_las_ordenes_normales_devuelven_0():
    """dir, git status y pytest vigias NO se deben frenar: devuelven 0."""
    fallos = []
    for orden in ORDENES_PERMITIDAS:
        codigo = _correr_candado(orden)
        if codigo != 0:
            fallos.append("%r devolvio %s (se esperaba 0)" % (orden, codigo))
    assert not fallos, (
        "El candado frena en falso ordenes normales: " + "; ".join(fallos)
    )


if __name__ == "__main__":
    # Permite correrlo a mano: python vigias/test_vigia_el_archivo_de_llaves_no_se_abre_por_la_terminal.py
    test_el_candado_existe()
    test_las_cuatro_ordenes_de_llaves_devuelven_2()
    test_las_ordenes_normales_devuelven_0()
    print("OK: el archivo de llaves no se abre por la terminal y lo normal pasa.")
