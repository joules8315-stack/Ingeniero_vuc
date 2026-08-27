# -*- coding: utf-8 -*-
"""VIGIA 3 — NO INVENTA (ley dura de Julio: sin alucinar).

Todo lo que el paquete nombra tiene que EXISTIR en el disco. Si algo no existe, el paquete
debe decir NO_ENCONTRADO, nunca rellenar.
"""
import os, re, sys, json
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
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


def test_la_terminal_no_es_via_para_inventar_ni_saltarse_el_equipo():
    """Julio, 2026-08-27: escribir codigo por la terminal se saltaba el candado de equipo, que
    solo vigila la herramienta de editar. Eso era una rendija por donde se colaba trabajo que no
    estaba consignado en el mapa ni legislado. Conectado aqui, a la vigia de NO INVENTAR:
    lo que se escribe tiene que ser conforme a lo consignado y pasar por el equipo, no una
    alucinacion por la ventana de la terminal.
    """
    # 1) la terminal esta conectada al candado (en usuario o proyecto, no quedo suelta)
    import _config
    pre = _config.comandos("PreToolUse")
    assert any("bash" in m.lower() for m, _ in pre), "la terminal no esta conectada a ningun candado"
    assert any("candado_terminal" in c for _, c in pre), "candado_terminal no esta en la terminal"

    # 2) escribir codigo por la terminal exige el equipo: rechaza algo no consignado/aprobado
    import candado_terminal as ct
    import subprocess, io, tempfile
    env = dict(os.environ)
    env["INGENIERO_SIN_PAQUETE_TEST"] = "1"
    env["INGENIERO_APAGONES_TEST"] = os.path.join(tempfile.gettempdir(), "apagones_no_inventa.log")
    d = tempfile.mkdtemp()
    env["INGENIERO_VEREDICTO_TEST"] = os.path.join(d, "v.json")   # sin veredicto: nada aprobado
    proy = grafo.proyectos().get("foto_informe")
    if not proy or not os.path.isdir(proy["ruta"]):
        import pytest as _pt
        _pt.skip("foto_informe no esta")
    fp = os.path.join(proy["ruta"], "algo.py").replace("\\", "/")
    p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_terminal.py")],
                       input=json.dumps({"tool_name": "Bash",
                                         "tool_input": {"command": 'echo "x=1" > "%s"' % fp}}),
                       capture_output=True, text=True, env=env, timeout=120)
    assert p.returncode == 2, "escribir codigo por terminal sin equipo no se freno"
