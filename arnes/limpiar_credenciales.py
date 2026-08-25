# -*- coding: utf-8 -*-
"""arnes/limpiar_credenciales.py — F8 (puntos k, l): las claves se usan el tiempo necesario y
siempre se BORRAN al final de cada sección.

Julio, 2026-08-24 (punto l): "que nunca se pidan las credenciales en chat, que no sean públicas,
que se usen por el tiempo necesario, y siempre, al final de cada sección, se borren."

Las claves de prueba/credenciales viven en las variables de entorno (protegidas, nunca en chat ni en
archivo). Esta función las BORRA del entorno cuando la sección termina, para que no queden dando
vueltas. `candado_prueba_real` y las pruebas la llaman al final.
"""
import os

_MARCAS = ("_KEY", "_TOKEN", "_SECRET", "_PASSWORD", "_CLAVE", "_REFRESH", "CREDENTIAL")


def limpiar(excluir=("") ):
    """Borra del entorno las claves que parecen credenciales. Devuelve las que borró.

    `excluir`: prefijos que NO se tocan (p. ej. variables de sistema que no son de prueba).
    """
    excluir = tuple(str(e).upper() for e in (excluir or ()))
    borradas = []
    for k in list(os.environ):
        up = k.upper()
        if excluir and up.startswith(excluir):
            continue
        if any(m in up for m in _MARCAS):
            os.environ.pop(k, None)
            borradas.append(k)
    return borradas


def hay_credenciales():
    """¿Queda alguna clave con pinta de credencial en el entorno?"""
    for k in os.environ:
        up = k.upper()
        if any(m in up for m in _MARCAS):
            return True
    return False


if __name__ == "__main__":
    import sys
    b = limpiar()
    sys.stdout.write("credentiales limpiadas: %d\n" % len(b))
    sys.exit(0)
