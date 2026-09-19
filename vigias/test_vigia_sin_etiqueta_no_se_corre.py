"""Vigia: sin etiqueta no se corre (plan v4, P3-2).

Una orden a la que le falta un campo de la etiqueta, o que lo trae mal,
no se corre: se queda pendiente y el capataz pasa a la siguiente.
Esta vigia nunca toca el ORDENES.json real: usa monkeypatch sobre leer_lista.
"""

import copy

import pytest

from cuerpo import capataz


ORDEN_COMPLETA = {
    'id': 'P1',
    'origen': 'prueba',
    'repara': 'nada',
    'pieza': 'cuerpo/x.py',
    'depende': [],
    'modo': 'IA',
    'razon': 'probar',
    'encargo': 'hacer algo',
    'estado': 'pendiente',
}


def test_orden_completa_no_tiene_problemas():
    """Una orden con todos los campos bien puestos no da ningun problema."""
    assert capataz.validar_etiqueta(copy.deepcopy(ORDEN_COMPLETA)) == []


@pytest.mark.parametrize('campo', capataz.CAMPOS_ETIQUETA)
def test_quitar_un_campo_deja_problemas(campo):
    """Si falta cualquier campo de la etiqueta, la orden ya no vale."""
    orden = copy.deepcopy(ORDEN_COMPLETA)
    orden.pop(campo)
    assert capataz.validar_etiqueta(orden) != []


def test_razon_en_blanco_no_vale():
    """Una razon de solo espacios es como si no estuviera."""
    orden = copy.deepcopy(ORDEN_COMPLETA)
    orden['razon'] = '   '
    assert capataz.validar_etiqueta(orden) != []


def test_depende_como_texto_no_vale():
    """depende tiene que ser una lista, no un texto."""
    orden = copy.deepcopy(ORDEN_COMPLETA)
    orden['depende'] = 'P0'
    assert 'depende no es una lista' in capataz.validar_etiqueta(orden)


def test_modo_desconocido_no_vale():
    """El modo solo puede ser PROGRAMA o IA."""
    orden = copy.deepcopy(ORDEN_COMPLETA)
    orden['modo'] = 'MAGIA'
    assert 'modo debe ser PROGRAMA o IA' in capataz.validar_etiqueta(orden)


def test_texto_suelto_no_es_orden():
    """Un texto que no es diccionario no es una orden."""
    assert capataz.validar_etiqueta('hola') == ['no es una orden']


def test_siguiente_pendiente_se_salta_la_sin_etiqueta(monkeypatch):
    """Si la primera pendiente no tiene etiqueta, se devuelve la siguiente completa."""
    orden_sin_encargo = copy.deepcopy(ORDEN_COMPLETA)
    orden_sin_encargo['id'] = 'P0'
    orden_sin_encargo.pop('encargo')
    orden_completa = copy.deepcopy(ORDEN_COMPLETA)
    monkeypatch.setattr(
        capataz,
        'leer_lista',
        lambda: [orden_sin_encargo, orden_completa],
    )
    assert capataz.siguiente_pendiente() == orden_completa


def test_si_la_unica_pendiente_no_tiene_etiqueta_devuelve_none(monkeypatch):
    """Si la unica pendiente no tiene etiqueta, no hay nada que correr."""
    orden_sin_encargo = copy.deepcopy(ORDEN_COMPLETA)
    orden_sin_encargo.pop('encargo')
    monkeypatch.setattr(
        capataz,
        'leer_lista',
        lambda: [orden_sin_encargo],
    )
    assert capataz.siguiente_pendiente() is None
