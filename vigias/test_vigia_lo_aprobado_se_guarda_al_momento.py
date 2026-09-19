"""VIGIA: lo aprobado se guarda en la historia AL MOMENTO.

QUE PROTEGE
------------
Protege el trabajo YA PAGADO del equipo. Cuando el equipo aprueba una ronda, el trabajo
aprobado tiene que quedar guardado en la historia de git en ese mismo momento, sin
depender de que alguien corra el guardado a mano despues. Mientras no se guarde, la
siguiente ronda o un deshacer pueden llevarse el trabajo por delante.

FECHA
-----
2026-09-14.

LO QUE ORDENO JULIO (2026-09-14), literal:
    "que se guarde de una vez el trabajo realizado y aprobado, que es algo que no se
     viene haciendo y eso si explica la perdida de trabajo"

LOS NUMEROS MEDIDOS
-------------------
El 13 y 14 de septiembre el equipo aprobo 30 rondas y hay 29 trabajos aprobados
archivados, pero NINGUNO se guardo en la historia al aprobarse: dependia de que alguien
corriera el guardado a mano despues. Asi se perdio trabajo pagado.

LA PIEZA QUE ESTA VIGIA EXIGE (todavia NO existe)
-------------------------------------------------
En arnes/candado_equipo.py, una funcion:

    guardar_en_la_historia(raiz, archivos, mensaje) -> (True, texto) | (False, motivo)

que guarda en git SOLO esos archivos (git add -- archivos y git commit -m mensaje --
archivos, con la entrada de teclado cerrada). Si el guardia de guardado la frena,
devuelve False con el motivo y el archivo sigue en el disco. NUNCA lanza.

ESTA VIGIA NACE ROJA A PROPOSITO
--------------------------------
La funcion guardar_en_la_historia aun no existe en arnes/candado_equipo.py. Que falle
hoy es lo pedido: la vigia exige la pieza que todavia no se ha construido.

COMO SE PRUEBA SIN TOCAR NINGUN PROYECTO REAL
---------------------------------------------
Cada prueba crea en tmp_path un repositorio git de mentira y trabaja solo ahi dentro.
"""

import os
import subprocess
import sys


AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import candado_equipo  # noqa: E402


# ---------------------------------------------------------------------------
# AYUDANTES
# ---------------------------------------------------------------------------

def _repo(tmp_path):
    """Prepara en tmp_path un repositorio git de mentira con un primer guardado.

    Deja el repositorio con un commit inicial que contiene base.txt, para que
    las pruebas puedan mirar despues cual fue el ULTIMO guardado.
    """
    subprocess.run(["git", "init", "-q"], cwd=str(tmp_path), check=True)
    subprocess.run(
        ["git", "config", "user.email", "prueba@ejemplo.invalido"],
        cwd=str(tmp_path),
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "prueba"],
        cwd=str(tmp_path),
        check=True,
    )
    (tmp_path / "base.txt").write_text("base\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "--", "base.txt"],
        cwd=str(tmp_path),
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-q", "-m", "primer guardado", "--", "base.txt"],
        cwd=str(tmp_path),
        check=True,
    )


def _archivos_del_ultimo_guardado(tmp_path):
    """Devuelve la lista de archivos que toca el ULTIMO guardado de la historia."""
    salida = subprocess.run(
        ["git", "log", "-1", "--name-only", "--format="],
        cwd=str(tmp_path),
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [linea.strip() for linea in salida.splitlines() if linea.strip()]


# ---------------------------------------------------------------------------
# LAS PRUEBAS (todas nacen rojas: la funcion aun no existe)
# ---------------------------------------------------------------------------

def test_lo_aprobado_queda_guardado(tmp_path):
    """Lo que el equipo aprueba tiene que quedar en la historia al momento."""
    _repo(tmp_path)
    (tmp_path / "pieza.py").write_text("x = 1\n", encoding="utf-8")

    ok, msg = candado_equipo.guardar_en_la_historia(
        str(tmp_path), ["pieza.py"], "equipo aprobado"
    )

    assert ok, msg
    assert "pieza.py" in _archivos_del_ultimo_guardado(tmp_path), (
        "lo aprobado no se guardo en la historia; la siguiente ronda o un deshacer "
        "puede llevarselo"
    )


def test_solo_se_guarda_lo_aprobado(tmp_path):
    """No se cuela en la historia nada que el equipo no haya aprobado."""
    _repo(tmp_path)
    (tmp_path / "otro.py").write_text("z = 3\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "--", "otro.py"],
        cwd=str(tmp_path),
        check=True,
    )
    (tmp_path / "pieza.py").write_text("x = 1\n", encoding="utf-8")

    ok, msg = candado_equipo.guardar_en_la_historia(
        str(tmp_path), ["pieza.py"], "equipo aprobado"
    )

    assert ok, msg
    guardados = _archivos_del_ultimo_guardado(tmp_path)
    assert "pieza.py" in guardados, (
        "lo aprobado no se guardo en la historia; la siguiente ronda o un deshacer "
        "puede llevarselo"
    )
    assert "otro.py" not in guardados, (
        "se guardo tambien algo que el equipo no aprobo"
    )


def test_si_el_guardia_frena_no_se_pierde_nada(tmp_path):
    """Si el guardia de guardado frena, el trabajo no se pierde: sigue en el disco o queda apartado."""
    _repo(tmp_path)
    hook = tmp_path / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    try:
        os.chmod(str(hook), 0o755)
    except OSError:
        pass
    (tmp_path / "pieza.py").write_text("y = 2\n", encoding="utf-8")

    ok, msg = candado_equipo.guardar_en_la_historia(
        str(tmp_path), ["pieza.py"], "equipo aprobado"
    )

    assert ok is False, "el guardia freno y la funcion dijo que si guardo"
    en_el_disco = tmp_path / "pieza.py"
    apartado = (
        tmp_path
        / "memoria"
        / "trabajos_sin_revisar"
        / "pieza.py.FRENADO_POR_EL_GUARDIA"
    )
    contenido = ""
    if en_el_disco.exists():
        contenido = en_el_disco.read_text(encoding="utf-8")
    elif apartado.exists():
        contenido = apartado.read_text(encoding="utf-8")
    assert "y = 2" in contenido, (
        "el guardia freno y el trabajo desaparecio: ni en el disco ni apartado"
    )


def test_sin_archivos_no_guarda_nada(tmp_path):
    """Sin archivos aprobados no hay nada que guardar: se dice que no."""
    _repo(tmp_path)

    ok, msg = candado_equipo.guardar_en_la_historia(str(tmp_path), [], "nada")

    assert ok is False, "sin archivos aprobados no se puede decir que se guardo"
