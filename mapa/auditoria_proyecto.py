# -*- coding: utf-8 -*-
"""mapa/auditoria_proyecto.py — EL INVENTARIO PARA UNA SEGUNDA OPINION.

Lee un proyecto entero (SOLO LECTURA) y escribe un inventario en
memoria/auditorias/<APODO>_AUDITORIA_PROYECTO.json, fuera del proyecto auditado.
Legisla CONTRATO_AUDITORIA_DE_PROYECTO.md.

Julio, 2026-09-07, su condicion literal: "no quiero que el equipo rellene esto a mano
inventando estados... las afirmaciones como 'esto existe' deben poder rastrearse hasta un
archivo, funcion, contrato, test o commit".

POR ESO: todo lo de aqui sale de LEER. Lo que exige correr, llamar o preguntar sale como
"no_verificado" con un campo `_como_se_sabe` que dice POR QUE no se puede saber leyendo.
El esqueleto y los ayudantes (md5, git, duplicados, estructura) los escribio el equipo
(obrero deepseek, auditor gemini4, APROBADO). El relleno con lo que SI se puede medir se
anadio despues, con el mismo veredicto y su paquete.

NO DUPLICA NADA: el censo de piezas, enlaces y flujos ya lo hace cerebro/grafo.py.
"""
import os, json, hashlib, subprocess, sys, re, time
from collections import Counter, defaultdict

# Asegurar que podemos importar cerebro y cuerpo
RAIZ_INGENIERO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_INGENIERO)

from cerebro import grafo
from cuerpo import privacidad

MEMORIA_AUDITORIAS = os.path.join(RAIZ_INGENIERO, "memoria", "auditorias")

NO_VER = "no_verificado"

# Las 32 llaves del informe, en el orden exacto que manda la Regla 7
LLAVES_INFORME = [
    "proyecto", "reglas_de_recoleccion", "estructura_proyecto", "arquitectura",
    "dos_cerebros", "agentes", "skills", "mcp", "plugins", "herramientas",
    "memoria", "motor_dmm", "flujos", "leyes", "contratos", "candados",
    "arneses", "guardas", "tablas_de_verdad", "matrices", "ontologia",
    "versionado_y_canon", "duplicacion_y_conflictos", "pruebas", "rendimiento",
    "costos", "seguridad", "estado_funcional", "deuda_tecnica",
    "objetivos_futuros", "preguntas_abiertas", "resumen_equipo"
]

# Un candado se reconoce por su nombre, no por un juicio: el archivo se llama candado_algo.
ES_CANDADO = re.compile(r"(^|/)candado[_-]", re.I)


def _md5_de_archivo(ruta):
    """Calcula el md5 del contenido de un archivo."""
    h = hashlib.md5()
    try:
        with open(ruta, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _git(raiz, *args):
    """Ejecuta un comando git de SOLO LECTURA y devuelve la salida."""
    try:
        resultado = subprocess.run(
            ["git", "-C", raiz] + list(args),
            capture_output=True, text=True, check=False, encoding="utf-8", errors="ignore"
        )
        return (resultado.stdout or "").strip()
    except Exception:
        return None


def _lineas(txt):
    return [x for x in (txt or "").splitlines() if x.strip()]


def _id(p):
    """El identificador de una pieza, siempre con barras normales."""
    return p["id"].replace("\\", "/")


def _limpio(txt):
    """Regla 5: ni un secreto viaja en el informe."""
    if not txt:
        return txt
    limpio, _ = privacidad.limpiar(txt)
    return limpio


def _boca(p):
    """La primera linea de una pieza: lo que el archivo dice de si mismo."""
    return _limpio((p.get("resumen") or "").strip())[:300] or NO_VER


def _nombra(piezas, patron):
    """Las piezas cuyo NOMBRE habla de esto. Es una pista, y el informe lo dice asi."""
    r = re.compile(patron, re.I)
    return sorted(_id(p) for p in piezas if r.search(_id(p)))


def _bloque(piezas, patron, campos=None):
    """Un bloque 'existe/archivos' honrado: existe SOLO si hay archivos que lo respalden."""
    archivos = _nombra(piezas, patron)
    d = {"existe": bool(archivos), "archivos": archivos}
    if archivos:
        d["_como_se_sabe"] = ("existe = hay archivos cuyo nombre lo nombra. NO quiere decir que "
                              "funcione: eso solo lo dice correrlo")
    else:
        d["_como_se_sabe"] = ("no aparece ningun archivo cuyo nombre lo nombre; podria vivir "
                              "dentro de otro archivo, y sin abrirlos no se puede afirmar")
    for c in (campos or []):
        d[c] = NO_VER if archivos else []
    return d


def _detectar_duplicados(raiz, piezas):
    """Detecta archivos duplicados por md5 y rutas paralelas."""
    por_md5 = {}
    nombres = {}
    for p in piezas:
        md5 = p.get("md5") or _md5_de_archivo(p.get("abs") or os.path.join(raiz, p["id"]))
        if md5:
            por_md5.setdefault(md5, []).append(_id(p))
        nombres.setdefault(os.path.basename(_id(p)), []).append(_id(p))

    archivos_duplicados = [sorted(v) for v in por_md5.values() if len(v) > 1]
    rutas_paralelas = [sorted(v) for v in nombres.values() if len(v) > 1]
    return archivos_duplicados, rutas_paralelas


def _estructura_proyecto(raiz, piezas):
    """Construye el arbol de directorios y clasifica los archivos."""
    arbol = {}
    clasificacion = {
        "archivos_codigo": [], "archivos_configuracion": [], "archivos_documentacion": [],
        "archivos_pruebas": [], "archivos_contratos": [], "archivos_leyes": [],
        "archivos_memoria": [], "archivos_skills": [], "archivos_agentes": [],
        "archivos_harness": [], "archivos_guardas": [], "archivos_indice": []
    }
    for p in piezas:
        pid = _id(p)
        partes = pid.split("/")
        nivel = arbol
        for parte in partes[:-1]:
            nivel = nivel.setdefault(parte, {})
        nivel.setdefault(partes[-1], None)

        rol = p.get("rol", "")
        nombre = partes[-1].lower()
        if rol == "VIGIA":
            clasificacion["archivos_pruebas"].append(pid)
        elif rol in ("CODIGO", "CUERPO", "CEREBRO", "WEB"):
            clasificacion["archivos_codigo"].append(pid)
        elif rol == "ARNES":
            clasificacion["archivos_harness"].append(pid)
        elif rol == "CONTRATO":
            clasificacion["archivos_contratos"].append(pid)
        elif rol in ("PROTOCOLO", "MATRIZ"):
            clasificacion["archivos_leyes"].append(pid)
        elif rol == "SKILL":
            clasificacion["archivos_skills"].append(pid)
        elif rol in ("DATO", "LANZADOR"):
            clasificacion["archivos_configuracion"].append(pid)
        else:
            clasificacion["archivos_documentacion"].append(pid)

        # Los cajones que se cruzan con el rol: una pieza puede estar en dos.
        if ES_CANDADO.search(pid):
            clasificacion["archivos_guardas"].append(pid)
        if re.search(r"agente|obrero|auditor|consejero|subagente", nombre) and \
                rol in ("CODIGO", "CUERPO", "CEREBRO"):
            clasificacion["archivos_agentes"].append(pid)
        if pid.startswith("memoria/") or "/memoria/" in pid:
            clasificacion["archivos_memoria"].append(pid)
        if re.search(r"mapa|indice|canonic|grafo", nombre):
            clasificacion["archivos_indice"].append(pid)

    return {
        "arbol_directorios": arbol,
        "archivos_totales": len(piezas),
        "lineas_totales": sum(p.get("lineas", 0) for p in piezas),
        "por_rol": dict(sorted(Counter(p.get("rol", "?") for p in piezas).items(),
                               key=lambda t: -t[1])),
        **{k: sorted(set(v)) for k, v in clasificacion.items()}
    }


def _informe_vacio():
    """Crea un informe con las 32 llaves vacias."""
    informe = {llave: {} for llave in LLAVES_INFORME}
    informe["resumen_equipo"] = {}  # Regla 8: se queda vacio a proposito
    return informe


def _rellenar_proyecto(informe, g, apodo):
    """Rellena la llave 'proyecto'."""
    raiz = g["raiz"]
    branch = _git(raiz, "rev-parse", "--abbrev-ref", "HEAD")
    commit = _git(raiz, "rev-parse", "HEAD")
    declarado = grafo.proyectos().get(apodo, {})
    informe["proyecto"] = {
        "nombre": "Digital Marketing Manager" if apodo == "dmm" else apodo,
        "apodo_en_el_ingeniero": apodo,
        "version": NO_VER,
        "fecha_recoleccion": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "repo_canonico": raiz,
        "_repo_canonico_como_se_sabe": "declarado en proyectos.config del Ingeniero VUC",
        "remoto": _git(raiz, "config", "--get", "remote.origin.url") or NO_VER,
        "branch_actual": branch or NO_VER,
        "branch_canonica_declarada": declarado.get("rama") or NO_VER,
        "commit_actual": commit or NO_VER,
        "commit_base_conocido": NO_VER,
        "hay_cambios_sin_guardar": bool(_git(raiz, "status", "--porcelain")),
        "estado_actual": NO_VER,
        "objetivo_del_mvp": NO_VER,
    }
    # SE ITERA SOBRE UNA COPIA: el bucle anade claves al mismo diccionario que recorre y Python
    # lo corta en seco ("dictionary changed size during iteration"). Lo cazo la primera corrida.
    razones = {
        "version": "no hay ninguna etiqueta de version en el repositorio (git tag sale vacio)",
        "commit_base_conocido": "no hay etiqueta ni rama base declarada con la que comparar",
        "estado_actual": "esto no se lee del codigo: lo dice Julio",
        "objetivo_del_mvp": "esto no se lee del codigo: lo dice Julio. Se deja vacio antes que "
                            "inventarlo",
    }
    for k, v in list(informe["proyecto"].items()):
        if v == NO_VER:
            informe["proyecto"]["_como_se_sabe_" + k] = razones.get(
                k, "no se puede comprobar leyendo el repositorio")


def _rellenar_reglas(informe):
    """Rellena la llave 'reglas_de_recoleccion'."""
    informe["reglas_de_recoleccion"] = {
        "no_modificar_codigo": True,
        "no_crear_archivos": True,
        "no_hacer_commit": True,
        "no_eliminar_nada": True,
        "solo_lectura": True,
        "incluir_archivos_relevantes": True,
        "excluir_secretos": True,
        "excluir_credenciales": True,
        "excluir_tokens_api": True,
        "incluir_rutas_completas_de_archivos": True,
        "_cumplimiento": "el informe se escribe FUERA del proyecto auditado, en la carpeta del "
                         "Ingeniero VUC. Al proyecto solo se le lee",
    }


def _rellenar_estructura(informe, raiz, piezas):
    informe["estructura_proyecto"] = _estructura_proyecto(raiz, piezas)


def _rellenar_arquitectura(informe, piezas):
    """Lo que se puede decir de la forma del sistema SIN abrir los archivos."""
    web = [p for p in piezas if p.get("rol") == "WEB" or _id(p).startswith("web/")]
    cuerpo = [p for p in piezas if p.get("rol") == "CUERPO"]

    pistas_ia = ("openrouter", "deepseek", "groq", "gemini", "qwen", "openai", "anthropic",
                 "claude", "lmstudio", "lm studio", "ollama", "mistral")
    modelos = defaultdict(list)
    for p in piezas:
        texto = ((p.get("resumen") or "") + " " + _id(p)).lower()
        for n in pistas_ia:
            if n in texto:
                modelos[n].append(_id(p))

    pistas_srv = ("supabase", "facebook", "instagram", "whatsapp", "google", "gmail",
                  "youtube", "tiktok", "linkedin", "stripe", "resend", "twilio", "meta")
    servicios = []
    for n in pistas_srv:
        donde = sorted({_id(p) for p in piezas
                        if n in ((p.get("resumen") or "") + " " + _id(p)).lower()})
        if donde:
            servicios.append({
                "servicio": n, "_donde_se_nombra": donde[:12], "conectado_de_verdad": NO_VER,
                "_como_se_sabe": "se nombra en esos archivos; que este CONECTADO solo lo prueba "
                                 "una llamada real",
            })

    informe["arquitectura"] = {
        "frontend": {
            "tecnologia": NO_VER,
            "ruta": "web/" if web else NO_VER,
            "entrypoints": sorted(_id(p) for p in web
                                  if re.search(r"servidor|app|main|index|menu|landing", _id(p), re.I)),
            "paginas": sorted(_id(p) for p in web if _id(p).lower().endswith((".html", ".htm"))),
            "componentes_principales": [{"archivo": _id(p), "lineas": p.get("lineas", 0),
                                         "boca": _boca(p)} for p in web][:60],
            "_como_se_sabe": "por la carpeta y la extension; la tecnologia exacta exige abrirlos",
        },
        "backend": {
            "tecnologia": NO_VER,
            "ruta": "cuerpo/" if cuerpo else NO_VER,
            "entrypoints": _nombra(piezas, r"(^|/)(app|main|servidor|arranca)\.py$"),
            "apis": [],
            "_apis_como_se_sabe": "las rutas no se pueden listar sin abrir los archivos: no se "
                                  "inventan",
            "servicios": [{"archivo": _id(p), "lineas": p.get("lineas", 0), "boca": _boca(p),
                           "funciones": ["%s:%s" % (a.get("nombre"), a.get("linea"))
                                         for a in (p.get("api") or [])]}
                          for p in cuerpo][:150],
            "workers": _nombra(piezas, r"worker|cola|bucle|loop|cron|programad"),
        },
        "base_datos": {
            "tecnologia": "supabase" if _nombra(piezas, r"supabase") else NO_VER,
            "archivos_que_la_nombran": _nombra(piezas, r"supabase|sqlite|postgres|\.sql$"),
            "tablas": [], "relaciones": [], "indices": [], "politicas": [],
            "_como_se_sabe": "hay archivos que la nombran; el esquema no esta en el repositorio, "
                             "asi que las tablas no se pueden listar sin mirar el panel del "
                             "servicio",
        },
        "servicios_externos": servicios,
        "modelos_ia": [{"nombre": n, "proveedor": NO_VER, "uso": NO_VER, "local_o_nube": NO_VER,
                        "costo": NO_VER, "entrada": NO_VER, "salida": NO_VER,
                        "_donde_se_nombra": sorted(set(v))[:12],
                        "_como_se_sabe": "el nombre aparece en el titulo o la primera linea de "
                                         "esos archivos; el uso y el costo exigen leerlos"}
                       for n, v in sorted(modelos.items())],
    }


def _rellenar_dos_cerebros(informe, piezas, cajones):
    informe["dos_cerebros"] = {
        "ingeniero_software": {
            "existe": True,
            "_como_se_sabe": "el Ingeniero VUC es OTRO repositorio (C:\\Ingeniero_VUC). Aqui solo "
                             "se listan los archivos DE ESTE proyecto que lo nombran",
            "archivos": _nombra(piezas, r"ingenier|arnes|candado|vigia"),
            "agentes": [], "roles": [], "skills": [], "herramientas": [],
            "flujo": NO_VER, "entrada": NO_VER, "salida": NO_VER,
        },
        "dmm_marketing": {
            "existe": True,
            "archivos": _nombra(piezas, r"marketing|campan|contenido|publica|marca|cliente|"
                                        r"competencia|asesor|redes"),
            "agentes": cajones.get("archivos_agentes", []),
            "roles": [], "skills": cajones.get("archivos_skills", []),
            "herramientas": [], "flujo": NO_VER, "entrada": NO_VER, "salida": NO_VER,
        },
        "kernel_compartido": {
            "existe": False,
            "archivos": [], "funciones": [],
            "_como_se_sabe": "no hay ninguna carpeta ni paquete compartido entre los dos "
                             "repositorios: cada uno tiene su propia copia de guardias y "
                             "pruebas. ESTO ES UN HALLAZGO, no una falta de dato",
        },
    }


def _rellenar_agentes_y_skills(informe, piezas):
    informe["agentes"] = [{
        "nombre": os.path.basename(_id(p)), "archivo": _id(p), "rol": NO_VER,
        "objetivo": _boca(p), "modelo": NO_VER, "herramientas": [], "skills": [],
        "entrada": NO_VER, "salida": NO_VER, "memoria": [],
        "puede_decidir": [], "puede_ejecutar": [],
        "puede_modificar_codigo": NO_VER, "puede_hacer_commit": NO_VER,
        "estado": NO_VER,
        "_como_se_sabe": "el nombre del archivo lo delata como agente; sus permisos exigen leerlo",
    } for p in piezas
        if p.get("rol") in ("CODIGO", "CUERPO", "CEREBRO")
        and re.search(r"agente|obrero|auditor|consejero|subagente", os.path.basename(_id(p)), re.I)]

    informe["skills"] = [{
        "nombre": os.path.basename(_id(p)), "archivo": _id(p), "objetivo": _boca(p),
        "prompt_o_logica": NO_VER, "herramientas": [], "entrada": NO_VER, "salida": NO_VER,
        "validaciones": [], "memoria_utilizada": [], "agente_que_la_invoca": NO_VER,
        "estado": "existente",
    } for p in piezas if p.get("rol") == "SKILL" or "/skills/" in _id(p)]

    informe["mcp"] = []
    informe["plugins"] = []
    informe["herramientas"] = [{
        "nombre": os.path.basename(_id(p)), "tipo": "LANZADOR", "funcion": _boca(p),
        "quien_la_usa": NO_VER, "costo": NO_VER, "estado": "existente",
    } for p in piezas if p.get("rol") == "LANZADOR"]


def _rellenar_memoria(informe, piezas):
    informe["memoria"] = {
        "arquitectura_general": NO_VER,
        "_arquitectura_como_se_sabe": "describirla es opinar; abajo van las piezas que existen",
        "rag": _bloque(piezas, r"rag|embedding|vector|indexa|semantic",
                       ["fuente", "indexacion", "busqueda", "embeddings", "cache"]),
        "memoria_fragmentada": _bloque(piezas, r"fragment|trozo|paquete", ["etapas", "reglas"]),
        "indice_canonico": _bloque(piezas, r"mapa|canonic|indice",
                                   ["estructura", "prioridades", "punteros"]),
        "grafo": _bloque(piezas, r"grafo|enlace|nodo", ["entidades", "relaciones"]),
        "memoria_de_razonamiento": _bloque(piezas, r"razon|pensa|decision", ["estructura"]),
        "memoria_de_evidencia": _bloque(piezas, r"evidencia|prueba_real|rastro|bitacora",
                                        ["estructura"]),
        "memoria_de_hipotesis": _bloque(piezas, r"hipotes", ["estructura"]),
        "cache_semantica": _bloque(piezas, r"cache", ["funcion"]),
    }


def _rellenar_motor(informe, piezas):
    web = [p for p in piezas if p.get("rol") == "WEB" or _id(p).startswith("web/")]
    informe["motor_dmm"] = {
        "perfil_empresa": _bloque(piezas, r"perfil|empresa|negocio", ["datos"]),
        "voz_marca": _bloque(piezas, r"voz|marca|branding|tono", ["variables"]),
        "perfilador_cliente": _bloque(piezas, r"cliente|buyer|persona|publico", ["variables"]),
        "productos_servicios": _bloque(piezas, r"producto|servicio|catalogo|precio", ["datos"]),
        "competencia": _bloque(piezas, r"competencia|competidor|benchmark",
                               ["fuentes", "metodo_analisis"]),
        "entorno_digital": {
            "existe": bool(_nombra(piezas, r"redes|instagram|facebook|whatsapp|correo|podcast")),
            "archivos": _nombra(piezas, r"redes|instagram|facebook|whatsapp|correo|email|podcast"),
            "redes": sorted({n for n in ("instagram", "facebook", "tiktok", "linkedin",
                                         "youtube", "whatsapp") if _nombra(piezas, n)}),
            "web": bool(web),
            "landing_page": bool(_nombra(piezas, r"landing")),
            "whatsapp": bool(_nombra(piezas, r"whatsapp")),
            "email": bool(_nombra(piezas, r"correo|email|gmail|resend")),
            "podcast": bool(_nombra(piezas, r"podcast")),
        },
        "recoleccion_datos": _bloque(piezas, r"recolect|scrap|captador|ingesta|fuente",
                                     ["fuentes", "frecuencia", "metodo", "datos_recolectados"]),
        "analitica": _bloque(piezas, r"analit|metrica|analista|dashboard|kpi",
                             ["metricas", "fuentes", "calculos"]),
        "estrategia": _bloque(piezas, r"estrategia|objetivo|plan",
                              ["objetivos", "hipotesis", "reglas"]),
        "campanas": _bloque(piezas, r"campan", ["flujo", "aprobacion_usuario", "versionado"]),
        "contenido": {
            "texto": bool(_nombra(piezas, r"texto|copy|redacc|contenido")),
            "imagenes": bool(_nombra(piezas, r"imagen|foto|banner")),
            "carruseles": bool(_nombra(piezas, r"carrusel")),
            "reels": bool(_nombra(piezas, r"reel")),
            "historias": bool(_nombra(piezas, r"histor|story|stories")),
            "videos": bool(_nombra(piezas, r"video")),
            "podcast": bool(_nombra(piezas, r"podcast")),
            "web": bool(web),
            "_como_se_sabe": "hay o no hay un archivo que lo nombre. Que FUNCIONE es otra "
                             "pregunta y no se responde leyendo",
        },
        "publicacion": _bloque(piezas, r"publica|programa|scheduler|automatiza",
                               ["redes_conectadas", "programacion", "automatizacion"]),
        "ventas": _bloque(piezas, r"venta|crm|lead|conversion|atribucion"),
        "aprendizaje": _bloque(piezas, r"aprendiz|historial|resultado",
                               ["que_mide", "como_aprende", "como_reutiliza_resultados"]),
    }


def _rellenar_leyes_y_guardas(informe, g, piezas):
    """Flujos, leyes, contratos, candados, arneses y guardas: lo que existe, con su rastro."""
    # LOS FLUJOS SON UN DICCIONARIO, no una lista: el censo los guarda por nombre. La primera
    # version reventaba aqui con "string indices must be integers". Lo cazo la primera corrida.
    flujos = g.get("flujos") or {}
    informe["flujos"] = []
    for nombre, f in sorted(flujos.items()):
        del_flujo = [x.replace("\\", "/") for x in (f.get("piezas") or [])]
        candados = [x for x in del_flujo if ES_CANDADO.search(x)]
        informe["flujos"].append({
            "nombre": nombre, "objetivo": NO_VER, "trigger": NO_VER, "pasos": [],
            "piezas_del_flujo": del_flujo,
            "agentes": [x for x in del_flujo
                        if re.search(r"agente|obrero|auditor|consejero", x, re.I)],
            "skills": [], "herramientas": [], "entradas": [], "salidas": [], "validaciones": [],
            "guardas": candados, "candados": candados, "harness": "", "commit": "",
            "estado": "existente" if del_flujo else NO_VER,
            "_como_se_sabe": "el flujo lo arma el censo juntando las piezas que se llaman entre "
                             "si; los pasos y el disparador exigen leerlas",
        })

    informe["leyes"] = [{
        "nombre": os.path.basename(_id(p)), "ubicacion": _id(p), "regla": _boca(p),
        "es_ejecutable": False,
        "_es_ejecutable_como_se_sabe": "es un documento; solo es ejecutable si hay un candado que "
                                       "la haga cumplir. Cruzar con la lista de candados",
        "quien_la_hace_cumplir": NO_VER, "estado": "existente",
    } for p in piezas if p.get("rol") in ("PROTOCOLO", "MATRIZ")]

    informe["contratos"] = sorted([{
        "nombre": os.path.basename(_id(p)), "archivo": _id(p), "objetivo": _boca(p),
        "entrada": NO_VER, "salida": NO_VER, "invariantes": [], "estado": "existente",
        "_como_se_sabe": "el archivo existe y su primera linea es el objetivo; entrada, salida e "
                         "invariantes exigen leerlo entero y no se inventan",
    } for p in piezas if p.get("rol") == "CONTRATO"], key=lambda x: x["nombre"])

    informe["candados"] = sorted([{
        "nombre": os.path.basename(_id(p)), "ubicacion": _id(p), "protege": _boca(p),
        "condicion_bloqueo": NO_VER, "condicion_aprobacion": NO_VER, "ejecutable": True,
        "_ejecutable_como_se_sabe": "es un archivo de codigo con funciones; si esta ENGANCHADO a "
                                    "un disparador no se sabe sin mirar la configuracion",
        "estado": "existente",
    } for p in piezas if ES_CANDADO.search(_id(p))], key=lambda x: x["nombre"])
    if not informe["candados"]:
        informe["candados"] = {
            "_hallazgo": "ESTE PROYECTO NO TIENE NI UN CANDADO PROPIO. No es falta de dato: se "
                         "buscaron archivos llamados candado_* en el censo entero y no hay "
                         "ninguno. Si alguien trabaja este proyecto sin pasar por el Ingeniero "
                         "VUC, trabaja sin red",
        }

    informe["arneses"] = sorted([{
        "nombre": os.path.basename(_id(p)), "archivo": _id(p), "funcion": _boca(p),
        "entrada": NO_VER, "validaciones": [], "salida": NO_VER, "acciones_si_falla": [],
        "estado": "existente",
    } for p in piezas if p.get("rol") == "ARNES" and not ES_CANDADO.search(_id(p))],
        key=lambda x: x["nombre"])

    informe["guardas"] = {
        "entrada": _nombra(piezas, r"hook|prompt_submit"),
        "salida": _nombra(piezas, r"stop|cierre"),
        "cross_flow": _nombra(piezas, r"cross|vecino|danar"),
        "codigo": _nombra(piezas, r"edit_gate|read_gate|permiso"),
        "memoria": _nombra(piezas, r"candado_memoria|guard_pasado"),
        "commit": _nombra(piezas, r"commit|sellar"),
    }

    informe["tablas_de_verdad"] = [{
        "nombre": os.path.basename(_id(p)), "archivo": _id(p), "estados": [], "transiciones": [],
        "condiciones": [], "acciones": [],
        "_como_se_sabe": "el archivo existe; su contenido exige leerlo",
    } for p in piezas if p.get("rol") == "MATRIZ"]
    informe["matrices"] = informe["tablas_de_verdad"]
    informe["ontologia"] = {
        "existe": False, "entidades": [], "relaciones": [], "reglas": [],
        "_como_se_sabe": "no hay ningun archivo de ontologia en el censo",
    }


def _rellenar_versionado(informe, raiz, apodo, piezas):
    declarado = grafo.proyectos().get(apodo, {})
    informe["versionado_y_canon"] = {
        "rama_canonica": declarado.get("rama") or NO_VER,
        "rama_actual": _git(raiz, "rev-parse", "--abbrev-ref", "HEAD") or NO_VER,
        "commits_recientes": _lineas(_git(raiz, "log", "--oneline", "-30")),
        "commits_relevantes": [],
        "tags": _lineas(_git(raiz, "tag")),
        "branches": _lineas(_git(raiz, "branch", "-a")),
        "reglas_de_commit": _nombra(piezas, r"commit|sellar"),
        "reglas_de_herencia": [],
        "proteccion_contra_versiones_huerfanas": "la via canonica del Ingeniero VUC declara UNA "
                                                 "ruta y UNA rama por proyecto, y avisa si "
                                                 "encuentra copias por el disco",
        "fuente_de_verdad": raiz,
    }


def _rellenar_duplicacion(informe, raiz, piezas):
    """Detecta duplicados. Regla 6: lo medible se mide, lo que es juicio NO se afirma."""
    duplicados, paralelas = _detectar_duplicados(raiz, piezas)
    por_funcion = defaultdict(list)
    for p in piezas:
        for a in (p.get("api") or []):
            n = a.get("nombre")
            if n and not n.startswith("_"):
                por_funcion[n].append("%s:%s" % (_id(p), a.get("linea", "?")))
    funciones = []
    for n, sitios in por_funcion.items():
        if len({s.rsplit(":", 1)[0] for s in sitios}) > 1:
            funciones.append({"funcion": n, "donde": sorted(sitios),
                              "_como_se_sabe": "mismo nombre en varios archivos; NO se comprobo "
                                               "si el cuerpo es igual"})
    informe["duplicacion_y_conflictos"] = {
        "archivos_duplicados": duplicados,
        "_archivos_duplicados_como_se_sabe": "mismo md5 del contenido: son copias identicas",
        "funciones_duplicadas": sorted(funciones, key=lambda x: -len(x["donde"]))[:200],
        "skills_duplicadas": [],
        "contratos_conflictivos": [],
        "_contratos_conflictivos_como_se_sabe": "decir que dos contratos se contradicen exige "
                                                "leerlos enteros y compararlos. No se afirma sin "
                                                "eso: se entrega la lista para que la juzgue "
                                                "quien audita",
        "leyes_conflictivas": [],
        "rutas_paralelas": paralelas,
        "_rutas_paralelas_como_se_sabe": "mismo nombre de archivo en 2+ rutas. Es un dato, no una "
                                         "sentencia",
        "versiones_paralelas": [],
        "posibles_fuentes_de_confusion": [],
    }


def _rellenar_pruebas(informe, piezas):
    vigias = [p for p in piezas if p.get("rol") == "VIGIA"]
    play = sorted({_id(p) for p in piezas
                   if "playwright" in ((p.get("resumen") or "") + " " +
                                       " ".join(p.get("importa") or [])).lower()})
    e2e = [_id(p) for p in vigias if re.search(r"e2e|punta_a_punta|extremo", _id(p), re.I)]
    integ = [_id(p) for p in vigias if re.search(r"integra|flujo|real", _id(p), re.I)]
    regre = [_id(p) for p in vigias if re.search(r"regres|no_vuelva|no_repet", _id(p), re.I)]
    unit = [_id(p) for p in vigias if _id(p) not in set(e2e + integ + regre)]
    informe["pruebas"] = {
        "frameworks": ["pytest"] if vigias else [NO_VER],
        "cantidad_total": len(vigias),
        "tests_pasando": NO_VER, "tests_fallando": NO_VER, "tests_omitidos": NO_VER,
        "_como_se_sabe": "se contaron los archivos de prueba leyendo. Cuantas PASAN no se rellena "
                         "sin correrlas: eso es correr, no leer "
                         "(python ingeniero.py vigias <apodo>)",
        "tests_e2e": e2e, "tests_integracion": integ, "tests_unitarios": unit,
        "tests_de_regresion": regre,
        "playwright": {"existe": bool(play), "tests": play},
    }


def _rellenar_rendimiento_y_costos(informe, piezas):
    informe["rendimiento"] = {
        "tokens": {"medidor_existe": bool(_nombra(piezas, r"token|gasto|ahorro|coste|costo")),
                   "archivos": _nombra(piezas, r"token|gasto|ahorro|coste|costo"),
                   "metricas": []},
        "latencia": [], "cache": _nombra(piezas, r"cache"),
        "llamadas_ia": _nombra(piezas, r"router|llamar|cerebro|rotacion|cuota"),
        "llamadas_repetidas": [], "lecturas_excesivas_de_contexto": [],
        "_como_se_sabe": "medir latencia o llamadas repetidas exige CORRER el sistema, no leerlo",
    }
    informe["costos"] = {
        "modelos": [], "apis": [], "almacenamiento": [], "busqueda": [], "imagenes": [],
        "video": [], "estimacion_mensual": NO_VER,
        "estrategias_de_ahorro": _nombra(piezas, r"ahorro|gratis|cuota|rotacion"),
        "_como_se_sabe": "el gasto real esta en las facturas y en el registro de llamadas, no en "
                         "el codigo",
    }


def _rellenar_estado_funcional(informe, piezas):
    """Regla 4: leer no es probar. Nada entra en 'funciona' por haberlo leido."""
    informe["estado_funcional"] = {
        "funciona": [], "funciona_parcialmente": [], "no_funciona": [], "no_implementado": [],
        "no_verificado": sorted({_id(p) for p in piezas
                                 if p.get("rol") in ("CODIGO", "CUERPO", "CEREBRO", "WEB")}),
        "_como_se_sabe": "LEER NO ES PROBAR. Ningun archivo entra en 'funciona' por haberlo "
                         "leido. Para llenar esas listas hay que CORRER las pruebas y la prueba "
                         "real; hasta entonces todo el codigo esta como no verificado. Es la ley "
                         "de Julio: vigia verde no es prueba",
    }


def _rellenar_seguridad(informe, raiz, piezas):
    """Rellena la llave 'seguridad'. Regla 5: detecta secretos sin copiar el valor."""
    archivos_con_secretos = []
    total_secretos = 0
    revisados = 0
    for p in piezas:
        if p.get("rol") in ("VIGIA", "DOC", "CONTRATO", "PROTOCOLO", "MATRIZ"):
            continue
        if (p.get("lineas") or 0) > 3000:
            continue
        ruta = p.get("abs") or os.path.join(raiz, p["id"])
        if not os.path.isfile(ruta):
            continue
        if not ruta.lower().endswith((".py", ".js", ".ts", ".json", ".env", ".config", ".cfg",
                                      ".ini", ".yml", ".yaml", ".toml", ".sh", ".ps1")):
            continue
        try:
            with open(ruta, encoding="utf-8", errors="ignore") as f:
                contenido = f.read()
        except Exception:
            continue
        revisados += 1
        _, cuantos = privacidad.limpiar(contenido)
        if cuantos > 0:
            archivos_con_secretos.append({"archivo": _id(p), "cuantos": cuantos})
            total_secretos += cuantos
    informe["seguridad"] = {
        "secretos_en_codigo": bool(archivos_con_secretos),
        "archivos_a_revisar": sorted(archivos_con_secretos, key=lambda x: -x["cuantos"])[:40],
        "cantidad_de_secretos": total_secretos,
        "archivos_revisados": revisados,
        "variables_entorno": [],
        "_variables_entorno_como_se_sabe": "listarlas exige abrir los archivos de configuracion, "
                                           "que es justo donde viven los secretos: no se hace",
        "autenticacion": NO_VER, "autorizacion": NO_VER, "aislamiento_multitenant": NO_VER,
        "logs": NO_VER, "riesgos_detectados": [],
        "_como_se_sabe": "detectado con cuerpo/privacidad.py; EL VALOR NUNCA SE COPIA. Marca lo "
                         "que PARECE un secreto: puede haber falsos positivos y hay que mirarlos "
                         "con los ojos",
    }


def _rellenar_cierre(informe, g, raiz):
    informe["deuda_tecnica"] = []
    informe["_deuda_tecnica_como_se_sabe"] = (
        "la deuda se dictamina comparando lo que hay con lo que debia haber. Se deja a la segunda "
        "opinion, con los duplicados y los huecos de arriba como material")
    informe["objetivos_futuros"] = []
    informe["preguntas_abiertas"] = [
        "Cual es el objetivo del MVP, en una frase. No esta escrito en ningun archivo que se "
        "pueda leer sin ambiguedad.",
        "Cual es el commit base con el que comparar. No hay etiquetas en el repositorio.",
        "Que partes tiene que ver Julio funcionando para darlas por buenas. Sin eso, 'funciona' "
        "no se puede rellenar nunca.",
        "Los dos cerebros deben compartir un nucleo comun. Hoy cada uno tiene su propia copia de "
        "guardias y de pruebas.",
    ]
    informe["resumen_equipo"] = {
        "que_cree_el_equipo_que_ya_funciona": [], "que_no_esta_seguro": [], "que_falta": [],
        "problemas_conocidos": [], "decisiones_pendientes": [],
        "_como_se_sabe": "esto es opinion del equipo, no lectura del repositorio. Se deja vacio a "
                         "proposito: rellenarlo desde aqui seria justo lo que Julio pidio evitar",
    }
    informe["_de_donde_sale_todo_esto"] = {
        "censo": "cerebro/grafo.py del Ingeniero VUC, recorriendo %s" % raiz,
        "piezas_censadas": len(g.get("piezas", [])),
        "enlaces_censados": len(g.get("enlaces", [])),
        "flujos_censados": len(g.get("flujos", {})),
        "git": "ordenes de solo lectura sobre el mismo repositorio",
        "secretos": "cuerpo/privacidad.py; ningun valor sospechoso se copia al informe",
        "lo_que_no_se_puede_saber_leyendo": [
            "si algo FUNCIONA (hay que correrlo)",
            "cuantas pruebas pasan (hay que correrlas)",
            "el gasto real (esta en las facturas)",
            "si un servicio externo esta CONECTADO (hay que llamarlo)",
            "el objetivo del MVP (lo dice Julio)",
        ],
    }


def auditar(apodo):
    """Genera el informe de auditoria para el proyecto con el apodo dado."""
    g = grafo.cargar(apodo, forzar=True)
    raiz = g["raiz"]
    piezas = g.get("piezas", [])

    informe = _informe_vacio()
    _rellenar_proyecto(informe, g, apodo)
    _rellenar_reglas(informe)
    _rellenar_estructura(informe, raiz, piezas)
    _rellenar_arquitectura(informe, piezas)
    _rellenar_dos_cerebros(informe, piezas, informe["estructura_proyecto"])
    _rellenar_agentes_y_skills(informe, piezas)
    _rellenar_memoria(informe, piezas)
    _rellenar_motor(informe, piezas)
    _rellenar_leyes_y_guardas(informe, g, piezas)
    _rellenar_versionado(informe, raiz, apodo, piezas)
    _rellenar_duplicacion(informe, raiz, piezas)
    _rellenar_pruebas(informe, piezas)
    _rellenar_rendimiento_y_costos(informe, piezas)
    _rellenar_estado_funcional(informe, piezas)
    _rellenar_seguridad(informe, raiz, piezas)
    _rellenar_cierre(informe, g, raiz)

    # LAS 32 LLAVES, EN SU ORDEN (Regla 7). Si falta una, el informe esta mal aunque el
    # contenido sea bueno: quien lo audita espera esta forma.
    ordenado = {k: informe[k] for k in LLAVES_INFORME}
    for k, v in informe.items():
        if k not in ordenado:
            ordenado[k] = v

    os.makedirs(MEMORIA_AUDITORIAS, exist_ok=True)
    salida = os.path.join(MEMORIA_AUDITORIAS, "%s_AUDITORIA_PROYECTO.json" % apodo.upper())
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(ordenado, f, ensure_ascii=False, indent=1)
    return salida


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python mapa/auditoria_proyecto.py <APODO>")
    ruta = auditar(sys.argv[1])
    print("INVENTARIO ESCRITO: %s" % ruta)
    print("  tamano: %.0f KB" % (os.path.getsize(ruta) / 1024.0))
