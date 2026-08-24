# -*- coding: utf-8 -*-
"""PRUEBA REAL CON NAVEGADOR — cuenta las llamadas a la nube de verdad.

Julio, 2026-08-21: "que haga solo las llamadas que necesite, nada mas, en el tiempo que
necesite, para esperar respuesta."

Ley: CONTRATO_VELOCIDAD_LLAMADAS.md
La otra vigia (test_vigia_solo_las_llamadas_necesarias.py) mira el codigo. Esta ABRE UN NAVEGADOR
DE VERDAD y CUENTA las llamadas. Es la que demuestra que la reparacion sirve.

QUE COMPRUEBA
  1. Quieto en el menu 20 segundos -> CERO llamadas de reloj. (Antes eran ~100 por hora.)
  2. En la pantalla de las FOTOS 20 segundos -> SI llama, cada 5 segundos.
  3. Con la ventana escondida 15 segundos, en la pantalla de fotos -> CERO llamadas.
  4. Al guardar algo, no se vacia la libreta entera: lo que no tiene que ver se sigue recordando.

CANDADO: se niega a correr con la cuenta REAL de Julio. Solo cuenta de prueba.
NUNCA se escribe aqui una clave: se leen de las variables de Windows.

COMO SE CORRE (PowerShell). Julio pone sus datos de PRUEBA, no los reales:

    $env:FOTO_INFORME_TEST_EMAIL = "tu-correo-de-prueba"
    $s = Read-Host "Clave de la cuenta de PRUEBA (no se vera)" -AsSecureString
    $b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)
    $env:FOTO_INFORME_TEST_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto($b)
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b)
    cd "C:/Users/USER/dev/Foto_info_repo/Foto_informe--main"; python rv3_prueba_real_velocidad.py

(Las barras van del derecho a proposito: dentro del texto de Python, una barra invertida seguida
 de U se lee como un codigo raro y parte el archivo entero. Ya paso aqui, el mismo dia.
 PowerShell acepta las dos formas, asi que el comando funciona igual.)
"""
from __future__ import annotations

import json
import os
import sys
import time

BASE_URL = os.environ.get("FOTO_INFORME_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
EMAIL = os.environ.get("FOTO_INFORME_TEST_EMAIL", "").strip()
PASSWORD = os.environ.get("FOTO_INFORME_TEST_PASSWORD", "")
CUENTA_REAL_PROHIBIDA = "joules8315@gmail.com"
AUTORIZADA_POR_JULIO = True   # Julio, 2026-08-22: "eso es de prueba". Es su cuenta de pruebas.

ESPERA_ENTRAR_MS = 45000   # lo que se le da a la nube para dejarnos entrar, de sobra
QUIETO_MENU_S = 20
QUIETO_FOTOS_S = 20
ESCONDIDA_S = 15


def fin(estado, mensaje, **extra):
    print(json.dumps({"estado": estado, "mensaje": mensaje, **extra},
                     ensure_ascii=False, indent=2))
    raise SystemExit(0 if estado == "VERDE" else 1)


def _comprobar_entrada():
    if not EMAIL or not PASSWORD:
        fin("NO_SE_PUDO",
            "Faltan los datos de la cuenta de PRUEBA. Mira el comando en la cabecera de este "
            "archivo. La clave nunca se escribe aqui: se lee de las variables de Windows.")
    # JULIO LO AUTORIZO EXPRESAMENTE (2026-08-22): "no importa que trabajes en el que te di,
    # eso es de prueba". Esa cuenta es la SUYA DE PRUEBAS, no la de trabajo. Se levanta el
    # bloqueo porque lo decide el dueno de los datos, no yo. Queda escrito aqui para que nadie
    # lo vuelva a bloquear "por precaucion" sin saber que ya se pregunto y se contesto.
    if EMAIL.lower() == CUENTA_REAL_PROHIBIDA and not AUTORIZADA_POR_JULIO:
        fin("BLOQUEADO",
            "Esta cuenta esta marcada como de trabajo. Esta prueba entra y navega. Si es de "
            "prueba de verdad, dilo y se levanta el bloqueo.")


def main() -> None:
    _comprobar_entrada()
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        fin("NO_SE_PUDO", "No esta el navegador automatico: %s" % str(exc)[:120])

    llamadas: list = []

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.on("request", lambda r: llamadas.append(
            {"cuando": time.time(), "metodo": r.method, "url": r.url}))

        def contar(desde: float, hasta: float) -> int:
            """Llamadas al servidor (no imagenes ni estilos) en esa ventana de tiempo."""
            return len([c for c in llamadas
                        if desde <= c["cuando"] <= hasta
                        and c["url"].startswith(BASE_URL)
                        and not c["url"].endswith((".css", ".js", ".png", ".jpg", ".ico"))])

        try:
            pagina.goto(BASE_URL, timeout=60000)
        except Exception as exc:
            navegador.close()
            fin("NO_SE_PUDO",
                "El MVP no responde en %s. Arrancalo primero y vuelve a correr esto. (%s)"
                % (BASE_URL, str(exc)[:100]))

        # ── entrar ────────────────────────────────────────────────────────────
        try:
            # Los nombres de los campos se MIRARON en la pantalla, no se adivinaron. La primera
            # version invento dos que no existen y la prueba murio esperandolos 30 segundos
            # (fallo real 2026-08-22). Los de verdad son estos.
            pagina.fill("#email", EMAIL)
            pagina.fill("#password", PASSWORD)
            pagina.click("#loginBtn")
            # No se esperan 6 segundos a ciegas: se espera a que la pantalla CAMBIE de verdad.
            # Con un tiempo fijo, si la nube va lenta la prueba sigue sin haber entrado y le
            # echa la culpa a la reparacion de algo que no es.
            pagina.set_default_timeout(ESPERA_ENTRAR_MS)
            pagina.wait_for_function(
                "() => { const s = document.getElementById('appShell');"
                " return s && !s.classList.contains('hidden'); }")
        except Exception as exc:
            navegador.close()
            fin("NO_SE_PUDO", "No se pudo entrar: %s" % str(exc)[:150])

        resultados = {}

        def esperar_a_que_se_calle(segundos_de_silencio=3, tope=30):
            """Espera a que la pantalla TERMINE de arrancar, tarde lo que tarde.

            POR QUE ASI Y NO CON UN NUMERO FIJO: al entrar, la pantalla pide su configuracion
            (medido: 2 llamadas en el segundo mas 1.3) y despues se calla. Eso NO es un reloj,
            es el arranque. Contarlo daba ROJO con la aplicacion perfecta.
            Se penso en esperar 5 segundos fijos, y se rechazo con razon: en una maquina mas
            lenta el arranque tardaria mas y la prueba daria ROJO sin motivo. Es el fallo ya
            apuntado de la prueba que depende de cuanto tarde la maquina.
            Asi que no se espera un numero: se espera a que DEJE de llamar. No se cuentan
            segundos, se cuentan llamadas. En una maquina lenta tarda mas y sigue valiendo.

            NO TAPA NADA: si hubiera un reloj llamando cada pocos segundos, nunca habria
            silencio, se agotaria el tope y la prueba daria ROJO igual. Que es lo correcto.
            """
            quietos = 0
            for _ in range(tope):
                antes = len(llamadas)
                pagina.wait_for_timeout(1000)
                quietos = quietos + 1 if len(llamadas) == antes else 0
                if quietos >= segundos_de_silencio:
                    return True
            return False

        # ── 1. quieto en el menu: CERO ────────────────────────────────────────
        esperar_a_que_se_calle()
        t0 = time.time()
        pagina.wait_for_timeout(QUIETO_MENU_S * 1000)
        resultados["quieto_en_el_menu"] = contar(t0 + 1, time.time())

        # ── 2. en la pantalla de las fotos: SI llama ───────────────────────────
        try:
            pagina.evaluate("go(4)")
            pagina.wait_for_timeout(1500)
        except Exception as exc:
            navegador.close()
            fin("NO_SE_PUDO", "No se pudo abrir la pantalla de fotos: %s" % str(exc)[:120])
        t1 = time.time()
        pagina.wait_for_timeout(QUIETO_FOTOS_S * 1000)
        resultados["en_la_pantalla_de_fotos"] = contar(t1 + 1, time.time())

        # ── 3. ventana escondida, en la de fotos: CERO ────────────────────────
        pagina.evaluate(
            "Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});"
            "document.dispatchEvent(new Event('visibilitychange'))")
        t2 = time.time()
        pagina.wait_for_timeout(ESCONDIDA_S * 1000)
        resultados["con_la_ventana_escondida"] = contar(t2 + 1, time.time())

        # ── 4. la libreta no se vacia entera al guardar ────────────────────────
        try:
            resultados["libreta_selectiva"] = pagina.evaluate("""() => {
                if(!state.apiResponseCache) state.apiResponseCache = {};
                state.apiResponseCache["GET /template/config"] = {at:Date.now(),data:{},status:200};
                state.apiResponseCache["GET /reports"] = {at:Date.now(),data:{},status:200};
                invalidarLibretaDeEsaRuta("/reports");
                return {
                    la_lista_se_olvido: !state.apiResponseCache["GET /reports"],
                    lo_demas_se_recuerda: !!state.apiResponseCache["GET /template/config"]
                };
            }""")
        except Exception as exc:
            resultados["libreta_selectiva"] = {"error": str(exc)[:120]}

        navegador.close()

    # ── veredicto ─────────────────────────────────────────────────────────────
    fallos = []
    if resultados["quieto_en_el_menu"] > 0:
        fallos.append("quieto en el menu hizo %d llamada(s): deberian ser CERO"
                      % resultados["quieto_en_el_menu"])
    if resultados["en_la_pantalla_de_fotos"] < 2:
        fallos.append("en la pantalla de fotos solo hizo %d llamada(s) en %d s: deberia mirar "
                      "cada 5 segundos, o las fotos del celular no apareceran"
                      % (resultados["en_la_pantalla_de_fotos"], QUIETO_FOTOS_S))
    if resultados["con_la_ventana_escondida"] > 0:
        fallos.append("con la ventana escondida hizo %d llamada(s): deberian ser CERO"
                      % resultados["con_la_ventana_escondida"])
    sel = resultados.get("libreta_selectiva") or {}
    if not sel.get("la_lista_se_olvido"):
        fallos.append("al guardar no olvido lo que tenia que olvidar")
    if not sel.get("lo_demas_se_recuerda"):
        fallos.append("al guardar borro la libreta ENTERA: la fuga sigue ahi")

    if fallos:
        fin("ROJO", "la reparacion NO quedo", fallos=fallos, medido=resultados)
    fin("VERDE",
        "Solo llama cuando hace falta. Falta que Julio lo vea con sus ojos: vigia verde NO es "
        "prueba.", medido=resultados)


if __name__ == "__main__":
    main()
