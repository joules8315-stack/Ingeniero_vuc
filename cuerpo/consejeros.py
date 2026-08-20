# -*- coding: utf-8 -*-
"""cuerpo/consejeros.py — LOS CONSEJEROS (orden de Julio, 2026-08-20).

  "los otros modelos de IA deben servir para ayudarte de respaldo, como consejeros, que te
   ayuden a traer cosas de la memoria, para que tomes mejores decisiones, de forma mas rapida
   y precisa"

QUE HACE Y QUE NO (honestidad, no humo):
  · NO sirven para "traer cosas de la memoria": eso lo hace el grafo, gratis y en milisegundos.
    Lo que se hace aqui es AL REVES: el grafo trae el material, y los consejeros OPINAN sobre el.
  · SI sirven para lo que hoy no tiene nadie: **revisar a Claude**. Qwen y Gemini se revisan
    entre ellos en `cuerpo/cruzado.py`, pero a Claude no lo revisa nadie. El 2026-08-20 esos
    mismos modelos cazaron dos fallos que 26 vigias verdes no habian visto.

LA SEÑAL MAS UTIL ES EL DESACUERDO. Si dos modelos distintos, sin verse, dicen lo mismo, la
decision es probablemente buena. Si discrepan, ahi hay algo que mirar ANTES de tocar codigo.
Por eso se les pregunta a la vez y por separado, y lo que se devuelve es si COINCIDEN.

    python ingeniero.py consejo "<la decision>" --proyecto dmm --porque "<mi razon>"
"""
import os, sys, json, time, threading

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cuerpo import obrero, cuotas, fallos   # noqa: E402


def _material(pregunta, proyecto=None, k=3):
    """El grafo trae el material; los consejeros solo opinan sobre el. Corto a proposito:
    un consejero con 20.000 letras tarda 300s; con 2.000 tarda 3s y opina igual de bien."""
    trozos_txt, fallos_txt = "", ""
    if proyecto:
        try:
            from cerebro import grafo, trozos as _t
            g = grafo.cargar(proyecto)
            codigo = [p for p in g["piezas"] if p["rol"] in ("CUERPO", "CODIGO", "CEREBRO", "WEB")]
            if codigo:
                b = _t.Buscador(codigo)
                partes = []
                for r in b.buscar(pregunta, k=k):
                    partes.append(f"--- {r['direccion']} ---\n{r['texto'][:900]}")
                trozos_txt = "\n".join(partes)
        except Exception:
            pass
    try:
        fallos_txt = fallos.aviso_para_el_paquete(pregunta, proyecto or "")
    except Exception:
        pass
    return trozos_txt, fallos_txt


def _prompt(pregunta, porque, trozos_txt, fallos_txt):
    partes = [
        "Eres CONSEJERO de un ingeniero de software. No ejecutas nada: opinas, y tu valor esta",
        "en detectar el error que el no ve. Se breve y concreto. Si no puedes saberlo con el",
        "material dado, di NO_SE en vez de inventar: inventar aqui hace mas dano que callar.",
        "",
        f"DECISION QUE SE VA A TOMAR: {pregunta}",
    ]
    if porque:
        partes.append(f"RAZON QUE DA EL INGENIERO: {porque}")
    if fallos_txt:
        partes += ["", "LO QUE YA FALLO ANTES AQUI:", fallos_txt]
    if trozos_txt:
        partes += ["", "MATERIAL DEL CODIGO (solo los pedazos que vienen al caso):", trozos_txt]
    partes += [
        "",
        "Responde SOLO JSON, sin texto alrededor:",
        '{"de_acuerdo": true/false,',
        ' "riesgo_principal": "el peligro mas gordo de hacer esto, en una frase",',
        ' "que_se_le_escapa": "algo importante que el ingeniero no ha tenido en cuenta, o NO_SE",',
        ' "alternativa_mejor": "si la hay; si no, pon NINGUNA",',
        ' "confianza": "alta|media|baja"}',
    ]
    return "\n".join(partes)


def consultar(pregunta, porque="", proyecto=None, cuantos=2):
    """Pregunta a varios cerebros A LA VEZ y por separado. Devuelve si coinciden."""
    ok, quien = obrero.disponible()
    if not ok:
        return {"_error": quien}
    hay = cuotas.fila(obrero.quienes_hay()) or obrero.quienes_hay()
    if not hay:
        return {"_error": "NO_ENCONTRADO: no hay ningun cerebro libre"}

    trozos_txt, fallos_txt = _material(pregunta, proyecto)
    p = _prompt(pregunta, porque, trozos_txt, fallos_txt)

    t0 = time.time()
    res = {}
    hilos = []

    def _correr(quien_):
        res[quien_] = obrero._preguntar_con_relevo(p, 0.3, primero=quien_)

    for q in hay[:cuantos]:
        h = threading.Thread(target=_correr, args=(q,), daemon=True)
        h.start()
        hilos.append(h)
    for h in hilos:
        h.join()

    opiniones = []
    for q, (txt, quien_real, avisos) in res.items():
        if not txt:
            opiniones.append({"cerebro": q, "_error": "; ".join(avisos)})
            continue
        d = obrero._json_de(txt)
        d["cerebro"] = quien_real or q
        opiniones.append(d)

    validas = [o for o in opiniones if "_error" not in o and "de_acuerdo" in o]
    coinciden, veredicto = None, "?"
    if len(validas) >= 2:
        votos = {bool(o.get("de_acuerdo")) for o in validas}
        coinciden = len(votos) == 1
        # OJO (fallo real 2026-08-20): "coinciden" NO quiere decir "aprueban". Los dos pueden
        # coincidir en RECHAZAR. El informe decia "tiene buena pinta" cuando ambos habian dicho
        # que NO. Un resumen que dice lo contrario de lo que paso es peor que no tener resumen.
        if coinciden:
            veredicto = "APRUEBAN" if True in votos else "RECHAZAN"
        else:
            veredicto = "DISCREPAN"
    elif len(validas) == 1:
        veredicto = "APRUEBA" if validas[0].get("de_acuerdo") else "RECHAZA"

    return {"pregunta": pregunta, "porque": porque, "proyecto": proyecto,
            "opiniones": opiniones, "coinciden": coinciden, "veredicto": veredicto,
            "material_chars": len(trozos_txt) + len(fallos_txt),
            "segundos": round(time.time() - t0, 1)}


def informe(r):
    """Lo unico que lee Claude. Corto, y con el DESACUERDO destacado."""
    if "_error" in r:
        return "SIN CONSEJO: " + str(r["_error"])[:300]
    L = [f"CONSEJEROS — {len(r['opiniones'])} opiniones en {r['segundos']}s "
         f"(material: {r['material_chars']} letras del grafo, no del repo entero)"]
    v = r.get("veredicto", "?")
    if v == "APRUEBAN":
        L.append("  LOS DOS APRUEBAN -> la decision tiene buena pinta.")
    elif v == "RECHAZAN":
        L.append("  *** LOS DOS LA RECHAZAN -> NO LO HAGAS sin resolver lo de abajo ***")
    elif v == "DISCREPAN":
        L.append("  *** DISCREPAN ENTRE ELLOS -> aqui hay algo que mirar ANTES de tocar nada ***")
    elif v in ("APRUEBA", "RECHAZA"):
        L.append(f"  solo contesto uno y {v} (con una sola opinion no hay contraste)")
    for o in r["opiniones"]:
        if "_error" in o:
            L.append(f"  [{o['cerebro']}] no contesto: {str(o['_error'])[:80]}")
            continue
        L.append(f"  [{o.get('cerebro','?')}] de acuerdo: {o.get('de_acuerdo')} "
                 f"(confianza {o.get('confianza','?')})")
        L.append(f"      riesgo    : {str(o.get('riesgo_principal',''))[:120]}")
        se_escapa = str(o.get("que_se_le_escapa", ""))
        if se_escapa and se_escapa != "NO_SE":
            L.append(f"      se te escapa: {se_escapa[:120]}")
        alt = str(o.get("alternativa_mejor", ""))
        if alt and alt.upper() not in ("NINGUNA", "NO_SE", ""):
            L.append(f"      alternativa : {alt[:120]}")
    L.append("  (esto es una OPINION, no una prueba. La prueba sigue siendo la de Julio.)")
    return "\n".join(L)
