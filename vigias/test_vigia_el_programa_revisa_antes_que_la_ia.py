"""Vigia: el revisor de PROGRAMA (gratis) revisa la propuesta del obrero ANTES de pagar
la revision de una IA. Si encuentra fallos, no se llama a la IA revisora y el obrero
recibe esos motivos en la vuelta siguiente.

Orden de Julio A-38 punto 2, tarea E-3. Nace ROJA hasta que cuerpo/obrero.py y
revisor_de_programa.py hagan lo que dice la orden.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, 'arnes'))

from cuerpo import obrero
import revisor_de_programa


PROPUESTA_OK = json.dumps({'archivo': 'x.py', 'texto_viejo': 'a', 'texto_nuevo': 'b'})


def _preparar(monkeypatch):
    """Deja el obrero con sus tripas falsas y devuelve los contadores y los prompts."""
    monkeypatch.setattr(obrero, '_propuesta_cumple', lambda p, c: (True, ''))
    monkeypatch.setattr(obrero, '_validar_en_paquete', lambda *a, **k: [])
    monkeypatch.setattr(obrero, '_filtrar_paquete', lambda paquete, **k: 'material')

    prompts = []

    def falsa_obrero(prompt, *a, **k):
        prompts.append(prompt)
        return (PROPUESTA_OK, 'deepseek', [])

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', falsa_obrero)

    llamadas_auditar = []

    def aud(*a, **k):
        llamadas_auditar.append((a, k))
        return ({'veredicto': 'APROBADO'}, 'groq', [])

    monkeypatch.setattr(obrero, 'auditar', aud)
    return prompts, llamadas_auditar


def test_fallos_de_programa_no_pagan_ia_y_vuelven_al_obrero(monkeypatch):
    """Si el revisor de programa encuentra fallos, no se llama a la IA y el obrero
    recibe esos motivos en la vuelta siguiente."""
    prompts, llamadas_auditar = _preparar(monkeypatch)

    veces = {'n': 0}

    def r(*a, **k):
        veces['n'] += 1
        if veces['n'] == 1:
            return ['FALLO DE PROGRAMA X']
        return []

    monkeypatch.setattr(revisor_de_programa, 'revisar', r)

    obrero.trabajar('paquete', 'tarea de prueba', generador='deepseek', auditor='bigpickle')

    assert len(llamadas_auditar) == 1, (
        'la IA revisora se llamo ' + str(len(llamadas_auditar)) + ' veces, se esperaba 1'
    )
    assert len(prompts) >= 2, (
        'el obrero solo fue preguntado ' + str(len(prompts)) + ' veces, se esperaba al menos 2'
    )
    assert 'FALLO DE PROGRAMA X' in prompts[1], (
        'el segundo prompt del obrero no lleva los motivos del revisor de programa: '
        + repr(prompts[1])
    )


def test_sin_fallos_de_programa_una_ia_y_un_obrero(monkeypatch):
    """Si el revisor de programa no encuentra fallos, la IA revisa una vez y el obrero
    solo trabaja una vez."""
    prompts, llamadas_auditar = _preparar(monkeypatch)

    monkeypatch.setattr(revisor_de_programa, 'revisar', lambda *a, **k: [])

    obrero.trabajar('paquete', 'tarea de prueba', generador='deepseek', auditor='bigpickle')

    assert len(llamadas_auditar) == 1, (
        'la IA revisora se llamo ' + str(len(llamadas_auditar)) + ' veces, se esperaba 1'
    )
    assert len(prompts) == 1, (
        'el obrero fue preguntado ' + str(len(prompts)) + ' veces, se esperaba 1'
    )


def test_si_el_revisor_de_programa_revienta_la_ia_sigue(monkeypatch):
    """Si el revisor de programa lanza una excepcion, la IA revisora se llama igual:
    el programa nunca bloquea por romperse."""
    prompts, llamadas_auditar = _preparar(monkeypatch)

    def r(*a, **k):
        raise RuntimeError('el revisor de programa se rompio')

    monkeypatch.setattr(revisor_de_programa, 'revisar', r)

    obrero.trabajar('paquete', 'tarea de prueba', generador='deepseek', auditor='bigpickle')

    assert len(llamadas_auditar) == 1, (
        'la IA revisora se llamo ' + str(len(llamadas_auditar)) + ' veces, se esperaba 1'
    )


if __name__ == '__main__':
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith('test_') and callable(_f):
            try:
                _f()
                print('  VERDE  ' + _n)
            except Exception as e:
                fails += 1
                print('  ROJA   ' + _n + ': ' + repr(e))
    raise SystemExit(1 if fails else 0)
