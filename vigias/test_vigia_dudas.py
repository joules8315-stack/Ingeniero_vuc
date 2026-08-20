# -*- coding: utf-8 -*-
"""VIGIA 13 — BUSCAR PRIMERO, PREGUNTAR DESPUES... PERO SIN MENTIR (Ley 16).

  Julio: "primero busque en los repositorios la respuesta, solo cuando no la halle, pregunte,
   siempre debe hacerlas, aun mas si pierde el contexto"

El peligro de esta pieza no es preguntar de mas: es dar por RESUELTA una duda que nadie ha
contestado. Si eso pasa, se asume — y asumir es justo lo que Julio prohibio.

FALLO REAL (2026-08-20, y es la TERCERA vez que se comete el mismo error en el dia):
se pregunto "de que color quiere Julio el boton de aprobar" —algo que no esta escrito en
ningun sitio— y contesto "RESUELTA sin molestar a Julio", trayendo contratos que no venian
al caso. Antes paso igual con el buscador de habilidades y con el de trozos.
La causa siempre es la misma: **cualquier texto "se parece" si no se exige la palabra que
de verdad distingue**.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cuerpo import dudas
from cerebro import grafo


def _hay(a):
    p = grafo.proyectos()
    return a in p and os.path.isdir(p[a]["ruta"])


def test_lo_que_NO_esta_escrito_se_pregunta():
    """El caso exacto del fallo."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    r = dudas.resolver("de que color quiere Julio el boton de aprobar", "dmm")
    assert r["hay_que_preguntar"], (
        "dio por resuelta una duda que no esta escrita en ningun sitio. "
        f"Se invento estas fuentes: {[h['donde'] for h in r['hallado']]}")


@pytest.mark.parametrize("duda", [
    "cuantos empleados tiene la empresa de Julio",
    "que dia de la semana prefiere Julio para publicar",
    "zzzqqq xyzzy pregunta que no existe",
])
def test_varias_dudas_no_escritas_se_preguntan(duda):
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    r = dudas.resolver(duda, "dmm")
    assert r["hay_que_preguntar"], f"'{duda}' no esta escrita y dijo que si: {r['hallado'][:1]}"


def test_lo_que_SI_esta_escrito_no_molesta_a_julio():
    """La otra mitad: si la respuesta existe en CUALQUIERA de las cuatro fuentes, no se pregunta.

    (Esta vigia estaba mal escrita: exigia que la respuesta viniera de un CONTRATO. La encontro
    en la memoria de fallos, que es una fuente igual de valida —de hecho la mas util, porque es
    algo que ya vivimos—. Se corrigio la vigia, no el codigo.)"""
    if not _hay("ingeniero"):
        pytest.skip("ingeniero no esta")
    r = dudas.resolver("relevo de cuotas entre los cerebros gratis", "ingeniero")
    assert not r["hay_que_preguntar"], "esta escrito y aun asi iba a molestar a Julio"
    assert any(h["fuente"] in ("CONTRATO", "CODIGO", "FALLO YA VIVIDO", "YA DECIDIDO")
               for h in r["hallado"]), f"fuentes raras: {[h['fuente'] for h in r['hallado']]}"


def test_el_historial_no_responde_por_una_palabra_suelta():
    """El historial del estado traia 'PRUEBA: una pregunta para Julio' para cualquier duda
    que llevara la palabra 'pregunta'. Hacen falta al menos DOS palabras distintivas."""
    from cuerpo import estado
    antes = estado.leer().get("problema", "")
    try:
        estado.apuntar(problema="una pregunta cualquiera de prueba")
        r = dudas.resolver("de que color quiere Julio el boton de aprobar", "dmm")
        malos = [h for h in r["hallado"] if h["fuente"] == "YA DECIDIDO"]
        assert not malos, f"el historial contesto por una palabra suelta: {malos}"
    finally:
        estado.apuntar(problema=antes)


def test_la_pregunta_dice_donde_se_busco():
    """Preguntar sin decir donde se busco parece pereza; diciendolo, es un informe."""
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    txt = dudas.formular("de que color quiere Julio el boton de aprobar")
    assert "PREGUNTA_REQUERIDA" in txt
    assert "busque" in txt.lower(), "no dice que ya se busco antes de preguntar"


def test_la_pregunta_queda_apuntada_para_que_no_se_olvide():
    """Si no se apunta, se pierde. El candado de cierre la exige."""
    from cuerpo import estado
    antes = estado.leer().get("decision_pendiente", "")
    try:
        estado.apuntar(decision_pendiente="")
        dudas.apuntar_pregunta("zzzqqq una duda que no existe en ningun sitio", "dmm")
        assert estado.leer().get("decision_pendiente"), "la pregunta no quedo apuntada"
    finally:
        estado.apuntar(decision_pendiente=antes)
