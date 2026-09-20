"""Vigia: el pit recoge los pedazos que el guardia aparto.

Cuando el guardia frena un guardado, la copia buena se aparta con el final
.FRENADO_POR_EL_GUARDIA y hoy alguien la devuelve a su sitio a mano. El pit
tiene que hacerlo solo (orden A-39 de Julio del 2026-09-20).

Esta vigia nace ROJA porque cuerpo/capataz.py todavia no sabe recoger los
pedazos: no existe la funcion recoger_lo_frenado. En cuanto el pit la tenga,
la vigia se pone verde sola.
"""

import os
import sys
import json


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARNES = os.path.join(RAIZ, 'arnes')
for _ruta in (RAIZ, ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from cuerpo import capataz


def test_el_pit_sabe_recoger_lo_frenado():
    """Solo texto: capataz.py tiene que nombrar recoger_los_pedazos."""
    ruta_capataz = os.path.join(RAIZ, 'cuerpo', 'capataz.py')
    with open(ruta_capataz, 'r', encoding='utf-8') as f:
        texto = f.read()
    assert 'recoger_los_pedazos' in texto, (
        'El pit no recoge lo que el guardia aparto: cuerpo/capataz.py no nombra '
        'recoger_los_pedazos, asi que el trabajo aprobado se queda tirado.'
    )


def test_el_pit_devuelve_la_copia_buena_a_su_sitio(tmp_path):
    """Con una casa de mentira, recoger_lo_frenado tiene que reponer la copia buena."""
    casa = tmp_path

    carpeta_sin_revisar = os.path.join(casa, 'memoria', 'trabajos_sin_revisar')
    os.makedirs(carpeta_sin_revisar, exist_ok=True)
    ruta_frenada = os.path.join(carpeta_sin_revisar, 'pieza.py.FRENADO_POR_EL_GUARDIA')
    with open(ruta_frenada, 'w', encoding='utf-8') as f:
        f.write('nuevo')

    carpeta_equipo = os.path.join(casa, 'memoria', 'trabajos_del_equipo')
    os.makedirs(carpeta_equipo, exist_ok=True)
    ruta_aprobado = os.path.join(
        carpeta_equipo, '2026-09-20_000000_APROBADO_pieza.py.json'
    )
    with open(ruta_aprobado, 'w', encoding='utf-8') as f:
        json.dump({'propuesta': {'archivo': 'cuerpo/pieza.py'}}, f, ensure_ascii=False)

    carpeta_cuerpo = os.path.join(casa, 'cuerpo')
    os.makedirs(carpeta_cuerpo, exist_ok=True)
    ruta_pieza = os.path.join(carpeta_cuerpo, 'pieza.py')
    with open(ruta_pieza, 'w', encoding='utf-8') as f:
        f.write('viejo')

    orden = {'pieza': 'cuerpo/pieza.py'}
    resultado = capataz.recoger_lo_frenado(orden, casa)

    assert isinstance(resultado, dict) and resultado.get('ok') is True, (
        'Si el pit no recoge la copia buena, el trabajo aprobado se pierde y hay '
        'que ir a buscarlo a mano: recoger_lo_frenado no devolvio ok verdadero.'
    )

    with open(ruta_pieza, 'r', encoding='utf-8') as f:
        contenido = f.read()
    assert 'nuevo' in contenido, (
        'Si el pit no recoge la copia buena, el trabajo aprobado se pierde y hay '
        'que ir a buscarlo a mano: cuerpo/pieza.py sigue con el texto viejo.'
    )
