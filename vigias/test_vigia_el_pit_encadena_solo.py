"""Vigia: el pit (bucle de cuerpo/capataz.py) encadena solo las ordenes pendientes.

Que se prueba aqui, y por que:
  - Se le da al bucle una lista de mentira con TRES ordenes pendientes.
  - Nadie empuja al bucle: se le llama UNA vez y el mismo tiene que ir tomando
    las tres, correrlas y dejarlas marcadas como 'hecha'.
  - El equipo (lanzar_al_equipo) y el guardia (sabotear_la_orden) se ponen en su
    sitio con monkeypatch: NUNCA se llama a ninguna IA de verdad, ni se lanza
    ningun subproceso.
  - No se toca memoria/ORDENES.json de verdad: leer_lista y marcar_estado se
    sustituyen por una lista en memoria.

Regla del proyecto que se respeta: una comprobacion NUNCA escribe en los
archivos de memoria reales (si no, da rojos falsos cuando corren dos a la vez).
"""

import os
import sys


# --- Dejar el proyecto en el camino de importacion, sin depender del cwd ---
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import capataz  # noqa: E402


# ---------------------------------------------------------------------------
# Utilidades de la prueba
# ---------------------------------------------------------------------------

def _orden_de_mentira(orden_id, pieza):
    """Una orden pendiente con la forma minima que el bucle espera leer."""
    return {
        'id': orden_id,
        'pieza': pieza,
        'encargo': 'encargo de mentira ' + orden_id,
        'estado': 'pendiente',
        'paso_fallido': '',
        'fallos_seguidos': 0,
    }


def _montar_mundo(monkeypatch, ordenes):
    """Deja el bucle aislado: lista en memoria, equipo falso, guardia falso.

    Devuelve el registro de lo que paso, para poder afirmar sobre ello.
    """
    registro = {
        'lanzadas': [],       # ids que el bucle mando correr
        'marcadas': [],       # (id, estado) en el orden en que se marcaron
        'avisos': [],         # lo que el bucle fue diciendo
        'sabotajes': [],      # ids que pasaron por el guardia
    }

    # --- La lista de ordenes vive en memoria, no en memoria/ORDENES.json ---
    def leer_lista_falsa():
        # Se devuelve una copia para que el bucle no mute la lista original
        # por accidente y la prueba siga viendo el estado real.
        return [dict(o) for o in ordenes]

    def marcar_estado_falso(orden_id, estado, paso_fallido='', fallos_seguidos=0):
        for orden in ordenes:
            if orden.get('id') == orden_id:
                orden['estado'] = estado
                orden['paso_fallido'] = paso_fallido
                orden['fallos_seguidos'] = fallos_seguidos
                registro['marcadas'].append((orden_id, estado))
                return True
        return False

    # --- Nada de gasto: el tope del mes nunca se alcanza ---
    def se_paso_del_tope_falso():
        return False

    def gastado_del_mes_falso():
        return 0.0

    # --- El equipo es de mentira: no se lanza ningun subproceso ni IA ---
    def lanzar_al_equipo_falso(proyecto, orden, tope_segundos=900):
        orden_id = str(orden.get('id', ''))
        registro['lanzadas'].append(orden_id)
        return {
            'guardado': True,
            'codigo': 0,
            'salida': 'EQUIPO DE MENTIRA: ' + orden_id,
        }

    # --- El guardia es de mentira: deja pasar todo ---
    def sabotear_la_orden_falso(orden):
        registro['sabotajes'].append(str(orden.get('id', '')))
        return {'ok': True, 'razon': 'guardia de mentira'}

    # --- Nada de forense ni de recogidas: no hay fallos que analizar ---
    def anotar_huella_fallida_falso(orden, tipo):
        return None

    def recoger_lo_frenado_falso(orden, algo):
        return {'ok': False, 'destino': ''}

    def forense_falso(orden, resultado):
        return {'paso': 'mentira', 'motivo': 'no deberia llamarse'}

    # --- Se enchufan todas las piezas del bucle ---
    monkeypatch.setattr(capataz, 'leer_lista', leer_lista_falsa)
    monkeypatch.setattr(capataz, 'marcar_estado', marcar_estado_falso)
    monkeypatch.setattr(capataz, 'se_paso_del_tope', se_paso_del_tope_falso)
    monkeypatch.setattr(capataz, 'gastado_del_mes', gastado_del_mes_falso)
    monkeypatch.setattr(capataz, 'lanzar_al_equipo', lanzar_al_equipo_falso)
    monkeypatch.setattr(capataz, 'sabotear_la_orden', sabotear_la_orden_falso)
    monkeypatch.setattr(capataz, 'anotar_huella_fallida', anotar_huella_fallida_falso)
    monkeypatch.setattr(capataz, 'recoger_lo_frenado', recoger_lo_frenado_falso)
    monkeypatch.setattr(capataz, 'forense', forense_falso)

    # --- Y la lista que el bucle vera al pedir 'listas_para_correr' ---
    # listas_para_correr devuelve las ordenes que se pueden correr AHORA.
    # En esta prueba todas las pendientes se pueden correr, asi que se le
    # devuelven las que aun estan en 'pendiente'.
    def listas_para_correr_falso():
        return [dict(o) for o in ordenes if o.get('estado') == 'pendiente']

    monkeypatch.setattr(capataz, 'listas_para_correr', listas_para_correr_falso)

    return registro


def _aviso_que_apunta(registro):
    """Un aviso=print de mentira que guarda lo que el bucle va diciendo."""
    def aviso(texto):
        registro['avisos'].append(str(texto))
    return aviso


# ---------------------------------------------------------------------------
# La prueba
# ---------------------------------------------------------------------------

def test_el_pit_encadena_solo_tres_ordenes(monkeypatch):
    """El bucle toma tres pendientes, las corre una tras otra y las deja hechas.

    Nadie empuja al bucle: se le llama UNA vez. Si el bucle no encadenara solo,
    se quedaria en la primera vuelta y las otras dos seguirian pendientes.
    """
    ordenes = [
        _orden_de_mentira('o-1', 'pieza-uno'),
        _orden_de_mentira('o-2', 'pieza-dos'),
        _orden_de_mentira('o-3', 'pieza-tres'),
    ]
    registro = _montar_mundo(monkeypatch, ordenes)

    # UNA sola llamada. El bucle tiene que hacer el resto por su cuenta.
    resultado = capataz.bucle(
        'proyecto-de-mentira',
        en_paralelo=1,
        tope_segundos=5,
        aviso=_aviso_que_apunta(registro),
    )

    # 1) El bucle se para porque ya no queda nada que correr.
    assert resultado == 'PARADO: TODO HECHO', (
        'el bucle no termino diciendo que todo estaba hecho: ' + repr(resultado)
    )

    # 2) Las tres ordenes se corrieron, y en el orden en que estaban.
    assert registro['lanzadas'] == ['o-1', 'o-2', 'o-3'], (
        'el bucle no encadeno las tres ordenes: ' + repr(registro['lanzadas'])
    )

    # 3) Las tres quedaron marcadas como terminadas.
    estados_finales = {o['id']: o['estado'] for o in ordenes}
    assert estados_finales == {'o-1': 'hecha', 'o-2': 'hecha', 'o-3': 'hecha'}, (
        'no todas las ordenes quedaron hechas: ' + repr(estados_finales)
    )

    # 4) Cada orden paso por 'corriendo' antes de quedar 'hecha'.
    for orden_id in ('o-1', 'o-2', 'o-3'):
        assert (orden_id, 'corriendo') in registro['marcadas'], (
            'la orden ' + orden_id + ' nunca se marco como corriendo'
        )
        assert (orden_id, 'hecha') in registro['marcadas'], (
            'la orden ' + orden_id + ' nunca se marco como hecha'
        )

    # 5) El guardia vio pasar las tres: no se salto a nadie.
    assert registro['sabotajes'] == ['o-1', 'o-2', 'o-3'], (
        'el guardia no vio pasar las tres ordenes: ' + repr(registro['sabotajes'])
    )

    # 6) El bucle lo fue diciendo: tres 'HECHA'.
    hechas_avisadas = [a for a in registro['avisos'] if a.startswith('HECHA ')]
    assert len(hechas_avisadas) == 3, (
        'el bucle no aviso de las tres hechas: ' + repr(registro['avisos'])
    )


def test_el_pit_no_llama_a_ninguna_ia_de_verdad(monkeypatch):
    """El bucle corre con el equipo y el guardia de mentira, sin tocar nada real.

    Si alguien quitara el monkeypatch de lanzar_al_equipo, esta prueba lo caza:
    el equipo de mentira es el unico que puede aparecer en el registro.
    """
    ordenes = [_orden_de_mentira('solo-una', 'pieza-sola')]
    registro = _montar_mundo(monkeypatch, ordenes)

    # Se guarda el original para comprobar que NO se uso.
    original_lanzar = capataz.lanzar_al_equipo
    original_sabotear = capataz.sabotear_la_orden

    resultado = capataz.bucle(
        'proyecto-de-mentira',
        en_paralelo=1,
        tope_segundos=5,
        aviso=_aviso_que_apunta(registro),
    )

    assert resultado == 'PARADO: TODO HECHO'
    assert registro['lanzadas'] == ['solo-una']
    assert registro['sabotajes'] == ['solo-una']

    # El equipo y el guardia que corrieron NO son los de verdad.
    assert capataz.lanzar_al_equipo is not original_lanzar, (
        'el bucle uso el lanzar_al_equipo de verdad: se llamo a una IA'
    )
    assert capataz.sabotear_la_orden is not original_sabotear, (
        'el bucle uso el guardia de verdad'
    )


def test_el_pit_se_para_si_no_hay_nada_que_correr(monkeypatch):
    """Sin ordenes pendientes, el bucle no corre nada y dice que todo esta hecho."""
    ordenes = []
    registro = _montar_mundo(monkeypatch, ordenes)

    resultado = capataz.bucle(
        'proyecto-de-mentira',
        en_paralelo=1,
        tope_segundos=5,
        aviso=_aviso_que_apunta(registro),
    )

    assert resultado == 'PARADO: TODO HECHO'
    assert registro['lanzadas'] == []
    assert registro['marcadas'] == []


if __name__ == '__main__':
    # Permite correrlo a mano sin pytest, por si acaso.
    import types

    class _MonkeyPatchDeMano:
        def __init__(self):
            self._guardados = []

        def setattr(self, obj, nombre, valor):
            self._guardados.append((obj, nombre, getattr(obj, nombre)))
            setattr(obj, nombre, valor)

        def undo(self):
            for obj, nombre, valor in reversed(self._guardados):
                setattr(obj, nombre, valor)

    for prueba in (
        test_el_pit_encadena_solo_tres_ordenes,
        test_el_pit_no_llama_a_ninguna_ia_de_verdad,
        test_el_pit_se_para_si_no_hay_nada_que_correr,
    ):
        mp = _MonkeyPatchDeMano()
        try:
            prueba(mp)
            print('OK ' + prueba.__name__)
        finally:
            mp.undo()
