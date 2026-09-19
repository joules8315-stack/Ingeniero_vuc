"""Vigia de arnes/vecinas.py (A-37).

Cada prueba arma un repo git REAL en tmp_path (git init -q, git config
user.email/user.name, subprocess), con carpeta vigias/ y archivos reales,
hace un commit inicial y luego cambia archivos. Nada de red, nada de
simuladores de biblioteca: git de verdad, archivos de verdad.

Se importa vecinas agregando la carpeta arnes (os.path.join(AQUI, 'arnes')
con AQUI = carpeta padre de vigias) a sys.path.

Casos cubiertos:
  (1) cambiar cuerpo/pieza_a.py cuando vigias/test_a.py nombra pieza_a y
      vigias/test_b.py no -> elegir == ['vigias/test_a.py']
  (2) cambiar solo un README.md -> []
  (3) cambiar vigias/conftest.py -> None
  (4) cambiar cuerpo/huerfana.py que ninguna vigia nombra -> None
  (5) con INGENIERO_BATERIA_COMPLETA=1 -> None
  (6) SABOTAJE: si elegir devolviera [] para un cambio de codigo con
      vecinas, la prueba (1) lo caza por su assert exacto.
"""

import os
import subprocess
import sys

import pytest


AQUI = os.path.dirname(os.path.abspath(__file__))
ARNES = os.path.join(os.path.dirname(AQUI), "arnes")
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import vecinas  # noqa: E402  (import tras ajustar sys.path)


# ---------------------------------------------------------------------------
# Utilidades: repo git real en tmp_path
# ---------------------------------------------------------------------------


def _git(repo, *args):
    """Ejecuta git en el repo con entorno controlado (sin red, sin prompts)."""
    entorno = dict(os.environ)
    entorno["GIT_AUTHOR_NAME"] = "Vigia"
    entorno["GIT_AUTHOR_EMAIL"] = "vigia@local"
    entorno["GIT_COMMITTER_NAME"] = "Vigia"
    entorno["GIT_COMMITTER_EMAIL"] = "vigia@local"
    entorno["GIT_TERMINAL_PROMPT"] = "0"
    entorno["GIT_CONFIG_NOSYSTEM"] = "1"
    return subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        check=True,
        capture_output=True,
        text=True,
        env=entorno,
    )


def _escribir(repo, relativo, contenido):
    ruta = os.path.join(str(repo), relativo)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


def _repo_con_commit(tmp_path, archivos):
    """Crea un repo git real, escribe archivos, hace commit inicial.

    Devuelve la ruta del repo (str).
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "vigia@local")
    _git(repo, "config", "user.name", "Vigia")
    for relativo, contenido in archivos.items():
        _escribir(repo, relativo, contenido)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "inicial")
    return str(repo)


def _cambiar(repo, relativo, contenido):
    """Modifica un archivo ya existente (queda como cambio sin commitear)."""
    _escribir(repo, relativo, contenido)


# ---------------------------------------------------------------------------
# Caso (1): cambio de codigo con vecina que lo nombra
# ---------------------------------------------------------------------------


def test_cambio_de_pieza_elige_la_vigia_que_la_nombra(tmp_path):
    repo = _repo_con_commit(
        tmp_path,
        {
            "cuerpo/pieza_a.py": "VALOR = 1\n",
            "vigias/test_a.py": (
                "def test_algo():\n"
                "    # esta vigia habla de pieza_a\n"
                "    assert True\n"
            ),
            "vigias/test_b.py": (
                "def test_otra():\n"
                "    assert True\n"
            ),
            "README.md": "hola\n",
        },
    )
    _cambiar(repo, "cuerpo/pieza_a.py", "VALOR = 2\n")

    elegidas = vecinas.elegir(repo)

    assert elegidas == ["vigias/test_a.py"]


# ---------------------------------------------------------------------------
# Caso (2): cambio que no es codigo -> lista vacia
# ---------------------------------------------------------------------------


def test_cambio_de_readme_no_elige_nada(tmp_path):
    repo = _repo_con_commit(
        tmp_path,
        {
            "cuerpo/pieza_a.py": "VALOR = 1\n",
            "vigias/test_a.py": (
                "def test_algo():\n"
                "    # esta vigia habla de pieza_a\n"
                "    assert True\n"
            ),
            "README.md": "hola\n",
        },
    )
    _cambiar(repo, "README.md", "hola mundo\n")

    elegidas = vecinas.elegir(repo)

    assert elegidas == []


# ---------------------------------------------------------------------------
# Caso (3): cambio en vigias/conftest.py -> None (no se puede decidir)
# ---------------------------------------------------------------------------


def test_cambio_de_conftest_devuelve_none(tmp_path):
    repo = _repo_con_commit(
        tmp_path,
        {
            "cuerpo/pieza_a.py": "VALOR = 1\n",
            "vigias/conftest.py": "# conftest\n",
            "vigias/test_a.py": (
                "def test_algo():\n"
                "    # esta vigia habla de pieza_a\n"
                "    assert True\n"
            ),
        },
    )
    _cambiar(repo, "vigias/conftest.py", "# conftest cambiado\n")

    elegidas = vecinas.elegir(repo)

    assert elegidas is None


# ---------------------------------------------------------------------------
# Caso (4): cambio de codigo que ninguna vigia nombra -> None
# ---------------------------------------------------------------------------


def test_cambio_de_huerfana_devuelve_none(tmp_path):
    repo = _repo_con_commit(
        tmp_path,
        {
            "cuerpo/pieza_a.py": "VALOR = 1\n",
            "cuerpo/huerfana.py": "OTRO = 1\n",
            "vigias/test_a.py": (
                "def test_algo():\n"
                "    # esta vigia habla de pieza_a\n"
                "    assert True\n"
            ),
        },
    )
    _cambiar(repo, "cuerpo/huerfana.py", "OTRO = 2\n")

    elegidas = vecinas.elegir(repo)

    assert elegidas is None


# ---------------------------------------------------------------------------
# Caso (5): bateria completa -> None (no se elige, se corre todo)
# ---------------------------------------------------------------------------


def test_bateria_completa_devuelve_none(tmp_path, monkeypatch):
    repo = _repo_con_commit(
        tmp_path,
        {
            "cuerpo/pieza_a.py": "VALOR = 1\n",
            "vigias/test_a.py": (
                "def test_algo():\n"
                "    # esta vigia habla de pieza_a\n"
                "    assert True\n"
            ),
        },
    )
    _cambiar(repo, "cuerpo/pieza_a.py", "VALOR = 2\n")
    monkeypatch.setenv("INGENIERO_BATERIA_COMPLETA", "1")

    elegidas = vecinas.elegir(repo)

    assert elegidas is None


# ---------------------------------------------------------------------------
# Caso (6): SABOTAJE — si elegir devolviera [] para un cambio de codigo con
# vecinas, la prueba (1) lo caza por su assert exacto. Aqui se deja constancia
# explicita: un cambio de codigo con vecina NUNCA puede dar lista vacia.
# ---------------------------------------------------------------------------


def test_sabotaje_lista_vacia_no_cuela(tmp_path):
    repo = _repo_con_commit(
        tmp_path,
        {
            "cuerpo/pieza_a.py": "VALOR = 1\n",
            "vigias/test_a.py": (
                "def test_algo():\n"
                "    # esta vigia habla de pieza_a\n"
                "    assert True\n"
            ),
            "vigias/test_b.py": (
                "def test_otra():\n"
                "    assert True\n"
            ),
        },
    )
    _cambiar(repo, "cuerpo/pieza_a.py", "VALOR = 2\n")

    elegidas = vecinas.elegir(repo)

    # Si alguien sabotea elegir para que devuelva [] ante un cambio de codigo
    # con vecinas, esta linea se pone roja. La prueba (1) ya lo caza con su
    # assert exacto; aqui se deja el candado explicito.
    assert elegidas != []
    assert elegidas == ["vigias/test_a.py"]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
