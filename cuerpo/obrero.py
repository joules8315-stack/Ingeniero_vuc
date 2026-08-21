# -*- coding: utf-8 -*-
"""cuerpo/obrero.py — EL OBRERO. Quien hace el trabajo pesado: el cerebro GRATIS, no Claude.

Manda el CONTRATO_MAESTRO_AHORRO de DMM:
  · Claude (caro)  = dirige y revisa. Lee VEREDICTOS, nunca volumenes.
  · Qwen  (Groq)   = Frente 2 / Ingeniero: GENERA.
  · Gemini         = AUDITA lo que genero Qwen (los "4 ojos").

Aqui no se duplica el cerebro (Ley 6, no repetidera): se TOMA PRESTADO el de DMM
(`cuerpo/cerebro.py` + `cuerpo/config.py`), que ya esta probado y ya sabe leer el `.env`.
Si DMM no esta en la maquina, se dice NO_ENCONTRADO. No se inventa un cerebro de repuesto.
"""
import os, sys, json, re, threading, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cerebro import grafo      # noqa: E402
from cuerpo import cuotas      # noqa: E402

_prestado = {}


def _cargar_por_ruta(nombre, ruta):
    """Carga un modulo por su RUTA, con nombre propio. Hace falta porque el Ingeniero tiene su
    propio paquete `cuerpo` y DMM tambien: un `from cuerpo import cerebro` normal agarra el
    equivocado (fallo real 2026-08-20)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def prestar_cerebro():
    """Trae el cerebro de DMM sin copiarlo. Devuelve (cerebro, config) o (None, None)."""
    if _prestado:
        return _prestado.get("cerebro"), _prestado.get("config")
    prs = grafo.proyectos()
    raiz = prs.get("dmm", {}).get("ruta", "")
    cbo = os.path.join(raiz, "cuerpo")
    if not raiz or not os.path.isdir(cbo):
        return None, None
    try:
        cf = _cargar_por_ruta("dmm_config", os.path.join(cbo, "config.py"))
        c = _cargar_por_ruta("dmm_cerebro", os.path.join(cbo, "cerebro.py"))
        if not c or not cf:
            return None, None
        cf.asegurar_cargado()
        _prestado["cerebro"], _prestado["config"] = c, cf
        return c, cf
    except Exception as e:
        _prestado["_error"] = str(e)
        return None, None


def disponible():
    c, cf = prestar_cerebro()
    if not c:
        return False, "NO_ENCONTRADO: no se pudo tomar prestado el cerebro de DMM"
    if not cf.hay_cerebro():
        return False, "NO_ENCONTRADO: no hay llave ni modelo local (revisa el .env de DMM)"
    return True, c.proveedor()


# ─── los prompts: cortos, con el paquete dentro, y prohibicion de inventar ──────────
def _prompt_obrero(paquete, tarea):
    return f"""Eres el OBRERO de un ingeniero de software. Trabajas SOLO con el material de abajo.

REGLAS DURAS (si las rompes, tu trabajo se descarta):
1. NO inventes archivos, funciones ni lineas. Si algo no esta en el material, escribe NO_ENCONTRADO.
2. NO decidas lo que el contrato no dice. Escribe PREGUNTA_REQUERIDA: <la pregunta en palabras simples>.
3. Cambia lo MINIMO. Nombra el archivo y la linea exacta de cada cambio.
4. Antes de terminar, di a quien puedes danar (mira la seccion "A QUIEN PUEDE DANAR").

TAREA: {tarea}

Responde SOLO un JSON valido, sin texto alrededor:
{{"diagnostico": "que esta mal, en una frase",
  "archivo": "ruta exacta del material",
  "lineas": "desde-hasta",
  "cambio": "que hay que cambiar, concreto",
  "codigo": "el codigo nuevo, solo el pedazo",
  "vigia": "que prueba lo comprobaria",
  "puede_danar": ["pieza1", "pieza2"],
  "preguntas": ["si falta decidir algo"],
  "confianza": "alta|media|baja"}}

===== MATERIAL (esto es TODO lo que existe) =====
{paquete}
===== FIN DEL MATERIAL ====="""


def _prompt_auditor(paquete, propuesta):
    return f"""Eres el AUDITOR. Otro modelo propuso una reparacion. Tu trabajo es buscarle el error,
no felicitarlo. Se duro y concreto.

Comprueba una por una:
1. INVENTO algo? (archivo/funcion/linea que no aparece en el material) -> es el fallo mas grave.
2. El cambio arregla de verdad lo que dice el diagnostico?
3. Rompe algun vecino de la seccion "A QUIEN PUEDE DANAR"?
4. Se salta alguna ley del contrato que viene en el material?
5. Cambia mas de lo necesario?

Responde SOLO JSON:
{{"veredicto": "APROBADO|RECHAZADO|DUDOSO",
  "invento_algo": true/false,
  "que_invento": ["..."],
  "fallos": ["fallo concreto 1", "..."],
  "riesgo_vecinos": ["..."],
  "que_falta": ["..."],
  "resumen_para_el_jefe": "una frase para que el director decida sin leer todo"}}

===== PROPUESTA A AUDITAR =====
{propuesta}
===== MATERIAL ORIGINAL =====
{paquete}
===== FIN ====="""


def _json_de(texto):
    """Saca el JSON aunque venga con ```json alrededor. Si no hay, lo dice; no lo inventa."""
    if not texto:
        return {"_error": "el cerebro no contesto nada"}
    m = re.search(r"\{.*\}", texto, re.S)
    if not m:
        return {"_error": "el cerebro no devolvio JSON", "_crudo": texto[:400]}
    try:
        return json.loads(m.group(0))
    except Exception:
        try:
            return json.loads(re.sub(r",\s*([}\]])", r"\1", m.group(0)))
        except Exception as e:
            return {"_error": f"JSON roto: {e}", "_crudo": m.group(0)[:400]}


def quienes_hay():
    """Que cerebros tienen con que atender AHORA (llave o servicio)."""
    c, cf = prestar_cerebro()
    if not c:
        return []
    hay = []
    if os.environ.get("GROQ_API_KEY", "").strip():
        hay.append("groq")
    if os.environ.get("GEMINI_API_KEY", "").strip():
        hay.append("gemini")
    # LM Studio se DETECTA, no se declara. Fallo real 2026-08-20: estaba encendido y
    # sirviendo qwen2.5-coder, pero como no habia variable de entorno el Ingeniero no lo veia,
    # y se quedaba sin cerebro cuando los de la nube tardaban. El local no tiene cuota ni
    # latencia caprichosa: es la red de seguridad.
    if os.environ.get("DMM_LOCAL", "").strip() or os.environ.get("LMSTUDIO_URL", "").strip()             or _local_responde():
        hay.append("local")
    return hay


def _local_responde(url=None, espera=3):
    """True si LM Studio esta escuchando de verdad. Se comprueba, no se supone."""
    import urllib.request
    url = (url or os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1")).rstrip("/")
    try:
        with urllib.request.urlopen(url + "/models", timeout=espera) as r:
            return r.status == 200
    except Exception:
        return False


def _modelo_local(url=None):
    """Que modelo esta sirviendo LM Studio ahora mismo. Se pregunta, no se adivina."""
    import urllib.request, json as _j
    url = (url or os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1")).rstrip("/")
    try:
        with urllib.request.urlopen(url + "/models", timeout=3) as r:
            datos = _j.load(r).get("data", [])
        for m in datos:                      # el de embeddings no sirve para conversar
            if "embed" not in m.get("id", "").lower():
                return m["id"]
    except Exception:
        pass
    return os.environ.get("LMSTUDIO_MODEL", "qwen2.5-coder-1.5b-instruct")


def preguntar_local(prompt, temperatura=0.2, espera=180):
    """Habla con LM Studio DIRECTAMENTE, sin pasar por el cerebro de DMM.

    Fallo real 2026-08-20: `cerebro.preguntar(forzar='local')` de DMM se iba a Gemini igual y
    devolvia 404 tras 305 segundos. El local es la RED DE SEGURIDAD (sin cuota, sin latencia
    caprichosa): tiene que funcionar aunque el cerebro prestado falle.
    """
    import urllib.request, json as _j
    url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1").rstrip("/")
    datos = _j.dumps({"model": _modelo_local(url),
                      "messages": [{"role": "user", "content": prompt}],
                      "temperature": temperatura, "max_tokens": 2000}).encode("utf-8")
    req = urllib.request.Request(url + "/chat/completions", data=datos, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=espera) as r:
        d = _j.load(r)
    return d["choices"][0]["message"]["content"]


def _velocidad():
    """Lee arnes/velocidad.config: que modelo usar y cuanto se espera antes de pasar turno."""
    d = {"modelo_groq": "llama-3.3-70b-versatile", "modelo_gemini": "gemini-2.0-flash",
         "tope_segundos": "75"}
    try:
        for ln in open(os.path.join(AQUI, "arnes", "velocidad.config"), encoding="utf-8").read().splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                d[k.strip()] = v.strip()
    except Exception:
        pass
    return d


def _con_tope(fn, segundos):
    """Corre fn con tope de tiempo. Si se pasa, se abandona y pasa el turno.
    Medido el 2026-08-20: qwen3.6-27b tardaba >300s con un paquete normal. Julio: nada lento."""
    caja = {}

    def _correr():
        try:
            caja["r"] = fn()
        except Exception as e:
            caja["e"] = e

    h = threading.Thread(target=_correr, daemon=True)
    h.start()
    h.join(segundos)
    if h.is_alive():
        raise TimeoutError(f"tardo mas de {segundos}s")
    if "e" in caja:
        raise caja["e"]
    return caja.get("r", "")


def _gemini_directo(prompt, temperatura, modelo):
    """Le habla a Gemini con EL MODELO QUE ELIGE EL INGENIERO.

    Hacia falta porque el cerebro prestado tenia quemados dos modelos que YA NO EXISTEN
    (gemini-2.0-flash y de respaldo gemini-1.5-flash): los dos daban 404. Por eso Gemini fallaba
    4 de cada 7 veces y el trabajo nunca acababa en el cerebro gratis, sino en la IA cara, o sea
    Julio pagando. Fallo real 2026-08-21, el que mas dinero le costo.
    MEDIDO ese dia con el paquete grande: 3.5-flash 3.3s | 3-flash-preview 3.4s | latest 9.3s |
    3.7-flash 29.1s | 3.6-flash 62.8s | 2.5-flash y 2.0-flash: 404, muertos."""
    import json as _j, os as _o, urllib.request as _u, urllib.parse as _up
    k = _o.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        raise RuntimeError("no hay llave de Gemini")
    body = _j.dumps({"contents": [{"parts": [{"text": prompt}]}],
                     "generationConfig": {"temperature": temperatura,
                                          "maxOutputTokens": 2000}}).encode("utf-8")
    url = ("https://generativelanguage.googleapis.com/v1beta/models/" + modelo +
           ":generateContent?key=" + _up.quote(k))
    req = _u.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    with _u.urlopen(req, timeout=300) as r:
        d = _j.load(r)
    return d["candidates"][0]["content"]["parts"][0]["text"]


def _preguntar_con_relevo(prompt, temperatura, evitar=None, primero=None):
    """Pregunta respetando el orden de Julio: Qwen -> Gemini -> local, y VOLVIENDO a Qwen
    en cuanto despierte. Si uno se agota (429/cuota), se le marca la siesta y sigue el de al lado.
    Devuelve (texto, quien_contesto, avisos)."""
    c, _ = prestar_cerebro()
    if not c:
        return "", "", ["NO_ENCONTRADO: sin cerebro"]
    hay = [q for q in quienes_hay() if q != (evitar or "")]
    turnos = cuotas.fila(hay) or hay          # si todos duermen, se intenta igual (por si desperto ya)
    if primero and primero in turnos:         # el que reparte el trabajo cruzado manda
        turnos = [primero] + [q for q in turnos if q != primero]
    avisos = []
    vel = _velocidad()
    # Cada modelo de Groq es un cupo gratis distinto: Groq reparte POR MODELO, no por llave.
    modelos = {"groq": vel["modelo_groq"], "groq20b": vel.get("modelo_groq20b"),
               "gemini": vel["modelo_gemini"], "local": None}
    tope = float(vel.get("tope_segundos", 75))

    def _pedirle_a(quien):
        """Le habla a UN cerebro. Directo, con su modelo, sin red que tape errores."""
        if quien == "local":
            return preguntar_local(prompt, temperatura)
        if quien == "gemini":
            return _gemini_directo(prompt, temperatura, modelos.get("gemini"))
        return c._preguntar_groq(prompt, modelos.get(quien), temperatura)

    # GANA EL PRIMERO QUE CONTESTE, no el reloj (Julio, 2026-08-21):
    #   "en vez de usar temporizador con los cerebros, pon mejor disparador, cuando responda, y un
    #    temporizador mas amplio. Puedo ser un poco flexible con el tiempo, solo un poco, mas no
    #    con la precision: aqui si es clave ser implacable."
    # Antes se preguntaba de uno en uno y se cortaba por reloj: si el primero tardaba, se perdia
    # ese tiempo ENTERO antes de probar el siguiente, y a veces se descartaba a uno que iba a
    # contestar bien. Ahora se les pregunta A LA VEZ —son todos gratis, preguntar no cuesta— y se
    # coge la primera respuesta VALIDA. Flexible con el tiempo, implacable con la precision: una
    # respuesta vacia NO vale, y un modelo que no existe da error a la vista, no se disimula.
    if len(turnos) > 1:
        import concurrent.futures as _cf
        # Se le aguanta a CADA UNO segun su propio record. Se espera al mas paciente de los que
        # hay: descartar antes de tiempo es lo que mandaba el trabajo a la IA cara.
        espera = max(cuotas.cuanto_esperarle(q) for q in turnos)
        arranque = time.time()
        with _cf.ThreadPoolExecutor(max_workers=len(turnos)) as pool:
            pendientes = {pool.submit(_pedirle_a, q): q for q in turnos}
            try:
                for fut in _cf.as_completed(pendientes, timeout=espera):
                    quien = pendientes[fut]
                    tardo = time.time() - arranque
                    try:
                        txt = fut.result()
                    except Exception as e:
                        cuotas.apuntar_uso(quien, ok=False)
                        msg = str(e)
                        if cuotas.es_agote(msg):
                            cuotas.dormir(quien, msg)
                            avisos.append(f"{cuotas.APODO[quien]} se agoto")
                        else:
                            avisos.append(f"{cuotas.APODO[quien]} fallo: {msg[:90]}")
                        continue
                    if not (txt or "").strip():        # implacable con la precision
                        cuotas.apuntar_uso(quien, ok=False)
                        avisos.append(f"{cuotas.APODO[quien]} contesto vacio -> no vale")
                        continue
                    if cuotas.se_paso_de_su_marca(quien, tardo):
                        # Contesto, pero mucho peor que su propia marca: se sigue usando su
                        # respuesta (ya esta pagada y es buena) y queda apuntado que va lento.
                        avisos.append("%s tardo %.0fs, mas de su marca (%.0fs)"
                                      % (cuotas.APODO[quien], tardo,
                                         cuotas.cuanto_esperarle(quien)))
                    cuotas.apuntar_uso(quien, ok=True, segundos=tardo)
                    return txt, quien, avisos
            except _cf.TimeoutError:
                avisos.append(f"ninguno de los {len(turnos)} contesto en {int(espera)}s")
        return "", "", avisos + ["NO_ENCONTRADO: ningun cerebro gratis pudo atender"]

    for quien in turnos:
        try:
            # SE LLAMA A CADA CEREBRO DIRECTO, a proposito.
            # Fallo real 2026-08-21, el que mas dinero le costo a Julio: la puerta comoda
            # (`preguntar(forzar=...)`) hacia DOS cosas a escondidas. Uno: a Gemini le quitaba el
            # modelo pedido y usaba siempre el suyo. Dos: si el modelo pedido no existia, en vez
            # de avisar caia CALLANDO en otro cerebro y contestaba como si tal cosa. Resultado:
            # se creia estar midiendo y eligiendo cerebros, y siempre contestaba el mismo. Se
            # descubrio porque un modelo inventado, "pepito-grillo-9000", contesto tan tranquilo.
            if quien == "local":
                txt = _con_tope(lambda: preguntar_local(prompt, temperatura), tope)
            elif quien == "gemini":
                gm = modelos.get("gemini")
                txt = _con_tope(lambda: _gemini_directo(prompt, temperatura, gm), tope)
            else:
                mod = modelos.get(quien)
                txt = _con_tope(lambda: c._preguntar_groq(prompt, mod, temperatura), tope)
            if not (txt or "").strip():
                raise ValueError("contesto vacio")
            cuotas.apuntar_uso(quien, ok=True)
            return txt, quien, avisos
        except TimeoutError as e:
            cuotas.apuntar_uso(quien, ok=False)
            cuotas.dormir(quien, "LENTO: " + str(e))
            avisos.append(f"{cuotas.APODO[quien]} tardo demasiado -> pasa el turno")
            continue
        except Exception as e:
            msg = str(e)
            cuotas.apuntar_uso(quien, ok=False)
            if cuotas.es_agote(msg):
                cuotas.dormir(quien, msg)
                avisos.append(f"{cuotas.APODO[quien]} se agoto -> pasa el turno")
            else:
                avisos.append(f"{cuotas.APODO[quien]} fallo (no es cuota): {msg[:90]}")
    return "", "", avisos + ["NO_ENCONTRADO: ningun cerebro gratis pudo atender"]


def trabajar(paquete, tarea, generador=None, auditor=None):
    """Un cerebro GENERA, OTRO distinto AUDITA (4 ojos). Quien es cada uno lo decide el relevo
    de cuotas, no una lista fija: asi nunca se para el trabajo por una cuota agotada."""
    c, _ = prestar_cerebro()
    if not c:
        return {"_error": "NO_ENCONTRADO: no se pudo tomar prestado el cerebro de DMM"}
    if not quienes_hay():
        return {"_error": "NO_ENCONTRADO: no hay llave ni modelo local (revisa el .env de DMM)"}

    crudo, quien_gen, av1 = _preguntar_con_relevo(_prompt_obrero(paquete, tarea), 0.2)
    if not crudo:
        return {"_error": "; ".join(av1)}
    propuesta = _json_de(crudo)

    # el auditor NUNCA puede ser el mismo que genero: si no, se aprueba a si mismo.
    crudo_a, quien_aud, av2 = _preguntar_con_relevo(
        _prompt_auditor(paquete, json.dumps(propuesta, ensure_ascii=False)), 0.1, evitar=quien_gen)
    if not crudo_a:
        auditoria = {"veredicto": "SIN_AUDITAR", "_error": "; ".join(av2),
                     "resumen_para_el_jefe": "no quedo un segundo cerebro libre para auditar"}
    else:
        auditoria = _json_de(crudo_a)

    return {"obrero": quien_gen, "auditor": quien_aud or "(ninguno)",
            "propuesta": propuesta, "auditoria": auditoria,
            "avisos": av1 + av2}


def veredicto_corto(r):
    """Lo UNICO que deberia leer Claude. Pocas lineas."""
    if "_error" in r:
        return f"NO SE PUDO: {r['_error']}"
    p, a = r.get("propuesta", {}), r.get("auditoria", {})
    L = [f"OBRERO {r['obrero']} -> AUDITOR {r['auditor']}"]
    # OJO: no llamar 'a' a esto. Antes se llamaba 'a' y PISABA la auditoria de arriba, asi que
    # leer el veredicto reventaba justo cuando habia avisos, que es cuando mas falta hace leerlo.
    for aviso in (r.get("avisos") or [])[:3]:
        L.append(f"  aviso       : {aviso}")
    if "_error" in p:
        L.append(f"  propuesta ILEGIBLE: {p['_error']}")
        return "\n".join(L)
    L.append(f"  diagnostico : {p.get('diagnostico', '?')}")
    L.append(f"  toca        : {p.get('archivo', '?')} lineas {p.get('lineas', '?')}")
    L.append(f"  confianza   : {p.get('confianza', '?')}")
    if p.get("preguntas"):
        L.append(f"  PREGUNTA_REQUERIDA: {'; '.join(p['preguntas'])}")
    v = a.get("veredicto", "?")
    L.append(f"  VEREDICTO   : {v}")
    if a.get("invento_algo"):
        L.append(f"  *** INVENTO: {'; '.join(a.get('que_invento', []))} -> SE DESCARTA")
    for f in (a.get("fallos") or [])[:4]:
        L.append(f"  fallo       : {f}")
    if a.get("resumen_para_el_jefe"):
        L.append(f"  resumen     : {a['resumen_para_el_jefe']}")
    return "\n".join(L)
