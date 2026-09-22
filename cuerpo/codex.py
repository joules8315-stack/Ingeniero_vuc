"""Enchufe de Codex (codex exec) SIN ventana, hermana de cuerpo/bigpickle.py.

Reglas duras del enchufe:

- El pedido va SIEMPRE por la entrada estandar (stdin), con '-' como ultimo
  argumento. Nunca como argumento suelto (Windows lo rompe con saltos de
  linea).
- Antes de nada, el texto pasa por cuerpo/privacidad.py: si limpiar encuentra
  una llave (aparece CLAVE) o hay_datos_personales dice que si, NO se llama a
  Codex. Codex trabaja con la cuenta personal de Julio y ahi no pueden salir
  llaves ni datos de clientes.
- Se ejecuta con --sandbox read-only, para que Codex no toque nada.
- Se le pasa -c con approval_policy="never" para que no pida permisos.
- Se le pasa --dangerously-bypass-hook-trust y --skip-git-repo-check.
- Se le pasa -C con la carpeta (raiz o, si no viene, la carpeta del Ingeniero).
- Se le pasa -o con un archivo temporal donde Codex deja su respuesta final.
- El entorno es una copia del actual con INGENIERO_OFF=1 y
  INGENIERO_LLAMADA_DEL_PROGRAMA=1, para que el gancho de legislar de Codex
  no tome el pedido por una orden de Julio.
- Si hay timeout, error o texto vacio: se devuelve ('', [aviso]) y NUNCA se
  lanza excepcion.
- El archivo temporal de la respuesta final se borra al terminar.

Este modulo NO escribe codigo por su cuenta: solo lanza el CLI ya autorizado
por Julio y devuelve lo que el CLI conteste.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Constantes del enchufe
# ---------------------------------------------------------------------------

TIMEOUT_POR_DEFECTO = 600

# La marca que deja el propio cuerpo/privacidad.py cuando tapa una llave.
# Si aparece en el texto limpio, es que habia una llave y no se manda.
MARCA_CLAVE = "CLAVE"


# ---------------------------------------------------------------------------
# Utilidades internas
# ---------------------------------------------------------------------------

def _carpeta_del_ingeniero() -> Path:
    """La carpeta del Ingeniero: la raiz del proyecto (dos niveles arriba).

    cuerpo/codex.py vive dentro de <raiz>/cuerpo/, asi que la raiz es
    parents[1] contando desde este archivo.
    """
    return Path(__file__).resolve().parents[1]


def _revisar_privacidad(texto: str) -> tuple[str, list[str]]:
    """Pasa el texto por cuerpo/privacidad.py y decide si se puede mandar.

    Devuelve (texto_limpio, avisos). Si hay avisos, NO se debe llamar a Codex.
    """
    try:
        from cuerpo import privacidad  # type: ignore
    except Exception:
        try:
            import privacidad  # type: ignore
        except Exception as exc:
            return texto, [f"No se pudo revisar la privacidad: {exc}"]

    try:
        limpio, _tapados = privacidad.limpiar(texto)
    except Exception as exc:
        return texto, [f"No se pudo limpiar el texto: {exc}"]

    if MARCA_CLAVE in (limpio or ""):
        return limpio, [
            "NO se manda a Codex: el texto trae una llave. Codex trabaja con "
            "la cuenta personal de Julio y ahi no pueden salir llaves."
        ]

    try:
        if privacidad.hay_datos_personales(texto):
            return limpio, [
                "NO se manda a Codex: el texto trae datos personales. Codex "
                "trabaja con la cuenta personal de Julio y ahi no pueden salir "
                "datos de clientes."
            ]
    except Exception as exc:
        return limpio, [f"No se pudo comprobar datos personales: {exc}"]

    return limpio, []


def _entorno_marcado() -> dict:
    """Copia del entorno actual con las marcas que pide la tarea.

    INGENIERO_OFF=1 y INGENIERO_LLAMADA_DEL_PROGRAMA=1, para que el gancho de
    legislar de Codex no tome el pedido por una orden de Julio.
    """
    entorno = dict(os.environ)
    entorno["INGENIERO_OFF"] = "1"
    entorno["INGENIERO_LLAMADA_DEL_PROGRAMA"] = "1"
    return entorno


def _armar_comando(ejecutable: str, carpeta: str, archivo_respuesta: str) -> list:
    """Arma la orden exacta que pide la tarea."""
    return [
        ejecutable,
        "exec",
        "--sandbox",
        "read-only",
        "-c",
        'approval_policy="never"',
        "--dangerously-bypass-hook-trust",
        "--skip-git-repo-check",
        "-C",
        carpeta,
        "-o",
        archivo_respuesta,
        "-",
    ]


# ---------------------------------------------------------------------------
# La funcion publica
# ---------------------------------------------------------------------------

def preguntar(prompt: str, timeout: int = TIMEOUT_POR_DEFECTO, raiz=None) -> tuple[str, list[str]]:
    """Manda el pedido a Codex y devuelve (texto, avisos).

    - El pedido va por stdin, con '-' como ultimo argumento.
    - Antes de nada, pasa por cuerpo/privacidad.py: si hay llave o datos
      personales, NO se llama a Codex.
    - La carpeta es raiz o, si no viene, la carpeta del Ingeniero.
    - Si hay timeout, error o texto vacio: ('', [aviso]) y NUNCA excepcion.
    - El archivo temporal de la respuesta final se borra al terminar.
    """
    # 0) El pedido tiene que ser texto con algo dentro.
    if not isinstance(prompt, str) or not prompt.strip():
        return "", ["NO se manda: el pedido esta vacio"]

    # 1) Privacidad: llave o datos personales cortan la llamada.
    limpio, avisos_privacidad = _revisar_privacidad(prompt)
    if avisos_privacidad:
        return "", avisos_privacidad

    # 2) La carpeta: raiz o, si no viene, la carpeta del Ingeniero.
    if raiz is None:
        carpeta = _carpeta_del_ingeniero()
    else:
        carpeta = Path(raiz)
    carpeta_str = str(carpeta)

    # 3) Buscar codex con shutil.which.
    ejecutable = shutil.which("codex")
    if not ejecutable:
        return "", ["codex no instalado"]

    # 4) Archivo temporal para la respuesta final.
    archivo_respuesta = None
    inicio = time.monotonic()
    try:
        fd, archivo_respuesta = tempfile.mkstemp(prefix="codex_resp_", suffix=".txt")
        os.close(fd)

        comando = _armar_comando(ejecutable, carpeta_str, archivo_respuesta)
        entorno = _entorno_marcado()
        creationflags = 0x08000000 if os.name == "nt" else 0

        try:
            proc = subprocess.run(
                comando,
                input=limpio,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=carpeta_str,
                env=entorno,
                timeout=timeout,
                creationflags=creationflags,
            )
        except subprocess.TimeoutExpired:
            return "", [f"Codex no contesto en {timeout}s (timeout)"]
        except FileNotFoundError:
            return "", ["codex no instalado"]
        except OSError as exc:
            return "", [f"Error al lanzar Codex: {exc}"]

        # 5) Codigo de salida distinto de cero: aviso claro, sin excepcion.
        if proc.returncode != 0:
            err = (proc.stderr or "").strip()
            aviso = f"Codex termino con codigo {proc.returncode}"
            if err:
                aviso = f"{aviso}: {err[:300]}"
            return "", [aviso]

        # 6) Leer el archivo de la respuesta final.
        try:
            with open(archivo_respuesta, "r", encoding="utf-8") as fh:
                texto = fh.read()
        except FileNotFoundError:
            return "", ["Codex no dejo archivo de respuesta"]
        except OSError as exc:
            return "", [f"No se pudo leer la respuesta de Codex: {exc}"]

        if not texto.strip():
            return "", ["Codex no devolvio texto"]

        return texto, []

    except Exception as exc:  # red de seguridad: nunca se lanza hacia fuera
        return "", [f"Error inesperado en el enchufe: {exc}"]
    finally:
        if archivo_respuesta is not None:
            try:
                os.remove(archivo_respuesta)
            except Exception:
                pass
