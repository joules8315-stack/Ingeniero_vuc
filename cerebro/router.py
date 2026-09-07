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
from . import grafo, flujos, trozos, enlaces, piezas

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAQUETES = os.path.join(AQUI, "memoria", "paquetes")
TOPE_LINEAS = 800   # un paquete mas largo que esto ya no es un paquete: es releer el proyecto
# Hasta que tamano vale la pena traer una funcion ENTERA en vez del trozo suelto (2026-09-05).
# Medido: una funcion de 700 renglones abarcaba el 87% de su archivo, y el paquete se fue a 963
# lineas. Traer la funcion entera cura los pedazos huerfanos, pero pasado este tope sale mas caro
# que el problema que resuelve, asi que se manda el trozo con su cabecera delante.
TOPE_FUNCION_ENTERA = 120


def _claves_de(g, nombres_flujo):
    cl = []
    for n in nombres_flujo:
        cl += g["flujos"].get(n, {}).get("claves", [n])
    return sorted(set(cl))


def _lineas_de(ruta, desde, hasta):
    """Lee las lineas `desde`..`hasta` (1-indexado) de un archivo. Devuelve lista de lineas.

    Para la ley L13/L14 (Julio, 2026-08-27): cuando el repartidor se toca a si mismo, hay que
    traer la funcion completa, no un trozo cortado por el fragmentador.
    """
    try:
        with open(ruta, encoding="utf-8", errors="ignore") as f:
            lineas = f.read().splitlines()
        return lineas[max(0, desde - 1):min(len(lineas), hasta)]
    except Exception:
        return []


def _las_que_hablan_del_problema(g, problema, cuantas=4):
    """Las piezas de CODIGO que mas tienen que ver con el problema, sin abrir un solo archivo.

    Se mira solo la FICHA de cada pieza —su nombre, su resumen y lo que ofrece— que es barato y
    ya esta en el indice. Abrir 1.089 archivos para decidir cual abrir seria absurdo y lento.

    Se prefiere el codigo de VERDAD antes que las pruebas: las pruebas hablan muchisimo del
    asunto (lo describen palabra por palabra) y por eso ganaban sitio y dejaban fuera al archivo
    donde esta el fallo. Una prueba cuenta lo que deberia pasar; el codigo es donde pasa.
    """
    palabras = set(trozos._palabras(problema))
    if not palabras:
        return sorted([p for p in g["piezas"] if p["rol"] in ("CODIGO", "WEB", "CUERPO")],
                      key=lambda x: -x["lineas"])[:cuantas]
    puntuadas = []
    for p in g["piezas"]:
        if p["rol"] not in ("CODIGO", "WEB", "CUERPO", "CEREBRO"):
            continue
        api_nombres = " ".join(a["nombre"] for a in (p.get("api", []) or []))
        ficha = " ".join([p["id"], p.get("resumen", "") or "", api_nombres])
        suyas = set(trozos._palabras(ficha))
        punto = float(len(palabras & suyas))
        nombre = p["id"].lower()
        if "test" in nombre or "prueba" in nombre or "vigia" in nombre:
            punto *= 0.4          # la prueba describe; el codigo hace
        if p["rol"] == "WEB":
            punto += 0.5          # la cara es donde Julio ve el fallo con sus ojos
        puntuadas.append((punto, p["lineas"], p))
    puntuadas.sort(key=lambda t: (-t[0], -t[1]))
    elegidas = [p for punto, _, p in puntuadas[:cuantas] if punto > 0]
    # Si nada casa, se vuelve a lo de antes: mejor las grandes que nada.
    return elegidas or [p for _, _, p in puntuadas[:cuantas]]


def _leyes_que_hablan_del_problema(g, problema, cuantas=4):
    """Contratos/matriz/protocolo de TODO el grafo que hablen del problema, aunque no esten en un
    flujo. 2026-08-24: sin esto, un contrato NUEVO no entraba al paquete y el equipo no podia
    construir el modulo que legisla (no veia el material y, correctamente, no inventaba)."""
    palabras = set(trozos._palabras(problema))
    if not palabras:
        return []
    puntuadas = []
    for p in g["piezas"]:
        if p["rol"] not in ("CONTRATO", "MATRIZ", "PROTOCOLO"):
            continue
        ficha = " ".join([p["id"], p.get("resumen", "") or ""])
        comunes = len(palabras & set(trozos._palabras(ficha)))
        if comunes:
            puntuadas.append((comunes, p))
    puntuadas.sort(key=lambda t: -t[0])
    return [p for _, p in puntuadas[:cuantas]]


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

    # Si el flujo no toco ningun codigo, se buscan las piezas que HABLAN DEL PROBLEMA.
    #
    # Antes se cogian las TRES MAS GRANDES, por numero de lineas. Eso es elegir por tamano, y el
    # archivo mas gordo no es el que tiene el fallo: en el MVP, un problema de LA PANTALLA traia
    # el servidor (16.845 lineas) y la pantalla (2.349) no entraba NUNCA. El equipo lo dijo tres
    # veces seguidas: "el archivo app_web.html no esta en el material". Fallo real 2026-08-21.
    # Es ademas lo contrario de la regla de Julio: se busca por lo que la cosa HACE, no por como
    # de grande es.
    codigo = [f for f in fichas if f["rol"] in ("CUERPO", "CODIGO", "WEB", "CEREBRO")]
    if not codigo:
        candidatas = _las_que_hablan_del_problema(g, problema)
        fichas += candidatas
        codigo = candidatas

    # LO QUE EL PROBLEMA NOMBRA, ENTRA (Julio, 2026-08-27, ley L13/L14).
    # Cuando Julio (o el encargo) dice el nombre exacto de una parte del programa, esa parte DEBE
    # entrar al material. Hoy se ignora: se nombra "app_web.html" y el repartidor devuelve solo las
    # pruebas o vigias, no la pantalla; el equipo no puede revisar ni aprobar, y todo se atasca.
    # Regla general: se detectan en el texto del problema las rutas/archivos que existen en el grafo
    # del proyecto (p.ej. app_web.html, app.py, rv3_prueba_x.py), y se agregan al material. Aplica a
    # TODOS los proyectos: el ingeniero es el central y transmite a los demas. Es el pedazo que hace
    # falta, no el archivo entero (los hay de 16 mil renglones: ni caben ni sirven).
    # Se guarda en _nombrados para que su trozo se agregue despues de que exista `pedazos`.
    _nombrados = []
    try:
        import re as _re
        for m in _re.finditer(r"([A-Za-z0-9_\\/.\-]+\.(?:py|html|js|css|ts|json|md))", problema):
            pieza = m.group(1).replace("\\", "/")
            base = pieza.split("/")[-1]
            ficha = next((p for p in g["piezas"]
                          if p["id"].replace("\\", "/").endswith(pieza)
                          or p["id"].split("/")[-1] == base), None)
            if not ficha or ficha in codigo:
                continue
            codigo.append(ficha)
            if ficha not in fichas:
                fichas.append(ficha)
            _nombrados.append(ficha["id"])
    except Exception:
        _nombrados = []

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

    # EL DICCIONARIO (Claude + Cline, 2026-08-25): si este problema YA se reparo antes, aqui esta
    # el sitio exacto del codigo, dicho en palabras de Julio. Es justo lo que la busqueda por
    # letras nunca logra (Julio habla espanol y de negocio; el codigo, ingles y comprimido). Se
    # agregan esos sitios PROBADOS al material, para que el paquete traiga el programa y no solo
    # las vigias recien escritas.
    diccionario_sitios = []
    try:
        sys.path.insert(0, AQUI)
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        from arnes import diccionario as _dic
        diccionario_sitios = _dic.buscar(problema, apodo)[:4]
        for sitio in diccionario_sitios:
            sufijo = str(sitio.get("archivo") or "").replace("\\", "/")
            if not sufijo:
                continue
            ficha = next((p for p in g["piezas"]
                          if p["id"].replace("\\", "/").endswith(sufijo)), None)
            if ficha and ficha not in codigo:
                codigo.append(ficha)
                if ficha not in fichas:
                    fichas.append(ficha)
    except Exception:
        pass

    # EL ROUTER SE CORRIGE SOLO (orden 3 de Julio, 2026-08-20).
    # Si en un problema del mismo flujo el paquete se quedo CORTO, el medidor apunto QUE falto.
    # Aqui se lee ese apunte y se mete esa pieza, para no repetir el mismo hueco dos veces.
    # Es lo que convierte el medidor en aprendizaje: medir sin corregir no sirve de nada.
    try:
        import re as _re
        sys.path.insert(0, AQUI)
        from cuerpo import medidor as _med
        for f in _med.lo_que_falto(apodo):
            if not (set(f.get("flujos", [])) & set(nombres)):
                continue
            for texto_falto in f.get("falto", []):
                for pieza in _re.findall(r"[\w/]+\.(?:py|html|js)", str(texto_falto)):
                    base = pieza.split("/")[-1]
                    extra = grafo.ficha(g, pieza) or next(
                        (p for p in g["piezas"] if p["id"].split("/")[-1] == base), None)
                    if extra and extra not in codigo:
                        codigo.append(extra)
                        if extra not in fichas:
                            fichas.append(extra)
    except Exception:
        pass

    claves = _claves_de(g, nombres)
    b = trozos.Buscador(codigo)
    # Se piden MAS candidatos de los que se van a entregar: los sobrantes son la materia prima
    # del re-ordenado por significado. Contar palabras es gratis; el significado se paga.
    pedazos = b.buscar(problema, k=k_trozos * 2, exigir=claves or None)
    if not pedazos:                       # el filtro de asunto puede ser muy duro: se afloja
        pedazos = b.buscar(problema, k=k_trozos * 2)

    # POR SIGNIFICADO, NO SOLO POR LETRAS (orden 4 de Julio, 2026-08-20).
    # Contar palabras no entiende sinonimos: el contrato dice "perfil" y el codigo "onboarding".
    # Se reordenan SOLO los candidatos que ya trajo el buscador (1 llamada, no 600), y si no
    # hay llave o cuota se queda el orden de siempre: nunca deja al Ingeniero sin buscador.
    if os.environ.get("INGENIERO_SIN_SIGNIFICADO", "").strip():
        pedazos = pedazos[:k_trozos]
    else:
        try:
            from . import semantico
            pedazos = semantico.reordenar(problema, pedazos, campo="texto", k=k_trozos)
        except Exception:
            pedazos = pedazos[:k_trozos]

    # LA HERRAMIENTA SE REPARA MIENTRAS CONSTRUYE (Julio, 2026-08-27, ley L13/L14).
    # Cuando el problema toca al REPARTIDOR, el fragmentador corta router.py en trozos de 40 lineas
    # y elige por relevancia: trae 1-40 y 129-168, pero NO la funcion `armar` completa (87-227).
    # Entonces el equipo no ve el codigo que hay que tocar, no puede validar, y rechaza. Es el
    # circulo que bloquea todo el proyecto. Cura: si el paquete incluye cerebro/router.py como pieza
    # de codigo, se garantiza que su trozo cubra la funcion `armar` entera, para que quien lo repare
    # vea la funcion completa y no un pedazo huerfano.
    try:
        router_id = "cerebro/router.py"
        soy = next((p for p in codigo if p["id"].replace("\\", "/").endswith(router_id)), None)
        if soy:
            # La funcion armar() se busca POR SU NOMBRE, nunca por un numero de renglon.
            # Antes aqui habia dos numeros escritos a mano, y se rompian en cuanto alguien anadia
            # algo mas arriba: apuntaban a otro sitio y el equipo recibia un pedazo huerfano.
            # El nombre no se mueve. Ley: CONTRATO_SE_BUSCA_POR_NOMBRE.md (Julio, 2026-08-31).
            hallazgo = piezas.funcion_completa(soy["abs"], "armar")
            if hallazgo:
                desde_armar = hallazgo["desde"]
                hasta_armar = hallazgo["hasta"]
                texto_armar = hallazgo["texto"]
                ya = any(t["pieza"] == soy["id"] and t["desde"] <= desde_armar
                         and t["hasta"] >= hasta_armar for t in pedazos)
                if not ya and texto_armar:
                    pedazos.insert(0, {"pieza": soy["id"], "abs": soy["abs"], "rol": soy["rol"],
                                       "desde": desde_armar, "hasta": hasta_armar,
                                       "direccion": "%s:%s-%s" % (router_id, desde_armar, hasta_armar),
                                       "texto": texto_armar, "puntaje": 99.0,
                                       "_completo": "armar"})
    except Exception:
        pass

    # GENERALIZAR LA REPARACION A CUALQUIER FUNCION (Julio, 2026-09-05).
    # El bloque de arriba solo arregla el caso de `armar`. El mismo problema ocurre con cualquier
    # otra funcion: el fragmentador entrega pedazos huerfanos. Esta funcion generaliza esa cura.
    pedazos = completar_funciones(pedazos, codigo)
    # (la funcion vive al final de este archivo, junto a las demas ayudas)

    # LO QUE EL PROBLEMA NOMBRA COMO FUNCION, ENTRA ENTERO (Julio, 2026-09-06).
    # Si el problema nombra una funcion que no cayo en ningun trozo elegido por relevancia,
    # nunca se trae. Se recorre el texto del problema y, por cada palabra que sea el nombre de
    # una funcion dentro de alguna pieza de codigo del paquete, se comprueba con
    # piezas.funcion_completa(ruta_abs, palabra) y si no esta ya en pedazos, se anade entera
    # respetando el tope TOPE_FUNCION_ENTERA.
    try:
        import re as _re2
        for _palabra in set(_re2.findall(r"[A-Za-z_][A-Za-z0-9_]*", problema)):
            for _ficha_codigo in codigo:
                if not _ficha_codigo.get("abs"):
                    continue
                _hallazgo = piezas.funcion_completa(_ficha_codigo["abs"], _palabra)
                if not _hallazgo:
                    continue
                _texto_funcion = _hallazgo["texto"]
                _lineas_funcion = _hallazgo["hasta"] - _hallazgo["desde"] + 1
                if _lineas_funcion > TOPE_FUNCION_ENTERA:
                    continue
                _ya_en_pedazos = any(
                    t["pieza"] == _ficha_codigo["id"] and t["desde"] <= _hallazgo["desde"]
                    and t["hasta"] >= _hallazgo["hasta"] for t in pedazos)
                if not _ya_en_pedazos and _texto_funcion:
                    pedazos.insert(0, {"pieza": _ficha_codigo["id"], "abs": _ficha_codigo["abs"],
                                       "rol": _ficha_codigo["rol"],
                                       "desde": _hallazgo["desde"], "hasta": _hallazgo["hasta"],
                                       "direccion": "%s:%s-%s" % (_ficha_codigo["id"], _hallazgo["desde"], _hallazgo["hasta"]),
                                       "texto": _texto_funcion, "puntaje": 99.0,
                                       "_completo": _palabra})
    except Exception:
        pass

    # LO QUE EL PROBLEMA NOMBRA, ENTRA SU PEDAZO (Julio, 2026-08-27, ley L13/L14).
    # Los archivos nombrados ya se agregaron a `codigo`/`fichas`. Aqui se garantiza que su trozo
    # llegue al material: si el fragmentador por relevancia no lo trajo, se pide el pedazo del
    # archivo. Es la pantalla (app_web.html) o el motor (app.py) que el equipo necesita ver para
    # revisar y aprobar; sin el, todo se atasca.
    try:
        for fid in list(_nombrados):
            ficha = next((p for p in codigo if p["id"] == fid), None)
            if not ficha or not ficha.get("abs"):
                continue
            texto = "\n".join(_lineas_de(ficha["abs"], 1, min(80, ficha.get("lineas", 80) or 80)))
            if not texto.strip():
                continue
            ya = any(t["pieza"] == fid for t in pedazos)
            if not ya:
                pedazos.insert(0, {"pieza": fid, "abs": ficha["abs"], "rol": ficha["rol"],
                                   "desde": 1, "hasta": min(80, ficha.get("lineas", 80) or 80),
                                   "direccion": "%s:1-%s" % (fid, min(80, ficha.get("lineas", 80) or 80)),
                                   "texto": texto, "puntaje": 99.0, "_nombrado": fid})
    except Exception:
        pass

    leyes = sorted([f for f in fichas if f["rol"] in ("CONTRATO", "MATRIZ", "PROTOCOLO")],
                   key=lambda x: x["id"])
    # 2026-08-24: incluir los contratos que HABLAN del problema aunque no esten en un flujo.
    # Sin esto el equipo no veia un contrato nuevo y no podia construir lo que legisla.
    for f in _leyes_que_hablan_del_problema(g, problema):
        if f not in leyes:
            leyes.append(f)
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
            "diccionario": diccionario_sitios,
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

    if pk.get("diccionario"):
        w("## 0. ESTO YA SE REPARO ANTES (no lo re-descubras)")
        for s in pk["diccionario"][:3]:
            w(f"- `{s.get('archivo')}` ({s.get('funcion')}, linea {s.get('linea')}) "
              f"— cuando pasaba: {str(s.get('problema'))[:70]}")
        w("")

    w("## 1. LA LEY QUE MANDA AQUI")
    if pk["leyes"]:
        for f in pk["leyes"]:
            w(f"- `{f['id']}` ({f['lineas']} lineas) — {f['resumen'][:120] or 's/resumen'}")
        w("")
        w("### Texto de la ley que manda aqui (primera de la lista):")
        w("```")
        f = pk["leyes"][0]
        try:
            if os.path.exists(f.get("abs", "")):
                with open(f["abs"], encoding="utf-8", errors="ignore") as _archivo_ley:
                    _texto_ley = _archivo_ley.read()
                _lineas_ley = _texto_ley.splitlines()
                if len(_lineas_ley) > 400:
                    w("\n".join(_lineas_ley[:400]))
                    w("")
                    w("... [AVISO: la ley se corto en 400 lineas por el tope del paquete]")
                else:
                    w(_texto_ley)
            else:
                w("NO_ENCONTRADO")
        except Exception:
            w("NO_ENCONTRADO")
        w("```")
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
        _MAX_VIGIAS = 12   # F8: no listar todas, o el paquete crece y deja de ser minimo
        for f in pk["vigias"][:_MAX_VIGIAS]:
            w(f"- `{f['id']}`")
        if len(pk["vigias"]) > _MAX_VIGIAS:
            w(f"- ... y {len(pk['vigias']) - _MAX_VIGIAS} vigias mas.")
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


def completar_funciones(pedazos, codigo):
    """Si un trozo cae DENTRO de una funcion, se entrega la funcion ENTERA. Nada mas.

    Julio, 2026-09-05: "estos son repos muy grandes y no tienes el contexto... ese es el objetivo
    de la memoria y del repartidor, que no has podido resolver".

    EL FALLO, MEDIDO: los trozos se eligen por parecido de palabras en ventanas de 40 renglones, y
    las palabras no saben donde empieza ni acaba una funcion. Resultado: pedazos huerfanos.
      · pidiendo la funcion que escribe una casilla, llegaron las lineas 1-80 (la portada del
        archivo) y la funcion estaba en la 5300;
      · pidiendo la funcion `cortar`, llegaron 1-40 y 129-168, y `cortar` empieza en la 54.
    El auditor rechazaba esas rondas diciendo que se usaban cosas inventadas, y esas cosas estaban
    declaradas en renglones que el paquete nunca le enseño. 2 de 70 trabajos sirvieron.

    Aqui arriba ya se hacia esto MISMO, pero solo para `armar`, con el nombre escrito a mano. Esto
    lo generaliza: la cura existia y se usaba una sola vez.

    NO se traen las funciones vecinas (eso seria gastar de mas) y NO se toca lo que esta fuera de
    toda funcion: las importaciones y las constantes de arriba son justo lo que evita que el
    auditor crea que algo esta inventado.
    """
    if not pedazos:
        return pedazos
    por_id = {}
    for p in (codigo or []):
        por_id[p.get("id")] = p
    salida, ya_entera = [], set()
    for t in pedazos:
        pieza = por_id.get(t.get("pieza"))
        abs_path = (pieza or {}).get("abs") or t.get("abs")
        if not abs_path or not str(abs_path).lower().endswith(".py"):
            salida.append(t)
            continue
        try:
            duena = piezas.funcion_que_contiene(abs_path, t.get("desde"), t.get("hasta"))
        except Exception:
            duena = None                       # leer mal una pieza no puede tumbar el paquete
        if not duena:
            salida.append(t)                   # fuera de toda funcion: se respeta tal cual
            continue
        # TOPE DE TAMANO (2026-09-05, lo cazo la vigia que vigila el GASTO). Una funcion de 700
        # renglones abarcaba el 87% de su archivo: traerla entera es releer el repo por la puerta
        # de atras. Si pasa del tope, se manda el trozo tal cual PERO con su cabecera delante, que
        # es lo minimo para que el auditor sepa de donde sale y no crea que algo esta inventado.
        if (duena["hasta"] - duena["desde"] + 1) > TOPE_FUNCION_ENTERA:
            cabecera = duena["texto"].splitlines()[:1]
            nuevo = dict(t)
            nuevo["texto"] = "\n".join(cabecera + ["    # ... (funcion larga: solo el trozo)"] +
                                       str(t.get("texto") or "").splitlines())
            salida.append(nuevo)
            continue
        marca = (t.get("pieza"), duena["nombre"])
        if marca in ya_entera:
            continue                           # esa funcion ya va: no se paga dos veces
        ya_entera.add(marca)
        nuevo = dict(t)
        nuevo.update({"desde": duena["desde"], "hasta": duena["hasta"], "texto": duena["texto"],
                      "direccion": "%s:%s-%s" % (t.get("pieza"), duena["desde"], duena["hasta"]),
                      "_completo": duena["nombre"]})
        salida.append(nuevo)
    return salida


if __name__ == "__main__":
    sys.exit(main())
