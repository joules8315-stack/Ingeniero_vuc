"""Vigia del bucle del capataz: comprueba que corre ordenes, respeta el tope de gasto,
para a la vez las de la misma pieza, y para cuando hay 3 fallos del mismo tipo o nada
se puede correr. Nunca llama al equipo de verdad ni toca la memoria real."""

import datetime
import json
import os
import sys
import threading
import time

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import capataz  # noqa: E402


# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------

def orden(id, pieza, depende=()):
    """Arma una orden con la etiqueta completa que pide el capataz."""
    return {
        'id': id,
        'pieza': pieza,
        'origen': 'prueba',
        'repara': 'nada',
        'modo': 'IA',
        'razon': 'probar',
        'encargo': 'encargo ' + id,
        'estado': 'pendiente',
        'depende': list(depende),
    }


def preparar(tmp_path, monkeypatch, ordenes):
    """Deja el capataz apuntando a una carpeta temporal y escribe ORDENES.json."""
    monkeypatch.setattr(capataz, '__file__', str(tmp_path / 'cuerpo' / 'capataz.py'))
    memoria = tmp_path / 'memoria'
    memoria.mkdir(parents=True, exist_ok=True)
    with open(memoria / 'ORDENES.json', 'w', encoding='utf-8') as f:
        json.dump(ordenes, f, indent=2)
    monkeypatch.setenv('INGENIERO_GASTO_USD_TEST', str(memoria / 'GASTO_USD.jsonl'))
    monkeypatch.setattr(capataz, 'forense', lambda *a, **k: {'ok': True, 'paso': 'prueba', 'motivo': 'forense falso'}, raising=False)
    monkeypatch.setenv('INGENIERO_FALLOS_TEST', str(memoria / 'FALLOS.json'))
    return memoria


def leer_ordenes(memoria):
    """Lee ORDENES.json de la memoria temporal y devuelve la lista."""
    with open(memoria / 'ORDENES.json', encoding='utf-8') as f:
        return json.load(f)


def estado_de(lista, orden_id):
    """Devuelve el estado de la orden con ese id, o None si no esta."""
    for o in lista:
        if isinstance(o, dict) and o.get('id') == orden_id:
            return o.get('estado')
    return None


def orden_de(lista, orden_id):
    """Devuelve la orden con ese id, o None si no esta."""
    for o in lista:
        if isinstance(o, dict) and o.get('id') == orden_id:
            return o
    return None


# ---------------------------------------------------------------------------
# Pruebas
# ---------------------------------------------------------------------------

def test_tres_piezas_distintas_todas_hechas(tmp_path, monkeypatch):
    """Tres ordenes de piezas distintas: todas se hacen y el bucle dice TODO HECHO."""
    ordenes = [
        orden('o1', 'pieza_a.py'),
        orden('o2', 'pieza_b.py'),
        orden('o3', 'pieza_c.py'),
    ]
    memoria = preparar(tmp_path, monkeypatch, ordenes)

    llamadas = []

    def falsa(proyecto, orden, tope_segundos):
        llamadas.append(orden.get('id'))
        return {'guardado': True, 'codigo': 0, 'salida': 'GUARDADO AL MOMENTO'}

    monkeypatch.setattr(capataz, 'lanzar_al_equipo', falsa)

    texto = capataz.bucle('prueba', aviso=lambda t: None)

    assert texto == 'PARADO: TODO HECHO'
    lista = leer_ordenes(memoria)
    assert estado_de(lista, 'o1') == 'hecha'
    assert estado_de(lista, 'o2') == 'hecha'
    assert estado_de(lista, 'o3') == 'hecha'
    assert sorted(llamadas) == ['o1', 'o2', 'o3']


def test_dos_piezas_distintas_corren_a_la_vez(tmp_path, monkeypatch):
    """Dos piezas distintas corren a la vez: la barrera de 2 se rompe si van en fila."""
    ordenes = [
        orden('o1', 'pieza_a.py'),
        orden('o2', 'pieza_b.py'),
    ]
    memoria = preparar(tmp_path, monkeypatch, ordenes)

    barrera = threading.Barrier(2, timeout=5)

    def falsa(proyecto, orden, tope_segundos):
        barrera.wait()
        return {'guardado': True, 'codigo': 0, 'salida': 'GUARDADO AL MOMENTO'}

    monkeypatch.setattr(capataz, 'lanzar_al_equipo', falsa)

    texto = capataz.bucle('prueba', aviso=lambda t: None)

    assert texto == 'PARADO: TODO HECHO'
    lista = leer_ordenes(memoria)
    assert estado_de(lista, 'o1') == 'hecha'
    assert estado_de(lista, 'o2') == 'hecha'


def test_misma_pieza_va_en_fila(tmp_path, monkeypatch):
    """Dos ordenes de la MISMA pieza no corren a la vez: el maximo simultaneo es 1."""
    ordenes = [
        orden('o1', 'pieza_a.py'),
        orden('o2', 'pieza_a.py'),
    ]
    memoria = preparar(tmp_path, monkeypatch, ordenes)

    cerrojo = threading.Lock()
    corriendo = {'ahora': 0, 'maximo': 0}

    def falsa(proyecto, orden, tope_segundos):
        with cerrojo:
            corriendo['ahora'] += 1
            if corriendo['ahora'] > corriendo['maximo']:
                corriendo['maximo'] = corriendo['ahora']
        time.sleep(0.2)
        with cerrojo:
            corriendo['ahora'] -= 1
        return {'guardado': True, 'codigo': 0, 'salida': 'GUARDADO AL MOMENTO'}

    monkeypatch.setattr(capataz, 'lanzar_al_equipo', falsa)

    texto = capataz.bucle('prueba', en_paralelo=2, aviso=lambda t: None)

    assert texto == 'PARADO: TODO HECHO'
    assert corriendo['maximo'] == 1
    lista = leer_ordenes(memoria)
    assert estado_de(lista, 'o1') == 'hecha'
    assert estado_de(lista, 'o2') == 'hecha'


def test_tres_fallos_del_mismo_tipo_para(tmp_path, monkeypatch):
    """Tres ordenes de la misma pieza que no aprueban: para y las tres quedan fallidas."""
    ordenes = [
        orden('o1', 'pieza_a.py'),
        orden('o2', 'pieza_a.py'),
        orden('o3', 'pieza_a.py'),
    ]
    memoria = preparar(tmp_path, monkeypatch, ordenes)

    def falsa(proyecto, orden, tope_segundos):
        return {'guardado': False, 'codigo': 0, 'salida': 'EL EQUIPO NO APROBO'}

    monkeypatch.setattr(capataz, 'lanzar_al_equipo', falsa)

    texto = capataz.bucle('prueba', aviso=lambda t: None)

    assert texto.startswith('PARADO: 3 FALLOS DEL MISMO TIPO (no_aprobo)')
    lista = leer_ordenes(memoria)
    for oid in ('o1', 'o2', 'o3'):
        assert estado_de(lista, oid) == 'fallida'
        o = orden_de(lista, oid)
        assert capataz.ya_fallo(o) is True


def test_tope_de_gasto_para_antes_de_llamar(tmp_path, monkeypatch):
    """Si el gasto del mes ya paso el tope, para y no llama al equipo."""
    ordenes = [orden('o1', 'pieza_a.py')]
    memoria = preparar(tmp_path, monkeypatch, ordenes)

    cuando = datetime.datetime.now().isoformat()
    linea = {
        'cuando': cuando,
        'modelo': 'deepseek-v4-pro',
        'uso': {'completion_tokens': 2000000},
    }
    with open(memoria / 'GASTO_USD.jsonl', 'w', encoding='utf-8') as f:
        f.write(json.dumps(linea) + '\n')

    llamadas = []

    def falsa(proyecto, orden, tope_segundos):
        llamadas.append(orden.get('id'))
        return {'guardado': True, 'codigo': 0, 'salida': 'GUARDADO AL MOMENTO'}

    monkeypatch.setattr(capataz, 'lanzar_al_equipo', falsa)

    texto = capataz.bucle('prueba', aviso=lambda t: None)

    assert texto.startswith('PARADO: TOPE DE GASTO')
    assert llamadas == []


def test_dependiente_de_fallida_no_se_corre(tmp_path, monkeypatch):
    """Si la primera falla, la que depende de ella sigue pendiente y el bucle para."""
    ordenes = [
        orden('o1', 'pieza_a.py'),
        orden('o2', 'pieza_b.py', depende=('o1',)),
    ]
    memoria = preparar(tmp_path, monkeypatch, ordenes)

    def falsa(proyecto, orden, tope_segundos):
        if orden.get('id') == 'o1':
            return {'guardado': False, 'codigo': 0, 'salida': 'EL EQUIPO NO APROBO'}
        return {'guardado': True, 'codigo': 0, 'salida': 'GUARDADO AL MOMENTO'}

    monkeypatch.setattr(capataz, 'lanzar_al_equipo', falsa)

    texto = capataz.bucle('prueba', aviso=lambda t: None)

    assert texto.startswith('PARADO: NADA SE PUEDE CORRER')
    lista = leer_ordenes(memoria)
    assert estado_de(lista, 'o1') == 'fallida'
    assert estado_de(lista, 'o2') == 'pendiente'
