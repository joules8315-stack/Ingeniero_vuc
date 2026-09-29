# -*- coding: utf-8 -*-
"""arnes/copia_de_la_orden.py

PIEZA NUEVA: cada orden del taller trabaja en SU PROPIA carpeta, no todas en
la misma. Nace del fallo medido el 2026-09-21: con dos tareas a la vez, las
dos comparten la misma carpeta de trabajo y el guardia de una ve el trabajo A
MEDIAS de la otra, asi que da por bueno o por malo lo que no le toca. Por eso
hoy el taller corre de a una. Esta pieza es lo que permite volver a dos.

Dos funciones publicas:

  - copia_para(orden_id, raiz, correr_uno=None)
      Devuelve un diccionario con 'ok', 'carpeta' y 'motivo'.
      La carpeta es <raiz>/memoria/copias/<orden_id limpio>, donde limpio
      quiere decir que del identificador se dejan solo letras, numeros, raya
y raya baja, y lo demas se cambia por raya baja.
      El MISMO orden_id pedido dos veces devuelve LA MISMA carpeta.
      Dos orden_id DISTINTOS devuelven carpetas DISTINTAS.
      La carpeta se crea como copia de trabajo aparte del mismo repositorio,
      con el programa de control de versiones: se le pide anadir una copia de
      trabajo desprendida en esa ruta, desde la raiz dada.
      Si el programa contesta que no pudo, ok es falso y motivo lo explica en
      palabras simples. Nunca revienta.

  - soltar_copia(copia, correr_uno=None)
      Suelta esa carpeta. Devuelve verdadero si la solto y falso si no habia
      nada que soltar. Es seguro llamarla dos veces: la segunda devuelve
      falso y no hace nada.

COMO SE SABE SI HABIA ALGO QUE SOLTAR: la pieza lleva por dentro su propia
libreta de las copias que ha entregado, con el orden_id como clave.
copia_para la apunta ahi; soltar_copia mira esa libreta: si la copia esta
apuntada, la quita, pide que se retire la copia de trabajo y devuelve
verdadero; si no esta apuntada, devuelve falso sin hacer nada. NO se decide
mirando si la carpeta existe en el disco, porque la prueba falsea el programa
y la carpeta no llega a crearse.

EL PARAMETRO correr_uno: si viene, se usa en lugar del programa de verdad,
llamandolo con los mismos argumentos. Si es None se usa subprocess.run. Es el
mismo patron que ya usa arnes/bateria_en_paralelo.py, que tiene su propio
correr_uno por la misma razon: que la prueba no lance procesos de verdad.

Reglas duras de esta pieza:
  - Solo libreria estandar: os, re, subprocess.
  - NUNCA lanza una excepcion hacia fuera: todo se captura y se cuenta.
  - Nada de leer ni escribir fuera de la raiz que se le pasa.
"""

import os
import re
import subprocess


# ---------------------------------------------------------------------------
# LIBRETA INTERNA DE COPIAS ENTREGADAS
# ---------------------------------------------------------------------------
# Clave: orden_id tal cual lo pidio quien llama.
# Valor: ruta de la carpeta de la copia de trabajo.
#
# Se usa una libreta en vez de mirar el disco porque la prueba falsea el
# programa de control de versiones y la carpeta no llega a crearse: si
# decidiramos por el disco, soltar_copia diria que no habia nada que soltar
# aunque copia_para hubiera entregado la copia.
_LIBRETA = {}


# ---------------------------------------------------------------------------
# LIMPIEZA DEL IDENTIFICADOR
# ---------------------------------------------------------------------------
def _limpiar(orden_id):
    """Deja solo letras, numeros, raya y raya baja; lo demas a raya baja.

    El MISMO orden_id produce SIEMPRE el mismo texto limpio, y dos orden_id
    distintos producen textos limpios distintos (salvo que solo se diferencien
    en caracteres que se cambian por raya baja, que es justo lo que se pide).
    """
    texto = '' if orden_id is None else str(orden_id)
    return re.sub(r'[^A-Za-z0-9_-]', '_', texto)


# ---------------------------------------------------------------------------
# PROGRAMA DE CONTROL DE VERSIONES
# ---------------------------------------------------------------------------
def _correr(palabras, raiz, correr_uno):
    """Corre el programa de control de versiones y devuelve su resultado.

    Si correr_uno viene, se usa en su lugar con los mismos argumentos. Si es
    None se usa subprocess.run. Nunca revienta: si algo falla se devuelve un
    objeto con returncode distinto de cero y el motivo en stderr.
    """
    if correr_uno is not None:
        try:
            return correr_uno(palabras, cwd=raiz, capture_output=True, text=True)
        except Exception as e:
            return _Resultado(1, '', 'no se pudo correr el programa: ' + str(e))
    try:
        return subprocess.run(
            palabras,
            cwd=raiz,
            capture_output=True,
            text=True,
        )
    except Exception as e:
        return _Resultado(1, '', 'no se pudo correr el programa: ' + str(e))


class _Resultado(object):
    """Objeto con exactamente tres atributos: returncode, stdout y stderr.

    Se usa para que quien llame no tenga que cambiar como lee el resultado:
    es lo mismo que devuelve subprocess.run.
    """

    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


# ---------------------------------------------------------------------------
# FUNCION PUBLICA: copia_para
# ---------------------------------------------------------------------------
def copia_para(orden_id, raiz, correr_uno=None):
    """Da a la orden su propia copia de trabajo y devuelve donde quedo.

    Devuelve un diccionario con tres cosas:
      - ok: verdadero o falso.
      - carpeta: la ruta de la copia de trabajo.
      - motivo: texto en palabras simples.

    El MISMO orden_id pedido dos veces devuelve LA MISMA carpeta. Dos
    orden_id DISTINTOS devuelven carpetas DISTINTAS. Nunca revienta.
    """
    limpio = _limpiar(orden_id)
    carpeta = os.path.join(str(raiz), 'memoria', 'copias', limpio)

    # Si ya la entregamos antes, devolvemos la misma carpeta sin volver a
    # pedirle nada al programa de control de versiones.
    if orden_id in _LIBRETA:
        return {
            'ok': True,
            'carpeta': _LIBRETA[orden_id],
            'motivo': 'esta orden ya tenia su copia de trabajo',
        }

    palabras = ['git', 'worktree', 'add', '--detach', carpeta]
    resultado = _correr(palabras, raiz, correr_uno)

    codigo = getattr(resultado, 'returncode', 1)
    if codigo != 0:
        error = getattr(resultado, 'stderr', '') or ''
        motivo = 'el programa de control de versiones no pudo crear la copia'
        if error:
            motivo = motivo + ': ' + str(error).strip()
        return {
            'ok': False,
            'carpeta': carpeta,
            'motivo': motivo,
        }

    _LIBRETA[orden_id] = carpeta
    return {
        'ok': True,
        'carpeta': carpeta,
        'motivo': 'copia de trabajo creada para esta orden',
    }


# ---------------------------------------------------------------------------
# FUNCION PUBLICA: soltar_copia
# ---------------------------------------------------------------------------
def soltar_copia(copia, correr_uno=None):
    """Suelta la copia de trabajo de una orden.

    Devuelve verdadero si la solto y falso si no habia nada que soltar. Es
    seguro llamarla dos veces: la segunda devuelve falso y no hace nada.

    Se decide por la libreta interna, NO por el disco: si la copia esta
    apuntada, se quita, se pide que se retire la copia de trabajo y se
    devuelve verdadero; si no esta apuntada, se devuelve falso sin hacer nada.
    """
    if isinstance(copia, dict):
        ruta_copia = copia.get('carpeta')
    else:
        ruta_copia = copia

    orden_id = None
    for clave, ruta in list(_LIBRETA.items()):
        if str(ruta) == str(ruta_copia):
            orden_id = clave
            break

    if orden_id is None:
        return False

    del _LIBRETA[orden_id]

    raiz = os.path.dirname(os.path.dirname(os.path.dirname(str(ruta_copia))))
    palabras = ['git', 'worktree', 'remove', '--force', str(ruta_copia)]
    try:
        _correr(palabras, raiz, correr_uno)
    except Exception:
        # Aunque el programa falle, la copia ya no esta apuntada: la soltamos.
        pass
    return True
