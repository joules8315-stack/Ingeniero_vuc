# -*- coding: utf-8 -*-
"""VIGIA — UN .py NUEVO Y ROTO NO LLEGA AL DISCO.

Julio/Claude, 2026-09-27. `cuerpo/aplicador.py::aplicar_cambio` tiene dos ramas:

  · la rama que REESCRIBE un archivo que YA existe SI comprueba la sintaxis con
    ast.parse y devuelve el renglon donde esta el error;
  · la rama que CREA un archivo que NO existe escribe el texto en disco SIN
    comprobar la sintaxis.

Esta vigia NACE ROJA A PROPOSITO: en esta ronda solo se crea la vigia, y el arreglo
que la pone verde entra en la ronda siguiente. No se toca ningun otro archivo.

QUE SE VIGILA AQUI:
  · un .py nuevo con codigo roto NO se crea: ok falso, sin archivo en disco, y el
    aviso nombra el renglon del error
  · un .py nuevo bien escrito SI se crea y queda en disco
  · un archivo nuevo que NO termina en .py (por ejemplo NOTAS.md) se crea igual que hoy

No se llama a ninguna IA y no se lanza ningun proceso: todo pasa en tmp_path.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "cuerpo"))
import pytest

from cuerpo import aplicador  # noqa: E402


@pytest.fixture(autouse=True)
def _sin_log(tmp_path, monkeypatch):
    """El aplicador apunta en memoria/APLICACIONES.log; se desvia para no ensuciar el real."""
    monkeypatch.setattr(aplicador, "_apuntar_log", lambda *a, **k: None)
    yield


def test_un_py_nuevo_roto_no_llega_al_disco(tmp_path):
    """Un .py nuevo con sintaxis rota NO debe quedar en disco y el aviso debe nombrar el renglon."""
    f = str(tmp_path / "nuevo_roto.py")
    codigo_roto = "def f(:\n    return 1\n"
    ok, msg = aplicador.aplicar_cambio({"archivo": f, "codigo": codigo_roto})
    assert not ok, "un .py nuevo con sintaxis rota no puede darse por aplicado: " + str(msg)
    assert not os.path.exists(f), "el .py roto llego al disco; la rama de creacion no comprueba la sintaxis"
    assert "renglon" in str(msg).lower(), "el aviso debe nombrar el renglon del error: " + str(msg)


def test_un_py_nuevo_bien_escrito_si_se_crea(tmp_path):
    """Un .py nuevo con codigo valido SI se crea y queda en disco."""
    f = str(tmp_path / "nuevo_bien.py")
    codigo_bien = "def f():\n    return 1\n"
    ok, msg = aplicador.aplicar_cambio({"archivo": f, "codigo": codigo_bien})
    assert ok, "un .py nuevo bien escrito debe crearse: " + str(msg)
    assert os.path.exists(f), "no quedo el archivo en disco"
    with open(f, encoding="utf-8") as fh:
        assert "def f():" in fh.read(), "no quedo el codigo aprobado"


def test_un_archivo_que_no_es_codigo_se_crea_igual(tmp_path):
    """Un archivo nuevo que NO termina en .py se crea igual que hoy, sin comprobar sintaxis."""
    f = str(tmp_path / "NOTAS.md")
    texto = "esto no es Python: solo son notas\n"
    ok, msg = aplicador.aplicar_cambio({"archivo": f, "codigo": texto})
    assert ok, "un archivo que no es codigo debe crearse igual: " + str(msg)
    assert os.path.exists(f), "no quedo el archivo en disco"
    with open(f, encoding="utf-8") as fh:
        assert "esto no es Python" in fh.read(), "no quedo el texto aprobado"
