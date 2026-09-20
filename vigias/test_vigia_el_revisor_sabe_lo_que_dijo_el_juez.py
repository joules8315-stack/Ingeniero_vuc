"""Vigia: el revisor sabe lo que ya dijo el juez de la prueba.

Dos cosas del equipo, en cuerpo/obrero.py:

  PRUEBA 1 (texto, sin ejecutar nada): el archivo cuerpo/obrero.py nombra a
  juzgar_con_vecinas. Si el equipo no llama al juez, se sigue pagando una IA para
  saber algo que se puede correr gratis.

  PRUEBA 2: el material que se le arma al revisor le dice lo que ya decidio el
  juez. Si el revisor no sabe que la prueba ya se corrio y quedo verde, vuelve a
  juzgar a ciegas lo que ya esta demostrado.

Esta segunda prueba nace ROJA a proposito: cuerpo/obrero.py todavia no mete la
marca '_juez_de_la_prueba' en el material que ve el revisor.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, 'arnes'))

from cuerpo import obrero


RUTA_OBRERO = os.path.join(RAIZ, 'cuerpo', 'obrero.py')

RAZON_DEL_JUEZ = 'la prueba de las vecinas quedo verde: el cambio no rompe nada'

PAQUETE = (
    '## 1. LA LEY\n'
    'nada\n'
    '## 3. LOS TROZOS EXACTOS\n'
    '### `cuerpo/obrero.py:1-10`\n'
    '```\n'
    'def _material_del_revisor(paquete, propuesta, tope):\n'
    '    return paquete\n'
    '```\n'
)

PROPUESTA = {
    'archivo': 'cuerpo/obrero.py',
    'texto_viejo': 'def _material_del_revisor(paquete, propuesta, tope):',
    'texto_nuevo': 'def _material_del_revisor(paquete, propuesta, tope):  # tocado',
    '_juez_de_la_prueba': RAZON_DEL_JUEZ,
}

TOPE = 100000


def test_el_equipo_llama_al_juez():
    """El texto de cuerpo/obrero.py tiene que nombrar a juzgar_con_vecinas.

    Si el equipo no llama al juez, se sigue pagando una IA para saber algo que se
    puede correr gratis.
    """
    with open(RUTA_OBRERO, 'r', encoding='utf-8', errors='replace') as f:
        texto = f.read()
    assert 'juzgar_con_vecinas' in texto, (
        'cuerpo/obrero.py NO nombra a juzgar_con_vecinas: si el equipo no llama al '
        'juez, se sigue pagando una IA para saber algo que se puede correr gratis')


def test_el_material_del_revisor_lleva_la_razon_del_juez(monkeypatch):
    """El material del revisor tiene que decir lo que ya decidio el juez.

    Si el revisor no sabe que la prueba ya se corrio y quedo verde, vuelve a juzgar
    a ciegas lo que ya esta demostrado.
    """
    prompts = []

    def _falso_preguntar_con_relevo(prompt, *resto, **con_nombre):
        prompts.append(prompt)
        return (
            '{"veredicto": "APROBADO", "fallos": []}',
            'groq',
            [],
        )

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', _falso_preguntar_con_relevo)
    obrero.auditar(
        PAQUETE,
        {'archivo': 'x.py', '_juez_de_la_prueba': RAZON_DEL_JUEZ, 'evitar': 'deepseek'},
    )
    assert not prompts, (
        'se le pregunto a una IA algo que el juez ya habia demostrado: eso es gastar '
        'sin ganar (orden A-39)')
