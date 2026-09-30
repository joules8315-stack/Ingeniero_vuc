# -*- coding: utf-8 -*-
"""arnes/asignador.py — EL COMPARADOR MANDA. La IA solo entra si sale ROJO, y no siempre.

DE DONDE SALE (Julio, 2026-09-08): "la revision se puede programar, dado que estamos esperando
un resultado especifico. Mejor crear un COMPARADOR: si no se logra, dice que no se logro, y
ahi si entra una IA a ver por que. Para eso debe tener la informacion pertinente de la pieza,
DEPURADA, no informacion irrelevante que haga bulto."

Y: "el que asigna ya debe tener la informacion pertinente completa: saber si la IA tiene
capacidad, si no esta dormida, diciendole claramente este es el resultado que queremos, se hizo
esto y no sirvio por esto, reparalo."

Y, apretando: "no solo que quepa, sino que venga LO NECESARIO, y no con peso innecesario".

LA CONTRADICCION QUE CAZO JULIO ANTES DE QUE ESTO SE CONSTRUYERA, y es la clave de todo:
"si nace roja, lo va a mandar para una IA, y no es asi; debe ser en la segunda vuelta".
El metodo de esta casa dice que LA VIGIA NACE ROJA A PROPOSITO. Si el criterio fuera
"rojo = llamar a una IA", cada prueba nueva dispararia una IA a reparar algo que todavia no
existe. Se estaria pagando por el paso 1 del propio metodo.

TODO LO QUE HAY AQUI SON CUENTAS. Este archivo NO llama a ningun cerebro: solo decide si hace
falta llamar, a quien, y con que. La IA la llama quien reciba esta decision.

LEY: CONTRATO_SIN_OBJETIVO_NO_SE_PIDE_NADA.md (reglas 5 y 6) y
     CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# Lo que aguanta el encargo entero. Los cerebros gratis medidos aguantan 19.042 y 20.169
# letras: con mas, se les salta a TODOS en silencio y acaba escribiendo y revisando el mismo
# cerebro de pago. Medido el 2026-09-08: eso costo dos o tres rondas por cada cambio.
# CORREGIDO EL 2026-09-09, PROBANDOLO DE VERDAD: 19.000 NO BASTABA. Al encargo se le pega
# DESPUES el texto fijo que se le manda al auditor, que pesa 3.350 letras. Con el tope en
# 19.000 lo que le llegaba de verdad eran 19.209 y se pasaba por 167 letras del cerebro que
# aguanta 19.042: se le saltaba igual. Un tope que no cuenta lo que se anade despues no es un
# tope. Se deja sitio para eso y un margen, y se comprueba MIDIENDO lo que llega, no lo que
# se manda.
TOPE_LETRAS = 15000

# Cuantas veces se le insiste al mismo cerebro antes de parar y avisar a Julio.
INTENTOS = 3


def leer_el_fallo(salida):
    """Saca de la salida de las pruebas QUE fallo y QUE tenia que pasar.

    EL OBJETIVO NO SE INVENTA: sale del propio mensaje de la vigia, que en esta casa se escribe
    diciendo que tenia que pasar ("NO SALE EL EMBUDO. Con 1000 de alcance y 100 clics ya se
    puede decir que de cada diez que lo vieron, uno entro"). Ese texto ES el objetivo.

    Devuelve {archivo, prueba, objetivo} o None si no se puede leer nada.
    """
    try:
        texto = str(salida or "")
        archivo = prueba = ""
        for linea in texto.splitlines():
            linea = linea.strip()
            if linea.startswith(("FAILED", "ERROR")):
                sin_marca = linea.split(None, 1)[1] if " " in linea else linea
                trozos = sin_marca.split("::")
                archivo = trozos[0].strip().replace("\\", "/")
                if len(trozos) > 1:
                    prueba = trozos[1].split()[0].strip()
                break
        if not archivo:
            return None
        # El objetivo: lo que dice el mensaje de la prueba al fallar.
        objetivo = ""
        for linea in texto.splitlines():
            tira = linea.strip()
            if tira.startswith("E ") or "AssertionError" in tira or "Failed:" in tira:
                objetivo = re.sub(r"^E\s+", "", tira)
                objetivo = re.sub(r"^\w*(AssertionError|Failed):\s*", "", objetivo).strip()
                if objetivo:
                    break
        return {"archivo": archivo, "prueba": prueba, "objetivo": objetivo or texto[:300]}
    except Exception:
        return None


def hay_que_llamar_a_alguien(salida, vigias_nuevas=None):
    """Hace falta una IA, o esta roja es el metodo funcionando?

    LA REGLA QUE CAZO JULIO: una vigia RECIEN NACIDA nace roja A PROPOSITO, porque se escribe
    ANTES que la pieza. Llamar a una IA ahi es pagar por el paso 1 del propio metodo, y encima
    la IA no encontraria nada que reparar: la pieza todavia no existe.

    Se llama SOLO si la vigia roja ya estaba guardada antes (o sea, estaba verde y se rompio).
    La lista de vigias nuevas la sabe el guardado: arnes/guardia_de_guardado.py ya se la
    pregunta a git.
    """
    try:
        fallo = leer_el_fallo(salida)
        if not fallo:
            return False
        nuevas = [str(v).replace("\\", "/") for v in (vigias_nuevas or [])]
        return fallo["archivo"] not in nuevas
    except Exception:
        return False


def elegir_cerebro(letras, evitar=None):
    """A QUIEN se le puede pedir, comprobandolo ANTES de gastar. Devuelve (quien, motivo).

    Se mira, en este orden y todo son cuentas:
      1. quien tiene llave       (cuerpo/obrero.py::quienes_hay)
      2. quien NO esta dormido   (cuerpo/cuotas.py::desperto)
      3. a quien le CABE         (cuerpo/cuotas.py::rankear, con lo MEDIDO, no lo declarado)
    Si no queda nadie, devuelve (None, motivo) y NO se gasta. Callarse y mandarlo igual es lo
    que hacia el sistema viejo: se les saltaba a todos en silencio y lo pagaba el de pago.
    """
    try:
        from cuerpo import cuotas, obrero
        con_llave = [q for q in obrero.quienes_hay() if q != evitar]
        if not con_llave:
            return None, "no hay ningun cerebro con llave puesta"
        despiertos = [q for q in con_llave if cuotas.desperto(q)]
        if not despiertos:
            return None, "todos los cerebros estan dormidos ahora mismo: se espera, no se gasta"
        caben = cuotas.rankear(despiertos, letras)
        if not caben:
            return None, ("el encargo pesa %d letras y no le cabe a ninguno de los que estan "
                          "despiertos: se recorta el encargo, no se gasta la vuelta" % letras)
        return caben[0], "tiene llave, esta despierto y le caben %d letras" % letras
    except Exception as e:
        return None, "no se pudo comprobar quien puede: %s" % str(e)[:90]


def pedido_bien_hecho(pedido):
    """¿El pedido esta bien hecho? Devuelve (True/False, lo que falta). Es una CUENTA, cero IA.

    NACE PARA ROMPER UN BUCLE (Julio, 2026-09-09): "por que se le pide que juzgue algo que ya
    esta. Eso es estupido. Debe pasar a EJECUTAR. Lo que debe hacer, a lo sumo, es con un
    PROGRAMA verificar que el pedido este bien hecho y lleve lo que se le pidio".

    EL BUCLE QUE ROMPE, ocurrido tres veces seguidas ese dia: se mandaba el trabajo ya hecho y
    verde a que un cerebro lo juzgara; el cerebro, ahogado en relleno, contestaba "errores de
    sintaxis graves"; se comprobaba y era FALSO (compilaba y sus vigias pasaban); se volvia a
    mandar; y otra vez. Cada vuelta costaba dinero y no aportaba nada.

    Esto NO opina sobre si el trabajo es bueno: de eso ya se encarga la vigia, que es quien lo
    corre de verdad. Aqui solo se mira que el pedido sirva para trabajar.
    """
    p = pedido or {}
    falta = []
    objetivo = str(p.get("objetivo") or "").strip()
    material = str(p.get("material") or "").strip()
    if len(objetivo) < 10:
        falta.append("no dice QUE se queria conseguir: sin eso no hay con que comparar")
    if not material:
        falta.append("no lleva dentro lo que se pidio: el cerebro contestaria NO_ENCONTRADO "
                     "y la vuelta ya estaria pagada")
    if len(objetivo) + len(material) > TOPE_LETRAS:
        falta.append("no le cabe a ningun cerebro gratis (%d letras, el tope son %d): se les "
                     "salta a todos en silencio y acaba pagandolo el de pago"
                     % (len(objetivo) + len(material), TOPE_LETRAS))
    return (not falta), falta


def armar_encargo(fallo, material, intento=1):
    """El encargo con LAS TRES COSAS. Depurado, pero SIN perder lo necesario.

    Ley: a nadie se le pide un trabajo sin decirle QUE tiene que conseguir, QUE hay ahora y
    QUE se espera de el.

    Y lo que aprieta Julio: recortar por lo bruto es trampa. Si al recortar se cae justo el
    trozo que hay que reparar, el encargo cabe y NO SIRVE PARA NADA. Por eso el recorte se hace
    por el FINAL del material, que es donde vive el relleno, conservando el trozo de la pieza.
    """
    f = fallo or {}
    # EL OBJETIVO TAMBIEN SE RECORTA (Julio, 2026-09-09). Fallo real medido ese dia: el tope
    # solo se aplicaba al material, y el objetivo entraba ENTERO. Cuando se pide juzgar trabajo
    # ya hecho, el objetivo lleva dentro el codigo a juzgar: 7.447 letras coladas por la puerta
    # de atras. Un tope que deja una puerta abierta no es un tope.
    # Se conserva el PRINCIPIO del objetivo, que es donde se dice que tenia que pasar.
    _obj = str(f.get("objetivo") or "(no se pudo leer el mensaje de la prueba)")
    _sitio_obj = int(TOPE_LETRAS * 0.6)
    if len(_obj) > _sitio_obj:
        _obj = _obj[:_sitio_obj] + "\n  ... [se recorto para que le quepa a un cerebro gratis]"
    cabecera = "\n".join([
        "OBJETIVO: esto es lo que tenia que pasar y no paso.",
        "  " + _obj,
        "",
        "LO QUE HAY: la prueba %s del archivo %s se pone ROJA."
        % (f.get("prueba") or "?", f.get("archivo") or "?"),
        "  Intento numero %d de %d." % (intento, INTENTOS),
        "",
        "TU PAPEL: repararlo. No expliques, repara: di el archivo, el texto de antes y el de",
        "  despues. Si te falta algo del material, escribe NO_ENCONTRADO y pidelo; no inventes.",
        "",
        "EL TROZO DE LA PIEZA:",
    ])
    sitio = TOPE_LETRAS - len(cabecera) - 200
    trozo = str(material or "")
    # POR PARTES, no por un solo lado (2026-09-10): cortar solo el final dejaba FUERA la pieza
    # (medido 2026-09-09: 9 funciones -> 0), porque en el paquete real el codigo viaja en el
    # MEDIO. Se conserva lo que el problema NOMBRA (la ley de Julio: se conserva siempre lo
    # que el problema nombra y la ley que aplica), el principio (donde vive la ley) y el
    # final; se tira el relleno del medio.
    nombres = _nombres(_obj + " " + str(f.get("archivo") or ""))
    if len(trozo) > sitio:
        trozo = _recortar_material(trozo, sitio, nombres, identificadores(_obj + " " + str(f.get("archivo") or "")))
    return cabecera + "\n" + trozo


def _nombres(texto):
    """Los nombres de archivo que el texto menciona: lo que NO se puede recortar.

    La ley de Julio (2026-09-09): "se conserva siempre lo que el problema nombra". Un archivo
    nombrado en la tarea o en la cabecera viaja como seccion '### `archivo`' en el material;
    esta funcion saca el nombre para poder dejar ESA seccion entera.
    """
    nombres = set()
    for m in re.finditer(r"[\w/]+\.(?:py|js|ts|css|sql|html|md|json)", str(texto or "")):
        ruta = m.group(0).lower()
        nombres.add(ruta)
        nombres.add(ruta.split("/")[-1])
        nombres.add(ruta.split("/")[-1].split(".")[0])
        nombres.add(ruta.split("/")[0])
    return nombres


def identificadores(texto):
    """Devuelve un CONJUNTO (set) con los nombres de funcion o de cosa que el texto nombra,
    todos en minusculas. Nunca revienta: si le llega algo vacio, None, o que no es texto,
    devuelve un conjunto vacio."""
    if not isinstance(texto, str) or not texto:
        return set()
    EXTENSIONES = (".py", ".js", ".ts", ".css", ".sql", ".html", ".md", ".json")
    PALABRAS_COMUNES = {
        "arreglar", "pantalla", "celular", "porque", "guarda", "nada", "mas",
        "para", "como", "cuando", "donde", "esta", "este", "esto", "esos",
        "esas", "unos", "unas", "pero", "solo", "todo", "toda", "todos",
        "todas", "hace", "hacer", "tiene", "tener", "puede", "poder", "debe",
        "deber", "sobre", "entre", "desde", "hasta", "segun", "cada", "otro",
        "otra", "otros", "otras", "mismo", "misma", "tambien", "ademas",
        "entonces", "luego", "despues", "antes", "ahora", "aqui", "alli",
        "alla", "muy", "poco", "mucho", "bien", "mal", "siempre", "nunca",
        "jamas", "quiza", "quizas", "tal", "vez", "veces", "cosa", "cosas",
        "parte", "partes", "lugar", "forma", "modo", "manera", "caso", "casos",
        "tipo", "tipos", "clase", "clases", "grupo", "grupos", "lista", "listas",
        "dato", "datos", "valor", "valores", "nombre", "nombres", "texto",
        "textos", "palabra", "palabras", "frase", "frases", "linea", "lineas",
        "renglon", "renglones", "archivo", "archivos", "funcion", "funciones",
        "codigo", "codigos", "programa", "programas", "sistema", "sistemas",
        "usuario", "usuarios", "cliente", "clientes", "empresa", "empresas",
        "negocio", "negocios", "amigo", "amiga", "amigos", "amigas", "dueno",
        "duena", "duenos", "duenas", "jefe", "jefa", "jefes", "jefas",
        "trabajo", "trabajos", "tarea", "tareas", "encargo", "encargos",
        "pedido", "pedidos", "peticion", "peticiones", "solicitud", "solicitudes",
        "respuesta", "respuestas", "pregunta", "preguntas", "aviso", "avisos",
        "error", "errores", "fallo", "fallos", "problema", "problemas",
        "solucion", "soluciones", "arreglo", "arreglos", "reparacion",
        "reparaciones", "cambio", "cambios", "mejora", "mejoras", "nuevo",
        "nueva", "nuevos", "nuevas", "viejo", "vieja", "viejos", "viejas",
        "bueno", "buena", "buenos", "buenas", "malo", "mala", "malos",
        "malas", "grande", "grandes", "pequeno", "pequena", "pequenos",
        "pequenas", "primero", "primera", "primeros", "primeras", "ultimo",
        "ultima", "ultimos", "ultimas", "siguiente", "siguientes", "anterior",
        "anteriores", "unico", "unica", "unicos", "unicas", "varios", "varias",
        "alguno", "alguna", "algunos", "algunas", "ninguno", "ninguna",
        "ningunos", "ningunas", "cualquiera", "cualesquiera", "quien", "quienes",
        "cual", "cuales", "cuanto", "cuanta", "cuantos", "cuantas",
    }
    encontrados = set()
    limpio = re.sub(r"[\w/]+\.(?:py|js|ts|css|sql|html|md|json)", " ", texto)
    for palabra in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", limpio):
        if len(palabra) < 3:
            continue
        if palabra.lower() in PALABRAS_COMUNES:
            continue
        if palabra.lower().endswith(EXTENSIONES):
            continue
        tiene_mayuscula_en_medio = any(c.isupper() for c in palabra[1:])
        tiene_raya_baja_en_medio = "_" in palabra[1:-1]
        if tiene_mayuscula_en_medio or tiene_raya_baja_en_medio:
            encontrados.add(palabra.lower())
    for m in re.finditer(r"(?:funcion|funci\u00f3n|def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", texto):
        palabra = m.group(1)
        if len(palabra) < 3:
            continue
        if palabra.lower().endswith(EXTENSIONES):
            continue
        encontrados.add(palabra.lower())
    return encontrados


def trozo_que_contiene(texto, aguja, presupuesto):
    """Devuelve un pedazo del texto, de como maximo presupuesto letras, que CONTIENE la aguja,
    dejando contexto por delante y por detras A PARTES IGUALES. Nunca revienta."""
    if not isinstance(texto, str):
        return ""
    if not isinstance(presupuesto, int) or presupuesto <= 0:
        return ""
    if len(texto) <= presupuesto:
        return texto
    if not isinstance(aguja, str) or not aguja:
        return texto[:presupuesto]
    pos = texto.find(aguja)
    if pos < 0:
        return texto[:presupuesto]
    largo_aguja = len(aguja)
    if largo_aguja >= presupuesto:
        return texto[pos:pos + presupuesto]
    sobra = presupuesto - largo_aguja
    antes = sobra // 2
    despues = sobra - antes
    inicio = pos - antes
    fin = pos + largo_aguja + despues
    if inicio < 0:
        fin += -inicio
        inicio = 0
    if fin > len(texto):
        inicio -= fin - len(texto)
        fin = len(texto)
        if inicio < 0:
            inicio = 0
    return texto[inicio:fin]


def _seccionar(material):
    """[(nombre, desde_material, hasta_seccion)] para cada '### `archivo`' del material."""
    marcas = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r"^### `([^`]+)`",
                                                                    material or "", re.M)]
    out = []
    for i, (a, _b, nombre) in enumerate(marcas):
        fin_bloque = marcas[i + 1][0] if i + 1 < len(marcas) else len(material)
        out.append((nombre, a, fin_bloque))
    return out


def _recortar_material(material, presupuesto, nombres, agujas=None):
    """Recorta `material` a `presupuesto` letras POR PARTES, no por un solo lado.

    Conserva, en orden: (1) las secciones '### `archivo`' que el problema NOMBRA (entera, si
    cabe), (2) el principio del material (donde vive la ley que aplica), y (3) el final. El
    codigo del paquete real viaja en el MEDIO; cortar un solo lado lo dejaba fuera (medido:
    9 funciones -> 0). El aviso se cuenta aparte del presupuesto.
    """
    if not material or len(material) <= presupuesto:
        return material
    presupuesto = max(0, presupuesto - 180)            # sitio para los separadores
    if presupuesto <= 0:
        return material[:60].rstrip() + " ... [recortado]"
    secciones = _seccionar(material)
    bloques = []                                       # (prioridad, desde, hasta)
    for nombre, a, b in secciones:
        clave = nombre.split("/")[-1].lower().split(".")[0]
        bloques.append(((0 if clave in nombres else 1), a, b))
    bloques.append((0, 0, min(len(material), presupuesto // 4)))          # la ley, al principio
    bloques.append((1, max(0, len(material) - presupuesto // 4), len(material)))  # el final
    bloques.sort(key=lambda t: (t[0], t[1]))
    elegidos, usado, ultimo = [], 0, 0
    for prio, a, b in bloques:
        a = max(a, ultimo)
        if b <= a:
            continue
        tam = b - a
        if usado + tam <= presupuesto:
            elegidos.append((a, b))
            usado += tam
            ultimo = b
        elif prio == 0 and presupuesto - usado > 100:
            queda = presupuesto - usado
            texto_sec = material[a:b]
            aguja_real = None
            if agujas:
                bajo = texto_sec.lower()
                mejor = None
                for ag in agujas:
                    pos = bajo.find(str(ag).lower())
                    if pos != -1 and (mejor is None or pos < mejor):
                        mejor = pos
                        aguja_real = texto_sec[pos:pos + len(str(ag))]
            if aguja_real is not None:
                pedazo = trozo_que_contiene(texto_sec, aguja_real, queda)
                pos = texto_sec.find(pedazo)
                if pos != -1:
                    elegidos.append((a + pos, a + pos + len(pedazo)))
                    ultimo = a + pos + len(pedazo)
                    usado += len(pedazo)
                else:
                    elegidos.append((a, a + queda))
                    ultimo = a + queda
                    usado = presupuesto
            else:
                elegidos.append((a, a + queda))
                ultimo = a + queda
                usado = presupuesto
    piezas = [material[a:b] for a, b in sorted(elegidos)]
    piezas = [p for p in piezas if p and p.strip()]
    if not piezas:
        return material[:max(60, presupuesto)].rstrip() + " ... [recortado]"
    sep = ("\n\n... [RECORTADO POR PARTES: se tiro solo el relleno del medio; lo nombrado "
           "quedo dentro] ...\n\n")
    return sep.join(p.rstrip() for p in piezas)


def recortar_prompt(prompt, tope):
    """EL FILTRO DEL PASILLO (2026-09-10): un solo recorte para las 9 puertas.

    Se llama DENTRO de _preguntar_con_relevo, una sola vez, antes de elegir cerebro. Si el
    prompt pasa del tope se corta SOLO el bloque del material (lo que va entre '===== MATERIAL'
    y '===== FIN...') con _recortar_material: por partes y conservando lo que la tarea nombra.
    La cabecera del prompt (reglas, tarea, esquema JSON, propuesta a auditar) nunca se toca.
    Si no se encuentra el bloque del material, NO se toca el prompt: romper la instruccion
    para ahorrar letras seria peor que el ahorro.
    """
    if not prompt or len(prompt) <= tope:
        return prompt
    inicio = prompt.find("===== MATERIAL")
    if inicio < 0:
        return prompt
    i_fin = prompt.find("===== FIN", inicio)
    fin = i_fin if i_fin >= 0 else len(prompt)
    cabeza, material, cola = prompt[:inicio], prompt[inicio:fin], prompt[fin:]
    presupuesto = tope - len(cabeza) - len(cola)
    if presupuesto <= 0 or len(material) <= presupuesto:
        return prompt
    nombres = _nombres(cabeza)
    agujas = identificadores(cabeza)
    for _ in range(4):
        material_corto = _recortar_material(material, presupuesto, nombres, agujas)
        nuevo = cabeza + material_corto + cola
        if len(nuevo) <= tope:
            return nuevo
        presupuesto = max(200, presupuesto * 2 // 3)
    return nuevo


def decidir(salida, material="", vigias_nuevas=None, intento=1):
    """La decision entera, de una vez. Devuelve un diccionario que dice que hacer.

    NO llama a ningun cerebro: solo dice si hace falta, a quien, y con que encargo.
    """
    fallo = leer_el_fallo(salida)
    if not fallo:
        return {"llamar": False, "motivo": "no se pudo leer que fallo"}
    if not hay_que_llamar_a_alguien(salida, vigias_nuevas):
        return {"llamar": False, "fallo": fallo,
                "motivo": "esa vigia es NUEVA: nace roja a proposito. No se llama a nadie."}
    if intento > INTENTOS:
        return {"llamar": False, "fallo": fallo,
                "motivo": "van %d intentos y sigue rojo: se para y se le dice a Julio, en vez "
                          "de insistir quemando dinero" % INTENTOS}
    encargo = armar_encargo(fallo, material, intento)
    quien, motivo = elegir_cerebro(len(encargo))
    return {"llamar": bool(quien), "quien": quien, "motivo": motivo,
            "encargo": encargo, "fallo": fallo, "intento": intento}


def informe(d):
    """En palabras simples, para que se vea sin saber de esto."""
    if not d.get("llamar"):
        return "NO SE LLAMA A NADIE: " + str(d.get("motivo") or "")
    return "\n".join([
        "SE LE PIDE A: %s" % d.get("quien"),
        "  por que    : %s" % d.get("motivo"),
        "  intento    : %d de %d" % (d.get("intento", 1), INTENTOS),
        "  el encargo pesa %d letras" % len(d.get("encargo") or ""),
    ])


if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], encoding="utf-8", errors="ignore") as f:
            print(informe(decidir(f.read())))
    else:
        print(__doc__)
    sys.exit(0)
