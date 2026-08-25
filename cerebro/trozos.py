# -*- coding: utf-8 -*-
"""cerebro/trozos.py — CAPA 3 del cerebro: los TROZOS (el "chunk").

Aqui esta la economia de verdad. Una pieza puede tener 10.818 lineas (app.py de Foto Informe).
Nadie necesita esas 10.818: necesita 40. Esta capa corta la pieza en trozos y sabe cual trozo
responde al problema, con su LINEA EXACTA.

Mejora sobre `cuerpo/indice.py` de DMM (de donde viene la idea): alli el trozo se corta por
caracteres y se devuelve como `archivo#3`, que no le sirve a nadie para ir a mirar. Aqui el
trozo se corta por LINEAS y se devuelve como `archivo:340-380`, que es una direccion real.

Sin llaves, sin internet, sin costo: cuenta palabras (la misma idea de BolsaDePalabras de DMM).
"""
import re, math
from collections import Counter, defaultdict

TAM = 40          # lineas por trozo
SOLAPE = 8        # lineas repetidas entre trozo y trozo (para no cortar una funcion en seco)

# Cuanto pesa un pedazo que viene de una PRUEBA (vigia, prueba real, sonda de aislar).
# No es cero: una prueba dice que ya se probo y como, y eso es contexto util. Pero no puede
# ganarle al codigo, porque las pruebas llevan el problema de Julio COPIADO en su cabecera y
# entonces se llevan el paquete entero. Ver `_es_prueba` y el fallo del 2026-08-25.
_PESO_PRUEBA = 0.25


def _es_prueba(pieza):
    """¿Este pedazo viene de una prueba, y no del programa?"""
    n = str(pieza or "").replace("\\", "/").lower()
    base = n.rsplit("/", 1)[-1]
    return ("/vigias/" in n or base.startswith("test_") or base.endswith("_test.py")
            or base.startswith("rv3_vigia") or base.startswith("rv3_prueba")
            or base.startswith("rv3_aislar"))
RUIDO = {"the", "and", "for", "que", "con", "por", "los", "las", "del", "una", "self",
         "import", "from", "return", "def", "class", "if", "else", "not", "none", "true", "false"}


# Tabla para quitar tildes. Julio escribe "economico" y el codigo dice "económico": si no se
# igualan, NUNCA coinciden. Fallo real 2026-08-20: `medidor.py`, cuyo titulo literal es
# "MEDIDOR de tokens del CICLO ECONOMICO", salia NO_ENCONTRADO al buscar justo esas palabras.
# Esto degradaba TODO el grafo en silencio, no solo una busqueda.
_TILDES = str.maketrans('áéíóúüàèìòùâêîôûäëïöñç', 'aeiouuaeiouaeiouaeionc')


def _sin_tildes(t):
    return t.translate(_TILDES)


def _palabras(txt):
    return [w for w in re.findall('[a-záéíóúüàèìòùâêîôûäëïöñç_]{3,}', _sin_tildes(txt.lower()))
            if w not in RUIDO]


def cortar(texto, tam=TAM, solape=SOLAPE):
    """Parte en trozos con solape. Devuelve [{desde, hasta, texto}] con lineas 1-indexadas."""
    lineas = texto.splitlines()
    if not lineas:
        return []
    out, i = [], 0
    paso = max(1, tam - solape)
    while i < len(lineas):
        bloque = lineas[i:i + tam]
        out.append({"desde": i + 1, "hasta": min(i + tam, len(lineas)), "texto": "\n".join(bloque)})
        if i + tam >= len(lineas):
            break
        i += paso
    return out


def _leer(abs_path):
    try:
        with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


class Buscador:
    """Indexa los trozos de unas piezas y trae los k que responden al problema.
    Usa TF-IDF simple: premia la palabra rara (la que de verdad distingue) y castiga la comun."""

    def __init__(self, fichas):
        self.trozos = []
        for f in fichas:
            txt = _leer(f["abs"])
            if not txt:
                continue
            for t in cortar(txt):
                self.trozos.append({
                    "pieza": f["id"], "abs": f["abs"], "rol": f["rol"],
                    "desde": t["desde"], "hasta": t["hasta"], "texto": t["texto"],
                    "bolsa": Counter(_palabras(t["texto"])),
                })
        # cuantos trozos contienen cada palabra (para saber cuales son raras)
        self.docs = len(self.trozos) or 1
        self.en_cuantos = defaultdict(int)
        for t in self.trozos:
            for w in t["bolsa"]:
                self.en_cuantos[w] += 1

    COMUNES = {"mandar", "crear", "hacer", "leer", "poner", "sacar", "generar", "usar", "para",
               "mensaje", "mensajes", "archivo", "archivos", "datos", "codigo", "canal", "canales",
               "sistema", "cuando", "quiere", "quiero", "color", "boton", "cosa", "algo", "esta",
               "este", "como", "donde", "porque", "cual", "cuales", "hace", "sobre", "todo"}

    def buscar_estricto(self, consulta, k=6, minimo=5.0):
        """Como buscar(), pero SOLO devuelve algo si aparece la palabra que de verdad distingue
        la consulta. Si esa palabra no esta en ningun trozo, devuelve VACIO.

        Existe por un fallo que ya se cometio DOS veces (2026-08-20):
          · el buscador de habilidades decia "ya lo escribiste" sobre cosas que Julio nunca hizo
          · el buscador de dudas decia "RESUELTA" sobre algo que no estaba escrito en ningun sitio
        Las dos veces la causa fue la misma: cualquier texto "se parece" si no se exige la palabra
        clave. Decir que se tiene la respuesta sin tenerla es peor que no responder.
        """
        # Las claves salen de la MISMA funcion que indexa (`_palabras`). Si se filtran a mano,
        # entran palabras que el indice nunca guardo ("del", "un", "que"): su cuenta es 0, parecen
        # rarisimas, ganan como "la mas distintiva" y tumban la busqueda entera.
        # Fallo real 2026-08-20, cometido DOS veces: primero con "un", luego con "del", que hizo
        # que `medidor.py` —cuyo titulo literal es "MEDIDOR de tokens"— saliera NO_ENCONTRADO.
        claves = [w for w in _palabras(consulta) if w not in self.COMUNES]
        if not claves:
            return []                     # nada que distinga -> no se afirma nada
        raras = sorted(claves, key=lambda w: self.en_cuantos.get(w, 0))[:1]
        if self.en_cuantos.get(raras[0], 0) == 0:
            return []                     # la palabra clave no aparece: NO esta escrito aqui
        return [r for r in self.buscar(consulta, k=k, exigir=raras) if r["puntaje"] >= minimo]

    def buscar(self, consulta, k=6, solo_piezas=None, exigir=None):
        """exigir = palabras del ASUNTO (el flujo). Si se pasan, el trozo que no hable del
        asunto se descarta aunque comparta palabras sueltas. Sin esto, buscar "no persiste la
        plantilla al cambiar de SESION" traia el login (por la palabra sesion). Caso real."""
        q = _palabras(consulta)
        if not q:
            return []
        res = []
        for t in self.trozos:
            if solo_piezas and t["pieza"] not in solo_piezas:
                continue
            if exigir and not any(_sin_tildes(e.lower()) in _sin_tildes(t["texto"].lower())
                                  for e in exigir):
                continue
            p = 0.0
            for w in q:
                c = t["bolsa"].get(w, 0)
                if c:
                    idf = math.log(self.docs / (1 + self.en_cuantos[w]))
                    p += (1 + math.log(c)) * max(idf, 0.1)
            if p > 0:
                # UNA PRUEBA QUE DESCRIBE UN FALLO NO ES DONDE VIVE EL FALLO (2026-08-25).
                # Julio lo cazo con una pregunta: "¿y por que vas a tocar 16 mil lineas? si ese
                # no es el contrato, solo un pedazo". Tenia razon: hacian falta ~10 lineas del
                # programa. Pero el paquete traia TRES pedazos y los tres eran de las vigias
                # recien escritas, que llevan el problema de Julio COPIADO en su cabecera y por
                # eso ganaban siempre. El repartidor se devolvia su propio texto y el codigo no
                # aparecia; sin el codigo delante, el candado de equipo no abria el archivo y la
                # reparacion de una sola linea quedaba bloqueada.
                # No se les echa: siguen entrando como contexto (dicen que ya se probo y como).
                # Solo dejan de TAPAR al codigo.
                p *= _PESO_PRUEBA if _es_prueba(t["pieza"]) else 1.0
                res.append((p, t))
        res.sort(key=lambda x: -x[0])
        vistos, out = set(), []
        for p, t in res:
            # no traer dos trozos pegados de la misma pieza: aburre y encarece
            clave = (t["pieza"], t["desde"] // 100)
            if clave in vistos:
                continue
            vistos.add(clave)
            out.append({"pieza": t["pieza"], "desde": t["desde"], "hasta": t["hasta"],
                        "puntaje": round(p, 2), "texto": t["texto"], "rol": t["rol"],
                        "direccion": f"{t['pieza']}:{t['desde']}-{t['hasta']}"})
            if len(out) >= k:
                break
        return out
