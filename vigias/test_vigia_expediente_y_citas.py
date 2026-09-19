"""Vigia del expediente y de las citas del capataz.

Comprueba que armar_expediente guarda el json donde toca y con lo que toca,
y que citas_que_no_existen detecta las citas malas sin lanzar.
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo import capataz


@pytest.fixture
def aislado(tmp_path, monkeypatch):
    """Deja a capataz creyendo que vive en tmp_path/cuerpo y crea tmp_path/memoria."""
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir()
    monkeypatch.setattr(capataz, '__file__', str(carpeta_cuerpo / 'capataz.py'))
    (tmp_path / 'memoria').mkdir()
    return tmp_path


def test_expediente_guarda_json_con_tipo_huella_y_orden(aislado):
    orden = {'id': 'P7', 'pieza': 'cuerpo/x.py', 'encargo': 'e'}
    resultado = {'guardado': False, 'codigo': 0, 'salida': 'algo\nEL EQUIPO NO APROBO'}
    ruta, datos = capataz.armar_expediente(orden, resultado)
    assert ruta is not None
    carpeta = aislado / 'memoria' / 'EXPEDIENTES'
    assert os.path.dirname(os.path.abspath(ruta)) == str(carpeta)
    assert os.path.exists(ruta)
    assert os.path.basename(ruta).startswith('P7_')
    with open(ruta, encoding='utf-8') as f:
        guardado = json.load(f)
    assert guardado['tipo'] == 'no_aprobo'
    assert guardado['huella'] == capataz.huella_de(orden)
    assert guardado['orden'] == orden
    assert datos['tipo'] == 'no_aprobo'


def test_expediente_corta_la_salida_a_las_ultimas_4000(aislado):
    orden = {'id': 'P8', 'pieza': 'cuerpo/x.py', 'encargo': 'e'}
    salida = 'a' * 10000
    ruta, datos = capataz.armar_expediente(orden, {'guardado': False, 'codigo': 1, 'salida': salida})
    assert len(datos['salida']) == 4000
    assert datos['salida'] == salida[-4000:]


def test_expediente_apartados_solo_los_de_la_pieza(aislado):
    carpeta = aislado / 'memoria' / 'trabajos_sin_revisar'
    carpeta.mkdir()
    (carpeta / 'x.py.FRENADO_POR_EL_GUARDIA').write_text('', encoding='utf-8')
    (carpeta / 'otro.py.FRENADO_POR_EL_GUARDIA').write_text('', encoding='utf-8')
    orden = {'id': 'P9', 'pieza': 'cuerpo/x.py', 'encargo': 'e'}
    ruta, datos = capataz.armar_expediente(orden, {'guardado': False, 'codigo': 1, 'salida': 'x'})
    assert datos['apartados'] == ['x.py.FRENADO_POR_EL_GUARDIA']


def _raiz_con_a(tmp_path):
    (tmp_path / 'a.py').write_bytes(b'def hola():\r\n    return 1\r\n')
    return tmp_path


def test_cita_con_salto_de_windows_si_existe(tmp_path):
    raiz = _raiz_con_a(tmp_path)
    citas = [{'archivo': 'a.py', 'texto': 'def hola():\n    return 1'}]
    assert capataz.citas_que_no_existen(citas, raiz) == []


def test_cita_que_no_aparece_literal(tmp_path):
    raiz = _raiz_con_a(tmp_path)
    citas = [{'archivo': 'a.py', 'texto': 'return 2'}]
    malas = capataz.citas_que_no_existen(citas, raiz)
    assert len(malas) == 1
    assert malas[0]['por_que'] == 'no aparece literal'


def test_cita_de_archivo_que_no_existe(tmp_path):
    citas = [{'archivo': 'b.py', 'texto': 'algo'}]
    malas = capataz.citas_que_no_existen(citas, tmp_path)
    assert len(malas) == 1
    assert malas[0]['por_que'] == 'el archivo no existe'


def test_cita_fuera_del_proyecto(tmp_path):
    citas = [{'archivo': '../fuera.py', 'texto': 'algo'}]
    malas = capataz.citas_que_no_existen(citas, tmp_path)
    assert len(malas) == 1
    assert malas[0]['por_que'] == 'fuera del proyecto'


def test_cita_vacia(tmp_path):
    citas = [{'archivo': 'a.py', 'texto': '   '}]
    malas = capataz.citas_que_no_existen(citas, tmp_path)
    assert len(malas) == 1
    assert malas[0]['por_que'] == 'cita vacia'


def test_archivo_binario_no_lanza(tmp_path):
    (tmp_path / 'c.bin').write_bytes(b'\xff\xfe\x00')
    citas = [{'archivo': 'c.bin', 'texto': 'algo'}]
    malas = capataz.citas_que_no_existen(citas, tmp_path)
    assert len(malas) == 1
    assert malas[0]['por_que'] == 'el archivo no existe'


def test_citas_que_no_son_lista(tmp_path):
    malas = capataz.citas_que_no_existen('hola', tmp_path)
    assert len(malas) == 1
    assert malas[0]['por_que'] == 'no hay lista de citas'


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
