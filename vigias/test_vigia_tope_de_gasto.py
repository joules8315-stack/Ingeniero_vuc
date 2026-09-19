# -*- coding: utf-8 -*-

"""Vigia del tope de gasto del pit (plan v4 P3-8).

Comprueba que el costo de DeepSeek se calcula bien, que el gasto del mes
suma lo que debe y que el registro de DeepSeek deja su linea. Todo aislado
en tmp_path: nunca toca la memoria real.
"""
import datetime
import io
import json
import os
import sys
import urllib.request

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from cuerpo import capataz  # noqa: E402
from cuerpo import obrero   # noqa: E402


@pytest.fixture
def aislado(tmp_path, monkeypatch):
    """Deja capataz y obrero mirando a una memoria de mentira en tmp_path."""
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir()
    monkeypatch.setattr(capataz, '__file__', str(carpeta_cuerpo / 'capataz.py'))
    memoria = tmp_path / 'memoria'
    memoria.mkdir()
    ruta_gasto = memoria / 'GASTO_USD.jsonl'
    monkeypatch.setenv('INGENIERO_GASTO_USD_TEST', str(ruta_gasto))
    return {'tmp_path': tmp_path, 'memoria': memoria, 'ruta_gasto': ruta_gasto}


def test_costo_deepseek_pro(aislado):
    """Un millon de cada cosa con el modelo pro da 0.044 + 1.32 + 3.96."""
    uso = {'prompt_cache_hit_tokens': 1000000,
           'prompt_cache_miss_tokens': 1000000,
           'completion_tokens': 1000000}
    esperado = 0.044 + 1.32 + 3.96
    assert capataz.costo_deepseek('deepseek-v4-pro', uso) == pytest.approx(esperado)


def test_costo_deepseek_flash(aislado):
    """Si el modelo trae 'Flash' se usa la tabla flash: 0.006 + 0.30 + 1.20."""
    uso = {'prompt_cache_hit_tokens': 1000000,
           'prompt_cache_miss_tokens': 1000000,
           'completion_tokens': 1000000}
    esperado = 0.006 + 0.30 + 1.20
    assert capataz.costo_deepseek('deepseek-v4-Flash', uso) == pytest.approx(esperado)


def test_costo_deepseek_desconocido_cobra_como_pro(aislado):
    """Un modelo que no se conoce se cobra como el caro (pro)."""
    uso = {'prompt_cache_hit_tokens': 1000000,
           'prompt_cache_miss_tokens': 1000000,
           'completion_tokens': 1000000}
    esperado = 0.044 + 1.32 + 3.96
    assert capataz.costo_deepseek('modelo-raro-xyz', uso) == pytest.approx(esperado)


def test_costo_deepseek_solo_prompt_tokens_cobra_como_fallo(aislado):
    """Si solo viene prompt_tokens se cobra como fallo (miss)."""
    uso = {'prompt_tokens': 1000000}
    esperado = 1.32
    assert capataz.costo_deepseek('deepseek-v4-pro', uso) == pytest.approx(esperado)


def test_gastado_del_mes_suma_jsonl_y_log(aislado):
    """Suma las lineas de septiembre, ignora agosto y la linea rota, y suma el costo del log."""
    ruta = aislado['ruta_gasto']
    lineas = [
        json.dumps({'cuando': '2026-09-19T09:00:00', 'modelo': 'deepseek-v4-pro',
                    'uso': {'prompt_cache_hit_tokens': 1000000}}),
        json.dumps({'cuando': '2026-08-31T10:00:00', 'modelo': 'deepseek-v4-pro',
                    'uso': {'prompt_cache_hit_tokens': 1000000}}),
        'esto no es json',
    ]
    with open(ruta, 'w', encoding='utf-8') as f:
        for l in lineas:
            f.write(l + '\n')
    log = aislado['memoria'] / 'BIGPICKLE.log'
    with open(log, 'w', encoding='utf-8') as f:
        f.write('2026-09-19T09:17:21\tsegundos=47.0\tcosto=0.250000\tok=True\tnota=ok\n')
        f.write('2026-08-15T09:17:21\tsegundos=47.0\tcosto=9.990000\tok=True\tnota=viejo\n')
    total = capataz.gastado_del_mes(datetime.date(2026, 9, 19))
    assert total == pytest.approx(0.044 + 0.250000)


def test_sin_archivos_gastado_cero_y_no_pasado(aislado):
    """Sin ningun archivo el gasto es 0 y no se ha pasado del tope."""
    assert capataz.gastado_del_mes(datetime.date(2026, 9, 19)) == 0
    assert capataz.se_paso_del_tope(datetime.date(2026, 9, 19)) is False


def test_con_cinco_usd_se_paso_del_tope(aislado):
    """Con 5 USD o mas en el mes se_paso_del_tope es True."""
    ruta = aislado['ruta_gasto']
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'cuando': '2026-09-19T09:00:00', 'modelo': 'deepseek-v4-pro',
                            'uso': {'prompt_cache_miss_tokens': 5000000}}) + '\n')
    assert capataz.gastado_del_mes(datetime.date(2026, 9, 19)) >= 5
    assert capataz.se_paso_del_tope(datetime.date(2026, 9, 19)) is True


def test_deepseek_directo_deja_su_linea(aislado, monkeypatch):
    """_deepseek_directo devuelve el contenido y deja su linea en GASTO_USD.jsonl."""
    monkeypatch.setenv('DEEPSEEK_API_KEY', 'x')
    respuesta = {'model': 'deepseek-v4-flash',
                 'usage': {'completion_tokens': 5},
                 'choices': [{'message': {'content': 'hola'}}]}
    cuerpo = json.dumps(respuesta).encode('utf-8')

    class _Falsa:
        def __enter__(self):
            return io.BytesIO(cuerpo)

        def __exit__(self, *a):
            return False

    def falsa(*args, **kwargs):
        return _Falsa()

    monkeypatch.setattr(urllib.request, 'urlopen', falsa)
    salida = obrero._deepseek_directo('p', 0, None)
    assert salida == 'hola'
    ruta = aislado['ruta_gasto']
    with open(ruta, encoding='utf-8') as f:
        lineas = [json.loads(l) for l in f if l.strip()]
    assert len(lineas) == 1
    assert lineas[0]['modelo'] == 'deepseek-v4-flash'
    assert lineas[0]['uso'] == {'completion_tokens': 5}
