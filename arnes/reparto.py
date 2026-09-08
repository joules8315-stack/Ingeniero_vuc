# -*- coding: utf-8 -*-
"""EL REPARTO — quien tiene que tarea, y en que estado esta.

Ley: CONTRATO_TRABAJO_CON_CLINE.md (Julio, 2026-08-31):
  "Trabaja con cline... Una vez termine la tarea cline, superviza, si es correcta, dale otra
   tarea, sino, dile que corrija, y me informas si falla."

POR QUE EXISTE: sin esto, dos IA cogen lo mismo (trabajo pagado dos veces y choque al guardar), y
una tarea entregada se da por buena sin mirarla. Aqui queda apuntado quien tiene que, y ninguna
tarea puede darse por cerrada sin que alguien la haya SUPERVISADO con la vigia en verde.

LOS ESTADOS, y no hay mas:
  asignada   — se le entrego, todavia no contesto
  entregada  — dice que termino: HAY QUE SUPERVISARLA (no se da por buena)
  correcta   — supervisada y su vigia esta VERDE
  a_corregir — supervisada y NO cumple: se le dijo que corrija, con el fallo concreto
  fallida    — no salio: SE LE INFORMA A JULIO
"""
import datetime
import io
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "REPARTO_IA.json")

ESTADOS = ("asignada", "entregada", "correcta", "a_corregir", "fallida")

# Los que hay que contarle a Julio si o si: uno porque no salio, y el otro porque lleva parado.
AVISAR_A_JULIO = ("fallida",)


def _ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def _leer():
    try:
        with io.open(RUTA, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _guardar(tareas):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    with io.open(RUTA, "w", encoding="utf-8", newline="\n") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=1)


def asignar(quien, tarea, vigia="", piezas=None):
    """Le da UNA tarea a UNA IA. Si esa tarea ya tiene dueno, no se asigna: se dice quien la tiene.

    Devuelve (se_asigno, motivo). Nunca se pisa una tarea viva: eso es pagarla dos veces.
    """
    quien = str(quien or "").strip().lower()
    tarea = str(tarea or "").strip()
    if not quien or not tarea:
        return False, "hace falta decir a quien y que tarea"

    tareas = _leer()
    for t in tareas:
        if t.get("tarea") == tarea and t.get("estado") in ("asignada", "entregada", "a_corregir"):
            if t.get("quien") != quien:
                return False, "esa tarea ya la tiene %s (esta %s)" % (t["quien"], t["estado"])
            return False, "ya la tienes tu (esta %s)" % t["estado"]

    tareas.append({"quien": quien, "tarea": tarea, "estado": "asignada",
                   "vigia": str(vigia or ""), "piezas": list(piezas or []),
                   "asignada": _ahora(), "historial": ["%s asignada a %s" % (_ahora(), quien)]})
    _guardar(tareas)
    return True, "asignada a %s" % quien


def _buscar(quien, tarea):
    for t in _leer():
        if t.get("quien") == str(quien or "").lower() and t.get("tarea") == tarea:
            return t
    return None


def _cambiar(quien, tarea, estado, nota):
    if estado not in ESTADOS:
        return False, "ese estado no existe: %s" % estado
    tareas = _leer()
    for t in tareas:
        if t.get("quien") == str(quien or "").lower() and t.get("tarea") == tarea:
            t["estado"] = estado
            t.setdefault("historial", []).append("%s %s — %s" % (_ahora(), estado, nota))
            _guardar(tareas)
            return True, "ahora esta %s" % estado
    return False, "no encuentro esa tarea asignada a %s" % quien


def entregada(quien, tarea, nota=""):
    """Dice que termino. NO es que este bien: es que hay que supervisarla."""
    return _cambiar(quien, tarea, "entregada", nota or "dice que termino")


def supervisar(quien, tarea, vigia_verde, nota=""):
    """El unico camino para cerrar una tarea. Sin vigia verde no hay 'correcta'.

    Devuelve (estado_nuevo, que_hay_que_hacer_ahora) en palabras simples.
    """
    t = _buscar(quien, tarea)
    if not t:
        return "", "no encuentro esa tarea asignada a %s" % quien
    if vigia_verde:
        _cambiar(quien, tarea, "correcta", nota or "supervisada: su vigia esta verde")
        return "correcta", "dale la siguiente tarea"
    _cambiar(quien, tarea, "a_corregir", nota or "supervisada: su vigia NO esta verde")
    return "a_corregir", "dile que corrija, con el fallo concreto y medido"


def fallida(quien, tarea, nota=""):
    """No salio. Esto SE LE INFORMA A JULIO: no se esconde ni se maquilla."""
    return _cambiar(quien, tarea, "fallida", nota or "no salio")


def sin_supervisar():
    """Las que dijeron estar terminadas y nadie ha mirado. Son deuda, no avance."""
    return [t for t in _leer() if t.get("estado") == "entregada"]


def para_julio():
    """Lo que hay que contarle a Julio si o si."""
    return [t for t in _leer() if t.get("estado") in AVISAR_A_JULIO]


def texto():
    """El reparto en palabras simples, para mirarlo de un vistazo."""
    tareas = _leer()
    if not tareas:
        return "no hay ninguna tarea repartida"
    L = ["REPARTO DE TAREAS (quien tiene que)"]
    for t in tareas:
        L.append("  [%-10s] %-8s  %s" % (t.get("estado", "?"), t.get("quien", "?"),
                                         str(t.get("tarea", ""))[:70]))
    pendientes = sin_supervisar()
    if pendientes:
        L.append("")
        L.append("  HAY %d ENTREGADA(S) SIN SUPERVISAR: no se dan por buenas hasta mirarlas."
                 % len(pendientes))
    avisos = para_julio()
    if avisos:
        L.append("")
        L.append("  HAY QUE CONTARLE A JULIO %d cosa(s) que no salieron." % len(avisos))
    return "\n".join(L)


def dueno(tarea):
    """Quien tiene VIVA esa tarea exacta. Devuelve (quien, estado) o (None, None). Estados vivos igual que los que ya usa asignar: asignada, entregada, a_corregir."""
    tarea = str(tarea or '').strip()
    for t in _leer():
        if t.get('tarea') == tarea and t.get('estado') in ('asignada', 'entregada', 'a_corregir'):
            return (str(t.get('quien') or ''), str(t.get('estado') or ''))
    return (None, None)
