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


# ─── NUNCA DEJA A JULIO ATRAPADO, PERO DEJA RASTRO ────────────────────────────
def test_sin_cerebros_deja_pasar_pero_lo_apunta(tmp_path, monkeypatch):
    import candado_equipo as ce
    monkeypatch.setattr(ce, "_hay_cerebros", lambda: False)
    f = _un_codigo(tmp_path)
    import io
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_input": {"file_path": f}})))
    assert ce.main() == 0, "dejo a Julio atrapado por una cuota agotada"
    assert os.path.exists(os.environ["INGENIERO_SIN_EQUIPO_TEST"]), \
        "paso sin equipo y no quedo rastro: asi no se puede ver si se cumple"


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
