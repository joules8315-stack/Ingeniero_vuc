# -*- coding: utf-8 -*-
"""VIGIA 3 — NO INVENTA (ley dura de Julio: sin alucinar).

Todo lo que el paquete nombra tiene que EXISTIR en el disco. Si algo no existe, el paquete
debe decir NO_ENCONTRADO, nunca rellenar.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import router, grafo


def _hay(apodo):
    prs = grafo.proyectos()
    return apodo in prs and os.path.isdir(prs[apodo]["ruta"])


@pytest.mark.parametrize("apodo,problema", [
    ("dmm", "el onboarding no guarda el perfil"),
    ("dmm", "algo rarisimo que no existe en este proyecto zzzqqq"),
])
def test_todo_lo_que_nombra_existe(apodo, problema):
    if not _hay(apodo):
        pytest.skip("dmm no esta en esta maquina")
    pk = router.armar(apodo, problema)
    for f in pk["fichas"] + pk["codigo"] + pk["leyes"] + pk["vigias"]:
        assert os.path.exists(f["abs"]), f"el paquete nombra {f['id']} y NO existe en el disco"


def test_las_lineas_de_los_trozos_existen_de_verdad():
    if not _hay("dmm"):
        pytest.skip("dmm no esta en esta maquina")
    pk = router.armar("dmm", "el onboarding no guarda el perfil")
    fichas = {f["id"]: f for f in pk["fichas"]}
    for t in pk["trozos"]:
        f = fichas.get(t["pieza"])
        assert f, f"el trozo {t['direccion']} apunta a una pieza que no esta en el paquete"
        assert t["hasta"] <= f["lineas"] + 1, \
            f"el trozo {t['direccion']} apunta a la linea {t['hasta']} pero el archivo tiene {f['lineas']}"


def test_cuando_no_hay_nada_lo_dice_en_vez_de_inventar():
    if not _hay("dmm"):
        pytest.skip("dmm no esta en esta maquina")
    txt = router.a_texto(router.armar("dmm", "zzzqqq xyzzy no existe nada de esto"))
    assert "NO_ENCONTRADO" in txt, "cuando no encuentra, debe decir NO_ENCONTRADO"


def test_proyecto_inexistente_no_se_inventa():
    from cerebro import grafo as g
    with pytest.raises(SystemExit) as e:
        g.cargar("proyecto_que_no_existe_jamas")
    assert "NO_ENCONTRADO" in str(e.value)
