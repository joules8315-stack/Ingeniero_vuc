# -*- coding: utf-8 -*-
"""VIGIA — EL QUE MANDA POR EL CANAL A CLAUDE, ESPERA (bloque B8, Julio 2026-09-13).

Julio: "cuando le des un mensaje por el canal a claude, queda atento cada 5 minutos, y espera
una hora en total."

Comprueba la ley entera: contrato escrito, fila en la matriz, ley en el consolidado, indexada en
el mapa del protocolo, candado que frena (marca la espera, exige revisar cada 5 minutos, suelta
al cumplir 1 hora) y vigia que muerde al sabotearla.
"""
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import candado_atento_canal as ac  # noqa: E402


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def _espera_de_prueba():
    """Un entorno aislado para las pruebas: bandeja y esperas falsas (ley 23)."""
    tmp = tempfile.mkdtemp(prefix="espera_test_")
    return {"INGENIERO_CANAL_TEST": os.path.join(tmp, "canal"),
            "INGENIERO_ESPERA_TEST": os.path.join(tmp, "esperas"),
            "INGENIERO_QUIEN": "videca_test"}


def test_contrato_de_la_ley_existe_y_dice_el_ritmo():
    txt = _leer(os.path.join(AQUI, "CONTRATO_ATENTO_AL_CANAL.md"))
    assert "atento" in txt, "el contrato no habla de quedar atento"
    assert "5 minutos" in txt, "el contrato no dice cada 5 minutos"
    assert "una hora" in txt, "el contrato no dice esperar una hora"


def test_la_ley_esta_en_la_matriz_y_en_el_consolidado():
    m = _leer(os.path.join(AQUI, "MATRIZ_LEGISLACION.md"))
    assert "B8" in m and "candado_atento_canal" in m, "la fila B8 no esta en la matriz"
    c = _leer(os.path.join(AQUI, "CONTRATO_LEGISLACION_TOTAL.md"))
    assert "L16" in c and "candado_atento_canal" in c, "la ley L16 no esta en el consolidado"


def test_la_ley_esta_indexada_en_el_mapa_del_protocolo():
    p = _leer(os.path.join(AQUI, "cerebro", "protocolo.py"))
    assert "Atento al canal" in p, "la ley no esta indexada en cerebro/protocolo.py"


def test_el_candado_existe_y_empezar_marca_la_espera():
    assert os.path.exists(os.path.join(AQUI, "arnes", "candado_atento_canal.py")), \
        "falta arnes/candado_atento_canal.py"
    old = dict(os.environ)
    os.environ.update(_espera_de_prueba())
    try:
        d = ac.empezar("yo", 1_000_000)
        assert d.get("de") == "yo", "empezar no devolvio la espera de 'yo'"
        assert float(d.get("enviado_ms", 0)) == 1_000_000, "no guardo la hora de envio"
    finally:
        os.environ.clear()
        os.environ.update(old)


def test_a_la_hora_sin_respuesta_es_vencido():
    old = dict(os.environ)
    os.environ.update(_espera_de_prueba())
    try:
        ac.empezar("yo", 1_000_000)
        e = ac.estado("yo", ahora_ms=1_000_000 + 61 * 60 * 1000)
        assert e["vencido"], "deberia estar vencido despues de 1 hora"
        assert not e["en_espera"], "vencido no puede estar 'en espera'"
    finally:
        os.environ.clear()
        os.environ.update(old)


def test_antes_de_la_hora_sigue_en_espera_sin_revisar():
    old = dict(os.environ)
    os.environ.update(_espera_de_prueba())
    try:
        ac.empezar("yo", 1_000_000)
        e = ac.estado("yo", ahora_ms=1_000_000 + 10 * 60 * 1000)
        assert e["en_espera"], "a los 10 minutos deberia seguir en espera"
        assert not e["vencido"], "a los 10 minutos no puede estar vencido"
        assert e["toca_revisar"], "pasaron 10 min desde el envio sin revisar: toca mirar"
    finally:
        os.environ.clear()
        os.environ.update(old)


def test_si_llega_respuesta_se_recoge_y_termina():
    old = dict(os.environ)
    env = _espera_de_prueba()
    os.environ.update(env)
    try:
        ac.empezar("yo", 1_000_000)
        # una respuesta de claude hacia "yo", posterior al envio
        bandeja = env["INGENIERO_CANAL_TEST"]
        os.makedirs(bandeja, exist_ok=True)
        ruta = os.path.join(bandeja, "%s.json" % int(2_000_000))
        json.dump({"de": "claude", "para": "yo", "texto": "veredicto",
                   "cuando": "2026-09-13 14:00", "leido": False},
                  open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        e = ac.estado("yo", ahora_ms=1_000_000 + 10 * 60 * 1000)
        assert e["respondido"], "deberia detectar la respuesta de claude"
        assert not e["en_espera"], "con respuesta la espera termina"
    finally:
        os.environ.clear()
        os.environ.update(old)


def test_el_ritmo_de_revision_es_cada_5_minutos():
    old = dict(os.environ)
    os.environ.update(_espera_de_prueba())
    try:
        ac.empezar("yo", 1_000_000)
        ac.revisar("yo", ahora_ms=1_000_000 + 4 * 60 * 1000)
        e = ac.estado("yo", ahora_ms=1_000_000 + 8 * 60 * 1000 + 59 * 1000)
        assert not e["toca_revisar"], "no pasaron 5 min desde la revision: no toca"
        e2 = ac.estado("yo", ahora_ms=1_000_000 + 9 * 60 * 1000 + 1000)
        assert e2["toca_revisar"], "pasaron 5 min y un segundo: toca revisar"
    finally:
        os.environ.clear()
        os.environ.update(old)


def test_sabotear_el_ritmo_no_sella():
    """La vigia muerde: si alguien afloja el ritmo o el tope, esto se cae."""
    assert ac.RITMO_SEG == 300, "el ritmo dejo de ser 5 minutos"
    assert ac.TOTAL_SEG == 3600, "el tope dejo de ser una hora"