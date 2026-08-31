# -*- coding: utf-8 -*-
"""VIGIA — el guardián NO cuenta sus propios cuadernos (encargo de Claude a Cline, 2026-08-31).

PROBLEMA medido: los candados escriben en sus cuadernos (memoria/GUARDIA.log,
memoria/CANDADOS_MEDICION.json, memoria/.commit_bloqueos y demas) CADA VEZ que actuan. El guardián
que mira si hay trabajo sin guardar ve esos cuadernos recien tocados por el mismo, y grita "hay
trabajo sin guardar". Es un bucle por diseno: nunca puede quedar limpio porque se ensucia solo al
comprobar. Eso es lo que Julio siente como "me pide permiso a cada rato".

LO QUE HAY QUE CONSEGUIR: que al mirar si hay trabajo sin guardar, el guardián NO cuente los
cuadernos de los propios candados. Solo el trabajo de verdad (codigo, leyes, vigias, paquetes).
NO vale apagar el guardián ni aflojarlo: si hay codigo sin guardar, tiene que seguir gritando.

NACE ROJA: hoy el guardián ignora TODO memoria/ (memoria/paquetes/ incluido), asi que deja
pasar sin avisar trabajo real indexado. La vigia 3 lo pilla.

No llama a ningun cerebro: se le da de comer a _cambios_sin_commit un git de mentira. Determinista.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import candado_commit as cc  # noqa: E402


def _correr_con(salida, monkeypatch):
    """Corre _cambios_sin_commit() con un git de mentira que devuelve `salida`."""
    class _R:
        returncode = 0
        stdout = salida
        stderr = ""
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _R())
    return cc._cambios_sin_commit()


def test_los_cuadernos_de_los_candados_NO_gritan(monkeypatch):
    """Los cuadernos que escriben los propios candados NO son trabajo sin guardar."""
    salida = (" M memoria/GUARDIA.log\n"
              " M memoria/CANDADOS_MEDICION.json\n"
              " M memoria/.commit_bloqueos\n")
    assert _correr_con(salida, monkeypatch) is False, (
        "los cuadernos de los candados hicieron gritar al guardián. Es un bucle: el candado se "
        "ensucia solo al comprobar. Eso es lo que Julio ve como 'me pide permiso a cada rato'.")


def test_un_archivo_de_codigo_modificado_SI_grita(monkeypatch):
    """NO se afloja: codigo real sin guardar tiene que seguir gritando igual de fuerte."""
    salida = " M cuerpo/obrero.py\n"
    assert _correr_con(salida, monkeypatch) is True, (
        "hay codigo real sin guardar y el guardián no grita: se aflojo el candado, y eso esta "
        "prohibido. Solo los cuadernos propios deben ignorarse.")


def test_el_trabajo_real_en_memoria_SI_grita(monkeypatch):
    """Ignorar 'todo memoria/' es demasiado amplio: los paquetes indexados son trabajo de verdad."""
    salida = " M memoria/paquetes/foto_informe__algo.md\n"
    assert _correr_con(salida, monkeypatch) is True, (
        "el guardián ignora TODO memoria/, pero memoria/paquetes/ es trabajo real indexado (lo que "
        "se le manda al equipo). Un paquete nuevo sin guardar no se puede dejar pasar en silencio. "
        "Hay que ignorar SOLO los cuadernos de los candados, no el trabajo de verdad.")
