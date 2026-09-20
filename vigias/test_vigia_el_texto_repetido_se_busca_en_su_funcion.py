# -*- coding: utf-8 -*-
"""VIGIA — EL TEXTO REPETIDO SE BUSCA EN SU FUNCION.

Julio/Claude, 2026-09-19. Cuando el obrero dice en que funcion trabaja, el aplicador tiene
que poder cambiar un renglon que aparece varias veces en el archivo, buscandolo DENTRO de
esa funcion. Si el obrero no dice la funcion, no se puede saber cual de los dos es y el
cambio se rechaza con un motivo que habla de cuantas veces aparece.

QUE SE VIGILA AQUI:
  · con funcion dicha, el cambio se aplica dentro de esa funcion y la otra queda intacta
  · sin funcion dicha, el cambio se rechaza y el motivo dice que aparece 2 veces

Se importa y se desvia el apunte del registro igual que vigias/test_vigia_aplicador.py,
para no ensuciar el registro de verdad.
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


RENGLON_VIEJO = "    return 1"
RENGLON_NUEVO = "    return 2"


def _escribir_archivo_con_dos_funciones(tmp_path):
    """Escribe en disco un archivo de verdad con dos funciones que comparten el mismo renglon."""
    f = tmp_path / "cuentas.py"
    f.write_text(
        "def primera_cuenta():\n"
        "    return 1\n"
        "\n"
        "\n"
        "def segunda_cuenta():\n"
        "    return 1\n",
        encoding="utf-8",
    )
    return f


def test_con_funcion_dicha_el_cambio_va_dentro_de_esa_funcion(tmp_path):
    """Con funcion dicha, el renglon repetido se cambia DENTRO de esa funcion y la otra queda intacta."""
    f = _escribir_archivo_con_dos_funciones(tmp_path)
    propuesta = {
        "archivo": str(f),
        "funcion": "segunda_cuenta",
        "texto_viejo": RENGLON_VIEJO,
        "texto_nuevo": RENGLON_NUEVO,
    }
    ok, msg = aplicador.aplicar_cambio(propuesta)
    assert ok, (
        "el obrero dijo que trabaja en segunda_cuenta y el cambio se rechazo (%s); "
        "se pierde la ronda aprobada porque el renglon aparece tambien en primera_cuenta" % msg
    )

    contenido = f.read_text(encoding="utf-8")
    trozo_primera = contenido.split("def primera_cuenta():")[1].split("def segunda_cuenta():")[0]
    trozo_segunda = contenido.split("def segunda_cuenta():")[1]

    assert RENGLON_NUEVO in trozo_segunda, (
        "el renglon nuevo no quedo dentro de segunda_cuenta; se pierde el cambio aprobado "
        "porque se aplico en la funcion equivocada"
    )
    assert RENGLON_VIEJO in trozo_primera, (
        "primera_cuenta quedo tocada; se pierde la funcion que no era la del obrero"
    )
    assert RENGLON_NUEVO not in trozo_primera, (
        "primera_cuenta recibio el renglon nuevo; se pierde la funcion que no era la del obrero"
    )


def test_sin_funcion_dicha_el_cambio_se_rechaza_por_aparecer_dos_veces(tmp_path):
    """Sin funcion dicha, no se sabe cual de las dos es y el cambio se rechaza hablando de 2 veces."""
    f = _escribir_archivo_con_dos_funciones(tmp_path)
    propuesta = {
        "archivo": str(f),
        "funcion": "",
        "texto_viejo": RENGLON_VIEJO,
        "texto_nuevo": RENGLON_NUEVO,
    }
    ok, msg = aplicador.aplicar_cambio(propuesta)
    assert not ok, (
        "sin decir en que funcion se trabaja el cambio se acepto; se pierde la garantia de "
        "que no se toca la funcion equivocada"
    )
    assert "2" in msg and "veces" in msg, (
        "el motivo no habla de que aparece 2 veces (%s); se pierde la pista de por que se "
        "rechazo y el obrero no sabe que tiene que decir la funcion" % msg
    )

    contenido = f.read_text(encoding="utf-8")
    assert contenido.count(RENGLON_VIEJO) == 2, (
        "el archivo quedo tocado tras un rechazo; se pierde el archivo original"
    )
    assert RENGLON_NUEVO not in contenido, (
        "el renglon nuevo entro en el archivo pese al rechazo; se pierde el archivo original"
    )
