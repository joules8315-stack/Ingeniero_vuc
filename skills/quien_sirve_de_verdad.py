# -*- coding: utf-8 -*-
"""HABILIDAD — QUIEN SIRVE DE VERDAD. Sin gastar ni una llamada a ninguna IA.

PIEZA 2 del plan aprobado por Julio el 2026-09-06, mejorada al ejecutarla.

EL PLAN DECIA: inventar una prueba nueva por tipo de trabajo y pasarsela a cada cerebro.
LO QUE SE DESCUBRIO AL EJECUTAR: no hace falta gastar ni una llamada. **El sistema ya cuenta
solo, en cada trabajo real, cuantas veces llamo a cada cerebro y cuantas fallo.** Eso es
trabajo REAL, no una prueba de laboratorio, que es justo lo que Julio pidio.

LO QUE DESTAPO AL ESTRENARSE (2026-09-06):
    DeepSeek (se paga) : 188 llamadas,  0 fallos    ->   0 %
    Groq 20B           :  94 llamadas, 29 fallos    ->  31 %
    Groq 120B          :  84 llamadas, 39 fallos    ->  46 %
    Gemini 2.5         : 111 llamadas, 74 fallos    ->  67 %
    Gemini 3 preview   :  81 llamadas, 69 fallos    ->  85 %
    LM Studio (tu PC)  :  34 llamadas, 32 fallos    ->  94 %
    Gemini 3.5         :  56 llamadas, 55 fallos    ->  98 %
Y el relevo, ese mismo dia, dijo "le toca a Gemini 3.5": el que falla 98 de cada 100.

Mientras tanto la tabla de "quien es bueno" (que mide una prueba de MARKETING) daba 100 % a
varios de esos. Por eso esa tabla no se puede conectar sin arreglarla antes: conectar una
mentira es peor que dejarla suelta.

Es leer dos cuadernos que ya existen y dividir: una CUENTA, no un juicio.

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/quien_sirve_de_verdad.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUOTAS = os.path.join(AQUI, "memoria", "CUOTAS.json")
CAPACIDADES = os.path.join(AQUI, "memoria", "CAPACIDADES.json")
PRECISION = os.path.join(AQUI, "memoria", "PRECISION.json")
TRABAJOS = os.path.join(AQUI, "memoria", "TRABAJOS_DEL_EQUIPO.log")

DE_PAGO = {"deepseek"}


def _leer(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _uso():
    """De CUOTAS.json: cuantas veces se llamo a cada cerebro y cuantas fallo. Se cuenta solo."""
    d = _leer(CUOTAS)
    g = d.get("gasto") if isinstance(d.get("gasto"), dict) else d
    salida = {}
    for quien, v in (g.items() if isinstance(g, dict) else []):
        if not isinstance(v, dict):
            continue
        llamadas = v.get("llamadas") or v.get("usos") or v.get("total") or 0
        fallos = v.get("fallos") or v.get("errores") or 0
        try:
            llamadas, fallos = int(llamadas), int(fallos)
        except Exception:
            continue
        if llamadas:
            salida[quien] = {"llamadas": llamadas, "fallos": fallos,
                             "fallo_pct": round(fallos * 100.0 / llamadas, 1),
                             "mayor_ok": int(v.get("mayor_ok") or 0)}
    return salida


def _escrituras_reales():
    """Del registro del equipo: quien ESCRIBIO en trabajo real y como acabo."""
    if not os.path.exists(TRABAJOS):
        return {}
    salida = {}
    with open(TRABAJOS, encoding="utf-8", errors="ignore") as f:
        for ln in f:
            p = [x.strip() for x in ln.split("|")]
            if len(p) < 5:
                continue
            archivos = p[4]
            # practica = toca archivos que no existen en el disco
            nombres = [a.strip() for a in archivos.split(",") if a.strip()]
            real = False
            for n in nombres:
                for base in ("", "cuerpo", "arnes", "cerebro", "vigias", "skills"):
                    if os.path.exists(os.path.join(AQUI, base, n)):
                        real = True
                        break
                if real:
                    break
            if not real:
                continue
            quien = p[1].replace("escribio", "").strip() or "(nadie)"
            e = salida.setdefault(quien, {"escribio": 0, "aprobado": 0})
            e["escribio"] += 1
            if "APROBADO" in p[3]:
                e["aprobado"] += 1
    return salida


def medir():
    uso, escrib = _uso(), _escrituras_reales()
    cap, prec = _leer(CAPACIDADES), _leer(PRECISION)
    quienes = sorted(set(uso) | set(escrib) | set(cap))
    tabla = []
    for q in quienes:
        u = uso.get(q, {})
        e = escrib.get(q, {})
        p = prec.get(q, {})
        tabla.append({
            "quien": q,
            "de_pago": q in DE_PAGO,
            "llamadas": u.get("llamadas", 0),
            "fallo_pct": u.get("fallo_pct"),
            "aguanta": (cap.get(q) or {}).get("max", 0),
            "escribio_real": e.get("escribio", 0),
            "aprobado_real": e.get("aprobado", 0),
            "dice_la_tabla_vieja": p.get("porcentaje"),
        })
    return sorted(tabla, key=lambda x: (x["fallo_pct"] is None, x["fallo_pct"] or 0))


def informe(t=None):
    t = t or medir()
    L = ["QUIEN SIRVE DE VERDAD — contado del trabajo real, sin gastar ninguna llamada",
         "=" * 78,
         "  %-22s %8s %8s %9s %9s %9s" % ("cerebro", "llamadas", "fallo%", "escribio",
                                          "aprobado", "aguanta"),
         "  " + "-" * 74]
    for r in t:
        marca = " (SE PAGA)" if r["de_pago"] else ""
        L.append("  %-22s %8d %7s%% %9d %9d %9d%s"
                 % (r["quien"], r["llamadas"],
                    "?" if r["fallo_pct"] is None else r["fallo_pct"],
                    r["escribio_real"], r["aprobado_real"], r["aguanta"], marca))
    L += ["", "LO QUE DICE LA TABLA VIEJA (la que mide MARKETING, no reparar codigo):"]
    for r in t:
        if r["dice_la_tabla_vieja"] is not None:
            L.append("  %-22s dice %s%%   pero falla el %s%% de las llamadas reales"
                     % (r["quien"], r["dice_la_tabla_vieja"],
                        "?" if r["fallo_pct"] is None else r["fallo_pct"]))
    L += ["",
          "REGLA DE REPARTO (CONTRATO_MEDIR_A_LOS_GRATIS.md):",
          "  - a los gratis, solo trabajo que una vigia pueda juzgar despues",
          "  - el 'quedo bien' NO lo firma un cerebro: lo firma la vigia",
          "  - antes de mandarle algo a uno que falla mucho, se mira esta tabla"]
    peores = [r for r in t if (r["fallo_pct"] or 0) >= 80 and not r["de_pago"]]
    if peores:
        L += ["", "AVISO: estos fallan 8 de cada 10 veces o mas. Mandarles trabajo es tirar tiempo:"]
        for r in peores:
            L.append("   %-22s %s%% de fallo" % (r["quien"], r["fallo_pct"]))
    return "\n".join(L)


def tiene_veredicto(ruta):
    """Devuelve True solo si el documento trae veredicto del equipo.

    Un documento trae veredicto cuando en su texto aparecen las dos palabras
    APROBADO y EQUIPO, sin distinguir mayusculas de minusculas. Si falta una
    de las dos, no trae veredicto. Nunca revienta: ante la duda, False.
    """
    if not ruta:
        return False
    try:
        if not os.path.isfile(ruta):
            return False
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            texto = f.read()
    except Exception:
        return False
    texto = texto.upper()
    return "APROBADO" in texto and "EQUIPO" in texto


if __name__ == "__main__":
    sys.stdout.write(informe() + "\n")
