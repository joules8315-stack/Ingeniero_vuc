"""Vigia: al perito no le ponen los candados de Julio.

La funcion pedir_al_perito de cuerpo/capataz.py llama a subprocess.run para
preguntarle al perito. Esa llamada tiene que llevar su PROPIO entorno con la
marca INGENIERO_OFF puesta a 1, para que los candados pensados para hablar
con Julio no le prohiban al perito contestar en formato JSON.

Esta vigia NO ejecuta nada: monkeypatch sobre subprocess.run y sobre
shutil.which dentro de cuerpo/capataz.py para espiar como se llama.
"""

import importlib
import json
import os
import sys

import pytest


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


class _ResultadoFalso:
    """Imita lo justo de un CompletedProcess para que pedir_al_perito siga."""

    def __init__(self, stdout='', returncode=0):
        self.stdout = stdout
        self.stderr = ''
        self.returncode = returncode


@pytest.fixture
def capataz(monkeypatch):
    """Importa cuerpo/capataz.py y deja espiar subprocess.run y shutil.which."""
    capataz = importlib.import_module('cuerpo.capataz')
    llamadas = {'run': [], 'which': []}

    def which_falso(nombre):
        llamadas['which'].append(nombre)
        return '/usr/bin/' + str(nombre)

    def run_falso(*args, **kwargs):
        llamadas['run'].append({'args': args, 'kwargs': kwargs})
        # El perito contesta un JSON valido para que pedir_al_perito llegue al final.
        salida = json.dumps({
            'que_paso': 'prueba',
            'causa_raiz': 'prueba',
            'donde': 'prueba',
            'quien_fallo': 'prueba',
            'citas': [],
            'no_volver_a': 'prueba',
            'tarea_nueva': {
                'repara': 'prueba',
                'pieza': 'prueba',
                'razon': 'prueba',
                'encargo': 'prueba',
                'modo': 'PROGRAMA',
            },
        })
        return _ResultadoFalso(stdout=salida, returncode=0)

    monkeypatch.setattr(shutil, 'which', which_falso)
    monkeypatch.setattr(subprocess, 'run', run_falso)
    return capataz, llamadas


def test_el_perito_lleva_su_propio_entorno_con_ingeniero_off(capataz):
    """La llamada al perito tiene que llevar env con INGENIERO_OFF=1."""
    modulo, llamadas = capataz
    expediente = {'fallo': 'prueba'}
    datos, mensaje = modulo.pedir_al_perito(expediente, RAIZ)

    assert mensaje == 'ok', 'pedir_al_perito no llego al final: %r' % (mensaje,)
    assert datos is not None
    assert len(llamadas['run']) == 1, 'se esperaba UNA llamada a subprocess.run'

    kwargs = llamadas['run'][0]['kwargs']
    assert 'env' in kwargs, 'la llamada al perito no lleva env propio'
    env = kwargs['env']
    assert isinstance(env, dict), 'el env del perito no es un diccionario'
    assert env.get('INGENIERO_OFF') == '1', (
        'la marca INGENIERO_OFF no esta puesta a 1 en el entorno del perito: %r'
        % (env.get('INGENIERO_OFF'),)
    )


def test_el_entorno_del_perito_no_pisa_el_del_proceso(capataz, monkeypatch):
    """El env del perito es SUYO: no debe ser el os.environ del proceso."""
    modulo, llamadas = capataz
    monkeypatch.setenv('INGENIERO_OFF', '0')

    datos, mensaje = modulo.pedir_al_perito({'fallo': 'prueba'}, RAIZ)
    assert mensaje == 'ok'
    assert len(llamadas['run']) == 1

    env = llamadas['run'][0]['kwargs'].get('env')
    assert env is not None, 'la llamada al perito no lleva env propio'
    assert env.get('INGENIERO_OFF') == '1', (
        'el env del perito no fuerza INGENIERO_OFF=1 aunque el proceso lo tenga a 0'
    )


def test_el_perito_se_busca_con_shutil_which(capataz):
    """Se espia shutil.which para comprobar que se busca el ejecutable del perito."""
    modulo, llamadas = capataz
    modulo.pedir_al_perito({'fallo': 'prueba'}, RAIZ)
    assert 'claude' in llamadas['which'], (
        'no se busco claude con shutil.which: %r' % (llamadas['which'],)
    )


def test_sin_perito_no_se_llama_a_subprocess(capataz, monkeypatch):
    """Si no hay claude en el PATH, no se ejecuta nada."""
    modulo, llamadas = capataz
    monkeypatch.setattr(modulo.shutil, 'which', lambda nombre: None)

    datos, mensaje = modulo.pedir_al_perito({'fallo': 'prueba'}, RAIZ)
    assert datos is None
    assert 'claude' in mensaje
    assert llamadas['run'] == [], 'no se debe llamar a subprocess.run sin perito'
