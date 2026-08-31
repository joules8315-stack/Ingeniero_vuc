# -*- coding: utf-8 -*-
"""VIGIA — EL CANDADO DEL NOMBRE FRENA DE VERDAD.

Ley: CONTRATO_SE_BUSCA_POR_NOMBRE.md (Julio, 2026-08-31).

No se mide lo que el candado DICE, se mide lo que HACE: se le da de comer una peticion de
mentira y se mira si frena o deja pasar. Una ley escrita que nadie hace cumplir ya se probo que
no sirve: Julio tuvo que repetir esto muchas veces estando escrito.

LO QUE SE MIDE
  1. Frena un numero de renglon escrito a mano para encontrar codigo.
  2. Frena leer un pedazo pasandole dos numeros sueltos.
  3. Frena pedirle al equipo un TRAMO de renglones para reparar.
  4. NO frena los documentos, ni las vigias, ni el propio arnes (o se apagaria por pesado).
  5. NO SE ABRE ANTE EL FALLO: si no entiende la peticion, frena. Ese fue el agujero medido
     el 2026-08-31 en el candado hermano, y no se repite aqui.
  6. Esta ENCHUFADO: un candado que no esta enchufado es un adorno.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDADO = os.path.join(AQUI, "arnes", "candado_por_nombre.py")

PASA, FRENA = 0, 2


def _preguntarle(ruta, contenido, crudo=None):
    """Le da de comer una peticion al candado. Devuelve (codigo, lo_que_dijo)."""
    env = dict(os.environ)
    env.pop("INGENIERO_OFF", None)
    env["INGENIERO_AUTORIZACION_TEST"] = os.path.join(AQUI, "memoria", ".no_existe_esta_llave")
    if crudo is None:
        crudo = json.dumps({"tool_input": {"file_path": ruta, "content": contenido}})
    r = subprocess.run([sys.executable, CANDADO], input=crudo, capture_output=True,
                       text=True, cwd=AQUI, env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def test_el_candado_existe():
    assert os.path.exists(CANDADO), \
        "no existe el candado del nombre: la ley esta escrita pero nadie la hace cumplir"


def test_frena_el_numero_escrito_a_mano():
    """El caso exacto que costo el dia entero."""
    codigo, dijo = _preguntarle("cerebro/algo.py",
                                "def f():\n    desde_armar, hasta_armar = 87, 227\n    return 1\n")
    assert codigo == FRENA, (
        "dejo pasar un numero de renglon escrito a mano. Es EXACTAMENTE lo que Julio mando "
        "reparar: ese numero se corre en cuanto alguien anade algo mas arriba. Dijo: %s" % dijo[:200])


def test_frena_leer_un_pedazo_con_dos_numeros():
    codigo, dijo = _preguntarle("cerebro/algo.py",
                                'def f(r):\n    return _lineas_de(r, 87, 227)\n')
    assert codigo == FRENA, \
        "dejo pasar la lectura de un pedazo por dos numeros sueltos. Dijo: %s" % dijo[:200]


def test_frena_pedirle_al_equipo_un_tramo():
    """Un tramo BORRA la funcion entera: es 'lo que borra todo'."""
    codigo, dijo = _preguntarle("cuerpo/algo.py",
                                'PROMPT = """responde\n  "lineas": "desde-hasta",\n"""\n')
    assert codigo == FRENA, \
        "dejo pasar un contrato que le pide al equipo un tramo de renglones. Dijo: %s" % dijo[:200]


def test_deja_pasar_el_codigo_sano():
    """Si frena lo sano, se acaba apagando, y entonces no protege nada."""
    codigo, _ = _preguntarle("cerebro/algo.py",
                             'def f(r):\n    return piezas.funcion_completa(r, "armar")\n')
    assert codigo == PASA, \
        "freno codigo sano que busca por nombre: un candado que grita en falso se apaga solo"


def test_no_estorba_en_los_documentos():
    codigo, _ = _preguntarle("NOTAS.md", "aqui se explica que antes decia desde, hasta = 87, 227")
    assert codigo == PASA, "freno un documento: los documentos no son codigo"


def test_no_estorba_en_las_vigias():
    """Una vigia TIENE que poder nombrar lo prohibido, o no puede probar que esta prohibido."""
    codigo, _ = _preguntarle(os.path.join(AQUI, "vigias", "test_algo.py"),
                             "def test_x():\n    desde_a, hasta_a = 87, 227\n")
    assert codigo == PASA, \
        "freno a una vigia: entonces ninguna vigia puede probar que esto esta prohibido"


def test_no_estorba_en_el_propio_arnes():
    codigo, _ = _preguntarle(os.path.join(AQUI, "arnes", "candado_x.py"),
                             "PATRON = 'desde_a, hasta_a = 87, 227'\n")
    assert codigo == PASA, "freno al propio arnes: hay que poder reparar un candado roto"


def test_no_se_abre_cuando_algo_va_mal():
    """EL AGUJERO MEDIDO el 2026-08-31 en el candado hermano: fallaba al leer y abria entero.

    Un candado que se abre solo cuando algo va mal no es un candado. Aqui se cierra.
    """
    codigo, dijo = _preguntarle(None, None, crudo="esto no se entiende {{{")
    assert codigo == FRENA, (
        "cuando no entiende la peticion, ABRE. Ese es el agujero por el que se colo todo: "
        "basta con que algo falle para que el candado deje pasar. Dijo: %s" % dijo[:200])


def test_esta_enchufado():
    """Un candado que no esta enchufado es un adorno caro."""
    sitios = [os.path.join(AQUI, ".claude", "settings.json"),
              os.path.join(AQUI, ".claude", "settings.local.json")]
    puesto = False
    for s in sitios:
        if os.path.exists(s):
            with open(s, encoding="utf-8", errors="ignore") as f:
                if "candado_por_nombre" in f.read():
                    puesto = True
                    break
    assert puesto, (
        "el candado existe pero NO esta enchufado en los ajustes: no lo llama nadie, asi que no "
        "frena nada. Escrito no es cumplido; esa es justo la leccion que costo el dia")
