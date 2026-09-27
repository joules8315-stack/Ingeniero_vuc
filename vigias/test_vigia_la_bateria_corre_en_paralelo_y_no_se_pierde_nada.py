# -*- coding: utf-8 -*-
"""vigias/test_vigia_la_bateria_corre_en_paralelo_y_no_se_pierde_nada.py

VIGIA NUEVA, NACIDA ROJA: la pieza que prueba todavia no existe.

De que fallo nace (medido hoy 2026-09-27):
  - el guardia corre las 257 pruebas del proyecto en FILA, con un tope de 900 segundos;
  - hoy tardan mas de 12 minutos;
  - un trabajo ya aprobado se perdio porque la bateria no termino en 15 minutos;
  - es el fallo mas repetido de la herramienta: 95 veces.

La pieza que hay que probar se llamara arnes/bateria_en_paralelo.py y tendra dos funciones:
  - repartir(archivos, grupos): reparto circular y equilibrado, sin perder ni repetir;
  - correr(raiz, objetivo, procesos=4, tope=600): corre cada grupo con pytest en su propio
    proceso a la vez y devuelve un objeto con returncode, stdout y stderr, igual que
    subprocess.run.

Mientras la pieza no exista, esta vigia falla con un mensaje en palabras simples.
"""

import importlib.util
import os
import subprocess
import sys

import pytest


# ---------------------------------------------------------------------------
# CARGA DE LA PIEZA
# ---------------------------------------------------------------------------
# La raiz del repo se calcula desde este archivo: vigias/ -> raiz.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PIEZA = os.path.join(RAIZ, "arnes", "bateria_en_paralelo.py")


def _cargar_pieza():
    """Carga arnes/bateria_en_paralelo.py por ruta, sin depender del sys.path."""
    if not os.path.isfile(RUTA_PIEZA):
        pytest.fail(
            "Falta la pieza arnes/bateria_en_paralelo.py: sin ella la bateria sigue "
            "corriendo en fila y se pierde el trabajo cuando no termina a tiempo."
        )
    especificacion = importlib.util.spec_from_file_location(
        "bateria_en_paralelo", RUTA_PIEZA
    )
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


@pytest.fixture()
def pieza():
    """Devuelve el modulo de la pieza, o falla con un mensaje claro si no existe."""
    return _cargar_pieza()


# ---------------------------------------------------------------------------
# DOBLE DE subprocess.run
# ---------------------------------------------------------------------------
def _doble_run(registro, por_grupo=None, lanzar_timeout=False):
    """Fabrica un doble de subprocess.run que apunta cada llamada.

    registro: lista donde se anota cada llamada (comando y kwargs).
    por_grupo: funcion que recibe el indice de la llamada y devuelve el returncode.
    lanzar_timeout: si es True, el doble lanza subprocess.TimeoutExpired.
    """

    def _run(comando, *args, **kwargs):
        indice = len(registro)
        registro.append({"comando": comando, "args": args, "kwargs": kwargs})
        if lanzar_timeout:
            raise subprocess.TimeoutExpired(cmd=comando, timeout=kwargs.get("timeout", 0))
        if por_grupo is None:
            codigo = 0
        else:
            codigo = por_grupo(indice)
        salida = ""
        if codigo == 1:
            salida = "FAILED vigias/test_que_falla.py::test_rojo\n"
        return subprocess.CompletedProcess(
            args=comando, returncode=codigo, stdout=salida, stderr=""
        )

    return _run


# ---------------------------------------------------------------------------
# CASO 1 — el reparto no pierde ni repite archivos
# ---------------------------------------------------------------------------
def test_el_reparto_no_pierde_ni_repite_archivos(pieza):
    archivos = ["test_%02d.py" % i for i in range(10)]
    grupos = pieza.repartir(archivos, 3)

    assert len(grupos) == 3, "con tres grupos tienen que salir tres listas"
    for g in grupos:
        assert g, "ningun grupo puede quedar vacio con diez archivos y tres grupos"

    union = sorted(a for g in grupos for a in g)
    assert union == sorted(archivos), "el reparto no puede perder ni repetir archivos"


# ---------------------------------------------------------------------------
# CASO 2 — con un solo grupo va todo junto
# ---------------------------------------------------------------------------
def test_con_un_solo_grupo_va_todo_junto(pieza):
    archivos = ["test_a.py", "test_b.py", "test_c.py"]

    con_uno = pieza.repartir(archivos, 1)
    assert len(con_uno) == 1, "con grupos=1 tiene que salir una sola lista"
    assert sorted(con_uno[0]) == sorted(archivos), "con grupos=1 va todo junto"

    con_cero = pieza.repartir(archivos, 0)
    assert len(con_cero) == 1, "con grupos=0 tiene que salir una sola lista"
    assert sorted(con_cero[0]) == sorted(archivos), "con grupos=0 va todo junto"


# ---------------------------------------------------------------------------
# CASO 3 — cada grupo corre en su proceso
# ---------------------------------------------------------------------------
def test_cada_grupo_corre_en_su_proceso(pieza, monkeypatch):
    registro = []
    monkeypatch.setattr(pieza.subprocess, "run", _doble_run(registro))

    archivos = ["test_a.py", "test_b.py", "test_c.py", "test_d.py"]
    resultado = pieza.correr(RAIZ, archivos, procesos=4, tope=600)

    assert len(registro) == 4, "con cuatro archivos y cuatro procesos tienen que ser cuatro llamadas"
    assert resultado.returncode == 0, "si todos los grupos salen en verde, el resultado es 0"


# ---------------------------------------------------------------------------
# CASO 4 — si un grupo sale rojo, el resultado sale rojo
# ---------------------------------------------------------------------------
def test_si_un_grupo_sale_rojo_el_resultado_sale_rojo(pieza, monkeypatch):
    registro = []

    def por_grupo(indice):
        return 1 if indice == 0 else 0

    monkeypatch.setattr(pieza.subprocess, "run", _doble_run(registro, por_grupo=por_grupo))

    archivos = ["test_a.py", "test_b.py", "test_c.py", "test_d.py"]
    resultado = pieza.correr(RAIZ, archivos, procesos=4, tope=600)

    assert resultado.returncode == 1, "un grupo rojo tiene que poner el resultado en rojo"
    assert "FAILED" in resultado.stdout, "la salida del grupo rojo tiene que aparecer en el stdout"


# ---------------------------------------------------------------------------
# CASO 5 — si un grupo se pasa del tope, no revienta
# ---------------------------------------------------------------------------
def test_si_un_grupo_se_pasa_del_tope_no_revienta(pieza, monkeypatch):
    registro = []
    monkeypatch.setattr(
        pieza.subprocess, "run", _doble_run(registro, lanzar_timeout=True)
    )

    archivos = ["test_a.py", "test_b.py", "test_c.py", "test_d.py"]
    resultado = pieza.correr(RAIZ, archivos, procesos=4, tope=1)

    assert resultado.returncode == 1, "un grupo cortado por tiempo tiene que poner el resultado en rojo"
    ultimo = resultado.stdout.strip().splitlines()[-1]
    assert "tiempo" in ultimo.lower(), "el ultimo renglon tiene que decir que algo se corto por tiempo"


# ---------------------------------------------------------------------------
# CASO 6 — una carpeta se convierte en sus archivos
# ---------------------------------------------------------------------------
def test_una_carpeta_se_convierte_en_sus_archivos(pieza, monkeypatch, tmp_path):
    raiz = tmp_path
    carpeta = raiz / "vigias"
    carpeta.mkdir()
    for nombre in ("test_a.py", "test_b.py", "test_c.py", "test_d.py"):
        (carpeta / nombre).write_text("# prueba\n", encoding="utf-8")

    registro = []
    monkeypatch.setattr(pieza.subprocess, "run", _doble_run(registro))

    pieza.correr(str(raiz), "vigias/", procesos=4, tope=600)

    vistos = set()
    for llamada in registro:
        comando = llamada["comando"]
        if isinstance(comando, (list, tuple)):
            for trozo in comando:
                texto = str(trozo)
                if texto.endswith(".py"):
                    vistos.add(os.path.basename(texto))
        else:
            for trozo in str(comando).split():
                if trozo.endswith(".py"):
                    vistos.add(os.path.basename(trozo))

    for nombre in ("test_a.py", "test_b.py", "test_c.py", "test_d.py"):
        assert nombre in vistos, "la carpeta tiene que convertirse en sus archivos test_*.py"
