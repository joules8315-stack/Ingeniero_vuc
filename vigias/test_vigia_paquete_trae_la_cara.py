# -*- coding: utf-8 -*-
"""VIGIA 8 — EL PAQUETE TRAE LA CARA, NO SOLO EL MOTOR.

Fallo REAL del 2026-08-20, y quien lo cazo NO fue ninguna de las 26 vigias que estaban verdes:
lo cazaron Qwen y Gemini. El paquete del onboarding traia `cuerpo/perfil.py` (el motor) pero
NO `web/` (la cara, donde esta el formulario que de verdad guarda). Qwen pregunto: "no veo el
codigo que invoca a guardar_perfil". Gemini rechazo la reparacion. Los dos tenian razon.

Es exactamente la leccion C25/C26 de Julio: vigia verde sobre un caso que el usuario no vive.
El usuario NO vive `perfil.py`: vive el formulario de la pantalla.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import router, grafo


def _hay(a):
    p = grafo.proyectos()
    return a in p and os.path.isdir(p[a]["ruta"])


@pytest.mark.parametrize("problema", [
    "el onboarding asesorado no guarda el perfil de la empresa",
    "el formulario de la empresa no guarda lo que escribo",
])
def test_un_problema_de_pantalla_trae_la_pantalla(problema):
    if not _hay("dmm"):
        pytest.skip("dmm no esta en esta maquina")
    pk = router.armar("dmm", problema)
    ids = [f["id"] for f in pk["codigo"]]
    assert any(i.startswith("web/") for i in ids), (
        "el paquete trae solo el motor y no la cara. Ids: " + str(ids))


def test_los_llamadores_entran_al_flujo():
    """Quien IMPORTA una pieza del flujo pertenece al flujo, aunque su nombre no lo diga."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    pk = router.armar("dmm", "el onboarding no guarda el perfil")
    ids = {f["id"] for f in pk["codigo"]}
    g = grafo.cargar("dmm")
    from cerebro import enlaces
    _, entra = enlaces.indexar(g["enlaces"])
    # alguien que importe a perfil.py tiene que estar en el paquete
    llaman = {e["de"] for e in entra.get("cuerpo/perfil.py", []) if e["tipo"] == "IMPORTA"}
    assert llaman & ids, f"ninguno de los que llaman a perfil.py entro al paquete: {sorted(llaman)[:6]}"


def test_el_paquete_avisa_de_los_fallos_ya_vividos():
    """Orden 6.1: memoria de fallos dentro del paquete, para no tropezar dos veces."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    from cuerpo import fallos
    # Se siembra en una copia APARTE: escribir en la memoria de verdad hacia que dos corridas
    # simultaneas se pisaran y salieran rojas sin estar nada roto (fallo real 2026-08-21).
    import tempfile
    aparte = os.path.join(tempfile.mkdtemp(), "FALLOS.json")
    viejo = os.environ.get("INGENIERO_FALLOS_TEST")
    os.environ["INGENIERO_FALLOS_TEST"] = aparte
    try:
        fallos.sembrar()
        txt = router.a_texto(router.armar("dmm", "el onboarding no guarda el perfil en la web"))
        assert "LO QUE YA NOS PASO AQUI" in txt, "el paquete no lleva la memoria de fallos"
    finally:
        if viejo:
            os.environ["INGENIERO_FALLOS_TEST"] = viejo
        else:
            os.environ.pop("INGENIERO_FALLOS_TEST", None)


def test_sigue_siendo_barato_despues_de_traer_la_cara():
    """Traer la cara no puede convertir el paquete en 'leer medio proyecto'."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    pk = router.armar("dmm", "el onboarding no guarda el perfil")
    n = len(router.a_texto(pk).splitlines())
    ahorro = 100 - n * 100 / max(1, pk["total_proyecto"])
    assert ahorro >= 90, f"al traer la cara el ahorro cayo a {ahorro:.1f}%"
