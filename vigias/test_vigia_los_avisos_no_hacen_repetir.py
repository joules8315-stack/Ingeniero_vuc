"""Vigia: los avisos de fallos ya dados no hacen repetir la accion (Julio A-38).

Comprueba tres cosas:
  1. Con los fallos REALES, los comandos normales no disparan ningun aviso.
  2. 'git commit --no-verify' SI dispara el aviso.
  3. sin_ruido conserva lo que es codigo y quita los docstrings sueltos.
  4. Por leccion: la primera vez frena (2), la segunda deja pasar (0);
     una leccion nueva vuelve a frenar una vez y luego deja pasar.
"""
import io
import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, 'arnes'))

import candado_memoria
import revisor_de_programa


COMANDOS_NORMALES = [
    'python ingeniero.py equipo ingeniero "En cuerpo/obrero.py el revisor auditor '
    'SIN_AUDITAR vigia" --escribe deepseek --revisa groq',
    'python -m pytest vigias/test_x.py -q',
    'git status --short',
    'git log --oneline -3',
    'grep -n auditar cuerpo/obrero.py',
]


def test_comandos_normales_no_disparan_avisos():
    """Con los fallos reales, ningun comando normal debe hacer saltar revisar."""
    for comando in COMANDOS_NORMALES:
        fallos = candado_memoria.revisar(comando)
        if fallos:
            ids = [str(f.get('id', '?')) for f in fallos]
            pytest.fail(
                'el comando normal %r disparo el aviso de los fallos %s'
                % (comando, ids)
            )


def test_commit_no_verify_si_dispara():
    """'git commit --no-verify' SI tiene que hacer saltar revisar."""
    fallos = candado_memoria.revisar('git commit --no-verify -m x')
    assert fallos, 'git commit --no-verify deberia disparar al menos un fallo'


def test_sin_ruido_conserva_cadena_valor():
    """sin_ruido no debe comerse una cadena que es un valor de verdad."""
    resultado = revisor_de_programa.sin_ruido("x = r'''git\s+commit'''")
    assert 'git' in resultado


def test_sin_ruido_quita_docstring_suelto():
    """sin_ruido debe quitar un docstring suelto dentro de una funcion."""
    resultado = revisor_de_programa.sin_ruido('def f():\n    """hola"""\n    return 1')
    assert 'hola' not in resultado


def _fallo(id_fallo):
    """Un fallo de mentira con las llaves que main necesita."""
    return {
        'id': id_fallo,
        'que_paso': 'paso %s' % id_fallo,
        'causa_raiz': 'causa %s' % id_fallo,
        'cura': 'cura %s' % id_fallo,
        'no_volver_a': 'no volver a %s' % id_fallo,
    }


def _accion():
    """El json de la accion que main lee por stdin."""
    return json.dumps({'tool_name': 'Bash', 'tool_input': {'command': 'x'}})


def test_por_leccion_avisa_una_vez_y_luego_deja_pasar(monkeypatch, tmp_path):
    """La primera vez frena; la segunda, con la misma leccion, deja pasar."""
    import autorizacion

    monkeypatch.setattr(candado_memoria, 'AVISADOS', str(tmp_path / 'avisos.json'))
    monkeypatch.setattr(autorizacion, 'autorizada', lambda: False)

    A = _fallo('A')
    B = _fallo('B')
    cola = [[A], [A], [A, B], [A, B], [A]]

    def revisar_falso(texto):
        return cola.pop(0)

    monkeypatch.setattr(candado_memoria, 'revisar', revisar_falso)

    def correr():
        monkeypatch.setattr(sys, 'stdin', io.StringIO(_accion()))
        return candado_memoria.main()

    assert correr() == 2, 'con [A] la primera vez debe frenar (2)'
    assert correr() == 0, 'con [A] la segunda vez debe dejar pasar (0)'
    assert correr() == 2, 'con [A, B] debe frenar porque B es nueva (2)'
    assert correr() == 0, 'con [A, B] otra vez debe dejar pasar (0)'
    assert correr() == 0, 'con [A] despues debe dejar pasar (0)'
