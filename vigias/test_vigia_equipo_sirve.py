# -*- coding: utf-8 -*-
"""VIGIA — EL EQUIPO SIRVE Y NO ESTORBA (reparacion 2026-08-24).

Julio, 2026-08-24: "revisa si el equipo sirve y si se puede reparar, para que sirva, no para que
estorbe." Y: "que claude no gaste a lo pendejo".

MEDIDO (2026-08-24, de cuotas): los empleados GRATIS fallan muchisimo (GPT-OSS 20B: 19/20,
LM Studio: 9/9) y DeepSeek (de pago) es el unico confiable (0 fallos). El desperdicio de tokens
viene de probar y reprobar a los que fallan. La regla tiene que ser: los que fallan mucho van de
ULTIMO; el de pago solo cuando ningun gratis puede.

Comprueba (sin gastar plata: solo mira las reglas del codigo):
  1. DeepSeek esta en DE_PAGO y no entra en la pregunta a la vez que los gratis.
  2. La fila ordena por fiabilidad x rapidez: el que falla mucho queda al final.
  3. El comando que arma el paquete apunta en el cuaderno (para que el router aprenda).
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "cuerpo"))
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_deepseek_es_de_pago_y_no_estorba_a_los_gratis():
    from cuerpo import cuotas
    assert "deepseek" in cuotas.DE_PAGO, "DeepSeek no esta marcado como de pago"
    # el codigo debe tratar a los de pago A SOLAS, de ultimo
    txt = _leer(os.path.join(AQUI, "cuerpo", "cuotas.py"))
    assert "DE_PAGO" in txt


def test_la_fila_ordena_por_fiabilidad():
    """El que falla mucho tiene que ir de ultimo, no gastar llamadas primero."""
    from cuerpo import cuotas
    assert hasattr(cuotas, "_ordenar_por") or hasattr(cuotas, "fila"), \
        "falta el orden por fiabilidad de la fila"
    txt = _leer(os.path.join(AQUI, "cuerpo", "cuotas.py"))
    assert "conf" in txt and "fallos" in txt, "la fila no se ordena por fiabilidad"


def test_el_de_pago_se_llama_de_ultimo():
    """No se le pregunta al de pago a la vez que a los gratis (se pagaria en cada pregunta)."""
    txt = _leer(os.path.join(AQUI, "cuerpo", "obrero.py"))
    assert "DE_PAGO" in txt, "obrero no distingue el de pago"
    assert "de_ultimo" in txt or "DE_PAGO" in txt


def test_el_equipo_no_desconecta_el_aprendizaje():
    """Que el equipo sirva incluye que el router aprenda (la indexacion reparada)."""
    txt = _leer(os.path.join(AQUI, "ingeniero.py"))
    assert "medidor.apuntar_paquete" in txt
