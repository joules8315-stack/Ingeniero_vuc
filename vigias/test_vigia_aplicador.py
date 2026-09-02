# -*- coding: utf-8 -*-
"""VIGIA — EL APLICADOR: el brazo que aplica en disco lo aprobado por el equipo (plan pieza 1 y 2).

Julio/Claude, 2026-09-02. `cuerpo/aplicador.py` es la pieza que el plan acepta entera: aplica lo
que el equipo aprobo SIN dejar el archivo roto. Esta vigia la protege y comprueba que esta
conectada al mando `equipo` (plan pieza 2: "conectarlo al mando del equipo").

QUE SE VIGILA AQUI:
  · crea un archivo nuevo cuando no existe
  · edita un archivo existente sustituyendo el texto aprobado
  · NO deja un .py con sintaxis rota (lo comprueba antes de confirmar)
  · el mando `equipo` de ingeniero.py usa el aplicador
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


def test_crea_archivo_nuevo(tmp_path):
    """Un archivo que NO existe se crea con el texto aprobado."""
    f = str(tmp_path / "nuevo.py")
    ok, _ = aplicador.aplicar_cambio({"archivo": f, "codigo": "x = 1\n"})
    assert ok, "no creo el archivo nuevo"
    assert os.path.exists(f), "no quedo el archivo en disco"
    assert "x = 1" in open(f, encoding="utf-8").read()


def test_edita_archivo_existente(tmp_path):
    """Un archivo que SI existe se edita sustituyendo el texto aprobado."""
    f = tmp_path / "a.py"
    f.write_text("def vieja():\n    return 1\n", encoding="utf-8")
    ok, _ = aplicador.aplicar_cambio({"archivo": str(f),
                                      "texto_viejo": "def vieja():",
                                      "texto_nuevo": "def nueva():"})
    assert ok, "no edito el archivo existente"
    assert "def nueva():" in f.read_text(encoding="utf-8"), "no quedo el cambio"


def test_no_deja_sintaxis_rota(tmp_path):
    """El nucleo: si el cambio deja el .py roto, NO se confirma y el archivo queda intacto."""
    f = tmp_path / "b.py"
    f.write_text("x = 1\n", encoding="utf-8")
    ok, _ = aplicador.aplicar_cambio({"archivo": str(f),
                                      "texto_viejo": "x = 1",
                                      "texto_nuevo": "def (:"})
    assert not ok, "dejo pasar un cambio que rompe la sintaxis"
    assert "x = 1" in f.read_text(encoding="utf-8"), "el archivo quedo roto en disco"


def test_esta_conectado_al_mando_del_equipo():
    """Plan pieza 2: el mando `equipo` tiene que usar el aplicador, o la pieza no sirve para nada."""
    txt = open(os.path.join(AQUI, "ingeniero.py"), encoding="utf-8").read()
    assert "aplicador" in txt, "el aplicador NO esta conectado al mando del equipo"
