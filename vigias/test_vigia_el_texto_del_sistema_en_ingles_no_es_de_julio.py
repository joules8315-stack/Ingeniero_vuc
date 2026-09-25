# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_texto_del_sistema_en_ingles_no_es_de_julio.py

VIGIA: comprueba que un texto interno del sistema escrito en inglés NO se apunta como orden de Julio, que el fallo real fue el 2026-09-25 cuando había 127 pendientes falsos y el cierre quedaba bloqueado para siempre, y que la vigia NACE ROJA a propósito porque la reparación aún no está.
"""

import os
import sys

# Añadir la carpeta 'arnes' al path (está al mismo nivel que 'vigias')
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(AQUI, "arnes"))

from candado_legislar import parece_una_orden


def test_el_texto_del_sistema_en_ingles_no_es_de_julio():
    assert not parece_una_orden('Generate a concise, single-line task title of at most 36 characters and under five words where possible')
    assert not parece_una_orden('Write a brief catch-up for a user returning to this Codex task')
    assert parece_una_orden('Busca donde esta toda la informacion que necesitas para reparar el equipo')

