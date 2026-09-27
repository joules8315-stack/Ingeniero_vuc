# -*- coding: utf-8 -*-
"""Vigia: la misma prueba no se corre dos veces en un mismo trabajo.

De que fallo nace
-----------------
La misma prueba se corre hasta cuatro veces en un mismo trabajo (el juez de
la prueba, el capataz y el guardia), y cada corrida cuesta minutos. Hacen
falta menos de 20 minutos por orden y hoy son 90. Esta vigia prueba la pieza
nueva arnes/memoria_de_pruebas.py, que apunta el resultado de una prueba y lo
reusa si nada cambio, para no repetir la misma corrida.

Nace ROJA porque la pieza arnes/memoria_de_pruebas.py todavia no existe.
"""

import importlib.util
import json
import os
import time

import pytest


# ---------------------------------------------------------------------------
# Carga de la pieza que se prueba
# ---------------------------------------------------------------------------

def _raiz_del_repo():
    """Raiz del repo: dos carpetas por encima de este archivo."""
    aqui = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(aqui))


def _cargar_memoria():
    """Carga arnes/memoria_de_pruebas.py por ruta.

    Si el archivo todavia no existe, se llama a pytest.fail con un mensaje en
    palabras simples: nunca un ImportError pelado en la cara de Julio.
    """
    raiz = _raiz_del_repo()
    ruta = os.path.join(raiz, 'arnes', 'memoria_de_pruebas.py')
    if not os.path.isfile(ruta):
        pytest.fail(
            'Falta la pieza arnes/memoria_de_pruebas.py. Sin ella no se puede '
            'apuntar el resultado de una prueba ni reusarlo, y la misma prueba '
            'se sigue corriendo cuatro veces en un mismo trabajo.'
        )
    especificacion = importlib.util.spec_from_file_location(
        'memoria_de_pruebas_de_la_vigia', ruta
    )
    if especificacion is None or especificacion.loader is None:
        pytest.fail(
            'No se pudo cargar arnes/memoria_de_pruebas.py desde ' + ruta +
            '. Revisa que el archivo sea Python valido.'
        )
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


# ---------------------------------------------------------------------------
# Ayudante: raiz de mentira dentro de tmp_path
# ---------------------------------------------------------------------------

def _raiz_de_mentira(tmp_path):
    """Crea una raiz de mentira con arnes, cuerpo, vigias y memoria.

    Dentro de arnes, cuerpo y vigias deja un .py con una linea cualquiera.
    Devuelve la ruta de la raiz de mentira.
    """
    raiz = str(tmp_path)
    for carpeta in ('arnes', 'cuerpo', 'vigias', 'memoria'):
        os.makedirs(os.path.join(raiz, carpeta), exist_ok=True)
    for carpeta, nombre in (
        ('arnes', 'pieza.py'),
        ('cuerpo', 'modulo.py'),
        ('vigias', 'test_uno.py'),
    ):
        with open(os.path.join(raiz, carpeta, nombre), 'w', encoding='utf-8') as f:
            f.write('# linea cualquiera\n')
    return raiz


def _archivos_dentro_de_memoria(raiz):
    """Devuelve las rutas de archivo que hay dentro de la carpeta memoria."""
    carpeta = os.path.join(raiz, 'memoria')
    encontrados = []
    if not os.path.isdir(carpeta):
        return encontrados
    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        if os.path.isfile(ruta):
            encontrados.append(ruta)
    return encontrados


# ---------------------------------------------------------------------------
# Caso 1: lo apuntado se reusa
# ---------------------------------------------------------------------------

def test_lo_apuntado_se_reusa(tmp_path):
    memoria = _cargar_memoria()
    raiz = _raiz_de_mentira(tmp_path)
    objetivos = ['vigias/test_uno.py']
    detalle = 'la prueba paso en 3 segundos'

    memoria.apuntar(raiz, objetivos, True, detalle)
    reusado = memoria.recordar(raiz, objetivos)

    assert isinstance(reusado, dict), (
        'recordar deberia devolver un diccionario cuando hay un apunte fresco'
    )
    assert reusado.get('paso') is True
    assert reusado.get('detalle') == detalle


# ---------------------------------------------------------------------------
# Caso 2: si cambia un archivo, no se reusa
# ---------------------------------------------------------------------------

def test_si_cambia_un_archivo_no_se_reusa(tmp_path):
    memoria = _cargar_memoria()
    raiz = _raiz_de_mentira(tmp_path)
    objetivos = ['vigias/test_uno.py']

    memoria.apuntar(raiz, objetivos, True, 'paso antes del cambio')

    # Se cambia el contenido de uno de los .py de la raiz de mentira.
    cambiado = os.path.join(raiz, 'cuerpo', 'modulo.py')
    with open(cambiado, 'w', encoding='utf-8') as f:
        f.write('# contenido cambiado\n')

    # Y se le pone una fecha de modificacion distinta, para no depender del
    # reloj del disco.
    ahora = time.time()
    os.utime(cambiado, (ahora + 10, ahora + 10))

    assert memoria.recordar(raiz, objetivos) is None


# ---------------------------------------------------------------------------
# Caso 3: un apunte viejo no se reusa
# ---------------------------------------------------------------------------

def test_un_apunte_viejo_no_se_reusa(tmp_path):
    memoria = _cargar_memoria()
    raiz = _raiz_de_mentira(tmp_path)
    objetivos = ['vigias/test_uno.py']

    memoria.apuntar(raiz, objetivos, True, 'paso hace rato')

    # Con ventana cero, ningun apunte es mas nuevo que cero segundos.
    assert memoria.recordar(raiz, objetivos, ventana_segundos=0) is None


# ---------------------------------------------------------------------------
# Caso 4: un apunte roto no revienta
# ---------------------------------------------------------------------------

def test_un_apunte_roto_no_revienta(tmp_path):
    memoria = _cargar_memoria()
    raiz = _raiz_de_mentira(tmp_path)
    objetivos = ['vigias/test_uno.py']

    memoria.apuntar(raiz, objetivos, True, 'paso y luego se rompio el apunte')

    # No se da por sabido el nombre exacto del archivo de apuntes: se busca
    # cualquier archivo que la pieza haya creado dentro de memoria y se rompe.
    archivos = _archivos_dentro_de_memoria(raiz)
    assert archivos, (
        'la pieza deberia haber creado algun archivo dentro de memoria al apuntar'
    )
    for ruta in archivos:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write('esto no es JSON {{{')

    # No debe lanzar ninguna excepcion: devuelve None.
    resultado = memoria.recordar(raiz, objetivos)
    assert resultado is None
