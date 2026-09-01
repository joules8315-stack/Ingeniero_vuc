# -*- coding: utf-8 -*-
"""VIGIA — EL EQUIPO TAMBIEN VIGILA FUERA DE LA CASA (Julio, 2026-09-02).

  "El cierre del equipo — el que me obliga a repartir el trabajo — mira solo lo que hay dentro
   de la casa. Mi mesa de trabajo esta fuera. Y hoy escribi ahi, con mis manos, cinco piezas."

LO QUE PASO, MEDIDO: `arnes/candado_equipo.py` devolvia 0 ("no es de esta casa: no se vigila")
para TODO archivo que no estuviera dentro de las rutas de `proyectos.config` (ingeniero, dmm,
foto_informe). El MVP y cualquier proyecto de la mesa de Julio estaban FUERA: la IA podia
escribir codigo A SOLAS, sin veredicto, y nadie lo veia.

QUE SE VIGILA AQUI:
  · que escribir codigo FUERA de las rutas registradas, sin veredicto, FRENE (antes escapaba)
  · que un borrador temporal del sistema SIGA pasando (no es un muro)
  · que un veredicto del equipo abra tambien un archivo de fuera (la llave vale en todas partes)
  · que un documento (.md) de fuera siga pasando
"""
import json
import os
import subprocess
import sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))


@pytest.fixture(autouse=True)
def _escenario(tmp_path, monkeypatch):
    """Desvia la casa, el temporal y las libretas a carpetas de mentira (como el resto del arnes)."""
    casa = tmp_path / "casa"
    casa.mkdir(exist_ok=True)
    temp = tmp_path / "temp"
    temp.mkdir(exist_ok=True)
    monkeypatch.setenv("INGENIERO_CASA_TEST", str(casa))
    monkeypatch.setenv("INGENIERO_TEMP_TEST", str(temp))
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_SIN_EQUIPO_TEST", str(tmp_path / "sin_equipo.log"))
    yield


def _correr(fp):
    r = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_equipo.py")],
                       input=json.dumps({"tool_input": {"file_path": fp}}),
                       capture_output=True, text=True, env=dict(os.environ), cwd=AQUI)
    return r.returncode, (r.stderr or "")


# ─── FUERA DE LA CASA: YA NO SE ESCAPA ────────────────────────────────────────
def test_bloquea_codigo_fuera_de_casa(tmp_path):
    """EL NUCLEO. Un archivo de codigo que NO esta en ninguna ruta registrada y NO es temporal
    tiene que FRENAR sin veredicto. Antes devolvia 0 y la IA escribia a solas en la mesa de Julio."""
    fuera = tmp_path / "fuera" / "algo.py"
    fuera.parent.mkdir(exist_ok=True)
    fuera.write_text("x = 1\n", encoding="utf-8")
    code, err = _correr(str(fuera))
    assert code == 2, "dejo escribir codigo FUERA de la casa sin que el equipo lo mirara"
    assert "equipo" in err.lower() or "A SOLAS" in err


def test_temporal_de_fuera_sigue_pasando(tmp_path):
    """Un borrador temporal no es trabajo: no debe frenar (leccion del 2026-09-01)."""
    t = tmp_path / "temp" / "borrador.py"
    t.write_text("x = 1\n", encoding="utf-8")
    code, _ = _correr(str(t))
    assert code == 0, "freno un borrador temporal, que es el muro que se acaba apagando"


def test_veredicto_abre_tambien_fuera_de_casa(tmp_path):
    """La llave del equipo vale en todas partes, no solo dentro. Si el equipo miro ese archivo
    de fuera, se puede escribir en el."""
    import candado_equipo as ce
    fuera = tmp_path / "fuera" / "algo.py"
    fuera.parent.mkdir(exist_ok=True)
    fuera.write_text("x = 1\n", encoding="utf-8")
    ce.guardar_veredicto("tarea fuera", [str(fuera)], "groq", "gemini", "APROBADO")
    code, _ = _correr(str(fuera))
    assert code == 0, "el veredicto del equipo no abrio el archivo de fuera"


def test_documento_de_fuera_sigue_pasando(tmp_path):
    """Los documentos (.md) de fuera no son codigo: no hay por que frenarlos."""
    fuera = tmp_path / "fuera" / "nota.md"
    fuera.parent.mkdir(exist_ok=True)
    fuera.write_text("# nota\n", encoding="utf-8")
    code, _ = _correr(str(fuera))
    assert code == 0, "freno un documento de fuera, y eso es un muro"
