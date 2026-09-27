# -*- coding: utf-8 -*-
"""arnes/bateria_en_paralelo.py

PIEZA NUEVA: corre la bateria de pruebas en PARALELO para que el guardia no se
quede sin tiempo. Nace del fallo medido el 2026-09-27: el guardia corre las 257
pruebas en FILA con tope de 900 segundos, tardan mas de 12 minutos y un trabajo
ya aprobado se perdio porque la bateria no termino.

Dos funciones publicas:

  - repartir(archivos, grupos): reparto circular, sin perder ni repetir.
  - correr(raiz, objetivo, procesos=4, tope=600): corre cada grupo con pytest
    en su propio proceso a la vez y devuelve un objeto con returncode, stdout
    y stderr, igual que subprocess.run.

Reglas duras de esta pieza:
  - Solo libreria estandar: os, sys, subprocess, concurrent.futures.
  - NUNCA lanza una excepcion hacia fuera: todo se captura y se cuenta.
  - El ultimo renglon del stdout es SIEMPRE el resumen, porque quien la usa se
    queda con el ultimo renglon para explicarle a Julio lo que paso.
"""

import concurrent.futures
import os
import subprocess
import sys


# ---------------------------------------------------------------------------
# OBJETO DE RESULTADO (mismo contrato que subprocess.run)
# ---------------------------------------------------------------------------
class Resultado(object):
    """Objeto con exactamente tres atributos: returncode, stdout y stderr.

    Se usa para que quien llame a correr() no tenga que cambiar como lee el
    resultado: es lo mismo que devuelve subprocess.run.
    """

    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        return "Resultado(returncode=%r, stdout=%r, stderr=%r)" % (
            self.returncode,
            self.stdout,
            self.stderr,
        )


# ---------------------------------------------------------------------------
# REPARTO CIRCULAR
# ---------------------------------------------------------------------------
def repartir(archivos, grupos):
    """Reparte los archivos entre ese numero de grupos en reparto circular.

    Reglas:
      - sin perder ni repetir ninguno;
      - sin grupos vacios cuando hay archivos de sobra;
      - si grupos <= 1 devuelve una sola lista con todos;
      - si la lista de archivos viene vacia devuelve lista vacia.

    Devuelve una lista de listas.
    """
    try:
        lista = list(archivos) if archivos is not None else []
    except Exception:
        return []

    if not lista:
        return []

    try:
        n = int(grupos)
    except Exception:
        n = 1

    if n <= 1:
        return [list(lista)]

    # No tiene sentido mas grupos que archivos: los grupos de mas irian vacios.
    if n > len(lista):
        n = len(lista)

    canastas = [[] for _ in range(n)]
    for indice, archivo in enumerate(lista):
        canastas[indice % n].append(archivo)
    return canastas


# ---------------------------------------------------------------------------
# EXPANSION DEL OBJETIVO
# ---------------------------------------------------------------------------
def _es_carpeta(objetivo):
    """True si el objetivo trae una carpeta, como 'vigias/' con barra al final."""
    if not isinstance(objetivo, str):
        return False
    return objetivo.endswith("/") or objetivo.endswith(os.sep)


def _archivos_de_carpeta(raiz, carpeta):
    """Lista ordenada de los test_*.py que hay dentro de esa carpeta de la raiz.

    Nunca lanza: si la carpeta no existe o no se puede leer, devuelve lista vacia.
    """
    try:
        ruta = os.path.join(raiz, carpeta)
        if not os.path.isdir(ruta):
            return []
        nombres = []
        for nombre in os.listdir(ruta):
            if nombre.startswith("test_") and nombre.endswith(".py"):
                nombres.append(nombre)
        nombres.sort()
        # Se devuelven con la carpeta delante para que pytest los encuentre
        # desde la raiz, que es el cwd con el que se corre.
        prefijo = carpeta.rstrip("/").rstrip(os.sep)
        return [prefijo + "/" + nombre for nombre in nombres]
    except Exception:
        return []


def _expandir_objetivo(raiz, objetivo):
    """Convierte el objetivo en una lista plana de archivos de prueba.

    - Si es una lista/tupla, se recorre cada elemento.
    - Si es un texto que termina en barra, se expande a los test_*.py de esa
      carpeta de la raiz, ordenados.
    - Si es un texto normal, se toma tal cual como un archivo.
    """
    archivos = []
    try:
        if isinstance(objetivo, (list, tuple)):
            for elemento in objetivo:
                archivos.extend(_expandir_objetivo(raiz, elemento))
            return archivos

        if isinstance(objetivo, str):
            if _es_carpeta(objetivo):
                archivos.extend(_archivos_de_carpeta(raiz, objetivo))
            else:
                archivos.append(objetivo)
            return archivos

        # Cualquier otra cosa: se intenta como texto.
        archivos.append(str(objetivo))
        return archivos
    except Exception:
        return archivos


# ---------------------------------------------------------------------------
# CORRIDA DE UN GRUPO
# ---------------------------------------------------------------------------
def _correr_grupo(raiz, grupo, tope, env=None, correr_uno=None):
    """Corre un grupo con pytest en su propio proceso.

    Devuelve una tupla (returncode, stdout, stderr, cortado, error).
    Nunca lanza: todo se captura aqui dentro.

    Si correr_uno no es None, se usa en lugar de subprocess.run, llamandolo
    con los mismos argumentos. Si env no es None, se anade el argumento env
    con ese valor a esa llamada; si es None no se anade.
    """
    orden = [sys.executable, "-m", "pytest", "-q"] + list(grupo)
    lanzar = correr_uno if correr_uno is not None else subprocess.run
    argumentos = dict(
        cwd=raiz,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
        timeout=tope,
    )
    if env is not None:
        argumentos["env"] = env
    try:
        completado = lanzar(orden, **argumentos)
        return (
            completado.returncode,
            completado.stdout or "",
            completado.stderr or "",
            False,
            None,
        )
    except subprocess.TimeoutExpired as fallo:
        salida = fallo.stdout or ""
        error = fallo.stderr or ""
        if isinstance(salida, bytes):
            salida = salida.decode("utf-8", "replace")
        if isinstance(error, bytes):
            error = error.decode("utf-8", "replace")
        return (None, salida, error, True, None)
    except Exception as fallo:
        return (None, "", "", False, repr(fallo))


# ---------------------------------------------------------------------------
# CORRIDA COMPLETA
# ---------------------------------------------------------------------------
def correr(raiz, objetivo, procesos=4, tope=600, env=None, correr_uno=None):
    """Corre la bateria repartida en grupos, cada grupo en su propio proceso.

    Devuelve un objeto con exactamente tres atributos: returncode, stdout y
    stderr, igual que subprocess.run.

    returncode vale 0 solo si TODOS los grupos devolvieron 0 o 5 (5 = no se
    recogio ninguna prueba); vale 1 en cualquier otro caso.

    stdout es la union de las salidas de los grupos en el orden de los grupos,
    y al final se le anade SIEMPRE un ultimo renglon de resumen con esta forma:

        bateria en paralelo: N grupos, R rojos, C cortados por tiempo

    stderr es la union de los errores de los grupos.

    UNICA excepcion a la regla de que nunca lanza: si NINGUN grupo pudo
    arrancar (es decir, TODOS los grupos tienen error distinto de None, porque
    la orden de pytest ni siquiera se pudo lanzar), se relanza con raise el
    error del primer grupo, tal cual. Esto existe para no confundir "no se
    pudo probar" con "salio mal": un grupo con returncode 1 SI arranco (las
    pruebas salieron rojas), y un grupo cortado por tiempo SI arranco. Solo
    cuando ningun grupo arranco se lanza. Si no hay grupos, no se lanza nada.
    """
    return _correr_seguro(raiz, objetivo, procesos, tope, env, correr_uno)


def _correr_seguro(raiz, objetivo, procesos, tope, env=None, correr_uno=None):
    """Cuerpo real de correr(), ya dentro de la red que captura todo."""
    # 1) Expandir el objetivo a una lista plana de archivos.
    archivos = _expandir_objetivo(raiz, objetivo)

    # 2) Repartir en grupos.
    try:
        n_procesos = int(procesos)
    except Exception:
        n_procesos = 1
    if n_procesos < 1:
        n_procesos = 1

    try:
        tope_segundos = float(tope)
    except Exception:
        tope_segundos = 600.0

    if not archivos:
        # Si la expansion dejo la lista vacia, se arma UN SOLO grupo con el
        # objetivo tal como llego, para que sea pytest quien decida (y pueda
        # devolver 5 = no se recogio ninguna prueba), como antes.
        if isinstance(objetivo, (list, tuple)):
            grupos = [list(objetivo)]
        else:
            grupos = [[objetivo]]
    else:
        grupos = repartir(archivos, n_procesos)

    # 3) Correr los grupos a la vez, cada uno en su propio proceso.
    resultados = []
    if grupos:
        try:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(grupos)
            ) as ejecutor:
                futuros = [
                    ejecutor.submit(_correr_grupo, raiz, grupo, tope_segundos, env, correr_uno)
                    for grupo in grupos
                ]
                for futuro in futuros:
                    try:
                        resultados.append(futuro.result())
                    except Exception as fallo:
                        resultados.append((None, "", "", False, repr(fallo)))
        except Exception as fallo:
            # Si ni siquiera se pudo montar el ejecutor, se corre en fila.
            resultados = []
            for grupo in grupos:
                resultados.append(_correr_grupo(raiz, grupo, tope_segundos, env, correr_uno))

    # 4) Juntar los resultados en el orden de los grupos.
    trozos_salida = []
    trozos_error = []
    rojos = 0
    cortados = 0
    todos_ok = True

    # Un grupo cuenta como ARRANCADO solo cuando su error es None, es decir
    # cuando la orden de pytest SI se pudo lanzar, aunque las pruebas hayan
    # salido rojas con returncode 1. Un grupo cortado por tiempo SI arranco
    # (su error es None). Un grupo cuyo error NO es None no arranco.
    # NO se cuenta por el returncode: returncode distinto de 0 significa
    # pruebas rojas, no que no arrancara.
    alguno_arranco = False
    primer_error = None

    for indice, grupo in enumerate(grupos):
        if indice < len(resultados):
            codigo, salida, error_texto, cortado, reventado = resultados[indice]
        else:
            codigo, salida, error_texto, cortado, reventado = (None, "", "", False, "sin resultado")

        if reventado is None:
            alguno_arranco = True
        elif primer_error is None:
            primer_error = reventado

        if salida:
            trozos_salida.append(salida)
        if error_texto:
            trozos_error.append(error_texto)

        if cortado:
            cortados += 1
            todos_ok = False
            trozos_salida.append(
                "bateria en paralelo: grupo cortado por tiempo: "
                + ", ".join(grupo)
                + "\n"
            )
        elif reventado is not None:
            rojos += 1
            todos_ok = False
            trozos_salida.append(
                "bateria en paralelo: grupo reventado: "
                + ", ".join(grupo)
                + " -> "
                + str(reventado)
                + "\n"
            )
        elif codigo not in (0, 5):
            rojos += 1
            todos_ok = False

    # 4.5) Si NINGUN grupo pudo arrancar, se relanza el error del primero.
    # Si no hay grupos, no se lanza nada. Si al menos uno arranco, todo sigue
    # igual que hoy.
    if grupos and not alguno_arranco and primer_error is not None:
        raise RuntimeError(primer_error)

    # 5) Resumen final: SIEMPRE el ultimo renglon del stdout.
    resumen = "bateria en paralelo: %d grupos, %d rojos, %d cortados por tiempo" % (
        len(grupos),
        rojos,
        cortados,
    )

    stdout = "".join(trozos_salida)
    if stdout and not stdout.endswith("\n"):
        stdout += "\n"
    stdout += resumen + "\n"

    stderr = "".join(trozos_error)

    return Resultado(
        returncode=0 if todos_ok else 1,
        stdout=stdout,
        stderr=stderr,
    )


# ---------------------------------------------------------------------------
# PRUEBA DE HUMO (no se ejecuta al importar)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Reparto de ejemplo, sin tocar nada del proyecto.
    ejemplo = ["test_a.py", "test_b.py", "test_c.py", "test_d.py", "test_e.py"]
    for canasta in repartir(ejemplo, 3):
        print(canasta)
