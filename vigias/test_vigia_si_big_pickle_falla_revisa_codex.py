# -*- coding: utf-8 -*-
"""VIGIA: si Big Pickle no devuelve un JSON, auditar revisa con Codex.

Vigila la funcion `auditar` de cuerpo/obrero.py. No llama a ninguna IA de verdad:
se monkeypatchean las funciones `preguntar` de cuerpo/bigpickle.py y cuerpo/codex.py,
y el relevo de cuerpo/obrero.py.

Tres pruebas:
  (1) el encargo pidio revisa bigpickle, Big Pickle no devuelve JSON -> se le pregunta
      a Codex con el mismo pedido y, si Codex aprueba, auditar devuelve ese veredicto
      con 'codex' como revisor.
  (2) si Big Pickle contesta bien, a Codex NO se le pregunta.
  (3) si quien escribio es codex, Codex NO puede revisar su propio trabajo y se pasa
      al siguiente como hoy.

Se importa lo que se prueba DENTRO de cada prueba, para que el monkeypatch llegue
siempre a la funcion viva.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)


# ---------------------------------------------------------------------------
# Utilidades de las pruebas (sin tocar nada real)
# ---------------------------------------------------------------------------

def _paquete_minimo():
    """Un paquete de encargo pequeno y suficiente para que auditar pueda trabajar."""
    return {
        "tarea": "arreglar un detalle de cuerpo/obrero.py",
        "archivo": "cuerpo/obrero.py",
        "material": "material de mentira para la vigia",
    }


def _propuesta_minima():
    """Una propuesta ya escrita que solo hay que revisar."""
    return {
        "archivo": "cuerpo/obrero.py",
        "texto_nuevo": "# cambio de mentira\n",
        "diagnostico": "cambio de mentira para la vigia",
    }


def _json_aprobado(quien):
    """Un veredicto APROBADO en JSON, tal como lo devolveria un revisor."""
    return json.dumps({
        "veredicto": "APROBADO",
        "invento_algo": False,
        "que_invento": [],
        "fallos": [],
        "riesgo_vecinos": [],
        "que_falta": [],
        "resumen_para_el_jefe": "aprobado por %s (mentira de la vigia)" % quien,
    }, ensure_ascii=False)


def _json_roto():
    """Texto que NO es un JSON: asi se simula que Big Pickle no devuelve JSON."""
    return "esto no es un json, es texto suelto sin llaves ni comillas"


# ---------------------------------------------------------------------------
# PRUEBA 1: Big Pickle no devuelve JSON -> se le pregunta a Codex con el mismo pedido
# ---------------------------------------------------------------------------

def test_si_big_pickle_no_devuelve_json_revisa_codex():
    """Si Big Pickle no devuelve un JSON, auditar pregunta a Codex con el mismo pedido.

    Y si Codex aprueba, auditar devuelve ese veredicto con 'codex' como revisor.
    """
    from cuerpo import obrero
    from cuerpo import bigpickle
    from cuerpo import codex

    pedidos_bp = []
    pedidos_codex = []

    def bp_falso(prompt, timeout=None):
        pedidos_bp.append(prompt)
        return _json_roto(), []

    def codex_falso(prompt, timeout=None, raiz=None):
        pedidos_codex.append(prompt)
        return _json_aprobado("codex"), []

    # El relevo no debe usarse en esta prueba: si se usa, la prueba falla.
    def relevo_falso(*args, **kwargs):
        raise AssertionError("no se debe llamar al relevo en la prueba 1")

    original_bp = bigpickle.preguntar
    original_codex = codex.preguntar
    original_relevo = obrero._preguntar_con_relevo
    original_desperto = obrero.cuotas.desperto
    original_bp_acierto = obrero.cuotas.bigpickle_acierto
    original_bp_fallo = obrero.cuotas.bigpickle_fallo
    original_puede_bp = obrero.cuotas.puede_revisar_bigpickle
    try:
        bigpickle.preguntar = bp_falso
        codex.preguntar = codex_falso
        obrero._preguntar_con_relevo = relevo_falso
        obrero.cuotas.desperto = lambda quien: True
        obrero.cuotas.bigpickle_acierto = lambda: None
        obrero.cuotas.bigpickle_fallo = lambda: None
        obrero.cuotas.puede_revisar_bigpickle = lambda *a, **k: False
        # limpiar la marca de caido que auditar deja pegada en la funcion
        if hasattr(obrero.auditar, "_bp_caido"):
            delattr(obrero.auditar, "_bp_caido")

        auditoria, quien, avisos = obrero.auditar(
            _paquete_minimo(), _propuesta_minima(), auditor="bigpickle")
    finally:
        bigpickle.preguntar = original_bp
        codex.preguntar = original_codex
        obrero._preguntar_con_relevo = original_relevo
        obrero.cuotas.desperto = original_desperto
        obrero.cuotas.bigpickle_acierto = original_bp_acierto
        obrero.cuotas.bigpickle_fallo = original_bp_fallo
        obrero.cuotas.puede_revisar_bigpickle = original_puede_bp
        if hasattr(obrero.auditar, "_bp_caido"):
            delattr(obrero.auditar, "_bp_caido")

    assert pedidos_bp, "Big Pickle tenia que haber sido preguntado"
    assert pedidos_codex, "Codex tenia que haber sido preguntado al fallar Big Pickle"
    assert isinstance(auditoria, dict), "auditar debe devolver un dict"
    assert auditoria.get("veredicto") == "APROBADO", (
        "si Codex aprueba, auditar debe devolver APROBADO; vino: %r" % (auditoria,))
    assert quien == "codex", (
        "el revisor debe ser codex; vino: %r" % (quien,))


# ---------------------------------------------------------------------------
# PRUEBA 2: si Big Pickle contesta bien, a Codex NO se le pregunta
# ---------------------------------------------------------------------------

def test_si_big_pickle_contesta_bien_no_se_pregunta_a_codex():
    """Si Big Pickle devuelve un JSON valido, auditar NO llama a Codex."""
    from cuerpo import obrero
    from cuerpo import bigpickle
    from cuerpo import codex

    pedidos_codex = []

    def bp_falso(prompt, timeout=None):
        return _json_aprobado("bigpickle"), []

    def codex_falso(prompt, timeout=None, raiz=None):
        pedidos_codex.append(prompt)
        return _json_aprobado("codex"), []

    def relevo_falso(*args, **kwargs):
        raise AssertionError("no se debe llamar al relevo en la prueba 2")

    original_bp = bigpickle.preguntar
    original_codex = codex.preguntar
    original_relevo = obrero._preguntar_con_relevo
    original_desperto = obrero.cuotas.desperto
    original_bp_acierto = obrero.cuotas.bigpickle_acierto
    original_bp_fallo = obrero.cuotas.bigpickle_fallo
    original_puede_bp = obrero.cuotas.puede_revisar_bigpickle
    try:
        bigpickle.preguntar = bp_falso
        codex.preguntar = codex_falso
        obrero._preguntar_con_relevo = relevo_falso
        obrero.cuotas.desperto = lambda quien: True
        obrero.cuotas.bigpickle_acierto = lambda: None
        obrero.cuotas.bigpickle_fallo = lambda: None
        obrero.cuotas.puede_revisar_bigpickle = lambda *a, **k: False
        if hasattr(obrero.auditar, "_bp_caido"):
            delattr(obrero.auditar, "_bp_caido")

        auditoria, quien, avisos = obrero.auditar(
            _paquete_minimo(), _propuesta_minima(), auditor="bigpickle")
    finally:
        bigpickle.preguntar = original_bp
        codex.preguntar = original_codex
        obrero._preguntar_con_relevo = original_relevo
        obrero.cuotas.desperto = original_desperto
        obrero.cuotas.bigpickle_acierto = original_bp_acierto
        obrero.cuotas.bigpickle_fallo = original_bp_fallo
        obrero.cuotas.puede_revisar_bigpickle = original_puede_bp
        if hasattr(obrero.auditar, "_bp_caido"):
            delattr(obrero.auditar, "_bp_caido")

    assert not pedidos_codex, (
        "a Codex NO se le debe preguntar si Big Pickle contesta bien; se le pregunto: %r"
        % (pedidos_codex,))
    assert isinstance(auditoria, dict), "auditar debe devolver un dict"
    assert auditoria.get("veredicto") == "APROBADO", (
        "Big Pickle aprobo: auditar debe devolver APROBADO; vino: %r" % (auditoria,))
    assert quien == "bigpickle", (
        "el revisor debe ser bigpickle; vino: %r" % (quien,))


# ---------------------------------------------------------------------------
# PRUEBA 3: si quien escribio es codex, Codex NO revisa su propio trabajo
# ---------------------------------------------------------------------------

def test_codex_no_revisa_su_propio_trabajo():
    """Si evitar='codex', Codex no puede revisar y se pasa al siguiente como hoy.

    Se comprueba que a Codex no se le pregunta y que el revisor final no es codex.
    """
    from cuerpo import obrero
    from cuerpo import bigpickle
    from cuerpo import codex

    pedidos_codex = []
    pedidos_relevo = []

    def bp_falso(prompt, timeout=None):
        # Big Pickle no contesta: asi el flujo tiene que buscar otro revisor.
        return "", ["bigpickle no contesta (mentira de la vigia)"]

    def codex_falso(prompt, timeout=None, raiz=None):
        pedidos_codex.append(prompt)
        return _json_aprobado("codex"), []

    def relevo_falso(prompt, temperatura, evitar=None, primero=None, pesado=False,
                     clase="", vuelta=1):
        pedidos_relevo.append({"evitar": evitar, "primero": primero, "pesado": pesado})
        # El relevo devuelve otro revisor distinto de codex.
        return _json_aprobado("otro"), "otro", []

    original_bp = bigpickle.preguntar
    original_codex = codex.preguntar
    original_relevo = obrero._preguntar_con_relevo
    original_desperto = obrero.cuotas.desperto
    original_bp_acierto = obrero.cuotas.bigpickle_acierto
    original_bp_fallo = obrero.cuotas.bigpickle_fallo
    original_puede_bp = obrero.cuotas.puede_revisar_bigpickle
    try:
        bigpickle.preguntar = bp_falso
        codex.preguntar = codex_falso
        obrero._preguntar_con_relevo = relevo_falso
        obrero.cuotas.desperto = lambda quien: True
        obrero.cuotas.bigpickle_acierto = lambda: None
        obrero.cuotas.bigpickle_fallo = lambda: None
        obrero.cuotas.puede_revisar_bigpickle = lambda *a, **k: False
        if hasattr(obrero.auditar, "_bp_caido"):
            delattr(obrero.auditar, "_bp_caido")

        auditoria, quien, avisos = obrero.auditar(
            _paquete_minimo(), _propuesta_minima(), auditor="bigpickle", evitar="codex")
    finally:
        bigpickle.preguntar = original_bp
        codex.preguntar = original_codex
        obrero._preguntar_con_relevo = original_relevo
        obrero.cuotas.desperto = original_desperto
        obrero.cuotas.bigpickle_acierto = original_bp_acierto
        obrero.cuotas.bigpickle_fallo = original_bp_fallo
        obrero.cuotas.puede_revisar_bigpickle = original_puede_bp
        if hasattr(obrero.auditar, "_bp_caido"):
            delattr(obrero.auditar, "_bp_caido")

    assert not pedidos_codex, (
        "Codex no puede revisar su propio trabajo: no se le debe preguntar; se le pregunto: %r"
        % (pedidos_codex,))
    assert pedidos_relevo, "el relevo tenia que haber sido consultado para buscar otro revisor"
    assert quien != "codex", (
        "el revisor no puede ser codex cuando codex escribio; vino: %r" % (quien,))
    assert isinstance(auditoria, dict), "auditar debe devolver un dict"


if __name__ == "__main__":
    test_si_big_pickle_no_devuelve_json_revisa_codex()
    test_si_big_pickle_contesta_bien_no_se_pregunta_a_codex()
    test_codex_no_revisa_su_propio_trabajo()
    print("OK: las tres pruebas de la vigia pasaron")
