"""Enchufe de Grok 4.7 por OpenCode Go SIN ventana.

Mismas reglas duras que cuerpo/bigpickle.py:

- El encargo va SIEMPRE por la entrada estandar (stdin). Nunca como argumento
  (Windows lo rompe con saltos de linea) ni con -f (se cuelga esperando
  permisos).
- Se ejecuta en una carpeta temporal vacia para que OpenCode no vea el repo.
- La salida son lineas JSON: se junta part.text de las lineas type=='text' y
  se suma part.cost de las lineas type=='step_finish'.
- Nunca se manda una llave: si el prompt trae 'API_KEY' o 'sk-' se corta.
- Si hay timeout, error o texto vacio: se devuelve ('', [aviso]) y NUNCA se
  lanza excepcion.
- Cada llamada se anota en el cuaderno con cuaderno.apuntar('grok47',
  clase='auditar', ...), dentro de un try que nunca tumba la llamada.

Este modulo NO escribe codigo por su cuenta: solo lanza el CLI ya autorizado
por Julio y devuelve lo que el CLI conteste. La generacion de codigo sigue
prohibida para la IA cara (CONTRATO_LA_IA_CARA_NUNCA_ESCRIBE_CODIGO.md).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time

from cuerpo import bigpickle


# ---------------------------------------------------------------------------
# Constantes del enchufe
# ---------------------------------------------------------------------------

MODELO = "opencode-go/grok-4.7"
COMANDO = ["opencode", "run", "-m", MODELO, "--format", "json"]
TIMEOUT_POR_DEFECTO = 240


def _anotar(segundos: float, costo: float, ok: bool, nota: str) -> None:
    """Apunta la llamada en el cuaderno. Nunca lanza."""
    try:
        from cuerpo import cuaderno

        cuaderno.apuntar(
            "grok47",
            clase="auditar",
            resultado=cuaderno.OK if ok else cuaderno.ERROR,
            crudo=nota,
            segundos=segundos,
        )
    except Exception:
        pass


def preguntar(prompt: str, timeout: int = TIMEOUT_POR_DEFECTO) -> tuple[str, list[str]]:
    """Manda el encargo a Grok 4.7 por OpenCode Go y devuelve (texto, avisos).

    - El encargo va por stdin, nunca como argumento ni con -f.
    - Se corre en una carpeta temporal vacia.
    - Si el prompt trae una llave, no se manda.
    - Si hay timeout, error o texto vacio: ('', [aviso]) y NUNCA excepcion.
    """
    # 1) Filtro de llaves: no se manda nada que parezca una llave.
    if bigpickle._trae_llave(prompt):
        _anotar(0.0, 0.0, False, nota="llave_detectada")
        return "", ["NO se manda: trae una llave"]

    if not isinstance(prompt, str) or not prompt.strip():
        _anotar(0.0, 0.0, False, nota="prompt_vacio")
        return "", ["NO se manda: el encargo esta vacio"]

    # 2) Carpeta temporal vacia para que OpenCode no vea el repo.
    carpeta = None
    inicio = time.monotonic()
    try:
        carpeta = tempfile.mkdtemp(prefix="grok_")
        ejecutable = shutil.which("opencode")
        if not ejecutable:
            segundos = time.monotonic() - inicio
            _anotar(segundos, 0.0, False, nota="opencode_no_encontrado")
            return "", ["opencode no instalado"]

        comando = [ejecutable] + COMANDO[1:]
        creationflags = 0x08000000 if os.name == "nt" else 0

        try:
            proc = subprocess.Popen(
                comando,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                cwd=carpeta,
                creationflags=creationflags,
            )
        except FileNotFoundError:
            segundos = time.monotonic() - inicio
            _anotar(segundos, 0.0, False, nota="opencode_no_encontrado")
            return "", ["opencode no instalado"]
        except OSError as exc:
            segundos = time.monotonic() - inicio
            _anotar(segundos, 0.0, False, nota=f"oserror:{exc}")
            return "", [f"Error al lanzar OpenCode: {exc}"]

        try:
            stdout, stderr = proc.communicate(input=prompt, timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                        creationflags=0x08000000,
                    )
                except Exception:
                    pass
            else:
                try:
                    proc.kill()
                except Exception:
                    pass
            try:
                proc.communicate(timeout=5)
            except Exception:
                pass
            segundos = time.monotonic() - inicio
            _anotar(segundos, 0.0, False, nota="timeout")
            return "", [f"Grok no contesto en {timeout}s (timeout)"]

        segundos = time.monotonic() - inicio

        # 3) Codigo de salida distinto de cero: aviso claro, sin excepcion.
        if proc.returncode != 0:
            err = (stderr or "").strip()
            _, costo = bigpickle._parsear_salida(stdout or "")
            _anotar(segundos, costo, False, nota=f"returncode={proc.returncode}")
            aviso = f"OpenCode termino con codigo {proc.returncode}"
            if err:
                aviso = f"{aviso}: {err[:300]}"
            return "", [aviso]

        # 4) Parseo de la salida JSON por lineas.
        texto, costo = bigpickle._parsear_salida(stdout or "")

        if not texto.strip():
            _anotar(segundos, costo, False, nota="texto_vacio")
            return "", ["Grok no devolvio texto"]

        _anotar(segundos, costo, True, nota="ok")
        return texto, []

    except Exception as exc:  # red de seguridad: nunca se lanza hacia fuera
        segundos = time.monotonic() - inicio
        _anotar(segundos, 0.0, False, nota=f"excepcion:{exc}")
        return "", [f"Error inesperado en el enchufe: {exc}"]
    finally:
        if carpeta is not None:
            try:
                shutil.rmtree(carpeta, ignore_errors=True)
            except Exception:
                pass
