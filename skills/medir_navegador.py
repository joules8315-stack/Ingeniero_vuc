# -*- coding: utf-8 -*-
"""Mide, con un navegador de verdad, que hace el MVP al abrirse: cuantas peticiones dispara,
cuanto tarda cada una y cuanto se espera en total. NO toca nada: solo mira y apunta.

Se hizo para medir la lentitud que sufre Julio, sin suposiciones (2026-08-20).

OJO — fallo ya cometido: pedir `networkidle` NUNCA termina, porque la pantalla consulta cada
12 segundos y por tanto la red nunca se queda quieta. Aqui se espera a que cargue y se observa
una ventana de tiempo fija.
"""
import sys, time
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/"
OBSERVAR = 12          # segundos mirando despues de que cargue
peticiones = []


def apuntar(resp):
    try:
        t = resp.request.timing
        dur = (t["responseEnd"] - t["startTime"]) if t and t.get("responseEnd", -1) > 0 else -1
    except Exception:
        dur = -1
    peticiones.append((resp.request.method, resp.url, resp.status, dur))


if __name__ == "__main__":
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        pag = nav.new_page()
        pag.on("response", apuntar)
        t0 = time.time()
        pag.goto(URL, wait_until="domcontentloaded", timeout=45000)
        carga = time.time() - t0
        try:
            pag.wait_for_load_state("load", timeout=20000)
        except Exception:
            pass
        hasta_load = time.time() - t0
        n_al_cargar = len(peticiones)
        time.sleep(OBSERVAR)          # se mira que hace la pantalla estando quieta
        titulo = (pag.title() or "")[:44]
        try:
            visible = pag.inner_text("body")[:160].replace("\n", " ")
        except Exception:
            visible = ""
        nav.close()

    print("=== ABRIR EL PROGRAMA (navegador de verdad) ===")
    print("  pantalla que sale : %s" % titulo)
    print("  primer dibujo     : %.2f s" % carga)
    print("  carga completa    : %.2f s" % hasta_load)
    print("  peticiones al cargar        : %d" % n_al_cargar)
    print("  peticiones EXTRA en %d s quieto: %d" % (OBSERVAR, len(peticiones) - n_al_cargar))
    print()
    lentas = sorted([x for x in peticiones if x[3] > 0], key=lambda x: -x[3])
    if lentas:
        print("  LAS QUE MAS TARDAN:")
        for met, url, cod, dur in lentas[:10]:
            corta = url.split("8000")[-1] if "8000" in url else url
            print("    %-5s %-44s %s %7.0f ms" % (met, corta[:44], cod, dur))
    suma = sum(d for _, _, _, d in peticiones if d > 0)
    print()
    print("  suma de todas las esperas: %.0f ms" % suma)
    if visible:
        print()
        print("  lo que se ve en pantalla: %s" % visible)
