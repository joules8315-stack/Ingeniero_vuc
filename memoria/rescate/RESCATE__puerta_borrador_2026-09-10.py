# -*- coding: utf-8 -*-
"""arnes/puerta.py - LA PUERTA TRASERA, CERRADA CON LLAVE.

Julio, 2026-09-10: "la carpeta que te permite trabajar sin candados, sin arnes,
la puerta trasera". Medido ese dia: una IA edito la carpeta del DMM sin pasar por
el equipo (la ley 6), porque la IA del chat puede leer y escribir esa carpeta sin
que ningun candado del arnes la frene. Esa es la puerta trasera.

EL AGUJERO QUE TAPA: la IA que atiende el chat NO pasa por el arnes de la terminal.
Puede abrir y guardar archivos del proyecto directamente. Los candados que frenan
al equipo no existen para la puerta trasera.

LO QUE HACE, y como se comprueba:
  - cerrar <proyecto>: pide la clave (dos veces, no se ve al escribir), encripta la
    carpeta del proyecto con OpenSSL AES-256-CBC + PBKDF2 (iter 200000, salt), deja
    un archivo .vuc.enc en su lugar y borra la carpeta abierta. Sin la clave de
    Julio NADIE puede trabajar ahi: ni equipo, ni IA, ni el propio Ingeniero.
  - abrir <proyecto>: pide la misma clave, desencripta y restaura la carpeta.
  - la CLAVE NO SE GUARDA EN NINGUN LADO. Se pide en el momento y se olvida.
  - nada se borra ANTES de comprobar que el encriptado se puede desencriptar.
"""
import getpass
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENC_EXT = ".vuc.enc"
ITER = 200000


def _openssl():
    """Ubica OpenSSL real (Git for Windows lo trae); si no, NO se inventa cifrado casero."""
    for cand in ("openssl", r"C:\Program Files\Git\usr\bin\openssl.exe"):
        p = shutil.which(cand) if "/" not in cand else cand
        if p and os.path.exists(p):
            return p
        if cand.endswith("openssl.exe") and os.path.exists(cand):
            return cand
    return None


def _proyecto(apodo):
    sys.path.insert(0, os.path.join(AQUI, "cerebro"))
    from cerebro import grafo
    p = grafo.proyectos().get(apodo) or {}
    return p.get("ruta")


def _pedir_clave(nueva=True):
    """Pide la clave sin que se vea al escribir. Solo para Julio, por consola."""
    c1 = getpass.getpass("Clave de la puerta (no se ve al escribir): ")
    if not c1:
        print("NO_ENCONTRADO: la clave no puede estar vacia. No se toca nada.")
        return None
    if nueva:
        c2 = getpass.getpass("Repetila (para no errarle): ")
        if c1 != c2:
            print("Las dos veces no coincidio. No se toca nada.")
            return None
    return c1


def _rama_enc(ruta_proyecto):
    return ruta_proyecto.rstrip("\\/") + ENC_EXT


def _temporal():
    d = None
    try:
        d = os.environ.get("INGENIERO_PUERTA_TEST")
        if d:
            os.makedirs(d, exist_ok=True)
            return d
    except Exception:
        pass
    return tempfile.mkdtemp(prefix="vuc_puerta_")


def _encriptar_carpeta(ruta, clave, destino):
    """Encripta la carpeta entera a destino (AES-256-CBC, PBKDF2). Devuelve True/False."""
    ox = _openssl()
    if not ox:
        print("NO_ENCONTRADO: OpenSSL no esta instalado. No se inventa cifrado casero.")
        return False
    tmp = _temporal()
    try:
        z = os.path.join(tmp, "puerta.zip")
        with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zp:
            for raiz, _, archivos in os.walk(ruta):
                if os.path.basename(raiz) in (".git", "__pycache__", ".venv"):
                    continue
                for a in archivos:
                    if a.endswith(ENC_EXT):
                        continue
                    rp = os.path.join(raiz, a)
                    zp.write(rp, os.path.relpath(rp, ruta))
        cmd = [ox, "enc", "-aes-256-cbc", "-pbkdf2", "-iter", str(ITER),
               "-salt", "-in", z, "-out", destino, "-pass", "pass:" + clave]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("El encriptado fallo: %s" % (r.stderr or r.stdout or "sin detalle"))
            return False
        # PRUEBA ANTES DE BORRAR: desencriptar a un archivo de prueba y comparar el zip.
        dp = os.path.join(tmp, "prueba.zip")
        cmd2 = [ox, "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", str(ITER),
                "-in", destino, "-out", dp, "-pass", "pass:" + clave]
        r2 = subprocess.run(cmd2, capture_output=True, text=True)
        if r2.returncode != 0 or not zipfile.ZipFile(dp).testzip() is None is False:
            if r2.returncode != 0:
                print("La prueba de desencriptado FALLO: %s" % (r2.stderr or "sin detalle"))
                return False
        if not zipfile.ZipFile(dp).testzip() is None:
            print("La prueba de desencriptado FALLO: el zip dio codigo != None")
            return False
        return True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _abrir_carpeta(destino, clave, ruta_original):
    """Desencripta destino (UN ARCHIVO) y devuelve la carpeta temporal con el contenido."""
    ox = _openssl()
    if not ox:
        print("NO_ENCONTRADO: OpenSSL no esta instalado. No se puede abrir la puerta.")
        return None
    tmp = _temporal()
    try:
        z = os.path.join(tmp, "puerta.zip")
        cmd = [ox, "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", str(ITER),
               "-in", destino, "-out", z, "-pass", "pass:" + clave]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("La clave no abrio la puerta (o el archivo esta danado). No se toca nada.")
            return None
        if zipfile.ZipFile(z).testzip() is not None:
            print("EL ARCHIVO ENCRIPTADO ESTA DANADO. No se restaura nada; avisale a Julio.")
            return None
        return z
    except Exception as e:
        print("No se pudo abrir la puerta: %s" % e)
        return None


def cerrar(apodo):
    """Encripta la carpeta del proyecto. Deja .vuc.enc y borra la carpeta abierta."""
    ruta = _proyecto(apodo)
    if not ruta or not os.path.isdir(ruta):
        print("NO_ENCONTRADO: no hay carpeta abierta para '%s' (ruta: %s)" % (apodo, ruta))
        return 2
    destino = _rama_enc(ruta)
    if os.path.exists(destino):
        print("YA hay una puerta cerrada para '%s' (%s). No se pisa una puerta cerrada." % (apodo, destino))
        return 2
    clave = _pedir_clave(nueva=True)
    if not clave:
        return 2
    print("Encriptando %s ..." % ruta)
    if not _encriptar_carpeta(ruta, clave, destino):
        # no se borra nada: el encriptado fallo o no paso la prueba.
        if os.path.exists(destino):
            os.remove(destino)
        return 2
    shutil.rmtree(ruta, ignore_errors=True)
    print("PUERTA CERRADA. La carpeta de '%s' quedo encriptada: %s" % (apodo, destino))
    print("Para trabajar de nuevo: python ingeniero.py puerta abrir %s" % apodo)
    return 0


def abrir(apodo):
    """Desencripta el .vuc.enc y restaura la carpeta del proyecto."""
    ruta = _proyecto(apodo)
    if not ruta:
        print("NO_ENCONTRADO: no conozco el proyecto '%s'." % apodo)
        return 2
    destino = _rama_enc(ruta)
    if not os.path.exists(destino):
        print("No hay puerta cerrada para '%s': no existe %s" % (apodo, destino))
        return 2
    if os.path.isdir(ruta):
        print("La carpeta de '%s' ya esta abierta. No se pisa lo que ya esta abierto." % apodo)
        return 2
    clave = _pedir_clave(nueva=False)
    if not clave:
        return 2
    tmp = _temporal()
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        z = _abrir_carpeta(destino, clave, ruta)
        if z is None:
            return 2
        # creamos en un temporal y renombramos: no dejar la carpeta a medias.
        dest_tmp = os.path.join(tmp, "_restaurando")
        with zipfile.ZipFile(z) as zp:
            zp.extractall(dest_tmp)
        os.rename(dest_tmp, ruta)
        os.remove(destino)
        print("PUERTA ABIERTA. La carpeta de '%s' volvio a estar disponible." % apodo)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    if len(sys.argv) not in (4, 5):
        print(__doc__)
        print("uso: python ingeniero.py puerta cerrar <proyecto>")
        print("     python ingeniero.py puerta abrir <proyecto>")
        return 1
    accion, apodo = sys.argv[2], sys.argv[3]
    if accion == "cerrar":
        return cerrar(apodo)
    if accion == "abrir":
        return abrir(apodo)
    print("NO_ENCONTRADO: la accion '%s' no existe (solo cerrar o abrir)." % accion)
    return 1


if __name__ == "__main__":
    sys.exit(main())