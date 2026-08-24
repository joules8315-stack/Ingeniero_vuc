# -*- coding: utf-8 -*-
"""VIGIA — EL BUCLE AI-AI ES AUTOMATICO Y NO SE DESBOCA (Julio, 2026-08-24).

Julio: "que se comuniquen (Claude y Cline), pero que sea fluido, que yo no tenga que intervenir,
porque sino no es automatico. Crea los disparadores o las vigias que hagan que su comunicacion
sea fluida."

La respuesta automatica es el bucle (arnes/loop.py): vigila el ENCARGO en segundo plano, lo manda
al EQUIPO y le devuelve el resultado al otro, sin que Julio toque nada. Pero un bucle automatico
que no tiene freno quema plata y da vueltas eternas. Esta vigia comprueba los FRENOS:

  · sin encargo, espera (no trabaja solo por gusto),
  · tiene tope de vueltas (no da vueltas para siempre),
  · se puede PARAR de una vez,
  · procesa y responde por el canal al otro (fluido).
"""
import os
import sys
import json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import loop  # noqa: E402


def _caja(tmp_path, monkeypatch):
    """Cada prueba con su copia del buzón (ley 23): no se toca el de verdad."""
    monkeypatch.setenv("INGENIERO_LOOP_TEST_DIR", str(tmp_path))
    return tmp_path


def test_sin_encargo_el_bucle_espera(tmp_path, monkeypatch):
    _caja(tmp_path, monkeypatch)
    assert loop.paso(procesar=False) == "sin encargo", \
        "el bucle trabajo sin encargo: se desboca"


def test_iniciar_deja_el_encargo(tmp_path, monkeypatch):
    _caja(tmp_path, monkeypatch)
    loop.iniciar("dmm", "el problema", para="claude", de="cline")
    e = loop._encargo()
    assert e and e["para"] == "claude" and e["de"] == "cline"
    assert e["vuelta"] == 0


def test_el_tope_termina_el_encargo(tmp_path, monkeypatch):
    _caja(tmp_path, monkeypatch)
    loop.iniciar("dmm", "el problema", rondas_max=2)
    # se simula que ya se gastaron las vueltas
    e = loop._encargo()
    e["vuelta"] = 2
    json.dump(e, open(loop._ruta_de(loop.ENCARGO), "w", encoding="utf-8"), ensure_ascii=False)
    assert loop.paso(procesar=False) == "tope", "el tope no paro el bucle"
    assert loop._encargo() is None, "el encargo no se cerro al llegar al tope"


def test_se_puede_parar_de_una_vez(tmp_path, monkeypatch):
    _caja(tmp_path, monkeypatch)
    loop.iniciar("dmm", "el problema")
    loop.parar()
    assert loop.paso(procesar=False) == "parado", "PARAR no freno el bucle"


def test_el_bucle_devuelve_al_otro_por_el_canal():
    """La comunicacion es fluida: el resultado va al destinatario (canal de salida)."""
    txt = open(os.path.join(AQUI, "arnes", "loop.py"), encoding="utf-8").read()
    assert "canal.enviar(e[\"para\"]" in txt, "el bucle no responde por el canal al otro"
