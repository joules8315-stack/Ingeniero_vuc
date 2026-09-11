# -*- coding: utf-8 -*-
"""skills/nace_conectada.py — CUENTA PURA, CERO IA.

Cuenta, para cada pieza de codigo de la casa, cuantas veces la llama DE VERDAD el resto,
y lista las que no llama nadie (huerfanas).

POR QUE: Julio lleva pidiendo que nada quede huerfano y siguen saliendo huerfanos.
El motivo es que ESTE CONTADOR NO EXISTIA: se diseño el 2026-09-08, se rechazo por un
falso invento y nunca se construyo. El contador de huerfanas era el primer huerfano.

NO OPINA: cuenta y lista, no decide si la pieza debe existir.
"""
import os
import re
import json
import sys

# AQUI = la carpeta del Ingeniero (dos niveles arriba del archivo).
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CARPETAS = skills, arnes, cuerpo, cerebro, mapa, web. De ahi salen las piezas:
# todo .py que no empiece por doble guion bajo.
CARPETAS = ["skills", "arnes", "cuerpo", "cerebro", "mapa", "web"]

# FUERA = vigias, __pycache__, .git, memoria, node_modules, docs_build, .venv.
# Esas carpetas NO cuentan como llamadores: las vigias son pruebas, no uso.
FUERA = {"vigias", "__pycache__", ".git", "memoria", "node_modules", "docs_build", ".venv"}


def sin_texto_muerto(codigo):
    """Quita los textos entre triples comillas de los dos tipos y todo lo que va
    detras de una almohadilla en cada linea. Es la clave: sin esto una mencion en
    un comentario contaria como llamada."""
    # Quitar textos entre triples comillas dobles
    codigo = re.sub(r'"""(?:[^"\\]|\\.)*?"""', '', codigo, flags=re.S)
    # Quitar textos entre triples comillas simples
    codigo = re.sub(r"'''(?:[^'\\]|\\.)*?'''", '', codigo, flags=re.S)
    # Quitar comentarios de linea (todo lo que va detras de una almohadilla)
    lineas = []
    for linea in codigo.splitlines():
        # Buscar la primera almohadilla que no este dentro de una cadena
        # (aproximacion simple: no se manejan cadenas con # dentro)
        idx = linea.find('#')
        if idx != -1:
            linea = linea[:idx]
        lineas.append(linea)
    return '\n'.join(lineas)


def enganchados_en_la_configuracion():
    """Lee los dos archivos settings.json (el del usuario en su carpeta .claude y
    el del proyecto) y saca con una expresion regular todos los nombres que acaban
    en .py. Devuelve un conjunto. Sirve para no contar como huerfanos a los
    candados: no se llaman desde el codigo, los lanza la configuracion."""
    enganchados = set()
    # settings.json del usuario en su carpeta .claude
    rutas = [
        os.path.expanduser("~/.claude/settings.json"),
        # LA CONFIGURACION DEL PROYECTO VIVE DENTRO DE .claude (Julio, 2026-09-09).
        # Segundo fallo del contador cazado el mismo dia: buscaba settings.json en la raiz,
        # y ahi no esta. Por eso daba por huerfanos a candados del proyecto que frenan cada
        # dia, como el de comunicacion. Un contador que miente manda a reparar lo sano.
        os.path.join(AQUI, ".claude", "settings.json"),
        os.path.join(AQUI, "settings.json"),
    ]
    for ruta in rutas:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            # Buscar todos los nombres que acaban en .py
            # SE GUARDA SOLO EL NOMBRE, SIN RUTA NI EXTENSION (Julio, 2026-09-09).
            # Fallo cazado el mismo dia de construirlo: se guardaba la ruta entera
            # ("C:/Ingeniero_VUC/arnes/candado_comunicacion.py") y despues se comparaba con el
            # nombre pelado ("candado_comunicacion"). Nunca cuadraba, asi que daba por
            # huerfanos a candados que estan enganchados y que frenan todos los dias.
            # Un contador que miente manda a reparar lo que no esta roto.
            for _crudo in re.findall(r"[\w./\\-]+\.py", contenido):
                nombre = os.path.basename(_crudo.replace("\\", "/"))[:-3]
                # Normalizar a nombre de archivo simple
                enganchados.add(os.path.basename(nombre))
        except FileNotFoundError:
            pass
    return enganchados


def llamadas_a(nombre, textos, raiz):
    """Devuelve las rutas relativas donde aparece alguno de estos patrones:
    import <nombre>, from <nombre> import, import algo.<nombre>,
    from algo import ... <nombre>, <nombre> seguido de punto, o <nombre>.py"""
    sitios = []
    # Patrones a buscar
    patrones = [
        re.compile(r"\bimport\s+" + re.escape(nombre) + r"\b"),
        re.compile(r"\bfrom\s+" + re.escape(nombre) + r"\s+import\b"),
        re.compile(r"\bimport\s+[\w.]+\s*\s*\.\s*" + re.escape(nombre) + r"\b"),
        re.compile(r"\bfrom\s+[\w.]+\s+import\s+[^\n]*\b" + re.escape(nombre) + r"\b"),
        # CUARTO FALLO cazado el 2026-09-11 ayudando al DMM (Asesor Marketing): el contador no veia
        # el enchufe con punto DENTRO del from ("from cuerpo.dashboard import leer_dashboard").
        # Decia huerfana a dashboard, meta_oauth, orquestador, rag, embeddings, indice_semantico y
        # redes_mock, que SI estan llamandose desde web/servidor.py. Un contador que manda a reparar
        # lo que ya esta enchufado es peor que no tenerlo: crear una ruta nueva para conseguir que
        # el numero baje es inventar trabajo, y es justo lo que la ley prohibe.
        re.compile(r"\bfrom\s+[\w.]+\s*\.\s*" + re.escape(nombre) + r"\s+import\b"),
        re.compile(r"\b" + re.escape(nombre) + r"\s*\."),
        re.compile(r"\b" + re.escape(nombre) + r"\.py\b"),
    ]
    for ruta_rel, texto in textos.items():
        # Un archivo que se nombra a si mismo no cuenta
        if os.path.basename(ruta_rel) == nombre + ".py":
            continue
        for patron in patrones:
            if patron.search(texto):
                sitios.append(ruta_rel)
                break
    return sitios


def revisar(solo=None, raiz=None):
    """Lee todos los archivos pasandolos por sin_texto_muerto y para cada pieza
    devuelve un diccionario con pieza, ruta, llamadas (los sitios mas uno si es
    candado), candado (verdadero o falso) y sitios (los 4 primeros). Un archivo
    que se nombra a si mismo no cuenta. Ordenado por llamadas de menor a mayor."""
    if raiz is None:
        raiz = AQUI
    # Recoger todas las piezas (archivos .py en las carpetas permitidas)
    piezas = {}
    for carpeta in CARPETAS:
        ruta_carpeta = os.path.join(raiz, carpeta)
        if not os.path.isdir(ruta_carpeta):
            continue
        for nombre_archivo in os.listdir(ruta_carpeta):
            if nombre_archivo.endswith(".py") and not nombre_archivo.startswith("__"):
                ruta_abs = os.path.join(ruta_carpeta, nombre_archivo)
                ruta_rel = os.path.relpath(ruta_abs, raiz)
                piezas[nombre_archivo[:-3]] = ruta_rel
    # Leer todos los archivos de las carpetas permitidas, excluyendo las de FUERA
    textos = {}
    # Y EL ARCHIVO PRINCIPAL DE LA RAIZ, QUE SE ESTABA SALTANDO (Julio, 2026-09-09).
    # Fallo real cazado el mismo dia de construirlo: el contador solo miraba DENTRO de las
    # carpetas, y el mando principal (ingeniero.py) vive en la raiz. Desde ahi se llama a
    # media casa. Resultado: decia que cuerpo/aplicador.py no lo llamaba nadie cuando se le
    # llama en cuatro sitios de ese archivo. Un contador que miente es peor que no tenerlo:
    # manda a reparar lo que no esta roto.
    for suelto in sorted(os.listdir(raiz)):
        if suelto.endswith(".py") and not suelto.startswith("__"):
            try:
                with open(os.path.join(raiz, suelto), "r", encoding="utf-8") as f:
                    textos[suelto] = sin_texto_muerto(f.read())
            except Exception:
                pass
    for carpeta in CARPETAS:
        ruta_carpeta = os.path.join(raiz, carpeta)
        if not os.path.isdir(ruta_carpeta):
            continue
        for raiz_dir, dirs, archivos in os.walk(ruta_carpeta):
            # Excluir carpetas de FUERA
            dirs[:] = [d for d in dirs if d not in FUERA]
            for nombre_archivo in archivos:
                if nombre_archivo.endswith(".py"):
                    ruta_abs = os.path.join(raiz_dir, nombre_archivo)
                    ruta_rel = os.path.relpath(ruta_abs, raiz)
                    try:
                        with open(ruta_abs, "r", encoding="utf-8") as f:
                            codigo = f.read()
                        textos[ruta_rel] = sin_texto_muerto(codigo)
                    except Exception:
                        pass
    # Obtener los candados de la configuracion
    candados = enganchados_en_la_configuracion()
    # Calcular llamadas para cada pieza
    resultados = []
    for pieza, ruta in piezas.items():
        if solo and pieza != solo:
            continue
        sitios = llamadas_a(pieza, textos, raiz)
        # SE COMPARA SIN EXTENSION (Julio, 2026-09-09). Tercer y ultimo fallo del contador
        # cazado el mismo dia: arriba ya se guardan los nombres pelados, y aqui se les volvia
        # a pegar el ".py" para comparar. Nunca cuadraba, y por eso salia "0 son candados"
        # teniendo 26 enganchados. Los tres fallos eran del mismo tipo: comparar dos cosas
        # escritas de forma distinta y dar por bueno el resultado.
        es_candado = pieza in candados
        num_llamadas = len(sitios) + (1 if es_candado else 0)
        resultados.append({
            "pieza": pieza,
            "ruta": ruta,
            "llamadas": num_llamadas,
            "candado": es_candado,
            "sitios": sitios[:4],
        })
    # Ordenar por llamadas de menor a mayor
    resultados.sort(key=lambda x: x["llamadas"])
    return resultados


def huerfanas(raiz=None):
    """Solo las que tienen cero llamadas."""
    return [r for r in revisar(raiz=raiz) if r["llamadas"] == 0]


def informe(r=None):
    """Texto simple que dice cuantas huerfanas hay de cuantas piezas, las lista
    con 0 llamadas <ruta>, avisa de que cada huerfana es TRABAJO SIN TERMINAR y de
    que crear y enganchar son UN SOLO trabajo, y al final cuantas conectadas y
    cuantas de ellas son candados."""
    if r is None:
        r = revisar()
    huerfanas_lista = [x for x in r if x["llamadas"] == 0]
    conectadas = [x for x in r if x["llamadas"] > 0]
    candados_conectados = [x for x in conectadas if x["candado"]]
    lineas = []
    lineas.append(f"HUERFANAS: {len(huerfanas_lista)} de {len(r)} piezas")
    for h in huerfanas_lista:
        lineas.append(f"  0 llamadas {h['ruta']}")
    if huerfanas_lista:
        lineas.append("")
        lineas.append("CADA HUERFANA ES TRABAJO SIN TERMINAR.")
        lineas.append("CREAR Y ENGANCHAR SON UN SOLO TRABAJO.")
    lineas.append("")
    lineas.append(f"CONECTADAS: {len(conectadas)} ({len(candados_conectados)} son candados)")
    return "\n".join(lineas)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Contador de piezas huerfanas")
    parser.add_argument("--raiz", type=str, default=None, help="Carpeta del proyecto a revisar")
    parser.add_argument("pieza", nargs="?", default=None, help="Nombre de la pieza a filtrar")
    args = parser.parse_args()
    raiz = args.raiz if args.raiz else AQUI
    if args.pieza:
        resultados = revisar(solo=args.pieza, raiz=raiz)
        if not resultados:
            print(f"NO_ENCONTRADO: pieza {args.pieza}")
        else:
            res = resultados[0]
            if res["llamadas"] == 0:
                print(f"HUERFANA: {res['pieza']} ({res['ruta']})")
            elif res["candado"]:
                print(f"CANDADO: {res['pieza']} ({res['ruta']}) — {res['llamadas']} llamadas (1 de configuracion)")
            else:
                print(f"CONECTADA: {res['pieza']} ({res['ruta']}) — {res['llamadas']} llamadas")
    else:
        print(informe(revisar(raiz=raiz)))
    sys.exit(0)
