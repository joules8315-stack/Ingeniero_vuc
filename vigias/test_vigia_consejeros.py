# -*- coding: utf-8 -*-
"""VIGIA 11 — LOS CONSEJEROS NO PUEDEN DECIR LO CONTRARIO DE LO QUE PASO.

Fallo REAL del 2026-08-20: los dos consejeros RECHAZARON una decision (borrar los respaldos)
y el resumen decia "COINCIDEN -> la decision tiene buena pinta". Coincidian, si... en decir
que NO. Un resumen que dice lo contrario de lo que paso es peor que no tener resumen: se lee
la primera linea, se da por bueno, y se hace justo lo que los dos desaconsejaban.

Aqui se prueba la LOGICA del veredicto sin gastar ni una llamada a los cerebros.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cuerpo import consejeros


def _fingir(votos):
    """Arma un resultado como si los cerebros hubieran contestado eso."""
    ops = [{"cerebro": f"c{i}", "de_acuerdo": v, "riesgo_principal": "x", "confianza": "media"}
           for i, v in enumerate(votos)]
    validas = ops
    coinciden, veredicto = None, "?"
    if len(validas) >= 2:
        s = {bool(o["de_acuerdo"]) for o in validas}
        coinciden = len(s) == 1
        veredicto = ("APRUEBAN" if True in s else "RECHAZAN") if coinciden else "DISCREPAN"
    elif len(validas) == 1:
        veredicto = "APRUEBA" if validas[0]["de_acuerdo"] else "RECHAZA"
    return {"pregunta": "p", "porque": "", "proyecto": None, "opiniones": ops,
            "coinciden": coinciden, "veredicto": veredicto, "material_chars": 0, "segundos": 1.0}


def test_los_dos_rechazan_NO_puede_decir_buena_pinta():
    """El fallo exacto del 2026-08-20."""
    txt = consejeros.informe(_fingir([False, False]))
    assert "RECHAZAN" in txt, "no dice que la rechazan"
    assert "buena pinta" not in txt.lower(), \
        "los dos la rechazaron y el informe dice que tiene buena pinta"


def test_los_dos_aprueban_se_dice_claro():
    txt = consejeros.informe(_fingir([True, True]))
    assert "APRUEBAN" in txt and "buena pinta" in txt.lower()


def test_si_discrepan_se_destaca():
    """El desacuerdo es la señal mas util: no puede pasar desapercibido."""
    txt = consejeros.informe(_fingir([True, False]))
    assert "DISCREPAN" in txt
    assert "***" in txt, "el desacuerdo tiene que saltar a la vista"


def test_una_sola_opinion_no_se_vende_como_contraste():
    txt = consejeros.informe(_fingir([True]))
    assert "una sola opinion" in txt.lower() or "solo contesto uno" in txt.lower()


def test_siempre_recuerda_que_es_opinion_no_prueba():
    """Ley 5 de Julio: nada de esto sustituye a que el lo vea."""
    for votos in ([True, True], [False, False], [True, False]):
        assert "no es una prueba" in consejeros.informe(_fingir(votos)).lower() or \
               "opinion" in consejeros.informe(_fingir(votos)).lower()


def test_el_material_sale_del_grafo_no_del_repo():
    """Los consejeros opinan sobre pedazos, no sobre el proyecto entero."""
    import inspect
    src = inspect.getsource(consejeros._material)
    assert "Buscador" in src, "no usa el buscador de trozos del grafo"
    assert "k=3" in inspect.signature(consejeros._material).__str__() or "k=3" in src
