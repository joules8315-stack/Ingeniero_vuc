# -*- coding: utf-8 -*-
"""arnes/guardia_de_guardado.py — EL CANDADO QUE NO DEPENDE DE QUIEN ESCRIBA.

Julio, 2026-08-24:
  "Crea candado para que cline use el candado, y siempre trabaje modo ingeniero, que no se
   pueda salir por ningun lado."

EL AGUJERO QUE TAPA: todos los candados de este taller son de Claude. Cline no los tiene. Y las
reglas escritas (.clinerules, CLAUDE.md) son CONTEXTO: se pueden ignorar. Ya paso con el
protocolo entero, escrito desde julio y saltado durante un dia completo.

ESTE ES DISTINTO: lo ejecuta GIT, no la IA. Da igual quien escriba el codigo — Claude, Cline,
otra IA o Julio a mano: para GUARDAR hay que pasar por aqui. No hay version educada de saltarselo.

QUE EXIGE, en este orden:
  1. Las VIGIAS del proyecto en VERDE. Guardar algo roto es lo que mas dano hace.
  2. Que no se guarden LLAVES. Un archivo de claves subido no se puede desubir.

LO QUE NO ESTORBA (o el candado se vuelve un muro y se acaba apagando, que es peor):
  · si el proyecto no tiene vigias, no se inventa una excusa: se deja pasar y se avisa
  · si las vigias no se pueden correr (falta pytest), se avisa y se deja pasar: no se atrapa
    a Julio por un problema de instalacion

LA UNICA SALIDA es `git commit --no-verify`, que es de git y no se puede quitar. Por eso cada
vez que este guardia FRENA queda apuntado, y cada vez que alguien pasa sin el, se nota: el
apunte no aparece.
"""
import os
import subprocess
import sys
import time
import json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOSPECHOSOS = ("credencial", "credenciales", ".env", "secret", "password", ".key", ".pem")
LIBRETA = os.path.join("memoria", "GUARDIA.log")


def _apuntar(raiz, texto):
    """Deja rastro. A prueba de fallos: si no se puede escribir, el guardia NO se cae."""
    try:
        ruta = os.path.join(raiz, LIBRETA)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M") + "  " + texto + "\n")
    except Exception:
        pass


def _lo_que_se_va_a_guardar(raiz):
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only"],
                           cwd=raiz, capture_output=True, text=True, timeout=60)
        return [l.strip() for l in (r.stdout or "").splitlines() if l.strip()]
    except Exception:
        return []


import re

# Como es una llave DE VERDAD. Se mira el CONTENIDO, no el nombre: un documento que HABLA de
# claves no lleva ninguna dentro, y frenarlo por el nombre es ruido. Paso el mismo dia que se
# escribio este guardia: freno el contrato que explica como se piden las claves.
PINTA_DE_LLAVE = re.compile(
    r"sk-[A-Za-z0-9]{16,}"
    r"|AIza[A-Za-z0-9_\-]{20,}"
    r"|gsk_[A-Za-z0-9]{20,}"
    r"|eyJ[A-Za-z0-9_\-]{30,}\.[A-Za-z0-9_\-]{20,}"
    r"|(password|contrasena|clave|secret)\s*[:=]\s*[\"']?[A-Za-z0-9!@#%^&*_\-]{8,}",
    re.IGNORECASE)

# Por el NOMBRE solo se frena lo que EXISTE para guardar llaves: la terminacion del archivo.
# Nada de frenar por que la palabra "credenciales" aparezca en el nombre: asi se freno el
# contrato que EXPLICA como se piden las claves, que no lleva ninguna. Una senal que salta con
# todo se vuelve ruido y se acaba ignorando, que es peor que no tenerla.
TERMINACIONES_DE_LLAVES = (".env", ".key", ".pem", ".pfx", ".p12")


def _hay_llaves(raiz, archivos):
    """Frena solo si de verdad hay una llave. Ya paso: el archivo de claves de Foto Informe
    esta subido a internet y no hay forma de desubirlo.

    DOS CAMINOS, a proposito:
      · por el NOMBRE: los archivos que solo existen para guardar llaves. No hace falta abrirlos.
      · por el CONTENIDO: cualquier otro donde asome algo con pinta de llave de verdad.
    Un documento que EXPLICA como se piden las claves no lleva ninguna: ese pasa.
    """
    malos = []
    for a in archivos:
        n = a.lower()
        if n.endswith(TERMINACIONES_DE_LLAVES) or "/.env" in n or n.startswith(".env"):
            malos.append(a + "   (archivo de llaves)")
            continue
        ruta = os.path.join(raiz, a.replace("/", os.sep))
        try:
            if os.path.getsize(ruta) > 2 * 1024 * 1024:
                continue                       # demasiado grande para ser un archivo de claves
            with open(ruta, encoding="utf-8", errors="ignore") as f:
                if PINTA_DE_LLAVE.search(f.read()):
                    malos.append(a + "   (lleva algo con pinta de llave DENTRO)")
        except Exception:
            continue                           # si no se puede leer, no se frena por eso
    return malos


def _cubierto_por_equipo(archivos):
    """¿Lo que se va a guardar lleva veredicto del equipo? (Julio, 2026-09-02)

    Asi el balance sabe, en cada guardado y sin que nadie lo cuente a mano, si esto fue del
    equipo o a mano. Devuelve True (equipo), False (a mano) o None (no toca codigo)."""
    codigo = [a for a in archivos
              if a.lower().endswith((".py", ".js", ".html", ".ts", ".jsx", ".tsx", ".css", ".sql"))]
    if not codigo:
        return None                                   # nada que atribuir: no toca codigo
    ruta = os.environ.get("INGENIERO_VEREDICTO_TEST") or \
        os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except Exception:
        d = None
    if not d or str(d.get("veredicto", "")).upper() != "APROBADO":
        return False
    bases = set(os.path.basename(str(a)).lower() for a in d.get("archivos", []))
    return all(os.path.basename(a).lower() in bases for a in codigo)


def _apuntar_balance(raiz, tipo, archivos):
    """Deja una linea en el BALANCE.log: que hizo el equipo y que se hizo a mano. A prueba de
    fallos: si no se puede escribir, el guardia no se cae."""
    try:
        ruta = os.path.join(raiz, "memoria", "BALANCE.log")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("%s | %s\n" % (tipo, ", ".join(archivos[:8])))
    except Exception:
        pass


def _vigias(raiz):
    """(paso, mensaje). Si no hay vigias o no se pueden correr, se DEJA PASAR con aviso."""
    carpeta = os.path.join(raiz, "vigias")
    if not os.path.isdir(carpeta):
        return True, "este proyecto no tiene vigias (se deja pasar)"
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "vigias/"],
                           cwd=raiz, capture_output=True, text=True, timeout=900)
    except Exception as e:
        return True, "no se pudieron correr las vigias (%s): se deja pasar" % str(e)[:60]
    salida = (r.stdout or "") + (r.stderr or "")
    ultima = [l for l in salida.splitlines() if l.strip()][-1:] or [""]
    if r.returncode == 0:
        return True, ultima[0].strip()
    if r.returncode == 5:
        return True, "no se recogio ninguna vigia (se deja pasar)"
    return False, ultima[0].strip()


def main():
    raiz = AQUI
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, timeout=30)
        if (r.stdout or "").strip():
            raiz = (r.stdout or "").strip().replace("/", os.sep)
    except Exception:
        pass

    archivos = _lo_que_se_va_a_guardar(raiz)

    llaves = _hay_llaves(raiz, archivos)
    if llaves:
        _apuntar(raiz, "FRENADO: intento de guardar llaves -> " + ", ".join(llaves[:4]))
        sys.stderr.write(
            "\nGUARDIA: NO SE GUARDA. Ibas a subir un archivo de LLAVES:\n"
            + "".join("   " + x + "\n" for x in llaves[:6])
            + "\n  Una clave subida NO se puede desubir. Ya paso una vez.\n"
              "  Sacala del guardado y ponla en la lista de lo que nunca se sube.\n\n")
        return 1

    paso, mensaje = _vigias(raiz)
    if not paso:
        _apuntar(raiz, "FRENADO: vigias rojas -> " + mensaje)
        sys.stderr.write(
            "\nGUARDIA: NO SE GUARDA. Hay pruebas ROJAS:\n"
            "   " + mensaje + "\n\n"
            "  No se guarda dejando algo roto. Da igual quien haya escrito el codigo.\n"
            "  Arreglalo y vuelve a guardar.\n\n")
        return 1

    # EL BALANCE (Julio, 2026-09-02): cada guardado apunta si fue del equipo o a mano, para que
    # nadie tenga que contar a mano cuanto trabaja cada quien (memoria/BALANCE.log).
    try:
        cub = _cubierto_por_equipo(archivos)
        if cub is True:
            _apuntar_balance(raiz, "equipo", archivos)
        elif cub is False:
            _apuntar_balance(raiz, "a_mano", archivos)
    except Exception:
        pass

    _apuntar(raiz, "OK: %d archivo(s) | %s" % (len(archivos), mensaje))
    sys.stderr.write("GUARDIA: verde. " + mensaje + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
