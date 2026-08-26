# -*- coding: utf-8 -*-
"""arnes/diccionario.py — DE LAS PALABRAS DE JULIO AL SITIO DEL CODIGO.

EL PROBLEMA, medido el 2026-08-25: se le pidio al repartidor el material para "al arrancar no se
piden los informes diarios y la lista sale vacia". Devolvio TRES pedazos y los tres eran vigias
recien escritas; del programa, CERO. Y no es que busque mal: Julio habla en espanol y de negocio,
el codigo esta en ingles y comprimido en lineas larguisimas. **Nunca se van a parecer**, por mucho
que se afine la busqueda por palabras.

LA IDEA: cada vez que se declara una causa, el sistema YA obliga a escribir el problema en
palabras de Julio Y el archivo, la funcion y la linea exactos, con evidencia medida. **Esa pareja
ya existe y ya esta probada.** El diccionario se cosecha de ahi: no hay que sentarse a
escribirlo, se llena solo con el trabajo del dia, y solo guarda parejas DEMOSTRADAS.

LO QUE NO ES: no adivina, no traduce por parecido de idioma, no inventa. Si algo no se ha
reparado nunca, aqui no esta, y decirlo es la respuesta correcta.

REPARTO CON CLINE (2026-08-25): Claude hace el diccionario; Cline lo conecta al repartidor con su
vigia de uso. Su correccion, aceptada entera: un diccionario que sea solo un documento acaba
siendo papel viejo. Tiene que consumirlo el router.
"""
import json
import os
import re
import unicodedata
from datetime import datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "DICCIONARIO.json")

# Palabras que no distinguen nada: si se cuentan, todo se parece a todo.
RUIDO = {"el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "al", "a", "en",
         "y", "o", "que", "se", "no", "si", "con", "por", "para", "es", "esta", "estan", "ser",
         "lo", "le", "su", "sus", "me", "mi", "te", "tu", "hay", "ha", "han", "pero", "como",
         "cuando", "donde", "porque", "mas", "muy", "ya", "todo", "todos", "toda", "todas"}

# CUANDO SE CONSIDERA QUE HABLA DE LO MISMO — y por que asi (2026-08-25).
# Medido con la vigia: Julio dice "al arrancar no se piden los informes diarios y la lista sale
# vacia" y luego "los informes no cargan al abrir el programa". Para una persona es lo MISMO.
# Por palabras comparten UNA de diez. Exigir un parecido alto es exigir que Julio repita el
# problema con las mismas palabras, y eso no pasa nunca.
#
# LA REGLA, dicha en simple: **comparten al menos una palabra que distingue.**
# "informes" distingue; "el", "la", "que" no (por eso estan en RUIDO).
#
# EL LIMITE, dicho sin adornos: esto NO entiende el significado. Si Julio describe el mismo
# problema SIN repetir ni una palabra que distinga, no lo va a encontrar. Eso se cura de verdad
# con el repartidor que pidio Julio, no aqui.
# Lo que si hace: APRENDER. Cada vez que el mismo sitio se declara con palabras nuevas, esas
# palabras se suman a esa pareja. Asi mejora con el uso en vez de quedarse quieto.
MINIMO_PALABRAS_COMPARTIDAS = 1


def _sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


def _palabras(texto):
    """Las palabras que de verdad distinguen. Julio escribe 'economico' y el codigo 'económico'."""
    t = _sin_tildes(str(texto or "").lower())
    return {p for p in re.findall(r"[a-z0-9]{3,}", t) if p not in RUIDO}


def _leer():
    try:
        with open(RUTA, encoding="utf-8-sig") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _guardar(parejas):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(parejas, f, ensure_ascii=False, indent=1)


def aprender(problema, archivo, funcion, linea, proyecto=""):
    """Guarda una pareja PROBADA: lo que dijo Julio <-> el sitio exacto del codigo.

    Se llama al declarar una causa raiz, que es el unico sitio donde el sistema ya exige las dos
    mitades con evidencia. Sin sitio probado no se guarda nada: una suposicion aqui envenenaria
    al repartidor, que es justo lo que se quiere arreglar.
    """
    problema = str(problema or "").strip()
    archivo = str(archivo or "").strip()
    funcion = str(funcion or "").strip()
    if not problema or not archivo or not funcion:
        return False
    if not _palabras(problema):
        return False

    parejas = _leer()
    for p in parejas:
        if p.get("archivo") != archivo or p.get("funcion") != funcion:
            continue
        # El MISMO sitio, ya conocido. Se refresca y, si Julio lo dijo con OTRAS palabras, esas
        # palabras se suman: asi el diccionario aprende su forma de hablar en vez de exigir que
        # repita la frase exacta. Es lo unico que lo hace mejorar con el uso.
        p["cuando"] = datetime.now().timestamp()
        p["veces"] = int(p.get("veces", 1)) + 1
        if problema != p.get("problema"):
            dichos = p.setdefault("tambien_dicho", [])
            if problema not in dichos:
                dichos.append(problema)
        _guardar(parejas)
        return True

    parejas.append({"problema": problema, "archivo": archivo, "funcion": funcion,
                    "linea": str(linea or ""), "proyecto": str(proyecto or ""),
                    "cuando": datetime.now().timestamp(), "veces": 1})
    _guardar(parejas)
    return True


def buscar(problema, proyecto=""):
    """Los sitios del codigo que ya se demostraron para un problema PARECIDO a este.

    Lo mas reciente primero: si el mismo problema se reparo en dos sitios, el ultimo manda.
    Devuelve vacio si no se parece a nada aprendido — callar es la respuesta correcta.
    """
    quiere = _palabras(problema)
    if not quiere:
        return []

    salen = []
    for p in _leer():
        if proyecto and p.get("proyecto") and p["proyecto"] != proyecto:
            continue
        # Todas las formas en que Julio ha descrito ESTE mismo sitio, no solo la ultima.
        tiene = _palabras(p.get("problema"))
        for otra in (p.get("tambien_dicho") or []):
            tiene |= _palabras(otra)
        if not tiene:
            continue
        comunes = quiere & tiene
        if len(comunes) < MINIMO_PALABRAS_COMPARTIDAS:
            continue
        # Se ordena por cuanto se parece, pero el corte ya lo decidio compartir una palabra que
        # distingue. Asi Julio puede decirlo con otras palabras y aun asi encontrarlo.
        parecido = len(comunes) / float(min(len(quiere), len(tiene)))
        salen.append((parecido, p.get("cuando", 0), p))

    salen.sort(key=lambda x: (-x[1], -x[0]))     # lo mas reciente manda, luego lo mas parecido
    return [p for _, _, p in salen]


def todo():
    """Todas las parejas aprendidas."""
    return _leer()


def texto(sitios):
    """Como se le cuenta a Julio, sin jerga."""
    if not sitios:
        return ""
    lineas = ["ESTO YA SE REPARO ANTES, y aqui esta donde:"]
    for s in sitios[:3]:
        lineas.append("  · %s (%s, linea %s) — cuando pasaba: %s"
                      % (s.get("archivo"), s.get("funcion"), s.get("linea"),
                         str(s.get("problema"))[:70]))
    return "\n".join(lineas)
