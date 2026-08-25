# -*- coding: utf-8 -*-
"""VIGIA 24 — NO SE ESCRIBE CODIGO A SOLAS (Julio, 2026-08-21).

  "pon candado de modo que siempre tengas que trabajar con equipo, y vigias para el arnes, que
   te frene cuando no lo hagas."
  "pon candado para que siempre actues con equipo, modo ingeniero y economico, sin excusa."
  "por no trabajar en equipo ya has gastado 19."

LO QUE PASO: la regla estaba escrita —en la memoria de Julio y en el protocolo— y aun asi se
escribio a solas un guardia entero, tres vigias y cuatro reparaciones, con los tres cerebros
disponibles. Julio lo pago de su bolsillo y tuvo que repetirlo por tercera vez.

**Una regla que depende de que la IA se acuerde NO es una regla.** Por eso deja de estar escrita
y pasa a estar cerrada con llave: para tocar codigo hace falta un veredicto del equipo.

QUE SE VIGILA AQUI:
  · que el candado FRENE de verdad al escribir codigo sin veredicto
  · que la llave del equipo abra, y solo para los archivos que el equipo miro
  · que un veredicto viejo NO sirva de llave para siempre
  · que NO estorbe: documentos, archivos nuevos y el propio arnes pasan siempre
  · que nunca deje a Julio atrapado si no hay cerebros, pero que quede APUNTADO
"""
import json
import os
import subprocess
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest


@pytest.fixture(autouse=True)
def _llave_aparte(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_SIN_EQUIPO_TEST", str(tmp_path / "sin_equipo.log"))
    yield


def _correr(fp, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    r = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_equipo.py")],
                       input=json.dumps({"tool_input": {"file_path": fp}}),
                       capture_output=True, text=True, env=env, cwd=AQUI)
    return r.returncode, (r.stderr or "")


def _un_codigo(tmp_path):
    f = tmp_path / "algo.py"
    f.write_text("x = 1\n", encoding="utf-8")
    return str(f)


# ─── FRENA ────────────────────────────────────────────────────────────────────
def test_frena_escribir_codigo_sin_equipo(tmp_path):
    """EL NUCLEO. Si esto pasa a verde sin llave, el candado no sirve para nada."""
    code, err = _correr(_un_codigo(tmp_path))
    assert code == 2, "dejo escribir codigo sin que el equipo lo mirara"
    assert "A SOLAS" in err or "equipo" in err.lower()


def test_el_aviso_dice_como_arreglarlo(tmp_path):
    """Un candado que frena sin decir la salida se acaba apagando, y eso es peor."""
    _, err = _correr(_un_codigo(tmp_path))
    assert "ingeniero.py equipo" in err, "frena pero no dice como cumplirlo"


# ─── LA LLAVE ─────────────────────────────────────────────────────────────────
def test_con_veredicto_del_equipo_deja_escribir(tmp_path):
    import candado_equipo as ce
    f = _un_codigo(tmp_path)
    ce.guardar_veredicto("una tarea", [f], "groq", "gemini", "APROBADO")
    code, _ = _correr(f)
    assert code == 0, "estorba: el equipo ya lo miro y aun asi no deja escribir"


def test_un_veredicto_de_OTRA_cosa_no_sirve_de_llave(tmp_path):
    """Si un veredicto cualquiera abriera todo, bastaria llamar al equipo una vez y ya."""
    import candado_equipo as ce
    ce.guardar_veredicto("otra tarea", [str(tmp_path / "otro.py")], "groq", "gemini", "APROBADO")
    code, _ = _correr(_un_codigo(tmp_path))
    assert code == 2, "un veredicto sobre otro archivo abrio este"


def test_un_veredicto_viejo_ya_no_abre(tmp_path):
    """La llave caduca: si no, el equipo se llama una vez al mes y el candado es decorativo."""
    import candado_equipo as ce
    f = _un_codigo(tmp_path)
    d = ce.guardar_veredicto("una tarea", [f], "groq", "gemini", "APROBADO")
    d["cuando"] = time.time() - (ce.VIGENCIA_MIN + 10) * 60
    json.dump(d, open(os.environ["INGENIERO_VEREDICTO_TEST"], "w", encoding="utf-8"))
    code, _ = _correr(f)
    assert code == 2, "un veredicto caducado siguio abriendo"


# ─── NO ESTORBA ───────────────────────────────────────────────────────────────
def test_los_documentos_pasan_siempre(tmp_path):
    d = tmp_path / "CONTRATO.md"
    d.write_text("ley\n", encoding="utf-8")
    code, _ = _correr(str(d))
    assert code == 0, "estorba: escribir la ley no es programar"


def test_un_archivo_nuevo_pasa(tmp_path):
    code, _ = _correr(str(tmp_path / "todavia_no_existe.py"))
    assert code == 0, "estorba: crear no es reescribir"


def test_el_propio_arnes_se_puede_arreglar():
    code, _ = _correr(os.path.join(AQUI, "arnes", "candado_equipo.py"))
    assert code == 0, "si el candado se rompe hay que poder arreglarlo o se queda todo parado"


# ─── SIN CEREBROS TAMPOCO SE PASA: LA PUERTA DE ESCAPE ESTA CERRADA ───────────
def test_sin_cerebros_bloquea_igual(tmp_path, monkeypatch):
    """LEY NUEVA (Julio, 2026-08-21): se CERRO la puerta de escape.

    Antes, si los cerebros estaban agotados, se podia escribir a solas y quedaba apuntado.
    Julio la cerro porque esa rendija dejaba a foto_informe y a cualquier proyecto SIN VIGILAR:
    bastaba con que las cuotas se agotaran para colar codigo sin que nadie lo auditara.

    Ahora, sin veredicto del equipo NO se toca codigo, haya cerebros o no. Si no hay ninguno
    libre, se BLOQUEA y decide Julio. Esta vigia es la que impide que la rendija vuelva a
    abrirse sin que el se entere.
    """
    import candado_equipo as ce
    monkeypatch.setattr(ce, "_hay_cerebros", lambda: False)     # cuotas agotadas: ni uno libre
    monkeypatch.setattr(ce, "veredicto_vigente", lambda: None)  # y el equipo no ha dicho nada
    f = _un_codigo(tmp_path)
    import io
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_input": {"file_path": f}})))
    assert ce.main() == 2, \
        "se colo codigo sin equipo: la puerta de escape volvio a abrirse"


def test_cada_frenada_queda_apuntada(tmp_path, monkeypatch):
    """LA LIBRETA AL REVES (Julio, 2026-08-21): "Si, que apunte al reves."

    Antes se apuntaba lo que se COLABA sin equipo. Como ya no se cuela nada, esa libreta se
    quedaba vacia para siempre (medido: el archivo no llego a existir nunca). Ahora se apunta
    cada vez que el candado FRENA, con el motivo. Asi Julio puede ver al final de la semana
    cuantas veces hubo que pararse, en vez de tener que creerselo.
    """
    import candado_equipo as ce
    monkeypatch.setattr(ce, "veredicto_vigente", lambda: None)
    f = _un_codigo(tmp_path)
    import io
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_input": {"file_path": f}})))
    assert ce.main() == 2, "no freno: sin esto no hay nada que apuntar"
    libreta = os.environ["INGENIERO_SIN_EQUIPO_TEST"]
    assert os.path.exists(libreta), "freno y no dejo rastro: Julio no puede ver cuantas veces fue"
    escrito = open(libreta, encoding="utf-8").read()
    assert os.path.basename(f) in escrito, "no apunto QUE archivo se freno"
    assert "veredicto" in escrito.lower(), "no apunto POR QUE se freno"


def test_la_salida_de_emergencia_sigue_siendo_de_julio(tmp_path, monkeypatch):
    """Cerrar la puerta no puede significar dejar a Julio encerrado.

    La ley dura dice que SIEMPRE tiene que haber una salida y que la salida deje rastro. Con la
    puerta de escape cerrada, la unica salida que queda es la que Julio maneja a mano
    (INGENIERO_OFF). Si un dia tambien desapareciera, el candado dejaria de ser un candado y
    pasaria a ser un muro: se acabaria apagando entero, que es peor que el problema.
    """
    import io
    import candado_equipo as ce
    import autorizacion as aut
    monkeypatch.setattr(ce, "veredicto_vigente", lambda: None)
    monkeypatch.setenv("INGENIERO_OFF", "1")
    f = _un_codigo(tmp_path)
    entrada = json.dumps({"tool_input": {"file_path": f}})

    # LEY NUEVA (Julio, 2026-08-24): "que solo pueda quitarlos yo, por medio de comando, en ps,
    # y debe ser con previa autorizacion". Antes bastaba prender la variable y los candados se
    # apagaban EN SILENCIO: cualquiera podia y no quedaba rastro. La salida sigue existiendo,
    # pero ahora es SUYA y deja constancia.
    monkeypatch.setenv("INGENIERO_AUTORIZACION_TEST", str(tmp_path / "aut_de_mentira"))

    # 1) La variable A SOLAS no abre nada.
    monkeypatch.setattr("sys.stdin", io.StringIO(entrada))
    assert ce.main() != 0, ("prender la variable a solas apago el candado: cualquiera podria "
                            "apagarlo, y sin dejar rastro")

    # 2) Con la autorizacion de Julio, SI abre. Un candado sin salida no es candado, es un muro,
    #    y acaba con Julio apagandolo todo, que es peor que el problema.
    aut.autorizar("prueba: comprobar que la salida de Julio sigue existiendo")
    monkeypatch.setattr("sys.stdin", io.StringIO(entrada))
    assert ce.main() == 0, "Julio se quedo encerrado: ni con su propio interruptor puede salir"


def test_tiene_interruptor_de_emergencia():
    txt = open(os.path.join(AQUI, "arnes", "candado_equipo.py"), encoding="utf-8").read()
    assert "INGENIERO_OFF" in txt


# ─── ENGANCHADO DE VERDAD ─────────────────────────────────────────────────────
def test_esta_en_el_instalador():
    """De nada sirve un candado que no se instala."""
    txt = open(os.path.join(AQUI, "arnes", "settings_propuesto.json"), encoding="utf-8").read()
    assert "candado_equipo" in txt, "el candado del equipo no esta en el instalador"


def test_la_orden_equipo_existe():
    """El candado manda usar `ingeniero.py equipo`: esa orden tiene que existir de verdad.
    Ya paso una vez: un candado ofrecia una llave que no existia y bloqueaba el trabajo entero."""
    txt = open(os.path.join(AQUI, "ingeniero.py"), encoding="utf-8").read()
    assert 'cmd == "equipo"' in txt, "el candado manda una orden que no existe"
