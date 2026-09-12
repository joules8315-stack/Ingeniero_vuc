# -*- coding: utf-8 -*-
"""VIGIA — EL CONTADOR DE LEYES SIN GUARDIAN NO PUEDE MENTIR.

POR QUE NACE (2026-09-12): skills/leyes_sin_vigia.py dijo que 35 de 56 leyes son "solo papel", el
62 por ciento. Al ir a repararlas, la primera de la lista (CONTRATO_NO_REPETIR) YA TENIA GUARDIAN:
vigias/test_vigia_no_repetir.py existe y lleva su nombre.

EL FALLO: el contador casa una ley con su guardian buscando el NOMBRE EN MAYUSCULAS dentro del
TEXTO de las vigias. Si un guardian protege una ley sin nombrarla con esa forma exacta, lo cuenta
como huerfana. Y ese guardian se llama test_vigia_no_repetir.py, en minusculas.

ES EL MISMO FALLO QUE EL CONTADOR DE PIEZAS DORMIDAS, que decia 17 cuando eran 10 y mandaba a
"reparar" lo que ya estaba enchufado. UN CONTADOR QUE MIENTE MANDA A TOCAR LO SANO, y eso es peor
que no tenerlo: se gasta trabajo donde no hace falta y se pierde la confianza en el numero.

LO QUE SE EXIGE:
  1. que una ley con guardian NO salga como huerfana, aunque el guardian la nombre en minusculas
     o solo la lleve en su nombre de archivo
  2. que una ley que de verdad no tiene a nadie SIGA saliendo: no se perdona de mas
  3. que las cuentas cuadren: las que tienen mas las que no tienen suman todas

COMO SE PRUEBA: se EJECUTA el contador contra una casa de mentira que se monta aqui. No se toca
la casa real y sale lo mismo las mil veces.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)


def _contador():
    """Cargado POR SU SITIO: en esta casa hay una carpeta skills/ y un archivo cuerpo/skills.py,
    y cuando otra prueba carga el archivo, el nombre queda ocupado."""
    import importlib.util
    ruta = os.path.join(AQUI, "skills", "leyes_sin_vigia.py")
    if not os.path.exists(ruta):
        pytest.fail("NO EXISTE skills/leyes_sin_vigia.py")
    spec = importlib.util.spec_from_file_location("leyes_sin_vigia_por_su_sitio", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _casa_de_mentira(tmp_path):
    """Dos leyes: una con guardian que la nombra SOLO en su nombre de archivo, y otra sin nadie."""
    (tmp_path / "CONTRATO_NO_REPETIR.md").write_text("# ley con guardian\n", encoding="utf-8")
    (tmp_path / "CONTRATO_SIN_NADIE.md").write_text("# ley sola\n", encoding="utf-8")
    vig = tmp_path / "vigias"
    vig.mkdir()
    # El guardian NO nombra la ley en mayusculas por dentro: solo en como se llama el archivo.
    (vig / "test_vigia_no_repetir.py").write_text(
        "def test_algo():\n    assert True\n", encoding="utf-8")
    return tmp_path


def _apuntar_a(c, casa, monkeypatch):
    """El contador mira DOS sitios: donde estan las leyes y donde estan los guardianes.

    Se desvian LOS DOS. Desviar solo uno fue el primer intento y dejaba al contador leyendo los
    guardianes DE VERDAD contra las leyes de mentira: la prueba salia verde por el motivo
    equivocado, que es la peor clase de verde.
    """
    monkeypatch.setattr(c, "AQUI", str(casa), raising=False)
    monkeypatch.setattr(c, "VIGIAS", str(casa / "vigias"), raising=False)


def test_una_ley_CON_guardian_no_sale_como_huerfana(tmp_path, monkeypatch):
    c = _contador()
    casa = _casa_de_mentira(tmp_path)
    _apuntar_a(c, casa, monkeypatch)
    sin = list(c.revisar()["sin_vigia"])
    assert "CONTRATO_NO_REPETIR.md" not in sin, (
        "EL CONTADOR MIENTE: dice que esa ley no tiene guardian y SI lo tiene "
        "(test_vigia_no_repetir.py). Un contador que miente manda a reparar lo sano, que es lo "
        "que ya paso con el de piezas dormidas: decia 17 cuando eran 10. Dijo: %s" % sin)


def test_una_ley_SIN_NADIE_sigue_saliendo(tmp_path, monkeypatch):
    """No se perdona de mas: si de verdad no tiene a nadie, tiene que salir."""
    c = _contador()
    casa = _casa_de_mentira(tmp_path)
    _apuntar_a(c, casa, monkeypatch)
    assert "CONTRATO_SIN_NADIE.md" in c.revisar()["sin_vigia"], (
        "dejo de ver una ley que NO tiene guardian: ahora peca de lo contrario y tampoco sirve")


def test_las_cuentas_cuadran(tmp_path, monkeypatch):
    """Las que tienen mas las que no, suman todas. Si no cuadra, el numero no significa nada."""
    c = _contador()
    casa = _casa_de_mentira(tmp_path)
    _apuntar_a(c, casa, monkeypatch)
    r = c.revisar()
    assert len(r["con_vigia"]) + len(r["sin_vigia"]) == len(r["todas"]), (
        "las cuentas no cuadran: %d con + %d sin != %d todas"
        % (len(r["con_vigia"]), len(r["sin_vigia"]), len(r["todas"])))
