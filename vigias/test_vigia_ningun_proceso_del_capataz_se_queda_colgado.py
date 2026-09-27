# -*- coding: utf-8 -*-
"""Vigia: ningun proceso del capataz se queda colgado.

De que fallo nace
------------------
cuerpo/capataz.py declara en su cabecera los topes de tiempo medidos
(LIMITE_TAREA_SEGUNDOS, SIN_AVANCE_SEGUNDOS, TOPE_DURO_SEGUNDOS), pero cuatro
llamadas a subprocess.run del mismo archivo salen SIN tope de tiempo. Un
guardado ya se quedo colgado 5 horas y media por eso. Ademas, la funcion
correr_orden_del_sistema llama a subprocess.run sin timeout y sin capturar
subprocess.TimeoutExpired, asi que un proceso colgado revienta al capataz en
vez de contarse como fallo.

Los dos casos nacen rojos a proposito
-------------------------------------
- CASO 1 (test_toda_llamada_a_subprocess_run_del_capataz_lleva_tope): hoy hay
  llamadas a subprocess.run sin timeout en cuerpo/capataz.py, asi que este caso
  falla nombrando las lineas culpables. Nace rojo.
- CASO 2 (test_si_una_orden_del_sistema_se_cuelga_se_devuelve_fallo_y_no_se_rompe):
  hoy correr_orden_del_sistema no captura TimeoutExpired, asi que la excepcion
  se propaga y el caso falla. Nace rojo.

Cuando el capataz se repare (todas las llamadas con timeout y correr_orden_del_sistema
capturando TimeoutExpired devolviendo un numero distinto de cero), los dos casos
pasaran a verde. Esa es la senal de que la reparacion esta hecha.
"""

import ast
import importlib.util
import os
import subprocess
import sys


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CAPATAZ = os.path.join(RAIZ, 'cuerpo', 'capataz.py')


def _es_subprocess_run(nodo):
    """Devuelve True si el nodo ast.Call es una llamada a subprocess.run."""
    if not isinstance(nodo, ast.Call):
        return False
    funcion = nodo.func
    if not isinstance(funcion, ast.Attribute):
        return False
    if funcion.attr != 'run':
        return False
    valor = funcion.value
    if isinstance(valor, ast.Name) and valor.id == 'subprocess':
        return True
    return False


def _tiene_timeout(nodo):
    """Devuelve True si la llamada lleva un keyword llamado timeout."""
    for kw in nodo.keywords:
        if kw.arg == 'timeout':
            return True
    return False


def test_toda_llamada_a_subprocess_run_del_capataz_lleva_tope():
    """Toda llamada a subprocess.run en cuerpo/capataz.py tiene que llevar timeout.

    No corre nada: solo lee el texto y lo analiza con ast. Si alguna llamada
    sale sin tope, falla nombrando TODAS las lineas culpables.
    """
    with open(RUTA_CAPATAZ, 'r', encoding='utf-8') as f:
        texto = f.read()
    arbol = ast.parse(texto, filename=RUTA_CAPATAZ)
    sin_tope = []
    for nodo in ast.walk(arbol):
        if _es_subprocess_run(nodo) and not _tiene_timeout(nodo):
            sin_tope.append(nodo.lineno)
    sin_tope.sort()
    assert not sin_tope, (
        'Hay llamadas a subprocess.run en cuerpo/capataz.py SIN tope de tiempo '
        '(sin keyword timeout). Lineas culpables: ' + ', '.join(str(n) for n in sin_tope)
    )


def _cargar_capataz():
    """Carga cuerpo/capataz.py como modulo, anadiendo la raiz del repo a sys.path."""
    if RAIZ not in sys.path:
        sys.path.insert(0, RAIZ)
    spec = importlib.util.spec_from_file_location('capataz_bajo_prueba', RUTA_CAPATAZ)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_si_una_orden_del_sistema_se_cuelga_se_devuelve_fallo_y_no_se_rompe(monkeypatch):
    """Si una orden del sistema se cuelga, se cuenta como fallo y no revienta al capataz.

    Se pone un doble de subprocess.run que siempre lanza TimeoutExpired. Se llama
    a correr_orden_del_sistema con una lista de palabras cualquiera y se comprueba
    que NO se propaga la excepcion y que devuelve un numero distinto de cero.
    """
    modulo = _cargar_capataz()

    def run_que_se_cuelga(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=['orden', 'de', 'mentira'], timeout=1)

    monkeypatch.setattr(modulo.subprocess, 'run', run_que_se_cuelga)

    resultado = modulo.correr_orden_del_sistema(['orden', 'de', 'mentira'])
    assert isinstance(resultado, int), (
        'correr_orden_del_sistema tiene que devolver un numero entero, devolvio: '
        + repr(resultado)
    )
    assert resultado != 0, (
        'Un proceso colgado tiene que contarse como fallo (numero distinto de cero), '
        'pero correr_orden_del_sistema devolvio: ' + repr(resultado)
    )
