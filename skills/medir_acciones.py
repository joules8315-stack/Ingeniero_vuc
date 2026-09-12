# -*- coding: utf-8 -*-
"""Mide, con un navegador de verdad, cuanto tarda CADA ACCION del MVP y cuantas veces
llama al servidor. Entra con las credenciales del archivo del proyecto.

NUNCA imprime la contrasena ni el correo. Solo mide.
Hecho para localizar la lentitud que sufre Julio, sin suposiciones (2026-08-20).
"""
import re, sys, time, json
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8000/"


def credenciales():
    t = open("CREDENCIALES_MVP.txt", encoding="utf-8", errors="ignore").read()
    email = re.search(r"email\s*[:=]\s*(\S+)", t, re.I)
    clave = re.search(r"password\s*[:=]\s*(\S+)", t, re.I)
    return (email.group(1) if email else ""), (clave.group(1) if clave else "")


peticiones = []


def apuntar(resp):
    try:
        t = resp.request.timing
        dur = (t["responseEnd"] - t["startTime"]) if t and t.get("responseEnd", -1) > 0 else -1
    except Exception:
        dur = -1
    peticiones.append({"metodo": resp.request.method, "url": resp.url,
                       "codigo": resp.status, "ms": dur, "t": time.time()})


def desde(marca):
    """Las peticiones disparadas despues de esa marca de tiempo."""
    return [p for p in peticiones if p["t"] >= marca]


def informe(nombre, marca, segundos):
    ps = desde(marca)
    reales = [p for p in ps if "/health" not in p["url"] and not p["url"].endswith(".svg")]
    espera = sum(p["ms"] for p in reales if p["ms"] > 0)
    print("  %-30s %6.2f s  |  %2d llamadas al servidor  |  %6.0f ms de espera"
          % (nombre, segundos, len(reales), espera))
    for p in sorted(reales, key=lambda x: -(x["ms"] or 0))[:4]:
        corta = p["url"].split("8000")[-1] if "8000" in p["url"] else p["url"]
        print("       %-5s %-46s %s %6.0f ms" % (p["metodo"], corta[:46], p["codigo"], p["ms"]))


if __name__ == "__main__":
    email, clave = credenciales()
    if not email or not clave:
        print("NO_ENCONTRADO: no se pudieron leer las credenciales del archivo")
        sys.exit(1)

    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        pag = nav.new_page()
        pag.on("response", apuntar)

        print("=== CUANTO TARDA CADA ACCION (navegador de verdad) ===")
        print()

        # 1) abrir
        m = time.time(); t0 = time.time()
        pag.goto(URL, wait_until="domcontentloaded", timeout=45000)
        pag.wait_for_timeout(1500)
        informe("abrir el programa", m, time.time() - t0)

        # 2) entrar
        try:
            pag.fill("input[type=email], #email, input[name=email]", email)
            pag.fill("input[type=password], #password, input[name=password]", clave)
        except Exception as e:
            print("  no se pudieron rellenar los campos:", str(e)[:90]); nav.close(); sys.exit(1)
        m = time.time(); t0 = time.time()
        pag.click("#loginBtn")
        try:
            pag.wait_for_selector("#loginBtn", state="hidden", timeout=45000)
        except Exception:
            pag.wait_for_timeout(6000)
        pag.wait_for_timeout(3000)
        informe("ENTRAR (login)", m, time.time() - t0)

        # 3) que se ve ahora
        try:
            visible = pag.inner_text("body")[:220].replace("\n", " ")
        except Exception:
            visible = ""
        print()
        print("  ya dentro, se ve: %s" % visible[:200])

        # 4) los botones que hay dentro (para saber que se puede medir)
        print()
        print("  BOTONES DISPONIBLES DENTRO:")
        vistos = []
        for b in pag.query_selector_all("button"):
            try:
                if b.is_visible():
                    t = (b.inner_text() or "").strip().replace("\n", " ")
                    if t and t not in vistos:
                        vistos.append(t)
            except Exception:
                pass
        for t in vistos[:18]:
            print("     -", t[:58])

        nav.close()

    json.dump(peticiones, open("MEDICION_ACCIONES.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print()
    print("  (el detalle quedo en MEDICION_ACCIONES.json)")
