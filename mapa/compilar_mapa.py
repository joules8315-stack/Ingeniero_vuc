# -*- coding: utf-8 -*-
"""compilar_mapa.py -- convierte MAPA_INGENIERO.json en MAPA_INGENIERO.md (para Julio).
El mapa es VIVO: se regenera, no se escribe a mano. Estilo copiado de arnes/compilar_mapa.py del MVP2.
"""
import json, os
from collections import defaultdict

base = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(base, "MAPA_INGENIERO.json"), encoding="utf-8"))
P = d["piezas"]

def de(proy, rol=None):
    return [p for p in P if p["proyecto"].startswith(proy) and (rol is None or p["rol"] == rol)]

L = []
w = L.append
w("# MAPA DEL INGENIERO VUC — paso 1 (inventario real, sin suposiciones)")
w("> Generado por `mapa/inventario.py` + `mapa/compilar_mapa.py`. NO se edita a mano: se regenera.")
w("> Regla: aqui solo entra lo que EXISTE en disco. Lo que no aparece, no existe.")
w("")
w(f"**Universo:** {d['total_piezas']} piezas · {d['total_lineas']:,} lineas · 4 proyectos.")
w("")
w("## 1. Cuanto hay en cada proyecto")
w("")
w("| Proyecto | Piezas |")
w("|---|---|")
for k, v in sorted(d["por_proyecto"].items(), key=lambda x: -x[1]):
    w(f"| {k} | {v} |")
w("")
w("## 2. Que tipo de piezas hay")
w("")
w("| Rol | Cuantas |")
w("|---|---|")
for k, v in sorted(d["por_rol"].items(), key=lambda x: -x[1]):
    w(f"| {k} | {v} |")
w("")
w("## 3. EL CUERPO que ya existe (no se vuelve a construir)")
w("")
w(r"Ruta: `C:\Users\USER\dev\Asesor Marketing\cuerpo`")
w("")
w("| Modulo | Lineas | Que hace | Boca (API publica) |")
w("|---|---|---|---|")
for p in sorted(de("DMM", "CUERPO (modulo)"), key=lambda x: -x["lineas"]):
    api = ", ".join(p["api"][:6]) or "-"
    w(f"| `{p['ruta']}` | {p['lineas']} | {(p['resumen'] or '-')[:90]} | {api} |")
w("")
w("## 4. LAS 5 CAPAS DE MEMORIA que ya estan (base del cerebro tipo Obsidian)")
w("")
w("| Capa | Pieza | Estado |")
w("|---|---|---|")
capas = [("1. RAG semantico", "cuerpo/rag.py"), ("2. Indice", "cuerpo/indice.py"),
         ("2b. Indice semantico", "cuerpo/indice_semantico.py"), ("2c. Embeddings", "cuerpo/embeddings.py"),
         ("3. Grafo (dependencias)", "cuerpo/grafo.py"), ("3b. Grafo de negocio", "cuerpo/grafo_negocio.py"),
         ("4. Persistencia", "cuerpo/almacen.py"), ("5. Aprendizaje", "cuerpo/memoria.py")]
idx = {p["ruta"]: p for p in de("DMM")}
for nom, ruta in capas:
    p = idx.get(ruta)
    w(f"| {nom} | `{ruta}` | {'EXISTE (' + str(p['lineas']) + ' lineas)' if p else 'NO EXISTE'} |")
w("")
w("## 5. EL ARNES que ya existe (metodo de trabajo a copiar y mejorar)")
w("")
w("| Pieza | Lineas | Que hace |")
w("|---|---|---|")
for p in sorted(de("DMM", "ARNES/CANDADO") + [x for x in de("DMM") if x["ruta"].startswith("arnes/")],
                key=lambda x: x["ruta"]):
    if p["ruta"].endswith((".json", ".md")) and "protocolo" not in p["ruta"]:
        continue
    w(f"| `{p['ruta']}` | {p['lineas']} | {(p['resumen'] or '-')[:100]} |")
w("")
w("## 6. CONTRATOS (las leyes ya escritas)")
w("")
c = de("DMM", "CONTRATO")
w(f"Son **{len(c)}** contratos. Los que mandan sobre el Ingeniero:")
w("")
clave = ["MAESTRO_AHORRO", "AHORRO_DE_TOKENS", "MEMORIA", "CUERPO_Y_RAG", "INGENIERO_AUTONOMO",
         "INGENIERO_ROLES", "PROTOCOLO_MAESTRO", "NUNCA_ASUMAS", "ESTADO_CANONICO", "ARQUITECTURA"]
for p in c:
    if any(k in p["ruta"].upper() for k in clave):
        w(f"- `{p['ruta']}` ({p['lineas']} lineas) — {(p['resumen'] or '')[:110]}")
w("")
w("## 7. MATRIZ Y TABLA DE LA VERDAD")
w("")
for p in de("DMM", "MATRIZ/TABLA_VERDAD") + de("Foto", "MATRIZ/TABLA_VERDAD"):
    w(f"- `{p['proyecto']}` :: `{p['ruta']}` ({p['lineas']} lineas)")
w("")
w("## 8. LOS ARCHIVOS MONSTRUO (los que queman tokens al releerlos)")
w("")
w("| Proyecto | Archivo | Lineas |")
w("|---|---|---|")
for p in sorted([x for x in P if x["lineas"] > 800 and x["rol"] in ("CODIGO", "WEB", "VIGIA")],
                key=lambda x: -x["lineas"])[:12]:
    w(f"| {p['proyecto']} | `{p['ruta']}` | {p['lineas']:,} |")
w("")
w("## 9. REPETIDERA DETECTADA")
w("")
w(f"- Copias con contenido identico en 2+ lugares: **{len(d['duplicados_identicos'])}**")
w(f"- Mismo nombre de archivo en 2+ lugares: **{len(d['duplicados_por_nombre'])}**")
w(r"- `C:\vigias` (52 vigias): comparada una por una contra la carpeta buena.")
w("  **Nada unico. Solo 2 pruebas rescatables:**")
w("  - `test_vigia_cerebro_gemini.py::test_sin_llave_error_claro_no_silencio`")
w("  - `test_vigia_credenciales_env.py::test_carga_llaves_del_env_sin_pisar_las_existentes`")
w("  El resto es copia vieja -> se desecha DESPUES de rescatar esas dos.")
w("")
w("## 10. LO QUE **NO** EXISTE (lo que hay que construir)")
w("")
w("| Falta | Por que importa |")
w("|---|---|")
w("| `router_contexto.py` | Nadie arma el paquete minimo. El grafo existe pero nadie lo usa para eso. Busqueda: 0 resultados. |")
w("| `guard_alcance.py` (candado de LECTURA) | El arnes frena EDITAR, no frena LEER. El gasto esta en la lectura. |")
w("| Vigias anti-token | De 190 vigias, NINGUNA vigila el gasto ni el alcance de lectura. |")
w("| `CLAUDE.md` + `.claude/rules/` | Ningun proyecto los tiene. Sin eso, la IA entra a ciegas y lee entero. |")
w("| `STATE.json` del Ingeniero | El estado vive en el chat; al cerrarse, se pierde y hay que repetir. |")
w("| Cerebro propio del Ingeniero | `cuerpo/` es el cuerpo de DMM (marketing), no el del Ingeniero. |")
w("| HULK | Julio lo nombro. Busqueda en los 4 proyectos: **NO EXISTE**. Falta que Julio diga que es. |")
w("")

open(os.path.join(base, "MAPA_INGENIERO.md"), "w", encoding="utf-8").write("\n".join(L))
print("MAPA_INGENIERO.md escrito:", len(L), "lineas")
