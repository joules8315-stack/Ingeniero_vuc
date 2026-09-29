"""Vigia: el guardado PIDE TURNO antes de trabajar y lo SUELTA al terminar.

NACE ROJA A PROPOSITO. Hoy arnes/guardia_de_guardado.py:main() no llama a
pedir_turno ni a soltar_turno, asi que la lista de apuntes queda vacia y la
prueba falla. El arreglo (conectar los turnos al guardado) entra en otra ronda;
aqui NO se toca ningun otro archivo.

Montaje: todo falseado. La pieza de los turnos se mete en sys.modules con la
clave 'turno_de_guardado' (porque el guardado la importa por nombre suelto) y
apunta en una lista cuando le piden turno y cuando lo sueltan. Dentro del
guardado se falsean _lo_que_se_va_a_guardar, _hay_llaves, _vigias y
subprocess.run para que la prueba sea rapida y no toque nada de verdad.

Sin IA, sin red, sin procesos de verdad, sin escribir en la memoria real.
"""

import importlib
import os
import sys
import types

import pytest


# --- Arranque: meter en sys.path la carpeta de arriba de vigias y la carpeta arnes ---
# La pieza del guardado importa a sus vecinas por nombre suelto, asi que arnes
# tiene que estar en sys.path. Y la carpeta de arriba de vigias tambien, para
# poder importar el paquete arnes si hiciera falta.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_VIGIAS = _AQUI
_RAIZ = os.path.dirname(_VIGIAS)
_ARNES = os.path.join(_RAIZ, "arnes")

for _p in (_RAIZ, _ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


class _ResultadoFalso:
    """Imita lo justo de subprocess.run para que no se llame a git de verdad."""

    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_el_guardado_pide_turno_y_lo_suelta(monkeypatch):
    """El guardado tiene que PEDIR turno antes de trabajar y SOLTARLO al final.

    Hoy sale roja porque el guardado no pide turno a nadie: la lista de apuntes
    queda vacia. No falla por mal montaje: el montaje es todo falseado y no
    revienta.
    """
    apuntes = []

    # --- 1. La pieza de los turnos, falseada y metida en sys.modules ---
    # El guardado la importa por nombre suelto ('turno_de_guardado'), asi que el
    # falso tiene que estar en la lista de modulos ya cargados de Python.
    def _pedir_turno_falso(carpeta, tope_segundos=None, segundos_atrancado=None):
        apuntes.append("pidio")
        return {
            "conseguido": True,
            "motivo": "turno concedido (falso de prueba)",
            "ruta": os.path.join(carpeta, "turno.falso"),
            "testigo": "testigo-falso",
        }

    def _soltar_turno_falso(turno):
        apuntes.append("solto")
        return True

    modulo_turnos_falso = types.ModuleType("turno_de_guardado")
    modulo_turnos_falso.pedir_turno = _pedir_turno_falso
    modulo_turnos_falso.soltar_turno = _soltar_turno_falso
    monkeypatch.setitem(sys.modules, "turno_de_guardado", modulo_turnos_falso)

    # --- 2. La pieza del guardado, importada dentro de la prueba ---
    guardia = importlib.import_module("guardia_de_guardado")

    # Falseamos lo que hace lento o toca el disco de verdad.
    monkeypatch.setattr(guardia, "_lo_que_se_va_a_guardar", lambda raiz: [])
    monkeypatch.setattr(guardia, "_hay_llaves", lambda raiz, archivos: [])
    monkeypatch.setattr(guardia, "_vigias", lambda raiz: (True, "todo bien"))

    # Y subprocess.run, para que no se llame a git de verdad.
    def _run_falso(*args, **kwargs):
        return _ResultadoFalso(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(guardia.subprocess, "run", _run_falso)

    # --- 3. Se llama a main() y se comprueban las DOS cosas juntas ---
    resultado = guardia.main()

    # El guardado deja pasar (0) porque todo esta falseado a bien.
    assert resultado == 0, (
        "el guardado deberia dejar pasar con todo falseado a bien, "
        "pero devolvio %r" % (resultado,)
    )

    # Y aqui esta lo que hoy falta: que se haya PEDIDO el turno y que se haya SOLTADO.
    assert "pidio" in apuntes, (
        "el guardado NO pidio turno antes de trabajar: la lista de apuntes "
        "quedo vacia (%r). Hoy el guardado no pide turno a nadie; el arreglo "
        "entra en otra ronda." % (apuntes,)
    )
    assert "solto" in apuntes, (
        "el guardado NO solto el turno al terminar: la lista de apuntes "
        "quedo en %r. Hoy el guardado no suelta turno a nadie; el arreglo "
        "entra en otra ronda." % (apuntes,)
    )

    # Y el orden correcto: primero se pide, despues se suelta.
    assert apuntes.index("pidio") < apuntes.index("solto"), (
        "el guardado solto el turno antes de pedirlo: %r" % (apuntes,)
    )
