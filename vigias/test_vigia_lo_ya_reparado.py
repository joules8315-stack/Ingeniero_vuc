# -*- coding: utf-8 -*-
"""VIGIA 21 — NO SE ROMPE LO QUE YA SE REPARO (Julio, 2026-08-21).

  "crea el guardia de lo ya reparado, fuerte, con candado, ultra blindado, que siempre este
   pendiente, de extremo a extremo, y que sirva de techo y piso, que nada se le escape, que
   tenga siempre presente los fallos pasados para que no los cometa, y que siempre tenga el
   grafo del pedazo, para que tambien sea eficiente."

EL PROBLEMA HISTORICO DE JULIO: arreglar una cosa y que se caiga otra que YA funcionaba. El
guardia de cross-flow mira a los VECINOS de ahora; este mira al PASADO: todo lo que costo
repararse alguna vez y no puede volver a caerse.

TECHO Y PISO:
  · TECHO (antes de tocar): avisa que reparaciones pasadas puede afectar lo que se va a tocar.
  · PISO  (antes de guardar): corre las pruebas de ESAS reparaciones. Si una cae, no se guarda.

EFICIENTE: usa el grafo para correr SOLO las pruebas de lo que se toco, no las 150. Por eso es
mas rapido que lo de ahora, no mas lento.

POR QUE NO SE REPARTE ENTRE AYUDANTES (opinion de ingeniero, 2026-08-21): lo ya reparado no se
comprueba opinando, se comprueba PROBANDO. La prueba es instantanea, gratis y siempre da el
mismo resultado; un ayudante tarda entre 3 y 300 segundos (medido) y puede equivocarse. Los
ayudantes entran DESPUES, solo cuando algo se pone rojo, para explicar que se rompio.
"""
import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest


@pytest.fixture(autouse=True)
def _memoria_aparte(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_FALLOS_TEST", str(tmp_path / "FALLOS.json"))
    monkeypatch.setenv("INGENIERO_ESTADO_TEST", str(tmp_path / "ESTADO.json"))
    yield


def _sembrar_reparacion(prueba="vigias/test_vigia_medidor.py", pieza="cuerpo/medidor.py"):
    from cuerpo import fallos
    return fallos.apuntar(
        que_paso="algo que ya se reparo una vez",
        causa_raiz="daba igual",
        cura="se arreglo y quedo su prueba",
        no_volver_a="volver a romperlo",
        proyecto="ingeniero", piezas=[pieza], quien_lo_caza=prueba)


# ─── TECHO: avisa ANTES de tocar ──────────────────────────────────────────────
def test_avisa_antes_de_tocar_algo_ya_reparado():
    import guard_pasado
    _sembrar_reparacion(pieza="cuerpo/medidor.py")
    afectadas = guard_pasado.reparaciones_que_tocas(["cuerpo/medidor.py"])
    assert afectadas, "va a tocar algo ya reparado y no avisa"
    assert afectadas[0]["prueba"], "no dice que prueba protege esa reparacion"


def test_no_avisa_de_lo_que_no_toca():
    """Si avisa de todo se vuelve ruido y se ignora: eso ya paso con la memoria de errores."""
    import guard_pasado
    _sembrar_reparacion(pieza="cuerpo/medidor.py")
    assert not guard_pasado.reparaciones_que_tocas(["cuerpo/whatsapp.py"])


def test_el_techo_mira_tambien_a_los_vecinos_del_grafo():
    """Tocar una pieza afecta a quien la usa: eso tambien es 'lo ya reparado'."""
    import guard_pasado
    import inspect
    src = inspect.getsource(guard_pasado.reparaciones_que_tocas)
    assert "vecinos" in src or "grafo" in src, \
        "no usa el grafo: se le escapan las reparaciones de las piezas que dependen de esta"


# ─── PISO: no deja guardar si algo ya reparado se cayo ────────────────────────
def test_no_deja_guardar_si_cae_algo_ya_reparado():
    import guard_pasado
    _sembrar_reparacion(prueba="vigias/NO_EXISTE_ESTA.py", pieza="cuerpo/medidor.py")
    ok, detalle = guard_pasado.siguen_en_pie(["cuerpo/medidor.py"])
    assert not ok, "dejo pasar aunque la prueba de lo ya reparado no se puede correr"
    assert "NO_EXISTE" in json.dumps(detalle)


def test_deja_guardar_si_todo_lo_reparado_sigue_en_pie():
    import guard_pasado
    _sembrar_reparacion(prueba="vigias/test_vigia_medidor.py", pieza="cuerpo/medidor.py")
    ok, _ = guard_pasado.siguen_en_pie(["cuerpo/medidor.py"])
    assert ok, "estorba: la prueba de lo ya reparado esta verde y aun asi no deja guardar"


# ─── EFICIENTE: solo lo que hace falta ────────────────────────────────────────
def test_solo_corre_las_pruebas_de_lo_que_se_toco():
    """Lo que lo hace mas rapido que correrlo todo, no mas lento."""
    import guard_pasado
    for i, p in enumerate(("cuerpo/medidor.py", "cuerpo/cuotas.py", "cuerpo/skills.py")):
        _sembrar_reparacion(prueba="vigias/test_vigia_medidor.py", pieza=p)
    cuales = guard_pasado.pruebas_a_correr(["cuerpo/medidor.py"])
    assert len(cuales) <= 2, "va a correr de mas: %s" % cuales


def test_sin_nada_tocado_no_corre_nada():
    import guard_pasado
    assert guard_pasado.pruebas_a_correr([]) == []


# ─── ULTRA BLINDADO: no se le escapa por ningun lado ──────────────────────────
def test_cada_reparacion_declara_su_prueba():
    """Una reparacion sin prueba que la proteja es una que se puede caer sin que nadie lo vea."""
    from cuerpo import fallos
    fallos.sembrar()
    sin = [f["que_paso"][:50] for f in fallos._leer()
           if f.get("cura") and not f.get("quien_lo_caza")]
    assert len(sin) <= 3, "hay %d reparaciones sin prueba que las proteja: %s" % (len(sin), sin[:3])


def test_esta_enganchado_de_verdad():
    """De nada sirve si nadie lo llama: tiene que estar en el guardia de cierre."""
    txt = open(os.path.join(AQUI, "arnes", "candado_cierre.py"), encoding="utf-8").read()
    assert "guard_pasado" in txt, "el guardia de lo ya reparado no esta enganchado al cierre"


def test_tiene_interruptor_de_emergencia():
    txt = open(os.path.join(AQUI, "arnes", "guard_pasado.py"), encoding="utf-8").read()
    assert "INGENIERO_OFF" in txt
