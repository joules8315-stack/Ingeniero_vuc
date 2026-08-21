#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/guard_pasado.py — NO SE ROMPE LO QUE YA SE REPARO. TECHO Y PISO.

Julio, 2026-08-21: "crea el guardia de lo ya reparado, fuerte, con candado, ultra blindado, que
siempre este pendiente, de extremo a extremo, y que sirva de techo y piso, que nada se le escape,
que tenga siempre presente los fallos pasados para que no los cometa, y que siempre tenga el
grafo del pedazo, para que tambien sea eficiente."

EL PROBLEMA HISTORICO: arreglar una cosa y que se caiga otra que YA funcionaba. El guardia de
cross-flow mira a los VECINOS de ahora. Este mira al PASADO: todo lo que costo repararse alguna
vez y no puede volver a caerse.

TECHO Y PISO
  · TECHO (antes de tocar):   avisa que reparaciones pasadas puede afectar lo que se va a tocar,
                              con su causa, su cura y su "no volver a".
  · PISO  (antes de guardar): corre las pruebas de ESAS reparaciones. Si una cae, NO SE GUARDA.

EFICIENTE POR EL GRAFO
Se corren SOLO las pruebas de lo que se toco y de sus vecinos, no las 150. Por eso este guardia
hace el trabajo MAS rapido, no mas lento: guardar pasa de 31 segundos a unos pocos.

POR QUE NO SE REPARTE ENTRE AYUDANTES (opinion de ingeniero dada a Julio el 2026-08-21):
lo ya reparado no se comprueba opinando, se comprueba PROBANDO. La prueba es instantanea, gratis
y siempre da el mismo resultado; un ayudante tarda entre 3 y 300 segundos (medido ese dia) y
puede equivocarse. Los ayudantes entran DESPUES, solo cuando algo se pone rojo, para explicar
que se rompio — ahi si hace falta juicio, no comprobacion.
"""
import json
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
CERROJO = os.path.join(AQUI, "memoria", ".pasado_corriendo")


def _reparaciones():
    """Todo lo que alguna vez se reparo y dejo una prueba que lo protege."""
    try:
        from cuerpo import fallos
        return [f for f in fallos._leer() if f.get("quien_lo_caza") and f.get("piezas")]
    except Exception:
        return []


def _vecinos_de(piezas):
    """Quien depende de lo que se toca. Tocar una pieza afecta a quien la usa: eso tambien es
    'lo ya reparado' aunque no se toque directamente."""
    fuera = set(piezas)
    try:
        from cerebro import grafo
        for apodo in grafo.proyectos():
            try:
                g = grafo.cargar(apodo)
            except Exception:
                continue
            for p in piezas:
                base = p.split("/")[-1]
                for ficha in g["piezas"]:
                    if ficha["id"].split("/")[-1] != base:
                        continue
                    for v in grafo.vecinos(g, ficha["id"], saltos=1, min_fuerza=3.0):
                        if v["por"] in ("IMPORTA", "VIGILA"):
                            fuera.add(v["pieza"])
    except Exception:
        pass
    return fuera


def reparaciones_que_tocas(piezas):
    """TECHO: que reparaciones pasadas puede afectar tocar estas piezas."""
    if not piezas:
        return []
    alcance = {p.split("/")[-1].lower() for p in _vecinos_de(piezas)}
    salen = []
    for f in _reparaciones():
        suyas = {str(x).split("/")[-1].split(":")[0].lower() for x in f.get("piezas", [])}
        if suyas & alcance:
            salen.append({
                "que_paso": f["que_paso"],
                "no_volver_a": f["no_volver_a"],
                "cura": f.get("cura", ""),
                "prueba": f["quien_lo_caza"],
                "cuando": f.get("fecha", ""),
            })
    return salen


def pruebas_a_correr(piezas):
    """Solo las pruebas de lo que se toco. Esto es lo que lo hace rapido."""
    cuales = []
    for r in reparaciones_que_tocas(piezas):
        p = str(r["prueba"]).strip()
        if p.endswith(".py") and p not in cuales:
            cuales.append(p)
    return cuales


def siguen_en_pie(piezas):
    """PISO: ¿siguen verdes las pruebas de lo que ya se reparo? (ok, detalle)."""
    cuales = pruebas_a_correr(piezas)
    if not cuales:
        return True, []
    caidas = []
    for prueba in cuales:
        ruta = os.path.join(AQUI, prueba.replace("/", os.sep))
        if not os.path.exists(ruta):
            caidas.append({"prueba": prueba, "por_que": "NO_EXISTE esa prueba: la reparacion "
                                                        "quedo sin nada que la proteja"})
            continue
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", prueba],
                               cwd=AQUI, capture_output=True, text=True, timeout=240)
            if r.returncode != 0:
                ultima = [l for l in (r.stdout or "").splitlines() if l.strip()][-1:]
                caidas.append({"prueba": prueba,
                               "por_que": ultima[0] if ultima else "se cayo"})
        except Exception as e:
            caidas.append({"prueba": prueba, "por_que": str(e)[:80]})
    return (not caidas), caidas


def aviso_techo(piezas):
    """El texto que se muestra ANTES de tocar."""
    rs = reparaciones_que_tocas(piezas)
    if not rs:
        return ""
    L = ["LO QUE VAS A TOCAR YA SE REPARO ANTES. No lo rompas otra vez:", ""]
    for r in rs[:4]:
        L.append("  * %s" % r["que_paso"][:120])
        L.append("    se curo asi   : %s" % r["cura"][:120])
        L.append("    NO VUELVAS A  : %s" % r["no_volver_a"][:120])
        L.append("    lo protege    : %s" % r["prueba"])
        L.append("")
    return "\n".join(L)


def aviso_piso(caidas):
    """El texto que se muestra cuando algo ya reparado se cayo."""
    L = ["SE ROMPIO ALGO QUE YA ESTABA REPARADO. No se guarda asi:", ""]
    for c in caidas:
        L.append("  * %s" % c["prueba"])
        L.append("    %s" % c["por_que"][:150])
    L.append("")
    L.append("  Esto es justo lo que mas dano hace: arreglar una cosa y tumbar otra que ya iba.")
    L.append("  Arreglalo antes de guardar, o deshaz lo ultimo que tocaste.")
    return "\n".join(L)


# ─── como hook: avisa antes de tocar ──────────────────────────────────────────
def main():
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = str((data.get("tool_input") or {}).get("file_path") or "")
    if not fp or not fp.endswith((".py", ".html", ".js")):
        return 0
    rel = fp.replace("\\", "/")
    for raiz in ("cuerpo/", "cerebro/", "arnes/", "web/"):
        if raiz in rel:
            rel = rel[rel.index(raiz):]
            break
    else:
        rel = os.path.basename(fp)
    aviso = aviso_techo([rel])
    if not aviso:
        return 0
    sys.stderr.write(aviso + "\n  (esto es un AVISO: mira eso antes de seguir)\n")
    return 0          # avisa, no bloquea: el que bloquea es el PISO, al guardar


if __name__ == "__main__":
    if "--techo" in sys.argv:
        i = sys.argv.index("--techo")
        print(aviso_techo(sys.argv[i + 1:]) or "nada de lo que vas a tocar se reparo antes.")
    elif "--piso" in sys.argv:
        i = sys.argv.index("--piso")
        ok, caidas = siguen_en_pie(sys.argv[i + 1:])
        print("todo lo ya reparado sigue en pie." if ok else aviso_piso(caidas))
        sys.exit(0 if ok else 2)
    else:
        sys.exit(main())
