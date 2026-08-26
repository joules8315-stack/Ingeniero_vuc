# -*- coding: utf-8 -*-
"""arnes/candados_medicion.py — MIDE a los candados, como Julio mide todo lo demas.

Claude, 2026-08-25 (punto final): "Cada candado deberia llevar cuenta de cuantas veces ha cazado
algo de verdad. Al mes se mira: el que no ha cazado nada, o su senal esta mal puesta, o ya no hace
falta. Tu mides todo lo demas. Ellos tambien deberian medirse."

Y su anadido: "cuenta tambien cuantas veces FRENO ALGO LEGITIMO. Un candado con muchas frenadas en
falso es peor que no tenerlo, porque ensena a ignorarlos todos. Con las dos cuentas, al mes se ve
solo cual sobra."

POR QUE: el arnes puede pesar mas que el trabajo (hoy Julio vio que se fue mucho tiempo negociando
con candados). Para que no pese de mas, hay que saber cual candado de verdad caza algo y cual solo
molesta. Dos contadores por candado:
  · cazadas      -> freno y tenia razon (evito un error real).
  · frenos_falsos-> freno algo que era legitimo (senal mal puesta o candado que sobra).

Se usa asi:
    python ingeniero.py candados-medicion          -> resumen: que cazo y que freno en falso
    python arnes/candados_medicion.py apuntar memoria cazo
    python arnes/candados_medicion.py apuntar memoria freno_falso
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "CANDADOS_MEDICION.json")


def _leer():
    try:
        return json.load(open(RUTA, encoding="utf-8"))
    except Exception:
        return {}


def _guardar(d):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def apuntar(quien, tipo):
    """Registra una cazada (cazo) o un freno en falso (freno_falso) de un candado."""
    tipo = str(tipo).lower()
    clave = "cazadas" if tipo in ("cazo", "cazada", "cazadas") else "frenos_falsos"
    d = _leer()
    e = d.setdefault(str(quien), {"cazadas": 0, "frenos_falsos": 0, "desde": time.time()})
    e[clave] = int(e.get(clave, 0)) + 1
    _guardar(d)
    return e


def resumen():
    """Tabla de cada candado: cuantas veces cazo y cuantas freno en falso. Marca los que sobran."""
    d = _leer()
    if not d:
        return "AUN SIN DATOS: ningun candado ha apuntado cazadas/frenos en falso todavia.\n" \
               "  Se llena con `candados_medicion.py apuntar <candado> cazo|freno_falso`."
    L = ["MEDICION DE CANDADOS (cazadas reales vs frenos en falso):", ""]
    L.append("  %-16s %-9s %-12s  senal" % ("candado", "cazo", "freno_falso"))
    for quien in sorted(d):
        e = d[quien]
        cazo = int(e.get("cazadas", 0))
        falso = int(e.get("frenos_falsos", 0))
        flag = ""
        if falso > 0 and cazo == 0 and falso >= 3:
            flag = "  <-- SOBRA o senal mal puesta (solo frena en falso)"
        elif cazo == 0 and falso == 0:
            flag = "  (sin actividad)"
        L.append("  %-16s %-9d %-12d%s" % (quien, cazo, falso, flag))
    L.append("")
    L.append("Regla: al mes, el que no cazo nada o tiene muchas frenadas en falso se revisa o se apaga.")
    return "\n".join(L)


def main():
    args = sys.argv[1:]
    if args and args[0] == "apuntar" and len(args) >= 3:
        r = apuntar(args[1], args[2])
        print("%s: ahora %d cazadas, %d frenos en falso"
              % (args[1], r["cazadas"], r["frenos_falsos"]))
        return 0
    print(resumen())
    return 0


if __name__ == "__main__":
    sys.exit(main())
