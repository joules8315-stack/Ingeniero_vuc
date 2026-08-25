#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_protocolo.py — LOS DISPARADORES DEL PROTOCOLO DE JULIO.

Julio, 2026-08-20: "Falta que actues segun protocolos, ya eso lo he dicho miles de veces...
crea los putos disparadores, lo que tengas que hacer."

EL PROTOCOLO YA ESTABA ESCRITO. Vive en `PROTOCOLO_DEL_CHAT.md` (Asesor Marketing) y Julio lo
redacto el 2026-07-28 con este fin textual: "yo solo digo hagamos esto y el lo hace, sin que yo
repita". El fallo NO era que faltara el protocolo: era que **nada obligaba a cumplirlo**.

Lo que se incumplio el 2026-08-20, con el protocolo escrito y delante:
  · LEY DURA "lenguaje simple": se le hablo de archivos .py, hooks, Playwright y commits en casi
    todos los mensajes, estando PROHIBIDO por escrito.
  · LEY DURA "confirmar el objetivo antes de construir": se construyo sin repetirle el resultado
    ni esperar su "si".
  · "¿Ya existe? ¿Ya lo decidio Julio?": se le pregunto 3 veces cosas que el ya habia escrito.

Tres puestos de guardia:
  candado_protocolo.py prompt   -> UserPromptSubmit: detecta si Julio REPITE y avisa en el momento
  candado_protocolo.py salida   -> Stop: frena si la respuesta lleva jerga prohibida
  candado_protocolo.py construir-> PreToolUse Write: exige haber confirmado el objetivo

Todos con `INGENIERO_OFF=1` para apagarlos, y ninguno bloquea mas de dos veces seguidas.
"""
import json, os, re, sys, time, difflib

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
DICHO = os.path.join(AQUI, "memoria", "LO_QUE_JULIO_YA_DIJO.json")
CONTADOR = os.path.join(AQUI, "memoria", ".protocolo_bloqueos")


def _contador():
    """El contador de verdad, o uno de prueba.

    Ley 23, CUARTO sitio con el mismo patron: era un archivo COMPARTIDO. Un bloqueo de verdad
    gastaba las oportunidades y la comprobacion se encontraba la valvula de escape ya abierta:
    salia roja sin que nada estuviera roto. Cada prueba usa su copia."""
    return os.environ.get("INGENIERO_CONTADOR_TEST") or CONTADOR
TOPE_BLOQUEOS = 2

# Jerga PROHIBIDA por la LEY DURA de lenguaje simple del PROTOCOLO_DEL_CHAT.md.
# Julio no es tecnico y lo ha repetido muchas veces, con enojo.
JERGA = [
    "playwright", "regex", "hash", "commit", "endpoint", "api rest", "localstorage",
    "service worker", "hook", "json", "parsear", "deploy", "backend", "frontend",
    "stack", "framework", "boilerplate", "refactor", "mock", "pytest", "subprocess",
    "manifest", "cache", "token de sesion", "middleware", "query", "schema",
]
# Se permiten si van traducidas al lado (ej: "el candado (hook)") — se detecta el parentesis.


def _bloqueos_seguidos():
    try:
        cuando, n = open(_contador(), encoding="utf-8").read().split("|")
        if time.time() - float(cuando) > 600:
            return 0
        return int(n)
    except Exception:
        return 0


def _apuntar_bloqueo(n):
    os.makedirs(os.path.dirname(_contador()), exist_ok=True)
    open(_contador(), "w", encoding="utf-8").write("%f|%d" % (time.time(), n))


# ─── 1) ¿JULIO ESTA REPITIENDO? (UserPromptSubmit) ─────────────────────────────
def _leer_dichos():
    try:
        return json.load(open(DICHO, encoding="utf-8"))
    except Exception:
        return []


def _guardar_dichos(d):
    os.makedirs(os.path.dirname(DICHO), exist_ok=True)
    json.dump(d[-200:], open(DICHO, "w", encoding="utf-8"), ensure_ascii=False)


def _normaliza(t):
    t = (t or "").lower()
    t = re.sub(r"[^a-záéíóúñü ]+", " ", t)
    return " ".join(w for w in t.split() if len(w) > 3)


def repite(texto, umbral=0.62):
    """¿Julio ya habia dicho esto? Devuelve (si_repite, lo_que_dijo_antes, parecido).

    ESTE ES EL TERMOMETRO DEL SISTEMA ENTERO. El fin del Ingeniero es "que Julio no repita".
    Antes se contaba a mano —y por eso marcaba CERO habiendo repetido cuatro veces el mismo dia—.
    Ahora se dispara solo en cada mensaje suyo, sin que nadie tenga que acordarse."""
    n = _normaliza(texto)
    if len(n.split()) < 4:
        return False, "", 0.0
    mejor, parecido = "", 0.0
    for viejo in _leer_dichos():
        p = difflib.SequenceMatcher(None, n, _normaliza(viejo)).ratio()
        if p > parecido:
            mejor, parecido = viejo, p
    return (parecido >= umbral), mejor, round(parecido, 2)


def prompt():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    texto = str(data.get("prompt") or "")
    aviso = ""
    if texto:
        si, antes, p = repite(texto)
        if si:
            try:
                from cuerpo import respuestas
                respuestas.apuntar_repeticion(texto, antes)
            except Exception:
                pass
            aviso = (
                "\n*** JULIO ESTA REPITIENDO ALGO QUE YA TE DIJO (parecido %s) ***\n"
                "   Ya te lo habia dicho asi: \"%s\"\n"
                "   El fin del Ingeniero es que NO tenga que repetir. Que lo haga significa que\n"
                "   algo se ignoro. Antes de contestar: mira por que no se cumplio la primera vez,\n"
                "   dilo, y arreglalo — no te limites a hacerlo ahora.\n" % (p, antes[:220])
            )
        d = _leer_dichos()
        d.append(texto)
        _guardar_dichos(d)

    protocolo = (
        "PROTOCOLO DEL CHAT (ley de Julio, 2026-07-28 — se cumple SIEMPRE):\n"
        "  1. LENGUAJE SIMPLE: PROHIBIDO usar jerga con Julio. Nada de nombres de archivos,\n"
        "     ni palabras tecnicas. Se explica como a un amigo dueno de un negocio.\n"
        "  2. CONFIRMAR EL OBJETIVO ANTES DE CONSTRUIR: se le repite con palabras propias el\n"
        "     RESULTADO que quiere y se ESPERA su 'si'. Prohibido el camino facil.\n"
        "  3. ANTES de responder: ¿ya existe? ¿Julio ya lo decidio? ¿hay una ley que lo gobierne\n"
        "     y por que no se cumplio? ¿me falta informacion? (nunca asumir).\n"
        "  4. LEGISLAR cada instruccion suya: contrato + vigia + aplicar + sellar.\n"
        "  5. Trabajar EN BUCLE hasta terminar; no parar a preguntar lo que se puede buscar.\n"
    )
    print(json.dumps({"additionalContext": protocolo + aviso,
                      "systemMessage": ("Julio esta repitiendo: mira por que se ignoro"
                                        if aviso else "")}, ensure_ascii=False))
    return 0


# ─── 2) ¿LA RESPUESTA LLEVA JERGA PROHIBIDA? (Stop) ────────────────────────────
def _jerga_en(texto):
    t = (texto or "").lower()
    fuera = []
    for p in JERGA:
        if p in t:
            # se permite si va traducida entre parentesis justo al lado
            if re.search(re.escape(p) + r"[^.\n]{0,40}\)", t) or re.search(r"\([^)]{0,40}" + re.escape(p), t):
                continue
            fuera.append(p)
    # nombres de archivos de codigo: tambien prohibidos
    for m in re.findall(r"\b[a-z_]+\.(?:py|html|js|json|md)\b", t):
        fuera.append(m)
    return sorted(set(fuera))


def salida():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (autorizar-off)
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ultimo = str(data.get("last_assistant_message") or "")
    if not ultimo:
        return 0
    fuera = _jerga_en(ultimo)
    if not fuera:
        _apuntar_bloqueo(0)
        return 0
    veces = _bloqueos_seguidos()
    if veces >= TOPE_BLOQUEOS:
        _apuntar_bloqueo(0)
        sys.stderr.write("AVISO: la respuesta lleva jerga prohibida (%s). Se deja pasar para no\n"
                         "  atascar a Julio, pero incumple la LEY DURA de lenguaje simple.\n"
                         % ", ".join(fuera[:6]))
        return 0
    _apuntar_bloqueo(veces + 1)
    sys.stderr.write(
        "NO SE PUEDE TERMINAR: la respuesta lleva JERGA PROHIBIDA por el protocolo de Julio.\n"
        "  Palabras que sobran: %s\n"
        "  Julio NO es tecnico y lo ha repetido muchas veces, con enojo. Reescribe la respuesta\n"
        "  como se la contarias a un amigo dueno de un negocio: sin nombres de archivos y sin\n"
        "  palabras de informatica. Si hay que nombrar algo, se traduce.\n" % ", ".join(fuera[:8]))
    return 2


# ─── 3) ¿SE CONFIRMO EL OBJETIVO ANTES DE CONSTRUIR? (PreToolUse Write) ────────
SEMAFORO = os.path.join(AQUI, "memoria", ".objetivo_confirmado")


def _semaforo():
    """La ruta del semaforo. Se puede desviar SOLO para que la vigia pueda probar el caso
    'Julio todavia no ha dicho que si' sin borrar el semaforo de verdad."""
    return os.environ.get("INGENIERO_SEMAFORO_TEST") or SEMAFORO


def construir():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (autorizar-off)
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = str((data.get("tool_input") or {}).get("file_path") or "")
    if not fp or os.path.exists(fp):
        return 0                      # solo vigila la creacion de cosas NUEVAS
    if os.path.splitext(fp)[1].lower() not in (".py", ".html", ".js"):
        return 0
    sem = _semaforo()
    if os.path.exists(sem):
        try:
            if time.time() - os.path.getmtime(sem) < 3 * 3600:
                return 0
        except Exception:
            return 0
    veces = _bloqueos_seguidos()
    if veces >= TOPE_BLOQUEOS:
        _apuntar_bloqueo(0)
        return 0
    _apuntar_bloqueo(veces + 1)
    sys.stderr.write(
        "BLOQUEADO: vas a CONSTRUIR algo nuevo sin haber confirmado el objetivo con Julio.\n"
        "  LEY DURA del protocolo (2026-07-28): antes de construir NADA nuevo se le repite con\n"
        "  palabras propias EL RESULTADO que el quiere y se ESPERA su 'si'.\n\n"
        "  Hazlo asi: dile en UNA frase que va a conseguir el, no que vas a programar tu.\n"
        "  Cuando el diga que si:\n"
        "     cd C:\\Ingeniero_VUC; python ingeniero.py objetivo-confirmado\n")
    return 2


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "prompt"
    sys.exit({"prompt": prompt, "salida": salida, "construir": construir}.get(q, prompt)())
