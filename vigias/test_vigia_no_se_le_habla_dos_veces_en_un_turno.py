#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vigias/test_vigia_no_se_le_habla_dos_veces_en_un_turno.py — NO SE LE HABLA DOS VECES A JULIO EN UN TURNO.

Fallo del 2026-09-25, confirmado por Julio el mismo dia: en un mismo turno recibe DOS
mensajes escritos, porque tras el primero un candado obliga a guardar y despues se le
escribe otro. El candado arnes/candado_no_repetir.py de hoy solo compara frases repetidas
y no cuenta cuantos mensajes se le escribieron en el turno, asi que no lo ve.

Esta prueba comprueba la funcion nueva mensajes_de_este_turno, que todavia no existe en
arnes/candado_no_repetir.py. Nace ROJA porque esa funcion no existe todavia, y asi tiene
que nacer.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from arnes import candado_no_repetir


def _escribir_jsonl(ruta, renglones):
    with open(ruta, "w", encoding="utf-8") as f:
        for r in renglones:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_dos_mensajes_del_asistente_despues_del_ultimo_user(tmp_path):
    # Fallo del 2026-09-25, confirmado por Julio el mismo dia.
    ruta = tmp_path / "conversacion.jsonl"
    _escribir_jsonl(ruta, [
        {"type": "user", "text": "Julio pregunta algo"},
        {"type": "assistant", "text": "Primer mensaje escrito"},
        {"type": "assistant", "text": "Segundo mensaje escrito"},
    ])
    assert candado_no_repetir.mensajes_de_este_turno(str(ruta)) == 2


def test_un_mensaje_del_asistente_despues_del_ultimo_user(tmp_path):
    # Fallo del 2026-09-25, confirmado por Julio el mismo dia.
    ruta = tmp_path / "conversacion.jsonl"
    _escribir_jsonl(ruta, [
        {"type": "user", "text": "Julio pregunta algo"},
        {"type": "assistant", "text": "Un solo mensaje escrito"},
    ])
    assert candado_no_repetir.mensajes_de_este_turno(str(ruta)) == 1
