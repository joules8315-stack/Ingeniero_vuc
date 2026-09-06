# -*- coding: utf-8 -*-
"""HABILIDAD — CUANTOS FRENOS ACABARON SABIENDO QUIEN FALLO. Sin gastar ninguna IA.

Julio, 2026-09-05 (la ley que manda sobre todas): "Se debe hacer siempre analizar la
informacion y determinar que esta mal: la herramienta, o el razonamiento, o la
informacion recibida, o quien reparte. Se debe ver que esta fallando."

La medida buena NO es cuantos frenos hubo: bajar ese numero se consigue apagando
candados, que es justo lo contrario de lo que Julio quiere. La medida buena es
QUE PORCENTAJE de frenos acabo con un culpable identificado.

Al 2026-09-05 estaba en 2 de 13.375, o sea 0,015 por ciento.

Es contar y dividir: una cuenta, no un juicio.

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/frenos_con_culpable.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDICION = os.path.join(AQUI, "memoria", "CANDADOS_MEDICION.json")

# Los cuatro sospechosos de la ley del 2026-09-05. Siempre los mismos.
SOSPECHOSOS = ("herramienta", "razonamiento", "informacion", "reparte")


def _leer(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _numero(v):
    """De un valor que puede ser numero o caja, saca el numero."""
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, dict):
        for k in ("cazadas", "frenadas", "veces", "total", "n"):
            if isinstance(v.get(k), (int, float)):
                return int(v[k])
    return 0


def _falsos(v):
    """Los frenos en falso, que son los unicos que hoy se apuntan a mano."""
    if isinstance(v, dict):
        for k in ("falsos", "en_falso", "falsos_positivos"):
            if isinstance(v.get(k), (int, float)):
                return int(v[k])
    return 0


def medir():
    d = _leer(MEDICION)
    por_candado, total, con_culpable = {}, 0, 0
    for nombre, v in (d.items() if isinstance(d, dict) else []):
        n = _numero(v)
        f = _falsos(v)
        if n:
            por_candado[nombre] = n
            total += n
        con_culpable += f
    return {"total": total, "con_culpable": con_culpable, "por_candado": por_candado}


def informe(r=None):
    r = r or medir()
    total, culp = r["total"], r["con_culpable"]
    pct = (culp * 100.0 / total) if total else 0.0
    L = ["FRENOS Y CULPABLES — del registro, sin gastar ninguna llamada",
         "=" * 64,
         "  frenos apuntados             : %d" % total,
         "  frenos con culpable dicho    : %d" % culp,
         "  porcentaje que sirvio        : %.3f %%" % pct,
         "",
         "La medida NO es bajar los frenos (eso se logra apagando candados).",
         "La medida es que cada freno acabe diciendo cual de los cuatro fallo:",
         "  " + ", ".join(SOSPECHOSOS),
         ""]
    if r["por_candado"]:
        L.append("QUIEN FRENA MAS (los de arriba son los que hay que mirar primero):")
        for k, v in sorted(r["por_candado"].items(), key=lambda x: -x[1])[:12]:
            parte = (v * 100.0 / total) if total else 0
            L.append("  %-34s %7d   (%.1f %% de todos)" % (k, v, parte))
    if total and pct < 1:
        L += ["", "AVISO: menos del 1 por ciento de los frenos acabo con culpable.",
              "       El sistema tuvo %d oportunidades de aprender y aprovecho %d." % (total, culp)]
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe() + "\n")
