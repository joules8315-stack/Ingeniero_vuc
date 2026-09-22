# -*- coding: utf-8 -*-
"""vigias/test_vigia_una_prueba_que_espera_su_arreglo_no_frena_el_guardado.py

VIGIA de arnes/guardia_de_guardado.py::_vigias

Julio, 2026-09-20: el pit dejo dos pruebas rojas esperando su arreglo, el guardia
freno TODOS los guardados siguientes y la maquina se quedo trabada sin poder avanzar
ni una tarea.

Lo que hoy hace _vigias:
  - si TODAS las rojas son nuevas (no estan en HEAD) -> deja pasar con aviso
  - si alguna roja ya estaba guardada -> FRENA

Lo que falta: una prueba roja que YA ESTA GUARDADA pero que la propia maquina
declaro como la vigia de una tarea suya todavia sin terminar (memoria/ORDENES.json)
tampoco debe frenar: esa prueba nacio roja a proposito y esta esperando su arreglo.

Tres casos:
  1. roja guardada que NO es de ninguna tarea pendiente -> FRENA
  2. roja guardada que SI es la vigia de una tarea cuyo estado no es 'hecha' ->
     deja pasar con aviso
  3. todo verde -> deja pasar

Se usa monkeypatch sobre subprocess.run DENTRO de arnes/guardia_de_guardado.py
para dar la salida de pytest y la de git sin ejecutarlos, y una lista de ordenes de
mentira en una carpeta temporal.
"""
import importlib.util
import json
import os
import subprocess
import sys

import pytest


AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_GUARDIA = os.path.join(AQUI, "arnes", "guardia_de_guardado.py")


def _cargar_guardia():
    """Carga arnes/guardia_de_guardado.py como modulo, sin depender del paquete."""
    spec = importlib.util.spec_from_file_location(
        "guardia_de_guardado_bajo_prueba", RUTA_GUARDIA)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _preparar_raiz(tmp_path, ordenes):
    """Crea una raiz de mentira con vigias/ y memoria/ORDENES.json.

    Devuelve la ruta de la raiz. La lista de ordenes se escribe tal cual en
    memoria/ORDENES.json para que _vigias la pueda leer.
    """
    raiz = tmp_path / "raiz"
    (raiz / "vigias").mkdir(parents=True)
    (raiz / "memoria").mkdir(parents=True)
    (raiz / "vigias" / "test_roja.py").write_text(
        "def test_roja():\n    assert False\n", encoding="utf-8")
    (raiz / "memoria" / "ORDENES.json").write_text(
        json.dumps(ordenes, ensure_ascii=False), encoding="utf-8")
    return str(raiz)


def _fake_run_factory(salida_pytest, returncode_pytest, guardados_en_head):
    """Devuelve un subprocess.run de mentira.

    - Cuando lo llaman para pytest (contiene '-m' y 'pytest'), devuelve la salida
      y el returncode dados.
    - Cuando lo llaman para 'git cat-file -e HEAD:<archivo>', devuelve returncode 0
      si el archivo esta en guardados_en_head, y 1 si no.
    - Cualquier otra llamada devuelve algo inofensivo.
    """
    def _fake_run(cmd, *args, **kwargs):
        if isinstance(cmd, (list, tuple)) and "pytest" in cmd:
            return subprocess.CompletedProcess(
                args=cmd, returncode=returncode_pytest,
                stdout=salida_pytest, stderr="")
        if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 and cmd[0] == "git" \
                and cmd[1] == "cat-file" and cmd[2] == "-e":
            ref = cmd[3] if len(cmd) > 3 else ""
            archivo = ref.split("HEAD:", 1)[-1] if "HEAD:" in ref else ref
            archivo = archivo.replace("\\", "/")
            if archivo in guardados_en_head:
                return subprocess.CompletedProcess(
                    args=cmd, returncode=0, stdout="", stderr="")
            return subprocess.CompletedProcess(
                args=cmd, returncode=1, stdout="", stderr="")
        return subprocess.CompletedProcess(
            args=cmd, returncode=0, stdout="", stderr="")
    return _fake_run


def _parchear(monkeypatch, modulo, salida_pytest, returncode_pytest,
              guardados_en_head):
    """Parchea subprocess.run DENTRO del modulo del guardia.

    Tambien neutraliza vecinas.elegir para que no decida por nosotros: queremos
    que _vigias corra pytest sobre vigias/ y vea lo que le damos.
    """
    fake = _fake_run_factory(salida_pytest, returncode_pytest, guardados_en_head)
    monkeypatch.setattr(modulo.subprocess, "run", fake)

    # vecinas.elegir puede devolver [] y saltarse pytest: lo forzamos a None para
    # que _vigias use el objetivo por defecto ['vigias/'].
    try:
        import vecinas as _vecinas  # noqa: F401
        monkeypatch.setattr(_vecinas, "elegir", lambda raiz: None)
    except Exception:
        # Si vecinas no esta disponible, _vigias ya cae en el except y usa
        # ['vigias/'] por defecto. No es un fallo de la vigia.
        pass


# ---------------------------------------------------------------------------
# CASO 1: roja guardada que NO es de ninguna tarea pendiente -> FRENA
# ---------------------------------------------------------------------------
def test_roja_guardada_sin_tarea_pendiente_frena(tmp_path, monkeypatch):
    modulo = _cargar_guardia()
    ordenes = []  # ninguna tarea pendiente declara esta prueba
    raiz = _preparar_raiz(tmp_path, ordenes)

    salida = (
        "F                                                                        [100%]\n"
        "FAILED vigias/test_roja.py::test_roja - AssertionError: assert False\n"
        "1 failed in 0.01s\n"
    )
    _parchear(monkeypatch, modulo,
              salida_pytest=salida, returncode_pytest=1,
              guardados_en_head={"vigias/test_roja.py"})

    paso, mensaje = modulo._vigias(raiz)
    assert paso is False, (
        "una roja guardada que no es de ninguna tarea pendiente debe FRENAR; "
        "mensaje: %r" % mensaje)


# ---------------------------------------------------------------------------
# CASO 2: roja guardada que SI es la vigia de una tarea cuyo estado no es
# 'hecha' -> deja pasar con aviso
# ---------------------------------------------------------------------------
def test_roja_guardada_que_espera_su_arreglo_deja_pasar(tmp_path, monkeypatch):
    modulo = _cargar_guardia()
    ordenes = [
        {
            "id": "tarea-1",
            "estado": "en_curso",
            "vigia": "vigias/test_roja.py",
        }
    ]
    raiz = _preparar_raiz(tmp_path, ordenes)

    salida = (
        "F                                                                        [100%]\n"
        "FAILED vigias/test_roja.py::test_roja - AssertionError: assert False\n"
        "1 failed in 0.01s\n"
    )
    _parchear(monkeypatch, modulo,
              salida_pytest=salida, returncode_pytest=1,
              guardados_en_head={"vigias/test_roja.py"})

    paso, mensaje = modulo._vigias(raiz)
    assert paso is True, (
        "una roja guardada que es la vigia de una tarea pendiente debe DEJAR "
        "PASAR con aviso; mensaje: %r" % mensaje)
    assert "espera" in mensaje.lower() or "arreglo" in mensaje.lower() \
        or "tarea" in mensaje.lower(), (
        "el aviso debe decir que la prueba espera su arreglo o que es de una "
        "tarea pendiente; mensaje: %r" % mensaje)


def test_roja_guardada_que_la_propia_tarea_edita_frena(tmp_path, monkeypatch):
    monkeypatch.setenv('INGENIERO_ETIQUETA', 'tarea-1')
    modulo = _cargar_guardia()
    ordenes = [
        {
            "id": "tarea-1",
            "estado": "en_curso",
            "vigia": "vigias/test_roja.py",
            "pieza": "vigias/test_roja.py",
        }
    ]
    raiz = _preparar_raiz(tmp_path, ordenes)

    salida = (
        "F                                                                        [100%]\n"
        "FAILED vigias/test_roja.py::test_roja - AssertionError: assert False\n"
        "1 failed in 0.01s\n"
    )
    _parchear(monkeypatch, modulo,
              salida_pytest=salida, returncode_pytest=1,
              guardados_en_head={"vigias/test_roja.py"})

    paso, mensaje = modulo._vigias(raiz)
    assert paso is False, (
        "una roja guardada que la propia tarea edita debe FRENAR; "
        "mensaje: %r" % mensaje)


def test_roja_de_otra_tarea_que_la_corrige_deja_pasar(tmp_path, monkeypatch):
    monkeypatch.setenv('INGENIERO_ETIQUETA', 'tarea-2')
    modulo = _cargar_guardia()
    ordenes = [
        {
            "id": "tarea-1",
            "estado": "en_curso",
            "vigia": "vigias/test_roja.py",
            "pieza": "vigias/test_roja.py",
        }
    ]
    raiz = _preparar_raiz(tmp_path, ordenes)

    salida = (
        "F                                                                        [100%]\n"
        "FAILED vigias/test_roja.py::test_roja - AssertionError: assert False\n"
        "1 failed in 0.01s\n"
    )
    _parchear(monkeypatch, modulo,
              salida_pytest=salida, returncode_pytest=1,
              guardados_en_head={"vigias/test_roja.py"})

    paso, mensaje = modulo._vigias(raiz)
    assert paso is True, (
        "una roja guardada que la propia tarea edita debe FRENAR; "
        "mensaje: %r" % mensaje)


def test_roja_que_la_propia_tarea_declara_que_queda_roja_deja_pasar(tmp_path, monkeypatch):
    monkeypatch.setenv('INGENIERO_ETIQUETA', 'tarea-1')
    modulo = _cargar_guardia()
    ordenes = [
        {
            "id": "tarea-1",
            "estado": "en_curso",
            "vigia": "vigias/test_roja.py",
            "pieza": "vigias/test_roja.py",
            "queda_roja": True,
        }
    ]
    raiz = _preparar_raiz(tmp_path, ordenes)

    salida = (
        "F                                                                        [100%]\n"
        "FAILED vigias/test_roja.py::test_roja - AssertionError: assert False\n"
        "1 failed in 0.01s\n"
    )
    _parchear(monkeypatch, modulo,
              salida_pytest=salida, returncode_pytest=1,
              guardados_en_head={"vigias/test_roja.py"})

    paso, mensaje = modulo._vigias(raiz)
    assert paso is True, (
        "una roja que la propia tarea declara que queda roja debe DEJAR PASAR; "
        "mensaje: %r" % mensaje)


# ---------------------------------------------------------------------------
# CASO 3: todo verde -> deja pasar
# ---------------------------------------------------------------------------
def test_todo_verde_deja_pasar(tmp_path, monkeypatch):
    modulo = _cargar_guardia()
    ordenes = []
    raiz = _preparar_raiz(tmp_path, ordenes)

    salida = "1 passed in 0.01s\n"
    _parchear(monkeypatch, modulo,
              salida_pytest=salida, returncode_pytest=0,
              guardados_en_head={"vigias/test_roja.py"})

    paso, mensaje = modulo._vigias(raiz)
    assert paso is True, (
        "todo verde debe DEJAR PASAR; mensaje: %r" % mensaje)
