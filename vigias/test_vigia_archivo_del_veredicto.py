# -*- coding: utf-8 -*-
"""VIGIA — un APROBADO sobre OTRO archivo no vale.

FALLO REAL (2026-08-24, Foto Informe). El encargo era reparar una prueba concreta. El reparador
diagnostico bien los defectos, pero dijo tocar OTRA prueba distinta, que estaba sana. Las tres
rondas apuntaron al archivo equivocado y el JUEZ firmo APROBADO igual. Aplicarlo habria
reescrito lo que funciona y dejado lo roto como estaba, con el sello del equipo encima — que es
lo peor, porque da confianza.

POR QUE PASO: comprobar que el archivo reparado es el archivo roto se estaba dejando al
criterio del juez. El mismo juez SI lo caza a veces (ese mismo dia, en DMM, escribio "existe
una discrepancia de ubicacion"), y otras veces no. Comparar dos nombres es mecanico: no puede
depender de que un cerebro se acuerde.

LEY QUE APLICA (Foto Informe, 2026-07-23): "un recordatorio se ignora; solo un candado que
FRENA se cumple". Por eso esto no es un aviso al juez: es un freno que tumba el APROBADO.

Test-first: esta vigia se escribio ANTES del candado y nacio ROJA.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))

candado = pytest.importorskip(
    "candado_archivo_del_veredicto",
    reason="todavia no existe el candado que compara el archivo reparado con el del encargo")

ROTO = "la_prueba_rota.py"       # lo que pedia el encargo
SANO = "la_prueba_sana.py"       # lo que el reparador dijo tocar
ENCARGO = [ROTO]


def test_el_caso_real_se_atrapa():
    """Encargo: el archivo roto. El reparador dijo otro. Tiene que caerse."""
    motivo = candado.se_equivoco_de_archivo(SANO, ENCARGO)
    assert motivo, "dejo pasar un APROBADO sobre un archivo que NO era el del encargo"
    assert SANO in motivo, "el motivo no dice que archivo se toco de mas"
    assert ROTO in motivo, "el motivo no dice cual era el del encargo"


def test_el_archivo_correcto_pasa():
    """Si repara lo que se pidio, no estorba. Un freno que frena siempre tapia la puerta."""
    assert not candado.se_equivoco_de_archivo(ROTO, ENCARGO)


def test_da_igual_la_carpeta_las_barras_y_las_mayusculas():
    """El reparador escribe la ruta como quiere; el freno no puede caerse por eso."""
    for escrito in (ROTO, "./" + ROTO, r"C:\Users\USER\dev\proy" + "\\" + ROTO, ROTO.upper()):
        assert not candado.se_equivoco_de_archivo(escrito, ENCARGO), \
            "se cayo por como estaba escrita la ruta: " + escrito


def test_si_no_dice_que_archivo_toca_tampoco_pasa():
    """Ley 2 de Julio: nunca inventar. Si no se sabe que toco, NO se aprueba."""
    for vacio in ("", "   ", "NO_ENCONTRADO", None):
        assert candado.se_equivoco_de_archivo(vacio, ENCARGO), \
            "aprobo sin que el reparador dijera que archivo toca: %r" % (vacio,)


def test_varios_archivos_en_el_encargo():
    """El encargo puede traer varias piezas: vale cualquiera de ellas, y solo ellas."""
    encargo = [ROTO, "otra_pieza.py"]
    assert not candado.se_equivoco_de_archivo("otra_pieza.py", encargo)
    assert candado.se_equivoco_de_archivo("app.py", encargo)


def test_si_el_encargo_no_trae_archivos_no_se_aprueba_a_ciegas():
    """Sin nada con que comparar no se puede decir que esta bien. Vigia verde NO es prueba."""
    assert candado.se_equivoco_de_archivo(ROTO, [])


def test_el_veredicto_completo_se_tumba():
    """La puerta de verdad: un APROBADO del juez sobre otro archivo sale rechazado."""
    final, motivo = candado.revisar_veredicto("APROBADO", SANO, ENCARGO)
    assert final != "APROBADO", "el APROBADO sobrevivio al archivo equivocado"
    assert motivo

    final, motivo = candado.revisar_veredicto("APROBADO", ROTO, ENCARGO)
    assert final == "APROBADO", "tumbo un APROBADO que estaba bien"
    assert not motivo


def test_lo_que_ya_venia_mal_sigue_mal():
    """El freno solo quita aprobados; no asciende a nadie."""
    final, _ = candado.revisar_veredicto("NO_APROBADO", ROTO, ENCARGO)
    assert final == "NO_APROBADO"
