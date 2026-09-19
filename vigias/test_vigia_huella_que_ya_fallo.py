"""Vigia: un encargo que ya fallo no se vuelve a mandar igual.

Prueba cuerpo/capataz.py: huella_de, anotar_huella_fallida y ya_fallo.
Cada prueba aisla el modulo con monkeypatch sobre __file__ y usa una
memoria de mentira en tmp_path. Nunca toca la memoria real.
"""

import json
import os

import pytest

from cuerpo import capataz


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    """Deja capataz.py apuntando a una carpeta falsa y crea su memoria."""
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir()
    monkeypatch.setattr(capataz, '__file__', str(carpeta_cuerpo / 'capataz.py'))
    memoria = tmp_path / 'memoria'
    memoria.mkdir()
    return tmp_path


def _orden(id_orden, encargo, pieza):
    """Fabrica una orden minima con id, encargo y pieza."""
    return {'id': id_orden, 'encargo': encargo, 'pieza': pieza}


def test_huella_igual_si_encargo_y_pieza_iguales_aunque_cambie_el_id(entorno):
    """Dos ordenes con igual encargo y pieza dan la misma huella de 16 caracteres."""
    orden_a = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    orden_b = _orden('B-2', 'arreglar el capataz', 'cuerpo/capataz.py')
    huella_a = capataz.huella_de(orden_a)
    huella_b = capataz.huella_de(orden_b)
    assert huella_a == huella_b
    assert isinstance(huella_a, str)
    assert len(huella_a) == 16


def test_huella_cambia_si_cambia_el_encargo(entorno):
    """Si cambia el encargo, cambia la huella."""
    orden_a = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    orden_b = _orden('A-1', 'arreglar la vigia', 'cuerpo/capataz.py')
    assert capataz.huella_de(orden_a) != capataz.huella_de(orden_b)


def test_huella_cambia_si_cambia_la_pieza(entorno):
    """Si cambia la pieza, cambia la huella."""
    orden_a = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    orden_b = _orden('A-1', 'arreglar el capataz', 'cuerpo/obrero.py')
    assert capataz.huella_de(orden_a) != capataz.huella_de(orden_b)


def test_sin_anotar_nada_ya_fallo_es_false(entorno):
    """Sin archivo de huellas, ya_fallo devuelve False."""
    orden = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    assert capataz.ya_fallo(orden) is False


def test_tras_anotar_ya_fallo_es_true_y_otra_orden_no(entorno):
    """Tras anotar la huella, esa orden falla y otra con distinto encargo no."""
    orden = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    capataz.anotar_huella_fallida(orden, 'vigia roja')
    assert capataz.ya_fallo(orden) is True
    otra = _orden('A-1', 'arreglar la vigia', 'cuerpo/capataz.py')
    assert capataz.ya_fallo(otra) is False


def test_otro_id_mismo_encargo_y_pieza_tambien_ya_fallo(entorno):
    """Una orden con otro id pero mismo encargo y pieza tambien da ya_fallo True."""
    orden = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    capataz.anotar_huella_fallida(orden, 'vigia roja')
    gemela = _orden('Z-9', 'arreglar el capataz', 'cuerpo/capataz.py')
    assert capataz.ya_fallo(gemela) is True


def test_linea_rota_antes_de_la_buena_no_lanza_y_encuentra_la_buena(entorno):
    """Una linea JSON rota antes de la buena no impide encontrar la buena."""
    orden = _orden('A-1', 'arreglar el capataz', 'cuerpo/capataz.py')
    ruta = os.path.join(str(entorno), 'memoria', 'HUELLAS_QUE_FALLARON.jsonl')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('{no es json\n')
        f.write(json.dumps({'huella': capataz.huella_de(orden), 'id': 'A-1',
                            'motivo': 'vigia roja', 'fecha': '2026-09-19'},
                           ensure_ascii=False) + '\n')
    assert capataz.ya_fallo(orden) is True
