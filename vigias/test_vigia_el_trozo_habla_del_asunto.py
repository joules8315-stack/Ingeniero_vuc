# -*- coding: utf-8 -*-
"""VIGIA 22 — EL TROZO TIENE QUE HABLAR DEL ASUNTO (2026-08-21).

COMO SE DESCUBRIO: se saboteo a proposito el filtro del asunto (se dejo muerto) y la vigia que
decia proteger esa reparacion siguio VERDE, 6 de 6. Miraba que ARCHIVOS llegaban, y la reparacion
era sobre que TROZOS llegan. Una reparacion protegida por una prueba que no la prueba es una
reparacion desprotegida sin que nadie lo vea: el mismo patron de los vigias verdes sobre un caso
que no se vive.

LA REPARACION QUE PROTEGE (esta escrita en cerebro/trozos.py, en `buscar`):
   "buscar 'no persiste la plantilla al cambiar de SESION' traia el login (por la palabra sesion)"

Traer el trozo equivocado no es un detalle: es lo que hace que se repare el sitio equivocado.

ESTA VIGIA NACE ROJA si se anula el filtro: se comprobo anulandolo antes de darla por buena.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import trozos


@pytest.fixture
def dos_piezas(tmp_path):
    """Dos piezas de mentira, controladas: una habla de plantilla, la otra de login.
    Comparten la palabra 'sesion', que es justo la trampa del caso real."""
    a = tmp_path / "plantilla.py"
    a.write_text(
        "# la plantilla del informe se guarda y se recupera en cada sesion\n"
        "def guardar_plantilla(informe, sesion):\n"
        "    " + '"""Guarda la plantilla del informe para esta sesion."""' + "\n"
        "    return informe\n" * 30, encoding="utf-8")
    b = tmp_path / "login.py"
    b.write_text(
        "# el login abre la sesion del usuario y la cierra al salir\n"
        "def entrar(usuario, clave, sesion):\n"
        "    " + '"""Abre la sesion del usuario tras comprobar la clave."""' + "\n"
        "    return sesion\n" * 30, encoding="utf-8")
    return [
        {"id": "cerebro/plantilla.py", "abs": str(a), "rol": "codigo"},
        {"id": "cerebro/login.py", "abs": str(b), "rol": "codigo"},
    ]


def test_el_filtro_de_asunto_descarta_lo_ajeno(dos_piezas):
    """EL NUCLEO: si se exige el asunto, el trozo que no lo menciona NO puede pasar.
    Con el filtro anulado esta prueba se pone ROJA (comprobado sabotenandolo)."""
    b = trozos.Buscador(dos_piezas)
    res = b.buscar("no persiste la plantilla al cambiar de sesion",
                   k=10, exigir=["plantilla"])
    assert res, "no trajo nada: el filtro no puede dejar la busqueda vacia"
    for r in res:
        assert "plantilla" in r["texto"].lower(), (
            "trajo un trozo que NO habla del asunto exigido: %s:%s-%s"
            % (r["pieza"], r["desde"], r["hasta"]))


def test_el_caso_real_la_plantilla_no_trae_el_login(dos_piezas):
    """El caso literal que se reparo en su dia, tal cual esta escrito en el codigo."""
    b = trozos.Buscador(dos_piezas)
    res = b.buscar("no persiste la plantilla al cambiar de sesion",
                   k=10, exigir=["plantilla"])
    trajo = {r["pieza"] for r in res}
    assert "cerebro/login.py" not in trajo, (
        "volvio a pasar: un problema de PLANTILLA trajo el codigo del LOGIN")


def test_sin_exigir_asunto_si_se_cuela_lo_ajeno(dos_piezas):
    """La prueba de que el filtro es lo unico que lo impide: sin el, el login se cuela.
    Si esta se pone roja, el filtro dejo de ser lo que protege y hay que mirar por que."""
    b = trozos.Buscador(dos_piezas)
    res = b.buscar("no persiste la plantilla al cambiar de sesion", k=10, exigir=None)
    assert any(r["pieza"] == "cerebro/login.py" for r in res), (
        "sin filtro ya no se cuela el login: el filtro puede haber dejado de hacer falta")


def test_el_trozo_dice_donde_esta(dos_piezas):
    """Un trozo sin linea exacta obliga a abrir el archivo entero: ahi se va el ahorro."""
    b = trozos.Buscador(dos_piezas)
    for r in b.buscar("plantilla del informe", k=4, exigir=["plantilla"]):
        assert isinstance(r["desde"], int) and isinstance(r["hasta"], int)
        assert r["hasta"] >= r["desde"], "el trozo dice un tramo imposible"
