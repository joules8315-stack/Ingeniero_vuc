# -*- coding: utf-8 -*-
"""vigias/test_vigia_no_se_pisa_el_trabajo_apartado.py — LA COPIA APARTADA NO SE PISA.

Julio, 2026-09-20.

EL AGUJERO QUE TAPA:
  arnes/candado_equipo.py, funcion volver_atras(), aparta la pieza a
  memoria/trabajos_sin_revisar/<nombre>.FRENADO_POR_EL_GUARDIA antes de deshacer el cambio.
  El nombre del destino es FIJO: solo depende del basename de la pieza. Si volver_atras se
  llama DOS VECES SEGUIDAS sobre la misma pieza con contenidos distintos, la segunda copia
  escribe ENCIMA de la primera y el trabajo aprobado anterior se pierde para siempre.

LO QUE EXIGE ESTA VIGIA:
  Tras dos llamadas seguidas a volver_atras sobre la misma pieza con contenidos distintos,
  tienen que quedar LAS DOS copias apartadas en memoria/trabajos_sin_revisar, cada una con
  su contenido. Si solo queda una, la vigia FRENA.

COMO SE MONTA (determinista, sin red, sin tocar el repo de verdad):
  - Carpeta temporal como raiz.
  - Se monkeypatchea subprocess.run DENTRO de arnes.candado_equipo para que las llamadas a
    git no salgan del proceso: 'git cat-file -e HEAD:<ruta>' devuelve 1 (la pieza es NUEVA)
    y 'git rm --cached' devuelve 0. Asi se ejercita la rama 'apartada (nueva)', que es la que
    usa os.replace y por tanto la que pisa.
  - Se monkeypatchea cuerpo.fallos.apuntar para que la libreta de fallos no escriba en la
    memoria de verdad (memoria de fallos: una prueba NUNCA escribe en la memoria real).

NO TOCA NINGUN OTRO ARCHIVO. Solo lee arnes/candado_equipo.py y escribe en tmp_path.
"""
import os
import sys
import types

import pytest


# ---------------------------------------------------------------------------
# Localizacion de la raiz del proyecto y de arnes/candado_equipo.py
# ---------------------------------------------------------------------------
def _raiz_proyecto():
    """Sube desde este archivo hasta la carpeta que contiene 'arnes'."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    candidato = os.path.dirname(aqui)  # vigias/ -> raiz
    if os.path.isdir(os.path.join(candidato, "arnes")):
        return candidato
    # por si el archivo se mueve de sitio
    actual = aqui
    for _ in range(6):
        actual = os.path.dirname(actual)
        if os.path.isdir(os.path.join(actual, "arnes")):
            return actual
    raise RuntimeError("no encuentro la carpeta 'arnes' subiendo desde %s" % aqui)


def _cargar_candado_equipo():
    """Importa arnes.candado_equipo con la raiz del proyecto en sys.path."""
    raiz = _raiz_proyecto()
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    import importlib
    return importlib.import_module("arnes.candado_equipo")


# ---------------------------------------------------------------------------
# Doblador de subprocess.run: las llamadas a git no salen del proceso
# ---------------------------------------------------------------------------
class _ResultadoFalso(object):
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _hacer_run_falso(registro):
    """Devuelve un subprocess.run de mentira.

    - 'git cat-file -e HEAD:<ruta>'  -> returncode 1  (la pieza NO estaba en HEAD: es nueva)
    - 'git rm --cached ...'          -> returncode 0  (se saca del indice, no hace nada real)
    - cualquier otra llamada a git   -> returncode 0
    Todo queda apuntado en 'registro' para poder afirmar que se llamo a git.
    """
    def _run_falso(cmd, *args, **kwargs):
        registro.append(list(cmd) if isinstance(cmd, (list, tuple)) else [cmd])
        if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 and cmd[0] == "git":
            if cmd[1] == "cat-file":
                return _ResultadoFalso(returncode=1)
            if cmd[1] == "rm":
                return _ResultadoFalso(returncode=0)
            if cmd[1] == "restore":
                return _ResultadoFalso(returncode=0)
        return _ResultadoFalso(returncode=0)
    return _run_falso


# ---------------------------------------------------------------------------
# Doblador de cuerpo.fallos.apuntar: la prueba NO escribe en la memoria real
# ---------------------------------------------------------------------------
@pytest.fixture()
def sin_tocar_la_memoria_de_fallos(monkeypatch):
    """Sustituye cuerpo.fallos.apuntar por un doble que solo apunta en memoria."""
    apuntes = []

    def _apuntar_falso(*args, **kwargs):
        apuntes.append({"args": args, "kwargs": kwargs})
        return None

    try:
        import cuerpo.fallos as fallos_mod
    except Exception:
        # Si cuerpo.fallos no se puede importar, se crea un modulo de pega para que
        # el 'from cuerpo import fallos' de volver_atras no falle.
        import importlib
        try:
            cuerpo_mod = importlib.import_module("cuerpo")
        except Exception:
            cuerpo_mod = types.ModuleType("cuerpo")
            sys.modules["cuerpo"] = cuerpo_mod
        fallos_mod = types.ModuleType("cuerpo.fallos")
        fallos_mod.apuntar = _apuntar_falso
        sys.modules["cuerpo.fallos"] = fallos_mod
        setattr(cuerpo_mod, "fallos", fallos_mod)
        yield apuntes
        return

    monkeypatch.setattr(fallos_mod, "apuntar", _apuntar_falso, raising=False)
    yield apuntes


# ---------------------------------------------------------------------------
# Utilidad: preparar una pieza nueva dentro de la raiz temporal
# ---------------------------------------------------------------------------
def _poner_pieza(raiz, nombre_relativo, contenido):
    ruta = os.path.join(str(raiz), nombre_relativo)
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def _copias_apartadas(raiz):
    """Lista de (nombre, contenido) de todo lo que hay en trabajos_sin_revisar."""
    carpeta = os.path.join(str(raiz), "memoria", "trabajos_sin_revisar")
    if not os.path.isdir(carpeta):
        return []
    salida = []
    for nombre in sorted(os.listdir(carpeta)):
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception:
            contenido = None
        salida.append((nombre, contenido))
    return salida


# ---------------------------------------------------------------------------
# LA VIGIA
# ---------------------------------------------------------------------------
def test_dos_llamadas_seguidas_apartan_las_dos_copias(tmp_path, monkeypatch, sin_tocar_la_memoria_de_fallos):
    """Dos volver_atras seguidos sobre la misma pieza con contenidos distintos:
    tienen que quedar LAS DOS copias apartadas, no una sola.
    """
    candado = _cargar_candado_equipo()

    registro_git = []
    monkeypatch.setattr(candado.subprocess, "run", _hacer_run_falso(registro_git), raising=True)

    raiz = tmp_path
    pieza = "cuerpo/pieza_de_prueba.py"

    # --- Primera vuelta: contenido A ---
    _poner_pieza(raiz, pieza, "# contenido A aprobado\nVALOR = 'A'\n")
    anotaciones_1 = candado.volver_atras(str(raiz), [pieza], "motivo de la primera vuelta")

    copias_tras_1 = _copias_apartadas(raiz)
    assert len(copias_tras_1) == 1, (
        "tras la primera llamada deberia haber UNA copia apartada, hay %d: %r"
        % (len(copias_tras_1), [c[0] for c in copias_tras_1])
    )
    assert "contenido A" in (copias_tras_1[0][1] or ""), (
        "la copia apartada de la primera vuelta no lleva el contenido A: %r" % (copias_tras_1[0][1],)
    )

    # --- Segunda vuelta: contenido B, misma pieza ---
    _poner_pieza(raiz, pieza, "# contenido B aprobado\nVALOR = 'B'\n")
    anotaciones_2 = candado.volver_atras(str(raiz), [pieza], "motivo de la segunda vuelta")

    copias_tras_2 = _copias_apartadas(raiz)

    # LA AFIRMACION QUE MANDA: no se pisa el trabajo apartado anterior.
    assert len(copias_tras_2) == 2, (
        "LA SEGUNDA LLAMADA PISO LA PRIMERA: deberia haber DOS copias apartadas "
        "(contenido A y contenido B) y hay %d: %r"
        % (len(copias_tras_2), [c[0] for c in copias_tras_2])
    )

    contenidos = [c[1] or "" for c in copias_tras_2]
    assert any("contenido A" in c for c in contenidos), (
        "se perdio el trabajo aprobado anterior (contenido A): %r" % (contenidos,)
    )
    assert any("contenido B" in c for c in contenidos), (
        "no se aparto el trabajo de la segunda vuelta (contenido B): %r" % (contenidos,)
    )

    # Las dos copias tienen que ser archivos distintos, no el mismo nombre repetido.
    nombres = [c[0] for c in copias_tras_2]
    assert len(set(nombres)) == 2, (
        "las dos copias comparten nombre, luego una piso a la otra: %r" % (nombres,)
    )

    # Y las dos llevan el final que exige el contrato.
    for nombre in nombres:
        assert nombre.endswith(".FRENADO_POR_EL_GUARDIA"), (
            "la copia apartada no lleva el final .FRENADO_POR_EL_GUARDIA: %r" % (nombre,)
        )

    # volver_atras nunca lanza y devuelve anotaciones.
    assert isinstance(anotaciones_1, list) and anotaciones_1, "la primera vuelta no anoto nada"
    assert isinstance(anotaciones_2, list) and anotaciones_2, "la segunda vuelta no anoto nada"

    # Se llamo a git (aunque doblado): la vigia no se cree el resultado sin ver el intento.
    assert any(c and c[0] == "git" for c in registro_git), (
        "no se llamo a git en ningun momento: el montaje no es real"
    )


def test_la_pieza_no_se_queda_en_su_sitio(tmp_path, monkeypatch, sin_tocar_la_memoria_de_fallos):
    """Complemento: tras apartar, la pieza original ya no esta en su sitio (se movio, no se copio).
    Si esto falla, la vigia de arriba podria estar pasando por accidente.
    """
    candado = _cargar_candado_equipo()

    registro_git = []
    monkeypatch.setattr(candado.subprocess, "run", _hacer_run_falso(registro_git), raising=True)

    raiz = tmp_path
    pieza = "cuerpo/otra_pieza.py"
    _poner_pieza(raiz, pieza, "# contenido unico\n")

    candado.volver_atras(str(raiz), [pieza], "motivo")

    assert not os.path.exists(os.path.join(str(raiz), pieza)), (
        "la pieza nueva deberia haberse MOVIDO a trabajos_sin_revisar, no quedarse en su sitio"
    )
    copias = _copias_apartadas(raiz)
    assert len(copias) == 1, "deberia haber exactamente una copia apartada: %r" % ([c[0] for c in copias],)
    assert "contenido unico" in (copias[0][1] or ""), "la copia apartada no lleva el contenido"


if __name__ == "__main__":
    sys.exit(pytest.main([os.path.abspath(__file__), "-q"]))
