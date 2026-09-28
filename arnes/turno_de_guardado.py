# -*- coding: utf-8 -*-
"""Turno para guardar: un solo trabajo a la vez escribe en el disco.

PROBLEMA QUE RESUELVE
---------------------
Escribir en el disco y guardar NO puede ir en paralelo: dos guardados a la vez
se pisan. Hecho medido el 2026-09-28: con dos rondas lanzadas a la vez se vieron
dos procesos peleando por el mismo archivo de bloqueo de git y el guardado quedo
trabado 7 minutos. La ley que manda es
CONTRATO_LA_MULTITAREA_ES_LA_FORMA_DE_TRABAJAR.md, punto tres: lo que va en fila
se resuelve con TURNOS, el segundo espera su turno con un tope de tiempo, y si
el tope se pasa es FALLO, no espera eterna.

QUE HACE ESTA PIEZA
-------------------
- Da turno a UN solo trabajo a la vez para escribir y guardar.
- Hace esperar al que llega despues, con un tope de tiempo en segundos.
- Si el tope se pasa, NO espera mas: devuelve que no consiguio el turno, con un
  motivo en palabras simples.
- Si el que tenia el turno se murio sin soltarlo, el turno no se queda atrancado
  para siempre: se detecta por el tiempo que lleva tomado y se puede retomar,
  diciendolo en el motivo.
- Sirve entre procesos distintos (no solo entre hilos del mismo programa),
  porque los guardados salen de procesos separados. Para eso el turno se apoya
  en un archivo dentro de la carpeta que se le pase, y la toma del turno se hace
  creando ese archivo en exclusiva (falla si ya existe).
- No usa red, no llama a ninguna IA y no corre pruebas. Es un programa puro.

FORMA DE USO
------------
Hay dos formas, y las dos hacen lo mismo:

1) Con la palabra `with` (lo normal):

       from arnes.turno_de_guardado import turno_para_guardar

       with turno_para_guardar(carpeta, tope_segundos=30) as turno:
           if not turno["conseguido"]:
               raise RuntimeError(turno["motivo"])
           ...guardar en el disco...

2) Por separado, para sitios que no pueden usar `with`:

       from arnes.turno_de_guardado import pedir_turno, soltar_turno

       turno = pedir_turno(carpeta, tope_segundos=30)
       if not turno["conseguido"]:
           raise RuntimeError(turno["motivo"])
       try:
           ...guardar en el disco...
       finally:
           soltar_turno(turno)

ORDEN CORRECTO DE USO: primero se PIDE el turno, despues se GUARDA, y al final
se SUELTA el turno (con `with` el soltado es automatico).

NOMBRES PUBLICOS
----------------
turno_para_guardar(carpeta, tope_segundos=30, ...)  -> gestor de contexto.
pedir_turno(carpeta, tope_segundos=30, ...)         -> pide el turno y devuelve
                                                       un diccionario.
soltar_turno(turno)                                 -> suelta el turno pedido.

El diccionario que devuelve `pedir_turno` trae:
    "conseguido": True/False
    "motivo":     texto en palabras simples (explica el fallo o el retome)
    "ruta":       ruta del archivo de turno
    "testigo":    identificador del dueno del turno
"""

import errno
import os
import time
import uuid


# Nombre del archivo de turno dentro de la carpeta que se le pase.
NOMBRE_ARCHIVO_TURNO = ".turno_de_guardado"

# Tope de tiempo por defecto, en segundos. Razonable: ni eterno ni tan corto
# que un guardado normal no termine.
TOPE_POR_DEFECTO = 30.0

# Cada cuanto se reintenta tomar el turno mientras se espera, en segundos.
INTERVALO_DE_ESPERA = 0.05

# Si el turno lleva tomado mas de esto, se considera que su dueno se murio sin
# soltarlo y se puede retomar. Es el antídoto contra el atranque eterno.
SEGUNDOS_PARA_CONSIDERAR_ATRANCADO = 600.0


def _ruta_del_turno(carpeta):
    """Devuelve la ruta del archivo de turno dentro de la carpeta dada."""
    return os.path.join(carpeta, NOMBRE_ARCHIVO_TURNO)


def _leer_antiguedad(ruta):
    """Segundos que lleva existiendo el archivo de turno, o None si no existe."""
    try:
        marca = os.path.getmtime(ruta)
    except OSError:
        return None
    return max(0.0, time.time() - marca)


def _intentar_tomar(ruta, testigo):
    """Intenta tomar el turno creando el archivo en exclusiva.

    Devuelve True si lo tomo, False si ya estaba tomado por otro.
    """
    try:
        # O_CREAT | O_EXCL falla si el archivo ya existe: eso es lo que hace que
        # dos procesos no puedan tomar el turno a la vez.
        descriptor = os.open(ruta, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except OSError as error:
        if error.errno == errno.EEXIST:
            return False
        raise
    try:
        os.write(descriptor, (testigo + "\n").encode("utf-8"))
    finally:
        os.close(descriptor)
    return True


def _retomar_si_esta_atrancado(ruta, segundos_atrancado):
    """Si el turno lleva tomado mas del limite, lo retoma.

    Devuelve (retomado, motivo). `retomado` es True si se pudo retomar.
    """
    antiguedad = _leer_antiguedad(ruta)
    if antiguedad is None:
        # Ya no existe: alguien lo solto justo ahora. No hay nada que retomar.
        return False, "el turno se solto solo"
    if antiguedad < segundos_atrancado:
        return False, "el turno sigue tomado y su dueno esta vivo"
    # El dueno se murio sin soltarlo: se retoma diciendolo en el motivo.
    try:
        os.remove(ruta)
    except OSError:
        return False, "el turno estaba atrancado pero no se pudo retomar"
    return True, (
        "el turno llevaba %.1f segundos tomado (mas del limite de %.1f): "
        "su dueno se murio sin soltarlo y se retoma"
        % (antiguedad, segundos_atrancado)
    )


def pedir_turno(carpeta, tope_segundos=TOPE_POR_DEFECTO,
                segundos_atrancado=SEGUNDOS_PARA_CONSIDERAR_ATRANCADO):
    """Pide el turno para guardar y espera como mucho `tope_segundos`.

    Devuelve un diccionario con "conseguido", "motivo", "ruta" y "testigo".
    Si el tope se pasa, "conseguido" es False y "motivo" lo explica en palabras
    simples: pasarse del tope es fallo, no paciencia.
    """
    if tope_segundos is None or tope_segundos < 0:
        tope_segundos = 0.0

    if not os.path.isdir(carpeta):
        os.makedirs(carpeta, exist_ok=True)

    ruta = _ruta_del_turno(carpeta)
    testigo = "%s-%s" % (os.getpid(), uuid.uuid4().hex)
    limite = time.time() + float(tope_segundos)
    motivo_retome = ""

    while True:
        if _intentar_tomar(ruta, testigo):
            motivo = "turno conseguido"
            if motivo_retome:
                motivo = motivo + "; " + motivo_retome
            return {
                "conseguido": True,
                "motivo": motivo,
                "ruta": ruta,
                "testigo": testigo,
            }

        # No se pudo tomar: puede que el dueno se haya muerto sin soltarlo.
        retomado, motivo = _retomar_si_esta_atrancado(ruta, segundos_atrancado)
        if retomado:
            motivo_retome = motivo
            continue

        if time.time() >= limite:
            return {
                "conseguido": False,
                "motivo": (
                    "no se consiguio el turno para guardar: se paso el tope de "
                    "%.1f segundos esperando a que el otro trabajo soltara"
                    % float(tope_segundos)
                ),
                "ruta": ruta,
                "testigo": testigo,
            }

        time.sleep(INTERVALO_DE_ESPERA)


def soltar_turno(turno):
    """Suelta el turno pedido con `pedir_turno`.

    Devuelve True si lo solto, False si no habia nada que soltar. Es seguro
    llamarlo dos veces: la segunda no hace nada.
    """
    if not turno or not turno.get("conseguido"):
        return False
    ruta = turno.get("ruta")
    if not ruta or not os.path.exists(ruta):
        return False
    try:
        os.remove(ruta)
    except OSError:
        return False
    turno["conseguido"] = False
    return True


class _TurnoDeGuardado(object):
    """Gestor de contexto que pide el turno al entrar y lo suelta al salir."""

    def __init__(self, carpeta, tope_segundos=TOPE_POR_DEFECTO,
                 segundos_atrancado=SEGUNDOS_PARA_CONSIDERAR_ATRANCADO):
        self.carpeta = carpeta
        self.tope_segundos = tope_segundos
        self.segundos_atrancado = segundos_atrancado
        self.turno = None

    def __enter__(self):
        self.turno = pedir_turno(
            self.carpeta,
            tope_segundos=self.tope_segundos,
            segundos_atrancado=self.segundos_atrancado,
        )
        return self.turno

    def __exit__(self, tipo, valor, traza):
        soltar_turno(self.turno)
        # No se traga ninguna excepcion: el que guarda decide que hacer.
        return False


def turno_para_guardar(carpeta, tope_segundos=TOPE_POR_DEFECTO,
                       segundos_atrancado=SEGUNDOS_PARA_CONSIDERAR_ATRANCADO):
    """Devuelve un gestor de contexto que da el turno para guardar.

    Uso normal:

        with turno_para_guardar(carpeta, tope_segundos=30) as turno:
            if not turno["conseguido"]:
                raise RuntimeError(turno["motivo"])
            ...guardar en el disco...
    """
    return _TurnoDeGuardado(
        carpeta,
        tope_segundos=tope_segundos,
        segundos_atrancado=segundos_atrancado,
    )
