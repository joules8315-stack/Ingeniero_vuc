"""Vigia: una pieza .py nueva tiene que nacer conectada en el pit.

Comprueba que cuerpo/capataz.comprobar_pasos devuelve "aplicada" cuando la pieza
.py existe pero NINGUN otro .py del proyecto la nombra (pieza suelta), y que NO
devuelve "aplicada" por ese motivo cuando SI hay otro .py que la nombra.

Se arma una casa de mentira con tmp_path y se apunta comprobar_pasos a esa casa
parcheando la funcion que calcula la carpeta del proyecto.
"""

import json
import os

import pytest

from cuerpo import capataz


def _preparar_casa(tmp_path, pieza_relativa, contenido_pieza, otros_py):
    """Arma una casa de mentira con la pieza y los otros .py indicados.

    Devuelve la ruta absoluta de la pieza creada.
    """
    raiz = tmp_path / "casa"
    raiz.mkdir(parents=True, exist_ok=True)
    ruta_pieza = raiz / pieza_relativa
    ruta_pieza.parent.mkdir(parents=True, exist_ok=True)
    ruta_pieza.write_text(contenido_pieza, encoding="utf-8")
    for rel, contenido in otros_py.items():
        ruta_otro = raiz / rel
        ruta_otro.parent.mkdir(parents=True, exist_ok=True)
        ruta_otro.write_text(contenido, encoding="utf-8")
    return str(ruta_pieza)


def _apuntar_capataz_a(monkeypatch, raiz):
    """Hace que comprobar_pasos crea que la carpeta del proyecto es `raiz`.

    comprobar_pasos calcula carpeta_proyecto con os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))). Parcheamos os.path.abspath para que devuelva una
    ruta falsa cuyo dirname(dirname(...)) sea la casa de mentira.
    """
    falso_archivo = os.path.join(raiz, "cuerpo", "capataz.py")
    original_abspath = os.path.abspath

    def abspath_falso(ruta):
        if os.path.basename(str(ruta)) == "capataz.py":
            return falso_archivo
        return original_abspath(ruta)

    monkeypatch.setattr(os.path, "abspath", abspath_falso)


def _escribir_aprobado(raiz, base_pieza, obrero="obrero-1", auditor="auditor-1"):
    """Deja un trabajo APROBADO de la pieza para que el paso 1 (ronda) pase."""
    carpeta = os.path.join(raiz, "memoria", "trabajos_del_equipo")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, base_pieza + "_APROBADO.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"obrero": obrero, "auditor": auditor}, f)
    return ruta


def test_pieza_que_nadie_nombra_devuelve_aplicada(tmp_path, monkeypatch):
    """Una pieza .py que existe pero que ningun otro .py nombra queda suelta.

    comprobar_pasos debe devolver "aplicada" por el paso 2b (pieza_suelta).
    """
    raiz = tmp_path / "casa"
    raiz.mkdir()
    pieza_rel = os.path.join("piezas", "huerfana.py")
    ruta_pieza = _preparar_casa(
        tmp_path,
        pieza_rel,
        "def saludar():\n    return 'hola'\n",
        {
            os.path.join("otro", "vecino.py"): "def otra():\n    return 1\n",
        },
    )
    _escribir_aprobado(str(raiz), "huerfana")
    _apuntar_capataz_a(monkeypatch, str(raiz))

    orden = {"pieza": ruta_pieza, "vigia": "", "comando": ""}
    resultado = capataz.comprobar_pasos(orden)

    assert resultado == "aplicada", (
        "una pieza .py que nadie nombra debe devolver 'aplicada' (pieza suelta), "
        "pero devolvio %r" % (resultado,)
    )


def test_pieza_nombrada_no_devuelve_aplicada_por_ese_motivo(tmp_path, monkeypatch):
    """Una pieza .py que SI la nombra otro .py no queda suelta.

    comprobar_pasos no debe devolver "aplicada" por el paso 2b. Como la orden no
    trae vigia, el siguiente paso es "vigia_verde".
    """
    raiz = tmp_path / "casa"
    raiz.mkdir()
    pieza_rel = os.path.join("piezas", "conectada.py")
    ruta_pieza = _preparar_casa(
        tmp_path,
        pieza_rel,
        "def saludar():\n    return 'hola'\n",
        {
            os.path.join("otro", "vecino.py"): (
                "import piezas.conectada\n\ndef usar():\n    return conectada.saludar()\n"
            ),
        },
    )
    _escribir_aprobado(str(raiz), "conectada")
    _apuntar_capataz_a(monkeypatch, str(raiz))

    orden = {"pieza": ruta_pieza, "vigia": "", "comando": ""}
    resultado = capataz.comprobar_pasos(orden)

    assert resultado != "aplicada", (
        "una pieza .py que SI la nombra otro .py no debe devolver 'aplicada' "
        "por pieza suelta, pero devolvio %r" % (resultado,)
    )
    assert resultado == "vigia_verde", (
        "sin vigia en la orden, tras pasar el paso 2b debe devolver 'vigia_verde', "
        "pero devolvio %r" % (resultado,)
    )


def test_pieza_que_no_existe_devuelve_aplicada(tmp_path, monkeypatch):
    """Control: si la ruta de la pieza no existe en disco, devuelve 'aplicada'."""
    raiz = tmp_path / "casa"
    raiz.mkdir()
    _escribir_aprobado(str(raiz), "fantasma")
    _apuntar_capataz_a(monkeypatch, str(raiz))

    orden = {
        "pieza": os.path.join(str(raiz), "piezas", "fantasma.py"),
        "vigia": "",
        "comando": "",
    }
    resultado = capataz.comprobar_pasos(orden)

    assert resultado == "aplicada", (
        "una pieza cuya ruta no existe debe devolver 'aplicada', pero devolvio %r"
        % (resultado,)
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
