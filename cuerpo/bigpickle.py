"""Enchufe de Big Pickle por OpenCode SIN ventana (plan v4 paso 1).

Probado a mano el 2026-09-18. Reglas duras del enchufe:

- El encargo va SIEMPRE por la entrada estandar (stdin). Nunca como argumento
  (Windows lo rompe con saltos de linea) ni con -f (se cuelga esperando
  permisos).
- Se ejecuta en una carpeta temporal vacia para que OpenCode no vea el repo.
- La salida son lineas JSON: se junta part.text de las lineas type=='text' y
  se suma part.cost de las lineas type=='step_finish'.
- Nunca se manda una llave: si el prompt trae 'API_KEY' o 'sk-' se corta.
- Si hay timeout, error o texto vacio: se devuelve ('', [aviso]) y NUNCA se
  lanza excepcion.
- Cada llamada se anota en memoria/BIGPICKLE.log.

Este modulo NO escribe codigo por su cuenta: solo lanza el CLI ya autorizado
por Julio y devuelve lo que el CLI conteste. La generacion de codigo sigue
prohibida para la IA cara (CONTRATO_LA_IA_CARA_NUNCA_ESCRIBE_CODIGO.md).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Constantes del enchufe
# ---------------------------------------------------------------------------

MODELO = "opencode/big-pickle"
COMANDO = ["opencode", "run", "-m", MODELO, "--format", "json"]
# Solo si no se puede medir; su record medido es 328 s (A-47, 2026-09-21).
TIMEOUT_POR_DEFECTO = 600

# Marcas que delatan una llave en el encargo. Si aparece cualquiera, no se manda.
MARCAS_DE_LLAVE = ("API_KEY", "sk-")

# Raiz del proyecto: este archivo vive en <raiz>/cuerpo/bigpickle.py
RAIZ = Path(__file__).resolve().parent.parent
RUTA_LOG = RAIZ / "memoria" / "BIGPICKLE.log"


# ---------------------------------------------------------------------------
# Anotacion en el log
# ---------------------------------------------------------------------------

def _anotar(
    segundos: float,
    costo: float,
    ok: bool,
    nota: str = "",
    tamano: int = 0,
    unidades: int = 0,
) -> None:
    """Anota una llamada en memoria/BIGPICKLE.log. Nunca lanza excepcion."""
    try:
        RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)
        fecha = datetime.now().isoformat(timespec="seconds")
        linea = (
            f"{fecha}\tsegundos={segundos:.3f}\tcosto={costo:.6f}\t"
            f"unidades={unidades}\t"
            f"ok={bool(ok)}\tnota={nota}\n"
        )
        with open(RUTA_LOG, "a", encoding="utf-8") as fh:
            fh.write(linea)
    except Exception:
        # El log no puede tumbar la llamada.
        pass
    try:
        from cuerpo import cuaderno
        cuaderno.apuntar(
            "bigpickle",
            clase="auditar",
            resultado=(cuaderno.OK if ok else cuaderno.ERROR),
            crudo=nota,
            segundos=segundos,
            tamano=tamano,
        )
    except Exception:
        # El cuaderno no puede tumbar la llamada.
        pass


# ---------------------------------------------------------------------------
# Filtro de llaves
# ---------------------------------------------------------------------------

def _trae_llave(prompt: str) -> bool:
    """True si el encargo trae algo que parece una llave. No se manda nunca.

    Detecta la FORMA de una llave (no palabras sueltas) con re.search.
    Ante la duda (excepcion), devuelve True: no se manda. Nunca lanza.
    """
    if not isinstance(prompt, str):
        return False
    try:
        patrones = (
            r'\b(?:sk|gsk|pk|rk)[-_][A-Za-z0-9_\-]{20,}',
            r'\bAIza[0-9A-Za-z_\-]{30,}',
            r'(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*[\x22\x27]?[A-Za-z0-9_\-]{16,}',
        )
        for patron in patrones:
            if re.search(patron, prompt):
                return True
        from cuerpo import privacidad
        if '<CLAVE>' in privacidad.limpiar(prompt)[0]:
            return True
        return False
    except Exception:
        return True


# ---------------------------------------------------------------------------
# Parseo de la salida JSON por lineas
# ---------------------------------------------------------------------------

def _parsear_salida(salida: str) -> tuple[str, float]:
    """Junta part.text de las lineas type=='text' y suma part.cost de
    las lineas type=='step_finish'.

    Devuelve (texto, costo). Las lineas que no son JSON valido se ignoran.
    """
    trozos: list[str] = []
    costo_total = 0.0
    if not salida:
        return "", 0.0
    for linea in salida.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            dato = json.loads(linea)
        except (ValueError, TypeError):
            continue
        if not isinstance(dato, dict):
            continue
        tipo = dato.get("type")
        parte = dato.get("part")
        if tipo == "text" and isinstance(parte, dict):
            texto = parte.get("text")
            if isinstance(texto, str) and texto:
                trozos.append(texto)
        elif tipo == "step_finish" and isinstance(parte, dict):
            coste = parte.get("cost")
            if isinstance(coste, (int, float)):
                costo_total += float(coste)
    return "".join(trozos), costo_total


def unidades_de_la_salida(salida: str) -> dict:
    """Suma las unidades que el recibo declara en cada step_finish.

    Recorre las lineas JSON de la salida y, en cada linea con type igual a
    'step_finish', suma part.tokens con las claves total, input y output.
    Devuelve un diccionario con esas tres sumas. Con un recibo vacio, sin
    tokens, o con lineas que no son JSON valido, devuelve ceros y no revienta.
    """
    total = 0
    entrada = 0
    salida_tokens = 0
    if not salida:
        return {"total": 0, "input": 0, "output": 0}
    for linea in salida.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            dato = json.loads(linea)
        except (ValueError, TypeError):
            continue
        if not isinstance(dato, dict):
            continue
        if dato.get("type") != "step_finish":
            continue
        parte = dato.get("part")
        if not isinstance(parte, dict):
            continue
        tokens = parte.get("tokens")
        if not isinstance(tokens, dict):
            continue
        valor = tokens.get("total")
        if isinstance(valor, (int, float)):
            total += int(valor)
        valor = tokens.get("input")
        if isinstance(valor, (int, float)):
            entrada += int(valor)
        valor = tokens.get("output")
        if isinstance(valor, (int, float)):
            salida_tokens += int(valor)
    return {"total": total, "input": entrada, "output": salida_tokens}


# ---------------------------------------------------------------------------
# Funcion publica
# ---------------------------------------------------------------------------

def preguntar(prompt: str, timeout: int = None) -> tuple[str, list[str]]:
    """Manda el encargo a Big Pickle por OpenCode y devuelve (texto, avisos).

    - El encargo va por stdin, nunca como argumento ni con -f.
    - Se corre en una carpeta temporal vacia.
    - Si el prompt trae una llave, no se manda.
    - Si hay timeout, error o texto vacio: ('', [aviso]) y NUNCA excepcion.
    """
    # 0) Si no me dan timeout, lo mido con cuotas; si no se puede, el de por defecto.
    if timeout is None:
        try:
            from cuerpo import cuotas
            timeout = cuotas.espera_de_bigpickle(len(prompt))
        except Exception:
            timeout = TIMEOUT_POR_DEFECTO

    # 1) Filtro de llaves: no se manda nada que parezca una llave.
    if _trae_llave(prompt):
        _anotar(0.0, 0.0, False, nota="llave_detectada", tamano=len(prompt))
        return "", ["NO se manda: trae una llave"]

    if not isinstance(prompt, str) or not prompt.strip():
        _anotar(0.0, 0.0, False, nota="prompt_vacio", tamano=len(prompt))
        return "", ["NO se manda: el encargo esta vacio"]

    # 2) Carpeta temporal vacia para que OpenCode no vea el repo.
    carpeta = None
    inicio = time.monotonic()
    try:
        carpeta = tempfile.mkdtemp(prefix="bigpickle_")
        ejecutable = shutil.which("opencode")
        if not ejecutable:
            segundos = time.monotonic() - inicio
            _anotar(segundos, 0.0, False, nota="opencode_no_encontrado", tamano=len(prompt))
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
            _anotar(segundos, 0.0, False, nota="opencode_no_encontrado", tamano=len(prompt))
            return "", ["opencode no instalado"]
        except OSError as exc:
            segundos = time.monotonic() - inicio
            _anotar(segundos, 0.0, False, nota=f"oserror:{exc}", tamano=len(prompt))
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
            _anotar(segundos, 0.0, False, nota="timeout", tamano=len(prompt))
            return "", [f"Big Pickle no contesto en {timeout}s (timeout)"]

        segundos = time.monotonic() - inicio

        # 3) Codigo de salida distinto de cero: aviso claro, sin excepcion.
        if proc.returncode != 0:
            err = (stderr or "").strip()
            _, costo = _parsear_salida(stdout or "")
            unidades = unidades_de_la_salida(stdout or "")
            _anotar(segundos, costo, False, nota=f"returncode={proc.returncode}", tamano=len(prompt), unidades=unidades["total"])
            aviso = f"OpenCode termino con codigo {proc.returncode}"
            if err:
                aviso = f"{aviso}: {err[:300]}"
            return "", [aviso]

        # 4) Parseo de la salida JSON por lineas.
        texto, costo = _parsear_salida(stdout or "")

        if not texto.strip():
            _anotar(segundos, costo, False, nota="texto_vacio", tamano=len(prompt))
            return "", ["Big Pickle no devolvio texto"]

        unidades = unidades_de_la_salida(stdout or "")
        _anotar(segundos, costo, True, nota="ok", tamano=len(prompt), unidades=unidades["total"])
        return texto, []

    except Exception as exc:  # red de seguridad: nunca se lanza hacia fuera
        segundos = time.monotonic() - inicio
        _anotar(segundos, 0.0, False, nota=f"excepcion:{exc}", tamano=len(prompt))
        return "", [f"Error inesperado en el enchufe: {exc}"]
    finally:
        if carpeta is not None:
            try:
                shutil.rmtree(carpeta, ignore_errors=True)
            except Exception:
                pass


if __name__ == "__main__":
    import sys

    encargo = sys.stdin.read()
    texto, avisos = preguntar(encargo)
    if avisos:
        for a in avisos:
            print(f"AVISO: {a}", file=sys.stderr)
    if texto:
        print(texto)
