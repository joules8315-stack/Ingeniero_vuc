# -*- coding: utf-8 -*-
"""
EL PORTERO DE LA ENTRADA.

Este programa decide, con reglas fijas y SIN llamar a ningun cerebro de pago ni gratis,
que hacer con una tarea que llega. No piensa: aplica un orden de comprobaciones y
devuelve un veredicto. Todo lo que no puede saber con seguridad lo dice con la palabra
NO_ENCONTRADO, y jamas bloquea el trabajo por adivinar.

Las decisiones posibles son:
- no_se_sabe: no hay informacion suficiente para decidir. Nunca bloquea.
- ya_tiene_dueno: esa tarea exacta ya esta asignada a alguien.
- ya_curado: la pieza que toca la tarea ya tiene un fallo curado por un vigia que existe.
- cuenta: la tarea ya trae el texto decidido, asi que la hace un programa, no un cerebro.
- juicio: no aplica ninguna regla anterior, hace falta que un cerebro la mire.
"""

NO_ENCONTRADO = 'NO_ENCONTRADO'

import json
import os
import sys

# Para REUSAR arnes/reparto.py (la fuente unica de la verdad del reparto) en vez de leer
# el JSON a mano. Este modulo ya sabe donde esta la raiz y como leer el archivo.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import arnes.reparto as _rep

# Ruta de la memoria de fallos, como constante de modulo para que una vigia pueda
# desviarla a un archivo temporal y probar sin tocar la memoria real de Julio.
FALLOS_RUTA = os.path.join(_rep.AQUI, 'memoria', 'FALLOS.json')


def _leer_json(ruta):
    """Lee un archivo JSON del disco.

    Devuelve (ok, contenido). Si el archivo no existe o no se puede leer,
    ok es False. Nunca convertimos un error de lectura en 'no pasa nada'.
    """
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
        return True, contenido
    except FileNotFoundError:
        return False, NO_ENCONTRADO
    except Exception:
        return False, NO_ENCONTRADO


def _normalizar(texto):
    """Quita espacios al principio y al final, y pasa a minusculas."""
    return str(texto or '').strip().lower()


def _existe_en_disco(ruta):
    """Comprueba si un archivo o carpeta existe en el disco."""
    return os.path.exists(ruta)


def decidir(proyecto, tarea):
    """Decide que hacer con una tarea, siguiendo el orden del contrato.

    Devuelve un diccionario con la decision, quien la tiene (si aplica),
    el estado (si aplica), las piezas (si aplica) y el motivo en palabras simples.
    """
    # --- PASO 1: Comprobar que el reparto existe ---
    if not os.path.exists(_rep.RUTA):
        return {
            'decision': 'no_se_sabe',
            'motivo': 'no se pudo leer el reparto. NO BLOQUEAR.',
            'quien_la_tiene': NO_ENCONTRADO,
            'estado': NO_ENCONTRADO,
            'piezas': NO_ENCONTRADO
        }

    # --- PASO 2: Preguntar al reparto si la tarea exacta ya tiene dueno ---
    _quien, _estado = _rep.dueno(tarea)
    if _quien:
        return {
            'decision': 'ya_tiene_dueno',
            'quien_la_tiene': _quien,
            'estado': _estado,
            'piezas': NO_ENCONTRADO,
            'motivo': 'esa tarea exacta ya la tiene alguien y no se puede pisar.'
        }

    # --- PASO 3: Leer la memoria de fallos ---
    ok_fallos, fallos = _leer_json(FALLOS_RUTA)
    if not ok_fallos:
        return {
            'decision': 'no_se_sabe',
            'motivo': 'no se pudo leer la memoria de fallos. NO BLOQUEAR.',
            'quien_la_tiene': NO_ENCONTRADO,
            'estado': NO_ENCONTRADO,
            'piezas': NO_ENCONTRADO
        }

    # --- PASO 4: Buscar si la tarea toca una pieza con un fallo curado ---
    # La tarea puede venir con una lista de piezas. Si no, no podemos saber que piezas toca.
    piezas_tarea = []
    if isinstance(tarea, dict):
        piezas_tarea = tarea.get('piezas', [])
    elif isinstance(tarea, str):
        # Si la tarea es solo texto, no sabemos que piezas toca.
        piezas_tarea = []

    if isinstance(fallos, list) and piezas_tarea:
        for fallo in fallos:
            if not isinstance(fallo, dict):
                continue
            piezas_fallo = fallo.get('piezas', [])
            quien_caza = str(fallo.get('quien_lo_caza') or '').strip()
            if quien_caza and _existe_en_disco(quien_caza):
                # Comprobamos si alguna pieza de la tarea coincide con alguna del fallo
                for pieza_tarea in piezas_tarea:
                    if pieza_tarea in piezas_fallo:
                        return {
                            'decision': 'ya_curado',
                            'quien_la_tiene': NO_ENCONTRADO,
                            'estado': NO_ENCONTRADO,
                            'piezas': piezas_fallo,
                            'motivo': 'esa pieza ya tiene un fallo curado por un vigia que existe.'
                        }

    # --- PASO 5: Comprobar si la tarea ya trae el texto decidido ---
    # Si la tarea es un diccionario y contiene TEXTO_VIEJO y TEXTO_NUEVO con valores validos,
    # entonces es una cuenta: la hace un programa, no un cerebro.
    if isinstance(tarea, dict):
        texto_viejo = str(tarea.get('TEXTO_VIEJO') or '').strip()
        texto_nuevo = str(tarea.get('TEXTO_NUEVO') or '').strip()
        if texto_viejo and texto_nuevo:
            if texto_viejo not in (NO_ENCONTRADO, 'si', 'no') and texto_nuevo not in (NO_ENCONTRADO, 'si', 'no'):
                return {
                    'decision': 'cuenta',
                    'quien_la_tiene': NO_ENCONTRADO,
                    'estado': NO_ENCONTRADO,
                    'piezas': NO_ENCONTRADO,
                    'motivo': 'la tarea ya trae el texto decidido, la hace un programa con reglas fijas.'
                }

    # --- PASO 6: Si nada aplica, es un juicio ---
    return {
        'decision': 'juicio',
        'quien_la_tiene': NO_ENCONTRADO,
        'estado': NO_ENCONTRADO,
        'piezas': NO_ENCONTRADO,
        'motivo': 'no aplica ninguna regla anterior, hace falta que un cerebro la mire.'
    }
