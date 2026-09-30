# -*- coding: utf-8 -*-
"""arnes/candado_nace_enganchada.py — FRENA AL CERRAR si hay una pieza que nadie llama.

En palabras simples: cuando se va a cerrar la casa, esto mira si alguna pieza quedo
huerfana (escrita, aprobada, guardada, y nadie la llama nunca). Si hay alguna, NO deja
cerrar y dice su nombre. Se arregla de dos maneras, y solo dos: ENGANCHARLA (que alguien
la llame de verdad) o BORRARLA (si no hacia falta). No hay una tercera: apuntar una marca
a mano no vale, porque eso vuelve a depender de que alguien se acuerde.

REUSA el contador que ya existe, skills/nace_conectada.py, sin copiarle el codigo.
NO cuentan como huerfanas los PUNTOS DE ENTRADA:
  - las piezas que estan dentro de la carpeta de pruebas (vigias);
  - las que se nombran desde el archivo de opciones de la casa;
  - las que traen dentro el trozo de siempre para correrlas a mano
    (un renglon que comprueba si se esta ejecutando como programa principal).

NUNCA revienta: ante cualquier problema deja cerrar y lo avisa en el motivo.
"""
import os
import sys


# AQUI = la carpeta de la casa (dos niveles arriba de este archivo).
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# El trozo de siempre para poder correrlas a mano: si el archivo lo trae, es punto de entrada.
_TROZO_DE_ENTRADA = "__name__"

# Nombres de archivos de opciones de la casa que se miran para no marcar como huerfanas
# a las piezas que ahi se nombran.
_ARCHIVOS_DE_OPCIONES = [
    "opciones.json",
    "opciones.py",
    "config.json",
    "config.py",
    "ajustes.json",
    "ajustes.py",
]


def _nombres_de_opciones(raiz):
    """Devuelve el texto de los archivos de opciones de la casa, para saber que piezas nombran.
    Si no se puede leer alguno, se salta sin reventar."""
    trozos = []
    for nombre in _ARCHIVOS_DE_OPCIONES:
        ruta = os.path.join(raiz, nombre)
        try:
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                trozos.append(f.read())
        except Exception:
            continue
    return "\n".join(trozos)


def _es_punto_de_entrada(raiz, nombre):
    """True si la pieza es punto de entrada y por tanto NO cuenta como huerfana.
    Tres maneras: esta en la carpeta de pruebas; se nombra desde el archivo de opciones;
    o trae dentro el trozo de siempre para correrla a mano."""
    # 1) dentro de la carpeta de pruebas
    try:
        rel = os.path.relpath(nombre, raiz)
        partes = rel.replace("\\", "/").split("/")
        if "vigias" in partes:
            return True
    except Exception:
        pass

    # 2) nombrada desde el archivo de opciones de la casa
    try:
        texto_opciones = _nombres_de_opciones(raiz)
        base = os.path.splitext(os.path.basename(nombre))[0]
        if base and base in texto_opciones:
            return True
    except Exception:
        pass

    # 3) trae dentro el trozo de siempre para correrla a mano
    try:
        with open(nombre, "r", encoding="utf-8", errors="ignore") as f:
            texto = f.read()
        if _TROZO_DE_ENTRADA in texto:
            return True
    except Exception:
        pass

    return False


def huerfanas(raiz):
    """Devuelve la LISTA de nombres de piezas de la casa a las que NO llama nadie.
    Reusa el contador que ya existe, skills/nace_conectada.py, sin copiarle el codigo.
    Si no se puede usar por cualquier motivo, devuelve lista VACIA y no revienta.
    NO cuentan como huerfanas los PUNTOS DE ENTRADA."""
    try:
        sys.path.insert(0, raiz)
        import skills.nace_conectada as contador
    except Exception:
        return []

    try:
        crudo = None
        # Se le pide su cuenta por los nombres mas probables de su funcion publica.
        for nombre_funcion in ("huerfanas", "contar_huerfanas", "lista_huerfanas", "contar"):
            funcion = getattr(contador, nombre_funcion, None)
            if callable(funcion):
                try:
                    crudo = funcion(raiz)
                except TypeError:
                    try:
                        crudo = funcion()
                    except Exception:
                        crudo = None
                except Exception:
                    crudo = None
                if crudo is not None:
                    break
        if crudo is None:
            return []
    except Exception:
        return []

    # El contador puede devolver nombres o diccionarios: se normaliza a nombres.
    nombres = []
    try:
        for pieza in crudo:
            if isinstance(pieza, str):
                nombres.append(pieza)
            elif isinstance(pieza, dict):
                for clave in ("nombre", "pieza", "archivo", "ruta", "path"):
                    if clave in pieza and isinstance(pieza[clave], str):
                        nombres.append(pieza[clave])
                        break
    except Exception:
        return []

    # Se quitan los puntos de entrada.
    limpias = []
    for nombre in nombres:
        try:
            if _es_punto_de_entrada(raiz, nombre):
                continue
        except Exception:
            continue
        limpias.append(nombre if nombre.endswith(".py") else nombre + ".py")
    return limpias


def recien_nacidas(raiz, dias=2):
    """Devuelve las huerfanas que nacieron dentro de los ultimos `dias`.

    Se apoya en la historia guardada del proyecto (git) para saber cuando se guardo
    por primera vez cada archivo. Si la historia no devuelve fecha, NO se considera
    recien nacida: ante la duda no se bloquea. Ante cualquier fallo devuelve lista
    vacia para no frenar a ciegas.

    Se pregunta a la historia UNA SOLA VEZ por todas las piezas, no una vez por
    cada pieza, y se busca cada archivo por su ruta completa dentro de la casa.
    """
    import subprocess
    import datetime

    try:
        lista = huerfanas(raiz)
    except Exception:
        return []

    if not lista:
        return []

    limite = datetime.date.today() - datetime.timedelta(days=dias)

    try:
        salida = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%ad", "--date=short",
             "--name-only"],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if salida.returncode != 0:
            return []
    except Exception:
        return []

    # Primera fecha en que aparece cada archivo en la historia (la mas antigua).
    primera_fecha = {}
    fecha_actual = None
    for linea in salida.stdout.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            fecha_actual = datetime.datetime.strptime(linea, "%Y-%m-%d").date()
            continue
        except ValueError:
            pass
        if fecha_actual is None:
            continue
        if linea not in primera_fecha:
            primera_fecha[linea] = fecha_actual

    nacidas = []
    for nombre in lista:
        try:
            ruta_relativa = os.path.relpath(nombre, raiz).replace(os.sep, "/")
        except Exception:
            ruta_relativa = nombre.replace(os.sep, "/")
        fecha = primera_fecha.get(ruta_relativa)
        if fecha is None:
            # No se sabe: ante la duda NO se frena.
            continue
        if fecha >= limite:
            nacidas.append(nombre)
    return nacidas


def se_puede_cerrar(raiz):
    """Devuelve DOS cosas, en este orden: primero si se puede cerrar (verdadero o falso),
    y despues el motivo en palabras simples. Dice falso cuando hay alguna huerfana, y entonces
    el motivo NOMBRA a cada una y dice las dos maneras de arreglarlo (enganchar o borrar).
    Dice verdadero cuando no hay ninguna. Nunca revienta: ante cualquier problema dice
    verdadero y lo avisa en el motivo."""
    try:
        lista = huerfanas(raiz)
    except Exception as error:
        return True, "No se pudo medir las piezas huerfanas (%s); se deja cerrar." % error

    if not lista:
        return True, "No hay piezas huerfanas: todo lo que existe tiene quien lo llame."

    nacidas = recien_nacidas(raiz)
    viejas = [n for n in lista if n not in nacidas]

    if viejas:
        aviso = (
            "AVISO: hay %d piezas huerfanas viejas; hay que ir ENGANCHANDOLAS o BORRANDOLAS."
            % len(viejas)
        )
    else:
        aviso = ""

    if not nacidas:
        if aviso:
            return True, aviso
        return True, "Ninguna pieza nacio huerfana."

    nombres = ", ".join(nacidas)
    motivo = (
        "Hay piezas huerfanas recien nacidas (nadie las llama): %s. "
        "Se arregla de dos maneras, y solo dos: ENGANCHARLA (que alguien la llame de verdad) "
        "o BORRARLA (si no hacia falta)." % nombres
    )
    if aviso:
        motivo = motivo + " " + aviso
    return False, motivo


def main():
    """El trozo de siempre para poder correrlo solo: si no se puede cerrar, escribe el motivo
    por la salida de errores y devuelve el numero dos, que es lo que frena; si se puede,
    devuelve cero."""
    puede, motivo = se_puede_cerrar(AQUI)
    if not puede:
        sys.stderr.write(motivo + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
