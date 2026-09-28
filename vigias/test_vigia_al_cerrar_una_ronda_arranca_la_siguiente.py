"""Vigia: al cerrar una ronda (marcar_estado con 'hecha') arranca la siguiente.

NACE ROJA A PROPOSITO: cuerpo/capataz.py todavia no tiene la funcion
reintentar_lo_que_esperaba, ni marcar_estado la llama cuando el estado es
'hecha'. En esta ronda NO se escribe esa funcion y no se toca ningun otro
archivo.

Contrato que se vigila:
  - reintentar_lo_que_esperaba(id_orden) recibe un id y devuelve la lista de
    ids que volvieron a la cola.
  - Busca en la lista de ordenes las que estan en estado 'fallida' y cuya
    lista 'depende' contiene ese id, y para cada una llama a la funcion que
    ya existe reintentar_tras_el_arreglo pasandole el id de esa orden
    fallida y el id que se recibio.
  - Devuelve la lista de los ids que reintento, y lista vacia si no habia
    ninguno. Nunca lanza.
  - marcar_estado, cuando el estado que se escribe es 'hecha', llama sola a
    esta funcion, para que nadie tenga que acordarse.

Hechos comprobados en el codigo (no se suponen):
  1. HUELLAS_QUE_FALLARON.jsonl guarda cada renglon con la clave 'huella',
     tal como la escribe anotar_huella_fallida.
  2. huella_de junta el texto 'encargo', un salto de renglon y el texto
     'pieza'; por eso las ordenes de mentira traen esos dos campos.
  3. marcar_estado NO devuelve nada definido, asi que la prueba NO comprueba
     lo que devuelve: comprueba SOLO lo que quedo escrito en los dos
     archivos.

No llama a ninguna IA, no lanza procesos y solo escribe en tmp_path.
"""

import json
import os

import pytest

from cuerpo import capataz


# ---------------------------------------------------------------------------
# Utilidades de montaje: todo vive dentro de tmp_path
# ---------------------------------------------------------------------------


def _montar_mundo(tmp_path, monkeypatch):
    """Deja capataz.__file__ dentro de tmp_path/cuerpo y crea memoria al lado.

    Devuelve (carpeta_memoria, ruta_ordenes, ruta_huellas).
    """
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir()
    monkeypatch.setattr(capataz, '__file__', str(carpeta_cuerpo / 'capataz.py'))

    carpeta_memoria = tmp_path / 'memoria'
    carpeta_memoria.mkdir()
    ruta_ordenes = carpeta_memoria / 'ORDENES.json'
    ruta_huellas = carpeta_memoria / 'HUELLAS_QUE_FALLARON.jsonl'
    return carpeta_memoria, ruta_ordenes, ruta_huellas


def _ordenes_de_mentira():
    """Las cuatro ordenes del encargo, con encargo y pieza para la huella."""
    return [
        {
            'id': 'A',
            'estado': 'pendiente',
            'depende': [],
            'encargo': 'encargo de la orden A',
            'pieza': 'pieza de la orden A',
        },
        {
            'id': 'B',
            'estado': 'fallida',
            'depende': ['A'],
            'paso_fallido': 'guardia',
            'fallos_seguidos': 2,
            'encargo': 'encargo de la orden B',
            'pieza': 'pieza de la orden B',
        },
        {
            'id': 'C',
            'estado': 'fallida',
            'depende': [],
            'paso_fallido': 'guardia',
            'fallos_seguidos': 1,
            'encargo': 'encargo de la orden C',
            'pieza': 'pieza de la orden C',
        },
        {
            'id': 'D',
            'estado': 'pendiente',
            'depende': ['A'],
            'encargo': 'encargo de la orden D',
            'pieza': 'pieza de la orden D',
        },
    ]


def _escribir_ordenes(ruta_ordenes, ordenes):
    with open(ruta_ordenes, 'w', encoding='utf-8') as f:
        json.dump(ordenes, f, indent=2, ensure_ascii=False)


def _escribir_huellas(ruta_huellas, ordenes):
    """Dos renglones: la huella de B y una huella distinta."""
    orden_b = None
    for orden in ordenes:
        if orden.get('id') == 'B':
            orden_b = orden
            break
    huella_b = capataz.huella_de(orden_b)
    huella_otra = capataz.huella_de({
        'encargo': 'un encargo que no es de ninguna orden',
        'pieza': 'una pieza que no es de ninguna orden',
    })
    with open(ruta_huellas, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'huella': huella_b, 'id': 'B', 'motivo': 'guardia', 'fecha': '2026-09-28'}, ensure_ascii=False) + '\n')
        f.write(json.dumps({'huella': huella_otra, 'id': 'Z', 'motivo': 'guardia', 'fecha': '2026-09-28'}, ensure_ascii=False) + '\n')
    return huella_b, huella_otra


def _leer_ordenes(ruta_ordenes):
    with open(ruta_ordenes, encoding='utf-8') as f:
        return json.load(f)


def _buscar_orden(lista, orden_id):
    for orden in lista:
        if isinstance(orden, dict) and orden.get('id') == orden_id:
            return orden
    return None


def _leer_huellas(ruta_huellas):
    with open(ruta_huellas, encoding='utf-8') as f:
        return f.read()


def _montar_completo(tmp_path, monkeypatch):
    carpeta_memoria, ruta_ordenes, ruta_huellas = _montar_mundo(tmp_path, monkeypatch)
    ordenes = _ordenes_de_mentira()
    _escribir_ordenes(ruta_ordenes, ordenes)
    huella_b, huella_otra = _escribir_huellas(ruta_huellas, ordenes)
    return {
        'memoria': carpeta_memoria,
        'ordenes': ruta_ordenes,
        'huellas': ruta_huellas,
        'huella_b': huella_b,
        'huella_otra': huella_otra,
    }


# ---------------------------------------------------------------------------
# PRUEBA 1: al cerrar A con 'hecha', B vuelve a la cola y su huella se borra
# ---------------------------------------------------------------------------


def test_al_cerrar_la_ronda_la_que_esperaba_vuelve_a_la_cola(tmp_path, monkeypatch):
    mundo = _montar_completo(tmp_path, monkeypatch)

    capataz.marcar_estado('A', 'hecha')

    lista = _leer_ordenes(mundo['ordenes'])
    orden_b = _buscar_orden(lista, 'B')
    assert orden_b is not None, 'la orden B desaparecio de ORDENES.json'
    assert orden_b.get('estado') == 'pendiente', (
        'B deberia haber vuelto a pendiente al cerrarse A, y quedo en '
        + repr(orden_b.get('estado'))
    )
    assert orden_b.get('fallos_seguidos') == 0, (
        'B deberia tener fallos_seguidos 0, y tiene '
        + repr(orden_b.get('fallos_seguidos'))
    )

    texto_huellas = _leer_huellas(mundo['huellas'])
    assert mundo['huella_b'] not in texto_huellas, (
        'la huella de B deberia haberse borrado de HUELLAS_QUE_FALLARON.jsonl'
    )


# ---------------------------------------------------------------------------
# PRUEBA 2: la que no esperaba a nadie sigue fallida
# ---------------------------------------------------------------------------


def test_la_que_no_esperaba_a_nadie_sigue_fallida(tmp_path, monkeypatch):
    mundo = _montar_completo(tmp_path, monkeypatch)

    capataz.marcar_estado('A', 'hecha')

    lista = _leer_ordenes(mundo['ordenes'])
    orden_c = _buscar_orden(lista, 'C')
    assert orden_c is not None, 'la orden C desaparecio de ORDENES.json'
    assert orden_c.get('estado') == 'fallida', (
        'C no esperaba a A, asi que deberia seguir fallida, y quedo en '
        + repr(orden_c.get('estado'))
    )


# ---------------------------------------------------------------------------
# PRUEBA 3: la que esta pendiente y espera a A no se toca
# ---------------------------------------------------------------------------


def test_la_pendiente_que_espera_a_A_no_se_toca(tmp_path, monkeypatch):
    mundo = _montar_completo(tmp_path, monkeypatch)

    capataz.marcar_estado('A', 'hecha')

    lista = _leer_ordenes(mundo['ordenes'])
    orden_d = _buscar_orden(lista, 'D')
    assert orden_d is not None, 'la orden D desaparecio de ORDENES.json'
    assert orden_d.get('estado') == 'pendiente', (
        'D ya estaba pendiente y no es fallida: no deberia tocarse, y quedo en '
        + repr(orden_d.get('estado'))
    )


# ---------------------------------------------------------------------------
# PRUEBA 4: un id que nadie espera devuelve lista vacia y no toca los archivos
# ---------------------------------------------------------------------------


def test_un_id_que_nadie_espera_devuelve_lista_vacia_y_no_toca_nada(tmp_path, monkeypatch):
    mundo = _montar_completo(tmp_path, monkeypatch)

    antes_ordenes = _leer_ordenes(mundo['ordenes'])
    antes_huellas = _leer_huellas(mundo['huellas'])

    resultado = capataz.reintentar_lo_que_esperaba('NADIE_ME_ESPERA')

    assert resultado == [], (
        'reintentar_lo_que_esperaba deberia devolver lista vacia, y devolvio '
        + repr(resultado)
    )
    assert _leer_ordenes(mundo['ordenes']) == antes_ordenes, (
        'ORDENES.json no deberia haber cambiado'
    )
    assert _leer_huellas(mundo['huellas']) == antes_huellas, (
        'HUELLAS_QUE_FALLARON.jsonl no deberia haber cambiado'
    )
