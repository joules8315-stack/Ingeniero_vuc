# -*- coding: utf-8 -*-
"""arnes/candado_legislar.py — F5 (punto a de Julio): TODA instruccion se legisla, con candado.

Julio, 2026-08-24 (punto a): "todo lo que yo escriba debe ser legislado, todo, absolutamente todo...
la orden es clara, siempre. Por eso me toca volver a repetir."

La ley L5 ya estaba escrita (CONTRATO_LEGISLACION_TOTAL), pero dependia de que la IA se acuerde.
Este candado lo hace FISICO: cada instruccion de Julio queda apuntada como PENDIENTE de legislar, y
bloquea el cierre hasta que se legisle (o se marque "ya existe" / "no aplica", con justificacion).

Uso (en PowerShell):
  apuntar:   python arnes/candado_legislar.py apuntar "<la instruccion de Julio>"
  resolver:  python arnes/candado_legislar.py hecho "<texto>" legislado|ya_existe|no_aplica ["motivo"]
  listar:    python arnes/candado_legislar.py listar
  hook:      (sin argumentos) -> si hay pendientes, devuelve 2 (bloquea el cierre).
"""
import hashlib
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(AQUI, "memoria", ".legislacion_pendiente.json")


def _ruta():
    return os.environ.get("INGENIERO_LEGISLAR_TEST") or LEDGER


def _leer():
    try:
        return json.load(open(_ruta(), encoding="utf-8"))
    except Exception:
        return {}


def _guardar(d):
    os.makedirs(os.path.dirname(_ruta()), exist_ok=True)
    json.dump(d, open(_ruta(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _h(texto):
    return hashlib.md5((texto or "").strip().lower().encode("utf-8")).hexdigest()


def apuntar(texto, fuente="julio"):
    """Registra una instruccion como PENDIENTE de legislar. Devuelve cuantas hay pendientes."""
    texto = (texto or "").strip()
    if not texto:
        return 0
    d = _leer()
    d[_h(texto)] = {"texto": texto[:2000], "fuente": fuente, "cuando": time.time(),
                    "estado": "pendiente", "resolucion": "", "motivo": ""}
    _guardar(d)
    return len([e for e in d.values() if e.get("estado") == "pendiente"])


def marcar(texto, resolucion, motivo=""):
    """Marca una instruccion como resuelta: legislado / ya_existe / no_aplica (con motivo)."""
    d = _leer()
    h = _h(texto)
    if h not in d:
        return False
    if resolucion not in ("legislado", "ya_existe", "no_aplica"):
        return False
    d[h]["estado"] = "resuelto"
    d[h]["resolucion"] = resolucion
    d[h]["motivo"] = (motivo or "")[:400]
    d[h]["cuando_resuelto"] = time.time()
    _guardar(d)
    return True


def pendientes():
    """Instrucciones que aun no estan legisladas (ni marcadas)."""
    return [e for e in _leer().values() if e.get("estado") == "pendiente"]


def main():
    args = sys.argv[1:]
    if args and args[0] == "apuntar":
        n = apuntar(" ".join(args[1:]))
        sys.stdout.write("apuntado. pendientes: %d\n" % n)
        return 0
    if args and args[0] == "hecho" and len(args) >= 3:
        ok = marcar(args[1], args[2], " ".join(args[3:]))
        sys.stdout.write("ok\n" if ok else "no_encontrado (o resolucion invalida)\n")
        return 0 if ok else 2
    if args and args[0] == "listar":
        p = pendientes()
        sys.stdout.write(("\n".join("- " + e["texto"][:120] for e in p)) or "sin pendientes\n")
        return 0
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    # modo HOOK de cierre: si hay instrucciones sin legislar, bloquea.
    p = pendientes()
    if not p:
        return 0
    sys.stderr.write(
        "NO SE PUEDE TERMINAR: hay instrucciones de Julio SIN LEGISLAR (L5, punto a):\n\n"
        + "\n".join("  - " + e["texto"][:160] for e in p[:6])
        + "\n\n  Cada una debe quedar legislada (contrato + tabla de verdad + matriz + vigia)\n"
          "  o marcarse 'ya existe' / 'no aplica' con su motivo:\n"
          "     cd C:\\Ingeniero_VUC; python arnes/candado_legislar.py hecho \"<texto>\" legislado\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
