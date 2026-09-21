"""Vigia: el puente de Codex pone los candados como Codex los entiende.

Vigila la pieza arnes/puente_codex.py, que se usa asi desde los ganchos de Codex:

    python C:/Ingeniero_VUC/arnes/puente_codex.py RUTA_DEL_CANDADO ARGUMENTOS

La pieza lee de su entrada el JSON que manda Codex, corre ese candado con el mismo
python pasandole el mismo JSON por la entrada, y traduce lo que conteste.

Motivo medido el 2026-09-21: Codex solo frena si el gancho escribe en su salida un
JSON con permissionDecision deny; la salida con 2 que usan los candados del
Ingeniero la toma por un fallo y deja pasar la orden.

Cinco pruebas:
  (1) candado sale con 2 y evento PreToolUse -> un JSON con hookSpecificOutput
      (hookEventName PreToolUse, permissionDecision deny, permissionDecisionReason
      con el motivo del candado) y el puente sale con 0.
  (2) candado sale con 0 -> el puente copia tal cual la salida normal del candado
      y sale con 0.
  (3) candado inexistente o que revienta y evento PreToolUse -> FRENA igual
      (deny con motivo de que el candado no pudo correr).
  (4) candado sale con 2 y evento NO PreToolUse -> JSON con decision block y
      reason con el motivo.
  (5) los argumentos tras la ruta del candado le llegan al candado.

La pieza se corre SOLO dentro de cada prueba, para no dejar ciega a la bateria
mientras la pieza no exista.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUENTE = os.path.join(RAIZ, "arnes", "puente_codex.py")


CANDADO_SALE_2 = '''\
import sys
sys.stderr.write("motivo del candado: no se toca eso")
sys.exit(2)
'''

CANDADO_SALE_0 = '''\
import sys
sys.stdout.write("salida normal del candado")
sys.exit(0)
'''

CANDADO_REVIENTA = '''\
raise RuntimeError("el candado se rompio")
'''

CANDADO_APUNTA_ARGUMENTOS = '''\
import sys
sys.stdout.write("ARGV=" + "|".join(sys.argv[1:]))
sys.exit(0)
'''


def _escribir_candado(carpeta, nombre, texto):
    ruta = os.path.join(carpeta, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta


def _correr_puente(candado, evento, argumentos=None, entrada=None):
    """Corre la pieza de verdad con subprocess y devuelve (codigo, salida, error).

    Si la pieza no existe todavia, se salta la prueba: la bateria no puede
    quedarse ciega mientras la pieza no exista.
    """
    if not os.path.isfile(PUENTE):
        raise unittest.SkipTest(
            "la pieza arnes/puente_codex.py todavia no existe: " + PUENTE
        )
    if entrada is None:
        entrada = {"hook_event_name": evento, "tool_name": "Bash"}
    orden = [sys.executable, PUENTE, candado]
    if argumentos:
        orden.extend(argumentos)
    proceso = subprocess.run(
        orden,
        input=json.dumps(entrada),
        capture_output=True,
        text=True,
        cwd=RAIZ,
    )
    return proceso.returncode, proceso.stdout, proceso.stderr


def _json_de_salida(salida):
    """Saca el JSON de la salida del puente, aunque venga con ruido alrededor."""
    texto = salida.strip()
    if not texto:
        raise AssertionError("el puente no escribio nada en su salida")
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        pass
    inicio = texto.find("{")
    fin = texto.rfind("}")
    if inicio == -1 or fin == -1 or fin <= inicio:
        raise AssertionError("la salida del puente no lleva un JSON: " + texto)
    return json.loads(texto[inicio:fin + 1])


class TestElPuentePoneLosCandadosACodex(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.carpeta = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_1_candado_sale_2_y_evento_pretooluse_frena_con_deny(self):
        candado = _escribir_candado(self.carpeta, "candado_2.py", CANDADO_SALE_2)
        codigo, salida, error = _correr_puente(candado, "PreToolUse")
        self.assertEqual(
            codigo, 0,
            "el puente debe salir con 0 aunque el candado frene; salio %r (err=%r)"
            % (codigo, error),
        )
        datos = _json_de_salida(salida)
        self.assertIn("hookSpecificOutput", datos)
        especifico = datos["hookSpecificOutput"]
        self.assertEqual(especifico.get("hookEventName"), "PreToolUse")
        self.assertEqual(especifico.get("permissionDecision"), "deny")
        motivo = especifico.get("permissionDecisionReason") or ""
        self.assertIn("no se toca eso", motivo)

    def test_2_candado_sale_0_copia_la_salida_normal(self):
        candado = _escribir_candado(self.carpeta, "candado_0.py", CANDADO_SALE_0)
        codigo, salida, error = _correr_puente(candado, "PreToolUse")
        self.assertEqual(
            codigo, 0,
            "el puente debe salir con 0 cuando el candado deja pasar; salio %r (err=%r)"
            % (codigo, error),
        )
        self.assertIn("salida normal del candado", salida)

    def test_3_candado_que_no_corre_frena_igual_en_pretooluse(self):
        inexistente = os.path.join(self.carpeta, "no_existe_este_candado.py")
        codigo, salida, error = _correr_puente(inexistente, "PreToolUse")
        self.assertEqual(
            codigo, 0,
            "un freno roto no puede abrir la puerta: el puente debe salir con 0 "
            "y frenar; salio %r (err=%r)" % (codigo, error),
        )
        datos = _json_de_salida(salida)
        especifico = datos.get("hookSpecificOutput") or {}
        self.assertEqual(especifico.get("permissionDecision"), "deny")
        motivo = especifico.get("permissionDecisionReason") or ""
        self.assertTrue(
            "no pudo correr" in motivo or "no pudo" in motivo or "candado" in motivo,
            "el motivo debe decir que el candado no pudo correr: %r" % motivo,
        )

        revienta = _escribir_candado(self.carpeta, "candado_revienta.py", CANDADO_REVIENTA)
        codigo2, salida2, error2 = _correr_puente(revienta, "PreToolUse")
        self.assertEqual(
            codigo2, 0,
            "el puente debe salir con 0 aunque el candado reviente; salio %r (err=%r)"
            % (codigo2, error2),
        )
        datos2 = _json_de_salida(salida2)
        especifico2 = datos2.get("hookSpecificOutput") or {}
        self.assertEqual(especifico2.get("permissionDecision"), "deny")

    def test_4_candado_sale_2_y_evento_no_pretooluse_bloquea(self):
        candado = _escribir_candado(self.carpeta, "candado_2.py", CANDADO_SALE_2)
        codigo, salida, error = _correr_puente(candado, "PostToolUse")
        self.assertEqual(
            codigo, 0,
            "el puente debe salir con 0; salio %r (err=%r)" % (codigo, error),
        )
        datos = _json_de_salida(salida)
        self.assertEqual(datos.get("decision"), "block")
        motivo = datos.get("reason") or ""
        self.assertIn("no se toca eso", motivo)

    def test_5_los_argumentos_le_llegan_al_candado(self):
        candado = _escribir_candado(
            self.carpeta, "candado_argumentos.py", CANDADO_APUNTA_ARGUMENTOS
        )
        codigo, salida, error = _correr_puente(
            candado, "PreToolUse", argumentos=["uno", "dos", "tres"]
        )
        self.assertEqual(
            codigo, 0,
            "el puente debe salir con 0; salio %r (err=%r)" % (codigo, error),
        )
        self.assertIn("uno|dos|tres", salida)


if __name__ == "__main__":
    unittest.main()
