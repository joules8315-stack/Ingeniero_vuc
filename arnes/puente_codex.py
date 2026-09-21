"""Puente entre los candados del Ingeniero y los ganchos de Codex.

Se usa asi desde los ganchos de Codex:

    python arnes/puente_codex.py RUTA_DEL_CANDADO ARGUMENTOS

Que hace:
  1. Lee de su entrada todo el JSON que manda Codex y saca de ahi hook_event_name.
  2. Corre el candado con sys.executable, pasandole los ARGUMENTOS y ese mismo JSON
     por su entrada, con un tope de 120 segundos.
  3. Traduce lo que el candado conteste:
       - salida 2 y evento PreToolUse -> JSON con hookSpecificOutput
         (hookEventName PreToolUse, permissionDecision deny,
         permissionDecisionReason con el motivo del candado, recortado a 2000 letras).
       - salida 2 y otro evento -> JSON con decision block y reason con ese motivo.
       - salida 0 -> copia tal cual la salida normal del candado.
       - candado inexistente, que se pasa del tope o que revienta:
           * PreToolUse -> FRENA con deny y motivo de que el candado no pudo correr.
           * otro evento -> no escribe nada.

El puente sale SIEMPRE con 0 y NUNCA lanza.

Motivo medido el 2026-09-21: Codex solo frena si el gancho escribe ese JSON; la
salida con 2 de los candados del Ingeniero la toma por un fallo y deja pasar la
orden.
"""

import json
import os
import subprocess
import sys


TOPE_SEGUNDOS = 120
TOPE_MOTIVO = 2000
EVENTO_PRE_TOOL_USE = "PreToolUse"


def _leer_entrada():
    """Lee de la entrada todo el texto disponible. Nunca lanza."""
    try:
        datos = sys.stdin.read()
    except Exception:
        return ""
    if datos is None:
        return ""
    return datos


def _sacar_evento(texto_entrada):
    """Saca hook_event_name del JSON de Codex. Si no se puede, cadena vacia."""
    if not texto_entrada:
        return ""
    try:
        datos = json.loads(texto_entrada)
    except Exception:
        return ""
    if not isinstance(datos, dict):
        return ""
    evento = datos.get("hook_event_name")
    if isinstance(evento, str):
        return evento
    return ""


def _recortar(texto):
    """Recorta el motivo a 2000 letras. Nunca lanza."""
    if texto is None:
        return ""
    if not isinstance(texto, str):
        try:
            texto = str(texto)
        except Exception:
            return ""
    return texto[:TOPE_MOTIVO]


def _motivo_del_candado(salida_normal, salida_errores):
    """El motivo es la salida de errores; si esta vacia, la normal."""
    if salida_errores and salida_errores.strip():
        return _recortar(salida_errores)
    return _recortar(salida_normal)


def _correr_candado(ruta_candado, argumentos, texto_entrada):
    """Corre el candado. Devuelve (codigo, salida_normal, salida_errores).

    Si el candado no existe, se pasa del tope o revienta, devuelve None para
    que el llamante decida frenar o callar.
    """
    if not ruta_candado or not os.path.exists(ruta_candado):
        return None
    orden = [sys.executable, ruta_candado] + list(argumentos)
    try:
        proceso = subprocess.run(
            orden,
            input=texto_entrada,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TOPE_SEGUNDOS,
            universal_newlines=True,
        )
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None
    salida_normal = proceso.stdout if proceso.stdout is not None else ""
    salida_errores = proceso.stderr if proceso.stderr is not None else ""
    return (proceso.returncode, salida_normal, salida_errores)


def _escribir_json(datos):
    """Escribe un JSON en la salida normal. Nunca lanza."""
    try:
        sys.stdout.write(json.dumps(datos, ensure_ascii=False))
        sys.stdout.flush()
    except Exception:
        pass


def _escribir_texto(texto):
    """Copia texto tal cual a la salida normal. Nunca lanza."""
    try:
        sys.stdout.write(texto)
        sys.stdout.flush()
    except Exception:
        pass


def _frenar(evento, motivo):
    """Escribe el JSON de freno que Codex entiende. Nunca lanza."""
    motivo = _recortar(motivo)
    if evento == EVENTO_PRE_TOOL_USE:
        _escribir_json({
            "hookSpecificOutput": {
                "hookEventName": EVENTO_PRE_TOOL_USE,
                "permissionDecision": "deny",
                "permissionDecisionReason": motivo,
            }
        })
    else:
        _escribir_json({
            "decision": "block",
            "reason": motivo,
        })


def main(argv=None):
    """Punto de entrada. Sale siempre con 0 y nunca lanza."""
    if argv is None:
        argv = sys.argv[1:]

    texto_entrada = _leer_entrada()
    evento = _sacar_evento(texto_entrada)

    if not argv:
        # Sin ruta de candado no hay nada que correr: un freno roto no abre la puerta.
        if evento == EVENTO_PRE_TOOL_USE:
            _frenar(evento, "El candado no pudo correr: no se recibio su ruta.")
        return 0

    ruta_candado = argv[0]
    argumentos = argv[1:]

    resultado = _correr_candado(ruta_candado, argumentos, texto_entrada)

    if resultado is None:
        # Candado inexistente, pasado del tope o reventado.
        if evento == EVENTO_PRE_TOOL_USE:
            _frenar(
                evento,
                "El candado no pudo correr (no existe, se paso del tope de "
                "%d segundos o revento): un freno roto no puede abrir la puerta."
                % TOPE_SEGUNDOS,
            )
        return 0

    codigo, salida_normal, salida_errores = resultado

    if codigo == 0:
        _escribir_salida_arreglada(salida_normal, evento)
        return 0

    if codigo == 2:
        motivo = _motivo_del_candado(salida_normal, salida_errores)
        _frenar(evento, motivo)
        return 0

    # Cualquier otro codigo: el candado no pudo decidir. Freno roto no abre.
    if evento == EVENTO_PRE_TOOL_USE:
        _frenar(
            evento,
            "El candado no pudo correr (salio con %s): un freno roto no puede "
            "abrir la puerta." % codigo,
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        # El puente nunca lanza: si algo se escapa, sale con 0.
        sys.exit(0)
