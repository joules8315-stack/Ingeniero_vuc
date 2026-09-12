# -*- coding: utf-8 -*-
"""VIGIA — SE TRABAJA CON CLINE, Y ALGUIEN RESPONDE POR ELLO.

Ley: CONTRATO_TRABAJO_CON_CLINE.md (Julio, 2026-08-31):
  "Trabaja con cline... Una vez termine la tarea cline, superviza, si es correcta, dale otra
   tarea, sino, dile que corrija, y me informas si falla."

No se mide lo que se promete: se mide lo que el codigo HACE. Se le dan casos de mentira al
reparto y se mira si de verdad impide lo que tiene que impedir.

LO QUE SE MIDE
  1. Existe la ley y existe la pieza que la hace cumplir.
  2. Dos IA no pueden coger la misma tarea (trabajo pagado dos veces y choque al guardar).
  3. Una tarea entregada NO se puede dar por buena sin su vigia en VERDE. Este es el corazon:
     "si es correcta, dale otra tarea, sino, dile que corrija".
  4. Lo entregado y no supervisado se ve: es deuda, no avance.
  5. Lo que no salio queda marcado PARA CONTARSELO A JULIO.
  6. Y de verdad, no en el laboratorio: Cline tiene una tarea asignada ahora mismo.
"""
import io
import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

import reparto   # noqa: E402

LEY = os.path.join(AQUI, "CONTRATO_TRABAJO_CON_CLINE.md")


@pytest.fixture
def cuaderno_de_mentira(tmp_path, monkeypatch):
    """Se prueba sobre un cuaderno de mentira: una prueba jamas escribe en la memoria de verdad.

    Esa leccion costo cara: las vigias envenenaron el diccionario de Julio escribiendo en el
    cuaderno bueno, y una entrada falsa acabo ganandole a todas las de verdad.
    """
    falso = tmp_path / "REPARTO_IA.json"
    monkeypatch.setattr(reparto, "RUTA", str(falso))
    return str(falso)


def test_existe_la_ley_y_quien_la_hace_cumplir():
    assert os.path.exists(LEY), "no esta escrita la ley de como se trabaja con Cline"
    assert hasattr(reparto, "asignar") and hasattr(reparto, "supervisar"), \
        "la pieza del reparto no sabe asignar ni supervisar: entonces no hace cumplir nada"


def test_dos_no_pueden_coger_la_misma_tarea(cuaderno_de_mentira):
    """Dos IA en la misma tarea es pagarla dos veces y chocar al guardar."""
    ok, _ = reparto.asignar("cline", "reparar el diccionario envenenado")
    assert ok, "no dejo asignar una tarea nueva"
    ok2, motivo = reparto.asignar("claude", "reparar el diccionario envenenado")
    assert not ok2, "dejo que dos IA cogieran la MISMA tarea: eso es pagarla dos veces"
    assert "cline" in motivo, "no dice quien la tiene ya, asi que no se puede resolver el choque"


def test_lo_entregado_no_se_da_por_bueno_sin_vigia_verde(cuaderno_de_mentira):
    """EL CORAZON: 'si es correcta, dale otra tarea, sino, dile que corrija'."""
    # La tarea nace CON su guardian nombrado (2026-09-12). Desde que la ley "una opinion no es
    # prueba" tiene quien la haga cumplir, una tarea sin guardian nombrado no se puede cerrar:
    # no habria nada que mirar, y darla por buena seria creerle a quien supervisa. Esta prueba
    # sigue comprobando lo suyo (sin verde no se cierra), ahora con el guardian puesto.
    reparto.asignar("cline", "reparar el diccionario envenenado",
                    vigia="vigias/test_vigia_diccionario_de_julio.py")
    reparto.entregada("cline", "reparar el diccionario envenenado")

    estado, que_hacer = reparto.supervisar("cline", "reparar el diccionario envenenado",
                                           vigia_verde=False)
    assert estado == "a_corregir", (
        "dio por buena una entrega con la vigia ROJA. Eso es exactamente lo que Julio prohibio: "
        "sin verde no se cierra, se manda corregir")
    assert "corrija" in que_hacer, "no dice que hay que mandarle corregir"

    estado, que_hacer = reparto.supervisar("cline", "reparar el diccionario envenenado",
                                           vigia_verde=True)
    assert estado == "correcta", "con la vigia verde no la dio por correcta"
    assert "siguiente" in que_hacer, "no dice que toca darle la siguiente tarea"


def test_lo_entregado_y_no_mirado_se_ve(cuaderno_de_mentira):
    """Una entrega sin supervisar es deuda, no avance. Si no se ve, se cuela."""
    reparto.asignar("cline", "una tarea cualquiera")
    reparto.entregada("cline", "una tarea cualquiera")
    pendientes = reparto.sin_supervisar()
    assert len(pendientes) == 1, "no detecta lo entregado y sin mirar: se daria por avance"
    assert "SIN SUPERVISAR" in reparto.texto(), \
        "el resumen no avisa de lo entregado y sin mirar"


def test_lo_que_no_salio_se_le_cuenta_a_julio(cuaderno_de_mentira):
    """'y me informas si falla'. Si no queda marcado, se acaba escondiendo."""
    reparto.asignar("cline", "algo que no va a salir")
    reparto.fallida("cline", "algo que no va a salir", "no salio tras tres intentos")
    avisos = reparto.para_julio()
    assert len(avisos) == 1, "lo que no salio no queda marcado para contarselo a Julio"
    assert "JULIO" in reparto.texto(), "el resumen no dice que hay que contarselo a Julio"


def test_cline_tiene_tarea_de_verdad_ahora_mismo():
    """Que funcione en el laboratorio no vale: Julio mando trabajar CON Cline, de verdad."""
    if not os.path.exists(reparto.RUTA):
        pytest.fail("no hay ningun reparto de verdad: se legislo trabajar con Cline y no se le "
                    "asigno nada. Escrito no es cumplido")
    with io.open(reparto.RUTA, encoding="utf-8") as f:
        tareas = json.load(f)
    suyas = [t for t in tareas if t.get("quien") == "cline"]
    assert suyas, "Cline no tiene ninguna tarea asignada: se legislo trabajar con el y no se hizo"
    vivas = [t for t in suyas if t.get("estado") in ("asignada", "entregada", "a_corregir")]
    assert vivas or any(t.get("estado") == "correcta" for t in suyas), \
        "Cline no tiene ninguna tarea viva ni ninguna terminada: el reparto es papel mojado"
