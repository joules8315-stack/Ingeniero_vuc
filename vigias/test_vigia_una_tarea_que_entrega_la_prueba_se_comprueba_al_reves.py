"""Vigia: una tarea que ENTREGA LA PRUEBA se comprueba AL REVES.

Motivo del encargo (2026-09-20): hoy la maquina da por fallida toda tarea
cuya prueba no este verde, asi que una tarea cuyo trabajo ES escribir la
prueba se marca fallida aunque haya salido perfecta. Con eso la maquina no
puede seguir sola el metodo de Julio de prueba roja primero.

Lo que se prueba aqui, sobre cuerpo/capataz.py::comprobar_pasos:

  * Si la orden trae entrega_la_prueba == "si", el paso de la vigia se
    comprueba AL REVES: la prueba tiene que EXISTIR y estar ROJA para que
    ese paso este bien. Si ya esta verde, ese paso FALLA, porque una prueba
    que pasa antes del cambio no demuestra nada.
  * Si la orden NO trae ese campo, se sigue comprobando como hoy: la prueba
    tiene que estar VERDE.

Montaje: todo aislado en tmp_path. No se toca memoria/trabajos_del_equipo,
ni vigias/, ni la raiz del proyecto. subprocess.run se sustituye con
monkeypatch DENTRO de cuerpo/capataz.py para no correr pytest de verdad.
"""

import json
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# Utilidades de montaje (todo dentro de tmp_path)
# ---------------------------------------------------------------------------


def _raiz_proyecto():
    """Raiz del proyecto real, para poder importar cuerpo.capataz."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(aqui)


def _importar_capataz():
    raiz = _raiz_proyecto()
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    from cuerpo import capataz  # noqa: E402
    return capataz


def _montar_proyecto_falso(tmp_path, pieza_rel, vigia_rel):
    """Crea un proyecto falso dentro de tmp_path.

    Devuelve (carpeta_proyecto, ruta_pieza, ruta_vigia).
    - La pieza existe en disco.
    - La pieza .py esta nombrada por otro .py del proyecto (para no caer en
      el paso 2b 'pieza_suelta').
    - La vigia existe en disco.
    - Hay un trabajo APROBADO en memoria/trabajos_del_equipo con obrero y
      auditor distintos, para que el paso 1 (ronda) pase.
    """
    carpeta_proyecto = tmp_path / "proyecto"
    carpeta_proyecto.mkdir()

    ruta_pieza = carpeta_proyecto / pieza_rel
    ruta_pieza.parent.mkdir(parents=True, exist_ok=True)
    ruta_pieza.write_text("# pieza de mentira\n", encoding="utf-8")

    # Otro .py que nombra a la pieza por su nombre de modulo, para que el
    # paso 2b no la declare 'suelta'.
    modulo = os.path.splitext(os.path.basename(pieza_rel))[0]
    nombrador = carpeta_proyecto / "nombrador.py"
    nombrador.write_text("import " + modulo + "\n", encoding="utf-8")

    ruta_vigia = carpeta_proyecto / vigia_rel
    ruta_vigia.parent.mkdir(parents=True, exist_ok=True)
    ruta_vigia.write_text("# vigia de mentira\n", encoding="utf-8")

    carpeta_trabajos = carpeta_proyecto / "memoria" / "trabajos_del_equipo"
    carpeta_trabajos.mkdir(parents=True, exist_ok=True)
    base = os.path.splitext(os.path.basename(pieza_rel))[0]
    trabajo = carpeta_trabajos / (base + "_APROBADO.json")
    trabajo.write_text(
        json.dumps({"obrero": "obrero-1", "auditor": "auditor-2"}),
        encoding="utf-8",
    )

    return str(carpeta_proyecto), str(ruta_pieza), str(ruta_vigia)


def _fabricar_subprocess_run(estado):
    """Devuelve un subprocess.run de mentira.

    'estado' es un dict con:
      - 'pytest_rc': codigo de retorno de pytest sobre la vigia.
      - 'git_ls': salida de 'git ls-files' (para el caso de vigia no guardada).
      - 'comando_rc': codigo de retorno del comando de la orden.
      - 'llamadas': lista donde se apunta cada llamada (para el sabotaje).
    """

    class _Resultado:
        def __init__(self, returncode, stdout="", stderr=""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def _run_falso(args, **kwargs):
        estado.setdefault("llamadas", []).append((args, kwargs))
        if isinstance(args, list) and len(args) >= 3 and args[1] == "-m" and args[2] == "pytest":
            return _Resultado(estado.get("pytest_rc", 0))
        if isinstance(args, list) and len(args) >= 2 and args[0] == "git" and args[1] == "ls-files":
            return _Resultado(0, stdout=estado.get("git_ls", ""), stderr="")
        # Comando de la orden (shell=True).
        return _Resultado(estado.get("comando_rc", 0))

    return _run_falso


def _orden(pieza, vigia, entrega_la_prueba=None):
    orden = {
        "pieza": pieza,
        "vigia": vigia,
        "comando": "echo ok",
    }
    if entrega_la_prueba is not None:
        orden["entrega_la_prueba"] = entrega_la_prueba
    return orden


# ---------------------------------------------------------------------------
# Pruebas
# ---------------------------------------------------------------------------


def test_1_sin_entrega_la_prueba_y_vigia_verde_termina_bien(tmp_path, monkeypatch):
    """Como hoy: sin el campo, la prueba VERDE deja la tarea terminada."""
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_x.py", "vigias/test_vigia_x.py"
    )
    monkeypatch.setattr(capataz.os.path, "dirname", capataz.os.path.dirname)
    # Forzamos la carpeta_proyecto que ve comprobar_pasos: la calcula desde
    # __file__ de capataz. Para no tocar el proyecto real, monkeypatcheamos
    # os.path.abspath/dirname solo en lo necesario: mas simple, monkeypatch
    # sobre os.path.dirname no basta. Usamos monkeypatch sobre __file__.
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    estado = {"pytest_rc": 0, "git_ls": vigia, "comando_rc": 0}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia)
    assert capataz.comprobar_pasos(orden) == ""


def test_2_sin_entrega_la_prueba_y_vigia_roja_no_termina(tmp_path, monkeypatch):
    """Como hoy: sin el campo, la prueba ROJA deja la tarea sin terminar."""
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_y.py", "vigias/test_vigia_y.py"
    )
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    # pytest rojo, pero la vigia SI esta guardada en git: no es el caso de
    # 'vigia no guardada', es el caso de 'vigia_verde' fallido.
    estado = {"pytest_rc": 1, "git_ls": vigia, "comando_rc": 0}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia)
    assert capataz.comprobar_pasos(orden) == "vigia_verde"


def test_3_con_entrega_la_prueba_si_y_prueba_roja_termina_bien(tmp_path, monkeypatch):
    """Al reves: con entrega_la_prueba='si', la prueba ROJA deja la tarea bien."""
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_z.py", "vigias/test_vigia_z.py"
    )
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    estado = {"pytest_rc": 1, "git_ls": vigia, "comando_rc": 0}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia, entrega_la_prueba="si")
    assert capataz.comprobar_pasos(orden) == ""


def test_4_con_entrega_la_prueba_si_y_prueba_verde_falla(tmp_path, monkeypatch):
    """Al reves: con entrega_la_prueba='si', la prueba VERDE hace fallar el paso.

    Una prueba que pasa antes del cambio no demuestra nada.
    """
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_w.py", "vigias/test_vigia_w.py"
    )
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    estado = {"pytest_rc": 0, "git_ls": vigia, "comando_rc": 0}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia, entrega_la_prueba="si")
    assert capataz.comprobar_pasos(orden) == "vigia_verde"


def test_5_con_entrega_la_prueba_si_y_prueba_inexistente_falla(tmp_path, monkeypatch):
    """Al reves: con entrega_la_prueba='si', si la prueba NO existe, el paso falla.

    La prueba tiene que existir Y estar roja. Si no existe, no hay prueba
    que demuestre nada.
    """
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_v.py", "vigias/test_vigia_v.py"
    )
    # Borramos la vigia: no existe.
    os.remove(vigia)
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    estado = {"pytest_rc": 1, "git_ls": "", "comando_rc": 0}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia, entrega_la_prueba="si")
    assert capataz.comprobar_pasos(orden) == "vigia_verde"


def test_6_con_entrega_la_prueba_si_y_prueba_verde_no_llama_a_pytest(tmp_path, monkeypatch):
    """Sabotaje: si el codigo NO mira entrega_la_prueba, esta prueba cae.

    Con entrega_la_prueba='si' y la prueba VERDE, el paso debe fallar. Si el
    codigo ignora el campo y se comporta 'como hoy', el paso pasaria y esta
    prueba se pondria roja. Es decir: esta prueba caza al codigo que no
    implementa la comprobacion al reves.
    """
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_u.py", "vigias/test_vigia_u.py"
    )
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    estado = {"pytest_rc": 0, "git_ls": vigia, "comando_rc": 0, "llamadas": []}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia, entrega_la_prueba="si")
    resultado = capataz.comprobar_pasos(orden)

    # El paso tiene que fallar (prueba verde con entrega_la_prueba='si').
    assert resultado == "vigia_verde"
    # Y ademas, el codigo SI tiene que haber mirado la prueba: si no llamo a
    # pytest, es que ni siquiera la comprobo.
    llamo_a_pytest = any(
        isinstance(args, list) and len(args) >= 3 and args[1] == "-m" and args[2] == "pytest"
        for args, _kwargs in estado["llamadas"]
    )
    assert llamo_a_pytest, "el codigo no llego a comprobar la prueba"


def test_7_sin_entrega_la_prueba_y_prueba_verde_si_llama_a_pytest(tmp_path, monkeypatch):
    """Control: sin el campo, el codigo SI comprueba la prueba (como hoy)."""
    capataz = _importar_capataz()
    carpeta, pieza, vigia = _montar_proyecto_falso(
        tmp_path, "cuerpo/pieza_t.py", "vigias/test_vigia_t.py"
    )
    monkeypatch.setattr(capataz, "__file__", os.path.join(carpeta, "cuerpo", "capataz.py"))

    estado = {"pytest_rc": 0, "git_ls": vigia, "comando_rc": 0, "llamadas": []}
    monkeypatch.setattr(capataz.subprocess, "run", _fabricar_subprocess_run(estado))

    orden = _orden(pieza, vigia)
    resultado = capataz.comprobar_pasos(orden)

    assert resultado == ""
    llamo_a_pytest = any(
        isinstance(args, list) and len(args) >= 3 and args[1] == "-m" and args[2] == "pytest"
        for args, _kwargs in estado["llamadas"]
    )
    assert llamo_a_pytest, "el codigo no llego a comprobar la prueba"
