# -*- coding: utf-8 -*-
"""HABILIDAD — AVISAR SI EL MATERIAL NO TRAE LA PIEZA DEL PROBLEMA. Sin gastar ninguna IA.

Julio, 2026-09-05. Criterio que la justifica: se gastaron DOS vueltas del equipo
pidiendo reparar algo cuyo codigo no venia en el material. El cerebro contesto
"NO_ENCONTRADO" y la vuelta se perdio. Antes de pagar una vuelta hay que mirar si
lo que el problema nombra esta dentro del paquete.

Es comparar palabras del problema con los nombres que trae el paquete: una cuenta,
no un juicio.

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/falta_en_el_material.py "<el problema>"
    cd C:\\Ingeniero_VUC; python skills/falta_en_el_material.py          (mira el ultimo paquete)
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAQUETES = os.path.join(AQUI, "memoria", "paquetes")

# Palabras que no dicen nada: no sirven para buscar una pieza.
VACIAS = {"que", "solo", "se", "no", "si", "lo", "la", "el", "los", "las", "de", "del", "un",
          "una", "por", "con", "para", "en", "y", "su", "sus", "mas", "ya", "esta", "son",
          "hay", "sin", "sobre", "cuando", "porque", "todo", "cada", "este", "ese", "muy",
          "pero", "como", "donde", "quien", "cual", "algo", "otro", "hacer", "ser", "tiene",
          "puede", "al", "le", "me", "mi", "yo", "es", "a", "o"}


def _ultimo_paquete():
    if not os.path.isdir(PAQUETES):
        return None
    hojas = [os.path.join(PAQUETES, n) for n in os.listdir(PAQUETES) if n.endswith(".md")]
    return max(hojas, key=os.path.getmtime) if hojas else None


def _texto(ruta):
    try:
        with open(ruta, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def _piezas_del_paquete(texto):
    """Los nombres que el paquete declara: las lineas que empiezan por tres almohadillas."""
    piezas = set()
    for m in re.finditer(r"^### `([^`]+?)`", texto or "", re.M):
        piezas.add(m.group(1).split(":")[0].strip())
    return piezas


def _palabras(problema):
    crudo = re.split(r"[^\wáéíóúñ]+", (problema or "").lower())
    return [w for w in crudo if len(w) > 2 and w not in VACIAS]


def revisar(problema="", paquete=None):
    ruta = paquete or _ultimo_paquete()
    if not ruta:
        return {"error": "no hay ningun paquete todavia"}
    texto = _texto(ruta)
    if not problema:
        # El problema esta escrito en el nombre del propio paquete.
        problema = os.path.basename(ruta).replace(".md", "").replace("_", " ")
    piezas = _piezas_del_paquete(texto)
    bajos = [p.split("/")[-1].lower() for p in piezas]
    faltan, hay = [], []
    for w in _palabras(problema):
        if any(w in b for b in bajos) or w.lower() in texto.lower():
            hay.append(w)
        else:
            faltan.append(w)
    return {"paquete": ruta, "problema": problema, "piezas": sorted(piezas),
            "encontradas": hay, "sin_rastro": faltan}


def informe(problema=""):
    r = revisar(problema)
    if "error" in r:
        return "FALTA EN EL MATERIAL: " + r["error"]
    L = ["FALTA EN EL MATERIAL — antes de gastar una vuelta del equipo", "=" * 60,
         "  paquete  : " + os.path.basename(r["paquete"]),
         "  problema : " + r["problema"][:100],
         "",
         "  piezas que trae el material (%d):" % len(r["piezas"])]
    for p in r["piezas"][:12]:
        L.append("     " + p)
    L.append("")
    if r["sin_rastro"]:
        L.append("PALABRAS DEL PROBLEMA QUE NO APARECEN EN EL MATERIAL:")
        L.append("   " + ", ".join(r["sin_rastro"][:14]))
        L.append("")
        L.append("AVISO: el material puede no traer la pieza del problema.")
        L.append("       Mandar la vuelta asi es arriesgarse a pagarla para nada.")
        L.append("       Fallo el QUE REPARTE, no el cerebro.")
    else:
        L.append("Todo lo que nombra el problema aparece en el material: se puede mandar.")
    return "\n".join(L)


if __name__ == "__main__":
    sys.stdout.write(informe(" ".join(sys.argv[1:])) + "\n")
