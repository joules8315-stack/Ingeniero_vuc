#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/modo_ingeniero.py — EL CANDADO DEL MODO. Orden de Julio (2026-08-20):

  "que para cada instruccion, sobre cualquier proyecto, nuevo o viejo, actue SIEMPRE el ingeniero,
   que nunca asuma, que siempre pregunte... que cuando pierda el contexto no continue, sino que
   instruya sobre que hacer para continuar."

Un mismo archivo, tres puestos de guardia:
  modo_ingeniero.py prompt     -> hook UserPromptSubmit : en CADA instruccion mete el protocolo + donde ibamos
  modo_ingeniero.py sesion     -> hook SessionStart     : al abrir, dice donde ibamos
  modo_ingeniero.py compactar  -> hook PreCompact       : ANTES de perder memoria, la guarda en disco

Por que asi y no en el CLAUDE.md: la documentacion oficial dice que el CLAUDE.md es CONTEXTO
(se puede ignorar) y que "para que algo se cumpla pase lo que pase, se usa un hook". Ademas el
CLAUDE.md de un proyecto no se carga en OTRO proyecto; este hook, puesto a nivel usuario, actua
en TODOS: los de hoy y los que Julio cree manana.

DISENO PRUDENTE: estos tres puestos NO bloquean nunca (salida 0). Meten contexto y avisan.
El unico que FRENA es `read_gate.py`, que tiene salida clara. Un candado que atrapa a Julio
sin salida seria peor que el problema.
"""
import json, os, sys, glob, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

LEYES = """MODO INGENIERO (candado del arnes — no es opcional)

Julio esta construyendo programas para su empresa. Aqui NO se actua como IA suelta: se actua como
INGENIERO DE SOFTWARE con arnes. En toda instruccion, sobre cualquier proyecto:

1. NUNCA ASUMIR. Si algo no esta escrito en un contrato o en el codigo, se PREGUNTA a Julio en
   palabras simples. Antes de preguntar, se busca en los proyectos. Nunca se adivina.
2. NUNCA INVENTAR. Archivo, funcion o linea que no exista -> se escribe NO_ENCONTRADO. Jamas se
   rellena con algo que suene bien.
3. NO LEER EL PROYECTO ENTERO. Se pide el paquete minimo:
     cd C:\Ingeniero_VUC; python ingeniero.py trabaja <proyecto> "<el problema>"
   Lo que falte se PIDE con NECESITO_LEER. El candado de lectura frena lo demas.
4. EL VOLUMEN LO HACE EL CEREBRO GRATIS, no Claude. Qwen genera, Gemini audita (4 ojos), y Claude
   lee el VEREDICTO, no el volumen:  python ingeniero.py resolver <proyecto> "<problema>"
   Orden de cuotas: Qwen -> Gemini -> local -> se vuelve a Qwen en cuanto reponga.
5. NO ROMPER VECINOS. Antes de tocar se mira "A QUIEN PUEDE DANAR" del paquete.
6. VIGIA VERDE NO ES PRUEBA. La prueba es que Julio lo vea con sus ojos. Ninguna IA se autocertifica.
7. TODA MEJORA SE LEGISLA: contrato + vigia + codigo + sello. Antes de crear, se busca si ya existe
   (no repetidera).
8. A JULIO SE LE HABLA SIMPLE, sin jerga, y el comando siempre listo para PowerShell (`;`, no `&&`).
9. NO IRSE POR OTRO LADO. Se hace lo que Julio pidio; si aparece algo mejor, se le dice y se le
   pregunta. No se cambia el rumbo por cuenta propia.
10. SI SE PIERDE EL CONTEXTO, NO SE SIGUE A CIEGAS. Se para y se dice que hacer para retomar."""


def _estado():
    try:
        from cuerpo import estado
        return estado.leer(), estado.texto()
    except Exception:
        return {}, ""


def _paquete_vigente(horas=8):
    try:
        ps = sorted(glob.glob(os.path.join(AQUI, "memoria", "paquetes", "*.md")),
                    key=os.path.getmtime, reverse=True)
        if ps and (time.time() - os.path.getmtime(ps[0])) < horas * 3600:
            return ps[0]
    except Exception:
        pass
    return ""


def _via():
    """Ley 14: lo primero de lo primero. Si se esta en la copia equivocada, todo lo demas sobra."""
    try:
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import via_canonica
        if via_canonica.esta_limpio():
            return ""
        return via_canonica.texto() + "\n*** NO SE TOCA CODIGO hasta arreglar esto. ***"
    except Exception:
        return ""


def _donde_ibamos():
    d, txt = _estado()
    L = []
    via = _via()
    if via:
        L.append(via)
        L.append("")
    if txt:
        L.append(txt)
    pk = _paquete_vigente()
    if pk:
        L.append(f"PAQUETE VIGENTE: {os.path.basename(pk)}")
        L.append("  -> se trabaja SOLO con ese paquete. Nada de abrir el proyecto.")
    else:
        L.append("NO HAY PAQUETE VIGENTE.")
        L.append('  -> antes de tocar codigo: python ingeniero.py trabaja <proyecto> "<problema>"')
    if d.get("decision_pendiente"):
        L.append("")
        L.append(f"*** PARADO: PREGUNTA SIN RESPONDER -> {d['decision_pendiente']}")
        L.append("*** No se avanza hasta que Julio conteste. Recuerdaselo antes que nada.")
    return "\n".join(L)


def _salida(texto, mensaje=None):
    out = {"hookSpecificOutput": {"hookEventName": "", "additionalContext": texto},
           "additionalContext": texto}
    if mensaje:
        out["systemMessage"] = mensaje
    print(json.dumps(out, ensure_ascii=False))
    return 0


def prompt():
    """En CADA instruccion de Julio: el protocolo + donde ibamos."""
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    return _salida(LEYES + "\n\n" + _donde_ibamos())


def sesion():
    """Al abrir la sesion: donde ibamos, para no arrancar de cero."""
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    return _salida(LEYES + "\n\n" + _donde_ibamos(),
                   "Modo Ingeniero activo — el estado se leyo de memoria/ESTADO.json")


def compactar():
    """ANTES de que la conversacion se resuma (ahi se pierde contexto): se guarda todo en disco
    y se deja escrito que hacer al volver. Esto es la orden 1d de Julio."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    d, _ = _estado()
    aviso = os.path.join(AQUI, "memoria", "AL_VOLVER.md")
    os.makedirs(os.path.dirname(aviso), exist_ok=True)
    pk = _paquete_vigente()
    with open(aviso, "w", encoding="utf-8") as f:
        f.write("# AL VOLVER — se acaba de perder contexto (la conversacion se resumio)\n\n")
        f.write("**NO SIGAS A CIEGAS.** Antes de hacer nada:\n\n")
        f.write("```powershell\ncd C:\Ingeniero_VUC; python ingeniero.py arranca\n```\n\n")
        f.write("## Donde ibamos\n\n```\n" + _donde_ibamos() + "\n```\n\n")
        if pk:
            f.write(f"## El material permitido sigue siendo\n\n`{pk}`\n\n")
            f.write("Vuelve a leer ESE paquete. No vuelvas a explorar el proyecto: ya se pago por eso.\n\n")
        else:
            f.write('## No habia paquete\n\nPide uno: `python ingeniero.py trabaja <proyecto> "<problema>"`\n\n')
        if d.get("decision_pendiente"):
            f.write(f"## PARADO\n\nHay una pregunta sin responder para Julio:\n\n> {d['decision_pendiente']}\n\n")
        f.write("## Si sigues perdido\n\nDile a Julio, en palabras simples:\n\n"
                "> Perdi el hilo. Para seguir al 100% necesito que refresques la sesion "
                "(cierra y abre, o escribe /clear) y me digas otra vez el problema en una frase. "
                "Todo lo trabajado esta guardado, no se perdio nada.\n")
    print(json.dumps({
        "systemMessage": "Contexto guardado en memoria/AL_VOLVER.md — al volver, leelo ANTES de seguir.",
        "additionalContext": ("SE ESTA PERDIENDO CONTEXTO. Todo quedo guardado en "
                              f"{aviso}. Al retomar: NO sigas a ciegas, lee ese archivo y "
                              "corre `python ingeniero.py arranca`.\n\n" + _donde_ibamos()),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    # INTERRUPTOR DE EMERGENCIA: INGENIERO_OFF=1 apaga el modo sin desinstalar nada.
    if os.environ.get("INGENIERO_OFF", "").strip():
        sys.exit(0)
    q = sys.argv[1] if len(sys.argv) > 1 else "prompt"
    sys.exit({"prompt": prompt, "sesion": sesion, "compactar": compactar}.get(q, prompt)())
