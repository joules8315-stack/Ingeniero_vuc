# -*- coding: utf-8 -*-

"""cuerpo/obrero.py — EL OBRERO. Quien hace el trabajo pesado: el cerebro GRATIS, no Claude.

Manda el CONTRATO_MAESTRO_AHORRO de DMM:
  · Claude (caro)  = dirige y revisa. Lee VEREDICTOS, nunca volumenes.
  · Qwen  (Groq)   = Frente 2 / Ingeniero: GENERA.
  · Gemini         = AUDITA lo que genero Qwen (los "4 ojos").

Aqui no se duplica el cerebro (Ley 6, no repetidera): se TOMA PRESTADO el de DMM
(`cuerpo/cerebro.py` + `cuerpo/config.py`), que ya esta probado y ya sabe leer el `.env`.
Si DMM no esta en la maquina, se dice NO_ENCONTRADO. No se inventa un cerebro de repuesto.
"""
import os, sys, json, re, threading, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cerebro import grafo      # noqa: E402
from cuerpo import cuotas      # noqa: E402
from cuerpo import cuaderno    # noqa: E402  (el cuaderno de llamadas: registra cada intento)
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import asignador               # noqa: E402  (el recortador del pasillo)

_prestado = {}


def _cargar_por_ruta(nombre, ruta):
    """Carga un modulo por su RUTA, con nombre propio. Hace falta porque el Ingeniero tiene su
    propio paquete `cuerpo` y DMM tambien: un `from cuerpo import cerebro` normal agarra el
    equivocado (fallo real 2026-08-20)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def prestar_cerebro():
    """Trae el cerebro de DMM sin copiarlo. Devuelve (cerebro, config) o (None, None)."""
    if _prestado:
        return _prestado.get("cerebro"), _prestado.get("config")
    prs = grafo.proyectos()
    raiz = prs.get("dmm", {}).get("ruta", "")
    cbo = os.path.join(raiz, "cuerpo")
    if not raiz or not os.path.isdir(cbo):
        return None, None
    try:
        cf = _cargar_por_ruta("dmm_config", os.path.join(cbo, "config.py"))
        c = _cargar_por_ruta("dmm_cerebro", os.path.join(cbo, "cerebro.py"))
        if not c or not cf:
            return None, None
        cf.asegurar_cargado()
        _prestado["cerebro"], _prestado["config"] = c, cf
        return c, cf
    except Exception as e:
        _prestado["_error"] = str(e)
        return None, None


def disponible():
    c, cf = prestar_cerebro()
    if not c:
        return False, "NO_ENCONTRADO: no se pudo tomar prestado el cerebro de DMM"
    if not cf.hay_cerebro():
        return False, "NO_ENCONTRADO: no hay llave ni modelo local (revisa el .env de DMM)"
    return True, c.proveedor()


# ─── los prompts: cortos, con el paquete dentro, y prohibicion de inventar ──────────
def _prompt_obrero(paquete, tarea, clase="reparar"):
    if clase != "reparar":
        # CREAR CODIGO O CREAR DOCUMENTO (2026-09-10). Medido: pedir crear vigias/_espia.py
        # salio RECHAZADO porque el encargo de --crear pedia SIEMPRE el documento entero escrito
        # en markdown: el gratis obedecio, entrego markdown con extension .py y el auditor lo
        # rechazo con razon (SyntaxError). El encargo pedia lo contrario de lo que mandaba la
        # tarea. Si la tarea pide un archivo de CODIGO (.py), el encargo pide CODIGO PYTHON.
        if re.search(r"[\w/]+\.py\b", str(tarea or "")):
            return f"""Eres el ANALISTA DE CODIGO de un ingeniero de software. Tu trabajo es PENSAR y ESCRIBIR
un archivo de CODIGO nuevo. NO vas a cambiar codigo que ya existe: ese archivo todavia no existe.

REGLAS DURAS (si las rompes, tu trabajo se descarta):
1. NO hay texto viejo que sustituir: el archivo todavia no existe. Lo escribes entero.
2. CREAR NO ES INVENTAR: el archivo nuevo lo pide la tarea y su ruta viene en la tarea. Que no
   exista en el material NO es motivo de rechazo: un archivo que aun no existe nunca puede venir
   en el material.
3. En "texto_nuevo" va CODIGO PYTHON de verdad, entero y ejecutable: sin markdown, sin cercas de
   codigo y sin nada de texto fuera del codigo. Lo que haya que explicar va dentro, como
   comentario o docstring.
4. El archivo tiene que IMPORTARSE y CORRER: funciones completas de verdad, con sus import, no
   huecos ni ejemplos. Nada de "aqui iria".
5. Los nombres son EXACTAMENTE los que pide la tarea: la ruta, las funciones y los atributos.
   No los cambies ni los mejores.
6. Trabaja SOLO con el material de abajo. Si te falta algo, pidelo asi y nada mas:
   NECESITO_LEER: archivo / motivo / que decide / riesgo.

TAREA: {tarea}

Responde SOLO un JSON valido, sin texto alrededor:
{{"diagnostico": "que has encontrado, en una frase",
  "archivo": "la ruta del archivo de codigo que creas",
  "texto_nuevo": "el archivo de CODIGO PYTHON ENTERO Y COMPLETO, ejecutable, sin markdown",
  "confianza": "alta|media|baja"}}

===== MATERIAL (esto es TODO lo que existe) =====
{paquete}
===== FIN DEL MATERIAL =====
"""
        return f"""Eres el ANALISTA de un ingeniero de software. Tu trabajo es PENSAR y ESCRIBIR un documento
nuevo. NO vas a cambiar codigo.

REGLAS DURAS (si las rompes, tu trabajo se descarta):
1. NO hay texto viejo que sustituir: el documento todavia no existe. Lo escribes entero.
2. NO inventes archivos, funciones ni datos. Si te falta informacion para analizar algo, escribe
   NO_ENCONTRADO en ese punto. Jamas lo rellenes a ojo.
3. NO decidas lo que el contrato no dice. Escribe PREGUNTA_REQUERIDA y la pregunta en palabras
   simples.
4. El documento se escribe para alguien que NO ES TECNICO: sin jerga, sin nombres de archivo
   salvo cuando sea imprescindible, y explicando cada cosa como se la contarias a un amigo dueno
   de un negocio.
5. Trabaja SOLO con el material de abajo. Si te falta algo, pidelo asi y nada mas:
   NECESITO_LEER: archivo / motivo / que decide / riesgo.

TAREA: {tarea}

Responde SOLO un JSON valido, sin texto alrededor:
{{"diagnostico": "que has encontrado, en una frase",
  "archivo": "el nombre del documento que creas",
  "texto_nuevo": "el documento ENTERO y completo, escrito en markdown",
  "confianza": "alta|media|baja"}}

===== MATERIAL (esto es TODO lo que existe) =====
{paquete}
===== FIN DEL MATERIAL ====="""
    return f"""Eres el OBRERO de un ingeniero de software. Trabajas SOLO con el material de abajo.

REGLAS DURAS (si las rompes, tu trabajo se descarta):
1. NO inventes archivos, funciones ni lineas. Si algo no esta en el material, escribe NO_ENCONTRADO. CREAR NO ES INVENTAR. Si el encargo pide expresamente crear un archivo nuevo y da su ruta y describe lo que debe hacer, ESO SE ESCRIBE ENTERO, y no es inventar: es el trabajo. Un archivo que todavia no existe nunca puede venir en el material. Inventar es usar un archivo, una funcion o un dato que nadie pidio y que no existe en ninguna parte. Nunca se rechaza un encargo de crear alegando que faltaria inventar.
2. NO decidas lo que el contrato no dice. Escribe PREGUNTA_REQUERIDA: <la pregunta en palabras simples>.
3. Cambia lo MINIMO. PROHIBIDO dar numeros de renglon o tramos: un tramo borra la funcion entera y
   los numeros se corren solos en cuanto alguien anade una linea. Senala el sitio por su NOMBRE
   (que archivo, que funcion) y copiando el TEXTO literal. IMPORTANTE: COPIAS el texto literal que
   hay AHORA (texto_viejo) y el que debe quedar (texto_nuevo), tal como aparecen en el material.
   Ese texto tiene que estar palabra por palabra en el material y ser UNICO en el archivo; si se
   repite, se alarga hasta que lo sea. Si no copias el texto exacto, tu trabajo se descarta.
   Trabaja con el material COMPLETO que te dan (la funcion entera), nunca con un pedazo suelto: si
   el material no trae la funcion completa que necesitas, pidela con NECESITO_LEER en vez de
   arreglar a ciegas.
4. Antes de terminar, di a quien puedes danar (mira la seccion "A QUIEN PUEDE DANAR").
5. Trabaja SOLO con la memoria del PAQUETE de abajo (la informacion indexada). Si te falta material
   para responder, pidelo asi y nada mas: NECESITO_LEER: archivo / motivo / que decide / riesgo.
   No rechaces el trabajo ni te inventes excusas: el material es el suficiente para lo que se te pide.

TAREA: {tarea if tarea not in paquete else "(el objetivo esta arriba, dentro del material, bajo el renglon que empieza por OBJETIVO)"}

Responde SOLO un JSON valido, sin texto alrededor:
{{"diagnostico": "que esta mal, en una frase",
  "archivo": "ruta exacta del material",
  "funcion": "el NOMBRE de la funcion o seccion donde esta el cambio (nunca un numero)",
  "texto_viejo": "el texto literal que hay AHORA y que se sustituye, copiado tal cual del material",
  "texto_nuevo": "el texto literal que debe quedar, copiado tal cual del material",
  "cambio": "que hay que cambiar, concreto",
  "codigo": "el codigo nuevo, solo el pedazo",
  "vigia": "que prueba lo comprobaria",
  "puede_danar": ["pieza1", "pieza2"],
  "preguntas": ["si falta decidir algo"],
  "confianza": "alta|media|baja"}}

===== MATERIAL (esto es TODO lo que existe) =====
{paquete}
===== FIN DEL MATERIAL ====="""


def _prompt_auditor(paquete, propuesta):
    return f"""Eres el AUDITOR. Otro modelo propuso una reparacion. Tu trabajo es buscarle el error,
no felicitarlo. Se duro y concreto.

Comprueba una por una:
1. INVENTO algo? (archivo/funcion/linea que no aparece en el material) -> es el fallo mas grave.
   PERO OJO CON QUE ES INVENTAR, porque confundirlo cuesta vueltas y dinero: inventar es usar un
   archivo, una funcion o un dato que NO EXISTE. Escribir codigo NUEVO que el encargo pide
   EXPRESAMENTE no es inventar: es hacer el trabajo. Una reparacion SIEMPRE trae codigo que antes
   no estaba; si eso fuera inventar, ninguna reparacion podria aprobarse jamas. Rechaza por
   inventar SOLO cuando se usa algo que no existe, NUNCA por escribir lo que se pidio. Crear un
   dato nuevo arriba del archivo, con su nombre, tampoco es inventar cuando el encargo lo pide
   expresamente. Al reves: poner el valor una sola vez arriba y que todos lo miren de ahi es la
   manera correcta de trabajar, porque evita que dos sitios se descuadren. Inventar es AFIRMAR
   que algo ya existia cuando no existia, o usar un archivo o una funcion que no esta en ninguna
   parte. Escribir lineas nuevas, aunque sean muchas y aunque antes no hubiera nada parecido en
   el archivo, NO es inventar cuando el encargo lo pide. Casi toda reparacion anade codigo que
   no estaba; esa es la unica manera de reparar. La frase "esto no estaba en el codigo original"
   NO es un motivo de rechazo por si sola, y usarla como motivo es un rechazo en falso.
   CREAR NO ES INVENTAR. Si el encargo pide expresamente crear un archivo nuevo y da su ruta, ese
   archivo NO cuenta como invento aunque su contenido no venga en el material, porque un archivo
   que todavia no existe nunca puede venir en el material. Inventar es usar un archivo o una
   funcion que nadie pidio y que no existe.
2. El cambio arregla de verdad lo que dice el diagnostico?
3. Rompe algun vecino de la seccion "A QUIEN PUEDE DANAR"?
4. Se salta alguna ley del contrato que viene en el material?
5. Cambia mas de lo necesario?
6. LA UBICACION SE JUZGA POR EL TEXTO, NUNCA POR EL NUMERO. Si el texto literal que el obrero dice
   tocar APARECE en el material, la ubicacion es CORRECTA aunque el numero no cuadre.
   El numero es solo ORIENTATIVO: se corre en cuanto alguien anade una linea, y ademas el obrero
   cuenta sobre el material que le llega y tu sobre otro recorte, asi que casi nunca coinciden.
   SOLO se rechaza por ubicacion si el texto NO aparece en el material o si no da texto ninguno.
   Un numero que no cuadre NO ES MOTIVO DE RECHAZO por si solo.
7. NO SE RECHAZA POR LA FORMA, SE JUZGA EL FONDO. Una coma, una palabra distinta, un
   mensaje redactado de otra manera o un nombre elegido con otro criterio NO son fallos si
   el cambio hace lo que se pidio. Rechazar por eso quema una vuelta entera y no arregla
   nada. Se rechaza cuando el cambio NO FUNCIONA, cuando rompe a un vecino, cuando usa
   algo que no existe, o cuando no hace lo que el encargo pedia.

Responde SOLO JSON:
{{"veredicto": "APROBADO|RECHAZADO|DUDOSO",
  "invento_algo": true/false,
  "que_invento": ["..."],
  "fallos": ["fallo concreto 1", "..."],
  "riesgo_vecinos": ["..."],
  "que_falta": ["..."],
  "resumen_para_el_jefe": "una frase para que el director decida sin leer todo"}}

===== PROPUESTA A AUDITAR =====
{propuesta}
===== MATERIAL ORIGINAL =====
{paquete}
===== FIN ====="""


def _json_de(texto):
    """Saca el JSON aunque venga con ```json alrededor. Si no hay, lo dice; no lo inventa."""
    if not texto:
        return {"_error": "el cerebro no contesto nada"}
    m = re.search(r"\{.*\}", texto, re.S)
    crudo = m.group(0) if m else None
    if crudo is None:
        # Puede venir CORTADO por el limite de salida: empieza pero no cierra. Antes se tiraba
        # entero, o sea que se perdia trabajo bueno ya hecho. Se intenta cerrar lo que llego.
        i = texto.find("{")
        if i < 0:
            return {"_error": "el cerebro no devolvio JSON", "_crudo": texto}
        crudo = texto[i:]
    for intento in _maneras_de_leerlo(crudo):
        try:
            return json.loads(intento)
        except Exception:
            continue
    return {"_error": "JSON roto o cortado", "_crudo": crudo}


def _maneras_de_leerlo(crudo):
    """El mismo texto, en varias formas, de la mas fiel a la mas apanada.
    Nunca se INVENTA contenido: solo se cierran llaves y se quitan comas sobrantes."""
    yield crudo
    yield re.sub(r",\s*([}\]])", r"\1", crudo)          # coma de mas antes de cerrar
    # cortado a medio camino: se recorta hasta el ultimo campo entero y se cierra
    corte = max(crudo.rfind('",'), crudo.rfind('"]'), crudo.rfind("},"))
    if corte > 0:
        tronco = crudo[:corte + 1]
        faltan = tronco.count("[") - tronco.count("]")
        yield tronco + "]" * max(0, faltan) + "}" * max(0, tronco.count("{") - tronco.count("}"))


def _trae_no_encontrado(propuesta, campos):
    """UN PROGRAMA, no una IA: la marca NO_ENCONTRADO no puede colarse como si fuera contenido.

    Julio, 2026-09-15: la marca se detecta como SUBTEXTO en cualquier campo, en las DOS ramas
    (crear y reparar). Si cualquiera de los campos que _propuesta_cumple ya revisa trae la
    marca, la propuesta NO cumple.
    """
    for campo in campos:
        if "NO_ENCONTRADO" in str(propuesta.get(campo) or ""):
            return True
    return False


def _propuesta_cumple(propuesta, clase):
    """UN PROGRAMA, no una IA: el pedido tiene que LLEVAR lo que se pidio.

    Ley (CONTRATO_EL_EQUIPO_ESCRIBE): "un PROGRAMA comprueba que el pedido este bien hecho",
    que lleve dentro lo que se pidio. Medido el 2026-09-10 (causa 2): el gratis devolvio un JSON
    "reparado" por _json_de que tenia diagnostico y archivo pero VACIO de texto_nuevo; el auditor
    lo vio DUDOSO y el trabajo murio SIN llamar al de pago. El de pago entra SIEMPRE que el
    gratis falle; aqui el fallo era del programa, no del cerebro. Devuelve (ok, falta): con la
    falta en terminos que el bucle convierte en motivo de nuevo intento.
    """
    if not isinstance(propuesta, dict):
        return False, f"no devolvio un JSON: {str(propuesta)[:80]}"
    if clase == "crear":
        # Crear una pieza entera: si no trae el contenido nuevo, no existe lo que se crea.
        if not str(propuesta.get("texto_nuevo") or "").strip():
            return False, "la propuesta NO trae texto_nuevo (el pedido llego incompleto)"
        if _trae_no_encontrado(propuesta, ("archivo", "codigo", "texto_viejo", "texto_nuevo")):
            return False, "la propuesta NO cumple porque trae la marca NO_ENCONTRADO"
    else:
        # Reparar: tiene que decir que toca y con que se reemplaza.
        if not str(propuesta.get("archivo") or "").strip():
            return False, "la propuesta NO dice que archivo toca"
        if "codigo" not in propuesta and "texto_viejo" not in propuesta and "texto_nuevo" not in propuesta:
            return False, "la propuesta NO trae el cambio (codigo/texto_viejo/texto_nuevo)"
        if _trae_no_encontrado(propuesta, ("archivo", "codigo", "texto_viejo", "texto_nuevo")):
            return False, "la propuesta NO cumple porque trae la marca NO_ENCONTRADO"
    return True, ""


TOPE_GRATIS = 19000   # MEDIDO 2026-09-09: el mas pequeno de los cerebros gratis aguanta ~19.000.
TOPE_REVISOR = 12000   # A-38 (Julio 2026-09-19): el revisor recibe solo el cambio y lo que toca, nunca el archivo entero.
                      # A partir de aqui el cerebro se apaga: corta la respuesta a la mitad.


def _filtrar_paquete(paquete, archivo=None, tope=None):
    """Recorta el paquete a lo minimo que necesita el cerebro que lo recibe.

    Medido el 2026-09-10 (Julio: "a un cerebro solo le llega lo suyo"): al auditor le
    llegaban 24.124 letras y aguanta ~19.000; por eso su respuesta salia cortada a mitad
    de palabra y el veredicto salia RECHAZADO o SIN_AUDITAR con JSON roto. La vigia verde
    mentia porque miraba si el mando NOMBRABA al filtro, no si el filtro existia.

    Se conserva SOLO lo que hace falta para juzgar:
      - la ley que manda (seccion "LA LEY QUE MANDA"),
      - los trozos EXACTOS del archivo que se toca (si viene), no los de todos los archivos,
      - la seccion "A QUIEN PUEDE DANAR" (para no romper vecinos).
    Se descarta el relleno: "ya se reparo antes", bocas de piezas, vigias, listados.
    """
    if not isinstance(paquete, str):
        from cerebro import router as _r
        paquete = _r.a_texto(paquete)
    tope = tope or TOPE_GRATIS
    bloques = {"__cabecera__": []}
    actual = "__cabecera__"
    for ln in paquete.splitlines():
        m = re.match(r"^## (\d+)\.\s+(.*)", ln)
        if m:
            actual = "%s. %s" % (m.group(1), m.group(2))
            bloques[actual] = [ln]
        else:
            bloques.setdefault(actual, []).append(ln)
    ley = next((k for k in bloques if "LA LEY QUE MANDA" in k), None)
    trozos = next((k for k in bloques if "LOS TROZOS" in k.upper()), None)
    dana = next((k for k in bloques if "DANAR" in k.upper()), None)
    salida = list(bloques["__cabecera__"])
    for k in (ley, dana):
        if k and k != "__cabecera__":
            salida += bloques[k]
    if trozos and archivo:
        _lista = [archivo] if isinstance(archivo, str) else [a for a in archivo if a]
        solo = []
        i = 0
        t = bloques[trozos]
        while i < len(t):
            if t[i].startswith("### `"):
                j = i + 1
                while j < len(t) and not t[j].startswith("### `"):
                    j += 1
                if any(a in t[i] for a in _lista):
                    solo += t[i:j]
                i = j
            else:
                solo.append(t[i])
                i += 1
        if solo:
            salida += solo
    elif trozos:
        # Sin archivo a que atarse, quedan los bloques de trozos, del mas relevante para abajo
        # hasta que entre en el tope. El relleno de menor relevancia se suelta primero.
        t = bloques[trozos]
        bloques_trozo = []
        i = 0
        while i < len(t):
            if t[i].startswith("### `"):
                j = i + 1
                while j < len(t) and not t[j].startswith("### `"):
                    j += 1
                m = re.search(r"relevancia\s+([\d\.]+)", t[i])
                bloques_trozo.append((float(m.group(1)) if m else 0.0, t[i:j]))
                i = j
            else:
                i += 1
        bloques_trozo.sort(key=lambda x: x[0], reverse=True)
        resto = salida
        for _relev, _lines in bloques_trozo:
            if len("\n".join(resto)) >= tope:
                break
            resto = resto + _lines
        salida = resto
    # Si aun asi se pasa del tope, se va soltando el relleno del final hasta caber: la cabecera,
    # la ley y "a quien puede danar" son LO NECESARIO, no se tocan.
    while len("\n".join(salida)) > tope and len(salida) > len(bloques["__cabecera__"]):
        salida.pop()
    return "\n".join(salida)


def _material_del_revisor(paquete, propuesta, tope):
    """Devuelve el material para el revisor con el trozo tocado entero delante."""
    try:
        archivo = propuesta.get("archivo") if isinstance(propuesta, dict) else None
        base = _filtrar_paquete(paquete, archivo=archivo, tope=tope)
        if not isinstance(propuesta, dict):
            return base
        viejo = str(propuesta.get("texto" + "_viejo") or "").strip()
        if not viejo:
            return base
        if not isinstance(paquete, str):
            from cerebro import router as _r
            paquete = _r.a_texto(paquete)
        lineas = paquete.splitlines()
        bloques = []
        i = 0
        while i < len(lineas):
            if lineas[i].startswith("### " + chr(96)):
                j = i + 1
                while j < len(lineas) and not lineas[j].startswith("### " + chr(96)) and not lineas[j].startswith("## "):
                    j += 1
                bloques.append(lineas[i:j])
                i = j
            else:
                i += 1
        tocados = [b for b in bloques if viejo in "\n".join(b)]
        if not tocados:
            return base
        arriba = ["## EL CAMBIO SE HACE AQUI (trozo entero)"]
        for b in tocados:
            arriba += b
        resultado = "\n".join(arriba) + "\n" + base
        if len(resultado) > tope:
            resultado = resultado[:tope]
        return resultado
    except Exception:
        try:
            return base
        except Exception:
            return ""


TOPE_LOCAL = 26000    # MEDIDO 2026-08-21: 3/3 hasta 26.000; 28.000/30.000/35.000/40.000 = 0/3 (RECHAZA)
# TOPE_PESADO ya NO decide el reparto (2026-09-09, punto 1 de la causa raiz): la decision la toma
# la capacidad MEDIDA (cuotas.rankear). El numero se deja porque `medir_las_nueve_puertas.py` lo
# lee para su tabla de medidas; borrarlo seria romper un vecino que solo lo mira.
TOPE_PESADO = 15000   # informativo: capacidad documentada vieja, ya no manda nada


def quienes_hay():
    """Que cerebros tienen con que atender AHORA (llave o servicio)."""
    c, cf = prestar_cerebro()
    if not c:
        return []
    # Cada cerebro de la fila entra si su PUERTA tiene llave y el tiene modelo configurado.
    # Antes solo se reconocian tres nombres sueltos, asi que los cerebros que se anadian a la
    # fila NUNCA entraban: se quedaban de adorno. Por eso, con Groq agotado, no quedaba un
    # segundo cerebro para AUDITAR y el que proponia se aprobaba solo (fallo real 2026-08-21).
    vel = _velocidad()
    llaves = {"groq": "GROQ_API_KEY", "gemini": "GEMINI_API_KEY",
              "router": "OPENROUTER_API_KEY", "deepseek": "DEEPSEEK_API_KEY"}
    hay = []
    for quien in cuotas.ORDEN:
        if quien == "local":
            continue
        puerta = next((p for p in llaves if quien.startswith(p)), None)
        if not puerta or not os.environ.get(llaves[puerta], "").strip():
            continue
        if vel.get("modelo_" + quien):
            hay.append(quien)
    # LM Studio se DETECTA, no se declara. Fallo real 2026-08-20: estaba encendido y
    # sirviendo qwen2.5-coder, pero como no habia variable de entorno el Ingeniero no lo veia,
    # y se quedaba sin cerebro cuando los de la nube tardaban. El local no tiene cuota ni
    # latencia caprichosa: es la red de seguridad.
    if os.environ.get("DMM_LOCAL", "").strip() or os.environ.get("LMSTUDIO_URL", "").strip()             or _local_responde():
        hay.append("local")
    return hay


def _local_responde(url=None, espera=3):
    """True si LM Studio esta escuchando de verdad. Se comprueba, no se supone."""
    import urllib.request
    url = (url or os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1")).rstrip("/")
    try:
        with urllib.request.urlopen(url + "/models", timeout=espera) as r:
            return r.status == 200
    except Exception:
        return False


def _modelo_local(url=None):
    """Que modelo esta sirviendo LM Studio ahora mismo. Se pregunta, no se adivina."""
    import urllib.request, json as _j
    url = (url or os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1")).rstrip("/")
    try:
        with urllib.request.urlopen(url + "/models", timeout=3) as r:
            datos = _j.load(r).get("data", [])
        for m in datos:                      # el de embeddings no sirve para conversar
            if "embed" not in m.get("id", "").lower():
                return m["id"]
    except Exception:
        pass
    return os.environ.get("LMSTUDIO_MODEL", "qwen2.5-coder-1.5b-instruct")


def preguntar_local(prompt, temperatura=0.2, espera=180):
    """Habla con LM Studio DIRECTAMENTE, sin pasar por el cerebro de DMM.

    Fallo real 2026-08-20: `cerebro.preguntar(forzar='local')` de DMM se iba a Gemini igual y
    devolvia 404 tras 305 segundos. El local es la RED DE SEGURIDAD (sin cuota, sin latencia
    caprichosa): tiene que funcionar aunque el cerebro prestado falle.
    """
    import urllib.request, json as _j
    url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1").rstrip("/")
    datos = _j.dumps({"model": _modelo_local(url),
                      "messages": [{"role": "user", "content": prompt}],
                      "temperature": temperatura, "max_tokens": 2000}).encode("utf-8")
    req = urllib.request.Request(url + "/chat/completions", data=datos, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=espera) as r:
        d = _j.load(r)
    return d["choices"][0]["message"]["content"]


def _velocidad():
    """Lee arnes/velocidad.config: que modelo usar y cuanto se espera antes de pasar turno."""
    d = {"modelo_groq": "llama-3.3-70b-versatile", "modelo_gemini": "gemini-2.0-flash",
         "tope_segundos": "75"}
    try:
        for ln in open(os.path.join(AQUI, "arnes", "velocidad.config"), encoding="utf-8").read().splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                d[k.strip()] = v.strip()
    except Exception:
        pass
    return d


def _con_tope(fn, segundos):
    """Corre fn con tope de tiempo. Si se pasa, se abandona y pasa el turno.
    Medido el 2026-08-20: qwen3.6-27b tardaba >300s con un paquete normal. Julio: nada lento."""
    caja = {}

    def _correr():
        try:
            caja["r"] = fn()
        except Exception as e:
            caja["e"] = e

    h = threading.Thread(target=_correr, daemon=True)
    h.start()
    h.join(segundos)
    if h.is_alive():
        raise TimeoutError(f"tardo mas de {segundos}s")
    if "e" in caja:
        raise caja["e"]
    return caja.get("r", "")


def _gemini_directo(prompt, temperatura, modelo):
    """Le habla a Gemini con EL MODELO QUE ELIGE EL INGENIERO.

    Hacia falta porque el cerebro prestado tenia quemados dos modelos que YA NO EXISTEN
    (gemini-2.0-flash y de respaldo gemini-1.5-flash): los dos daban 404. Por eso Gemini fallaba
    4 de cada 7 veces y el trabajo nunca acababa en el cerebro gratis, sino en la IA cara, o sea
    Julio pagando. Fallo real 2026-08-21, el que mas dinero le costo.
    MEDIDO ese dia con el paquete grande: 3.5-flash 3.3s | 3-flash-preview 3.4s | latest 9.3s |
    3.7-flash 29.1s | 3.6-flash 62.8s | 2.5-flash y 2.0-flash: 404, muertos."""
    import json as _j, os as _o, urllib.request as _u, urllib.parse as _up
    # Un nombre de la fila SIN modelo configurado reventaba mudo con "can only concatenate str
    # (not NoneType) to str" y tumbaba el relevo dejando el ciclo sin revisor (fallo real
    # 2026-08-31: gemini4 estaba en ORDEN pero no en el dict `modelos`). Se avisa CLARO y por
    # su nombre, no con un mensaje sin sentido: un cerebro de adorno hace creer que hay relevo
    # cuando no lo hay, peor que no tenerlo.
    if not modelo:
        raise RuntimeError("no hay modelo configurado para Gemini")
    k = _o.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        raise RuntimeError("no hay llave de Gemini")
    # 2000 era MUY corto: la propuesta llega con codigo dentro y se cortaba a medio JSON, asi
    # que el motor la tiraba entera por "ilegible". Se tiraba trabajo BUENO ya hecho y pagado.
    body = _j.dumps({"contents": [{"parts": [{"text": prompt}]}],
                     "generationConfig": {"temperature": temperatura,
                                          "maxOutputTokens": 8192}}).encode("utf-8")
    url = ("https://generativelanguage.googleapis.com/v1beta/models/" + modelo +
           ":generateContent?key=" + _up.quote(k))
    req = _u.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    with _u.urlopen(req, timeout=300) as r:
        d = _j.load(r)
    return d["candidates"][0]["content"]["parts"][0]["text"]


def _openrouter_directo(prompt, temperatura, modelo):
    """La puerta de OpenRouter, que Julio pidio el 2026-08-21 para traer DeepSeek y los que quiera.

    Es UNA puerta con MUCHOS cerebros detras, que es justo lo que el pedia: "tu debes ser el
    ultimo recurso, cuando se agoten los modelos gratis, o sea nunca, porque existen cientos".
    La llave va SOLA en el .env privado (OPENROUTER_API_KEY): nunca se le pide a Julio que la
    escriba en el chat. Sin llave, este cerebro no entra en la fila y no estorba."""
    import json as _j, os as _o, urllib.request as _u
    k = _o.environ.get("OPENROUTER_API_KEY", "").strip()
    if not k:
        raise RuntimeError("no hay llave de OpenRouter en el .env")
    if not modelo:
        raise RuntimeError("no hay modelo de OpenRouter configurado")
    body = _j.dumps({"model": modelo, "temperature": temperatura,
                     "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = _u.Request("https://openrouter.ai/api/v1/chat/completions", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + k)
    with _u.urlopen(req, timeout=300) as r:
        d = _j.load(r)
    return d["choices"][0]["message"]["content"]


def _deepseek_directo(prompt, temperatura, modelo):
    """La puerta PROPIA de DeepSeek. Julio, 2026-08-21: "no es openrouter, es deepseek".

    Se le habla a SU casa (api.deepseek.com), no a traves de otra empresa que hace de
    intermediaria. Habla el mismo idioma que Groq (formato OpenAI), asi que lo unico que cambia
    es la direccion y la llave: DEEPSEEK_API_KEY, que va SOLA en las variables de Windows y no se
    le pide nunca a Julio por el chat.

    Es el supervisor de pago que Julio quiere por defecto (si Claude son las manos, DeepSeek supervisa;
    y al reves). OJO: NO es el "4ojos" del canal — en el canal "4ojos" es Cline, el encargado de la
    ventana de VS Code. DeepSeek es el CEREBRO de pago; Cline es el ENCARGADO; son dos cosas distintas.

    LO QUE LO SEPARA DE TODOS LOS DEMAS: DeepSeek NO ES GRATIS, va con saldo. Por eso esta en
    `cuotas.DE_PAGO` y no se le pregunta a la vez que a los gratis, sino a solas y de ultimo.
    Sin llave no entra en la fila y no estorba a nadie."""
    import json as _j, os as _o, urllib.request as _u
    k = _o.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not k:
        raise RuntimeError("no hay llave de DeepSeek en las variables de Windows")
    body = _j.dumps({"model": modelo or "deepseek-chat", "temperature": temperatura,
                     "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = _u.Request("https://api.deepseek.com/chat/completions", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + k)
    with _u.urlopen(req, timeout=300) as r:
        d = _j.load(r)
    try:
        import datetime
        _ruta = _o.environ.get('INGENIERO_GASTO_USD_TEST') or _o.path.join(
            _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), 'memoria', 'GASTO_USD.jsonl')
        with open(_ruta, 'a', encoding='utf-8') as _f:
            _f.write(_j.dumps({'cuando': datetime.datetime.now().isoformat(timespec='seconds'),
                               'modelo': d.get('model', ''),
                               'uso': d.get('usage') or {}}) + '\n')
    except Exception:
        pass
    return d["choices"][0]["message"]["content"]


# Ley Julio 2026-09-14: Claude revisa lo de DeepSeek solo cuando todas las gratis duermen.
def _claude_directo(prompt):
    import shutil, subprocess
    exe = shutil.which('claude')
    if not exe:
        raise RuntimeError('no encuentro el programa claude en el PATH')
    r = subprocess.run([exe, '-p'], input=prompt, capture_output=True, text=True, encoding='utf-8', timeout=300)
    if r.returncode != 0 or not (r.stdout or '').strip():
        raise RuntimeError((r.stderr or '')[:200])
    return r.stdout


def _preguntar_con_relevo(prompt, temperatura, evitar=None, primero=None, pesado=False,
                          clase="", vuelta=0):
    """Pregunta respetando el orden de Julio: Qwen -> Gemini -> local, y VOLVIENDO a Qwen
    en cuanto despierte. Si uno se agota (429/cuota), se le marca la siesta y sigue el de al lado.
    Devuelve (texto, quien_contesto, avisos). Cada intento queda anotado en el cuaderno de
    llamadas (cuerpo/cuaderno.py), que es un PROGRAMA: el por que de cada fallo se MIDE, no se
    supone (CONTRATO_EL_EQUIPO_ESCRIBE, "el cuaderno de llamadas dira si sigue pasando y cuando")."""
    c, _ = prestar_cerebro()
    if not c:
        return "", "", ["NO_ENCONTRADO: sin cerebro"]
    evitar_lista = evitar if isinstance(evitar, list) else [evitar] if evitar else []
    hay = [q for q in quienes_hay() if q not in evitar_lista]
    turnos = cuotas.fila(hay) or hay          # si todos duermen, se intenta igual (por si desperto ya)
    if primero and primero in turnos:         # el que reparte el trabajo cruzado manda
        turnos = [primero] + [q for q in turnos if q != primero]
    avisos = []
    vel = _velocidad()
    # DE UNA SOLA FUENTE, NUNCA A MANO (fallo real 2026-08-31, el que mas dinero costo ese dia).
    # Antes esta lista se escribia nombre por nombre, y quienes_hay() sacaba los suyos de otro
    # sitio: de `vel`. Dos listas que tenian que decir lo mismo y que nadie comparaba nunca.
    # Un nombre configurado entraba en la fila pero NO estaba aqui, asi que al hablarle el modelo
    # llegaba vacio, reventaba, el relevo lo contaba como un fallo mas y el ciclo se quedaba SIN
    # REVISOR: todo el trabajo caia en el cerebro de PAGO, pagandolo Julio, sin ninguna necesidad.
    # Anadir el nombre que faltaba habria tapado el caso de ese dia; manana se configura otro y
    # vuelve a pasar igual. Por eso ahora sale de la MISMA fuente: quien se configura, entra en la
    # fila Y se sabe como llamarle. No hay dos sitios que recordar.
    # Cada modelo de Groq es un cupo gratis distinto: Groq reparte POR MODELO, no por llave.
    modelos = {}
    for _quien in cuotas.ORDEN:
        # el de casa no se llama por internet: no tiene modelo que pedirle a nadie
        modelos[_quien] = None if _quien == "local" else vel.get("modelo_" + _quien)
    for k in vel:
        if k.startswith("modelo_router"):
            modelos[k[len("modelo_"):]] = vel[k]
    tope = float(vel.get("tope_segundos", 75))

    # EL DE PAGO NO ENTRA EN LA PREGUNTA A LA VEZ (auditoria de DeepSeek, 2026-08-21).
    # Abajo se les pregunta a TODOS A LA VEZ porque "son todos gratis, preguntar no cuesta".
    # Con DeepSeek dentro esa frase deja de ser cierta: se le pagaria una llamada en CADA
    # pregunta aunque contestase antes uno gratis. Lo cazo el propio DeepSeek al auditar esto.
    # Asi que se le aparta aqui y se le guarda para el ULTIMO RECURSO, a solas.
    de_pago = [q for q in turnos if q in cuotas.DE_PAGO]
    turnos = [q for q in turnos if q not in cuotas.DE_PAGO]
    # EL FILTRO DEL PASILLO (2026-09-10, la solucion unica): aqui es donde nace de verdad el
    # fallo recurrente (medido: se mandaban 7.575 letras y llegaban 35.845; la vigia miraba el
    # papel, no el hecho). Para cuando el prompt llega aqui ya viene inflado (plantilla + tarea
    # + material del auditor duplicado), y la unica jugada posible era saltar cerebros; saltar
    # a todos = paga el de pago = se juzga a si mismo. Ahora se RECORTA antes de elegir, UNA
    # vez, para las 9 puertas. El tope es la capacidad real MEDIDA del gratis mas pequeno que
    # esta despierto: recortar para el garantiza que ningun gratis quede fuera por tamano.
    # Se respeta lo "pesado": si Julio pidio de verdad al de pago, no se le recorta su material.
    if turnos and not pesado:
        _capas = [cuotas._capacidad(q) for q in turnos]
        _capas = [c for c in _capas if c > 0]
        if _capas:
            _tope_pasillo = min(_capas)
            if len(prompt) > _tope_pasillo:
                _antes = len(prompt)
                _recortado = asignador.recortar_prompt(prompt, _tope_pasillo)
                if 0 < len(_recortado) < _antes:
                    prompt = _recortado
                    avisos.append("el pasillo recorto el encargo de %d a %d letras para que "
                                  "le quepa a un cerebro gratis (tope medido: %d)"
                                  % (_antes, len(_recortado), _tope_pasillo))
    # EL DE PAGO ENTRA SI NADIE GRATIS AGUANTA, NO POR UN TOPE ESCRITO A MANO.
    # Antes el reparto lo decidia un numero puesto de memoria (15.000 letras) sin mirar a nadie.
    # Medido el 2026-09-09 (punto 1 de la auditoria de causa raiz): los gratis llevan 0 de 72
    # trabajos escritos, y en un paquete normal 8 de 12 salidas pasaban ese tope aunque los gratis
    # SI las aguantaban (un paquete de 14.858 llego a medir 25.122).
    # Ahora la condicion es la verdad medible: si NINGUN gratis de `turnos` (que ya viene sin los
    # de pago, arriba) aguanta ese tamano segun la capacidad MEDIDA, entra el de pago de primero;
    # si algun gratis aguanta, se le da la oportunidad y el de pago queda solo de ultimo recurso.
    # `pesado` sigue mandando cuando de verdad se pidio trabajo pesado (regla F2 de Julio).
    # Y sigue en pie la orden de siempre: lo que NO le cabe a nadie va a DeepSeek, y el bloqueo F2
    # de abajo salta si DeepSeek no esta. AUDITAR (lo ligero) sigue gratis, que es donde manda la
    # ley de coste.
    if pesado or not cuotas.rankear(turnos, len(prompt)):
        turnos = de_pago + turnos
        de_pago = []
    # REPARTIDOR POR METRICAS (Julio, 2026-08-21): se asigna por eficiencia, no preguntando a
    # todos a la vez. `cuotas.rankear` ordena del mas eficiente al menos y SALTA a los que no
    # soportan el tamano. Asi no se gasta tokens en preguntar a quien no va a poder.
    turnos_antes = list(turnos)
    turnos = cuotas.rankear(turnos, len(prompt))
    # DESPUES de rankear, nunca antes: rankear ordena por eficiencia y volveria a hundir al de
    # pago, deshaciendo la orden de Julio sin que se notara.
    # AVISOS DE CAPACIDAD (2026-09-01): si rankear salto a alguien por tamano, se dice quien fue
    # y cuanto aguantaba. Y si no quedo nadie, se avisa claro de que hay que PARTIR el trabajo.
    saltados = [q for q in turnos_antes if q not in turnos]
    for _saltado in saltados:
        avisos.append("%s no le cabe (%d letras, aguanta %d) -> se le salta" % (
            cuotas.APODO[_saltado], len(prompt), cuotas._capacidad(_saltado)))
    if not turnos:
        _mas_aguanta = max(turnos_antes, key=cuotas._capacidad, default=None)
        if _mas_aguanta:
            avisos.append("ENCARGO NO LE CABE A NADIE: mide %d letras, el que mas aguanta es %s "
                          "con %d. HAY QUE PARTIRLO en trozos mas pequenos." % (
                              len(prompt), cuotas.APODO[_mas_aguanta], cuotas._capacidad(_mas_aguanta)))
        else:
            avisos.append("ENCARGO NO LE CABE A NADIE: mide %d letras y no hay cerebro disponible. "
                          "HAY QUE PARTIRLO en trozos mas pequenos." % len(prompt))
    # SI NO HAY LLAVE DE DEEPSEEK no pasa nada: no estara en `turnos`, esto no hace nada y el
    # relevo sigue con los gratis. Julio no se queda atrapado por no tener saldo.
    # SI DEEPSEEK FALLA tampoco pasa nada: comprobado en el bucle de abajo, cualquier fallo cae
    # en el `except` y PASA EL TURNO al siguiente. (Los dos cerebros avisaron de que aqui se
    # colgaria; se fue a mirar el codigo y los dos se equivocaban.)
    if pesado and "deepseek" in turnos:
        turnos = ["deepseek"] + [q for q in turnos if q != "deepseek"]
    # F2 (Julio 2026-08-24): NUNCA trabajar solo. Si la tarea es de VOLUMEN y DeepSeek (la mano
    # de pago) NO esta disponible, se BLOQUEA: no se cae a qwen/gemini para llenar el hueco.
    if pesado and "deepseek" not in [q for q in quienes_hay()]:
        return ("", "", [
            "BLOQUEADO F2 (Julio 2026-08-24): tarea de VOLUMEN y DeepSeek (la mano) no esta "
            "disponible. No se usa qwen/gemini para lo pesado. Habilita DeepSeek o reduce la tarea."])

    def _ultimo_recurso(avisos):
        """Se llama SOLO cuando ningun cerebro gratis pudo. Aqui empieza a costar dinero."""
        for quien in de_pago:
            try:
                txt = _con_tope(lambda: _pedirle_a(quien),
                                max(tope, cuotas.cuanto_esperarle(quien)))
                if not (txt or "").strip():
                    raise ValueError("contesto vacio")
                cuotas.apuntar_uso(quien, ok=True)
                avisos.append("no quedaba ningun cerebro gratis: contesto %s, que SE PAGA"
                              % cuotas.APODO[quien])
                cuaderno.apuntar(quien, tamano=len(prompt_nube), vuelta=vuelta, clase=clase,
                                 resultado=cuaderno.OK, crudo=(txt or "")[:120])
                return txt, quien, avisos
            except Exception as e:
                msg = str(e)
                cuotas.apuntar_uso(quien, ok=False)
                if cuotas.es_agote(msg):      # sin saldo cuenta como agotado: a dormir, no insistir
                    cuotas.dormir(quien, msg)
                avisos.append("%s fallo: %s" % (cuotas.APODO[quien], msg[:90]))
                cuaderno.apuntar(quien, tamano=len(prompt_nube), vuelta=vuelta, clase=clase,
                                 resultado=cuaderno.ERROR, crudo=msg[:120])
        return "", "", avisos + ["NO_ENCONTRADO: ningun cerebro pudo atender"]

    # SOLO CODIGO A LA NUBE (Julio, 2026-08-21). Se tapa AQUI, en el unico sitio por donde sale
    # todo, y no en cada sitio que llama: si depende de acordarse, un dia no se acuerda.
    # El cerebro de tu PC no cuenta: ahi no sale nada del ordenador.
    try:
        from cuerpo import privacidad as _pv
        prompt_nube, _tapados = _pv.limpiar(prompt)
        if _tapados:
            avisos.append(_pv.aviso(_tapados))
    except Exception:
        prompt_nube, _tapados = prompt, 0

    def _pedirle_a(quien):
        """Le habla a UN cerebro. Directo, con su modelo, sin red que tape errores.
        A la nube va el encargo LIMPIO; al de tu PC va entero, porque no sale de casa."""
        if quien == "local":
            # El de casa es un modelo pequeno: con un encargo largo devuelve error 400 porque no
            # le cabe. Fallaba 8 de cada 9 veces por esto. Se le dan los cortos, que si atiende.
            if len(prompt) > TOPE_LOCAL:
                raise ValueError("encargo demasiado largo para el cerebro de tu PC "
                                 "(%d letras): no le cabe" % len(prompt))
            return preguntar_local(prompt, temperatura)
        # De aqui para abajo el encargo SALE DE CASA: va el limpio, sin datos de clientes.
        # DeepSeek va el PRIMERO de los desvios, como pidio el en su auditoria: asi se ve de un
        # vistazo que el unico de pago tiene su camino propio y no se cuela por el de nadie.
        if quien.startswith("deepseek"):
            return _deepseek_directo(prompt_nube, temperatura, modelos.get(quien))
        if quien.startswith("gemini"):
            return _gemini_directo(prompt_nube, temperatura, modelos.get(quien))
        if quien.startswith("router"):
            return _openrouter_directo(prompt_nube, temperatura, modelos.get(quien))
        return c._preguntar_groq(prompt_nube, modelos.get(quien), temperatura)

    # REPARTIDOR POR CAPACIDAD Y EFICIENCIA (Julio, 2026-08-21). Antes se les preguntaba a TODOS
    # A LA VEZ y ganaba el primero: eso gastaba tokens en todos, los desgastaba y les mandaba
    # trabajo que no aguantan. Ahora `turnos` ya viene ordenado por `cuotas.rankear` (del mas
    # eficiente al menos, SALTANDO a los que no soportan el tamano), y se pregunta de UNO EN UNO
    # con su propio tope de tiempo. Flexible con el tiempo, implacable con la precision: una
    # respuesta vacia NO vale, y un modelo que no existe da error a la vista, no se disimula.
    for quien in turnos:
        try:
            _t0 = time.time()
            # UNA SOLA PUERTA para hablar con los cerebros: `_pedirle_a`.
            # Antes esto era una copia de aquella logica, y las copias se desincronizan: la ley de
            # privacidad de Julio se engancho arriba y por AQUI seguian saliendo los datos sin
            # tapar. Un camino duplicado es un agujero esperando su turno.
            txt = _con_tope(lambda: _pedirle_a(quien), max(tope, cuotas.cuanto_esperarle(quien)))
            if not (txt or "").strip():
                cuaderno.apuntar(quien, tamano=len(prompt_nube), vuelta=vuelta, clase=clase,
                                 resultado=cuaderno.VACIO, crudo="", segundos=time.time() - _t0)
                raise ValueError("contesto vacio")
            cuotas.apuntar_uso(quien, ok=True, tamano=len(prompt_nube))
            cuaderno.apuntar(quien, tamano=len(prompt_nube), vuelta=vuelta, clase=clase,
                             resultado=cuaderno.OK, crudo=(txt or "")[:120], segundos=time.time() - _t0)
            return txt, quien, avisos
        except TimeoutError as e:
            cuotas.apuntar_uso(quien, ok=False)
            cuotas.dormir(quien, "LENTO: " + str(e))
            avisos.append(f"{cuotas.APODO[quien]} tardo demasiado -> pasa el turno")
            continue
        except Exception as e:
            msg = str(e)
            cuotas.apuntar_uso(quien, ok=False)
            if cuotas.es_agote(msg):
                cuotas.dormir(quien, msg)
                avisos.append(f"{cuotas.APODO[quien]} se agoto -> pasa el turno")
            elif cuotas.es_no_cupo(msg):
                cuaderno.apuntar(quien, tamano=len(prompt_nube), vuelta=vuelta, clase=clase,
                                 resultado=cuaderno.NO_CUPO, crudo=msg[:120], segundos=time.time() - _t0)
                # NO LE CABE (CONTRATO_EQUIPO_QUE_AGUANTA, 2026-08-24). Mandarle a dormir no
                # sirve de nada: no se va a hacer mas grande. Se le BAJA EL TECHO para no
                # volver a pedirle algo de este tamano.
                # Sin esto, los dos gratis devolvieron 413 en TODAS las llamadas del dia sobre
                # Foto Informe y se les siguio eligiendo en cada intento: el equipo no podia
                # auditar ese proyecto y "auditado" acabo significando "nadie lo vio".
                cuotas.apuntar_no_cupo(quien, len(prompt_nube))
                avisos.append(f"{cuotas.APODO[quien]} NO LE CUPO ({len(prompt_nube)} letras) "
                              f"-> se le baja el techo y no se le vuelve a pedir de este tamano")
            else:
                cuaderno.apuntar(quien, tamano=len(prompt_nube), vuelta=vuelta, clase=clase,
                                 resultado=cuaderno.ERROR, crudo=msg[:120], segundos=time.time() - _t0)
                avisos.append(f"{cuotas.APODO[quien]} fallo (no es cuota): {msg[:90]}")
    return _ultimo_recurso(avisos)          # ningun gratis pudo: ahora si, el de pago


def _validar_en_paquete(paquete, propuesta, tarea=""):
    """FRENO (2026-08-24): que el modelo use SOLO la memoria del paquete, no invente.

    Julio: "que usen la memoria indexada, los paquetes, para que no vuelvan a rechazar trabajo
    o hacer lo que se les de la gana." Esto comprueba que todo archivo que el modelo nombra
    (archivo, codigo, puede_danar) esta DECLARADO en el paquete. Si inventa uno, se le marca
    para que el auditor y el bucle lo atajen; no se le deja pasar como si valiera.

    SEGURIDAD (2026-08-24): si le llega la CAJA (dict del paquete) en vez del texto, se normaliza.
    Antes esto se caia con TypeError y el freno no protegia nada (fallo real 2026-08-24).
    """
    if not isinstance(paquete, str):
        from cerebro import router as _r
        paquete = _r.a_texto(paquete)
    declarados = set()
    for m in re.finditer(r"^### `([^`]+?)`", paquete or "", re.M):
        declarados.add(m.group(1).split(":")[0].split("/")[-1].strip())
    # LO QUE LA TAREA PIDE CREAR NO ES INVENTO (Julio, 2026-09-05: "crea las habilidades").
    # Una pieza NUEVA nunca puede venir en el paquete: todavia no existe. Si la tarea nombra su
    # ruta, la declara la propia tarea. Sin esto el equipo NO PODIA CREAR NADA NUEVO: cinco
    # encargos seguidos de crear una habilidad se rechazaron por invento el 2026-09-05.
    for m in re.findall(r"[\w/]+\.(?:py|html|js|ts|css|sql|md)", str(tarea or "")):
        declarados.add(m.split("/")[-1].strip())
    p = propuesta or {}
    inventados = []
    arch = str(p.get("archivo") or "")
    if arch:
        b = arch.split("/")[-1]
        if b and b not in declarados:
            inventados.append(b)
    for campo in ("codigo", "cambio", "puede_danar"):
        for m in re.findall(r"[\w/]+\.(?:py|html|js|ts|css|sql)", str(p.get(campo) or "")):
            b = m.split("/")[-1]
            if b and b not in declarados:
                inventados.append(b)
    return sorted(set(inventados))


def auditar(paquete, propuesta, auditor=None, evitar=None):
    """Pide a un cerebro que REVISE una propuesta ya escrita. No escribe ni genera nada.

    Nace porque arnes/copista.py aplica cambios ya decididos sin llamar a un cerebro, y
    despues hay que pedirle al equipo que lo revise. Antes toda la logica de revisar
    estaba metida dentro de trabajar, mezclada con la de escribir, y no habia forma de
    decir "esto ya esta hecho, solo revisalo".

    Devuelve (auditoria, quien_reviso, avisos).
    """
    auditoria = None
    avisos = []   # se acumulan TODOS los avisos de TODOS los intentos del revisor
    quien_aud = None
    auditor_ok = auditor
    if auditor == evitar:
        # el auditor pedido es el mismo que genero: se descarta, se busca otro y se avisa
        auditor_ok = None
        avisos.append("el auditor pedido (%s) era el mismo que genero; se busca otro" % auditor)
    # AL AUDITOR SOLO LE LLEGA LO SUYO (Julio, 2026-09-10). Antes le llegaba el bulto entero:
    # medido 24.124 letras y aguanta ~19.000, y por eso la respuesta salia cortada a la mitad.
    # Se filtra el paquete a lo que de verdad necesita para auditar esta propuesta.
    archivo_tocado = None
    if isinstance(propuesta, dict):
        archivo_tocado = propuesta.get("archivo") or propuesta.get("archivos")
        if isinstance(archivo_tocado, list) and archivo_tocado:
            archivo_tocado = archivo_tocado[0]
        if isinstance(archivo_tocado, str):
            archivo_tocado = archivo_tocado.strip()
    material_auditor = _filtrar_paquete(paquete, archivo=archivo_tocado,
                                        tope=TOPE_REVISOR - 3344 - 47 -
                                             len(json.dumps(propuesta, ensure_ascii=False)))
    if auditor == 'bigpickle':
        # Big Pickle es la revisora (plan v4 paso 1). Se llama aqui, antes del bucle de
        # reintentos, y el bucle se deja en 0 vueltas para que ningun otro cerebro la sustituya.
        from cuerpo import bigpickle
        _texto_bp, _avisos_bp = bigpickle.preguntar(
            _prompt_auditor(material_auditor, json.dumps(propuesta, ensure_ascii=False)))
        avisos.extend(_avisos_bp or [])
        if _texto_bp:
            quien_aud = 'bigpickle'
            auditoria = _json_de(_texto_bp)
    for _intento in range(0 if auditor == 'bigpickle' else 2):
        crudo_a, quien_aud, av_intento = _preguntar_con_relevo(
            _prompt_auditor(material_auditor, json.dumps(propuesta, ensure_ascii=False)), 0.1,
            evitar=evitar, primero=auditor_ok, clase="auditar", vuelta=_intento + 1)
        avisos += av_intento   # no se pierde lo que dijo el primer intento
        if not crudo_a:
            continue                       # no contesto: se le pide de nuevo
        auditoria = _json_de(crudo_a)
        if isinstance(auditoria, dict) and "_error" not in auditoria:
            break                          # se entendio: listo
        # JSON roto/cortado: no se da por perdido (cura que ya existe en cruzado.py).
    if not isinstance(auditoria, dict) or "_error" in (auditoria or {}):
        # EL INFORME NO MIENTE: si el revisor contesto roto, se dice claro, no '?'.
        auditoria = {"veredicto": "SIN_AUDITAR",
                     "_error": ((auditoria or {}).get("_error", "")
                                 if isinstance(auditoria, dict) else ""),
                     "resumen_para_el_jefe":
                         "el revisor contesto roto; se conserva la propuesta del obrero"}

    # Si se pidio un auditor y no fue el que reviso, se avisa.
    if auditor and quien_aud != auditor:
        avisos.append("se pidio auditar a %s y no esta disponible: reviso %s" % (auditor, quien_aud))

    # A-38 punto 4 (Julio 2026-09-19): si bigpickle esta caido, revisa otra IA con solo lo necesario, nunca claude ni quien escribio.
    revisor_fijo = auditor if auditor == 'bigpickle' else None
    if revisor_fijo and quien_aud != revisor_fijo:
        crudo_r, quien_r, av_r = _preguntar_con_relevo(
            _prompt_auditor(material_auditor, json.dumps(propuesta, ensure_ascii=False)), 0.1,
            evitar=evitar, clase='auditar', vuelta=1)
        avisos += av_r
        aud_r = _json_de(crudo_r) if crudo_r else None
        if isinstance(aud_r, dict) and '_error' not in aud_r and quien_r != 'claude':
            auditoria = aud_r
            quien_aud = quien_r
            avisos.append('bigpickle no estaba: revisa %s con solo lo necesario (A-38)' % quien_r)
        else:
            auditoria = {'veredicto': 'SIN_AUDITAR',
                         'resumen_para_el_jefe': 'bigpickle no estaba y ninguna otra IA pudo revisar'}
            avisos.append('bigpickle no estaba y el relevo no contesto: SIN_AUDITAR (A-38)')
        return auditoria, quien_aud, avisos

    # A-32 (Julio 2026-09-18, reemplaza la ley del 2026-09-14): si todas las gratis duermen, revisa Big Pickle, nunca Claude ni quien escribio.
    # SOLO si el encargo NO pidio un revisor fijo (ley de Julio 2026-09-15).
    if auditoria is None or auditoria.get('veredicto') == 'SIN_AUDITAR':
        dormidos = {q for q in cuotas.ORDEN if not cuotas.desperto(q)}
        if cuotas.puede_revisar_bigpickle(evitar or '', dormidos):
            try:
                from cuerpo import bigpickle as _bp_a32
                _texto_bp2, _avisos_bp2 = _bp_a32.preguntar(_prompt_auditor(material_auditor, json.dumps(propuesta, ensure_ascii=False)))
                auditoria = _json_de(_texto_bp2)
                quien_aud = 'bigpickle'
                avisos.extend(_avisos_bp2)
                avisos.append('todas las gratis duermen: revisa bigpickle (A-32)')
            except Exception as e:
                avisos.append('bigpickle no pudo revisar: ' + str(e)[:120])
    # Si no hay auditor, intentar con el cerebro de pago, PERO APARTANDO SIEMPRE AL QUE ESCRIBIO.
    # NADIE REVISA SU PROPIO TRABAJO (Julio, 2026-09-13). Antes aqui no se apartaba a nadie y el que
    # escribio acababa revisandose: medido, 40 de 102 rondas aprobadas en 7 dias, que por ley no se
    # aplican y la ronda siguiente borraba. El intento con el de pago se mantiene (ley de Julio, lo
    # vigila test_vigia_lo_pesado_a_deepseek.py); si no queda nadie distinto, queda SIN_AUDITAR y el
    # trabajo ya esta archivado para revisarlo despues. Lo vigila test_vigia_nadie_revisa_su_propio_trabajo.py
    # SOLO si el encargo NO pidio un revisor fijo (ley de Julio 2026-09-15).
    if (not auditoria or auditoria.get("veredicto") == "SIN_AUDITAR"):
        crudo_a, quien_aud, av_intento = _preguntar_con_relevo(
            _prompt_auditor(material_auditor, json.dumps(propuesta, ensure_ascii=False)), 0.1,
            evitar=evitar, primero=None, pesado=True, clase="auditar", vuelta=3)
        avisos += av_intento
        if crudo_a:
            auditoria = _json_de(crudo_a)

    # Si al final el mismo cerebro escribio y reviso, se avisa.
    if evitar and quien_aud == evitar:
        avisos.append("el mismo cerebro escribio y reviso: hay que comprobarlo con los ojos antes de darlo por bueno")

    return auditoria, quien_aud, avisos

def trabajar(paquete, tarea, generador=None, auditor=None, clase="reparar"):
    """Un cerebro GENERA, OTRO distinto AUDITA (4 ojos). Quien es cada uno lo decide el relevo
    de cuotas, no una lista fija: asi nunca se para el trabajo por una cuota agotada.

    SEGURIDAD (2026-08-24): el que llama a veces manda la CAJA (dict) en vez del texto. Se
    normaliza a texto aqui para que ni el generador, ni el freno, ni el auditor vean basura
    (fallo real: el comando 'equipo' pasaba el dict y se caia tras pagar a DeepSeek).

    CLASE (2026-09-06): "reparar" es lo de siempre (por defecto, nada cambia para quien ya
    llamaba). "crear" le manda al obrero el encargo de ANALISTA, el que sabe escribir un
    documento nuevo entero sin pedir texto viejo. Antes ese encargo existia en _prompt_obrero
    pero era inalcanzable, porque esta firma no tenia por donde recibirlo: pedirle crear un
    archivo nuevo acababa siempre en el encargo de reparar, que exige un texto_viejo que no
    existe, y el obrero se rendia. Quien enciende "crear" es Julio con una marca explicita;
    nunca se adivina de las palabras de la tarea (CONTRATO_CREAR_PIEZA_NUEVA, regla 5: una
    pieza nueva se crea CON AUTORIZACION)."""
    if not isinstance(paquete, str):
        from cerebro import router as _r
        paquete = _r.a_texto(paquete)
    c, _ = prestar_cerebro()
    if not c:
        return {"_error": "NO_ENCONTRADO: no se pudo tomar prestado el cerebro de DMM"}
    if not quienes_hay():
        return {"_error": "NO_ENCONTRADO: no hay llave ni modelo local (revisa el .env de DMM)"}

    # GENERAR SE MIDE, NO SE SUPONE (Julio, 2026-09-09, punto 1 de la auditoria de causa raiz).
    # Antes esto salia de la AUSENCIA de generador: si nadie pedia generador, se daba el encargo
    # por pesado y el de pago entraba EL PRIMERO sin mirar cuanto medía. Eso dejo a los gratis con
    # 0 de 72 trabajos: no es que no aguantaran, es que nunca se les pregunto. Y metia el bloqueo
    # F2 (pesado + sin DeepSeek) en el caso NORMAL, donde nadie habia pedido nada pesado.
    # Ahora lo unico que enciende el pesado aqui es que el que llama haya pedido DE VERDAD un
    # generador de pago. Si no pidio nada, o pidio uno gratis, queda apagado y el tamano real lo
    # mide `cuotas.rankear` dentro del relevo, que ademas salta a quien no aguanta. Lo que de
    # verdad no le quepa a ningun gratis sigue cayendo en el de pago.
    pesado_ahora = bool(generador) and generador in cuotas.DE_PAGO
    avisos_totales = []
    motivos_rechazo = []
    vueltas = 0
    propuesta = {}
    auditoria = {}
    quien_aud = None
    for _vuelta in range(4):
        vueltas += 1
        encargo = tarea
        if motivos_rechazo:
            encargo = ("Este trabajo ya se rechazo antes, y estos fueron los motivos:\n" +
                       "\n".join(motivos_rechazo) +
                       "\nArregla todos esos motivos y no repitas el mismo fallo.\n" + tarea)
        # AL OBRERO SOLO LE LLEGA LO SUYO (Julio, 2026-09-10). Antes le llegaba el bulto entero
        # y el gratis cortaba la respuesta a la mitad. El filtro le deja la ley, los trozos del
        # archivo que la tarea nombra (si lo nombra) y quien puede danar.
        _archivo_tarea = None
        _encontrados = re.findall(r"[\w./\\]*(?:\.py|\.md)\b", str(tarea))
        _vistos = []
        for _n in _encontrados:
            _n = _n.strip()
            if _n and _n not in _vistos:
                _vistos.append(_n)
        if _vistos:
            _archivo_tarea = _vistos
        material_obrero = _filtrar_paquete(paquete, archivo=_archivo_tarea,
                                       tope=(min(max(cuotas._capacidad(generador), TOPE_GRATIS), 40000) if generador else TOPE_GRATIS) - 2690)
        crudo, quien_gen, av1 = _preguntar_con_relevo(_prompt_obrero(material_obrero, encargo, clase), 0.2,
                                                      pesado=pesado_ahora, primero=generador,
                                                      clase=clase, vuelta=_vuelta + 1)
        avisos_totales += av1
        if not crudo:
            return {"_error": "; ".join(avisos_totales)}
        propuesta = _json_de(crudo)
        cumple, falta = _propuesta_cumple(propuesta, clase)
        if not cumple:
            # PROGRAMA (no IA): el pedido llego incompleto. No se gasta en auditor ni se deja
            # morir DUDOSO: se anota en el cuaderno, se guarda el motivo y se reintenta. Si se
            # agotan las vueltas, el bucle cae al ultimo recurso con el cerebro de pago.
            cuaderno.apuntar(quien_gen, tamano=len(crudo or ""), vuelta=_vuelta + 1, clase=clase,
                             resultado=cuaderno.VACIO, crudo=(crudo or "")[:120])
            motivos_rechazo.append(falta)
            avisos_totales.append(f"{cuotas.APODO.get(quien_gen, quien_gen)} dejo el pedido a mitad "
                                  f"({falta}) -> se reintenta")
            if _vuelta + 1 >= 3:
                # LEY (CONTRATO_EL_EQUIPO_ESCRIBE, regla 1): el de pago entra SIEMPRE que el
                # gratis falle. Si el gratis dejo el pedido a mitad 3 veces, el de pago lo escribe
                # entero. Sin esto, el trabajo moria "DUDOSO" sin llamarlo (fallo real 2026-09-10).
                pesado_ahora = True
            continue
        inventados = _validar_en_paquete(paquete, propuesta, tarea)
        # Si el obrero dijo NO_ENCONTRADO y PREGUNTA_REQUERIDA, es falta de material, no invento.
        # Eso sale como PREGUNTA al que reparte, no como rechazo.
        if inventados and not ("NO_ENCONTRADO" in str(propuesta) and "PREGUNTA_REQUERIDA" in str(propuesta)):
            propuesta["_fuera_del_paquete"] = inventados   # marco: no se deja pasar como valido

        # Si se pidio un generador y contesto otro, se avisa. Nunca en silencio.
        if generador and quien_gen != generador:
            avisos_totales.append("se pidio generar a %s y no esta disponible: contesto %s" % (generador, quien_gen))

        # La revision se delega entera a auditar(): asi arnes/copista.py puede pedir SOLO una
        # revision (un cambio gratis ya aplicado) y no hay el mismo codigo en dos sitios.
        # Dentro de auditar() siguen vivos la cura de los dos reintentos del 2026-08-31 y el
        # ultimo recurso con el cerebro de pago: no se quito nada, solo se movio.
        auditoria, quien_aud, av2 = auditar(paquete, propuesta, auditor=auditor, evitar=quien_gen)
        avisos_totales += av2

        # Si el veredicto es RECHAZADO, guardar motivos y reintentar (hasta 3 veces).
        if isinstance(auditoria, dict) and auditoria.get("veredicto") == "RECHAZADO":
            motivo = auditoria.get("motivo", "") or auditoria.get("resumen_para_el_jefe", "")
            if motivo:
                motivos_rechazo.append(motivo)
            continue
        # Si APROBADO o SIN_AUDITAR, salir del bucle.
        break

    avisos_totales.append("vueltas_dadas: %d" % vueltas)
    return {"obrero": quien_gen, "auditor": quien_aud or "(ninguno)",
            "propuesta": propuesta, "auditoria": auditoria,
            "avisos": avisos_totales}


def veredicto_corto(r):
    """Lo UNICO que deberia leer Claude. Pocas lineas."""
    if "_error" in r:
        return f"NO SE PUDO: {r['_error']}"
    p, a = r.get("propuesta", {}), r.get("auditoria", {})
    L = [f"OBRERO {r['obrero']} -> AUDITOR {r['auditor']}"]
    # OJO: no llamar 'a' a esto. Antes se llamaba 'a' y PISABA la auditoria de arriba, asi que
    # leer el veredicto reventaba justo cuando habia avisos, que es cuando mas falta hace leerlo.
    for aviso in (r.get("avisos") or [])[:3]:
        L.append(f"  aviso       : {aviso}")
    if "_error" in p:
        L.append(f"  propuesta ILEGIBLE: {p['_error']}")
        return "\n".join(L)
    L.append(f"  diagnostico : {p.get('diagnostico', '?')}")
    L.append(f"  toca        : {p.get('archivo', '?')} funcion {p.get('funcion', '?')}")
    L.append(f"  confianza   : {p.get('confianza', '?')}")
    if p.get("preguntas"):
        L.append(f"  PREGUNTA_REQUERIDA: {'; '.join(p['preguntas'])}")
    v = a.get("veredicto", "?")
    L.append(f"  VEREDICTO   : {v}")
    if a.get("invento_algo"):
        L.append(f"  *** INVENTO: {'; '.join(a.get('que_invento', []))} -> SE DESCARTA")
    for f in (a.get("fallos") or [])[:4]:
        L.append(f"  fallo       : {f}")
    if a.get("resumen_para_el_jefe"):
        L.append(f"  resumen     : {a['resumen_para_el_jefe']}")
    return "\n".join(L)
