# -*- coding: utf-8 -*-
"""arnes/revisor_de_programa.py — EL OJO 2. Caza lo mecanico SIN gastar ni una IA.

SOLO HACE CUENTAS. El JUICIO sigue siendo del auditor de IA: si un cambio esta bien pensado,
si rompe a un vecino o si es una regresion, eso NO lo mira este programa. Se suma, no
sustituye. Lo que cambia es que lo mecanico deja de depender de que un cerebro se fije.

POR QUE NACE (dos fallos medidos el 2026-09-08, los dos con DOS cerebros delante):
  1. El equipo escribio una prueba que REVENTABA en la primera linea: usaba re sin haberlo
     importado. La aprobo un cerebro DISTINTO con "confianza alta". Se corrio y fallo.
  2. El equipo RECHAZO por invento las constantes que el propio encargo mandaba definir.

De lo que el auditor rechazo en un dia, casi todo era CUENTA, no juicio:
    "texto viejo y nuevo son identicos"  -> comparar
    "usa un nombre que no existe"        -> leer el codigo
    "no implementa lo que se pidio"      -> buscar un nombre
    "es una regresion total"             -> ESO SI es juicio: se queda para la IA

LEY: CONTRATO_CUENTA_O_JUICIO.md y CONTRATO_MENOS_IA_MAS_PROGRAMA.md (Julio).

Se usa asi:
    from arnes import revisor_de_programa
    fallos = revisor_de_programa.revisar(propuesta, tarea)
"""
import ast
import builtins
import os
import re
import sys
import textwrap

# Palabras con las que empieza un PEDAZO que vive dentro de otro bloque. Un texto que empieza
# asi no es un archivo entero y no se puede leer suelto, por mucho que este perfecto.
EMPIEZOS_DE_PEDAZO = ("else", "elif", "except", "finally", "case")


def es_un_pedazo(texto):
    """El texto es un PEDAZO de dentro de otro bloque, no un archivo entero?

    Se sabe por la forma, que es una cuenta: o viene sangrado desde el primer renglon, o
    empieza por una palabra que solo existe colgando de algo de mas arriba.
    """
    for linea in str(texto or "").splitlines():
        if not linea.strip():
            continue
        if linea[:1] in (" ", "\t"):
            return True
        primera = linea.strip().split()[0].rstrip(":") if linea.strip().split() else ""
        return primera in EMPIEZOS_DE_PEDAZO
    return False

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Los nombres propios de Python (round, len, print...). No son invento de nadie.
PROPIOS_DE_PYTHON = set(dir(builtins))
# Los duendes de MODULO: en todo .py existen (__file__, __name__, __package__...), como
# en el propio modulo builtins. dir(builtins) trae algunos pero NO __file__ (builtins no
# tiene archivo), y un .py normal SI: frenar por eso era una frenada en falso (2026-09-10).
PROPIOS_DE_PYTHON |= {"__file__", "__cached__", "__builtins__", "__annotations__",
                      "__package__", "__loader__", "__name__", "__doc__",
                      "__spec__", "__path__", "__debug__"}


def sin_ruido(texto):
    """Quita comentarios, textos entre triples comillas y lineas en blanco.

    La misma idea que ya usan skills/cazar_el_humo.py y cuerpo/aplicador.py: no se duplica el
    criterio, se reusa. Sirve para comparar dos textos por lo que de verdad hacen.
    """
    t = str(texto or "")
    t = re.sub(r'"""(?:.|\n)*?"""', " ", t)
    t = re.sub(r"'''(?:.|\n)*?'''", " ", t)
    fuera = []
    for linea in t.splitlines():
        linea = re.sub(r"#.*$", "", linea).strip()
        if linea:
            fuera.append(linea)
    return "\n".join(fuera)


def _conocidos(arbol):
    """Todo nombre que en ese texto SI existe: lo importado, lo definido, lo asignado, los
    argumentos, los de except y los de global. Mas los nombres propios de Python."""
    vistos = set(PROPIOS_DE_PYTHON)
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import):
            for a in n.names:
                vistos.add((a.asname or a.name).split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                vistos.add(a.asname or a.name)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            vistos.add(n.name)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            vistos.add(n.id)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            vistos.add(n.name)
        elif isinstance(n, ast.arg):
            vistos.add(n.arg)
        elif isinstance(n, (ast.Global, ast.Nonlocal)):
            for nombre in n.names:
                vistos.add(nombre)
    return vistos


def _leidos(arbol):
    """Los nombres que el texto LEE: los que tienen que existir de antes."""
    fuera = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            fuera.append(n.id)
    return fuera


def _piezas(arbol):
    """Los nombres de funcion y de clase que hay en ese texto, en el orden en que salen.

    Es la cuenta que faltaba. Comparando esta lista antes y despues se ve, sin gastar ni una
    IA, si un cambio se lleva por delante algo que ya estaba. Se miran tambien las de dentro
    (los metodos de una clase), porque el 2026-09-11 lo que desaparecio fue justo eso.
    """
    fuera = []
    for n in ast.walk(arbol):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if n.name not in fuera:
                fuera.append(n.name)
    return fuera


def revisar(propuesta, tarea=""):
    """Las cuatro cuentas. Devuelve una LISTA de frases; vacia si no encuentra nada.

    NUNCA lanza: si algo raro pasa, lo dice como un fallo mas y sigue. Un revisor que revienta
    deja pasar todo, que es lo contrario de para lo que existe.
    """
    fallos = []
    try:
        p = propuesta if isinstance(propuesta, dict) else {}
        viejo = str(p.get("texto_viejo") or "")
        nuevo = str(p.get("texto_nuevo") or p.get("codigo") or "")
        tarea = str(tarea or "")

        if not nuevo.strip():
            return ["La propuesta no trae texto nuevo: no hay nada que aplicar."]

        # 1 — HUMO: el cambio solo toca comentarios y no repara nada.
        if viejo.strip() and sin_ruido(viejo) == sin_ruido(nuevo):
            fallos.append("HUMO: quitando comentarios y lineas en blanco, el texto nuevo es "
                          "IGUAL al viejo. Ese cambio no repara nada.")

        # 2 — SINTAXIS: si queda roto, no se puede aplicar ni se puede seguir leyendo.
        #
        # OJO, FRENADA EN FALSO CAZADA EL 2026-09-08 la primera vez que este revisor se uso
        # con trabajo de verdad: el equipo entrego un PEDAZO que empieza a media altura
        # (dentro de otro bloque, con su sangria y empezando por else). No estaba roto: es un
        # pedazo, no un archivo entero. Y este revisor grito "el codigo queda roto".
        # Su propia vigia lo dice: un candado que frena lo legitimo es PEOR que no tenerlo,
        # porque ensena a ignorarlos todos. Por eso, si es un pedazo y no se deja leer entero,
        # NO se acusa de nada: no se puede comprobar, y callar es mas honrado que gritar.
        arbol = None
        try:
            arbol = ast.parse(nuevo)
        except SyntaxError as e:
            try:
                arbol = ast.parse(textwrap.dedent(nuevo))
            except SyntaxError:
                if es_un_pedazo(nuevo):
                    return fallos       # pedazo suelto: no hay nada que se pueda comprobar
                fallos.append("EL CODIGO QUEDA ROTO en el renglon %s: %s. Asi no arranca."
                              % (getattr(e, "lineno", "?"), e.msg))
                return fallos
        except Exception as e:
            fallos.append("No se pudo leer el codigo nuevo: %s" % str(e)[:120])
            return fallos

        # 3 — USA UN NOMBRE QUE NO EXISTE. El fallo real del 2026-09-08: re sin importar.
        #
        # SOLO SI ES UN ARCHIVO ENTERO. Segunda frenada en falso cazada el mismo dia: se
        # reviso un PEDAZO del interior de una funcion y el revisor grito que perfil,
        # objetivo, camp, experimentos e hipotesis "no existen". Existen todos: son los datos
        # que recibe la funcion de mas arriba y lo que se importa al principio del archivo.
        # Mirando un pedazo suelto no se puede ver nada de eso, asi que acusar es mentir.
        # Cuando no se puede comprobar, se calla. Frenar lo bueno ensena a ignorar los frenos.
        if es_un_pedazo(nuevo):
            return fallos
        conocidos = _conocidos(arbol)
        ya_dicho = set()
        for nombre in _leidos(arbol):
            if nombre not in conocidos and nombre not in ya_dicho:
                ya_dicho.add(nombre)
                fallos.append("USA UN NOMBRE QUE NO EXISTE: '%s'. No se importa, no se define "
                              "y no es de Python. En cuanto se corra, revienta." % nombre)

        # 4 — NO HACE LO QUE SE PIDIO. Solo se miran las palabras con guion bajo dentro: son
        # nombres de funcion o de dato. Las palabras normales del castellano se ignoran, porque
        # si no, "reparar" o "impuesto" darian frenadas en falso.
        # FRENADA EN FALSO CAZADA EL 2026-09-08, en la primera mordida de verdad: un encargo
        # nombra archivos (cuerpo/campana_flujo.py) y palabras del propio encargo
        # (texto_viejo, texto_nuevo). Esas NO son funciones que la reparacion deba tocar, y
        # contarlas frena trabajos buenos. Un candado que frena lo legitimo ensena a ignorar
        # todos los candados. Por eso se quitan antes de mirar.
        limpia = re.sub(r"[\w/\\.]+\.(?:py|md|json|txt|js|html|css|sql|cfg|config)\b", " ", tarea)
        for jerga in ("texto_viejo", "texto_nuevo"):
            limpia = limpia.replace(jerga, " ")
        # FRENADA EN FALSO CAZADA EL 2026-09-13: la ruta de la carpeta de la herramienta y el nombre del
        # plan frenaban rondas buenas. Se quitan las rutas de Windows y los nombres de archivo con guiones,
        # y si el archivo que se cambia EXISTE, solo cuentan las palabras que estan en ese archivo: las demas
        # son contexto del encargo. Si no existe, se sigue como antes. Lo vigila la vigia del revisor.
        limpia = re.sub(r"[A-Za-z]:\\[^\s,;]*", " ", limpia)
        limpia = re.sub(r"[\w/\\.-]+\.(?:py|md|json|txt|js|html|css|sql|cfg|config)\b", " ", limpia)
        contenido_archivo = None
        try:
            ruta_archivo = str(p.get("archivo") or "")
            if ruta_archivo and os.path.isfile(ruta_archivo):
                with open(ruta_archivo, encoding="utf-8-sig", errors="replace") as fa:
                    contenido_archivo = fa.read()
        except Exception:
            contenido_archivo = None
        for palabra in set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]*\b", limpia)):
            if contenido_archivo is not None and palabra not in contenido_archivo:
                continue
            if palabra not in viejo and palabra not in nuevo:
                fallos.append("NO HACE LO QUE SE PIDIO: el encargo habla de '%s' y esa palabra "
                              "no aparece ni en el texto viejo ni en el nuevo." % palabra)

        # 5 — DESAPARECE LO QUE YA ESTABA. EL AGUJERO MEDIDO EL 2026-09-11: este revisor
        # vigilaba que lo NUEVO estuviera bien y NO vigilaba que lo VIEJO siguiera ahi. Por
        # ese hueco se perdio la puerta del jefe que coordina del DMM (paso de 81 a 56
        # renglones sin guardar) y NINGUN guardia dijo nada: las 526 vigias siguieron verdes.
        # Ni el revisor, ni el que aplica los cambios, ni el copista miraban los borrados.
        #
        # Es una CUENTA, no un juicio: se listan los nombres de funcion y de clase de cada
        # texto y se dice cuales estaban y ya no estan. SI es querido borrarlos, se dice y se
        # sigue; lo que no puede pasar es que se pierdan en silencio.
        #
        # SOLO SI LOS DOS TEXTOS SON ARCHIVOS ENTEROS QUE SE DEJAN LEER. Con un pedazo suelto
        # no se puede comparar nada y acusar seria mentir: es la misma leccion de las dos
        # frenadas en falso del 2026-09-08. Cuando no se puede comprobar, se calla.
        if viejo.strip() and not es_un_pedazo(viejo):
            arbol_viejo = None
            try:
                arbol_viejo = ast.parse(viejo)
            except SyntaxError:
                try:
                    arbol_viejo = ast.parse(textwrap.dedent(viejo))
                except SyntaxError:
                    arbol_viejo = None
            except Exception:
                arbol_viejo = None
            if arbol_viejo is not None:
                quedan = _piezas(arbol)
                perdidas = [n for n in _piezas(arbol_viejo) if n not in quedan]
                if perdidas:
                    fallos.append(
                        "DESAPARECE LO QUE YA ESTABA: el texto nuevo se lleva por delante %d "
                        "pieza(s) que si estaban en el viejo: %s. Si ese borrado es querido, "
                        "hay que decirlo por escrito; si no, es trabajo que se pierde en "
                        "silencio, que fue lo que paso el 2026-09-11."
                        % (len(perdidas), ", ".join(perdidas)))
    except Exception as e:      # un revisor que revienta deja pasar todo
        fallos.append("El revisor no pudo terminar la revision: %s" % str(e)[:140])
    return fallos


def informe(fallos):
    if not fallos:
        return ("REVISOR DE PROGRAMA: nada mecanico que objetar.\n"
                "  OJO: esto NO dice que el cambio sea bueno. El juicio (si esta bien pensado\n"
                "  y si rompe vecinos) sigue siendo del auditor de IA.")
    L = ["REVISOR DE PROGRAMA: %d fallo(s) cazados sin gastar ni una IA:" % len(fallos), ""]
    for f in fallos:
        L.append("   - " + f)
    return "\n".join(L)


if __name__ == "__main__":
    import json
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], encoding="utf-8") as f:
            datos = json.load(f)
        prop = datos.get("propuesta") if isinstance(datos, dict) else {}
        tar = (prop or {}).get("diagnostico", "") if isinstance(prop, dict) else ""
        print(informe(revisar(prop or {}, tar)))
    else:
        print(__doc__)
    sys.exit(0)
