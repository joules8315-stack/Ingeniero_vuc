"""vigias/test_vigia_la_orden_corta.py -- Vigia de la funcion nueva
cuerpo/director.py: orden_corta(raiz, id, pieza, vigia, que_hacer).

Comprueba, con asserts de verdad:

  1) orden_corta devuelve (True, motivo) y deja la orden '1' la primera
     y pendiente.
  2) El encargo de esa orden empieza por el texto de que_hacer y contiene
     'def dos(): (linea 3)' -- el programa encuentra solo el sitio de cada
     nombre de funcion que aparece en que_hacer y apunta su linea.
  3) El encargo contiene 'No toques ningun otro archivo'.
  4) Con una pieza que no existe en el disco, la orden queda con crear True.

Solo biblioteca estandar. No toca ningun otro archivo.
"""

import json
import os

from cuerpo import director


# ----------------------------------------------------------------------
# Utilidades de la prueba
# ----------------------------------------------------------------------


def _preparar(tmp_path):
    """Deja memoria/ORDENES.json con [] y el archivo m.py con dos funciones.

    Devuelve (raiz, ruta_ordenes, ruta_m).
    """
    raiz = str(tmp_path)
    memoria = os.path.join(raiz, 'memoria')
    os.makedirs(memoria, exist_ok=True)

    ruta_ordenes = os.path.join(memoria, 'ORDENES.json')
    with open(ruta_ordenes, 'w', encoding='utf-8') as f:
        json.dump([], f)

    ruta_m = os.path.join(raiz, 'm.py')
    with open(ruta_m, 'w', encoding='utf-8') as f:
        f.write('def uno():\n')
        f.write('    return 1\n')
        f.write('def dos():\n')
        f.write('    return 2\n')

    return raiz, ruta_ordenes, ruta_m


def _leer_ordenes(ruta_ordenes):
    with open(ruta_ordenes, 'r', encoding='utf-8') as f:
        return json.load(f)


def _buscar_orden(ordenes, id_orden):
    for o in ordenes:
        if isinstance(o, dict) and o.get('id') == id_orden:
            return o
    return None


# ----------------------------------------------------------------------
# Pruebas
# ----------------------------------------------------------------------


def test_orden_corta_crea_la_orden_la_primera_y_pendiente(tmp_path):
    """(1) Devuelve (True, motivo) y la orden 1 queda la primera, pendiente."""
    raiz, ruta_ordenes, _ruta_m = _preparar(tmp_path)

    resultado = director.orden_corta(
        raiz,
        '1',
        'm.py',
        'vigias/t.py',
        'que dos devuelva 3',
    )

    assert isinstance(resultado, tuple), 'orden_corta debe devolver una tupla'
    assert len(resultado) == 2, 'orden_corta debe devolver (ok, motivo)'
    ok, motivo = resultado
    assert ok is True, 'orden_corta debe devolver True, devolvio: %r' % (resultado,)
    assert isinstance(motivo, str) and motivo, 'el motivo no puede estar vacio'

    ordenes = _leer_ordenes(ruta_ordenes)
    assert isinstance(ordenes, list), 'ORDENES.json debe seguir siendo una lista'
    assert len(ordenes) >= 1, 'tiene que haber al menos una orden'

    primera = ordenes[0]
    assert isinstance(primera, dict), 'la primera orden debe ser un objeto'
    assert primera.get('id') == '1', 'la orden 1 tiene que quedar la primera'
    assert primera.get('estado') == 'pendiente', (
        'la orden 1 tiene que quedar pendiente, quedo: %r' % primera.get('estado')
    )


def test_el_encargo_empieza_por_que_hacer_y_apunta_la_linea_de_dos(tmp_path):
    """(2) El encargo empieza por que_hacer y trae 'def dos(): (linea 3)'."""
    raiz, ruta_ordenes, _ruta_m = _preparar(tmp_path)

    que_hacer = 'que dos devuelva 3'
    ok, _motivo = director.orden_corta(
        raiz,
        '1',
        'm.py',
        'vigias/t.py',
        que_hacer,
    )
    assert ok is True, 'orden_corta tenia que devolver True'

    ordenes = _leer_ordenes(ruta_ordenes)
    orden = _buscar_orden(ordenes, '1')
    assert orden is not None, 'no se encontro la orden 1'

    encargo = orden.get('encargo', '')
    assert isinstance(encargo, str) and encargo, 'el encargo no puede estar vacio'
    assert encargo.startswith(que_hacer), (
        'el encargo tiene que empezar por %r, empieza por: %r'
        % (que_hacer, encargo[:60])
    )
    assert 'def dos(): (linea 3)' in encargo, (
        'el encargo tiene que apuntar el sitio de dos: %r' % encargo
    )


def test_el_encargo_prohibe_tocar_otros_archivos(tmp_path):
    """(3) El encargo contiene 'No toques ningun otro archivo'."""
    raiz, ruta_ordenes, _ruta_m = _preparar(tmp_path)

    ok, _motivo = director.orden_corta(
        raiz,
        '1',
        'm.py',
        'vigias/t.py',
        'que dos devuelva 3',
    )
    assert ok is True, 'orden_corta tenia que devolver True'

    ordenes = _leer_ordenes(ruta_ordenes)
    orden = _buscar_orden(ordenes, '1')
    assert orden is not None, 'no se encontro la orden 1'

    encargo = orden.get('encargo', '')
    assert 'No toques ningun otro archivo' in encargo, (
        'el encargo tiene que prohibir tocar otros archivos: %r' % encargo
    )


def test_pieza_que_no_existe_queda_con_crear_true(tmp_path):
    """(4) Con una pieza que no existe, la orden queda con crear True."""
    raiz, ruta_ordenes, _ruta_m = _preparar(tmp_path)

    ok, _motivo = director.orden_corta(
        raiz,
        '1',
        'no_existe_esta_pieza.py',
        'vigias/t.py',
        'que dos devuelva 3',
    )
    assert ok is True, 'orden_corta tenia que devolver True'

    ordenes = _leer_ordenes(ruta_ordenes)
    orden = _buscar_orden(ordenes, '1')
    assert orden is not None, 'no se encontro la orden 1'
    assert orden.get('crear') is True, (
        'con una pieza que no existe, crear tiene que ser True, quedo: %r'
        % orden.get('crear')
    )
