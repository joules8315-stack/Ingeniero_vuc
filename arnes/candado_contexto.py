#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_contexto.py — NO SEGUIR A CIEGAS TRAS PERDER EL HILO (hook PostCompact).

Julio: "que cuando pierda el contexto no continue, sino que instruya sobre que hacer para
continuar... que no perdera contexto y comenzara a decir incoherencias".

EL PROBLEMA QUE RESUELVE: cuando la conversacion se resume, Claude pierde el detalle pero
SIGUE HABLANDO como si lo tuviera. Ahi empiezan las incoherencias: se inventa lo que se decidio,
repite trabajo hecho, o contradice algo acordado hace media hora. Antes de hoy, nada lo paraba.

COMO SE BLINDA: al perder contexto se deja una MARCA en disco. Mientras esa marca exista,
los candados de lectura y edicion BLOQUEAN todo. La marca solo se quita de una forma:
**leyendo el archivo `memoria/AL_VOLVER.md`**, que dice donde ibamos. Es decir, el propio acto
de recuperar el contexto es lo que desbloquea. No hay atajo.

  PreCompact  (modo_ingeniero.py compactar) -> guarda AL_VOLVER.md ANTES de perder nada
  PostCompact (este)                        -> pone la marca de "vengo de perder contexto"
  Al leer AL_VOLVER.md                      -> se quita la marca y se sigue
"""
import json, os, sys, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(AQUI, "memoria", ".contexto_perdido")


def _marca():
    """La marca de verdad, o una de prueba.

    Ley 23: la marca era un archivo COMPARTIDO. Una comprobacion la ponia y otra, corriendo a la
    vez, se la encontraba puesta y se ponia roja sin que nada estuviera roto: el candado de
    edicion bloqueaba un contrato que debe poder escribirse siempre. Sola, verde; en tanda, roja.
    Fallo real 2026-08-21, el mismo patron que ya se curo en la memoria y en los apagones."""
    return os.environ.get("INGENIERO_CONTEXTO_TEST") or MARCA
AL_VOLVER = os.path.join(AQUI, "memoria", "AL_VOLVER.md")


def poner_marca(motivo="la conversacion se resumio"):
    os.makedirs(os.path.dirname(_marca()), exist_ok=True)
    open(_marca(), "w", encoding="utf-8").write(
        json.dumps({"cuando": datetime.datetime.now().isoformat(), "motivo": motivo},
                   ensure_ascii=False))


def hay_marca():
    return os.path.exists(_marca())


def quitar_marca():
    try:
        os.remove(_marca())
        return True
    except Exception:
        return False


def aviso():
    """El texto que ve quien intenta seguir a ciegas."""
    return (
        "BLOQUEADO: SE PERDIO EL CONTEXTO Y NO SE SIGUE A CIEGAS\n"
        "  La conversacion se resumio. Lo que creas recordar del detalle puede ser inventado,\n"
        "  y ahi es donde empiezan las incoherencias.\n\n"
        "  Para seguir, UNA cosa (y es barata):\n"
        f"     lee  {AL_VOLVER}\n"
        "  Ese archivo dice en que proyecto ibamos, cual era el problema, que material estaba\n"
        "  permitido y si hay una pregunta de Julio sin contestar. Al leerlo, se desbloquea solo.\n\n"
        "  Si no basta, dile a Julio en palabras simples:\n"
        '     "Perdi el hilo. Para seguir al 100% refresca la sesion y dime otra vez el problema\n'
        '      en una frase. Todo lo trabajado esta guardado, no se perdio nada."\n')


def main():
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    poner_marca()
    print(json.dumps({
        "systemMessage": "Contexto perdido: bloqueado hasta leer memoria/AL_VOLVER.md",
        "additionalContext": aviso(),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    if "--estado" in sys.argv:
        print("marca de contexto perdido:", "SI" if hay_marca() else "no")
        sys.exit(0)
    if "--quitar" in sys.argv:
        print("marca quitada" if quitar_marca() else "no habia marca")
        sys.exit(0)
    sys.exit(main())
