import json
import subprocess
import sys
import os

# La carpeta arnes vive al lado de vigias/. Se mete en sys.path para poder importar
# candado_cierre igual que lo hacen las demas vigias de ese candado.
AQUI = os.path.dirname(os.path.abspath(__file__))
ARNES = os.path.join(os.path.dirname(AQUI), "arnes")
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import candado_cierre


class _ResultadoFalso:
    """Objeto minimo que imita lo que devuelve subprocess.run."""

    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _preparar(monkeypatch, tmp_path, ordenes):
    """Deja el entorno listo: sin pytest dentro de pytest, sin cerrojo real y sin
    correr nada de verdad. Devuelve la raiz (tmp_path) ya montada."""
    # Dentro de una vigia no se corren vigias: se prueba la logica.
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    # Nunca hay otra corrida en marcha.
    monkeypatch.setattr(candado_cierre, "_ya_hay_otra_corrida", lambda: False)

    # El cerrojo no toca el disco de verdad.
    monkeypatch.setattr(candado_cierre, "_poner_cerrojo", lambda: None)
    monkeypatch.setattr(candado_cierre, "_quitar_cerrojo", lambda: None)

    # subprocess.run NUNCA corre nada de verdad.
    def _run_falso(orden, *args, **kwargs):
        texto = " ".join(str(x) for x in orden) if isinstance(orden, (list, tuple)) else str(orden)
        if "pytest" in texto:
            return _ResultadoFalso(
                1,
                "FAILED vigias/test_a.py::test_x - AssertionError\n",
                "",
            )
        if "git" in texto:
            # La prueba ya estaba guardada: git la reconoce.
            return _ResultadoFalso(0, "", "")
        return _ResultadoFalso(0, "", "")

    monkeypatch.setattr(subprocess, "run", _run_falso)

    # raiz = tmp_path, con vigias/ creada y memoria/ORDENES.json si toca.
    (tmp_path / "vigias").mkdir()
    (tmp_path / "memoria").mkdir()
    if ordenes is not None:
        (tmp_path / "memoria" / "ORDENES.json").write_text(
            json.dumps(ordenes, ensure_ascii=False), encoding="utf-8"
        )
    return tmp_path


def test_orden_pendiente_hace_que_el_cierre_no_pare(monkeypatch, tmp_path):
    """Si hay una orden pendiente sobre una vigia, el primer valor es True:
    el cierre no para por una prueba que todavia espera."""
    ordenes = {
        "ordenes": [
            {"estado": "pendiente", "vigia": "vigias/test_a.py"},
        ]
    }
    raiz = _preparar(monkeypatch, tmp_path, ordenes)
    verde, detalle = candado_cierre._vigias_verdes(raiz)
    assert verde is True, detalle


def test_orden_que_corrige_su_propia_prueba_tambien_espera(monkeypatch, tmp_path):
    """Una orden pendiente que corrige su propia prueba tambien espera: el cierre no sabe que tarea se guarda ahora, eso lo mira el guardia (medido 2026-09-21)"""
    ordenes = {
        "ordenes": [
            {"estado": "pendiente", "vigia": "vigias/test_a.py", "pieza": "vigias/test_a.py"},
        ]
    }
    raiz = _preparar(monkeypatch, tmp_path, ordenes)
    verde, detalle = candado_cierre._vigias_verdes(raiz)
    assert verde is True, detalle


def test_orden_hecha_hace_que_el_cierre_pare(monkeypatch, tmp_path):
    """Si esa orden ya esta hecha, el primer valor es False: la prueba ya no espera."""
    ordenes = {
        "ordenes": [
            {"estado": "hecha", "vigia": "vigias/test_a.py"},
        ]
    }
    raiz = _preparar(monkeypatch, tmp_path, ordenes)
    verde, detalle = candado_cierre._vigias_verdes(raiz)
    assert verde is False, detalle


def test_sin_ordenes_el_cierre_pare_como_hoy(monkeypatch, tmp_path):
    """Si ORDENES.json no existe, el primer valor es False, como hoy."""
    raiz = _preparar(monkeypatch, tmp_path, None)
    verde, detalle = candado_cierre._vigias_verdes(raiz)
    assert verde is False, detalle
