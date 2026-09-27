# -*- coding: utf-8 -*-
"""cuotas.py — EL RELEVO DE CEREBROS GRATIS (orden de Julio, 2026-08-20: critico).

Regla de Julio, literal: "gasta los token gratis de Qwen, despues los de Gemini, y cuando se
repongan los de Qwen continua con el".

Por que hace falta: las cuotas gratis no avisan que volvieron. Si nadie lleva la cuenta, el
sistema se queda pegado al segundo cerebro para siempre y se desperdicia el primero, que es
gratis y ya se repuso.

Como funciona:
  · ORDEN fijo: qwen (Groq) -> gemini -> local (LM Studio, sin cuota).
  · Cuando uno se agota (429 / quota / rate limit), se marca DORMIDO con hora de despertar.
  · En cada llamada se revisa si ya desperto. Si desperto, **se vuelve a el**, no se sigue de largo.
  · Todo se guarda en `memoria/CUOTAS.json`, asi sobrevive a que se cierre la sesion.
"""
import os, json, time, datetime, re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "CUOTAS.json")

# MEDIDO el 2026-09-27 sobre memoria/CUADERNO_DE_LLAMADAS.jsonl: de las 163 respuestas buenas de
# Big Pickle, la mas lenta tardo 314 segundos; de las 27 buenas de grok47, todas antes de 240.
# Julio, 2026-09-27: el disparador es la respuesta, no un temporizador, asi que en cuanto contesta
# no se espera ni un segundo mas; y si no contesta en 400 segundos, el encargo pasa a otro cerebro.
# Con 400 no se pierde ni una sola respuesta buena de las 163 medidas, y el peor caso baja de 600 a 400.
TECHO_ESPERA = 400

# MEDIDO el 2026-08-21: Groq reparte el cupo POR MODELO, no por llave. O sea que cada modelo
# que se anade es cupo gratis DE MAS sobre la misma llave, sin pagar ni registrarse en nada.
# Julio: "por eso necesito a kimi, y a otros modelos que no duerman tanto". Kimi K2 ya venia
# incluido en su llave de Groq: 7 segundos con el paquete grande. No habia que descargar nada.
# COMPROBADO uno por uno el 2026-08-21 llamando a cada proveedor DIRECTO (sin la red que tapaba
# los errores). En la llave de Julio SOLO viven estos. Kimi (K2 y K3) y los Llama dan 404: no los
# tiene. Lo que antes parecia que funcionaba era Gemini contestando disfrazado.
#   openai/gpt-oss-120b  0.9 s     openai/gpt-oss-20b  0.9 s     gemini  (el suyo fijo)
# gpt-oss-120b y gpt-oss-20b son DOS cupos gratis distintos: Groq reparte por modelo.
# OPENROUTER ANEXADO el 2026-08-27 con la llave de Julio, para UN solo arreglo: el equipo se
# quedaba SIN AUDITOR (Gemini agotado + los otros con 503) y sin segundo cerebro no hay 4 ojos,
# asi que ningun trabajo se podia aprobar. Julio: "la idea es no quedarse sin combustible".
# COMPROBADOS uno por uno el 2026-08-27, preguntando primero a la API cuales tienen precio CERO
# (21 modelos) y luego probandolos con una auditoria de codigo real:
#   cohere/north-mini-code:free              0.9 s  ACIERTA    256.000 de contexto
#   nvidia/nemotron-3-ultra-550b-a55b:free   3.1 s  ACIERTA  1.000.000 de contexto  <- el gigante
#   poolside/laguna-s-2.1:free               5.6 s  ACIERTA    262.000 de contexto
#   z-ai/glm-5.2:free                        429 Too Many Requests -> saturado, NO entra
# OJO CON LA CUOTA, y es distinta a la de Groq: OpenRouter da 50 llamadas al dia POR CUENTA, no
# por modelo. Tener tres aqui NO triplica nada: es para que si uno esta caido haya otro. Por eso
# van DESPUES de Groq y Gemini, que tienen mas holgura, y solo entran cuando esos se agotan.
# Medido del historial de Julio: gasta 29 llamadas al dia (202 en 7 dias), asi que 50 alcanzan.
# Van ANTES del local porque el local fallo 8 de 8 veces: un cerebro que no contesta no es relevo.
# Julio saco a los tres cerebros de OpenRouter el 2026-09-01: llave no autorizada todo el dia,
# llave presente pero sin acceso, y se les llamaba en balde en cada vuelta. Sus nombres eran
# router, router2 y router3. Si algun dia se renueva la llave, se devuelven asi: volver a poner
# los tres nombres en la lista de orden, y sus entradas en las dos tablas, con los mismos valores
# que tenian.
# A-31 (Julio 2026-09-18, gana A-9; forense en PLAN_PITS/02_FORENSE.md): salen por datos groq20b,
# gemini (Gemini 1, 92% de fallos), gemini3 (94%) y local (97%). Sus APODOS se conservan.
ORDEN = ["groq", "gemini4", "gemini2", "deepseek"]
APODO = {"groq": "GPT-OSS 120B (Groq)", "groq20b": "GPT-OSS 20B (Groq)",
         "gemini": "Gemini 3.5", "gemini2": "Gemini 3 preview",
         "gemini3": "Gemini flash-latest", "gemini4": "Gemini 2.5 flash-lite",
         "local": "LM Studio (tu PC)",
         "deepseek": "DeepSeek (SE PAGA)"}

# LOS QUE CUESTAN DINERO. Todos los de arriba son gratis menos estos.
# Julio, 2026-08-21, ordeno meter a DeepSeek en el equipo (es el mismo "4 ojos" que le contesta
# por el canal interno). Pero DeepSeek va con saldo, y a los cerebros se les pregunta A TODOS A
# LA VEZ porque "son todos gratis, preguntar no cuesta". Esa frase deja de ser verdad en cuanto
# entra uno de pago: se pagaria una llamada en CADA pregunta aunque contestase antes uno gratis.
# Lo cazo el propio DeepSeek auditando esta reparacion. Por eso quien esta aqui NO entra en la
# pregunta a la vez: se le llama A SOLAS y solo cuando ningun gratis pudo atender.
DE_PAGO = {"deepseek"}
# Julio, 2026-08-21: "tu debes ser el ultimo recurso, cuando se agoten los modelos gratis, o sea
# nunca, porque existen cientos". Su llave de Gemini tiene 37 modelos vivos. Se anaden los que se
# COMPROBARON uno por uno (3.5-flash 2.1s | 3-flash-preview 3.9s | flash-latest 3.2s; el 3.7 dio
# 503). Hacia falta de verdad: con Groq agotado y LM Studio dando error, no quedaba un segundo
# cerebro para AUDITAR, y sin segundo cerebro no hay 4 ojos: el que propone se aprueba solo.

# Cuanto duerme un cerebro agotado antes de volver a probarlo.
# Groq reparte por minuto y por dia; Gemini por minuto y por dia. Se prueba pronto y seguido:
# es gratis probar, y lo caro es NO volver al gratis cuando ya se repuso.
SIESTA = {"minuto": 90, "hora": 3700, "dia": 3600, "lento": 20}   # segundos
# "lento" duerme POCO a proposito: tardar una vez no es estar agotado. Fallo real 2026-08-20:
# se marcaba lento igual que agotado y el sistema se quedaba SIN NINGUN cerebro disponible.


def _leer():
    try:
        return json.load(open(RUTA, encoding="utf-8"))
    except Exception:
        return {"dormidos": {}, "gasto": {}, "historial": []}


def _guardar(d):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _tipo_de_agote(error_txt):
    """Que clase de tope se toco, para saber cuanto dormir."""
    t = (error_txt or "").lower()
    if t.startswith("lento") or "tardo mas de" in t:
        return "lento"
    if "per day" in t or "daily" in t or "por dia" in t:
        return "dia"
    if "per hour" in t:
        return "hora"
    return "minuto"


def es_agote(error_txt):
    """True si el error es de CUOTA (no de codigo). Solo entonces se releva."""
    t = (error_txt or "").lower()
    if any(x in t for x in ("429", "quota", "rate limit", "rate_limit",
                            "resource_exhausted", "too many requests", "exceeded")):
        return True
    # QUEDARSE SIN SALDO ES AGOTARSE, NO UN FALLO DE CODIGO (DeepSeek, 2026-08-21).
    # DeepSeek es el unico de la fila que se paga. Si se le acaba el saldo y esto no lo reconoce,
    # no se le manda a dormir y se le vuelve a llamar una y otra vez en balde. Un cerebro de pago
    # mal tratado sale MAS caro que no tenerlo.
    if any(x in t for x in ("insufficient balance", "insufficient_quota",
                            "payment required", "402")):
        return True
    # El cerebro de DMM esconde el error real detras de un mensaje generico
    # ("Ningun cerebro respondio: pon GEMINI_API_KEY o GROQ_API_KEY") INCLUSO cuando la llave
    # esta puesta y lo que paso fue un tope de cuota. Fallo real 2026-08-20: por eso el relevo
    # no mandaba a dormir al cerebro agotado y se reintentaba con el mismo, en balde.
    # Si se forzo un proveedor concreto y contesta eso, ESE proveedor no atendio: se releva.
    if "ningun cerebro respondio" in t or "ningún cerebro respondió" in t:
        return True
    # FALLO DE LLAVE, PERMISO O SERVICIO CAIDO: NO SE ARREGLAN SOLOS, SE APARTAN IGUAL QUE AGOTADOS.
    # Julio ordeno 2026-09-01: "no funcionar cuenta igual que no estar".
    if any(x in t for x in ("401", "403", "unauthorized", "forbidden",
                            "invalid api key", "invalid_api_key", "api key not valid",
                            "no auth", "authentication")):
        return True
    if any(x in t for x in ("500", "502", "503", "504", "service unavailable",
                            "bad gateway", "internal server error", "overloaded")):
        return True
    return False


def dormir(quien, error_txt=""):
    """Marca un cerebro como agotado y calcula cuando volver a probarlo."""
    d = _leer()
    tipo = _tipo_de_agote(error_txt)
    hasta = time.time() + SIESTA.get(tipo, 90)
    d["dormidos"][quien] = {"hasta": hasta, "tipo": tipo,
                            "desde": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "motivo": (error_txt or "")[:180]}
    d["historial"] = (d.get("historial", []) + [
        {"cuando": d["dormidos"][quien]["desde"], "quien": quien, "que": f"agotado ({tipo})"}])[-80:]
    _guardar(d)
    return hasta


def desperto(quien):
    """True si ya paso su siesta. Si desperto, se le quita la marca (vuelve a la fila)."""
    d = _leer()
    info = d["dormidos"].get(quien)
    if not info:
        return True
    if time.time() >= info["hasta"]:
        d["dormidos"].pop(quien, None)
        d["historial"] = (d.get("historial", []) + [
            {"cuando": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
             "quien": quien, "que": "desperto, vuelve a la fila"}])[-80:]
        _guardar(d)
        return True
    return False


def bigpickle_fallo():
    """Orden de Julio A-46 del 2026-09-21: cuenta los fallos seguidos de bigpickle.
    Al segundo fallo seguido, lo duerme 30 min la primera vez y 1 hora desde la segunda,
    y pide revisar Grok 4.7."""
    d = _leer()
    seguidos = d.setdefault("seguidos", {})
    seguidos["bigpickle"] = seguidos.get("bigpickle", 0) + 1
    if seguidos["bigpickle"] >= 2:
        descansos = d.setdefault("descansos", {}).get("bigpickle", 0)
        if descansos == 0:
            segundos = 1800
            motivo = "fallo dos veces seguidas: descansa 30 min mientras revisa Grok 4.7 (A-46)"
        else:
            segundos = 3600
            motivo = "fallo dos veces seguidas: descansa 1 hora mientras revisa Grok 4.7 (A-46)"
        d["dormidos"]["bigpickle"] = {
            "hasta": time.time() + segundos,
            "tipo": "dos_fallos",
            "desde": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "motivo": motivo}
        seguidos["bigpickle"] = 0
        d.setdefault("descansos", {})["bigpickle"] = descansos + 1
        d["historial"] = (d.get("historial", []) + [
            {"cuando": d["dormidos"]["bigpickle"]["desde"], "quien": "bigpickle",
             "que": "agotado (dos_fallos)"}])[-80:]
    _guardar(d)


def bigpickle_acierto():
    """Orden de Julio A-46 del 2026-09-21: un acierto de bigpickle borra la cuenta de fallos seguidos
    y la cuenta de descansos de bigpickle."""
    d = _leer()
    d.setdefault("seguidos", {})["bigpickle"] = 0
    d.setdefault("descansos", {})["bigpickle"] = 0
    _guardar(d)


def apuntar_uso(quien, ok=True, segundos=None, tamano=None):
    d = _leer()
    g = d.setdefault("gasto", {}).setdefault(quien, {"llamadas": 0, "fallos": 0})
    g["llamadas"] += 1
    if not ok:
        g["fallos"] += 1
    if ok and segundos is not None:
        # Se guarda lo que TARDO DE VERDAD, no lo que se supone que tarda.
        g["ultimo_seg"] = round(float(segundos), 1)
        g["record_seg"] = max(round(float(segundos), 1), float(g.get("record_seg", 0)))
    if ok and tamano is not None:
        # Se guarda el TAMANO mas grande que este cerebro manejo bien: asi no se le vuelve a dar
        # un encargo que se sabe que no va a aguantar (Julio, 2026-08-21: repartir por metricas).
        g["mayor_ok"] = max(int(g.get("mayor_ok", 0)), int(tamano))
    _guardar(d)


# Capacidad documentada (letras de encargo aprox) de cada cerebro, SEGUN LOS PROVEEDORES.
# OJO (Julio, 2026-08-21): esto es lo que DICEN los proveedores, pero Claude midio que los gratis
# se caen ~21k letras aunque su contexto sea enorme. Por eso NO se legisla con esto: `medir_capacidad.py`
# mide la capacidad REAL y la guarda en memoria/CAPACIDADES.json, que es lo que manda de verdad.
# FALLO REAL 2026-08-27, y es una trampa cerrada: un cerebro que NO figure aqui entra con
# capacidad CERO, y `rankear` descarta a todo el que no aguante el encargo. O sea: nunca se le
# llama, y como nunca se le llama nunca mide cuanto aguanta. Queda de adorno para siempre.
# Se cazo asi: se anadio OpenRouter a la fila, quedaron 11 cerebros, y el equipo siguio diciendo
# "no quedo un segundo cerebro libre para auditar". Los tres router (y gemini4, anadido ese mismo
# dia) estaban en la fila pero invisibles. Por eso ahora TODO el que entre en ORDEN entra tambien
# aqui. Los numeros son en LETRAS y van por lo bajo a proposito: si uno revienta, `no_cupo` baja
# el techo solo; si aguanta mas, `mayor_ok` lo sube solo. Lo caro es quedarse en cero.
CAPACIDAD = {"local": 26000, "groq": 500000, "groq20b": 500000,
             "gemini": 4000000, "gemini2": 4000000, "gemini3": 4000000,
             "gemini4": 4000000, "deepseek": 250000,
             # OpenRouter, por el contexto que declara cada uno (probados el 2026-08-27):
             "router": 400000,      # cohere/north-mini-code   256.000 de contexto
             "router2": 1000000,    # nvidia/nemotron-3-ultra  1.000.000 de contexto
             "router3": 400000}     # poolside/laguna-s        262.000 de contexto


def _medidas():
    """Capacidad MEDIDA de verdad (memoria/CAPACIDADES.json), hecha con medir_capacidad.py.
    Formato: {quien: {"max": letras, "tipo": OK/LENTO/CAPACIDAD/RATE, "detalle": {...}}}."""
    try:
        d = json.load(open(os.path.join(AQUI, "memoria", "CAPACIDADES.json"), encoding="utf-8"))
    except Exception:
        return {}
    return {k: (v.get("max", 0) if isinstance(v, dict) else int(v)) for k, v in d.items()}


def es_no_cupo(msg):
    """¿Este fallo es 'no me cabe el material'? (y no cuota, ni servicio caido, ni sin llave).

    Las frases son las REALES que devolvieron los cerebros el 2026-08-24 trabajando sobre Foto
    Informe, no inventadas: 413 Payload Too Large una y otra vez, todo el dia.
    Distinguirlo importa: a un agote se le manda a dormir un rato, pero a quien NO LE CABE hay
    que bajarle el techo, porque dormir no le va a hacer mas grande.
    """
    t = str(msg or "").lower()
    if not t:
        return False
    señales = ("413", "payload too large", "request entity too large", "request too large",
               "too large for model", "maximum context length", "context length exceeded",
               "context_length_exceeded", "input is too long", "prompt is too long")
    return any(s in t for s in señales)


def apuntar_no_cupo(quien, tamano):
    """A este cerebro NO LE CUPO un encargo de este tamaño. Se le baja el techo.

    Es el UNICO numero del sistema que puede bajar, y tiene que poder bajar: bajarlo ES la
    leccion. Se queda con la evidencia mas dura (el tamaño MAS PEQUENO que ya reviento), para
    que un fallo posterior mas grande no borre lo que ya se sabe.

    Ley: CONTRATO_EQUIPO_QUE_AGUANTA.md
    """
    try:
        tamano = int(tamano)
    except Exception:
        return
    if tamano <= 0:
        return
    d = _leer()
    g = d.setdefault("gasto", {}).setdefault(quien, {"llamadas": 0, "fallos": 0})
    anterior = int(g.get("no_cupo", 0) or 0)
    g["no_cupo"] = tamano if anterior <= 0 else min(anterior, tamano)
    _guardar(d)


def _capacidad(quien):
    """Cuanto aguanta DE VERDAD.

    Antes era: lo medido o la promesa del proveedor, lo que sea MAYOR. Y ahi estaba el fallo
    (2026-08-24): la promesa siempre ganaba y nunca bajaba. Groq figuraba con 500.000 letras
    mientras devolvia 413 Payload Too Large en TODAS las llamadas sobre Foto Informe, y se le
    seguia eligiendo en cada intento. Asi el equipo no podia auditar ese proyecto, y "auditado"
    acabo significando "alguien dijo que si sin haber visto nada" — que es como llego a manos de
    Julio una prueba con cinco fallos, uno de ellos capaz de borrarle textos suyos.

    Ahora manda la EVIDENCIA sobre la promesa: si ya reviento con un tamaño, el techo se queda
    POR DEBAJO de ese tamaño (no en el, o volveria a admitirse el mismo encargo).
    """
    g = _leer().get("gasto", {}).get(quien, {})
    medido = max(int(g.get("mayor_ok", 0)), int(_medidas().get(quien, 0)))
    cabe = medido if medido > 0 else int(CAPACIDAD.get(quien, 0))
    no_cupo = int(g.get("no_cupo", 0) or 0)
    if no_cupo > 0:
        cabe = min(cabe, no_cupo - 1)
    return max(0, cabe)


def rankear(disponibles, tamano):
    """Del MAS eficiente al MENOS, entre los que aguantan este tamano.

    Julio, 2026-08-21: "donde veas cual es mas eficiente, del mayor al menor, y asi se asignen
    las tareas... es estupido darle una tarea a una IA que sabes que no va a soportar."
    Antes se les preguntaba a TODOS a la vez y gana el primero: eso gastaba tokens en todos y les
    mandaba trabajo que no aguantan. Ahora se ordena por fiabilidad x rapidez y se SALTAN los
    que no soportan el encargo.
    """
    elegibles = [q for q in disponibles if tamano <= _capacidad(q)]

    def score(q):
        g = _leer().get("gasto", {}).get(q, {})
        llam = float(g.get("llamadas", 0))
        fall = float(g.get("fallos", 0))
        conf = (llam - fall) / llam if llam > 0 else 0.0     # fiabilidad (sin fallos)
        vel = 1.0 / (1.0 + float(g.get("record_seg", 0)))    # rapidez (mas lento = menos)
        # Penaliza a los que fallan mucho: si falla el 98%, su score se divide por 50.
        penal = 1.0 / (1.0 + fall) if llam > 0 else 1.0
        return round(conf * vel * penal, 6)

    return sorted(elegibles, key=score, reverse=True)


MARGEN = 1.5          # se le da la mitad mas de su propio record antes de descartarlo
MINIMO_ESPERA = 60    # Julio: "puedo ser un poco flexible con el tiempo, solo un poco"


def cuanto_esperarle(quien):
    """CUANTO SE LE AGUANTA A ESTE CEREBRO, segun lo que EL ha tardado de verdad.

    Julio, 2026-08-21: "mira cual es el mayor tiempo de respuesta registrado y que esa sea la
    base: si responde en ese rango se sigue trabajando con el, si se pasa lo descartamos y
    buscamos otros. Y que el disparador sea la respuesta del modelo, no un temporizador, porque
    ante cualquier demora te envia a ti, y tu debes ser el ULTIMO recurso, cuando se agoten los
    modelos gratis, o sea nunca, porque existen cientos."

    Un tope inventado, igual para todos, hacia dos destrozos: descartaba a uno que iba a contestar
    bien, y mandaba el trabajo a la IA cara, que la paga Julio. Ahora el tope sale de su propio
    historial: cada cerebro se mide contra si mismo."""
    g = _leer().get("gasto", {}).get(quien, {})
    record = float(g.get("record_seg", 0))
    if record <= 0:
        return min(float(TECHO_ESPERA), float(MINIMO_ESPERA * 3))  # aun no se sabe lo que tarda: margen ancho, topado
    return min(float(TECHO_ESPERA), max(float(MINIMO_ESPERA), record * MARGEN))


def se_paso_de_su_marca(quien, segundos):
    """¿Tardo MAS de lo que el mismo ha tardado nunca? Entonces se descarta y se busca otro."""
    return float(segundos) > cuanto_esperarle(quien)


def espera_de_bigpickle(letras):
    """CUANTO ESPERARLE A BIG PICKLE, segun lo que tarda de verdad con tareas de ese tamano.

    Orden de Julio A-47 del 2026-09-21: la espera sale de lo que Big Pickle tarda de verdad con
    tareas de ese tamano, nunca menor, para no descartarlo por darle un tiempo que no le
    corresponde ni esperar de mas en una tarea chica. Completa la ley del 2026-08-21 de
    cuanto_esperarle.

    Lee las filas del cuaderno de llamadas (cuerpo/cuaderno.py::_ruta()). Solo cuentan las
    filas con quien == 'bigpickle', resultado == cuaderno.OK y segundos mayor que 0.
    Parecidas = las filas con tamano entre letras/2 y letras*2 (y tamano mayor que 0).
    Si hay 5 o mas parecidas: devuelve max(MINIMO_ESPERA, el mayor segundos de las parecidas
    por MARGEN). Si no: devuelve max(MINIMO_ESPERA, el mayor segundos de todas por MARGEN).
    Sin filas: devuelve 600.0."""
    from cuerpo import cuaderno
    filas = []
    try:
        with open(cuaderno._ruta(), encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    fila = json.loads(linea)
                except Exception:
                    continue
                if not isinstance(fila, dict):
                    continue
                if fila.get("quien") != "bigpickle":
                    continue
                if fila.get("resultado") != cuaderno.OK:
                    continue
                try:
                    seg = float(fila.get("segundos") or 0)
                except Exception:
                    continue
                if seg <= 0:
                    continue
                try:
                    tam = int(fila.get("tamano") or 0)
                except Exception:
                    tam = 0
                filas.append({"segundos": seg, "tamano": tam})
    except Exception:
        filas = []
    if not filas:
        return 600.0
    try:
        letras = float(letras)
    except Exception:
        letras = 0.0
    parecidas = [f for f in filas
                 if f["tamano"] > 0 and letras / 2.0 <= f["tamano"] <= letras * 2.0]
    if len(parecidas) >= 5:
        mayor = max(f["segundos"] for f in parecidas)
    else:
        mayor = max(f["segundos"] for f in filas)
    return max(float(MINIMO_ESPERA), mayor * MARGEN)


def turno(disponibles=None):
    """A QUIEN LE TOCA AHORA. Respeta el orden de Julio y devuelve al primero que ya desperto.
    `disponibles` = los que tienen llave/servicio; los demas ni se consideran."""
    for quien in ORDEN:
        if disponibles is not None and quien not in disponibles:
            continue
        if desperto(quien):
            return quien
    return ""


def acierto_de(quien):
    """Cuenta los renglones donde ese cerebro escribio y devuelve que parte acabo en APROBADO.
    Entre 0 y 1. None con menos de tres trabajos. NUNCA lanza."""
    # SE REUSA AQUI, QUE ES LA CONSTANTE QUE YA EXISTE ARRIBA EN ESTE MISMO ARCHIVO.
    #
    # FALLO CAZADO EL 2026-09-12, y es de libro: la primera version usaba una constante CASA que
    # NO EXISTE en esta pieza. Eso reventaba, el "nunca lanza" se lo tragaba en silencio, y
    # acierto_de devolvia "sin datos" para todos PARA SIEMPRE. La vigia estaba verde porque las
    # pruebas le ponen los aciertos a mano; en la casa real no funcionaba nada.
    #
    # NO SE VIO LEYENDO: se vio corriendolo contra el registro de verdad, que tiene 1424
    # renglones. Un "nunca lanza" mal puesto no protege: ESCONDE. Por eso se mira tambien que la
    # cuenta de la casa real de un numero, no solo que la vigia este verde.
    #
    # Y SE MIRA QUIEN ESCRIBIO, NO EL RENGLON ENTERO: el nombre de un cerebro aparece tambien
    # como REVISOR, y contar esos renglones le atribuiria al obrero el trabajo de otro.
    try:
        ruta = os.path.join(AQUI, "memoria", "TRABAJOS_DEL_EQUIPO.log")
        if not os.path.exists(ruta):
            return None
        total = 0
        aprobados = 0
        with open(ruta, encoding="utf-8", errors="replace") as _f:
            _renglones = _f.read().splitlines()
        for linea in _renglones:
            partes = [p.strip() for p in linea.split("|")]
            if len(partes) < 4:
                continue
            if partes[1].replace("escribio", "").strip() != quien:
                continue
            total += 1
            if partes[3].startswith("APROBADO"):
                aprobados += 1
        if total < 3:
            return None
        return aprobados / total
    except Exception:
        return None


def fila(disponibles=None):
    """Todos los que pueden atender, en orden. Para intentar uno tras otro en la misma llamada.
    Ordenados por acierto de mayor a menor; los que no tienen dato van al final, en su orden de siempre."""
    candidatos = [q for q in ORDEN
                  if (disponibles is None or q in disponibles) and desperto(q)]
    return sorted(candidatos, key=lambda q: (acierto_de(q) is not None, acierto_de(q) or 0.0), reverse=True)


def puede_revisar_claude(escritor, dormidos):
    # Ley Julio 2026-09-14: Claude revisa a DeepSeek solo si todas las IA gratis duermen.
    if escritor == 'claude':
        return False
    gratis = [q for q in ORDEN if not q.startswith('deepseek')]
    return all(q in dormidos for q in gratis)

def puede_revisar_bigpickle(escritor, dormidos):
    # A-32 (Julio 2026-09-18): si todas las IA gratis duermen, revisa Big Pickle, nunca Claude; y nunca lo que escribio Big Pickle.
    if escritor == 'bigpickle':
        return False
    gratis = [q for q in ORDEN if not q.startswith('deepseek')]
    return all(q in dormidos for q in gratis)


def estado_texto():
    d = _leer()
    L = ["RELEVO DE CEREBROS GRATIS (orden de Julio: Qwen -> Gemini -> local -> vuelta a Qwen)"]
    for q in ORDEN:
        info = d["dormidos"].get(q)
        g = d.get("gasto", {}).get(q, {})
        uso = f"{g.get('llamadas', 0)} llamadas, {g.get('fallos', 0)} fallos"
        if info and time.time() < info["hasta"]:
            faltan = int(info["hasta"] - time.time())
            L.append(f"  {APODO[q]:18} DORMIDO {faltan//60}m {faltan%60}s (tope por {info['tipo']}) — {uso}")
        else:
            L.append(f"  {APODO[q]:18} LISTO — {uso}")
    t = turno()
    L.append(f"  -> le toca a: {APODO.get(t, 'NINGUNO (todos agotados)')}")
    return "\n".join(L)
