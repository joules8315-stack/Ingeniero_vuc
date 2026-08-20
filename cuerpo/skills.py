# -*- coding: utf-8 -*-
"""cuerpo/skills.py — BUSCADOR Y CREADOR DE HABILIDADES (orden 4 de Julio, 2026-08-20).

  "que haya tambien un buscador, creador de skills, cuando falte alguna, la busque en las
   respectivas librerias, y en caso de no existencia que cree las propias."

Antes de crear NADA se busca, en este orden (Ley 6: no repetidera):
  1. En las habilidades propias del Ingeniero      (`skills/`)
  2. En el codigo de los proyectos de Julio        (por el grafo: quiza ya lo escribio)
  3. En las librerias de Python instaladas         (pip: quiza ya existe hecha por otros)
  4. En las librerias conocidas que NO estan puestas (se dice como instalarla)
Solo si no aparece en ninguno de los cuatro, se CREA — y la crea el cerebro GRATIS, no Claude.
"""
import os, sys, re, importlib.util

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
SKILLS = os.path.join(AQUI, "skills")

# Librerias conocidas por asunto: si la necesidad casa, se dice cual instalar en vez de inventarla.
CONOCIDAS = {
    "docx": ("python-docx", "docx", "leer y escribir archivos Word (.docx)"),
    "word": ("python-docx", "docx", "leer y escribir archivos Word (.docx)"),
    "pdf": ("pypdf", "pypdf", "leer y partir PDF"),
    "excel": ("openpyxl", "openpyxl", "leer y escribir Excel"),
    "imagen": ("Pillow", "PIL", "abrir, recortar y convertir imagenes"),
    "foto": ("Pillow", "PIL", "abrir, recortar y convertir imagenes"),
    "internet": ("requests", "requests", "pedir paginas y APIs por internet"),
    "html": ("beautifulsoup4", "bs4", "leer y extraer datos de paginas HTML"),
    "correo": ("imaplib", "imaplib", "leer buzon de correo (viene con Python)"),
    "grafica": ("matplotlib", "matplotlib", "hacer graficas"),
    "audio": ("pydub", "pydub", "cortar y convertir audio"),
    "video": ("moviepy", "moviepy", "editar video"),
    "supabase": ("supabase", "supabase", "hablar con Supabase"),
    "qr": ("qrcode", "qrcode", "generar codigos QR"),
}


def _propias():
    if not os.path.isdir(SKILLS):
        return []
    out = []
    for f in sorted(os.listdir(SKILLS)):
        if f.endswith(".py") and not f.startswith("_"):
            ruta = os.path.join(SKILLS, f)
            txt = open(ruta, encoding="utf-8", errors="ignore").read(1500)
            m = re.search(r'"""(.+?)"""', txt, re.S)
            out.append({"nombre": f[:-3], "ruta": ruta,
                        "que_hace": " ".join(m.group(1).split())[:150] if m else ""})
    return out


def _instalada(modulo):
    try:
        return importlib.util.find_spec(modulo) is not None
    except Exception:
        return False


def _en_los_proyectos(necesidad, k=4, minimo=4.0):
    """Julio ya escribio algo que hace esto? Se busca con el mismo cerebro del router.

    OJO (fallo real 2026-08-20): sin exigir la palabra clave, buscar "telegram" devolvia
    trozos cualesquiera y el informe decia "ya lo escribiste" sobre algo que Julio nunca hizo.
    Decirle que ya existe algo que no existe es tan grave como inventarlo. Por eso:
      - el trozo tiene que CONTENER alguna palabra distintiva de la necesidad, y
      - tiene que pasar un puntaje minimo.
    """
    try:
        from cerebro import grafo, trozos
    except Exception:
        return []
    COMUNES = {"mandar", "crear", "hacer", "leer", "poner", "sacar", "generar", "usar", "para",
               "mensaje", "mensajes", "archivo", "archivos", "datos", "codigo", "canal", "canales",
               "una", "uno", "con", "por", "del", "las", "los", "que", "sus", "sistema"}
    # len >= 3 porque el indexador de trozos solo guarda palabras de 3 letras en adelante.
    # Fallo real (2026-08-20): "un" salia con cuenta 0 y por tanto parecia la palabra MAS RARA,
    # ganandole a "telegram". Se exigia "un", que esta en todas partes, y el informe mentia.
    claves = [w for w in re.split(r"[^\wáéíóúñ]+", necesidad.lower())
              if len(w) >= 3 and w not in COMUNES]
    if not claves:
        # No quedo NINGUNA palabra que distinga (caso real: "generar un codigo QR" -> "qr" tiene
        # 2 letras y el indexador no la guarda). Sin algo que distinguir, cualquier trozo "se
        # parece" y el informe acabaria diciendo "ya lo escribiste" sobre algo que no existe.
        # Ley de Julio: si no se puede saber, se dice que no se sabe. No se afirma.
        return []
    hallados = []
    for apodo in grafo.proyectos():
        try:
            g = grafo.cargar(apodo)
        except SystemExit:
            continue
        except Exception:
            continue
        codigo = [p for p in g["piezas"] if p["rol"] in ("CUERPO", "CODIGO")]
        if not codigo:
            continue
        try:
            b = trozos.Buscador(codigo)
        except Exception:
            continue
        # De las claves, quedarse con las 2 mas RARAS en este proyecto. "telegram" es rara;
        # "canal" la usa Julio a diario para redes. Exigir la rara es lo que separa
        # "ya lo escribiste" de "se parece de lejos".
        # SOLO la mas rara, no "cualquiera de las dos": con `any` bastaba que apareciera la
        # palabra comun ("canal") y el informe mentia diciendo que Julio ya lo habia escrito.
        raras = sorted(claves, key=lambda w: b.en_cuantos.get(w, 0))[:1] if claves else []
        # Si la palabra que de verdad distingue la necesidad NO aparece ni una vez en este
        # proyecto, entonces Julio NO lo escribio aqui. Se dice que no, en vez de traer parecidos.
        if raras and b.en_cuantos.get(raras[0], 0) == 0:
            continue
        for r in b.buscar(necesidad, k=2, exigir=raras or None):
            if r["puntaje"] >= minimo:
                hallados.append({"proyecto": apodo, "donde": r["direccion"], "puntaje": r["puntaje"]})
    return sorted(hallados, key=lambda x: -x["puntaje"])[:k]


def buscar(necesidad):
    """Devuelve el informe de busqueda. NO crea nada: solo dice que hay."""
    q = necesidad.lower()
    r = {"necesidad": necesidad, "propias": [], "en_proyectos": [], "librerias": [], "faltan": []}

    palabras = [w for w in re.split(r"[^\wáéíóúñ]+", q) if len(w) > 3]
    for s in _propias():
        texto = (s["nombre"] + " " + s["que_hace"]).lower()
        if any(w in texto for w in palabras):
            r["propias"].append(s)

    r["en_proyectos"] = _en_los_proyectos(necesidad)

    vistas = set()
    for clave, (lib, modulo, para) in CONOCIDAS.items():
        if clave in q and lib not in vistas:
            vistas.add(lib)
            puesta = _instalada(modulo)
            r["librerias"].append({"libreria": lib, "para": para, "instalada": puesta})
            if not puesta:
                r["faltan"].append("pip install " + lib)
    return r


def informe(r):
    L = ["BUSQUEDA DE HABILIDAD: " + r["necesidad"]]
    if r["propias"]:
        L.append("  YA LA TIENES (habilidad propia):")
        for s in r["propias"]:
            L.append("    - " + s["nombre"] + ": " + s["que_hace"][:90])
    if r["en_proyectos"]:
        L.append("  YA LO ESCRIBISTE en tus proyectos (mira antes de crear otra cosa):")
        for s in r["en_proyectos"]:
            L.append("    - " + s["proyecto"] + " :: " + s["donde"])
    if r["librerias"]:
        L.append("  EXISTE HECHA POR OTROS (libreria):")
        for s in r["librerias"]:
            estado = "YA INSTALADA" if s["instalada"] else "FALTA INSTALAR"
            L.append("    - " + s["libreria"] + " (" + s["para"] + ") — " + estado)
    if r["faltan"]:
        L.append("  Para instalarla:")
        for c in r["faltan"]:
            L.append("    " + c)
    if not (r["propias"] or r["en_proyectos"] or r["librerias"]):
        L.append("  NO_ENCONTRADO en ningun lado -> toca CREARLA:")
        L.append('    python ingeniero.py crear-skill "<nombre>" "' + r["necesidad"] + '"')
    return "\n".join(L)


def crear(nombre, que_hace, forzar=False):
    """Crea la habilidad con el cerebro GRATIS. Antes comprueba que no exista (Ley 6)."""
    from cuerpo import obrero
    nombre = re.sub(r"[^a-z0-9_]", "_", nombre.lower()).strip("_")
    destino = os.path.join(SKILLS, nombre + ".py")
    if os.path.exists(destino) and not forzar:
        return {"_error": "YA EXISTE: " + destino + ". Usa --forzar solo si de verdad quieres pisarla."}

    hallado = buscar(que_hace)
    if (hallado["propias"] or hallado["librerias"]) and not forzar:
        return {"_error": "NO SE CREA: ya hay algo que sirve (Ley 6, no repetidera).",
                "informe": informe(hallado)}

    tarea = (
        "Escribe una habilidad de Python llamada `" + nombre + "` que haga esto: " + que_hace + "\n\n"
        "REGLAS:\n"
        "- Un solo archivo, sin dependencias raras. Si necesita una libreria, que sea de las normales\n"
        "  (os, json, re, urllib) o una muy conocida, y que lo diga en el docstring.\n"
        "- Docstring arriba en espanol, simple, diciendo QUE hace y COMO se usa.\n"
        "- Funciones publicas claras y cortas. Si algo no se puede saber, devuelve \"NO_ENCONTRADO\".\n"
        "- Nada de inventar rutas ni llaves. Las llaves se leen del entorno, nunca se escriben.\n"
        "- Incluye al final, en un comentario, la prueba (vigia) que la comprobaria.\n\n"
        "Responde SOLO el codigo Python, sin explicaciones y sin comillas de bloque.")

    ok, quien = obrero.disponible()
    if not ok:
        return {"_error": quien}
    texto, quien_gen, avisos = obrero._preguntar_con_relevo(tarea, 0.2)
    if not texto:
        return {"_error": "; ".join(avisos)}
    codigo = re.sub(r"^```(?:python)?\s*|\s*```$", "", texto.strip(), flags=re.M).strip()
    os.makedirs(SKILLS, exist_ok=True)
    cabecera = ("# -*- coding: utf-8 -*-\n"
                "# HABILIDAD CREADA por el Ingeniero VUC con " + quien_gen + ".\n"
                "# Necesidad: " + que_hace + "\n"
                "# NO probada por Julio todavia: vigia verde NO es prueba (Ley 5).\n\n")
    open(destino, "w", encoding="utf-8").write(cabecera + codigo + "\n")
    return {"creada": destino, "por": quien_gen, "avisos": avisos,
            "aviso": "FALTA: escribir su vigia y que Julio la pruebe. No esta certificada."}
