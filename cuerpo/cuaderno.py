# -*- coding: utf-8 -*-
"""cuerpo/cuaderno.py — EL CUADERNO DE LLAMADAS (CONTRATO_EL_EQUIPO_ESCRIBE, causa "propuesta vacia").

Es un PROGRAMA, no una IA: registra en disco cada llamada que sale por el relevo
(cuerpo/obrero.py::_preguntar_con_relevo) para poder CONTESTAR con datos la pregunta
de la ley: "El cuaderno de llamadas dira si sigue pasando y cuando". Sin esto no se puede
decidir nada: un cerebro que contesto vacio NO es lo mismo que uno que se corto a mitad,
ni que uno que dijo que si y el JSON venia roto. Cada causa tiene su cura.

Que se guarda por llamada (todo medido, nada opinado):
  cuando   - fecha y hora
  quien    - quien contesto (o a quien se le intento)
  tamano   - letras del encargo que llego al pasillo
  vuelta   - en que intento del trabajo (1, 2, 3)
  clase    - reparar | crear | auditar (lo que se estaba haciendo)
  resultado - ok | vacio | cortado | roto | error | no_cupo
  crudo    - las primeras letras de lo que devolvio (para ver con los ojos que paso)
"""
import os, json, time, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "CUADERNO_DE_LLAMADAS.jsonl")

MAX_LINEAS = 1000
# Los resultados posibles, para no escribir nombres raros a mano.
OK = "ok"
VACIO = "vacio"
CORTADO = "cortado"
ROTO = "roto"
ERROR = "error"
NO_CUPO = "no_cupo"


def _ruta():
    """La de verdad, o una de prueba (las vigias no tocan el cuaderno real)."""
    return os.environ.get("INGENIERO_CUADERNO_TEST") or RUTA


def apuntar(quien, tamano=0, vuelta=0, clase="", resultado=ERROR, crudo="", segundos=None):
    """Escribe una linea en el cuaderno. Nunca rompe el trabajo: si el disco falla, calla."""
    try:
        fila = {
            "cuando": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "quien": str(quien or "?"),
            "tamano": int(tamano or 0),
            "vuelta": int(vuelta or 0),
            "clase": str(clase or ""),
            "resultado": str(resultado or ERROR),
            "crudo": str(crudo or "")[:300],
        }
        if segundos is not None:
            fila["segundos"] = round(float(segundos), 1)
        ruta = _ruta()
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        lineas = []
        if os.path.exists(ruta):
            with open(ruta, encoding="utf-8") as f:
                lineas = f.readlines()
        lineas.append(json.dumps(fila, ensure_ascii=False) + "\n")
        lineas = lineas[-MAX_LINEAS:]
        with open(ruta, "w", encoding="utf-8") as f:
            f.writelines(lineas)
    except Exception:
        pass


def resumen(limite=200):
    """Cuenta los resultados por cerebro (para que el lector vea el cuadro de golpe, sin IA)."""
    totales = {}
    ultimo = {}
    try:
        with open(_ruta(), encoding="utf-8") as f:
            for linea in f.readlines()[-limite:]:
                try:
                    fila = json.loads(linea)
                except Exception:
                    continue
                quien = fila.get("quien", "?")
                r = fila.get("resultado", "?")
                c = totales.setdefault(quien, {"ok": 0, "vacio": 0, "cortado": 0,
                                               "roto": 0, "error": 0, "no_cupo": 0, "total": 0})
                c["total"] += 1
                if r in c:
                    c[r] += 1
                ultimo[quien] = fila
    except Exception:
        return {}
    return {"totales": totales, "ultimo": ultimo}