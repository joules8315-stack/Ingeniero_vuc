# -*- coding: utf-8 -*-
"""vigias/test_vigia_lo_que_pide_el_programa_no_es_de_julio.py

VIGIA: lo que pide el programa NO es de Julio.

Julio, 2026-09-21: el candado arnes/candado_legislar.py, cuando se corre con el argumento
`desde-julio`, apunta como PENDIENTES DE LEGISLAR las ordenes que vengan en el prompt. Pero
ese mismo modo lo usan los arneses y las otras IA para hablarle al candado, y ahi dentro
viajan frases que PARECEN ordenes sin serlo ("hay que arreglar X", "debes revisar Y").

Esta vigia comprueba tres cosas, cada una con su assert, corriendo el candado de verdad con
subprocess y sys.executable, y con un JSON de mentira cuyo prompt trae frases que parecen
ordenes:

  (1) con INGENIERO_OFF=1 en el entorno  -> NO apunta nada.
  (2) con INGENIERO_LLAMADA_DEL_PROGRAMA=1 -> NO apunta nada.
  (3) sin ninguna de las dos marcas -> SI apunta, como hoy.

Aislamiento: la lista de ordenes de Julio se manda a una carpeta temporal con
INGENIERO_LEGISLAR_TEST, para no ensuciar memoria/.legislacion_pendiente.json de verdad.
Es el mismo truco que usan las otras vigias de este candado.

No toca ningun otro archivo.
"""
import json
import os
import subprocess
import sys
import tempfile


AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDADO = os.path.join(AQUI, "arnes", "candado_legislar.py")

# Frases que PARECEN ordenes (llevan marca de mando) pero vienen del programa, no de Julio.
PROMPT_FALSO = (
    "Hay que arreglar el candado de legislar. "
    "Debes revisar la vigia del diccionario. "
    "Tienes que apuntar esto como pendiente. "
    "Necesitas legislar esta instruccion. "
    "Quiero que se cumpla la ley L5."
)


def _entorno_limpio(tmpdir, marcas):
    """Entorno copiado del actual, con el ledger aislado y SIN las dos marcas por defecto.

    Quita INGENIERO_OFF e INGENIERO_LLAMADA_DEL_PROGRAMA del entorno copiado y solo pone
    las que pida `marcas`. Asi la prueba (3) corre sin ninguna de las dos, como hoy.
    """
    env = dict(os.environ)
    env.pop("INGENIERO_OFF", None)
    env.pop("INGENIERO_LLAMADA_DEL_PROGRAMA", None)
    env["INGENIERO_LEGISLAR_TEST"] = os.path.join(tmpdir, ".legislacion_pendiente.json")
    for k, v in (marcas or {}).items():
        env[k] = v
    return env


def _correr_desde_julio(tmpdir, marcas):
    """Corre el candado con `desde-julio` y un JSON de mentira. Devuelve (rc, stderr, ledger)."""
    env = _entorno_limpio(tmpdir, marcas)
    entrada = json.dumps({"prompt": PROMPT_FALSO})
    proc = subprocess.run(
        [sys.executable, CANDADO, "desde-julio"],
        input=entrada,
        capture_output=True,
        text=True,
        cwd=AQUI,
        env=env,
    )
    ruta = env["INGENIERO_LEGISLAR_TEST"]
    try:
        with open(ruta, encoding="utf-8") as f:
            ledger = json.load(f)
    except Exception:
        ledger = {}
    return proc.returncode, proc.stderr, ledger


def _cuantos(ledger):
    """Cuenta las entradas apuntadas en el ledger, sea dict o lista."""
    if isinstance(ledger, dict):
        return len(ledger)
    if isinstance(ledger, list):
        return len(ledger)
    return 0


def test_con_ingeniero_off_no_apunta_nada():
    """(1) Con INGENIERO_OFF=1 el candado NO apunta nada, aunque el prompt parezca ordenes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rc, err, ledger = _correr_desde_julio(tmpdir, {"INGENIERO_OFF": "1"})
        assert rc == 0, "el candado debe salir 0 en modo desde-julio, salio %r" % rc
        assert _cuantos(ledger) == 0, (
            "con INGENIERO_OFF=1 no debe apuntarse nada, y se apuntaron %d" % _cuantos(ledger)
        )


def test_con_llamada_del_programa_no_apunta_nada():
    """(2) Con INGENIERO_LLAMADA_DEL_PROGRAMA=1 el candado NO apunta nada."""
    with tempfile.TemporaryDirectory() as tmpdir:
        rc, err, ledger = _correr_desde_julio(tmpdir, {"INGENIERO_LLAMADA_DEL_PROGRAMA": "1"})
        assert rc == 0, "el candado debe salir 0 en modo desde-julio, salio %r" % rc
        assert _cuantos(ledger) == 0, (
            "con INGENIERO_LLAMADA_DEL_PROGRAMA=1 no debe apuntarse nada, y se apuntaron %d"
            % _cuantos(ledger)
        )


def test_sin_marcas_si_apunta():
    """(3) Sin ninguna de las dos marcas, SI apunta, como hoy.

    El entorno copiado se limpia de INGENIERO_OFF e INGENIERO_LLAMADA_DEL_PROGRAMA antes de
    correr, para que esta prueba mida el comportamiento de hoy y no lo que hubiera en la
    maquina de quien la lanza.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        rc, err, ledger = _correr_desde_julio(tmpdir, {})
        assert rc == 0, "el candado debe salir 0 en modo desde-julio, salio %r" % rc
        assert _cuantos(ledger) > 0, (
            "sin INGENIERO_OFF ni INGENIERO_LLAMADA_DEL_PROGRAMA el candado SI debe apuntar, "
            "y no apunto nada"
        )


if __name__ == "__main__":
    test_con_ingeniero_off_no_apunta_nada()
    test_con_llamada_del_programa_no_apunta_nada()
    test_sin_marcas_si_apunta()
    print("ok: lo que pide el programa no es de julio")
