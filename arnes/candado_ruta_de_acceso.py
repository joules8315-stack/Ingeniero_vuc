# -*- coding: utf-8 -*-
"""arnes/candado_ruta_de_acceso.py — EL PLAN APROBADO DICE QUE SE PUEDE TOCAR. NADA MAS.

Julio, 2026-09-06:
  "Cuando pidas permiso debe haber una ruta clara de lo que se va a tocar, para que no toque
   nada mas, y esto lo define el plan. Una vez aprobado el plan, este debe tener todo lo que
   necesita acceso, y pedir acceso para eso unicamente. Legislado fuerte, con candado,
   blindado y con super vigia."

POR QUE EXISTE (el numero que lo justifica):
  El permiso que Julio dio el 2026-09-05 abre los DOCE candados a la vez durante 24 horas, y
  no limita QUE se toca. Eso choca de frente con su propia ley de la llave unica: "no se abren
  los 12 candados de golpe; se abren solo los que la tarea necesita, y antes se dice cuales".

LO QUE HACE, en simple:
  - Si hay un PLAN APROBADO vigente, solo se puede tocar lo que ese plan declaro.
  - Fuera de esa lista NO se toca nada, AUNQUE los candados esten apagados por autorizacion.
    Eso es el blindaje: la autorizacion de Julio deja de ser barra libre.
  - Si NO hay plan aprobado, este candado no estorba: mandan los demas, como siempre.

LO QUE NO HACE (alcance cerrado, ley del 2026-09-05):
  - No decide si el cambio es bueno: de eso van las vigias.
  - No sustituye a ningun otro candado: se suma.
  - No bloquea LEER. Solo escribir.

Es comparar rutas contra una lista: una CUENTA, no un juicio.
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "RUTA_DE_ACCESO.json")
CUADERNO = os.path.join(AQUI, "memoria", "RUTA_DE_ACCESO.log")

# Un plan no vale para siempre: si nadie lo cierra, caduca y deja de mandar.
VIGENCIA_H = 48


def _ruta():
    return os.environ.get("INGENIERO_RUTA_ACCESO_TEST") or RUTA


def leer():
    """El plan aprobado y su lista de acceso. Si no hay, devuelve caja vacia."""
    try:
        with open(_ruta(), encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _guardar(d):
    os.makedirs(os.path.dirname(_ruta()), exist_ok=True)
    with open(_ruta(), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def abrir(plan, piezas, motivo=""):
    """Declara la ruta: que plan y QUE se puede tocar. Es lo que se le enseña a Julio."""
    d = {"plan": (plan or "").strip(), "motivo": (motivo or "").strip(),
         "piezas": sorted({str(p).replace("\\", "/").strip() for p in (piezas or []) if str(p).strip()}),
         "desde": time.time(), "estado": "abierta"}
    _guardar(d)
    return d


def cerrar():
    """Se termino el plan: la ruta deja de mandar y vuelve el regimen normal."""
    d = leer()
    d["estado"] = "cerrada"
    d["hasta"] = time.time()
    _guardar(d)
    return d


def vigente(d=None):
    """¿Hay un plan aprobado mandando ahora mismo?"""
    d = leer() if d is None else d
    if not d or d.get("estado") != "abierta" or not d.get("piezas"):
        return False
    try:
        return (time.time() - float(d.get("desde") or 0)) <= VIGENCIA_H * 3600
    except Exception:
        return False


def _normal(p):
    p = str(p or "").replace("\\", "/")
    raiz = AQUI.replace("\\", "/")
    if p.lower().startswith(raiz.lower()):
        p = p[len(raiz):]
    return p.strip("/").lower()


def permitido(archivo, d=None):
    """¿Esta este archivo dentro de lo que el plan declaro? Se compara por ruta, no por nombre
    suelto: 'cuotas.py' no abre 'otra/cuotas.py'."""
    d = leer() if d is None else d
    objetivo = _normal(archivo)
    if not objetivo:
        return True
    for pieza in d.get("piezas", []):
        p = _normal(pieza)
        if not p:
            continue
        if objetivo == p or objetivo.startswith(p + "/"):
            return True
    return False


def _apuntar(archivo, dejo_pasar, plan):
    """El freno deja RASTRO. Un candado que frena en silencio no se puede medir."""
    try:
        os.makedirs(os.path.dirname(CUADERNO), exist_ok=True)
        with open(CUADERNO, "a", encoding="utf-8") as f:
            f.write("%s | %s | %s | plan: %s\n"
                    % (time.strftime("%Y-%m-%dT%H:%M:%S"),
                       "DEJO PASAR" if dejo_pasar else "FRENO", archivo, plan))
    except Exception:
        pass


MENSAJE = (
    "\nFRENADO POR LA RUTA DE ACCESO (Julio, 2026-09-06)\n\n"
    "  Ibas a tocar:  {archivo}\n"
    "  Y el plan aprobado NO lo incluye.\n\n"
    "  PLAN VIGENTE : {plan}\n"
    "  LO QUE SE PUEDE TOCAR, y nada mas:\n{lista}\n"
    "  Esto frena AUNQUE los candados esten apagados: la autorizacion de Julio\n"
    "  no es barra libre, es permiso para LO QUE EL PLAN DIJO.\n\n"
    "  Si de verdad hace falta tocar esa pieza, no se rodea el freno: se le dice\n"
    "  a Julio que el plan se quedo corto, y el decide si se amplia la ruta.\n")


def main():
    crudo = sys.stdin.read()
    try:
        data = json.loads(crudo) if crudo.strip().startswith("{") else {}
    except Exception:
        data = {}
    if str(data.get("tool_name") or "") not in ("Write", "Edit", "NotebookEdit"):
        return 0
    archivo = str((data.get("tool_input") or {}).get("file_path") or "")
    if not archivo:
        return 0

    d = leer()
    if not vigente(d):
        return 0                       # sin plan aprobado, este candado no estorba

    # El propio registro de la ruta y su cuaderno siempre se pueden tocar: si no, no habria
    # forma de cerrar la ruta ni de dejar rastro.
    if _normal(archivo) in (_normal(RUTA), _normal(CUADERNO)):
        return 0

    if permitido(archivo, d):
        _apuntar(archivo, True, d.get("plan", ""))
        return 0

    _apuntar(archivo, False, d.get("plan", ""))
    lista = "\n".join("     - " + p for p in d.get("piezas", []))
    sys.stderr.write(MENSAJE.format(archivo=archivo, plan=d.get("plan", "(sin nombre)"),
                                    lista=lista))
    try:
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candados_medicion
        candados_medicion.cazado("ruta_de_acceso")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
