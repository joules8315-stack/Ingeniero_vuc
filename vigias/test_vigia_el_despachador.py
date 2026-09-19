"""Vigia del despachador: comprueba que listas_para_correr de cuerpo/capataz.py
solo devuelve las ordenes que de verdad se pueden correr ya.

Cada prueba aisla la memoria: desvia capataz.__file__ a una carpeta temporal y
escribe ahi su propio ORDENES.json. Nunca toca la memoria real.
"""

import json
import os
import sys

import pytest

# Aseguramos que la raiz del proyecto este en el path para poder importar cuerpo.capataz
_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from cuerpo import capataz  # noqa: E402


def _orden(oid, pieza, estado='pendiente', depende=None, encargo=None):
    """Arma una orden con la etiqueta completa que pide la tarea."""
    if depende is None:
        depende = []
    if encargo is None:
        encargo = 'encargo ' + oid
    return {
        'id': oid,
        'origen': 'prueba',
        'repara': 'nada',
        'pieza': pieza,
        'depende': depende,
        'modo': 'IA',
        'razon': 'probar',
        'encargo': encargo,
        'estado': estado,
    }


def _preparar(tmp_path, monkeypatch, ordenes):
    """Desvia capataz.__file__ a tmp_path y escribe ahi el ORDENES.json de prueba."""
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(capataz, '__file__', str(carpeta_cuerpo / 'capataz.py'))
    carpeta_memoria = tmp_path / 'memoria'
    carpeta_memoria.mkdir(parents=True, exist_ok=True)
    ruta_ordenes = carpeta_memoria / 'ORDENES.json'
    with open(ruta_ordenes, 'w', encoding='utf-8') as f:
        json.dump(ordenes, f, ensure_ascii=False, indent=2)
    return ruta_ordenes


def _ids(lista):
    return [o.get('id') for o in lista]


def test_dos_pendientes_de_piezas_distintas_sin_dependencias_salen_las_dos(tmp_path, monkeypatch):
    ordenes = [
        _orden('a', 'pieza_a.py'),
        _orden('b', 'pieza_b.py'),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == ['a', 'b']


def test_dos_pendientes_de_la_misma_pieza_sale_solo_la_primera(tmp_path, monkeypatch):
    ordenes = [
        _orden('a', 'pieza_x.py'),
        _orden('b', 'pieza_x.py'),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == ['a']


def test_pendiente_con_pieza_corriendo_en_otra_orden_no_sale(tmp_path, monkeypatch):
    ordenes = [
        _orden('a', 'pieza_x.py', estado='corriendo'),
        _orden('b', 'pieza_x.py', estado='pendiente'),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == []


def test_pendiente_que_depende_de_otra_pendiente_no_sale_y_si_esta_hecha_si_sale(tmp_path, monkeypatch):
    # Caso 1: la dependencia esta pendiente -> no sale
    ordenes = [
        _orden('a', 'pieza_a.py', estado='pendiente'),
        _orden('b', 'pieza_b.py', estado='pendiente', depende=['a']),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == ['a']

    # Caso 2: la dependencia esta hecha -> si sale
    ordenes = [
        _orden('a', 'pieza_a.py', estado='hecha'),
        _orden('b', 'pieza_b.py', estado='pendiente', depende=['a']),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == ['b']


def test_pendiente_que_depende_de_un_id_que_no_existe_no_sale(tmp_path, monkeypatch):
    ordenes = [
        _orden('a', 'pieza_a.py', estado='pendiente', depende=['fantasma']),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == []


def test_pendiente_sin_encargo_no_sale(tmp_path, monkeypatch):
    incompleta = _orden('a', 'pieza_a.py', estado='pendiente')
    incompleta['encargo'] = ''
    ordenes = [incompleta]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == []


def test_pendiente_con_huella_ya_fallida_no_sale(tmp_path, monkeypatch):
    orden = _orden('a', 'pieza_a.py', estado='pendiente')
    ordenes = [orden]
    _preparar(tmp_path, monkeypatch, ordenes)
    # Anotamos la huella como fallida antes de pedir la lista
    capataz.anotar_huella_fallida(orden, 'x')
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == []


def test_ordenes_hecha_o_corriendo_nunca_salen(tmp_path, monkeypatch):
    ordenes = [
        _orden('a', 'pieza_a.py', estado='hecha'),
        _orden('b', 'pieza_b.py', estado='corriendo'),
    ]
    _preparar(tmp_path, monkeypatch, ordenes)
    resultado = capataz.listas_para_correr()
    assert _ids(resultado) == []
