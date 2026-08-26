# -*- coding: utf-8 -*-
"""VIGIA — PREGUNTA DE CRITERIO: la causa se declara con el CAMBIO aislado.

Claude, 2026-08-25 (punto 1): "Nada vigila si entendi mal. Al declarar una causa hay que responder
'que cambio entre la medicion de antes y la de despues? Enumeralo.' Si hay mas de una cosa en la
lista, eso no es aislar: es una coincidencia. Es una pregunta, no un candado."

Sus dos diagnosticos falsos de hoy pasaron todos los candados: aparto un archivo creyendo aislar su
cambio (y aparto el cambio de tres personas); comparo dos cosas creyendo comparar una. Esto no lo
cazaba nada. La cura: el campo `cambio` en la causa raiz, obligatorio, que nombre UNA sola cosa; si
enumera varias, se avisa (coincidencia) pero no se bloquea.

Comprueba:
  · declarar exige `cambio` (sin el, error),
  · una sola cosa no da aviso,
  · enumerar dos o mas (coma / "y") da aviso de coincidencia,
  · el mando `causa` pasa --cambio.
"""
import io
import os
import time

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import candado_diagnostico as cd   # noqa: E402


@pytest.fixture
def _dir(monkeypatch, tmp_path):
    ruta = str(tmp_path / "DIAGNOSTICO_test.json")
    monkeypatch.setattr(cd, "RUTA", ruta)
    return ruta


def _causa(cambio):
    return cd.declarar("p", "a.py", "f", "1", "mide 5 -> 2", cambio)


def test_sin_cambio_no_se_declara(_dir):
    r = cd.declarar("p", "a.py", "f", "1", "evi", "")
    assert "_error" in r, "declarar sin --cambio debe fallar: la causa exige responder QUE cambio"


def test_una_sola_cosa_no_da_aviso(_dir):
    r = _causa("cambie scheduleAutoSync de la pantalla 4 a la 2")
    assert "_aviso" not in r, "una sola cosa cambiada es aislar: no debe sonar la coincidencia"


def test_varias_cosas_da_aviso_de_coincidencia(_dir):
    r = _causa("cambie la funcion X y agregue el campo Y")
    assert "_aviso" in r, "enumerar dos cambios es una coincidencia, no aislar: debe avisar"


def test_varias_cosas_con_coma_da_aviso(_dir):
    r = _causa("cambie la funcion, agregue un reloj y toque el indice")
    assert "_aviso" in r, "con coma / 'y' enumera varias cosas: debe avisar"


def test_el_mando_pasa_cambio():
    txt = io.open(os.path.join(AQUI, "ingeniero.py"), encoding="utf-8", errors="ignore").read()
    assert "--cambio" in txt, "el comando 'causa' debe aceptar --cambio"
    assert "declarar(a[0]" in txt and "--cambio" in txt.split("declarar(a[0]")[1][:200], \
        "causa debe pasarle --cambio a declarar"
