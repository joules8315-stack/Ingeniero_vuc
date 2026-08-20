# -*- coding: utf-8 -*-
"""cerebro/router.py — EL REPARTIDOR. La pieza que faltaba en todo el sistema.

Recibe un PROBLEMA en palabras normales y entrega un PAQUETE MINIMO: lo justo para
repararlo. Ni un archivo entero de mas.

    python -m cerebro.router dmm "el onboarding no guarda el perfil"

Lo que SIEMPRE lleva el paquete (y por que):
  1. LA LEY          — que contrato manda aqui        (para no legislar dos veces)
  2. LAS PIEZAS      — con su boca y su tamano        (para saber que llamar sin abrirlas)
  3. LOS TROZOS      — archivo:linea-linea, exactos   (para no releer 10.818 lineas)
  4. LAS VIGIAS      — cuales protegen esto           (para probar antes y despues)
  5. A QUIEN DANA    — los vecinos del grafo          (cross-flow obligatorio)
  6. COMO PEDIR MAS  — el formato NECESITO_LEER       (leer de mas se pide, no se hace)

Regla dura: aqui NO se inventa. Si algo no esta en el disco, se escribe NO_ENCONTRADO.
"""
import os, sys, json, datetime
from . import grafo, flujos, trozos, enlaces

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAQUETES = os.path.join(AQUI, "memoria", "paquetes")
TOPE_LINEAS = 400   # un paquete que pasa de esto ya no es un paquete: es releer el proyecto


def _claves_de(g, nombres_flujo):
    cl = []
    for n in nombres_flujo:
        cl += g["flujos"].get(n, {}).get("claves", [n])
    return sorted(set(cl))


def armar(apodo, problema, k_trozos=6, saltos=1):
    g = grafo.cargar(apodo)
    hits = flujos.buscar(g["flujos"], problema)[:3]
    nombres = [h[0] for h in hits]

    # piezas del flujo
    ids = []
    for n in nombres:
        ids += g["flujos"].get(n, {}).get("piezas", [])
    ids = sorted(set(ids))
    fichas = [p for p in g["piezas"] if p["id"] in ids]

    # si el flujo no toco ningun codigo, se abre a las piezas grandes del proyecto
    # (caso app.py: el problema es de plantilla pero el codigo esta en un solo monstruo)
    codigo = [f for f in fichas if f["rol"] in ("CUERPO", "CODIGO", "WEB", "CEREBRO")]
    if not codigo:
        monstruos = sorted([p for p in g["piezas"] if p["rol"] in ("CODIGO", "WEB", "CUERPO")],
                           key=lambda x: -x["lineas"])[:3]
        fichas += monstruos
        codigo = monstruos

    # LA CARA TAMBIEN ES DEL FLUJO (fallo real 2026-08-20, cazado por Qwen y Gemini).
    # El paquete del onboarding traia `cuerpo/perfil.py` (el motor) pero NO `web/` (la cara,
    # donde esta el formulario que de verdad guarda). Qwen: "no veo el codigo que invoca a
    # guardar_perfil". Ninguna de las 26 vigias lo vio: verde sobre un caso que no se vive.
    # Cura: QUIEN LLAMA a una pieza del flujo pertenece al flujo, aunque su nombre no lo diga.
    _, entra = enlaces.indexar(g["enlaces"])
    ya = {f["id"] for f in codigo}
    llamadores = []
    for f in list(codigo):
        for e in entra.get(f["id"], []):
            if e["tipo"] != "IMPORTA" or e["de"] in ya:
                continue
            fv = grafo.ficha(g, e["de"])
            if fv and fv["rol"] in ("WEB", "CODIGO", "CUERPO"):
                llamadores.append(fv)
                ya.add(fv["id"])
    # la cara primero: ahi suele estar el fallo que Julio ve con sus ojos
    llamadores.sort(key=lambda x: (x["rol"] != "WEB", -x["lineas"]))
    codigo += llamadores[:4]
    for f in llamadores[:4]:
        if f not in fichas:
            fichas.append(f)

    claves = _claves_de(g, nombres)
    b = trozos.Buscador(codigo)
    pedazos = b.buscar(problema, k=k_trozos, exigir=claves or None)
    if not pedazos:                       # el filtro de asunto puede ser muy duro: se afloja
        pedazos = b.buscar(problema, k=k_trozos)

    leyes = sorted([f for f in fichas if f["rol"] in ("CONTRATO", "MATRIZ", "PROTOCOLO")],
                   key=lambda x: x["id"])
    vigias = sorted([f for f in fichas if f["rol"] == "VIGIA"], key=lambda x: x["id"])

    # cross-flow: a quien puede danar tocar esto
    dana = []
    for f in codigo[:4]:
        for v in grafo.vecinos(g, f["id"], saltos=saltos, min_fuerza=3.0):
            if v["por"] in ("IMPORTA", "VIGILA"):
                dana.append((v["pieza"], v["por"], f["id"]))
    dana = sorted(set(dana))

    return {"apodo": apodo, "raiz": g["raiz"], "problema": problema, "flujos": hits,
            "claves": claves, "fichas": fichas, "codigo": codigo, "trozos": pedazos,
            "leyes": leyes, "vigias": vigias, "dana": dana,
            "total_proyecto": g["resumen"]["lineas"]}


def a_texto(pk):
    L, w = [], None
    L = []
    w = L.append
    hoy = datetime.date.today().isoformat()
    w(f"# PAQUETE MINIMO — {pk['apodo']} — {hoy}")
    w(f"> **Problema:** {pk['problema']}")
    fl = ", ".join(f"{n} ({p})" for n, p in pk["flujos"]) or "NO_ENCONTRADO (ningun flujo casa)"
    w(f"> **Flujo(s) detectado(s):** {fl}")
    w(f"> **Raiz:** `{pk['raiz']}`")
    w("")
    w("**REGLA DE ESTE PAQUETE:** esto es TODO lo que hace falta. No abras nada mas.")
    w("Si de verdad necesitas otra cosa, PIDELA con el formato del final. No la leas por tu cuenta.")
    w("")

    w("## 1. LA LEY QUE MANDA AQUI")
    if pk["leyes"]:
        for f in pk["leyes"]:
            w(f"- `{f['id']}` ({f['lineas']} lineas) — {f['resumen'][:120] or 's/resumen'}")
    else:
        w("- NO_ENCONTRADO: ningun contrato cubre este flujo. **Hay que legislarlo antes de tocar codigo.**")
    w("")

    w("## 2. LAS PIEZAS (su boca, sin abrirlas)")
    for f in pk["codigo"]:
        w(f"### `{f['id']}` — {f['lineas']} lineas")
        if f["resumen"]:
            w(f"  {f['resumen'][:160]}")
        if f["api"]:
            w("  Funciones: " + ", ".join(f"`{a['nombre']}`:{a['linea']}" for a in f["api"][:18]))
        w("")

    w("## 3. LOS TROZOS EXACTOS (aqui esta el problema, ve directo)")
    if pk["trozos"]:
        for t in pk["trozos"]:
            w(f"### `{t['direccion']}`  (relevancia {t['puntaje']})")
            w("```")
            w(t["texto"])
            w("```")
            w("")
    else:
        w("NO_ENCONTRADO: ningun trozo casa con el problema. Describelo con otras palabras.")
        w("")

    w("## 4. LAS VIGIAS QUE PROTEGEN ESTO")
    if pk["vigias"]:
        for f in pk["vigias"]:
            w(f"- `{f['id']}`")
        w("")
        w("Correlas ANTES de tocar (para ver de que color estan) y DESPUES (para no romper):")
        w("```")
        w(f'cd "{pk["raiz"]}"; python -m pytest -q ' + " ".join(f["id"] for f in pk["vigias"][:8]))
        w("```")
    else:
        w("- NO_ENCONTRADO: **este flujo no tiene vigia.** Se escribe la vigia PRIMERO, luego se repara.")
    w("")

    w("## 5. A QUIEN PUEDE DANAR TOCAR ESTO (cross-flow obligatorio)")
    if pk["dana"]:
        for pieza, por, de in pk["dana"][:20]:
            w(f"- `{pieza}` — lo {por.lower()} desde `{de}`")
        w("")
        w("Antes de sellar, declara cual de estos revisaste.")
    else:
        w("- Nadie depende de estas piezas. Reparacion aislada.")
    w("")

    # LA MEMORIA DE FALLOS (orden 6.1 de Julio): que el Ingeniero sepa si ya tropezo aqui.
    try:
        import sys as _s
        _s.path.insert(0, AQUI)
        from cuerpo import fallos as _f
        aviso = _f.aviso_para_el_paquete(pk["problema"], pk["apodo"])
    except Exception:
        aviso = ""
    if aviso:
        w(aviso)
        w("")

    w("## 6. SI NECESITAS ALGO MAS, PIDELO ASI (no lo leas por tu cuenta)")
    w("```")
    w("NECESITO_LEER:")
    w("  archivo:  <ruta exacta>")
    w("  motivo:   <que pregunta responde>")
    w("  decide:   <que decision desbloquea>")
    w("  riesgo:   <que pasa si no lo leo>")
    w("```")
    w("")
    w("## 7. LO QUE NO SE HACE")
    w("- No inventar archivos, funciones ni lineas. Si no esta arriba, se escribe `NO_ENCONTRADO`.")
    w("- No decidir lo que el contrato no dice. Se escribe `PREGUNTA_REQUERIDA:` y se le pregunta a Julio.")
    w("- No sellar con una vigia roja.")
    w("- Una vigia verde NO es prueba. La prueba es que Julio lo vea funcionar.")
    return "\n".join(L)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("Proyectos declarados:", ", ".join(grafo.proyectos()) or "(ninguno)")
        return 1
    apodo, problema = sys.argv[1], " ".join(sys.argv[2:])
    pk = armar(apodo, problema)
    txt = a_texto(pk)
    os.makedirs(PAQUETES, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in problema.lower())[:40]
    destino = os.path.join(PAQUETES, f"{apodo}__{slug}.md")
    open(destino, "w", encoding="utf-8").write(txt)
    n = len(txt.splitlines())
    print(f"PAQUETE: {destino}")
    print(f"  lineas del paquete : {n}")
    print(f"  lineas del proyecto: {pk['total_proyecto']:,}")
    print(f"  AHORRO             : {100 - n * 100 / max(1, pk['total_proyecto']):.1f}%")
    if n > TOPE_LINEAS:
        print(f"  AVISO: el paquete pasa de {TOPE_LINEAS} lineas. Afina el problema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
