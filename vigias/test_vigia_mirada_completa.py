# vigias/test_vigia_mirada_completa.py
# -*- coding: utf-8 -*-
"""Vigía de la mirada completa (arnes/mirada_completa.py).

Comprueba que la función que junta el código de una función con el de las que
llama lo hace siguiendo el hilo real de llamadas, y que no lee de más ni de
menos. Si un día empezara a leer el módulo entero, las 17 comprobaciones de
10 vigías que dependen de esto pasarían siempre y dejarían de proteger sin que
nadie se enterara. Eso es peor que no tenerlas.
"""

import os
import sys
import inspect

# Se asegura de que la raíz del proyecto esté en el camino de importación.
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# Importa la pieza que se va a vigilar y el módulo real que se usará en las pruebas.
from arnes import mirada_completa
from cuerpo import obrero


def test_encuentra_lo_que_se_mudo_a_otra_funcion():
    """Caso real que provocó todo: el texto 'primero=auditor_ok' vive en 'auditar',
    no en 'trabajar'. La mirada debe seguirlo porque 'trabajar' llama a 'auditar'."""
    codigo = mirada_completa.codigo_de(obrero.trabajar)
    assert "primero=auditor_ok" in codigo, (
        "La mirada no encontró el texto 'primero=auditor_ok' que está en la función "
        "'auditar', a la que 'trabajar' llama. Si esto falla, la garantía se estaría "
        "dando por rota solo porque el código cambió de sitio."
    )


def test_no_lee_de_mas():
    """La función '_json_de' no llama a 'auditar', así que su código no debe contener
    el texto que está en 'auditar'. Esta es la prueba MÁS IMPORTANTE: si un día la
    mirada leyera el módulo entero, todas las vigías que dependen de esto pasarían
    siempre y dejarían de proteger."""
    codigo = mirada_completa.codigo_de(obrero._json_de)
    assert "primero=auditor_ok" not in codigo, (
        "La mirada leyó de más: el código de '_json_de' no debería contener el texto "
        "'primero=auditor_ok', porque '_json_de' no llama a 'auditar'. Si esto pasa, "
        "es que está leyendo el módulo entero, y las 17 comprobaciones que dependen "
        "de esta pieza dejarían de proteger."
    )


def test_sigue_el_hilo_de_verdad():
    """Comprueba que 'tambien_llama' lee las llamadas del árbol del código, no una
    lista escrita a mano."""
    llamadas = mirada_completa.tambien_llama(obrero.trabajar)
    assert "auditar" in llamadas, (
        "La mirada no detectó que 'trabajar' llama a 'auditar'. Debería leer las "
        "llamadas del código, no una lista fija."
    )
    assert "_prompt_obrero" in llamadas, (
        "La mirada no detectó que 'trabajar' llama a '_prompt_obrero'. Debería leer "
        "las llamadas del código, no una lista fija."
    )


def test_la_mirada_es_mas_grande_que_la_funcion_sola():
    """El código de 'trabajar' debe ser más largo que solo su fuente, porque trae
    también el de las funciones que llama. El de '_json_de' debe ser mucho más
    corto. Si los dos fueran parecidos, sería que lee el archivo entero."""
    codigo_trabajar = mirada_completa.codigo_de(obrero.trabajar)
    fuente_trabajar = inspect.getsource(obrero.trabajar)
    assert len(codigo_trabajar) > len(fuente_trabajar), (
        "El código de 'trabajar' debería ser más largo que solo su fuente, porque "
        "trae además el de las funciones que llama. Si no es así, la mirada no está "
        "siguiendo el hilo de llamadas."
    )

    codigo_json = mirada_completa.codigo_de(obrero._json_de)
    assert len(codigo_json) < len(codigo_trabajar) // 2, (
        "El código de '_json_de' debería ser mucho más corto que el de 'trabajar'. "
        "Si son parecidos, es que la mirada está leyendo el archivo entero, y las "
        "vigías que dependen de esto dejarían de proteger."
    )


def test_no_se_atasca_con_una_funcion_que_se_llama_a_si_misma():
    """Llama a 'codigo_de' con hondura=2 sobre una función real del sistema y
    comprueba que termina y devuelve texto. No debe quedarse dando vueltas para
    siempre."""
    # Se usa una función que se llama a sí misma indirectamente (por ejemplo, 'trabajar'
    # llama a 'auditar', que llama a '_preguntar_con_relevo', que podría llamar a otras).
    # Con hondura=2 debe terminar sin problemas.
    codigo = mirada_completa.codigo_de(obrero.trabajar, hondura=2)
    assert isinstance(codigo, str) and len(codigo) > 0, (
        "La mirada se atascó o devolvió algo vacío al seguir llamadas con hondura=2. "
        "No debe quedarse dando vueltas para siempre."
    )


def test_si_algo_no_se_puede_leer_no_revienta():
    """Si se le pasa algo que no es una función normal (por ejemplo, la función
    incorporada 'len'), debe devolver algo o fallar de forma controlada, pero NO
    soltar un error feo."""
    try:
        resultado = mirada_completa.codigo_de(len)
        # Si devuelve algo, está bien. Si lanza una excepción controlada, también.
        assert resultado is not None
    except Exception as e:
        # Si lanza una excepción, debe ser clara y no un error feo de Python.
        assert "NO_ENCONTRADO" in str(e) or "no se pudo leer" in str(e), (
            "La mirada soltó un error feo al intentar leer una función que no se puede "
            "leer (como 'len'). Debería devolver algo o fallar de forma controlada."
        )
