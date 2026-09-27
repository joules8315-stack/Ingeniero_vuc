# -*- coding: utf-8 -*-
"""Vigia: el juez no repite la misma corrida.

De que fallo nace
-----------------
La misma prueba se corre hasta cuatro veces en un mismo trabajo (el juez de
la prueba, el capataz y el guardia), y eso es lo que hace que una orden tarde
90 minutos cuando la meta son menos de 20. La pieza arnes/memoria_de_pruebas.py
ya existe y sabe apuntar y reusar el resultado de una corrida mientras no
cambie ningun .py; lo que falta es que el juez la use.

Esta vigia nace ROJA: si el juez todavia no consulta la memoria de pruebas,
los casos 1 y 3 fallan. Cuando el juez la use, los tres casos pasan.

Que comprueba
-------------
- Caso 1: dos llamadas seguidas a la funcion interna del juez que corre la
  prueba, con la misma raiz y la misma ruta, sin cambiar nada en medio, solo
  producen UNA llamada a subprocess.run y las dos respuestas coinciden en su
  primer valor.
- Caso 2: si entre las dos llamadas se cambia un .py de la raiz de mentira y
  se le pone otra fecha de modificacion, se producen DOS llamadas.
- Caso 3: si la memoria ya tiene apuntado que esa prueba con esa raiz salio en
  falso, el juez responde falso y NO llama a subprocess.run: reusar nunca
  convierte un rojo en verde.

Es autocontenida: no importa nada del proyecto salvo por ruta, y no depende de
ninguna funcion del juez que no exista. Si el juez no expone la funcion interna
que corre la prueba, la vigia falla con un mensaje claro en vez de reventar.
"""

import importlib.util
import os
import subprocess
import sys

import pytest


# ---------------------------------------------------------------------------
# Rutas base
# ---------------------------------------------------------------------------

#: Raiz del repo: dos niveles por encima de este archivo (vigias/ -> raiz).
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Ruta del juez de la prueba.
RUTA_JUEZ = os.path.join(RAIZ, 'arnes', 'juez_de_la_prueba.py')

#: Ruta de la memoria de pruebas.
RUTA_MEMORIA = os.path.join(RAIZ, 'arnes', 'memoria_de_pruebas.py')


# ---------------------------------------------------------------------------
# Carga de modulos por ruta
# ---------------------------------------------------------------------------

def _cargar_modulo(ruta, nombre):
    """Carga un archivo .py como modulo por su ruta.

    Devuelve el modulo cargado. Si el archivo no existe, lanza un error claro
    para que la vigia falle diciendo que falta la pieza, no con un traceback
    opaco.
    """
    if not os.path.isfile(ruta):
        raise AssertionError('falta la pieza: %s' % ruta)

    especificacion = importlib.util.spec_from_file_location(nombre, ruta)
    if especificacion is None or especificacion.loader is None:
        raise AssertionError('no se pudo cargar la pieza: %s' % ruta)

    modulo = importlib.util.module_from_spec(especificacion)
    sys.modules[nombre] = modulo
    especificacion.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope='module')
def juez():
    """El modulo del juez de la prueba, cargado por ruta."""
    return _cargar_modulo(RUTA_JUEZ, 'juez_de_la_prueba_vigia')


@pytest.fixture(scope='module')
def memoria():
    """El modulo de la memoria de pruebas, cargado por ruta."""
    return _cargar_modulo(RUTA_MEMORIA, 'memoria_de_pruebas_vigia')


# ---------------------------------------------------------------------------
# Ayudantes
# ---------------------------------------------------------------------------

def _funcion_correr_prueba(juez):
    """Devuelve la funcion interna del juez que corre la prueba.

    El juez la usa por dentro (``_correr_prueba``). Si no existe, la vigia
    falla con un mensaje claro: no se inventa una funcion que el juez no tiene.
    """
    funcion = getattr(juez, '_correr_prueba', None)
    if funcion is None or not callable(funcion):
        raise AssertionError(
            'el juez no expone la funcion interna _correr_prueba(raiz, ruta_prueba); '
            'sin ella no se puede comprobar que no repita la misma corrida'
        )
    return funcion


def _montar_raiz_de_mentira(tmp_path):
    """Crea una raiz de mentira con arnes, cuerpo, vigias y memoria.

    Dentro de arnes, cuerpo y vigias deja un .py con una linea cualquiera, y
    ademas el archivo vigias/test_uno.py, que sera la prueba de mentira.

    Devuelve una tupla (raiz, ruta_prueba, ruta_archivo_cambiable).
    """
    raiz = str(tmp_path)

    for carpeta in ('arnes', 'cuerpo', 'vigias', 'memoria'):
        os.makedirs(os.path.join(raiz, carpeta), exist_ok=True)

    # Un .py cualquiera dentro de cada carpeta vigilada.
    for carpeta in ('arnes', 'cuerpo', 'vigias'):
        ruta = os.path.join(raiz, carpeta, 'pieza_%s.py' % carpeta)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write('# pieza de mentira de %s\n' % carpeta)

    # La prueba de mentira.
    ruta_prueba = os.path.join(raiz, 'vigias', 'test_uno.py')
    with open(ruta_prueba, 'w', encoding='utf-8') as f:
        f.write('# prueba de mentira\n')

    # El archivo que se cambia en el caso 2.
    ruta_archivo = os.path.join(raiz, 'cuerpo', 'pieza_cuerpo.py')

    return raiz, ruta_prueba, ruta_archivo


def _doble_de_subprocess_run(llamadas):
    """Devuelve un doble de subprocess.run que apunta cada llamada.

    Apunta los argumentos en la lista recibida y devuelve un
    subprocess.CompletedProcess con returncode 0 y stdout vacio.
    """
    def doble(*args, **kwargs):
        llamadas.append((args, kwargs))
        return subprocess.CompletedProcess(
            args=args[0] if args else kwargs.get('args', []),
            returncode=0,
            stdout='',
            stderr='',
        )
    return doble


# ---------------------------------------------------------------------------
# Caso 1: dos veces la misma prueba solo se corre una
# ---------------------------------------------------------------------------

def test_dos_veces_la_misma_prueba_solo_se_corre_una(tmp_path, monkeypatch, juez):
    """Dos llamadas seguidas, sin cambiar nada, solo producen UNA corrida."""
    raiz, ruta_prueba, _ = _montar_raiz_de_mentira(tmp_path)
    correr = _funcion_correr_prueba(juez)

    llamadas = []
    monkeypatch.setattr(juez.subprocess, 'run', _doble_de_subprocess_run(llamadas))

    primera = correr(raiz, ruta_prueba)
    segunda = correr(raiz, ruta_prueba)

    assert len(llamadas) == 1, (
        'la misma prueba con la misma raiz se corrio %d veces; debe correrse una sola'
        % len(llamadas)
    )
    assert primera[0] == segunda[0], (
        'las dos respuestas deben decir lo mismo en su primer valor: %r vs %r'
        % (primera[0], segunda[0])
    )


# ---------------------------------------------------------------------------
# Caso 2: si cambia un archivo se vuelve a correr
# ---------------------------------------------------------------------------

def test_si_cambia_un_archivo_se_vuelve_a_correr(tmp_path, monkeypatch, juez):
    """Si cambia un .py de la raiz, la prueba se vuelve a correr."""
    raiz, ruta_prueba, ruta_archivo = _montar_raiz_de_mentira(tmp_path)
    correr = _funcion_correr_prueba(juez)

    llamadas = []
    monkeypatch.setattr(juez.subprocess, 'run', _doble_de_subprocess_run(llamadas))

    correr(raiz, ruta_prueba)

    # Cambiar el contenido de un .py de la raiz de mentira.
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write('# pieza de mentira cambiada\n')

    # Ponerle una fecha de modificacion distinta.
    ahora = os.path.getmtime(ruta_archivo)
    os.utime(ruta_archivo, (ahora + 10, ahora + 10))

    correr(raiz, ruta_prueba)

    assert len(llamadas) == 2, (
        'al cambiar un .py la prueba debe volver a correrse; se corrio %d veces'
        % len(llamadas)
    )


# ---------------------------------------------------------------------------
# Caso 3: un apunte rojo no se vuelve verde
# ---------------------------------------------------------------------------

def test_un_apunte_rojo_no_se_vuelve_verde(tmp_path, monkeypatch, juez, memoria):
    """Si la memoria dice que salio en falso, el juez responde falso y no corre."""
    raiz, ruta_prueba, _ = _montar_raiz_de_mentira(tmp_path)
    correr = _funcion_correr_prueba(juez)

    # Apuntar a mano que esa prueba con esa raiz salio en falso.
    memoria.apuntar(raiz, [ruta_prueba], False, 'apunte rojo de la vigia')

    llamadas = []
    monkeypatch.setattr(juez.subprocess, 'run', _doble_de_subprocess_run(llamadas))

    respuesta = correr(raiz, ruta_prueba)

    assert respuesta[0] is False, (
        'un apunte rojo debe devolver falso en su primer valor; devolvio %r'
        % (respuesta[0],)
    )
    assert len(llamadas) == 0, (
        'reusar un apunte rojo no debe correr la prueba; se corrio %d veces'
        % len(llamadas)
    )
