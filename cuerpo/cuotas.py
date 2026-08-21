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

# MEDIDO el 2026-08-21: Groq reparte el cupo POR MODELO, no por llave. O sea que cada modelo
# que se anade es cupo gratis DE MAS sobre la misma llave, sin pagar ni registrarse en nada.
# Julio: "por eso necesito a kimi, y a otros modelos que no duerman tanto". Kimi K2 ya venia
# incluido en su llave de Groq: 7 segundos con el paquete grande. No habia que descargar nada.
# COMPROBADO uno por uno el 2026-08-21 llamando a cada proveedor DIRECTO (sin la red que tapaba
# los errores). En la llave de Julio SOLO viven estos. Kimi (K2 y K3) y los Llama dan 404: no los
# tiene. Lo que antes parecia que funcionaba era Gemini contestando disfrazado.
#   openai/gpt-oss-120b  0.9 s     openai/gpt-oss-20b  0.9 s     gemini  (el suyo fijo)
# gpt-oss-120b y gpt-oss-20b son DOS cupos gratis distintos: Groq reparte por modelo.
ORDEN = ["groq", "groq20b", "gemini", "local"]
APODO = {"groq": "GPT-OSS 120B (Groq)", "groq20b": "GPT-OSS 20B (Groq)",
         "gemini": "Gemini", "local": "LM Studio (tu PC)"}

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
    # El cerebro de DMM esconde el error real detras de un mensaje generico
    # ("Ningun cerebro respondio: pon GEMINI_API_KEY o GROQ_API_KEY") INCLUSO cuando la llave
    # esta puesta y lo que paso fue un tope de cuota. Fallo real 2026-08-20: por eso el relevo
    # no mandaba a dormir al cerebro agotado y se reintentaba con el mismo, en balde.
    # Si se forzo un proveedor concreto y contesta eso, ESE proveedor no atendio: se releva.
    if "ningun cerebro respondio" in t or "ningún cerebro respondió" in t:
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


def apuntar_uso(quien, ok=True, segundos=None):
    d = _leer()
    g = d.setdefault("gasto", {}).setdefault(quien, {"llamadas": 0, "fallos": 0})
    g["llamadas"] += 1
    if not ok:
        g["fallos"] += 1
    if ok and segundos is not None:
        # Se guarda lo que TARDO DE VERDAD, no lo que se supone que tarda.
        g["ultimo_seg"] = round(float(segundos), 1)
        g["record_seg"] = max(round(float(segundos), 1), float(g.get("record_seg", 0)))
    _guardar(d)


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
        return float(MINIMO_ESPERA * 3)      # aun no se sabe lo que tarda: margen ancho
    return max(float(MINIMO_ESPERA), record * MARGEN)


def se_paso_de_su_marca(quien, segundos):
    """¿Tardo MAS de lo que el mismo ha tardado nunca? Entonces se descarta y se busca otro."""
    return float(segundos) > cuanto_esperarle(quien)


def turno(disponibles=None):
    """A QUIEN LE TOCA AHORA. Respeta el orden de Julio y devuelve al primero que ya desperto.
    `disponibles` = los que tienen llave/servicio; los demas ni se consideran."""
    for quien in ORDEN:
        if disponibles is not None and quien not in disponibles:
            continue
        if desperto(quien):
            return quien
    return ""


def fila(disponibles=None):
    """Todos los que pueden atender, en orden. Para intentar uno tras otro en la misma llamada."""
    return [q for q in ORDEN
            if (disponibles is None or q in disponibles) and desperto(q)]


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
