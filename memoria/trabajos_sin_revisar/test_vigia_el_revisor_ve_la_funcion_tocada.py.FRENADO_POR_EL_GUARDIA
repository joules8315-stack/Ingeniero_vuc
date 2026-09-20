"""Vigia: el revisor tiene que VER la funcion tocada entera.

Hoy el material del revisor se recorta desde el final y el trozo tocado se pierde,
y el revisor rechaza sin ver el codigo. Esta vigia nace ROJA hasta que exista
cuerpo/obrero.py::_material_del_revisor(paquete, propuesta, tope).
"""
import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import obrero


# El nombre del campo del texto viejo se arma asi a proposito: la tarea lo pide.
CAMPO_V = 'texto' + '_viejo'


def _paquete_de_prueba():
    """Arma el paquete de texto con ley, vecinos y dos trozos de distinta relevancia."""
    lineas = []
    lineas.append('## 1. LA LEY QUE MANDA')
    for _ in range(150):
        lineas.append('ley ' * 10)
    lineas.append('## 2. A QUIEN PUEDE DANAR')
    for _ in range(150):
        lineas.append('vecino ' * 10)
    lineas.append('## 3. LOS TROZOS EXACTOS')
    lineas.append('### ' + chr(96) + 'x.py' + chr(96) + ' relevancia 0.9')
    for _ in range(60):
        lineas.append('relleno = 0')
    lineas.append('### ' + chr(96) + 'x.py' + chr(96) + ' relevancia 0.1')
    lineas.append('def tocada():')
    lineas.append('    return 12345')
    return '\n'.join(lineas)


def _propuesta_tocada():
    return {'archivo': 'x.py', CAMPO_V: '    return 12345'}


def test_el_revisor_ve_la_funcion_tocada():
    """El material del revisor trae el trozo tocado entero y cabe en el tope."""
    paquete = _paquete_de_prueba()
    propuesta = _propuesta_tocada()
    resultado = obrero._material_del_revisor(paquete, propuesta, 8000)
    assert 'def tocada():' in resultado, 'el revisor NO ve la funcion tocada'
    assert 'return 12345' in resultado, 'el revisor NO ve el cuerpo de la funcion tocada'
    assert len(resultado) <= 8000, 'el material del revisor se pasa del tope: ' + str(len(resultado))


def test_el_trozo_tocado_va_antes_que_la_ley():
    """El trozo tocado va ANTES que la ley en el resultado."""
    paquete = _paquete_de_prueba()
    propuesta = _propuesta_tocada()
    resultado = obrero._material_del_revisor(paquete, propuesta, 8000)
    i_tocado = resultado.find('def tocada():')
    i_ley = resultado.find('LA LEY QUE MANDA')
    assert i_tocado != -1, 'el trozo tocado no aparece en el resultado'
    assert i_ley != -1, 'la ley no aparece en el resultado'
    assert i_tocado < i_ley, 'el trozo tocado va DESPUES de la ley: ' + str(i_tocado) + ' vs ' + str(i_ley)


def test_sin_texto_viejo_es_igual_que_filtrar_paquete():
    """Si el texto viejo no aparece en ningun trozo, se cae al filtro de siempre."""
    paquete = _paquete_de_prueba()
    propuesta = {'archivo': 'x.py', CAMPO_V: 'esto no esta en ningun trozo del paquete'}
    resultado = obrero._material_del_revisor(paquete, propuesta, 8000)
    esperado = obrero._filtrar_paquete(paquete, archivo='x.py', tope=8000)
    assert resultado == esperado, 'sin texto viejo el resultado deberia ser el filtro de siempre'


def test_propuesta_que_no_es_dict_no_lanza():
    """Si la propuesta no es dict, no lanza y devuelve lo mismo que _filtrar_paquete."""
    paquete = _paquete_de_prueba()
    esperado = obrero._filtrar_paquete(paquete, archivo='x.py', tope=8000)
    for basura in ('no soy un dict', 12345, None, ['a', 'b']):
        resultado = obrero._material_del_revisor(paquete, basura, 8000)
        assert resultado == esperado, 'con propuesta no dict deberia caer al filtro: ' + repr(basura)


if __name__ == '__main__':
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith('test_') and callable(_f):
            try:
                _f()
                print('  VERDE  ' + _n)
            except Exception as e:
                fails += 1
                print('  ROJA   ' + _n + ': ' + repr(e))
    raise SystemExit(1 if fails else 0)
