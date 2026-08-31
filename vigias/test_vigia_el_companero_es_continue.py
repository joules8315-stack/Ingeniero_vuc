# -*- coding: utf-8 -*-
"""VIGIA — CON QUIEN SE TRABAJA LO DICE JULIO, Y SE CUMPLE.

Julio, 2026-08-31:
  "a partir de ahora trabajaras con continue, no con cline"
  y al preguntarle, preciso: **Cline queda de RESERVA**, para cuando Continue no pueda.

POR QUE UN CANDADO Y NO UN RECORDATORIO:
  Ya paso con el equipo. La regla estaba escrita en la memoria y en el protocolo, y aun asi
  Julio tuvo que repetirla TRES veces, porque dependia de que la IA se acordara. Lo unico que
  se cumple es lo que FRENA.

  Y aqui el olvido cuesta doble: se le manda el trabajo al de siempre por costumbre, el nuevo
  no se estrena nunca, y encima parece que se avanzo.

PERO OJO, LECCION YA PAGADA: "no hacer un candado sin una forma honrada de satisfacerlo: empuja
a saltarselo, y eso es peor que no tenerlo". Por eso la reserva NO esta prohibida: esta
condicionada. Se abre diciendo POR QUE el de ahora no pudo, y queda apuntado.

LO QUE SE MIDE
  1. Existe una pieza que dice CON QUIEN se trabaja, en un solo sitio.
  2. El companero de ahora es `continue`.
  3. `cline` figura como RESERVA, con el motivo apuntado: la memoria no olvida por que.
  4. El candado FRENA mandarle trabajo a la reserva por costumbre.
  5. Pero la DEJA pasar cuando consta que el de ahora no pudo, y con su motivo.
  6. Deja trabajar con el de ahora sin estorbar.
  7. Esta ENCHUFADO, o es un adorno.
"""
import io
import json
import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

CANDADO = os.path.join(AQUI, "arnes", "candado_companero.py")
PASA, FRENA = 0, 2


def _companero():
    import companero
    return companero


@pytest.fixture
def sin_permiso(monkeypatch, tmp_path):
    """Se prueba sobre un cuaderno de mentira: una prueba jamas toca la memoria de verdad."""
    import companero
    monkeypatch.setattr(companero, "MARCA_NO_PUDO", str(tmp_path / ".no_pudo"))
    return companero


def test_existe_quien_diga_con_quien_se_trabaja():
    assert os.path.exists(os.path.join(AQUI, "arnes", "companero.py")), (
        "no existe ninguna pieza que diga con quien se trabaja. Si esta escrito a mano en cada "
        "sitio, cambiar de companero obliga a acordarse de diez sitios, y eso no se cumple")
    c = _companero()
    for pieza in ("activo", "es_reserva", "por_que_reserva", "declarar_que_no_pudo"):
        assert hasattr(c, pieza), "la pieza no sabe %s" % pieza


def test_el_companero_de_ahora_es_continue():
    assert _companero().activo() == "continue", (
        "el companero de ahora no es `continue`, y Julio lo mando el 2026-08-31")


def test_cline_es_reserva_y_se_sabe_por_que():
    c = _companero()
    assert c.es_reserva("cline"), "cline no figura como reserva"
    motivo = c.por_que_reserva("cline")
    assert motivo and len(motivo) > 15, (
        "cline es reserva pero no se apunto POR QUE. Dentro de un mes nadie sabra si fue una "
        "orden de Julio o un capricho")


def _preguntarle_al_candado(a_quien, marca=None):
    env = dict(os.environ)
    env.pop("INGENIERO_OFF", None)
    env["INGENIERO_AUTORIZACION_TEST"] = os.path.join(AQUI, "memoria", ".no_existe_esta_llave")
    if marca:
        env["INGENIERO_MARCA_NO_PUDO"] = marca
    entrada = json.dumps({"tool_input": {"command": "canal.enviar('%s', 'haz esto')" % a_quien}})
    r = subprocess.run([sys.executable, CANDADO], input=entrada, capture_output=True,
                       text=True, cwd=AQUI, env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def test_frena_ir_a_la_reserva_por_costumbre(tmp_path):
    assert os.path.exists(CANDADO), "no existe el candado del companero"
    codigo, dijo = _preguntarle_al_candado("cline", marca=str(tmp_path / ".no_hay"))
    assert codigo == FRENA, (
        "dejo mandarle trabajo a la reserva sin mas. Asi el companero nuevo no se estrena nunca "
        "y Julio tiene que repetirlo otra vez. Dijo: %s" % dijo[:200])


def test_deja_ir_a_la_reserva_cuando_consta_que_el_de_ahora_no_pudo(sin_permiso, tmp_path):
    """La forma honrada de satisfacer el candado. Sin ella, se acabaria saltando."""
    sin_permiso.declarar_que_no_pudo("continue", "los servidores no contestan")
    codigo, dijo = _preguntarle_al_candado("cline", marca=sin_permiso.MARCA_NO_PUDO)
    assert codigo == PASA, (
        "no deja usar la reserva ni siquiera constando que el de ahora no pudo. Un candado sin "
        "forma honrada de satisfacerlo empuja a saltarselo. Dijo: %s" % dijo[:200])


def test_deja_trabajar_con_el_de_ahora(tmp_path):
    codigo, _ = _preguntarle_al_candado("continue", marca=str(tmp_path / ".no_hay"))
    assert codigo == PASA, \
        "freno al companero de ahora: un candado que estorba se acaba apagando"


def test_el_candado_esta_enchufado():
    sitios = [os.path.join(AQUI, ".claude", "settings.json"),
              os.path.join(AQUI, ".claude", "settings.local.json")]
    texto = ""
    for s in sitios:
        if os.path.exists(s):
            with io.open(s, encoding="utf-8", errors="ignore") as f:
                texto += f.read()
    assert "candado_companero" in texto, \
        "el candado del companero no esta enchufado: no lo llama nadie, asi que no frena nada"
