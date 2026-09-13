# -*- coding: utf-8 -*-
"""cerebro/protocolo.py — EL GRAFO DE LA FORMA DE TRABAJO (Julio, 2026-08-20).

  "indexa toda la forma de trabajo, crea el grafo que te lo recuerde siempre, crea el arnes,
   vigilantes, helpers, y todo lo que necesites, para que siempre sigas la misma ruta. Asi mismo
   como debes buscar la informacion, como preguntar, cuando hacerlo."

QUE ES: el grafo de las otras capas mapea el CODIGO. Este mapea el METODO. Los 8 pasos, en
orden, cada uno con lo que exige, lo que prohibe, su candado y de que documento de Julio sale.

POR QUE HACE FALTA: el protocolo estaba escrito en tres documentos distintos, en dos proyectos
distintos, y se violo entero el 2026-08-20. Un metodo que hay que recordar no se sigue. Uno que
el sistema te recuerda en cada momento, si.

LO QUE APORTA SOBRE UN DOCUMENTO SUELTO:
  · sabe EN QUE PASO se esta ahora mismo (mirando el estado real, no preguntando)
  · dice QUE TOCA AHORA y QUE ESTA PROHIBIDO ahora
  · dice si el paso tiene candado o si es solo un deseo
  · indexa los documentos de metodo de TODOS los proyectos, para citarlos con archivo:linea
"""
import os, sys, json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

# ─── LOS 8 PASOS: el grafo del metodo ─────────────────────────────────────────
PASOS = [
    {
        "n": 1, "nombre": "¿Estoy donde debo?",
        "exige": ["ruta canonica del proyecto", "rama canonica",
                  "que no haya copias mas nuevas del proyecto por el disco"],
        "prohibe": ["trabajar en una copia vieja", "guardar en otra rama"],
        "candado": "arnes/via_canonica.py",
        "comando": "python ingeniero.py via",
        "fuente": "PROTOCOLO_MVP § 1 precheck + LEY 0 de DMM (una sola via)",
        "listo_si": lambda e: True,
    },
    {
        "n": 2, "nombre": "Buscar solo lo necesario, en orden",
        "exige": ["punto de retomada", "contrato del flujo", "objetivos", "tabla de la verdad",
                  "historico de fallos", "el archivo:linea exacto del rastro"],
        "prohibe": ["explorar a ciegas", "abrir archivos enteros",
                    "mas de 2 lecturas fuera de la lista (a la tercera: parar y preguntar)"],
        "candado": "arnes/read_gate.py",
        "comando": 'python ingeniero.py trabaja <proyecto> "<problema>"',
        "fuente": "PROTOCOLO_MVP § 2 (mapa cerrado de lectura)",
        "listo_si": lambda e: bool(e.get("paquete")),
    },
    {
        "n": 3, "nombre": "Causa raiz, nunca sintoma",
        "exige": ["archivo", "funcion", "linea", "flujo reproducido", "evidencia medida"],
        "prohibe": ["reparar lo inferido", "tapar aguas abajo lo que se rompio aguas arriba",
                    "proponer una solucion antes de localizar el fallo"],
        "candado": "arnes/candado_diagnostico.py",
        "comando": 'python ingeniero.py causa <proyecto> --archivo .. --funcion .. --linea .. --evidencia ".."',
        "fuente": "PROTOCOLO_MVP § 6 (diagnostico)",
        "listo_si": lambda e: _causa_declarada(),
    },
    {
        "n": 4, "nombre": "Agotar las fuentes antes de preguntar",
        "exige": ["haber mirado objetivos, contratos, historico, tabla de verdad y matriz",
                  "citar archivo:linea de lo que dice cada fuente"],
        "prohibe": ["preguntarle a Julio algo que ya escribio",
                    "preguntar sin decir donde se busco"],
        "candado": "arnes/candado_preguntar.py",
        "comando": 'python ingeniero.py duda "<lo que no se>" --proyecto <proyecto>',
        "fuente": "PROTOCOLO_MVP § 22 (Julio, 2026-07-15) + Ley 16 del Ingeniero",
        "listo_si": lambda e: not e.get("decision_pendiente"),
    },
    {
        "n": 5, "nombre": "Confirmar el objetivo antes de construir",
        "exige": ["repetirle a Julio con palabras propias el RESULTADO que quiere",
                  "esperar su 'si'"],
        "prohibe": ["construir sin su 'si'", "irse por el camino facil cuando pide otra cosa"],
        "candado": "arnes/candado_protocolo.py construir",
        "comando": "python ingeniero.py objetivo-confirmado",
        "fuente": "PROTOCOLO_DEL_CHAT — LEY DURA (Julio, 2026-07-28)",
        "listo_si": lambda e: True,
    },
    {
        "n": 6, "nombre": "Plan cerrado y reparacion minima",
        "exige": ["archivos y funciones exactas", "a quien puede danar",
                  "que pruebas se corren", "cuando se da por cerrado"],
        "prohibe": ["tocar codigo sin el paquete del asunto",
                    "mas de un fallo o mas de dos funciones a la vez"],
        "candado": "arnes/edit_gate_universal.py",
        "comando": 'python ingeniero.py trabaja <proyecto> "<problema>"',
        "fuente": "PROTOCOLO_MVP § 7 (plan cerrado, compuerta obligatoria)",
        "listo_si": lambda e: bool(e.get("vigias_antes")),
    },
    {
        "n": 7, "nombre": "La prueba la manda la realidad",
        "exige": ["prueba nueva por cada causa reparada", "que la escriba OTRO, no el que reparo",
                  "probarla metiendole el fallo a proposito", "abrirlo de verdad y mirarlo"],
        "prohibe": ["dar algo por bueno porque la prueba este verde",
                    "que el que repara escriba su propia prueba",
                    "fingir que una prueba cubre lo que el usuario ve cuando no lo cubre",
                    "pedirle a Julio que pruebe sin haber corrido la prueba real interna (con equipo, Playwright)"],
        "candado": "arnes/candado_cierre.py + cuerpo/cruzado.py + arnes/candado_prueba_real.py",
        "comando": "python ingeniero.py pedir-prueba",
        "fuente": "PROTOCOLO_MVP § 10 y § 19 + Ley 5 (vigia verde NO es prueba)",
        "listo_si": lambda e: e.get("prueba_humana") == "HECHA",
    },
    {
        "n": 8, "nombre": "Legislar, sellar y aprender",
        "exige": ["contrato + prueba + aplicar", "sellar en la rama canonica",
                  "apuntar el fallo con su 'no volver a'"],
        "prohibe": ["sellar con una prueba roja", "dejar una ley sin candado"],
        "candado": "sellar.sh",
        "comando": 'bash sellar.sh "<lo que cambio>"',
        "fuente": "PROTOCOLO_DEL_CHAT § despues + PROTOCOLO_MVP § 11",
        "listo_si": lambda e: False,
    },
]

# ─── EL NORTE: manda sobre los pasos ──────────────────────────────────────────
NORTE = [
    ("Consolidar a UNA sola version", "una reparacion que no consolida, o que rompe otro flujo, se RECHAZA"),
    ("Decision por pieza", "CONSERVAR / FUSIONAR / ELIMINAR / CONGELAR — una y solo una"),
    ("Una sola fuente de verdad", "las copias y cachas son espejo, nunca autoridad"),
    ("Cero perdida de trabajo", "se confirma donde quedo guardado; fuera de la via canonica es fallo"),
    ("No asumir nada", "lo que no se dijo se convierte en BUSQUEDA, no en suposicion"),
]

LEYES_DURAS = [
    ("Hablarle simple a Julio", "no es tecnico; prohibida la jerga y los nombres de archivos"),
    ("Nunca asumir", "si no esta: NO_ENCONTRADO. Si falta decidir: PREGUNTA_REQUERIDA"),
    ("Que Julio no repita", "si repite, fallo el sistema: mirar por que se ignoro la primera vez"),
    ("No romper lo de al lado", "antes de tocar, mirar a quien se puede danar"),
    ("No duplicar", "antes de crear, buscar; lo viejo se migra o se borra, nunca queda suelto"),
    ("El volumen lo hacen los ayudantes gratis", "aqui solo se dirige y se leen veredictos"),
    ("Siempre en equipo, sin salto", "aplica a TODAS las IA (Claude, Cline, ChatGPT); para saltarlo se pide permiso y la respuesta es SIEMPRE denegado"),
    ("Probar de verdad antes de pedir a Julio", "con el equipo, Playwright; si se logro se avisa a Julio, si no se aprende y se reinicia el ciclo"),
    ("Solo se pregunta despues de buscar", "repo, objetivos, legislacion, tablas de verdad, matriz y errores, todo indexado; nunca antes"),
    ("Todo lo que se habla se legisla", "candado + vigia, sin romper lo que sirve"),
    ("Todo queda limpio y en commit", "lo nuevo se indexa; el guardia lo exige"),
    ("Pruebas reales, no autovalidacion", "Playwright abre el navegador y comprueba de verdad"),
    ("Atento al canal: el que manda, espera", "mensaje a Claude por el canal: revisar cada 5 minutos y esperar una hora en total; al vencer sin respuesta, avisar (Julio 2026-09-13)"),
]


def _causa_declarada():
    try:
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candado_diagnostico as cd
        return cd.vigente() is not None
    except Exception:
        return False


def _estado():
    try:
        from cuerpo import estado
        return estado.leer()
    except Exception:
        return {}


def paso_actual():
    """En que paso estamos AHORA, mirando el estado real. No se pregunta: se mira."""
    e = _estado()
    for p in PASOS:
        try:
            if not p["listo_si"](e):
                return p
        except Exception:
            return p
    return PASOS[-1]


def tiene_candado(p):
    for parte in p["candado"].replace("+", " ").split():
        parte = parte.strip()
        if not parte or "/" not in parte:
            continue
        if not os.path.exists(os.path.join(AQUI, parte.split()[0])):
            return False
    return True


def ahora():
    """Lo que hay que recordar EN ESTE MOMENTO. Corto, para meterlo en cada mensaje."""
    p = paso_actual()
    e = _estado()
    L = ["PASO %d DE 8: %s" % (p["n"], p["nombre"])]
    L.append("  exige   : " + " · ".join(p["exige"][:3]))
    L.append("  PROHIBIDO: " + " · ".join(p["prohibe"][:2]))
    L.append("  hazlo con: " + p["comando"])
    if not tiene_candado(p):
        L.append("  *** este paso NO tiene candado: se puede saltar. Ojo. ***")
    if e.get("decision_pendiente"):
        L.append("  *** PARADO: hay una pregunta para Julio sin hacer ***")
    return "\n".join(L)


def mapa():
    """El grafo entero, para verlo de un vistazo."""
    L = ["MAPA DE LA FORMA DE TRABAJO — 8 pasos, en orden, ninguno se salta", ""]
    actual = paso_actual()
    for p in PASOS:
        marca = ">>" if p["n"] == actual["n"] else "  "
        cand = "candado OK" if tiene_candado(p) else "SIN CANDADO"
        L.append("%s %d. %-42s [%s]" % (marca, p["n"], p["nombre"], cand))
        L.append("      exige    : " + " · ".join(p["exige"]))
        L.append("      prohibe  : " + " · ".join(p["prohibe"]))
        L.append("      viene de : " + p["fuente"])
        L.append("")
    L.append("EL NORTE (manda sobre los pasos):")
    for a, b in NORTE:
        L.append("  · %-34s %s" % (a, b))
    L.append("")
    L.append("LEYES DURAS (por encima de todo):")
    for a, b in LEYES_DURAS:
        L.append("  · %-34s %s" % (a, b))
    return "\n".join(L)


# ─── INDICE DE LOS DOCUMENTOS DE METODO ───────────────────────────────────────
DOCS_METODO = {
    "dmm": ["PROTOCOLO_DEL_CHAT.md", "CONTRATO_PROTOCOLO_MAESTRO.md", "CONTRATO_NUNCA_ASUMAS.md",
            "MAPA_CANONICO.md", "CONTRATOS_Y_LEYES.md", "CONTRATO_ESTADO_CANONICO.md",
            "CONTRATO_MEMORIA.md", "CONTRATO_MAESTRO_AHORRO.md"],
    "foto_informe": ["PROTOCOLO_MVP.md", "CLAUDE.md", "OBJETIVO_MVP.md",
                     "CONTRATO_UNICO_RUTA_P2.md", "CONTRATO_RV2_NO_ASUMIR_CRITERIOS.md",
                     "HISTORICO_RV2_FALLOS_Y_REPARACIONES.md", "CONTRATO_FILAS_ASIGNADAS.md"],
    "ingeniero": ["PROTOCOLO_UNICO.md", "CONTRATO_INGENIERO_VUC.md", "ORDENES.md",
                  "CONTRATO_LEGISLACION_2026-08-24.md", "MATRIZ_LEGISLACION.md",
                  "CONTRATO_LEGISLACION_TOTAL.md"],
}
INDICE = os.path.join(AQUI, "memoria", "INDICE_METODO.json")


def indexar():
    """Indexa los documentos que definen la forma de trabajo, en todos los proyectos."""
    from cerebro import grafo
    prs = grafo.proyectos()
    fichas = []
    for apodo, docs in DOCS_METODO.items():
        raiz = prs.get(apodo, {}).get("ruta", AQUI if apodo == "ingeniero" else "")
        if not raiz or not os.path.isdir(raiz):
            continue
        for doc in docs:
            ruta = os.path.join(raiz, doc)
            if not os.path.exists(ruta):
                continue
            try:
                txt = open(ruta, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            secciones = []
            for i, ln in enumerate(txt.splitlines(), 1):
                if ln.startswith("#") or ln.startswith("**LEY") or ln.startswith("## LEY"):
                    secciones.append({"linea": i, "titulo": ln.lstrip("# *").strip()[:110]})
            fichas.append({"proyecto": apodo, "doc": doc, "ruta": ruta,
                           "lineas": len(txt.splitlines()), "secciones": secciones[:60]})
    os.makedirs(os.path.dirname(INDICE), exist_ok=True)
    json.dump(fichas, open(INDICE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return fichas


def buscar_en_el_metodo(consulta, k=5):
    """¿Que dice el metodo sobre esto? Devuelve doc + linea, para poder citarlo."""
    try:
        fichas = json.load(open(INDICE, encoding="utf-8"))
    except Exception:
        fichas = indexar()
    from cerebro.trozos import _palabras
    q = set(_palabras(consulta))
    out = []
    for f in fichas:
        for s in f["secciones"]:
            comunes = q & set(_palabras(s["titulo"]))
            if comunes:
                out.append({"donde": "%s:%d" % (f["doc"], s["linea"]),
                            "proyecto": f["proyecto"], "titulo": s["titulo"],
                            "puntos": len(comunes), "ruta": f["ruta"]})
    return sorted(out, key=lambda x: -x["puntos"])[:k]
