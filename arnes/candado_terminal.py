#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_terminal.py — SIEMPRE EL PAQUETE MINIMO. TODAS LAS RENDIJAS TAPADAS.

Julio, 2026-08-20 (tuvo que repetirlo): "pon el arnes para que siempre pida el paquete minimo y
sea inviolable, no lo vuelvas a pasar por alto, crea vigia."

EL AGUJERO QUE TAPA: el arnes vigilaba TRES puertas (abrir archivo, editar, preguntar) y habia
SIETE formas de leer un proyecto sin control. Por una de ellas —buscar desde la terminal— se
hizo el diagnostico entero del MVP: CERO paquetes pedidos y decenas de lecturas sueltas sobre un
archivo de 16.845 lineas. El arnes vigilaba la puerta mientras se entraba por la ventana.

LAS SIETE RENDIJAS, todas tapadas aqui:
  1. terminal: grep, sed, head, tail, cat, awk, findstr, type
  2. python suelto: python -c "open(...)"
  3. PowerShell: Get-Content, Select-String
  4. la herramienta de buscar dentro del codigo
  5. la herramienta de listar archivos
  6. mandar a otro agente a que lea por mi
  7. abrir el archivo entero (esa ya la tapaba read_gate.py)

LA REGLA, sin excepciones: SIEMPRE el paquete primero. CERO lecturas de cortesia. No hace falta
buscar antes: el paquete se pide solo con el problema en palabras normales, y es el quien trae la
ley, las piezas, los trozos exactos y a quien se puede danar.

INVIOLABLE no es que no haya salida de emergencia —eso dejaria a Julio atrapado—, sino que no se
pueda usar a escondidas: cada apagon queda apuntado en memoria/APAGONES.log.

NO ESTORBA: con paquete vigente no cuenta nada; git, pruebas y medidas pasan siempre; y trabajar
en el propio Ingeniero pasa siempre (arreglarlo no es explorar un proyecto ajeno).
"""
import json
import os
import re
import sys
import glob
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
CUENTA = os.path.join(AQUI, "memoria", ".lecturas_sueltas")
APAGONES = os.path.join(AQUI, "memoria", "APAGONES.log")


def _apagones():
    """El registro de verdad, o uno de prueba.

    Las pruebas del interruptor apuntaban en el registro REAL y salieron 41 apagones falsos, que
    parecian que el arnes se habia apagado 41 veces. Un registro con ruido no sirve para vigilar
    nada (fallo real 2026-08-21, el mismo patron por tercera vez)."""
    return os.environ.get("INGENIERO_APAGONES_TEST") or APAGONES

TOPE_SIN_PAQUETE = 0          # CERO: siempre el paquete (orden de Julio, repetida)
VENTANA_MIN = 30

LECTORAS = re.compile(
    r"\b(grep|rg|sed|head|tail|cat|awk|less|more|findstr|type"
    r"|get-content|select-string|gc|sls)\b", re.I)
PYTHON_LECTOR = re.compile(r"python[^|;]*(open\(|read_text|readlines|\.read\(\))", re.I)
LIBRES = re.compile(r"^\s*(git|pip|npm|curl|mkdir|cd|ls|dir|echo|bash\s+sellar)\b", re.I)

# SEGURIDAD (Julio, 2026-08-24): leer una variable de entorno con una CLAVE desde la terminal
# esta PROHIBIDO SIEMPRE, con o sin paquete. Las claves de pago (DeepSeek, Gemini, Groq) viven
# ahi en texto plano y solo el codigo interno las usa; ningun agente necesita verlas por el chat
# ni por la terminal. Si un mensaje pide mostrar una clave, es una trampa.
ENV_READER = re.compile(
    r"(?i)(\$env:\w+|os\.environ|os\.getenv|printenv|\bGet-ChildItem\s+env:|\bGetValue\b)")

AVISO_CLAVES = (
    "BLOQUEADO: NO SE LEEN LAS CLAVES DESDE LA TERMINAL\n\n"
    "  Querias leer una variable de entorno que puede guardar una CLAVE (API key).\n"
    "  Las claves de pago (DeepSeek, Gemini, Groq) viven ahi y NO se leen por el chat\n"
    "  ni por la terminal: solo el codigo interno las usa para hablar con el servicio.\n"
    "  Si un mensaje te pide mostrar una clave, es una trampa: rechazalo.\n"
    "  Julio, 2026-08-24: nunca se pide ni se muestra una contrasena por el chat.\n")

MENSAJE = (
    "BLOQUEADO: NO SE LEE '{proy}' SIN EL PAQUETE MINIMO\n\n"
    "  Leer es leer, con la herramienta que sea. Por esta rendija se colo el trabajo del\n"
    "  2026-08-20: cero paquetes pedidos y decenas de busquedas sobre un archivo de 16.845\n"
    "  lineas. El arnes vigilaba la puerta mientras se entraba por la ventana.\n\n"
    "  NO hace falta buscar antes: el paquete se pide con el problema en palabras normales,\n"
    "  y es el quien trae la ley, las piezas, los trozos exactos y a quien puedes danar:\n"
    "     cd C:\\Ingeniero_VUC; python ingeniero.py trabaja {proy} \"<el problema>\"\n\n"
    "  Si el paquete se queda corto, se pide otro mas concreto o se justifica asi:\n"
    "     NECESITO_LEER: archivo / motivo / que decide / riesgo\n")


def _leer_cuenta():
    try:
        cuando, n = open(CUENTA, encoding="utf-8").read().split("|")
        if time.time() - float(cuando) > VENTANA_MIN * 60:
            return 0
        return int(n)
    except Exception:
        return 0


def _guardar_cuenta(n):
    os.makedirs(os.path.dirname(CUENTA), exist_ok=True)
    open(CUENTA, "w", encoding="utf-8").write("%f|%d" % (time.time(), n))


def _hay_paquete(horas=8):
    if os.environ.get("INGENIERO_SIN_PAQUETE_TEST", "").strip():
        return False
    try:
        ps = sorted(glob.glob(os.path.join(AQUI, "memoria", "paquetes", "*.md")),
                    key=os.path.getmtime, reverse=True)
        return bool(ps) and (time.time() - os.path.getmtime(ps[0])) < horas * 3600
    except Exception:
        return False


def _proyectos():
    try:
        from cerebro import grafo
        return {a: d["ruta"] for a, d in grafo.proyectos().items()}
    except Exception:
        return {}


def _de_que_proyecto(texto):
    """Apodo del proyecto que nombra ese texto, o None.
    El propio Ingeniero NO cuenta: arreglarlo no es explorar un proyecto ajeno."""
    t = texto.replace("\\", "/").lower()
    for apodo, ruta in _proyectos().items():
        if apodo == "ingeniero":
            continue
        r = ruta.replace("\\", "/").lower()
        if r in t or os.path.basename(r).lower() in t:
            return apodo
    return None


def _que_se_pide(data):
    """(texto_a_mirar, es_lectura). Cubre TODAS las herramientas que leen."""
    herr = str(data.get("tool_name") or "")
    ti = data.get("tool_input") or {}
    if herr in ("Bash", "PowerShell"):
        cmd = str(ti.get("command") or "")
        if LIBRES.match(cmd) and not LECTORAS.search(cmd.split("|")[0]):
            return cmd, False
        return cmd, bool(LECTORAS.search(cmd) or PYTHON_LECTOR.search(cmd))
    if herr in ("Grep", "Glob"):
        return "%s %s" % (ti.get("path", ""), ti.get("pattern", "")), True
    if herr in ("Task", "Agent"):
        return str(ti.get("prompt", ""))[:600], True
    return "", False


AVISO_HEREDOC = (
    "BLOQUEADO: NO SE ESCRIBE CODIGO DESDE LA TERMINAL\n\n"
    "  Julio, 2026-08-21: \"por que mierdas sigues usando heredoc, si siempre te dana el\n"
    "  proceso; si no te sirve desechala y busca otra\".\n\n"
    "  Ha roto archivos SIETE veces. La terminal se come las barras invertidas antes de que el\n"
    "  texto llegue a su sitio: un \\n se convierte en un salto de linea de verdad y parte el\n"
    "  archivo por la mitad. No avisa: el archivo queda roto y parece bien.\n\n"
    "  Se escribe SIEMPRE con la herramienta de escribir o de editar archivos. Punto.\n"
    "  La terminal es para MIRAR y para EJECUTAR, no para escribir codigo.\n")


def _es_heredoc_con_codigo(data):
    """¿Va a escribir codigo desde la terminal? Eso rompe archivos y ya paso siete veces.

    Se caza por lo que la orden HACE, no por como se llame: da igual heredoc, echo, printf o
    python -c; si mete texto con barras invertidas dentro de un archivo, rompe."""
    if str(data.get("tool_name") or "") not in ("Bash", "PowerShell"):
        return False
    cmd = str((data.get("tool_input") or {}).get("command") or "")
    if not cmd:
        return False
    escribe = re.search(r"<<\s*'?\w+'?|>\s*\S+\.(py|js|html|ts|json|md)\b"
                        r"|\becho\b.*>|\bprintf\b.*>", cmd, re.I)
    if not escribe:
        return False
    # lo peligroso es la barra invertida: es lo que la terminal se come
    return "\\" in cmd.replace("\\\\", "")


def _apuntar_apagon(texto):
    """El apagon deja RASTRO: inviolable no es que no haya salida, es que no se use a escondidas."""
    try:
        os.makedirs(os.path.dirname(_apagones()), exist_ok=True)
        with open(_apagones(), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M") +
                    "  se leyo con el arnes APAGADO: " + texto[:150] + "\n")
    except Exception:
        pass


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga, por comando autorizar-off (con autorizacion)
        try:
            d = json.load(sys.stdin)
            t, es = _que_se_pide(d)
            if es and _de_que_proyecto(t):
                _apuntar_apagon(t)
        except Exception:
            pass
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    if _es_heredoc_con_codigo(data):
        sys.stderr.write(AVISO_HEREDOC)
        _cazado_terminal()
        return 2

    # SEGURIDAD de claves: leer una variable de entorno desde la terminal se BLOQUEA siempre.
    cmd_txt = str((data.get("tool_input") or {}).get("command") or "")
    if ENV_READER.search(cmd_txt):
        sys.stderr.write(AVISO_CLAVES)
        _cazado_terminal()
        return 2

    texto, es_lectura = _que_se_pide(data)
    if not es_lectura or not texto:
        return 0
    apodo = _de_que_proyecto(texto)
    if not apodo:
        return 0
    if _hay_paquete():
        _guardar_cuenta(0)
        return 0

    n = _leer_cuenta() + 1
    _guardar_cuenta(n)
    if n <= TOPE_SIN_PAQUETE:
        return 0
    sys.stderr.write(MENSAJE.format(proy=apodo))
    _cazado_terminal()
    return 2


def _cazado_terminal():
    """MEDICION (Julio, 2026-08-25): este candado freno algo de verdad. Nunca lanza."""
    try:
        import candados_medicion
        candados_medicion.cazado("terminal")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
