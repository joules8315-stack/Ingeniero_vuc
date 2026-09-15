import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from cuerpo import cuotas


def _gratis():
    """La lista de cerebros gratis es cuotas.ORDEN sin deepseek."""
    return [n for n in cuotas.ORDEN if n != "deepseek"]


def test_si_todas_las_gratis_duermen_claude_puede_revisar_a_deepseek():
    dormidos = set(_gratis())
    assert cuotas.puede_revisar_claude("deepseek", dormidos) is True


def test_si_una_gratis_esta_despierta_claude_no_revisa():
    dormidos = set(_gratis()) - {"gemini4"}
    assert cuotas.puede_revisar_claude("deepseek", dormidos) is False


def test_claude_no_revisa_lo_que_escribio_claude():
    dormidos = set(_gratis())
    assert cuotas.puede_revisar_claude("claude", dormidos) is False
