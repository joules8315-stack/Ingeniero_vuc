import os
import sys

import pytest


# Arranque: la carpeta que esta un nivel arriba de vigias/ entra en la ruta de busqueda,
# para poder importar cuerpo.capataz como parte del proyecto.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


# PRIMER ASSERT: la pieza que vigila esta prueba todavia NO existe.
# Esta prueba NACE ROJA a proposito: la pieza se escribe en la ronda siguiente.
# Si este assert pasa, es que la pieza ya entro y hay que revisar el resto.
from cuerpo import capataz  # noqa: E402

assert hasattr(capataz, "correr_una_orden"), (
    "LA PIEZA TODAVIA NO ESTA ESCRITA: cuerpo.capataz.correr_una_orden no existe. "
    "Esta prueba nace ROJA a proposito; la pieza se escribe en la ronda siguiente."
)


# ---------------------------------------------------------------------------
# Dobles hechos a mano. Cada uno apunta en una lista lo que se le pidio.
# Nada se lee ni se escribe en el disco de verdad.
# ---------------------------------------------------------------------------

class _DobleLanzar:
    """Doble de lanzar_al_equipo: apunta (proyecto, orden, tope, carpeta) y devuelve lo fijado."""

    def __init__(self, devolver=None, reventar=None):
        self.llamadas = []
        self.devolver = devolver if devolver is not None else {"ok": True, "guardado": True}
        self.reventar = reventar

    def __call__(self, proyecto, orden, tope_segundos=900, carpeta=None):
        self.llamadas.append({
            "proyecto": proyecto,
            "orden": orden,
            "tope_segundos": tope_segundos,
            "carpeta": carpeta,
        })
        if self.reventar is not None:
            raise self.reventar
        return self.devolver


class _DobleCopia:
    """Doble de copia_para: apunta (orden_id, raiz) y devuelve lo fijado."""

    def __init__(self, devolver=None):
        self.llamadas = []
        self.devolver = devolver if devolver is not None else {
            "ok": True, "carpeta": "/tmp/copia_de_mentira", "motivo": ""
        }

    def __call__(self, orden_id, raiz, correr_uno=None):
        self.llamadas.append({"orden_id": orden_id, "raiz": raiz})
        return self.devolver


class _DobleSoltar:
    """Doble de soltar_copia: apunta lo que se le pidio soltar."""

    def __init__(self):
        self.llamadas = []

    def __call__(self, copia, correr_uno=None):
        self.llamadas.append({"copia": copia})
        return True


# ---------------------------------------------------------------------------
# Caso 1: LE PASA LA CARPETA A QUIEN LANZA LA TAREA.
# Este es el fallo medido de los DOS intentos anteriores: se pedia la copia y no se
# le pasaba a quien lanza, asi que no servia de nada.
# ---------------------------------------------------------------------------
def test_le_pasa_la_carpeta_a_quien_lanza_la_tarea(monkeypatch):
    carpeta_de_mentira = "/tmp/copia_propia_de_la_orden_7"
    doble_copia = _DobleCopia(devolver={
        "ok": True, "carpeta": carpeta_de_mentira, "motivo": ""
    })
    doble_lanzar = _DobleLanzar(devolver={"ok": True, "guardado": True})
    doble_soltar = _DobleSoltar()

    monkeypatch.setattr(capataz, "copia_para", doble_copia)
    monkeypatch.setattr(capataz, "lanzar_al_equipo", doble_lanzar)
    monkeypatch.setattr(capataz, "soltar_copia", doble_soltar)

    capataz.correr_una_orden("proyecto_de_mentira", 7)

    assert len(doble_lanzar.llamadas) == 1, (
        "El lanzamiento no se llamo exactamente una vez."
    )
    assert doble_lanzar.llamadas[0]["carpeta"] == carpeta_de_mentira, (
        "PEDIR LA COPIA SIN PASARLA NO SIRVE DE NADA: es el fallo medido de los DOS "
        "intentos anteriores. El lanzamiento tiene que recibir EXACTAMENTE la carpeta "
        "que devolvio la pieza de las copias."
    )


# ---------------------------------------------------------------------------
# Caso 2: SUELTA LA COPIA AUNQUE LA TAREA REVIENTE, y no deja escapar el error.
# ---------------------------------------------------------------------------
def test_suelta_la_copia_aunque_la_tarea_reviente(monkeypatch):
    doble_copia = _DobleCopia(devolver={
        "ok": True, "carpeta": "/tmp/copia_propia", "motivo": ""
    })
    doble_lanzar = _DobleLanzar(reventar=RuntimeError("la tarea revento a proposito"))
    doble_soltar = _DobleSoltar()

    monkeypatch.setattr(capataz, "copia_para", doble_copia)
    monkeypatch.setattr(capataz, "lanzar_al_equipo", doble_lanzar)
    monkeypatch.setattr(capataz, "soltar_copia", doble_soltar)

    resultado = capataz.correr_una_orden("proyecto_de_mentira", 8)

    assert len(doble_soltar.llamadas) == 1, (
        "La copia se tiene que soltar SIEMPRE, pase lo que pase, incluso si la tarea "
        "revienta. El doble de soltar no se llamo."
    )
    assert isinstance(resultado, dict), (
        "Si algo revienta, la pieza devuelve un diccionario, no deja escapar el error."
    )
    assert resultado.get("ok") is False, (
        "El diccionario devuelto tiene que decir que NO se guardo (ok=False)."
    )
    assert "motivo" in resultado, (
        "El diccionario devuelto tiene que traer el motivo dentro."
    )


# ---------------------------------------------------------------------------
# Caso 3: SI NO SE PUEDE DAR LA COPIA, LA TAREA CORRE IGUAL (como hoy).
# ---------------------------------------------------------------------------
def test_si_no_se_puede_dar_la_copia_la_tarea_corre_igual(monkeypatch):
    doble_copia = _DobleCopia(devolver={
        "ok": False, "carpeta": None, "motivo": "no se pudo copiar"
    })
    lo_que_devuelve_el_lanzamiento = {"ok": True, "guardado": True, "nota": "corrio igual"}
    doble_lanzar = _DobleLanzar(devolver=lo_que_devuelve_el_lanzamiento)
    doble_soltar = _DobleSoltar()

    monkeypatch.setattr(capataz, "copia_para", doble_copia)
    monkeypatch.setattr(capataz, "lanzar_al_equipo", doble_lanzar)
    monkeypatch.setattr(capataz, "soltar_copia", doble_soltar)

    resultado = capataz.correr_una_orden("proyecto_de_mentira", 9)

    assert len(doble_lanzar.llamadas) == 1, (
        "Si no se puede dar la copia, la tarea tiene que correr igual, como hoy."
    )
    assert doble_lanzar.llamadas[0]["carpeta"] is None, (
        "Si no se pudo dar la copia, el lanzamiento va SIN carpeta."
    )
    assert resultado == lo_que_devuelve_el_lanzamiento, (
        "La pieza devuelve lo que devuelva el lanzamiento."
    )


# ---------------------------------------------------------------------------
# Caso 4: SUELTA LA COPIA TAMBIEN CUANDO TODO SALE BIEN.
# ---------------------------------------------------------------------------
def test_suelta_la_copia_tambien_cuando_todo_sale_bien(monkeypatch):
    doble_copia = _DobleCopia(devolver={
        "ok": True, "carpeta": "/tmp/copia_propia", "motivo": ""
    })
    lo_que_devuelve_el_lanzamiento = {"ok": True, "guardado": True}
    doble_lanzar = _DobleLanzar(devolver=lo_que_devuelve_el_lanzamiento)
    doble_soltar = _DobleSoltar()

    monkeypatch.setattr(capataz, "copia_para", doble_copia)
    monkeypatch.setattr(capataz, "lanzar_al_equipo", doble_lanzar)
    monkeypatch.setattr(capataz, "soltar_copia", doble_soltar)

    resultado = capataz.correr_una_orden("proyecto_de_mentira", 10)

    assert len(doble_soltar.llamadas) == 1, (
        "La copia se suelta tambien cuando todo sale bien."
    )
    assert resultado == lo_que_devuelve_el_lanzamiento, (
        "La pieza devuelve lo que devuelva el lanzamiento."
    )
