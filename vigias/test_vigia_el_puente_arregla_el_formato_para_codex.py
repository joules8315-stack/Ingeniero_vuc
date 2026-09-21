"""Vigia: el puente de Codex arregla el formato de lo que contesta el candado.

Motivo medido el 2026-09-21: Codex solo entiende su propio formato de gancho. El
puente arnes/puente_codex.py corre el candado y, cuando el candado sale con 0,
debe envolver su JSON en hookSpecificOutput con hookEventName UserPromptSubmit
(rellenando el evento si viene vacio) y dejar pasar tal cual el texto que no sea
JSON. Esta vigia comprueba ese arreglo con un candado de mentira escrito en
tmp_path, sin tocar ningun candado de verdad.

Se corre el puente con subprocess y sys.executable, se le pasa por la entrada el
JSON {"hook_event_name": "UserPromptSubmit"} y se mira el JSON que sale.
"""

import json
import os
import subprocess
import sys


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUENTE = os.path.join(RAIZ, "arnes", "puente_codex.py")
EVENTO = "UserPromptSubmit"
TOPE_SEGUNDOS = 60


def _escribir_candado(tmp_path, texto_salida):
    """Escribe un candado de mentira que imprime texto_salida y sale con 0."""
    ruta = os.path.join(str(tmp_path), "candado_de_mentira.py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("import sys\n")
        f.write("sys.stdin.read()\n")
        f.write("sys.stdout.write(%r)\n" % (texto_salida,))
        f.write("sys.exit(0)\n")
    return ruta


def _correr_puente(ruta_candado):
    """Corre el puente con el candado dado y devuelve su salida normal."""
    entrada = json.dumps({"hook_event_name": EVENTO})
    resultado = subprocess.run(
        [sys.executable, PUENTE, ruta_candado],
        input=entrada,
        capture_output=True,
        text=True,
        timeout=TOPE_SEGUNDOS,
    )
    assert resultado.returncode == 0, (
        "el puente debe salir siempre con 0, salio con %r: %s"
        % (resultado.returncode, resultado.stderr)
    )
    return resultado.stdout


def _json_de_salida(salida):
    """Convierte la salida del puente en JSON. Falla si no es JSON."""
    try:
        return json.loads(salida)
    except ValueError as exc:
        raise AssertionError(
            "la salida del puente no es JSON: %r (%s)" % (salida, exc)
        )


def test_evento_vacio_se_rellena_y_se_conserva_el_contexto(tmp_path):
    """(1) hookEventName vacio se rellena con UserPromptSubmit y el contexto se conserva."""
    candado = _escribir_candado(
        tmp_path,
        json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "",
                "additionalContext": "A",
            }
        }),
    )
    salida = _correr_puente(candado)
    datos = _json_de_salida(salida)

    assert "hookSpecificOutput" in datos, (
        "la salida debe traer hookSpecificOutput: %r" % (datos,)
    )
    assert datos["hookSpecificOutput"]["hookEventName"] == EVENTO, (
        "hookEventName debe ser %r, fue %r"
        % (EVENTO, datos["hookSpecificOutput"].get("hookEventName"))
    )
    assert datos["hookSpecificOutput"]["additionalContext"] == "A", (
        "additionalContext debe ser 'A', fue %r"
        % (datos["hookSpecificOutput"].get("additionalContext"),)
    )


def test_contexto_suelto_se_envuelve_en_hook_specific_output(tmp_path):
    """(2) additionalContext suelto se envuelve con el evento y no queda arriba."""
    candado = _escribir_candado(
        tmp_path,
        json.dumps({"additionalContext": "B"}),
    )
    salida = _correr_puente(candado)
    datos = _json_de_salida(salida)

    assert "hookSpecificOutput" in datos, (
        "la salida debe traer hookSpecificOutput: %r" % (datos,)
    )
    assert datos["hookSpecificOutput"]["hookEventName"] == EVENTO, (
        "hookEventName debe ser %r, fue %r"
        % (EVENTO, datos["hookSpecificOutput"].get("hookEventName"))
    )
    assert datos["hookSpecificOutput"]["additionalContext"] == "B", (
        "additionalContext debe ser 'B', fue %r"
        % (datos["hookSpecificOutput"].get("additionalContext"),)
    )
    assert "additionalContext" not in datos, (
        "no debe quedar additionalContext suelto arriba: %r" % (datos,)
    )


def test_texto_que_no_es_json_pasa_tal_cual(tmp_path):
    """(3) un texto que no es JSON sale igual, sin tocarlo."""
    texto = "esto no es JSON, es texto plano del candado"
    candado = _escribir_candado(tmp_path, texto)
    salida = _correr_puente(candado)

    assert salida == texto, (
        "el texto que no es JSON debe salir igual: esperado %r, salio %r"
        % (texto, salida)
    )


def test_json_ya_correcto_sale_igual(tmp_path):
    """(4) un JSON ya bien formado sale igual, sin cambios."""
    original = {
        "hookSpecificOutput": {
            "hookEventName": EVENTO,
            "additionalContext": "C",
        }
    }
    candado = _escribir_candado(tmp_path, json.dumps(original))
    salida = _correr_puente(candado)
    datos = _json_de_salida(salida)

    assert datos == original, (
        "un JSON ya correcto debe salir igual: esperado %r, salio %r"
        % (original, datos)
    )
