import os

from cuerpo import capataz


def _orden(tmp_path):
    return {
        'id': '9',
        'pieza': 'pieza.py',
        'vigia': 'vigias/test_x.py',
        'sabotaje': str(tmp_path / 'no_existe.json'),
    }


def test_si_armar_sabotaje_devuelve_false_no_se_corre_la_orden(tmp_path, monkeypatch):
    llamadas = []

    def correr_falso(palabras):
        llamadas.append(palabras)
        return 0

    def armar_falso(orden, raiz=None):
        return False

    monkeypatch.setattr(capataz, 'correr_orden_del_sistema', correr_falso)
    monkeypatch.setattr(capataz, 'armar_sabotaje', armar_falso)

    resultado = capataz.sabotear_la_orden(_orden(tmp_path))

    assert isinstance(resultado, dict)
    assert resultado.get('ok') is None
    assert 'armar' in str(resultado.get('razon', '')).lower()
    assert llamadas == []


def test_si_armar_sabotaje_devuelve_true_se_corre_la_orden_una_vez(tmp_path, monkeypatch):
    llamadas = []

    def correr_falso(palabras):
        llamadas.append(palabras)
        return 0

    def armar_falso(orden, raiz=None):
        return True

    monkeypatch.setattr(capataz, 'correr_orden_del_sistema', correr_falso)
    monkeypatch.setattr(capataz, 'armar_sabotaje', armar_falso)

    resultado = capataz.sabotear_la_orden(_orden(tmp_path))

    assert len(llamadas) == 1
    assert isinstance(resultado, dict)
    assert resultado.get('ok') is True


def test_una_orden_sin_ruta_de_sabotaje_recibe_una_y_se_sabotea(tmp_path, monkeypatch):
    llamadas = []
    ordenes = []

    def correr_falso(palabras):
        llamadas.append(palabras)
        return 0

    def armar_falso(orden, raiz=None):
        ordenes.append(orden)
        return True

    monkeypatch.setattr(capataz, 'correr_orden_del_sistema', correr_falso)
    monkeypatch.setattr(capataz, 'armar_sabotaje', armar_falso)

    orden = {'id': '9', 'pieza': 'pieza.py', 'vigia': 'vigias/test_x.py'}
    resultado = capataz.sabotear_la_orden(orden)

    assert len(ordenes) == 1
    assert ordenes[0].get('sabotaje') == 'memoria/sabotajes/orden_9.json'
    assert len(llamadas) == 1
    assert resultado.get('ok') is True


def test_una_orden_que_cambia_su_propia_prueba_no_se_sabotea(tmp_path, monkeypatch):
    llamadas = []
    ordenes = []

    def correr_falso(palabras):
        llamadas.append(palabras)
        return 0

    def armar_falso(orden, raiz=None):
        ordenes.append(orden)
        return True

    monkeypatch.setattr(capataz, 'correr_orden_del_sistema', correr_falso)
    monkeypatch.setattr(capataz, 'armar_sabotaje', armar_falso)

    orden = {'id': '9', 'pieza': 'vigias/test_x.py', 'vigia': 'vigias/test_x.py'}
    resultado = capataz.sabotear_la_orden(orden)

    assert ordenes == []
    assert llamadas == []
    assert resultado.get('ok') is None
