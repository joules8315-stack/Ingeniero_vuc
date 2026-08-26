#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_preguntar.py — NO SE LE PREGUNTA A JULIO LO QUE YA ESCRIBIO.

Julio, 2026-08-20, despues de que se le preguntara TRES veces cosas que estaban en su contrato:
"Busca el contrato que dice, estas muy estupida. Fuy claro..."

LO QUE PASO, EXACTO:
  · Se pregunto "¿que es el complemento?" -> estaba en OBJETIVO_MVP.md linea 2975.
  · Se pregunto por el fallo de Render sin red -> estaba en la 2983, listado como fallo conocido.
  · Se pregunto por el tope de fotos -> estaba en la 802, con el mensaje exacto.
Julio tuvo que explicar por chat lo que el mismo ya habia dejado escrito. Eso es hacerle perder
el tiempo, y es justo lo contrario del fin del Ingeniero ("que Julio no repita").

POR QUE PASO, y esta es la leccion de verdad:
`cuerpo/dudas.py` YA existia y hace exactamente esto. Estaba probado y funcionando. **Pero era
un comando que habia que acordarse de llamar, no un candado que frena.** Lo que se ejecuta solo
se cumple; lo que depende de que alguien se acuerde, no se cumple. Por eso esto es un HOOK.

COMO FUNCIONA (PreToolUse sobre AskUserQuestion):
  1. Saca las preguntas que se le van a hacer a Julio.
  2. Las busca en sus contratos, en el codigo, en los fallos y en el estado (`cuerpo/dudas.py`).
  3. Si la respuesta YA ESTABA ESCRITA -> BLOQUEA y dice donde esta.
  4. Si no esta en ningun sitio -> deja pasar: esa pregunta si hay que hacerla.

No estorba: preguntar lo que NO esta escrito es obligatorio (Ley 16). Lo que se frena es
preguntar lo que Julio ya se molesto en escribir.
"""
import json, os, sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPE_SEGUNDOS = 25          # buscar no puede hacer esperar a Julio


def _proyecto_activo():
    """En que proyecto se esta trabajando ahora (para buscar en sus contratos)."""
    try:
        sys.path.insert(0, AQUI)
        from cuerpo import estado
        return estado.leer().get("proyecto") or None
    except Exception:
        return None


def _preguntas(data):
    """Saca el texto de las preguntas que se le iban a hacer a Julio."""
    out = []
    ti = data.get("tool_input") or {}
    for q in (ti.get("questions") or []):
        t = str(q.get("question") or "").strip()
        if t:
            out.append(t)
    return out


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (comando autorizar-off)
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    preguntas = _preguntas(data)
    if not preguntas:
        return 0

    sys.path.insert(0, AQUI)
    try:
        from cuerpo import dudas
    except Exception:
        return 0                      # si el buscador no esta, no se estorba

    proyecto = _proyecto_activo()
    ya_escritas = []
    for p in preguntas:
        try:
            r = dudas.resolver(p, proyecto)
        except Exception:
            continue
        if not r["hay_que_preguntar"]:
            fuentes = [f"{h['fuente']}: {h['donde']}" for h in r["hallado"][:2]]
            ya_escritas.append((p, fuentes))

    if not ya_escritas:
        return 0                      # ninguna estaba escrita: preguntar es lo correcto

    partes = ["BLOQUEADO: LE IBAS A PREGUNTAR A JULIO ALGO QUE EL YA ESCRIBIO\n"]
    for p, fuentes in ya_escritas:
        partes.append('  Pregunta: "%s"' % p[:150])
        for f in fuentes:
            partes.append("     -> ya esta escrito en %s" % f)
        partes.append("")
    partes.append("  Lee eso ANTES de preguntar. Hacerle repetir lo que ya dejo escrito es")
    partes.append("  justo lo contrario del fin del Ingeniero.")
    partes.append("")
    partes.append("  Si de verdad el contrato NO lo resuelve, di en que se queda corto y")
    partes.append("  pregunta lo que falta, no lo que ya esta.")
    sys.stderr.write("\n".join(partes) + "\n")
    # MEDICION (Julio, 2026-08-25): freno la pregunta que ya estaba respondida por Julio.
    try:
        import candados_medicion
        candados_medicion.cazado("preguntar")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
