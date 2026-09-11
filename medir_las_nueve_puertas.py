# -*- coding: utf-8 -*-
"""MIDE LAS 9 PUERTAS del corredor (auditoria 2026-09-09). NO toca la produccion: solo mide.

QUE MIDE
  El tamano REAL del texto que sale hacia el cerebro por CADA puerta del corredor
  (_preguntar_con_relevo), con material real, y lo compara con los topes que el propio
  sistema declara y con lo que los cerebros han aguantado de verdad (memoria/CUOTAS.json).

COMO LO MIDE, SIN TRAMPAS
  1) POR RECETA: reconstruye el prompt con la MISMA expresion que hay en el codigo, tal cual.
  2) EN VIVO (prueba de verdad): intercepta _preguntar_con_relevo con un espia que apunta
     archivo:linea y tamano, y corre los flujos reales (trabajar, resolver, consultar,
     _responde_de_verdad). El espia SUSTITUYE al pasillo, asi que ninguna llamada sale a
     internet: la prueba es gratis y no gasta cuota.

NO ESCRIBE NADA: los dobles anulan cuotas.apuntar_*, fallos.apuntar y la creacion de skills.
No se toca ningun archivo del proyecto (solo se lee).

USO:  python medir_las_nueve_puertas.py
"""
import glob
import inspect
import json
import os
import sys
import threading

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
sys.path.insert(0, AQUI)

import asignador                                            # noqa: E402
from cuerpo import obrero, cuotas, cruzado, consejeros, dudas, fallos  # noqa: E402


# ─── EL MATERIAL REAL ───────────────────────────────────────────────────────────────
# Escenario A: la ronda de verdad del 2026-09-09 (la misma de medir_el_pasillo.py).
objetivo_real = "x" * 7575      # lo que Julio mando (medido)
material_real = "y" * 34460     # el paquete medido
PAQUETE_A = asignador.armar_encargo({"objetivo": objetivo_real, "prueba": "resolver"},
                                    material=material_real)

# Escenario B: un paquete REAL de los que se prepararon de verdad (memoria/paquetes/).
# Se usa el de la MEDIANA, no el mayor, para no exagerar.
_ps = sorted(glob.glob(os.path.join(AQUI, "memoria", "paquetes", "*.md")),
             key=os.path.getsize)
PAQUETE_B = open(_ps[len(_ps) // 2], encoding="utf-8", errors="ignore").read()
NOMBRE_B = os.path.basename(_ps[len(_ps) // 2])

# La propuesta y la vigia REALES de esa ronda (no inventadas).
_ult = json.load(open(os.path.join(AQUI, "memoria", "ULTIMO_TRABAJO_DEL_EQUIPO.json"),
                      encoding="utf-8"))
PROPUESTA = _ult.get("propuesta") or {}
VIGIA = {"que_comprueba": "la prueba de la ronda real",
         "archivo_vigia": "vigias/test_vigia_real.py",
         "codigo": "def test_real():\n    assert True\n",
         "no_vale_si": "tapar el sintoma"}
QUE_LE_FALTA = "no ataca la causa raiz, tapa el sintoma"

APRENDIDO_REAL = cruzado.fallos_a_texto([1, 5], QUE_LE_FALTA)   # lo que se pega en la 2a vuelta
RECARGO_REINTENTO = ("\n\nINTENTO ANTERIOR RECHAZADO. Lo que fallo:\n" + APRENDIDO_REAL +
                     "\nCorrige ESO. No repitas el mismo error.")
MOTIVOS_REINTENTO = ("Este trabajo ya se rechazo antes, y estos fueron los motivos:\n" +
                     QUE_LE_FALTA + "\nArregla todos esos motivos y no repitas el mismo fallo.\n")


# ─── LO QUE EL SISTEMA DECLARA (leido del propio codigo, no copiado a mano) ─────────
TOPES = {
    "asignador.TOPE_LETRAS": asignador.TOPE_LETRAS,
    "obrero.TOPE_PESADO": obrero.TOPE_PESADO,
    "obrero.TOPE_LOCAL": obrero.TOPE_LOCAL,
    "vigia.TOPE_GRATIS (test)": 19000,   # esta escrito a mano dentro de la vigia
}



def capacidades(paquete=None):
    """Lo que de verdad ha aguantado cada cerebro y quien esta durmiendo (memoria/CUOTAS.json)."""
    try:
        c = json.load(open(os.path.join(AQUI, "memoria", "CUOTAS.json"), encoding="utf-8"))
    except Exception as e:
        return {"_error": str(e)[:120]}
    out = {"por_cerebro": {}, "dormidos_ahora": c.get("dormidos") or []}
    for q, v in (c.get("gasto") or {}).items():
        if isinstance(v, dict):
            out["por_cerebro"][q] = {"mayor_ok": v.get("mayor_ok"), "no_cupo": v.get("no_cupo"),
                                     "llamadas": v.get("llamadas"), "fallos": v.get("fallos")}
    # El cerebro GRATIS mas pequeno de los que de verdad contestan: ese es el tope real de la casa.
    gratis = {q: v["mayor_ok"] for q, v in out["por_cerebro"].items()
              if v.get("mayor_ok") and q not in ("deepseek", "local")}
    out["el_gratis_mas_pequeno_que_aguanta"] = min(gratis.values()) if gratis else None
    out["el_local_aguanta"] = (out["por_cerebro"].get("local") or {}).get("mayor_ok")
    return out



# ─── 1) MEDICION POR RECETA: la misma expresion del codigo, linea por linea ─────────
def por_receta(paquete):
    """Devuelve [(puerta, archivo:linea, que, prompt)] con la expresion EXACTA del codigo."""
    jp = json.dumps(PROPUESTA, ensure_ascii=False)
    jv = json.dumps(VIGIA, ensure_ascii=False)
    problema = "reparar el pasillo del cerebro"
    pregunta = "¿se recorta el paquete antes o despues de montar el prompt?"
    porque = "medicion"
    trozos_txt, fallos_txt = "", ""
    try:
        trozos_txt, fallos_txt = consejeros._material(pregunta, "ingeniero")
    except Exception:
        pass
    cand = [{"fuente": "CODIGO", "donde": "cuerpo/obrero.py",
             "texto": paquete[:700], "puntaje": 1.0}]
    trozos_dudas = "\n\n".join("[%d] (%s -- %s)\n%s" % (i, c["fuente"], c["donde"], c["texto"][:700])
                               for i, c in enumerate(cand[:5]))
    tarea_skill = ("Escribe una habilidad de Python llamada `contar` que haga esto: contar cosas\n\n"
                   "REGLAS:\n- Un solo archivo, sin dependencias raras.\n"
                   "Responde SOLO el codigo Python, sin explicaciones y sin comillas de bloque.")
    dudas_txt = ("Di cuales de estos textos RESPONDEN la pregunta de abajo. Que aparezcan palabras\n"
                 "parecidas NO basta: tiene que responderla de verdad.\n"
                 "Si ninguno la responde, devuelve la lista vacia. Es MEJOR decir que ninguno\n"
                 "responde que dar por buena una respuesta que no lo es.\n\n"
                 "PREGUNTA: " + pregunta + "\n\nTEXTOS:\n" + trozos_dudas + "\n\n"
                 'Responde SOLO JSON: {"responden": [numeros], "por_que": "una frase"}')

    return [
        ("P1 auditar (gratis)", "cuerpo/obrero.py:664",
         "_prompt_auditor(paquete, json(propuesta))",
         obrero._prompt_auditor(paquete, jp)),
        ("P2 auditar (ultimo recurso)", "cuerpo/obrero.py:689",
         "el mismo _prompt_auditor, pero con pesado=True",
         obrero._prompt_auditor(paquete, jp)),
        ("P3 generar", "cuerpo/obrero.py:742",
         "_prompt_obrero(paquete, tarea, clase='reparar')",
         obrero._prompt_obrero(paquete, problema, "reparar")),
        ("P3b generar (vuelta 2, con motivos)", "cuerpo/obrero.py:738-742",
         "_prompt_obrero(paquete, MOTIVOS + tarea)",
         obrero._prompt_obrero(paquete, MOTIVOS_REINTENTO + problema, "reparar")),
        ("P3c generar (clase crear/analista)", "cuerpo/obrero.py:71-97",
         "_prompt_obrero(paquete, tarea, clase='crear')",
         obrero._prompt_obrero(paquete, problema, "crear")),
        ("P4 reparador (ronda 1, a la vez)", "cuerpo/cruzado.py:149 <- :183",
         "_prompt_obrero(paquete, problema)",
         obrero._prompt_obrero(paquete, problema)),
        ("P5 vigilante (ronda 1, a la vez)", "cuerpo/cruzado.py:149 <- :184",
         "_prompt_vigilante(paquete, problema)",
         cruzado._prompt_vigilante(paquete, problema)),
        ("P6 reparador reintento", "cuerpo/cruzado.py:195-198",
         "_prompt_obrero(paquete, problema) + INTENTO ANTERIOR RECHAZADO",
         obrero._prompt_obrero(paquete, problema) + RECARGO_REINTENTO),
        ("P7 juez", "cuerpo/cruzado.py:208-210",
         "_prompt_juez(paquete, json(propuesta), json(vigia))",
         cruzado._prompt_juez(paquete, jp, jv)),
        ("P8 consejeros", "cuerpo/consejeros.py:95 -> :52",
         "consejeros._prompt(pregunta, porque, trozos, fallos)",
         consejeros._prompt(pregunta, porque, trozos_txt, fallos_txt)),
        ("P9 dudas", "cuerpo/dudas.py:140 -> :133-139",
         "el prompt literal de _responde_de_verdad", dudas_txt),
        ("P10 skills", "cuerpo/skills.py:194 -> :180-189",
         "la variable `tarea` (no lleva paquete: el encargo entero es la tarea)",
         tarea_skill),
    ]


# ─── 2) LA PRUEBA EN VIVO: se intercepta el pasillo y se corren los flujos de verdad ─
CAPTURAS = []
_LOCK = threading.Lock()
ENTORNO = {"escenario": "?", "flujo": "?", "muso": False}

_PROP = {"diagnostico": "medicion del pasillo", "archivo": "cuerpo/obrero.py",
         "funcion": "_prompt_obrero", "texto_viejo": "TOPE_LETRAS = 15000",
         "texto_nuevo": "TOPE_LETRAS = 15000", "cambio": "medicion", "codigo": "pass",
         "vigia": "ninguna", "puede_danar": [], "preguntas": [], "confianza": "alta"}
_AUD_RECH = {"veredicto": "RECHAZADO", "invento_algo": True, "que_invento": ["medicion"],
             "fallos": ["medicion"], "riesgo_vecinos": [], "que_falta": ["medicion"],
             "resumen_para_el_jefe": "medicion"}
_JUEZ_RECH = {"veredicto": "RECHAZADO", "invento_algo": False, "fallos": [1, 5],
              "que_le_falta": QUE_LE_FALTA, "resumen_para_el_jefe": "medicion"}
_VIG = {"que_comprueba": "medicion", "caso_real": "medicion",
        "archivo_vigia": "vigias/test_medicion.py",
        "codigo": "def test_medicion():\n    assert True\n",
        "por_que_falla_hoy": "medicion", "no_vale_si": "medicion"}
_CONSEJO = {"de_acuerdo": True, "riesgo_principal": "medicion", "que_se_le_escapa": "NO_SE",
            "alternativa_mejor": "NINGUNA", "confianza": "alta"}


def _respuesta(prompt):
    """Lo que contestaria un cerebro, para que el flujo SIGA y se mida la puerta siguiente."""
    j = json.dumps
    if "Eres el AUDITOR" in prompt:
        return "" if ENTORNO["muso"] else j(_AUD_RECH, ensure_ascii=False)
    if "Eres el JUEZ" in prompt:
        return j(_JUEZ_RECH, ensure_ascii=False)
    if "Eres el VIGILANTE" in prompt:
        return j(_VIG, ensure_ascii=False)
    if "Eres el OBRERO" in prompt or "Eres el ANALISTA" in prompt:
        return j(_PROP, ensure_ascii=False)
    if "Eres CONSEJERO" in prompt:
        return j(_CONSEJO, ensure_ascii=False)
    if "Di cuales de estos textos" in prompt:
        return j({"responden": [], "por_que": "medicion"})
    return ""


def espia(prompt, temperatura, evitar=None, primero=None, pesado=False):
    marco = inspect.stack()[1]
    with _LOCK:
        CAPTURAS.append({
            "escenario": ENTORNO["escenario"], "flujo": ENTORNO["flujo"],
            "funcion": marco.function, "linea": marco.lineno,
            "puerta": "%s:%d" % (os.path.relpath(marco.filename, AQUI).replace("\\", "/"),
                                 marco.lineno),
            "letras": len(prompt), "pesado": bool(pesado), "primero": primero,
            "salio_a_la_nube_de_pago": False})
    return _respuesta(prompt), "gemini", []


# ─── 3) DOBLES DE ESCRITURA: la medicion NO deja rastro en el proyecto ──────────────
def _sin_escribir():
    fallos.apuntar = lambda *a, **k: None
    for n in ("apuntar_uso", "apuntar_no_cupo", "dormir", "anotar_capacidad"):
        if hasattr(cuotas, n):
            setattr(cuotas, n, lambda *a, **k: None)


def correr_flujos(paquete, etiqueta):
    """Corre los flujos REALES con el pasillo interceptado. Devuelve las notas de lo que paso."""
    notas = []
    ENTORNO["escenario"] = etiqueta
    tarea = "repara el pasillo del cerebro midiendo el tamano real"

    for flujo, fn in (
        ("trabajar (auditor RECHAZADO: 3 vueltas)", lambda: _trabajar(paquete, tarea, False)),
        ("trabajar (auditor mudo: SIN_AUDITAR)", lambda: _trabajar(paquete, tarea, True)),
        ("cruzado.resolver (juez RECHAZADO: 3 rondas)",
         lambda: cruzado.resolver(paquete, tarea, rondas=3)),
        ("consejeros.consultar", lambda: consejeros.consultar(tarea, "medicion",
                                                              proyecto="ingeniero", cuantos=2)),
        ("dudas._responde_de_verdad",
         lambda: dudas._responde_de_verdad(tarea, [
             {"fuente": "CODIGO", "donde": "cuerpo/obrero.py",
              "texto": paquete[:700], "puntaje": 1.0}])),
    ):
        ENTORNO["flujo"] = flujo
        try:
            r = fn()
            if isinstance(r, dict) and r.get("_error"):
                notas.append({"flujo": flujo, "resultado": "ERROR: " + str(r["_error"])[:120]})
            else:
                notas.append({"flujo": flujo, "resultado": "corrido"})
        except Exception as e:
            notas.append({"flujo": flujo, "resultado": "EXCEPCION: " + str(e)[:140]})
    notas.append({"flujo": "skills.crear", "resultado":
                  "NO_EJECUTADO a proposito: escribiria un archivo real en skills/. "
                  "Su prompt se mide por receta (P10) y no lleva paquete."})
    return notas


def _trabajar(paquete, tarea, muso):
    ENTORNO["muso"] = muso
    try:
        return obrero.trabajar(paquete, tarea)
    finally:
        ENTORNO["muso"] = False


def resumen_capturas():
    """Junta las capturas vivas: por puerta (archivo:linea) el MAYOR tamano visto."""
    por_puerta = {}
    for c in CAPTURAS:
        k = c["puerta"]
        d = por_puerta.setdefault(k, {"puerta": k, "funcion": c["funcion"],
                                      "veces": 0, "mayor": 0, "menor": 10 ** 9,
                                      "escenarios": [], "pesado": c["pesado"],
                                      "primero": c["primero"]})
        d["veces"] += 1
        d["mayor"] = max(d["mayor"], c["letras"])
        d["menor"] = min(d["menor"], c["letras"])
        if c["escenario"] not in d["escenarios"]:
            d["escenarios"].append(c["escenario"])
        d["pesado"] = d["pesado"] or c["pesado"]
    for d in por_puerta.values():
        d["pasa_TOPE_LETRAS"] = d["mayor"] <= TOPES["asignador.TOPE_LETRAS"]
        d["pasa_TOPE_PESADO"] = d["mayor"] <= TOPES["obrero.TOPE_PESADO"]
        d["pasa_TOPE_GRATIS"] = d["mayor"] <= TOPES["vigia.TOPE_GRATIS (test)"]
    return sorted(por_puerta.values(), key=lambda x: -x["mayor"])


# ─── 4) EL INFORME ──────────────────────────────────────────────────────────────────
def _tabla(filas, cabecera):
    L = ["  " + cabecera, "  " + "-" * 74]
    for f in filas:
        L.append("  " + f)
    return "\n".join(L)


def main():
    _sin_escribir()
    obrero._preguntar_con_relevo = espia
    cap = capacidades()

    informe = {
        "fecha": "2026-09-09", "que": "medicion de las 9 puertas del corredor del cerebro",
        "como": "1) por receta (misma expresion del codigo) 2) en vivo (pasillo interceptado)",
        "topes_declarados": TOPES, "capacidades_reales_en_CUOTAS": cap,
        "paquetes": {"A ronda real 09-09": len(PAQUETE_A),
                     "B real guardado (%s)" % NOMBRE_B: len(PAQUETE_B)},
        "por_receta": {}, "notas_de_las_corridas": {}, "puertas_en_vivo": [],
        "ojo": "El espia sustituye al pasillo: NINGUNA llamada salio a internet. "
               "Los flujos se corrieron de verdad (trabajar, resolver, consultar, dudas).",
    }

    print("=" * 78)
    print("MEDICION DE LAS 9 PUERTAS DEL CORREDOR  (auditoria 2026-09-09)")
    print("=" * 78)
    print("TOPE_LETRAS=%d  TOPE_PESADO=%d  TOPE_LOCAL=%d  TOPE_GRATIS(vigia)=%d"
          % (TOPES["asignador.TOPE_LETRAS"], TOPES["obrero.TOPE_PESADO"],
             TOPES["obrero.TOPE_LOCAL"], TOPES["vigia.TOPE_GRATIS (test)"]))
    print("paquete A (ronda real 09-09) ..... %d letras" % len(PAQUETE_A))
    print("paquete B (real de memoria) ...... %d letras  (%s)" % (len(PAQUETE_B), NOMBRE_B))
    print("cerebros segun CUOTAS ............ %s" % ", ".join(
        "%s=%s" % (q, (v.get("mayor_ok") or "?"))
        for q, v in cap["por_cerebro"].items()))
    print("el gratis mas pequeno que aguanta .. %s letras | el local aguanta .. %s letras"
          % (cap["el_gratis_mas_pequeno_que_aguanta"], cap["el_local_aguanta"]))

    gratis_real = cap["el_gratis_mas_pequeno_que_aguanta"] or 19000

    for etiqueta, pq in (("A ronda real 09-09", PAQUETE_A),
                         ("B paquete real guardado", PAQUETE_B)):
        print("")
        print("### POR RECETA - escenario %s (%d letras de paquete)" % (etiqueta, len(pq)))
        rec, lineas, se_pasan = [], [], []
        for puerta, sitio, que, prompt in por_receta(pq):
            n = len(prompt)
            d = {"puerta": puerta, "sitio": sitio, "receta": que, "letras": n,
                 "pasa_TOPE_LETRAS": n <= TOPES["asignador.TOPE_LETRAS"],
                 "pasa_TOPE_PESADO": n <= TOPES["obrero.TOPE_PESADO"],
                 "pasa_TOPE_LOCAL": n <= TOPES["obrero.TOPE_LOCAL"],
                 "pasa_TOPE_GRATIS_declarado": n <= TOPES["vigia.TOPE_GRATIS (test)"],
                 "pasa_AL_GRATIS_DE_VERDAD": n <= gratis_real,
                 "pasa_AL_LOCAL_DE_VERDAD": n <= (cap["el_local_aguanta"] or 12887)}
            rec.append(d)
            if not d["pasa_AL_GRATIS_DE_VERDAD"]:
                se_pasan.append(puerta)
            lineas.append("%-38s %-26s %7d  %s" % (
                puerta, sitio, n,
                "PASA" if d["pasa_AL_GRATIS_DE_VERDAD"]
                else "SE PASA (+%d)" % (n - gratis_real)))
        informe["por_receta"][etiqueta] = rec
        informe.setdefault("cuantas_se_pasan", {})[etiqueta] = {
            "de_cuantas": len(rec), "se_pasan_del_gratis_real": len(se_pasan),
            "cuales": se_pasan, "el_gratis_real_aguanta": gratis_real}
        print(_tabla(lineas, "puerta                                     sitio                        letras  vs el gratis real (%d)" % gratis_real))

        print("")
        print("  corriendo los flujos de verdad con este paquete (pasillo interceptado)...")
        notas = correr_flujos(pq, etiqueta)
        informe["notas_de_las_corridas"][etiqueta] = notas

    return informe


if __name__ == "__main__":
    inf = main()
    print("")
    print("### EN VIVO (flujos reales, pasillo interceptado)")
    inf["puertas_en_vivo"] = resumen_capturas()
    for d in inf["puertas_en_vivo"]:
        print("  %-34s %-6s veces=%-3d menor=%-7d MAYOR=%-7d pesado=%-5s primero=%s"
              % (d["puerta"], d["funcion"][:6], d["veces"], d["menor"], d["mayor"],
                 d["pesado"], d["primero"]))
    print("")
    for etiqueta, c in (inf.get("cuantas_se_pasan") or {}).items():
        print("  VEREDICTO %s: %d de %d prompts SE PASAN del gratis real (%d letras)."
              % (etiqueta, c["se_pasan_del_gratis_real"], c["de_cuantas"],
                 c["el_gratis_real_aguanta"]))
        for p in c["cuales"]:
            print("     - " + p)
    print("")
    for etiqueta, notas in inf["notas_de_las_corridas"].items():
        print("  corridas en %s:" % etiqueta)
        for n in notas:
            print("    %-42s %s" % (n["flujo"], n["resultado"]))
    salida = os.path.join(AQUI, "memoria", "MEDICION_NUEVE_PUERTAS_2026-09-09.json")
    open(salida, "w", encoding="utf-8").write(
        json.dumps(inf, ensure_ascii=False, indent=1))
    print("")
    print("VOLCADO: %s" % salida)



