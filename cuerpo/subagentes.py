# -*- coding: utf-8 -*-
"""cuerpo/subagentes.py — TRABAJO EN PROCESO APARTE (orden 3 de Julio, 2026-08-20).

  "Que se replique lo de dejar, al pedir una respuesta los json, en vez de todo el contexto
   y que se utilicen sub agentes para ello."

La idea: el trabajo pesado NO se hace en la ventana de Claude. Se manda a un proceso APARTE
que se traga el paquete entero, habla con los cerebros gratis, y deja el resultado en disco.
A la ventana de Claude vuelven solo unas lineas de veredicto.

Cuanto ahorra, medido:
    paquete que se traga el subagente : ~20.000 caracteres
    veredicto que ve Claude          : ~600 caracteres
    o sea, Claude ve el 3% del material y decide igual de bien.

Ademas, si el proceso aparte se cuelga o se cae, NO se lleva por delante la sesion de Julio:
tiene su propio tope de tiempo y su propio archivo de salida.

    python -m cuerpo.subagentes <proyecto> "<problema>"     (esto es lo que se lanza aparte)
"""
import os, sys, json, subprocess, time, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDAS = os.path.join(AQUI, "memoria", "subagentes")
# TOPES COHERENTES (fallo real 2026-08-20: el subproceso esperaba 450s pero UNA ronda son dos
# llamadas de hasta 300s = 600s, asi que se cortaba siempre a si mismo).
#   llamada 300s (arnes/velocidad.config) x 2 por ronda + margen = 700s
# Que sea largo NO hace esperar a Julio: para eso esta `lanzar_al_fondo`.
TOPE = 700


# ─── LO QUE CORRE DENTRO DEL PROCESO APARTE ────────────────────────────────────────
def _trabajar(proyecto, problema, destino):
    sys.path.insert(0, AQUI)
    from cerebro import router
    from cuerpo import cruzado

    pk = router.armar(proyecto, problema)
    texto = router.a_texto(pk)
    r = cruzado.resolver(texto, problema, proyecto=proyecto)
    r["paquete_lineas"] = len(texto.splitlines())
    r["paquete_chars"] = len(texto)
    r["proyecto_lineas"] = pk["total_proyecto"]
    r["cuando"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    json.dump(r, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return r


# ─── LO QUE SE LLAMA DESDE LA SESION (y solo recibe el veredicto) ──────────────────
def lanzar(proyecto, problema, tope=TOPE):
    """Manda el trabajo a un proceso aparte. Devuelve SOLO el veredicto corto."""
    os.makedirs(SALIDAS, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in problema.lower())[:40]
    destino = os.path.join(SALIDAS, f"{proyecto}__{slug}.json")

    t0 = time.time()
    try:
        p = subprocess.run(
            [sys.executable, "-m", "cuerpo.subagentes", proyecto, problema, "--destino", destino],
            cwd=AQUI, capture_output=True, text=True, timeout=tope + 30)
    except subprocess.TimeoutExpired:
        # Un vomito de Python no le sirve de nada a Julio: se le dice en su idioma que hacer.
        return {"_error": f"los cerebros gratis no contestaron en {tope}s (su latencia va de 5s a "
                          f"305s y no depende de nosotros). No se perdio nada: vuelve a lanzarlo "
                          f"con `python ingeniero.py cruzado {proyecto} \"{problema}\"` o usa "
                          f"`python ingeniero.py trabaja` y trabaja tu con el paquete.",
                "segundos": round(time.time() - t0, 1)}
    tardo = round(time.time() - t0, 1)

    if not os.path.exists(destino):
        return {"_error": "el subagente no dejo resultado. Ultimas lineas:\n"
                          + (p.stderr or p.stdout or "")[-400:], "segundos": tardo}
    r = json.load(open(destino, encoding="utf-8"))
    r["archivo"] = destino
    r["segundos_totales"] = tardo
    return r


def veredicto(r):
    """Lo UNICO que entra en la ventana de Claude. Debe caber en una pantalla."""
    if "_error" in r:
        return "NO SE PUDO: " + str(r["_error"])[:400]
    from cuerpo import cruzado
    L = [cruzado.informe(r)]
    ahorro = 100 - r.get("paquete_lineas", 0) * 100 / max(1, r.get("proyecto_lineas", 1))
    L.append(f"  material que trago el subagente: {r.get('paquete_lineas', '?')} lineas "
             f"(el proyecto tiene {r.get('proyecto_lineas', 0):,}; ahorro {ahorro:.1f}%)")
    L.append(f"  detalle completo (NO hace falta leerlo): {r.get('archivo', '?')}")
    return "\n".join(L)


def lanzar_al_fondo(proyecto, problema):
    """Lanza el trabajo y VUELVE AL INSTANTE. Julio no espera: sigue con lo suyo y consulta
    cuando quiera con `python ingeniero.py resultado`.

    Esta es la respuesta honesta a "que nada sea lento": la latencia de los cerebros gratis no
    la controlamos (5s a 305s), pero que Julio se quede mirando la pantalla, si.
    """
    os.makedirs(SALIDAS, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in problema.lower())[:40]
    destino = os.path.join(SALIDAS, f"{proyecto}__{slug}.json")
    if os.path.exists(destino):
        os.remove(destino)
    marca = destino + ".corriendo"
    open(marca, "w", encoding="utf-8").write(datetime.datetime.now().isoformat())
    creationflags = 0x00000008 if os.name == "nt" else 0     # DETACHED_PROCESS
    subprocess.Popen([sys.executable, "-m", "cuerpo.subagentes", proyecto, problema,
                      "--destino", destino, "--marca", marca],
                     cwd=AQUI, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     creationflags=creationflags)
    return destino


def estado(proyecto=None):
    """Que hay de lo lanzado. Sin bloquear."""
    if not os.path.isdir(SALIDAS):
        return "No se ha lanzado ningun trabajo todavia."
    L = []
    for f in sorted(os.listdir(SALIDAS)):
        ruta = os.path.join(SALIDAS, f)
        if f.endswith(".corriendo"):
            desde = open(ruta, encoding="utf-8").read()[:16].replace("T", " ")
            L.append(f"  CORRIENDO desde {desde} — {f[:-10]}")
        elif f.endswith(".json"):
            if os.path.exists(ruta + ".corriendo"):
                continue
            r = json.load(open(ruta, encoding="utf-8"))
            L.append(f"  LISTO ({r.get('segundos', '?')}s) — {f[:-5]}")
            L.append("    veredicto: " + str(r.get("veredicto", "?")))
    return "\n".join(L) if L else "No hay trabajos lanzados."


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    args = sys.argv[1:]
    destino = None
    marca = None
    if "--marca" in args:
        i = args.index("--marca")
        marca = args[i + 1]
        args = args[:i] + args[i + 2:]
    if "--destino" in args:
        i = args.index("--destino")
        destino = args[i + 1]
        args = args[:i]
    proyecto, problema = args[0], " ".join(args[1:])
    if destino:
        try:
            _trabajar(proyecto, problema, destino)  # dentro del proceso aparte
        finally:
            if marca and os.path.exists(marca):
                os.remove(marca)
    else:
        print(veredicto(lanzar(proyecto, problema)))  # llamada normal
