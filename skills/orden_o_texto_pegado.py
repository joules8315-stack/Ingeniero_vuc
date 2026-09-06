# -*- coding: utf-8 -*-
"""HABILIDAD — DISTINGUIR UNA ORDEN DE JULIO DE UN TEXTO PEGADO. Sin gastar ninguna IA.

Julio, 2026-09-05. Criterio que la justifica: ese dia la maquina tomo 32 frases del
texto de OTRA IA (que Julio habia pegado para pedir analisis) como si fueran ordenes
suyas, y bloqueo el cierre hasta legislarlas. Ya habia pasado antes con otro plan
pegado. Es la segunda vez, asi que se convierte en habilidad.

Julio no habla en informatica. Cuando en un trozo aparecen nombres de archivo, rutas,
codigo, tablas o titulos de documento, ese trozo NO lo escribio el: lo pego.

Es mirar la forma del texto: una cuenta, no un juicio.

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/orden_o_texto_pegado.py "<el trozo>"
"""
import re
import sys

# Señales de que el trozo viene de otra maquina o de otro documento, no de la boca de Julio.
SENALES = [
    (r"[\w/\\]+\.(?:py|js|ts|json|md|html|yml|sh)\b", "nombra un archivo"),
    (r"`[^`]+`", "trae codigo entre comillas raras"),
    (r"^\s*#{1,6}\s", "es un titulo de documento"),
    (r"^\s*\|.*\|", "es una fila de tabla"),
    (r"\*\*[^*]+\*\*", "trae letra resaltada de documento"),
    (r"\b(?:def|class|import|return|json|dict|str|None|True|False)\b", "trae palabras de codigo"),
    (r"^\s*\d+\.\d+\.", "es un punto numerado de un informe"),
    (r"https?://", "trae una direccion de internet"),
    (r"\bCI/CD\b|\blinter\b|\bAST\b|\bsession_id\b|\bunit ?test\b", "trae jerga tecnica"),
]

# Señales de que SI habla Julio: su forma de decir las cosas.
SUYAS = [
    (r"\b(?:no vuelvas|nunca mas|siempre|de una vez|hazlo|quiero que|debes|tienes que)\b",
     "manda directamente"),
    (r"\b(?:mierda|putas?|puta|carajo|hijo de)\b", "habla como habla Julio"),
    (r"\bJulio\b", "se nombra a si mismo"),
]


def juzgar(trozo):
    """Devuelve (es_orden, motivos). No adivina intenciones: mira la FORMA del texto."""
    t = trozo or ""
    pegado = [m for p, m in SENALES if re.search(p, t, re.M | re.I)]
    propias = [m for p, m in SUYAS if re.search(p, t, re.I)]
    # Si trae señales de documento y ninguna forma de hablar de Julio, es texto pegado.
    if pegado and not propias:
        return False, pegado
    if pegado and propias:
        return True, ["tiene forma de documento pero habla como Julio: se le pregunta"] + propias
    return True, propias or ["habla llano, sin nada de documento: suena a orden suya"]


def informe(trozo):
    es_orden, motivos = juzgar(trozo)
    L = ["ORDEN DE JULIO O TEXTO PEGADO", "=" * 40,
         "  trozo: " + (trozo or "")[:110],
         ""]
    if es_orden:
        L.append("VEREDICTO: parece una ORDEN DE JULIO. Se legisla.")
    else:
        L.append("VEREDICTO: parece TEXTO PEGADO de otra IA o de otro documento.")
        L.append("           NO se legisla como orden suya. Si se quiere que sea ley,")
        L.append("           lo dice Julio con sus palabras.")
    L.append("")
    L.append("POR QUE:")
    for m in motivos:
        L.append("   - " + m)
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe(" ".join(sys.argv[1:])) + "\n")
