import subprocess
import shutil
import json
from cuerpo import capataz


class _Respuesta:
    """Objeto que imita lo que devuelve subprocess.run: stdout, stderr y returncode."""

    def __init__(self, stdout='', stderr='', returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def _montar(monkeypatch, respuestas):
    """Deja shutil.which devolviendo 'claude' y subprocess.run falso.

    Devuelve (ordenes, entradas) donde ordenes guarda el primer argumento de
    cada llamada y entradas guarda el input de cada llamada.
    """
    monkeypatch.setattr(shutil, 'which', lambda nombre: 'claude')
    ordenes = []
    entradas = []
    cola = list(respuestas)

    def falso_run(orden, *args, **kwargs):
        ordenes.append(orden)
        entradas.append(kwargs.get('input'))
        if cola:
            texto = cola.pop(0)
        else:
            texto = ''
        return _Respuesta(stdout=texto, stderr='', returncode=0)

    monkeypatch.setattr(subprocess, 'run', falso_run)
    return ordenes, entradas


def test_la_orden_exige_json_schema(monkeypatch):
    """La primera llamada al perito tiene que pedir el JSON con --json-schema."""
    ordenes, _ = _montar(monkeypatch, ['{"que_paso": "x", "causa_raiz": "y"}'])
    capataz.pedir_al_perito({'fallo': 'algo'}, '.')
    assert ordenes, 'no se llamo al perito'
    assert '--json-schema' in ordenes[0]


def test_si_la_primera_no_trae_json_reintenta_con_recordatorio(monkeypatch):
    """Si la primera respuesta no trae JSON, la segunda lleva RECORDATORIO y devuelve dict."""
    respuestas = [
        'esto no es JSON, es texto suelto',
        '{"que_paso": "x", "causa_raiz": "y"}',
    ]
    ordenes, entradas = _montar(monkeypatch, respuestas)
    datos, estado = capataz.pedir_al_perito({'fallo': 'algo'}, '.')
    assert isinstance(datos, dict)
    assert datos.get('que_paso') == 'x'
    assert len(ordenes) == 2
    assert 'RECORDATORIO' in (entradas[1] or '')


def test_si_las_tres_son_texto_devuelve_none_y_tres_llamadas(monkeypatch):
    """Si las tres respuestas son texto sin JSON, devuelve None y se llamo 3 veces."""
    respuestas = ['texto uno', 'texto dos', 'texto tres']
    ordenes, _ = _montar(monkeypatch, respuestas)
    datos, estado = capataz.pedir_al_perito({'fallo': 'algo'}, '.')
    assert datos is None
    assert len(ordenes) == 3


def test_si_la_primera_ya_es_json_solo_una_llamada(monkeypatch):
    """Si la primera respuesta ya es JSON valido, se llama una sola vez."""
    respuestas = ['{"que_paso": "x", "causa_raiz": "y"}']
    ordenes, _ = _montar(monkeypatch, respuestas)
    datos, estado = capataz.pedir_al_perito({'fallo': 'algo'}, '.')
    assert isinstance(datos, dict)
    assert datos.get('que_paso') == 'x'
    assert len(ordenes) == 1
