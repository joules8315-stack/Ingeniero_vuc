"""Vigia: la IA revisora sabe lo que el revisor de PROGRAMA ya comprobo.

Orden de Julio A-38: a la IA revisora solo le queda el juicio. Si el revisor de
programa ya comprobo que los nombres existen, la IA no debe rechazar por
'no aparece en el material', porque ya no ve el archivo entero.

Nace ROJA hasta que cuerpo/obrero.py marque la propuesta con
'_comprobado_por_programa' y lo diga en el prompt de la IA revisora.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, 'arnes'))

from cuerpo import obrero
import revisor_de_programa


MARCA = 'COMPROBADO POR PROGRAMA'

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


def test_auditar_marca_la_nota(monkeypatch):
    """Con la marca puesta, el prompt que ve la IA dice COMPROBADO POR PROGRAMA."""
    prompts = []

    def falsa(prompt, *a, **k):
        prompts.append(prompt)
        return (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), 'groq', [])

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', falsa)

    obrero.auditar('paquete', {'archivo': 'x.py', '_comprobado_por_programa': True},
                   evitar='deepseek')

    assert prompts, 'auditar no llego a preguntar a ninguna IA'
    assert MARCA in prompts[0], (
        'el prompt de la IA revisora no dice que el programa ya comprobo: ' + prompts[0])


def test_auditar_sin_marca_no_la_pone(monkeypatch):
    """Sin la marca, el prompt NO debe decir COMPROBADO POR PROGRAMA."""
    prompts = []

    def falsa(prompt, *a, **k):
        prompts.append(prompt)
        return (json.dumps({'veredicto': 'APROBADO', 'fallos': []}), 'groq', [])

    monkeypatch.setattr(obrero, '_preguntar_con_relevo', falsa)

    obrero.auditar('paquete', {'archivo': 'x.py'}, evitar='deepseek')

    assert prompts, 'auditar no llego a preguntar a ninguna IA'
    assert MARCA not in prompts[0], (
        'el prompt dice que el programa comprobo cuando no lo hizo: ' + prompts[0])


def test_trabajar_pone_la_marca(monkeypatch):
    """trabajar marca la propuesta con _comprobado_por_programa antes de auditar."""
    prompts, llamadas_auditar = _preparar(monkeypatch)

    monkeypatch.setattr(revisor_de_programa, 'revisar', lambda *a, **k: [])

    obrero.trabajar('paquete', 'tarea', generador='deepseek', auditor='bigpickle')

    assert llamadas_auditar, 'trabajar no llego a llamar a auditar'
    propuesta = llamadas_auditar[0][0][1]
    assert isinstance(propuesta, dict), 'auditar no recibio la propuesta como dict'
    assert propuesta.get('_comprobado_por_programa') is True, (
        'la propuesta que recibio auditar no trae _comprobado_por_programa True: '
        + repr(propuesta))


if __name__ == '__main__':
    import inspect

    class _MP:
        def __init__(self):
            self._hechos = []

        def setattr(self, obj, nombre, valor):
            self._hechos.append((obj, nombre, getattr(obj, nombre, None)))
            setattr(obj, nombre, valor)

        def undo(self):
            for obj, nombre, viejo in reversed(self._hechos):
                setattr(obj, nombre, viejo)
            self._hechos = []

    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if not nombre.startswith('test_') or not callable(fn):
            continue
        mp = _MP()
        try:
            if 'monkeypatch' in inspect.signature(fn).parameters:
                fn(mp)
            else:
                fn()
            print('  VERDE  ' + nombre)
        except Exception as e:
            fallos += 1
            print('  ROJA   ' + nombre + ': ' + repr(e))
        finally:
            mp.undo()
    raise SystemExit(1 if fallos else 0)
