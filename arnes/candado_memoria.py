#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_memoria.py — EL FALLO TE AVISA ANTES, NO DESPUES.

Julio, 2026-08-21: "Verifica que se esten guardando los errores y que estes aprendiendo de ellos,
no veo que te llegue ningun paquete recordandote el error... otra vez estas confiando de tu
memoria y es justo lo que debemos combatir."

LO QUE DESCUBRIO: habia 29 fallos guardados y NINGUNO avisaba jamas. La memoria de fallos solo se
consultaba al pedir un paquete, y solo si las palabras del problema coincidian. Pero hay fallos
que no son "un problema con nombre" sino **una accion**: escribir codigo desde la terminal, por
ejemplo. Ese no coincidia con nada, y por eso se repitio SEIS veces en un dia.

LA PRUEBA MAS CLARA: el apunte de ese fallo decia
    "NO VOLVER A: meter codigo con \\n o rutas con \\a dentro de un heredoc"
y **el propio apunte estaba corrompido por el mismo fallo que describia.**

LA REGLA: guardar un fallo no es aprender. Aprender es que el fallo te FRENE la proxima vez.
Por eso cada fallo puede declarar un DISPARADOR: la accion que lo revive. Antes de cada accion
se mira si hay algun fallo con ese disparador, y si lo hay, se recuerda ANTES de cometerlo.

No estorba: solo avisa de lo que viene al caso (si avisa de todo, se vuelve ruido y se ignora),
y siempre dice QUE HACER en su lugar, no solo que esta mal.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)


def _texto_de_la_accion(data):
    """Que se va a hacer, en texto, para poder compararlo con los disparadores."""
    herr = str(data.get("tool_name") or "")
    ti = data.get("tool_input") or {}
    partes = [herr]
    for clave in ("command", "file_path", "old_string", "new_string", "content",
                  "pattern", "path", "prompt"):
        v = ti.get(clave)
        if isinstance(v, str):
            partes.append(v[:2000])
    return "\n".join(partes)


def revisar(texto):
    """Los fallos ya vividos que esta accion puede revivir."""
    try:
        from cuerpo import fallos
        guardados = fallos._leer()
    except Exception:
        return []
    salen = []
    for f in guardados:
        disp = (f.get("disparador") or "").strip()
        if not disp:
            continue
        try:
            if re.search(disp, texto, re.I | re.S):
                salen.append(f)
        except re.error:
            continue
    return salen[:3]


def main():
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    texto = _texto_de_la_accion(data)
    if not texto:
        return 0
    revividos = revisar(texto)
    if not revividos:
        return 0

    partes = ["ESTO YA TE PASO. No lo repitas:", ""]
    for f in revividos:
        veces = f.get("veces", 1)
        cuantas = (" (te ha pasado %d veces)" % veces) if veces > 1 else ""
        partes.append("  * %s%s" % (f["que_paso"][:130], cuantas))
        partes.append("    por que paso : %s" % f["causa_raiz"][:130])
        partes.append("    HAZLO ASI    : %s" % f["cura"][:150])
        partes.append("    NO VUELVAS A : %s" % f["no_volver_a"][:130])
        partes.append("")
    partes.append("  Guardar un fallo no es aprender. Esto es el aviso ANTES de cometerlo otra vez.")
    sys.stderr.write("\n".join(partes) + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
