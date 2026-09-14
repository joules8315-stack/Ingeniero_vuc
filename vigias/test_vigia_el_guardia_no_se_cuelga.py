"""VIGIA — EL GUARDIA NO SE CUELGA.

QUE PROTEGE
------------
Protege que el guardia de guardado (arnes/guardia_de_guardado.py) no vuelva a
colgarse lanzando las vigias con la entrada de teclado (stdin) ABIERTA, y que
no vuelva a DEJAR GUARDAR cuando las vigias no terminan.

EL FALLO, MEDIDO
----------------
El 2026-09-13/14 un guardado se quedo COLGADO 5 horas y media: de 22:56 a 04:27.
El guardia lanzaba las vigias con subprocess.run SIN cerrar stdin, y alguna
prueba lanzaba un candado que se quedo esperando datos por esa entrada, que
nunca llegaban. El tope de 900 segundos NO lo corto. Al parar a mano la corrida
colgada, el guardia apunto "no se pudieron correr las vigias: se deja pasar" y
DEJO GUARDAR SIN PROBAR. Dos dias antes, una corrida igual tardo 1 hora 19
minutos. Big Pickle corrio las mismas vigias con la entrada cerrada: 759 verdes
en 4 minutos.

LAS PALABRAS DE JULIO
---------------------
"que mas no permite que avancemos, porque hasta que lo que nos frena no se
repare, seguimos perdiendo tiempo y dinero".

AVISO AL REVISOR
----------------
Esta vigia NACE ROJA a proposito (pruebas 1 y 2): exige una reparacion que
todavia no esta hecha. Se escribe la vigia primero, luego la cura. Que falle hoy
contra el codigo actual NO es un error del trabajo: es lo que se pide.

La prueba 3 NO se cambia: si falta la herramienta de pruebas (pytest no esta),
se avisa y se deja pasar, como dice su ley.
"""

import os
import subprocess
import sys
import types


AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import guardia_de_guardado  # noqa: E402


def _preparar_raiz(tmp_path):
    """Crea en tmp_path la carpeta vigias/ que _vigias espera encontrar."""
    os.makedirs(tmp_path / "vigias")
    return str(tmp_path)


def test_las_vigias_se_lanzan_con_la_entrada_cerrada(tmp_path, monkeypatch):
    """Las vigias deben lanzarse con stdin cerrado (subprocess.DEVNULL).

    NACE ROJA: hoy el guardia lanza subprocess.run sin stdin, y una prueba que
espera datos por la entrada cuelga el guardado para siempre (paso 5 horas y
media el 2026-09-13).
    """
    raiz = _preparar_raiz(tmp_path)
    kwargs_vistos = []

    def falso(*args, **kwargs):
        kwargs_vistos.append(kwargs)
        return types.SimpleNamespace(returncode=0, stdout="1 passed", stderr="")

    monkeypatch.setattr(guardia_de_guardado.subprocess, "run", falso)

    guardia_de_guardado._vigias(raiz)

    assert kwargs_vistos, "no se llego a lanzar subprocess.run"
    assert kwargs_vistos[0].get("stdin") is subprocess.DEVNULL, (
        "las vigias se lanzan con la entrada abierta; una prueba que espera "
        "datos por ahi cuelga el guardado para siempre (paso 5 horas y media "
        "el 2026-09-13)"
    )


def test_si_las_vigias_no_terminan_NO_se_deja_guardar(tmp_path, monkeypatch):
    """Si las vigias no terminan (TimeoutExpired), el guardia debe FRENAR.

    NACE ROJA: hoy cualquier excepcion devuelve (True, "...se deja pasar"), y
asi entra codigo roto sin que nadie lo vea.
    """
    raiz = _preparar_raiz(tmp_path)

    def falso(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="pytest", timeout=900)

    monkeypatch.setattr(guardia_de_guardado.subprocess, "run", falso)

    paso, mensaje = guardia_de_guardado._vigias(raiz)

    assert paso is False, (
        "las vigias no terminaron y el guardia dejo guardar sin probar; asi "
        "entra codigo roto sin que nadie lo vea"
    )


def test_si_pytest_no_esta_se_sigue_dejando_pasar_con_aviso(tmp_path, monkeypatch):
    """Si falta la herramienta de pruebas, se avisa y se deja pasar.

    Esto NO se cambia: si falta pytest, se avisa y se deja pasar, como dice su
ley.
    """
    raiz = _preparar_raiz(tmp_path)

    def falso(*args, **kwargs):
        raise FileNotFoundError("no hay python")

    monkeypatch.setattr(guardia_de_guardado.subprocess, "run", falso)

    paso, mensaje = guardia_de_guardado._vigias(raiz)

    assert paso is True
    assert "no se pudieron correr" in mensaje
