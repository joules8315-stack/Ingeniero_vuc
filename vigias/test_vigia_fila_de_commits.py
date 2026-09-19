# -*- coding: utf-8 -*-
"""vigias/test_vigia_fila_de_commits.py — Vigia de la fila de guardado en git.

Prueba que fila_de_commits deja entrar a uno y frena al otro, que suelta el candado
al salir (aunque salga con error) y que un candado abandonado (mas de 2 horas) se
pisa. Tambien prueba que guardar_en_la_historia guarda DENTRO de la fila.
"""
import glob
import os
import subprocess
import sys
import tempfile
import time
import types

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, 'arnes'))
import candado_equipo  # noqa: E402


def _lock_de(raiz):
    """Devuelve la ruta del candado de esa raiz (mismo calculo que fila_de_commits)."""
    import hashlib
    clave = hashlib.sha1(os.path.abspath(str(raiz)).lower().encode('utf-8')).hexdigest()[:12]
    return os.path.join(tempfile.gettempdir(), 'ingeniero_fila_' + clave + '.lock')


def test_uno_entra_y_el_otro_espera(tmp_path):
    """Con la fila tomada, el segundo con espera=1 se rinde con TimeoutError."""
    raiz = str(tmp_path)
    with candado_equipo.fila_de_commits(raiz):
        with pytest.raises(TimeoutError):
            with candado_equipo.fila_de_commits(raiz, espera=1):
                pass


def test_al_salir_se_puede_volver_a_entrar(tmp_path):
    """Al salir del with, la fila queda libre y se puede volver a entrar."""
    raiz = str(tmp_path)
    with candado_equipo.fila_de_commits(raiz):
        pass
    with candado_equipo.fila_de_commits(raiz, espera=1):
        pass


def test_si_dentro_falla_el_candado_se_libera(tmp_path):
    """Si dentro del with salta un ValueError, al salir la fila queda libre."""
    raiz = str(tmp_path)
    with pytest.raises(ValueError):
        with candado_equipo.fila_de_commits(raiz):
            raise ValueError('fallo dentro de la fila')
    with candado_equipo.fila_de_commits(raiz, espera=1):
        pass


def test_candado_abandonado_se_pisa(tmp_path):
    """Un candado con mas de 2 horas de antiguedad no bloquea: se pisa y se entra."""
    raiz = str(tmp_path)
    patron = os.path.join(tempfile.gettempdir(), 'ingeniero_fila_*.lock')
    antes = set(glob.glob(patron))
    with candado_equipo.fila_de_commits(raiz):
        nuevos = set(glob.glob(patron)) - antes
        assert len(nuevos) == 1, 'deberia aparecer un unico candado nuevo'
        ruta = nuevos.pop()
    # Se crea a mano el mismo candado y se envejece 3 horas.
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('999999')
    viejo = time.time() - 3 * 3600
    os.utime(ruta, (viejo, viejo))
    with candado_equipo.fila_de_commits(raiz, espera=1):
        pass


def test_guardar_en_la_historia_guarda_dentro_de_la_fila(tmp_path, monkeypatch):
    """guardar_en_la_historia corre git DENTRO de la fila: el 'add' no puede entrar."""
    raiz = str(tmp_path)
    intento = {'timeout': False, 'visto': False}

    def falsa(cmd, *args, **kwargs):
        if 'add' in cmd:
            intento['visto'] = True
            try:
                with candado_equipo.fila_de_commits(raiz, espera=0.2):
                    pass
            except TimeoutError:
                intento['timeout'] = True
        return types.SimpleNamespace(returncode=0, stdout='', stderr='')

    monkeypatch.setattr(subprocess, 'run', falsa)
    ok, motivo = candado_equipo.guardar_en_la_historia(raiz, ['a.py'], 'msg')
    assert ok is True, motivo
    assert intento['visto'] is True, 'no se llego a llamar a git add'
    assert intento['timeout'] is True, 'la fila no estaba tomada durante el guardado'
