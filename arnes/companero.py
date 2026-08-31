# -*- coding: utf-8 -*-
"""EL COMPANERO — con que otra IA se trabaja, dicho en UN SOLO SITIO.

Ley: CONTRATO_EL_COMPANERO.md (Julio, 2026-08-31):
  "a partir de ahora trabajaras con continue, no con cline"
  "De ahora en adelante todo es con continue, es lo mejor, mas economico"
  "solo si se bloquea continue, solo si eso pasa, o falla, no responde como es, trabajas
   nuevamente con cline"

POR QUE EXISTE, medido el mismo dia que se creo: al cambiar de companero, el candado del buzon
siguio exigiendo el buzon del anterior, porque llevaba su nombre ESCRITO A MANO dentro. Un nombre
repetido por diez sitios obliga a acordarse de diez sitios, y lo que depende de acordarse no se
cumple. Aqui vive la respuesta, y los demas la preguntan.

LA RESERVA NO ESTA PROHIBIDA: ESTA CONDICIONADA. Se acude a ella declarando que el activo no
pudo, y queda apuntado. Eso es a proposito, y tambien es leccion pagada:
  "no hacer un candado sin una forma honrada de satisfacerlo: empuja a saltarselo, y eso es peor
   que no tenerlo"
"""
import datetime
import io
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Las pruebas desvian esta ruta para no tocar la memoria de verdad. Esa leccion tambien se pago:
# las vigias envenenaron el diccionario de Julio escribiendo en el cuaderno bueno.
MARCA_NO_PUDO = os.path.join(AQUI, "memoria", ".el_activo_no_pudo")

VIGENCIA_MIN = 60       # lo que dura la marca de "el activo no pudo"

ARRANQUE = {
    "activo": "continue",
    "reservas": [{
        "quien": "cline",
        "por_que": ("Julio, 2026-08-31: a partir de ahora se trabaja con continue; cline queda "
                    "de reserva para cuando continue se bloquee, falle o no responda"),
        "desde": "2026-08-31",
    }],
    "historial": ["2026-08-31 se empieza asi por orden de Julio: activo continue, reserva cline"],
}


def _ruta_estado():
    """La ruta del cuaderno. Se mira cada vez, para que las pruebas la puedan desviar."""
    return (os.environ.get("INGENIERO_COMPANERO", "").strip()
            or os.path.join(AQUI, "memoria", "COMPANERO.json"))


def _ruta_marca():
    """La ruta de la marca. Igual que la de arriba: se resuelve cada vez, no al importar."""
    return (os.environ.get("INGENIERO_MARCA_NO_PUDO", "").strip()
            or MARCA_NO_PUDO)


def _leer():
    """El estado. Si el cuaderno no esta, esta vacio o esta roto, se devuelve el de arranque.

    Nunca se cae por un archivo mal: mas vale arrancar de cero que dejar el sistema sin saber
    con quien trabaja.
    """
    try:
        with io.open(_ruta_estado(), encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict) and d.get("activo"):
            return d
    except Exception:
        pass
    return json.loads(json.dumps(ARRANQUE))     # una copia limpia, no el original


def _guardar(d):
    ruta = _ruta_estado()
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with io.open(ruta, "w", encoding="utf-8", newline="\n") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        return True
    except Exception:
        return False


def _ahora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def activo():
    """Con quien se trabaja AHORA."""
    return str(_leer().get("activo", "")).strip().lower()


def reservas():
    """Los que estan de reemplazo, con su motivo."""
    return list(_leer().get("reservas", []) or [])


def es_reserva(nombre):
    """Si ese nombre es un reemplazo (no el activo)."""
    n = str(nombre or "").strip().lower()
    return bool(n) and any(str(r.get("quien", "")).lower() == n for r in reservas())


def por_que_reserva(nombre):
    """El motivo por el que ese quedo de reemplazo. La memoria no olvida por que."""
    n = str(nombre or "").strip().lower()
    for r in reservas():
        if str(r.get("quien", "")).lower() == n:
            return str(r.get("por_que", ""))
    return ""


def cambiar(nuevo, por_que):
    """Cambia de companero. El que entra SALE de la reserva; el que sale entra en ella.

    Nadie puede figurar a la vez como activo y como reemplazo: eso volveria mentira a es_reserva.
    """
    nuevo = str(nuevo or "").strip().lower()
    if not nuevo:
        return False, "hace falta decir quien entra"
    d = _leer()
    anterior = str(d.get("activo", "")).strip().lower()
    if nuevo == anterior:
        return False, "%s ya es el companero" % nuevo

    # el que entra deja de ser reemplazo
    d["reservas"] = [r for r in (d.get("reservas") or [])
                     if str(r.get("quien", "")).lower() != nuevo]
    # el que sale pasa a serlo, con su motivo
    if anterior:
        d["reservas"].append({"quien": anterior, "por_que": str(por_que or ""),
                              "desde": _ahora()[:10]})
    d["activo"] = nuevo
    d.setdefault("historial", []).append(
        "%s entra %s y sale %s — %s" % (_ahora(), nuevo, anterior or "(nadie)", por_que or "?"))
    _guardar(d)
    return True, "ahora se trabaja con %s" % nuevo


def declarar_que_no_pudo(quien, motivo):
    """Deja dicho que el activo no pudo, para poder acudir al reemplazo. Caduca sola."""
    ruta = _ruta_marca()
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with io.open(ruta, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"quien": str(quien or ""), "motivo": str(motivo or ""),
                       "cuando": datetime.datetime.now().timestamp(),
                       "cuando_texto": _ahora()}, f, ensure_ascii=False, indent=1)
        return True
    except Exception:
        return False


def puede_acudir_a_la_reserva():
    """Solo si consta que el activo no pudo, y esa marca sigue vigente."""
    try:
        with io.open(_ruta_marca(), encoding="utf-8") as f:
            d = json.load(f)
        minutos = (datetime.datetime.now().timestamp() - float(d.get("cuando", 0))) / 60.0
        return minutos <= VIGENCIA_MIN
    except Exception:
        return False


def por_que_se_acudio():
    """El motivo declarado la ultima vez, para poder contarselo a Julio."""
    try:
        with io.open(_ruta_marca(), encoding="utf-8") as f:
            return str(json.load(f).get("motivo", ""))
    except Exception:
        return ""


def texto():
    """En palabras simples, para mirarlo de un vistazo."""
    L = ["CON QUIEN SE TRABAJA", "  ahora   : %s" % (activo() or "(nadie)")]
    for r in reservas():
        L.append("  reemplazo: %-10s — %s" % (r.get("quien", "?"),
                                              str(r.get("por_que", ""))[:70]))
    if puede_acudir_a_la_reserva():
        L.append("  AHORA MISMO se puede acudir al reemplazo: %s" % (por_que_se_acudio() or "?"))
    else:
        L.append("  (para acudir al reemplazo hay que declarar antes que el activo no pudo)")
    return "\n".join(L)
