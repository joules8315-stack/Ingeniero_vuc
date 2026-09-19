import os
import sys
import types

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, 'arnes'))

import guardia_de_guardado
import vecinas


def _falso_run(comandos_vistos, stdout_pytest):
    """Devuelve una funcion que imita a subprocess.run.

    Si el comando trae 'pytest', devuelve returncode 1 y el stdout que se le pase.
    Si el comando trae 'ls-files', apunta el ultimo elemento del comando y devuelve
    returncode 0 solo si ese elemento es exactamente 'vigias/test_viejo.py'.
    """
    def _run(cmd, *args, **kwargs):
        cmd = list(cmd)
        if 'pytest' in cmd:
            return types.SimpleNamespace(returncode=1, stdout=stdout_pytest, stderr='')
        if 'ls-files' in cmd:
            comandos_vistos.append(cmd[-1])
            if cmd[-1] == 'vigias/test_viejo.py':
                return types.SimpleNamespace(returncode=0, stdout='vigias/test_viejo.py\n', stderr='')
            return types.SimpleNamespace(returncode=1, stdout='', stderr='')
        return types.SimpleNamespace(returncode=0, stdout='', stderr='')
    return _run


def test_vigia_vieja_que_no_carga_frena(tmp_path, monkeypatch):
    """Una vigia vieja que ni carga (ERROR NameError) tiene que hacer frenar al guardia."""
    (tmp_path / 'vigias').mkdir()
    monkeypatch.setattr(vecinas, 'elegir', lambda raiz: None)
    comandos_vistos = []
    stdout = ("ERROR vigias/test_viejo.py - NameError: name 'contextlib' is not defined\n"
              "1 error in 0.10s")
    monkeypatch.setattr(guardia_de_guardado.subprocess, 'run',
                        _falso_run(comandos_vistos, stdout))

    paso, mensaje = guardia_de_guardado._vigias(str(tmp_path))

    assert paso is False, 'una vigia vieja que no carga tiene que frenar: %r' % (mensaje,)
    assert 'vigias/test_viejo.py' in comandos_vistos, \
        'a git se le tiene que preguntar por la vigia roja: %r' % (comandos_vistos,)


def test_vigia_vieja_que_falla_frena(tmp_path, monkeypatch):
    """Una vigia vieja que falla (FAILED) tambien tiene que hacer frenar al guardia."""
    (tmp_path / 'vigias').mkdir()
    monkeypatch.setattr(vecinas, 'elegir', lambda raiz: None)
    comandos_vistos = []
    stdout = 'FAILED vigias/test_viejo.py::test_algo - assert 1 == 2\n'
    monkeypatch.setattr(guardia_de_guardado.subprocess, 'run',
                        _falso_run(comandos_vistos, stdout))

    paso, mensaje = guardia_de_guardado._vigias(str(tmp_path))

    assert paso is False, 'una vigia vieja que falla tiene que frenar: %r' % (mensaje,)
    assert 'vigias/test_viejo.py' in comandos_vistos, \
        'a git se le tiene que preguntar por la vigia roja: %r' % (comandos_vistos,)
