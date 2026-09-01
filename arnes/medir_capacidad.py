#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/medir_capacidad.py — MIDE la CAPACIDAD REAL de cada cerebro (cuanto aguanta).

Julio, 2026-08-21: "la idea es ver cual es la verdadera capacidad de cada modelo, legislar y
en ese orden asignar las tareas. Estamos todos en las versiones GRATIS."

La documentacion dice contextos enormes (Groq 131k, Gemini 1M, DeepSeek 64k), pero Claude midio
que los gratis se caen ~21k letras. Esta herramienta resuelve la contradiccion con datos REALES:
le manda a cada cerebro un encargo que crece hasta que falla, y apunta el mas grande que contesto.

    python arnes/medir_capacidad.py             -> mide todos los disponibles
    python arnes/medir_capacidad.py groq gemini  -> solo esos

Guarda el resultado en memoria/CAPACIDADES.json, que es lo que de verdad usa cuotas.rankear.
"""
import os, sys, json, time, threading

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cuerpo import obrero, cuotas   # noqa: E402

SIZES = [4000, 8000, 12000, 16000, 20000, 26000, 30000, 40000, 60000, 80000]
TOPE_SEG = 180          # mas tiempo de espera: se sospecha LENTITUD, no capacidad
INTENTOS = 3            # robustez: cada tamano se prueba varias veces, no una sola
BASE = "Responde SOLO con la palabra OK. Relleno inofensivo para medir cuanto aguantas: "
PAD = " nada de datos, solo relleno inofensivo y neutral "

TRABAJO_PRUEBA = """Abajo hay una funcion con un fallo. Suma los numeros de una lista, pero empieza a contar desde
el segundo en vez de desde el primero, asi que siempre se deja uno fuera.

def suma(numeros):
    total = 0
    for n in numeros[1:]:
        total = total + n
    return total

Contesta SOLO con la linea corregida, sin explicar nada."""

RESPUESTA_CORRECTA = "for n in numeros:"


def _prompt_de(tamano):
    trabajo = TRABAJO_PRUEBA
    if len(trabajo) >= tamano:
        return trabajo
    p = trabajo + BASE
    while len(p) < tamano:
        p += PAD
    return p[:tamano]


def _pedirle(quien, prompt):
    """Llama directo al cerebro indicado. Devuelve el texto o lanza una excepcion."""
    c, _cf = obrero.prestar_cerebro()
    vel = {}
    try:
        for ln in open(os.path.join(AQUI, "arnes", "velocidad.config"), encoding="utf-8"):
            ln = ln.strip()
            if ln and "=" in ln and not ln.startswith("#"):
                k, v = ln.split("=", 1)
                vel[k.strip()] = v.strip()
    except Exception:
        pass
    modelos = {"groq": vel.get("modelo_groq"), "groq20b": vel.get("modelo_groq20b"),
               "gemini": vel.get("modelo_gemini"), "gemini2": vel.get("modelo_gemini2"),
               "gemini3": vel.get("modelo_gemini3"), "deepseek": vel.get("modelo_deepseek")}
    if quien == "local":
        return obrero.preguntar_local(prompt, 0.2)
    if quien.startswith("deepseek"):
        return obrero._deepseek_directo(prompt, 0.2, modelos.get(quien))
    if quien.startswith("gemini"):
        return obrero._gemini_directo(prompt, 0.2, modelos.get(quien))
    return c._preguntar_groq(prompt, modelos.get(quien), 0.2)


def _tipo_de_fallo(err):
    """Distingue CAPACIDAD (rechaza el tamano) de RATE (cuota) de OTRO. Es la clave: si es
    lentitud y no capacidad, el arreglo es ampliar el tope de espera, no dividir ni saltar."""
    e = str(err).lower()
    if any(k in e for k in ("429", "rate limit", "rate_limit", "quota", "insufficient balance",
                            "agotado", "too many requests")):
        return "RATE"
    if any(k in e for k in ("context", "length", "too large", "too long", "max_tokens",
                            "prompt is too", "exceed", "large prompt", "400")):
        return "CAPACIDAD"
    return "OTRO"


def medir(quien):
    """Cuanto aguanta y con QUE ROBUSTEZ. Prueba cada tamano INTENTOS veces, aguantando hasta
    TOPE_SEG. Devuelve (mejor, tipo, detalle). tipo distingue LENTO / CAPACIDAD / RATE / VACIO
    para saber si el arreglo es ampliar espera o dividir."""
    mejor, tipo, detalle = 0, "OK", {}
    for tamano in SIZES:
        aciertos, primer_fallo = 0, None
        for _ in range(INTENTOS):
            r = {}
            def _run():
                try:
                    r["txt"] = _pedirle(quien, _prompt_de(tamano))
                except Exception as e:
                    r["err"] = str(e)
            th = threading.Thread(target=_run)
            th.start()
            th.join(TOPE_SEG)
            if th.is_alive():
                primer_fallo = primer_fallo or ("LENTO (>%ds)" % TOPE_SEG)
                continue
            if "err" in r:
                primer_fallo = primer_fallo or _tipo_de_fallo(r["err"])
                continue
            txt = (r.get("txt") or "").strip()
            if RESPUESTA_CORRECTA.strip() not in txt:
                primer_fallo = primer_fallo or "VACIO"
                continue
            aciertos += 1
        detalle[tamano] = "%d/%d" % (aciertos, INTENTOS)
        if aciertos == INTENTOS:
            mejor = tamano
        else:
            if tipo == "OK":
                tipo = primer_fallo or "PARCIAL"
            if aciertos == 0:       # ni uno: aqui se rompe de verdad
                break
    return mejor, tipo, detalle


def promedio():
    """Promedio real de las instrucciones (los paquetes ya generados), para medir con cifras
    realistas y no con tamaños inventados."""
    import glob
    pk = glob.glob(os.path.join(AQUI, "memoria", "paquetes", "*.md"))
    if not pk:
        print("NO hay paquetes reales para promediar.")
        print("Genera uno primero: python ingeniero.py trabaja <proyecto> \"<problema>\"")
        return 1
    tam = sorted(os.path.getsize(p) for p in pk)
    n = len(tam)
    print("INSTRUCCIONES REALES (%d paquetes):" % n)
    print("  minimo   : %d letras" % tam[0])
    print("  maximo   : %d letras" % tam[-1])
    print("  promedio : %.0f letras" % (sum(tam) / n))
    print("  mediana  : %.0f letras" % (tam[n // 2] if n % 2 else (tam[n // 2 - 1] + tam[n // 2]) / 2))
    print("  (el trabajo en equipo suma el paquete + los roles, ~1.5x el paquete)")
    return 0


def probar(quien, tamano):
    """Prueba UN solo tamano en este cerebro, INTENTOS veces, y dice cuantas acerto.
    Sirve para confirmar un limite puntual (ej: 'probar local 40000')."""
    if quien not in cuotas.ORDEN:
        print("NO_ENCONTRADO: '%s' no esta en la fila" % quien)
        return 1
    if quien == "local" and tamano > obrero.TOPE_LOCAL:
        print("AVISO: %s tiene tope interno de %d; probar mas arriba fallara antes de llamar"
              % (cuotas.APODO[quien], obrero.TOPE_LOCAL))
    aciertos = 0
    fallos = []
    for _ in range(INTENTOS):
        r = {}
        def _run():
            try:
                r["txt"] = _pedirle(quien, _prompt_de(tamano))
            except Exception as e:
                r["err"] = str(e)
        th = threading.Thread(target=_run)
        th.start()
        th.join(TOPE_SEG)
        if th.is_alive():
            fallos.append("LENTO (>%ds)" % TOPE_SEG)
        elif "err" in r:
            fallos.append(_tipo_de_fallo(r["err"]))
        elif "OK" not in (r.get("txt") or "").strip():
            fallos.append("VACIO")
        else:
            aciertos += 1
    print("%s a %d letras: %d/%d aciertos" % (cuotas.APODO[quien], tamano, aciertos, INTENTOS))
    if fallos:
        print("  fallos: " + "; ".join(set(fallos)))
    return 0 if aciertos == INTENTOS else 2


def main():
    blancos = sys.argv[1:] or cuotas.ORDEN
    if "promedio" in blancos:
        return promedio()
    if blancos and blancos[0] == "probar" and len(blancos) >= 3:
        return probar(blancos[1], int(blancos[2]))
    ruta = os.path.join(AQUI, "memoria", "CAPACIDADES.json")
    datos = {}
    if os.path.exists(ruta):
        try:
            datos = json.load(open(ruta, encoding="utf-8"))
        except Exception:
            datos = {}
    L = ["MEDICION DE CAPACIDAD REAL (letras) y ROBUSTEZ (aciertos/3 por tamano):"]
    for quien in blancos:
        if quien not in cuotas.ORDEN:
            print("NO_ENCONTRADO: '%s' no esta en la fila" % quien)
            continue
        print("  midiendo %s ..." % cuotas.APODO[quien], flush=True)
        mejor, tipo, detalle = medir(quien)
        datos[quien] = {"max": mejor, "tipo": tipo, "detalle": detalle}
        if tipo == "OK":
            estado = "aguanta todo lo probado (~%d letras)" % mejor
        elif tipo == "LENTO":
            estado = ("aguanta ~%d letras y luego LENTO (>%ds): se RESUELVE AMPLIANDO "
                      "el tope de espera" % (mejor, TOPE_SEG))
        elif tipo == "CAPACIDAD":
            estado = "aguanta ~%d letras y RECHAZA el tamano: pedazo mas chico o saltar" % mejor
        elif tipo == "RATE":
            estado = "se agoto la cuota (rate limit): se espera a que se reponga"
        else:
            estado = "aguanta ~%d letras y fallo raro: %s" % (mejor, tipo)
        L.append("  %-18s %s" % (cuotas.APODO[quien], estado))
        L.append("           robustez: " + " | ".join("%d:%s" % (s, d) for s, d in detalle.items()))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    json.dump(datos, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(L))
    print("\nGuardado en " + ruta + "  (es lo que usa cuotas.rankear)")
    print("Para el promedio de instrucciones reales: python arnes/medir_capacidad.py promedio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
