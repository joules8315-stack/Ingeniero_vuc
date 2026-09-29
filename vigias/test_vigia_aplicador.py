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


def test_crea_archivo_nuevo_aunque_el_obrero_ponga_la_marca_NO_ENCONTRADO(tmp_path):
    """El equipo aprobo crear el archivo: la marca NO_ENCONTRADO no puede impedirlo."""
    f = str(tmp_path / "nuevo_con_marca.py")
    propuesta = {
        "archivo": f,
        "funcion": "NO_ENCONTRADO",
        "texto_viejo": "NO_ENCONTRADO",
        "texto_nuevo": "NO_ENCONTRADO",
        "codigo": "x = 1\n",
    }
    ok, msg = aplicador.aplicar_cambio(propuesta)
    assert ok, (
        "el equipo aprobo crear el archivo y la marca NO_ENCONTRADO lo impidio; "
        "se tira una ronda pagada: " + str(msg)
    )
    assert os.path.exists(f), "no quedo el archivo nuevo en disco"
    contenido = open(f, encoding="utf-8").read()
    assert "x = 1" in contenido, "no se escribio el codigo aprobado"
    assert "NO_ENCONTRADO" not in contenido, "la marca NO_ENCONTRADO se colo en el archivo"


def test_la_marca_sola_no_crea_un_archivo(tmp_path):
    """Sin codigo aprobado, la marca sola no puede crear nada."""
    f = str(tmp_path / "solo_marca.py")
    propuesta = {
        "archivo": f,
        "funcion": "NO_ENCONTRADO",
        "texto_viejo": "NO_ENCONTRADO",
        "texto_nuevo": "NO_ENCONTRADO",
    }
    ok, _ = aplicador.aplicar_cambio(propuesta)
    assert not ok, "creo un archivo que solo tenia la marca"
    assert not os.path.exists(f), "quedo un archivo en disco que solo tenia la marca"


def test_anadir_al_final_con_ancla_igual_y_codigo_no_es_humo(tmp_path):
    """Ancla igual + codigo nuevo es anadir al final, no humo."""
    f = tmp_path / "existente.py"
    f.write_text("def a():\n    return 1\n", encoding="utf-8")
    propuesta = {
        "archivo": str(f),
        "texto_viejo": "def a():",
        "texto_nuevo": "def a():",
        "codigo": "def b():\n    return 2\n",
    }
    ok, msg = aplicador.aplicar_cambio(propuesta)
    assert ok, (
        "el obrero pidio anadir codigo al final y se tomo por humo: " + str(msg)
    )
    txt = f.read_text(encoding="utf-8")
    assert "def a():" in txt and "return 1" in txt, "se perdio lo que ya habia"
    assert "def b():" in txt, "no se anadio el codigo nuevo"
    assert txt.index("def b():") > txt.index("def a():"), "el codigo nuevo no quedo al final"

def test_un_archivo_con_marca_BOM_se_puede_editar(tmp_path):
    """fallo real 2026-09-13, ingeniero.py tiene BOM y el aplicador tiraba todo cambio aprobado."""
    f = tmp_path / "con_bom.py"
    f.write_bytes(b"\xef\xbb\xbf" + "def vieja():\n    return 1\n".encode("utf-8"))
    propuesta = {
        "archivo": str(f),
        "texto_viejo": "def vieja():",
        "texto_nuevo": "def nueva():",
    }
    ok, msg = aplicador.aplicar_cambio(propuesta)
    assert ok, (
        "un archivo con marca BOM no se pudo editar; asi se tira todo cambio aprobado a ingeniero.py: "
        + str(msg)
    )
    datos = f.read_bytes()
    assert "def nueva():" in datos.decode("utf-8-sig"), "no quedo el cambio"
    assert datos.count(b"\xef\xbb\xbf") <= 1, "la marca BOM quedo duplicada"


def test_un_archivo_con_marca_BOM_se_puede_editar_por_varios_pedazos(tmp_path):
    """fallo real 2026-09-28: aplicar_cambios (varios pedazos) tiraba todo cambio aprobado a ingeniero.py por la marca BOM."""
    f = tmp_path / "con_bom.py"
    f.write_bytes(b"\xef\xbb\xbf" + "def vieja():\n    return 1\n".encode("utf-8"))
    propuesta = {
        "cambios": [
            {
                "archivo": str(f),
                "texto_viejo": "def vieja():",
                "texto_nuevo": "def nueva():",
            }
        ]
    }
    ok, msg = aplicador.aplicar_cambios(propuesta)
    assert ok, (
        "un archivo con marca BOM no se pudo editar por el camino de varios pedazos; asi se tira todo cambio aprobado a ingeniero.py: "
        + str(msg)
    )
    datos = f.read_bytes()
    assert "def nueva():" in datos.decode("utf-8-sig"), "no quedo el cambio"
    assert datos.count(b"\xef\xbb\xbf") == 1, "la marca BOM no quedo exactamente una vez"
