# arnes/mirada_completa.py
# -*- coding: utf-8 -*-
"""Mirada completa: junta el codigo de una funcion y el de las que llama.

Nace por una roja falsa: hoy 2026-09-07 se movio la logica de una funcion a otra,
pero la vigia que buscaba el texto en el sitio viejo se puso roja, aunque el
comportamiento no cambio. Hay 17 comprobaciones atadas a un sitio, y eso es un
candado que salta con el trabajo bueno. Este programa junta el codigo siguiendo
las LLAMADAS, no el sitio, para que la vigia mire el flujo entero.

Es una cuenta pura: lee codigo y sigue nombres. No ejecuta nada, no toca la red,
no decide nada.
"""

import ast
import inspect


def _mismo_modulo(funcion):
    """Devuelve el modulo al que pertenece la funcion, o None si no se puede."""
    try:
        return inspect.getmodule(funcion)
    except Exception:
        return None


def _es_funcion_del_modulo(modulo, nombre):
    """Devuelve True si 'nombre' existe en 'modulo' y es una funcion."""
    if modulo is None:
        return False
    try:
        return inspect.isfunction(getattr(modulo, nombre))
    except Exception:
        return False


def _nombres_llamados(funcion):
    """Devuelve la lista de nombres de funciones a las que llama 'funcion'.

    Usa el arbol de codigo (ast), que es exacto, no busqueda de texto.
    De una llamada 'algo.otra_cosa()' toma 'otra_cosa'.
    """
    try:
        codigo_fuente = inspect.getsource(funcion)
        arbol = ast.parse(codigo_fuente)
    except Exception:
        return []

    nombres = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Call):
            if isinstance(nodo.func, ast.Name):
                nombres.append(nodo.func.id)
            elif isinstance(nodo.func, ast.Attribute):
                nombres.append(nodo.func.attr)
    return nombres


def tambien_llama(funcion):
    """Devuelve la lista de nombres de funciones del mismo modulo a las que llama."""
    modulo = _mismo_modulo(funcion)
    return [n for n in _nombres_llamados(funcion) if _es_funcion_del_modulo(modulo, n)]


def codigo_de(funcion, hondura=1):
    """Devuelve el codigo de 'funcion' y el de las funciones que llama.

    - hondura=1: junta el codigo de 'funcion' y el de las que llama directamente.
    - hondura=2: ademas junta el de las que llaman esas.
    Cada trozo va separado por un comentario que dice de que funcion es.
    Nunca se sigue dos veces a la misma funcion.
    Si algo falla al leer una funcion, se salta y se sigue.
    """
    modulo = _mismo_modulo(funcion)
    if modulo is None:
        return NO_ENCONTRADO

    vistos = set()
    texto_final = []

    def _juntar(func, profundidad):
        if func in vistos or profundidad < 0:
            return
        vistos.add(func)
        try:
            texto_final.append("# --- codigo de: %s ---" % func.__name__)
            texto_final.append(inspect.getsource(func))
        except Exception:
            # Si no se puede leer, se salta y se sigue.
            return

        if profundidad > 0:
            for nombre in _nombres_llamados(func):
                if _es_funcion_del_modulo(modulo, nombre):
                    _juntar(getattr(modulo, nombre), profundidad - 1)

    _juntar(funcion, hondura)
    return "\n".join(texto_final)


if __name__ == "__main__":
    # Prueba a mano: escribe el nombre de una funcion y su modulo.
    # Por ejemplo: python arnes/mirada_completa.py cuerpo.obrero.trabajar
    import sys
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        try:
            partes = ruta.split(".")
            modulo_nombre = ".".join(partes[:-1])
            funcion_nombre = partes[-1]
            modulo = __import__(modulo_nombre, fromlist=[funcion_nombre])
            funcion = getattr(modulo, funcion_nombre)
            print(codigo_de(funcion))
        except Exception as e:
            print("No se pudo probar: %s" % e)
    else:
        print("Pasa el nombre de una funcion, por ejemplo: cuerpo.obrero.trabajar")
