# -*- coding: utf-8 -*-
"""VIGIA — apagar los candados solo puede Julio, por comando y con autorizacion escrita.

Ley (Julio, 2026-08-24): "que solo pueda quitarlos yo, por medio de comando, en ps, y debe ser
con previa autorizacion."

Antes bastaba con prender una variable y los candados se apagaban EN SILENCIO: cualquiera podia,
y no quedaba rastro. Ahora el unico camino es un comando que deja una autorizacion escrita, con
fecha, y que caduca.

DOS COSAS A LA VEZ, y las dos importan:
  1. Sin autorizacion, prender la variable NO abre nada.
  2. CON autorizacion, abre de verdad. Un candado sin salida no es un candado, es un muro, y
     acaba con Julio apagandolo todo, que es peor que el problema.
"""
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import autorizacion  # noqa: E402


def _apuntar_a(tmp_path, monkeypatch):
    """La autorizacion de mentira vive aparte: NUNCA se toca la de verdad de Julio."""
    falsa = str(tmp_path / ".autorizacion_de_mentira")
    monkeypatch.setenv("INGENIERO_AUTORIZACION_TEST", falsa)
    return falsa


def test_sin_autorizacion_no_se_apaga_nada(tmp_path, monkeypatch):
    _apuntar_a(tmp_path, monkeypatch)
    assert not autorizacion.autorizada(), (
        "sin la autorizacion escrita de Julio los candados se apagarian igual: entonces "
        "cualquiera puede apagarlos y no queda rastro")


def test_con_la_autorizacion_de_julio_SI_se_apaga(tmp_path, monkeypatch):
    """La salida tiene que existir de verdad. Un muro sin puerta acaba tirandose entero."""
    _apuntar_a(tmp_path, monkeypatch)
    autorizacion.autorizar("prueba: comprobar que la salida existe")
    assert autorizacion.autorizada(), (
        "Julio autorizo y aun asi no puede apagar: se quedo encerrado en su propia casa")


def test_la_autorizacion_deja_rastro(tmp_path, monkeypatch):
    """Apagar en silencio fue el problema. Apagar tiene que dejar constancia."""
    falsa = _apuntar_a(tmp_path, monkeypatch)
    autorizacion.autorizar("motivo de la prueba")
    assert os.path.exists(falsa), "no quedo constancia escrita de la autorizacion"
    dice = open(falsa, encoding="utf-8", errors="replace").read()
    assert "motivo de la prueba" in dice, (
        "la constancia no guarda el MOTIVO: sin motivo no se puede revisar despues por que se "
        "apago")


def test_la_autorizacion_CADUCA(tmp_path, monkeypatch):
    """Una autorizacion eterna es lo mismo que no tener candado."""
    falsa = _apuntar_a(tmp_path, monkeypatch)
    autorizacion.autorizar("prueba de caducidad")
    viejo = time.time() - (autorizacion.VIGENCIA_H + 1) * 3600
    os.utime(falsa, (viejo, viejo))
    assert not autorizacion.autorizada(), (
        "una autorizacion de hace mas de %d horas sigue valiendo: eso es dejar la puerta "
        "abierta para siempre" % autorizacion.VIGENCIA_H)


def test_la_ley_esta_escrita_en_la_propia_pieza():
    texto = open(os.path.join(AQUI, "arnes", "autorizacion.py"),
                 encoding="utf-8", errors="replace").read().lower()
    assert "autorizacion" in texto
    assert "julio" in texto, "la pieza ya no dice de quien es la llave"
