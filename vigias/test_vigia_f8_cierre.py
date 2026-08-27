# -*- coding: utf-8 -*-
"""VIGIA — F8 (Julio 2026-08-24): CERRAR EL CICLO. Registra aciertos y errores (disponibles como
paquete), commit siempre (no perder trabajo) y claves protegidas y borradas al final de cada seccion."""
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys = __import__("sys")


def _leer(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_registra_aciertos_y_errores():
    assert os.path.exists(os.path.join(AQUI, "cuerpo", "lecciones.py")), "falta el registro de aciertos"
    assert os.path.exists(os.path.join(AQUI, "cuerpo", "fallos.py")), "falta el registro de errores"
    t = _leer(os.path.join(AQUI, "cuerpo", "lecciones.py"))
    assert "apuntar" in t and "texto_paquete" in t, "lecciones no se fragmenta ni sale en el paquete"


def test_los_aciertos_salen_en_el_paquete():
    # el cuaderno de aciertos es consultable y fragmentado por proyecto/pieza (queda disponible)
    t = _leer(os.path.join(AQUI, "cuerpo", "lecciones.py"))
    assert "def apuntar" in t and "def texto_paquete" in t, "lecciones no es consultable"
    # el router NO queda sobrecargado (no romper la vigia del tamano del paquete)
    rt = _leer(os.path.join(AQUI, "cerebro", "router.py"))
    assert "lecciones" not in rt, "el router no debe incluir los aciertos (rompe el paquete)"


def test_commit_siempre_esta_conectado():
    import _config
    assert _config.comandos_de("Stop", "candado_commit"), \
        "el commit-siempre no esta conectado al cierre (en usuario o proyecto)"


def test_las_claves_se_borran_al_cerrar():
    assert os.path.exists(os.path.join(AQUI, "arnes", "limpiar_credenciales.py")), \
        "falta limpiar credenciales"
    t = _leer(os.path.join(AQUI, "arnes", "limpiar_credenciales.py"))
    assert "limpiar" in t, "no hay funcion que borre las claves"


def test_limpiar_borra_credenciales(tmp_path, monkeypatch):
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import limpiar_credenciales as lc
    monkeypatch.setenv("FOTO_TEST_PASSWORD", "x-secreta-1")
    monkeypatch.setenv("ALGO_API_KEY", "sk-abc")
    borradas = lc.limpiar(excluir=("NOTEST",))
    assert "FOTO_TEST_PASSWORD" in borradas and "ALGO_API_KEY" in borradas, "no borro las claves"
    assert "FOTO_TEST_PASSWORD" not in os.environ, "quedo la clave en el entorno"


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
