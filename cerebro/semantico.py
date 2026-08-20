# -*- coding: utf-8 -*-
"""cerebro/semantico.py — BUSCAR POR SIGNIFICADO, NO POR LETRAS (orden 4 de Julio, 2026-08-20).

EL PROBLEMA QUE RESUELVE: contar palabras no entiende sinonimos. Si el contrato dice "perfil" y
el codigo dice "onboarding", o Julio escribe "no guarda" y el codigo dice "no persiste", el
buscador de letras no los une. Y ese fue justo el fallo del 2026-08-20: el paquete traia el
motor y no la pantalla.

MEDIDO ESE DIA, con dos frases que dicen lo mismo con otras palabras contra una que no tiene
nada que ver:
    LM Studio (nomic-embed local) ... diferencia 0.022  -> NO distingue. No sirve.
    gemini-embedding-001 .......... diferencia 0.202  -> SI distingue. Este es.

DECISION IMPORTANTE — no se indexa el proyecto entero:
Embeber los ~600 trozos de un proyecto costaria 600 llamadas y una espera larga. En vez de eso
se usa como **re-ordenador**: el buscador de palabras (gratis, instantaneo) trae 12 candidatos,
y solo esos 12 se pasan por el significado. Cuesta 1 llamada por consulta en vez de 600, y el
resultado es el mismo, porque lo que importa es el ORDEN de los primeros.

Si no hay llave, no hay cuota o falla: se devuelve el orden del buscador de palabras.
**Nunca deja al Ingeniero sin buscador.**
"""
import os, sys, json, math, hashlib, urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(AQUI, "memoria", "significados.json")
MODELO = "gemini-embedding-001"
TOPE_TEXTO = 1800          # letras por texto: mas no aporta y tarda mas


def _llave():
    try:
        sys.path.insert(0, AQUI)
        from cuerpo import obrero
        obrero.prestar_cerebro()          # carga el .env de DMM sin duplicar nada
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


def hay():
    return bool(_llave())


def _cache_leer():
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except Exception:
        return {}


def _cache_guardar(d):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    # se guardan como cadenas cortas para que el archivo no se dispare
    json.dump(d, open(CACHE, "w", encoding="utf-8"))


def _clave(t):
    return hashlib.md5(t[:TOPE_TEXTO].encode("utf-8", "ignore")).hexdigest()


def vector(texto, cache=None):
    """El significado de un texto, como lista de numeros. Se cachea: nunca se paga dos veces."""
    c = cache if cache is not None else _cache_leer()
    k = _clave(texto)
    if k in c:
        return c[k]
    llave = _llave()
    if not llave:
        return None
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           + MODELO + ":embedContent?key=" + llave)
    datos = json.dumps({"content": {"parts": [{"text": texto[:TOPE_TEXTO]}]}}).encode("utf-8")
    req = urllib.request.Request(url, data=datos, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            v = json.load(r)["embedding"]["values"]
    except Exception:
        return None
    c[k] = v
    if cache is None:
        _cache_guardar(c)
    return v


def parecido(a, b):
    if not a or not b:
        return 0.0
    s = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return s / (na * nb) if na and nb else 0.0


def reordenar(consulta, candidatos, campo="texto", k=None):
    """Reordena por SIGNIFICADO los candidatos que ya trajo el buscador de palabras.

    Devuelve la lista reordenada. Si no se puede (sin llave, sin cuota, sin internet),
    devuelve la lista TAL CUAL: el Ingeniero nunca se queda sin buscador.
    """
    if not candidatos or not hay():
        return candidatos
    cache = _cache_leer()
    vq = vector(consulta, cache)
    if not vq:
        return candidatos
    con_nota = []
    for c in candidatos:
        v = vector(str(c.get(campo, ""))[:TOPE_TEXTO], cache)
        nota = parecido(vq, v) if v else 0.0
        c = dict(c)
        c["significado"] = round(nota, 3)
        con_nota.append(c)
    _cache_guardar(cache)
    con_nota.sort(key=lambda x: -x["significado"])
    return con_nota[:k] if k else con_nota


def texto_estado():
    c = _cache_leer()
    return ("BUSQUEDA POR SIGNIFICADO: " +
            ("activa (" + MODELO + ")" if hay() else "APAGADA (no hay llave de Gemini)") +
            "\n  significados guardados: %d (no se vuelven a pagar)" % len(c))
