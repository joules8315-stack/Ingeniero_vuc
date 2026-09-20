# -*- coding: utf-8 -*-
"""cuerpo/cruzado.py — TRABAJO CRUZADO: nadie se autovalida (orden de Julio, 2026-08-20).

  "mientras un agente trabaja en la tarea con los vigias, otro agente trabaja en observar,
   o crear el vigia, o el kit de vigias, para que no se autovalide"

La trampa que esto mata: si el MISMO que repara escribe la prueba, escribe la prueba que su
reparacion pasa. Verde garantizado, y no prueba nada. Es la vieja leccion de Julio
(no-ship-sin-prueba-humana, C25/C26: verde sobre un caso que no se vive).

Como se reparte el trabajo (los tres a la vez, no en fila — orden 4: nada lento):

    REPARADOR  (cerebro A)  ve el paquete + el problema      -> propone la cura
    VIGILANTE  (cerebro B)  ve el paquete + el problema      -> escribe la vigia
                            **NO VE la propuesta del reparador**
    AUDITOR    (cerebro C)  ve las dos cosas                 -> dice si la cura pasa la vigia

El vigilante trabaja A CIEGAS respecto de la cura. Por eso su vigia prueba EL PROBLEMA,
no la solucion de nadie.

Y si el auditor rechaza, se vuelve a intentar con lo aprendido (orden 6: "hasta encontrar la
solucion real"), con un tope para no gastar cuota de gusto.
"""
import os, sys, json, time, threading

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cuerpo import obrero, cuotas, fallos   # noqa: E402

RONDAS_MAX = 3
# Tope de RELOJ para el ciclo entero (orden 4 de Julio: nada lento). El tope por llamada no
# basta: 3 rondas x 2 llamadas podian sumar 15 minutos. Fallo real 2026-08-20.
TOPE_CICLO = 300   # segundos


def _prompt_vigilante(paquete, problema):
    """OJO: aqui NO entra la propuesta de nadie. A ciegas a proposito."""
    return f"""Eres el VIGILANTE. Tu trabajo NO es reparar: es escribir la PRUEBA que dira si el
problema quedo arreglado de verdad. Otro esta reparando en paralelo y tu NO ves lo que hace,
a proposito: asi tu prueba comprueba EL PROBLEMA, no la solucion de nadie.

PROBLEMA: {problema}

REGLAS DURAS:
1. La prueba debe FALLAR hoy (con el problema presente) y PASAR cuando se arregle.
   Una prueba que ya pasa hoy no prueba nada.
2. Prueba el caso que el DUENO de verdad vive, no un caso de laboratorio.
3. Usa solo archivos y funciones que aparezcan en el material. Lo que no este: NO_ENCONTRADO.
4. Nada de mocks que se prueben a si mismos.

Responde SOLO JSON:
{{"que_comprueba": "en una frase, que tiene que pasar para decir que quedo bien",
  "caso_real": "el caso concreto que vive el dueno",
  "archivo_vigia": "vigias/test_vigia_<nombre>.py",
  "codigo": "el codigo de la prueba en python/pytest",
  "por_que_falla_hoy": "por que esta prueba se pone ROJA con el problema presente",
  "no_vale_si": "que atajo haria que esta prueba pasara sin arreglar nada de verdad"}}

===== MATERIAL =====
{paquete}
===== FIN ====="""


def _prompt_juez(paquete, propuesta, vigia):
    return f"""Eres el JUEZ. Tienes dos trabajos hechos POR SEPARADO y sin verse:
  (A) una REPARACION propuesta
  (B) una PRUEBA escrita a ciegas, que comprueba el problema

Di si la reparacion (A) pasaria la prueba (B). Se duro: tu trabajo es encontrar el hueco.

RESPONDE LOS FALLOS CON CODIGOS NUMERICOS, NO CON TEXTO (Julio, 2026-08-27): asi no te atas
en lo generico y el sistema siempre te entiende. La lista de fallos esta numerada abajo.

Comprueba y, si algo falla, apunta SU CODIGO en "fallos":
  1 = INVENTA (la reparacion usa un archivo/funcion/linea que no esta en el material)
  2 = NO PASA LA PRUEBA (la reparacion no hace pasar de verdad la prueba B, solo se le parece)
  3 = ATAJO PROHIBIDO (la reparacion usa el atajo que la prueba B marca como "no_vale_si")
  4 = ROMPE UN VECINO (daña a alguno de "A QUIEN PUEDE DANAR")
  5 = TAPA EL SINTOMA (no ataca la causa raiz, solo lo disfraza)
  6 = DUDOSO (no puedes decidir: di en "que_le_falta" que te falta para aprobar)

RESPONDE SOLO UN JSON, sin texto antes ni despues, sin ```:
{{"veredicto": "APROBADO|RECHAZADO|DUDOSO",
  "invento_algo": true/false,
  "fallos": [<codigos numericos, ej: 1, 5>],
  "que_le_falta": "solo si fallos=6 o si falta un detalle concreto",
  "resumen_para_el_jefe": "una frase para decidir sin leer todo"}}

PON PRIMERO "veredicto": es lo unico imprescindible, llega siempre. Los "fallos" son codigos
(1..6), no frases. Si no puedes decidir, pon "veredicto":"DUDOSO" y "fallos":[6].

===== (A) REPARACION PROPUESTA =====
{propuesta}
===== (B) PRUEBA ESCRITA A CIEGAS =====
{vigia}
===== MATERIAL ORIGINAL =====
{paquete}
===== FIN ====="""


# CATALOGO NUMERICO DE FALLOS DEL JUEZ (Julio, 2026-08-27): el juez responde con codigos (1..6),
# no con texto generico, para que el sistema siempre lo entienda y no se atasca. Esta funcion
# convierte los codigos en texto para que el reparador entienda que corregir.
FALLOS_DEL_JUEZ = {
    1: "la reparacion INVENTA (usa un archivo/funcion/linea que no esta en el material)",
    2: "la reparacion NO hace pasar la prueba de verdad (solo se le parece)",
    3: "la reparacion usa el ATAJO PROHIBIDO que la prueba marca como no_vale_si",
    4: "la reparacion ROMPE UN VECINO de 'A QUIEN PUEDE DANAR'",
    5: "la reparacion TAPA EL SINTOMA, no ataca la causa raiz",
    6: "el juez no pudo decidir (DUDOSO)",
}


def fallos_a_texto(codigos, extra=""):
    """Convierte los codigos del juez a texto entendible. Acepta codigos (1..6) o texto ya escrito.

    SI EL JUEZ NO SE CIÑE AL CATALOGO (Julio, 2026-08-27): un codigo fuera de rango (0, 7, ...)
    o texto libre donde deberia ir un numero es una SEÑAL de que el juez no sigue el codigo. No se
    deja pasar silencioso: se marca como "fallo de codigo del juez" y devuelve tambien ese aviso.
    """
    if not codigos:
        return str(extra or "").strip()
    partes, raros = [], []
    for c in (codigos if isinstance(codigos, (list, tuple)) else [codigos]):
        try:
            n = int(c)
            if n in FALLOS_DEL_JUEZ:
                partes.append(FALLOS_DEL_JUEZ[n])
            else:
                raros.append(str(c))     # codigo fuera del catalogo 1..6
        except (TypeError, ValueError):
            raros.append(str(c))         # texto libre donde iba un codigo
    txt = "; ".join(p for p in partes if p)
    if raros:
        aviso = "CODIGO DE JUEZ NO RECONOCIDO: %s" % ", ".join(raros)
        txt = (aviso + " | " + txt) if txt else aviso
    if extra:
        txt = (txt + " | " + str(extra)) if txt else str(extra)
    return txt[:600]


def _en_paralelo(tareas):
    """Lanza varias preguntas al mismo tiempo. Orden 4 de Julio: nada de procesos lentos.
    Cada tarea = (nombre, prompt, temperatura, evitar, primero)."""
    res = {}
    hilos = []

    def _correr(nombre, prompt, temp, evitar, primero):
        res[nombre] = obrero._preguntar_con_relevo(prompt, temp, evitar=evitar, primero=primero)

    for nombre, prompt, temp, evitar, primero in tareas:
        h = threading.Thread(target=_correr, args=(nombre, prompt, temp, evitar, primero), daemon=True)
        h.start()
        hilos.append(h)
    for h in hilos:
        h.join()
    return res


def resolver(paquete, problema, proyecto="", rondas=RONDAS_MAX, al_vuelo=None):
    """El ciclo completo. Devuelve el informe con la ronda que aprobo (o el porque no)."""
    def _decir(t):
        if al_vuelo:
            al_vuelo(t)

    ok, quien = obrero.disponible()
    if not ok:
        return {"_error": quien}

    t0 = time.time()
    historial = []
    aprendido = ""

    # 1) REPARADOR y VIGILANTE, a la vez y sin verse.
    _decir("Reparador y vigilante trabajando A LA VEZ (el vigilante no ve la reparacion)...")
    # SE REPARTEN LOS CEREBROS (fallo real 2026-08-20): si los dos hilos piden el mismo,
    # compiten, tardan el doble y acaban marcados como lentos... dejando al sistema sin nadie.
    # Ademas conviene que reparador y vigilante NO sean el mismo modelo: dos cabezas distintas.
    libres = cuotas.fila(obrero.quienes_hay()) or obrero.quienes_hay()
    para_reparar = libres[0] if libres else None
    para_vigilar = libres[1] if len(libres) > 1 else libres[0] if libres else None
    tareas = [
        ("reparador", obrero._prompt_obrero(paquete, problema), 0.2, None, para_reparar),
        ("vigilante", _prompt_vigilante(paquete, problema), 0.2, None, para_vigilar),
    ]
    r = _en_paralelo(tareas)
    txt_vig, quien_vig, av_vig = r.get("vigilante", ("", "", []))
    vigia = obrero._json_de(txt_vig) if txt_vig else {"_error": "; ".join(av_vig)}

    for ronda in range(1, rondas + 1):
        if ronda == 1:
            txt_rep, quien_rep, av_rep = r.get("reparador", ("", "", []))
        else:
            _decir(f"Ronda {ronda}: el reparador lo intenta otra vez con lo que dijo el juez...")
            txt_rep, quien_rep, av_rep = obrero._preguntar_con_relevo(
                obrero._prompt_obrero(paquete, problema) +
                "\n\nINTENTO ANTERIOR RECHAZADO. Lo que fallo:\n" + aprendido +
                "\nCorrige ESO. No repitas el mismo error.", 0.3)
        if not txt_rep:
            return {"_error": "; ".join(av_rep), "vigia": vigia}
        propuesta = obrero._json_de(txt_rep)

        # 2) JUEZ: distinto del reparador, ve las dos cosas.
        _decir(f"Ronda {ronda}: el juez compara la reparacion contra la vigia...")
        juez = None
        txt_juez, quien_juez, av_juez = "", "", []
        try:
            from arnes import juez_de_la_prueba as jp
            archivo_prop = propuesta.get("archivo")
            texto_viejo_prop = propuesta.get("texto_viejo")
            texto_nuevo_prop = propuesta.get("texto_nuevo")
            raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_rel = str(archivo_prop).replace("\\", "/")
            if ruta_rel.startswith(raiz.replace("\\", "/")):
                ruta_rel = ruta_rel[len(raiz.replace("\\", "/")):].lstrip("/")
            if archivo_prop and texto_viejo_prop:
                res = jp.juzgar_con_vecinas(raiz, ruta_rel, texto_viejo_prop, texto_nuevo_prop, dejar_el_cambio=False)
                if isinstance(res, dict) and res.get("ok") is True:
                    juez = {"veredicto": "APROBADO", "invento_algo": False, "fallos": [],
                            "que_le_falta": "",
                            "resumen_para_el_jefe": "La prueba se corrio de verdad y quedo verde."}
                    quien_juez = "juez de la prueba (programa)"
                elif isinstance(res, dict) and res.get("ok") is False:
                    juez = {"veredicto": "RECHAZADO", "invento_algo": False, "fallos": [2],
                            "que_le_falta": res.get("razon", ""),
                            "resumen_para_el_jefe": "La prueba se corrio de verdad y NO paso."}
                    quien_juez = "juez de la prueba (programa)"
        except Exception:
            pass
        for intento_juez in range(0 if juez is not None else 2):   # el juez puede devolver JSON roto: se le pide de nuevo
            txt_juez, quien_juez, av_juez = obrero._preguntar_con_relevo(
                _prompt_juez(paquete, json.dumps(propuesta, ensure_ascii=False),
                             json.dumps(vigia, ensure_ascii=False)), 0.1, evitar=quien_rep)
            juez = (obrero._json_de(txt_juez) if txt_juez
                    else {"veredicto": "SIN_JUEZ", "_error": "; ".join(av_juez)})
            if "_error" not in juez:
                break    # se entendio: listo
            # JSON roto/cortado: no se da por perdido, se le pide de nuevo (Julio, 2026-08-27).
            _decir(f"  el juez respondio ilegible ({juez.get('_error')[:40]}); se le pide de nuevo")
        if "_error" in juez:
            juez = {"veredicto": "SIN_JUEZ", "_error": juez.get("_error"),
                    "_crudo": juez.get("_crudo", "")}

        historial.append({"ronda": ronda, "reparador": quien_rep, "juez": quien_juez,
                          "veredicto": juez.get("veredicto"),
                          "propuesta": propuesta, "juez_dice": juez})

        v = (juez.get("veredicto") or "").upper()
        if v == "APROBADO" and not juez.get("invento_algo"):
            break
        if time.time() - t0 > TOPE_CICLO:
            _decir(f"Se acabo el tiempo ({TOPE_CICLO}s): se entrega lo que hay y se dice que falta.")
            historial[-1]["corto_por_tiempo"] = True
            break
        aprendido = fallos_a_texto(juez.get("fallos"), juez.get("que_le_falta"))
        if v == "SIN_JUEZ":
            break

    ultimo = historial[-1] if historial else {}
    salida = {
        "problema": problema, "proyecto": proyecto,
        "vigilante": quien_vig, "vigia": vigia,
        "rondas": historial, "rondas_usadas": len(historial),
        "veredicto": ultimo.get("veredicto", "?"),
        "propuesta": ultimo.get("propuesta", {}),
        "juez_dice": ultimo.get("juez_dice", {}),
        "segundos": round(time.time() - t0, 1),
    }

    # 3) Se apunta en la memoria de fallos, gane o pierda: de los dos se aprende.
    try:
        import os as _os
        if _os.environ.get("PYTEST_CURRENT_TEST"):
            return salida
        p = salida["propuesta"]
        if p and "_error" not in p and p.get("diagnostico") not in (None, "NO_ENCONTRADO"):
            fallos.apuntar(
                que_paso=problema,
                causa_raiz=str(p.get("diagnostico", ""))[:300],
                cura=str(p.get("cambio", ""))[:300],
                no_volver_a=str(salida["juez_dice"].get("que_le_falta") or
                                vigia.get("no_vale_si") or "")[:300],
                proyecto=proyecto,
                piezas=[str(p.get("archivo", ""))],
                quien_lo_caza=str(vigia.get("archivo_vigia", "")))
    except Exception:
        pass
    return salida


def informe(s):
    """Lo UNICO que lee Claude. Pocas lineas, veredicto primero."""
    if "_error" in s:
        return "NO SE PUDO: " + s["_error"]
    L = [f"TRABAJO CRUZADO — {s['rondas_usadas']} ronda(s), {s['segundos']}s"]
    if s.get("rondas") and s["rondas"][-1].get("corto_por_tiempo"):
        L.append("  (se corto por tiempo: no se dejo a Julio esperando)")
    v = s.get("vigia", {})
    L.append(f"  VIGILANTE ({s['vigilante']}) escribio la prueba A CIEGAS:")
    L.append(f"    comprueba : {str(v.get('que_comprueba', '?'))[:110]}")
    L.append(f"    caso real : {str(v.get('caso_real', '?'))[:110]}")
    L.append(f"    no vale si: {str(v.get('no_vale_si', '?'))[:110]}")
    p = s.get("propuesta", {})
    L.append(f"  REPARADOR propone:")
    L.append(f"    diagnostico: {str(p.get('diagnostico', '?'))[:110]}")
    L.append(f"    toca       : {p.get('archivo', '?')} lineas {p.get('lineas', '?')}")
    j = s.get("juez_dice", {})
    L.append(f"  JUEZ: {s.get('veredicto', '?')}"
             + ("  *** INVENTO ALGO -> SE DESCARTA" if j.get("invento_algo") else ""))
    if j.get("ataca_la_causa_raiz") is False:
        L.append("    OJO: tapa el sintoma, no la causa raiz")
    for f in (j.get("fallos") or [])[:3]:
        L.append(f"    fallo: {str(f)[:110]}")
    if j.get("resumen_para_el_jefe"):
        L.append(f"    resumen: {str(j['resumen_para_el_jefe'])[:150]}")
    if p.get("preguntas"):
        L.append(f"  PREGUNTA_REQUERIDA: {'; '.join(str(x) for x in p['preguntas'])[:200]}")
    L.append("  (vigia verde NO es prueba: falta que Julio lo vea con sus ojos)")
    return "\n".join(L)
