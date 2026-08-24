# -*- coding: utf-8 -*-
"""VIGIA — CADA INSTRUCCION SE LEGISLA (bloque B3, legislacion 2026-08-24).

Julio, 2026-08-24: con cada instruccion suya hay que analizarla, legislarla, agregarla a la tabla
de la verdad y la matriz, dividirla en bloques, indexarla, crearle vigias y aplicar el arnes, para
que lo que se repara no destruya algo que sirva.

Comprueba que la legislacion del 2026-08-24 quedo completa: contrato, matriz, leyes en el mapa,
candados conectados y el ciclo de "si se logro avisa a Julio / si no se aprendio y se reinicia".
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_contrato_de_legislacion_existe():
    assert os.path.exists(os.path.join(AQUI, "CONTRATO_LEGISLACION_2026-08-24.md")), \
        "falta el contrato de legislacion"


def test_matriz_y_tabla_de_la_verdad_existe():
    txt = _leer(os.path.join(AQUI, "MATRIZ_LEGISLACION.md"))
    assert "B1" in txt and "B2" in txt and "B3" in txt, "la matriz no tiene los bloques"


def test_leyes_en_el_mapa_de_la_forma_de_trabajo():
    txt = _leer(os.path.join(AQUI, "cerebro", "protocolo.py"))
    assert "Siempre en equipo, sin salto" in txt, "la ley de equipo total no esta en el mapa"
    assert "Probar de verdad antes de pedir a Julio" in txt, "la ley de prueba real no esta en el mapa"


def test_candado_de_prueba_real_existe_y_esta_conectado():
    assert os.path.exists(os.path.join(AQUI, "arnes", "candado_prueba_real.py")), \
        "falta el candado de prueba real"
    txt = _leer(os.path.join(AQUI, "cerebro", "protocolo.py"))
    assert "candado_prueba_real" in txt, "el candado de prueba real no esta conectado en el paso 7"


def test_el_ciclo_segun_resultado_esta_legislado():
    """B2.1 si se logra -> avisar a Julio; B2.2 si no -> aprender y reiniciar."""
    txt = _leer(os.path.join(AQUI, "CONTRATO_LEGISLACION_2026-08-24.md")).lower()
    assert "avisarle a julio" in txt or "avisar" in txt, "falta el 'avisar a Julio' si se logro"
    assert "reiniciar el ciclo" in txt, "falta el 'reiniciar' si no se logro"
    assert "sin excusas" in txt, "falta el 'sin excusas'"
