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
    # JULIO LO CAMBIO OTRA VEZ EL 2026-09-12, y lo dijo con estas palabras, enfadado y con razon:
    #
    #   "Ojo, le estas mandando cosas a cline, NO ES A BP, de opencode."
    #
    # Lo dijo porque el guardian de comunicacion le estaba obligando a la direccion a escribirle
    # recados a alguien que ya no trabaja, mientras el companero de verdad (Big Pickle, que corre
    # en opencode) esperaba en su propio canal. Un recado al que no trabaja no es comunicacion:
    # es ruido que ademas da la sensacion de haber avisado.
    #
    # LA HISTORIA SE CONSERVA, porque la memoria no olvida por que: el 2026-08-31 Julio mando
    # trabajar con continue en vez de cline; el 2026-09-02 volvio a cline; y hoy pasa a opencode.
    # No es capricho: es que el companero que de verdad esta entregando trabajo ha ido cambiando,
    # y esta vigia existe justamente para que el nombre de la casa SIEMPRE sea el de quien
    # trabaja, y no el de quien trabajaba.
    #
    # ESTA VIGIA NO SE AFLOJA: sigue exigiendo un nombre EXACTO y sigue frenando si alguien lo
    # cambia sin que Julio lo haya dicho. Lo unico que cambia es cual es ese nombre hoy.
    assert _companero().activo() == "opencode", (
        "el companero de ahora no es `opencode` (Big Pickle), y Julio lo mando el 2026-09-12")


def test_cline_esta_fuera_y_se_sabe_por_que():
    """Julio lo saco del todo, no lo dejo de reemplazo. Son cosas distintas.

    La reserva tiene salida honrada (se declara que el activo no pudo). El retiro NO la tiene:
    "No uses mas a cline, no lo uses" (Julio, 2026-08-31). Si siguiera figurando como reserva,
    volveria a entrar por la puerta de atras en cuanto el companero de ahora fallara.
    """
    c = _companero()
    assert c.es_retirado("continue"), (
        "continue no figura como retirado. Julio lo saco del todo el 2026-09-02, no lo dejo de "
        "reemplazo")
    assert not c.es_reserva("continue"), (
        "continue sigue figurando como reserva: asi volveria a entrar por la puerta de atras en "
        "cuanto el companero de ahora fallara, y eso es justo lo que Julio prohibio")
    motivo = c.por_que_retirado("continue")
    assert motivo and len(motivo) > 15, (
        "esta retirado pero no se apunto POR QUE. Dentro de un mes nadie sabra si fue una orden "
        "de Julio o un capricho, y la memoria no puede olvidar eso")


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
    c = _companero()
    fuera = c.retirados()
    if not fuera:
        pytest.skip("no hay ningun retirado que probar")
    nombre = fuera[0]["quien"]
    codigo, dijo = _preguntarle_al_candado(nombre, marca=str(tmp_path / ".no_hay"))
    assert codigo == FRENA, (
        "dejo mandarle trabajo a la reserva sin mas. Asi el companero nuevo no se estrena nunca "
        "y Julio tiene que repetirlo otra vez. Dijo: %s" % dijo[:200])




def test_deja_trabajar_con_el_de_ahora(tmp_path):
    """Comprueba que el candado no estorba al companero de ahora, sin fijar su nombre a mano."""
    quien = _companero().activo()
    codigo, _ = _preguntarle_al_candado(quien, marca=str(tmp_path / ".no_hay"))
    assert codigo == PASA, \
        f"freno al companero de ahora ({quien}): un candado que estorba se acaba apagando"


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
