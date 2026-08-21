# -*- coding: utf-8 -*-
"""VIGIA 19 — LOS FALLOS TIENEN QUE AVISAR ANTES, NO SOLO GUARDARSE (Julio, 2026-08-21).

  "Verifica que se esten guardando los errores y que estes aprendiendo de ellos, no veo que te
   llegue ningun paquete recordandote el error... otra vez estas confiando de tu memoria y es
   justo lo que debemos combatir."

LO QUE SE DESCUBRIO: habia 29 fallos guardados y NINGUNO avisaba nunca. La memoria de fallos
solo se consultaba al pedir un paquete, y solo si las palabras del problema coincidian. Pero
hay fallos que no son "un problema con nombre" sino **una accion**: escribir codigo desde la
terminal, por ejemplo. Ese no coincidia con nada y por eso se repitio SEIS veces el mismo dia.

La prueba mas clara de todas: el apunte de ese fallo decia
    "NO VOLVER A: meter codigo con \\n o rutas con \\a dentro de un heredoc"
y **el propio apunte estaba corrompido por el mismo fallo que describia**.

LA REGLA: guardar un fallo no es aprender. Aprender es que el fallo te FRENE la proxima vez que
vayas a repetirlo. Por eso cada fallo puede llevar un DISPARADOR: la accion que lo revive.
"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest
from cuerpo import fallos


@pytest.fixture(autouse=True)
def _limpio(tmp_path, monkeypatch):
    monkeypatch.setattr(fallos, "RUTA", str(tmp_path / "FALLOS.json"))
    yield


def _correr(payload):
    """El guardia corre APARTE, asi que hay que decirle cual es la memoria de prueba.
    Si no, lee la memoria de verdad y la prueba no prueba lo que dice probar."""
    env = dict(os.environ)
    env.pop("PYTEST_CURRENT_TEST", None)
    env["INGENIERO_FALLOS_TEST"] = fallos.RUTA
    p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_memoria.py")],
                       input=json.dumps(payload), capture_output=True, text=True,
                       env=env, timeout=120)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


# ─── un fallo puede declarar QUE ACCION lo revive ─────────────────────────────
def test_un_fallo_puede_llevar_disparador():
    f = fallos.apuntar(
        que_paso="escribir codigo desde la terminal lo corrompe",
        causa_raiz="los saltos de linea se convierten en saltos de verdad",
        cura="usar la herramienta de escribir archivos",
        no_volver_a="meter codigo con saltos dentro de una orden de terminal",
        disparador=r"<<'?\w+'?")
    assert f.get("disparador"), "no se pudo declarar la accion que revive el fallo"


def test_los_fallos_ya_vividos_tienen_disparador():
    """Los que se repitieron muchas veces son justo los que mas falta hacen."""
    fallos.sembrar()
    con = [f for f in fallos._leer() if f.get("disparador")]
    assert con, "ningun fallo declara que accion lo revive: entonces ninguno avisara jamas"


# ─── el aviso llega ANTES de repetir la accion ────────────────────────────────
def test_avisa_antes_de_escribir_codigo_desde_la_terminal():
    """El caso exacto que se repitio seis veces el 2026-08-20."""
    fallos.apuntar(
        que_paso="escribir codigo desde la terminal lo corrompe en silencio",
        causa_raiz="los saltos de linea se rompen",
        cura="usar la herramienta de escribir archivos",
        no_volver_a="meter codigo dentro de una orden de terminal",
        disparador=r"<<\s*'?\w+'?")
    code, txt = _correr({"tool_name": "Bash",
                         "tool_input": {"command": "cat > x.py <<'PY'\nimport os\nPY"}})
    assert "YA TE PASO" in txt.upper() or "no volver" in txt.lower(), \
        "no aviso del fallo ya cometido: %s" % txt[:150]


def test_no_avisa_de_lo_que_no_viene_al_caso():
    """Si avisa de todo, el aviso se vuelve ruido y se ignora."""
    fallos.apuntar(que_paso="algo de fotos", causa_raiz="x", cura="y",
                   no_volver_a="z", disparador=r"foto|imagen")
    code, txt = _correr({"tool_name": "Bash", "tool_input": {"command": "git status"}})
    assert code == 0 and "YA TE PASO" not in txt.upper(), "aviso de un fallo que no venia al caso"


def test_el_aviso_dice_QUE_hacer_en_vez_de_solo_regañar():
    fallos.apuntar(
        que_paso="escribir codigo desde la terminal lo corrompe",
        causa_raiz="los saltos se rompen",
        cura="usar la herramienta de escribir archivos, nunca la terminal",
        no_volver_a="meter codigo en una orden de terminal",
        disparador=r"<<\s*'?\w+'?")
    _, txt = _correr({"tool_name": "Bash",
                      "tool_input": {"command": "cat > y.py <<'EOF'\nx=1\nEOF"}})
    assert "herramienta de escribir" in txt.lower(), "no dice como hacerlo bien, solo que esta mal"


def test_no_estorba_cuando_no_hay_fallos_guardados():
    code, _ = _correr({"tool_name": "Bash", "tool_input": {"command": "cat > z.py <<'EOF'\nx\nEOF"}})
    assert code == 0


def test_el_interruptor_de_emergencia_lo_apaga():
    fallos.apuntar(que_paso="x", causa_raiz="y", cura="z", no_volver_a="w",
                   disparador=r"<<\s*'?\w+'?")
    env = dict(os.environ)
    env["INGENIERO_OFF"] = "1"
    env.pop("PYTEST_CURRENT_TEST", None)
    p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_memoria.py")],
                       input=json.dumps({"tool_name": "Bash",
                                         "tool_input": {"command": "cat > a.py <<'EOF'\nx\nEOF"}}),
                       capture_output=True, text=True, env=env, timeout=60)
    assert p.returncode == 0
