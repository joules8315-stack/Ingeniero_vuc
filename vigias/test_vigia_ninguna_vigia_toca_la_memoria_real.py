"""Vigia: ninguna vigia que importa a Big Pickle toca la memoria real.

Medido el 2026-10-01: 423 de las 1678 lineas del registro de Big Pickle (25 por ciento)
las escribieron las pruebas al correr, porque la ruta del registro es fija y ninguna
prueba la cambia. Rompe la ley 23 (ninguna comprobacion toca el estado real).

Esta vigia:
  1. Localiza las vigias que importan a Big Pickle.
  2. Corre cada una con una COPIA de memoria/ (nunca la real).
  3. Comprueba que el registro real NO cambia de tamano ni de contenido.

Nace ROJA hoy: el assert final falla porque las vigias escriben en el registro real.
Pasa cuando todas las partes de esta pieza esten conectadas (cada vigia usa su copia).
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


RAIZ = Path(__file__).resolve().parent.parent
VIGIAS = RAIZ / "vigias"
MEMORIA_REAL = RAIZ / "memoria"

# El registro de Big Pickle: ruta fija que hoy nadie desvia.
REGISTRO_REAL = MEMORIA_REAL / "registro_big_pickle.jsonl"

# Nombres de las vigias que importan a Big Pickle (10 segun la medicion del 2026-10-01).
# Se descubren por funcion: cualquier vigia que mencione 'big_pickle' o 'Big Pickle'.
MARCADORES_BIG_PICKLE = ("big_pickle", "Big Pickle", "BIG_PICKLE")


def _huella(ruta: Path) -> str:
    """Devuelve el sha256 del archivo, o cadena vacia si no existe."""
    if not ruta.exists():
        return ""
    h = hashlib.sha256()
    with ruta.open("rb") as fh:
        for bloque in iter(lambda: fh.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def _vigias_que_importan_a_big_pickle() -> list[Path]:
    """Descubre por funcion las vigias que mencionan a Big Pickle.

    No se busca por nombre de archivo: se lee el contenido y se mira si aparece
    alguno de los marcadores. Asi se encuentran las 10 vigias medidas el 2026-10-01.
    """
    encontradas: list[Path] = []
    if not VIGIAS.is_dir():
        return encontradas
    for ruta in sorted(VIGIAS.glob("test_*.py")):
        if ruta.name == Path(__file__).name:
            continue
        try:
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(marcador in texto for marcador in MARCADORES_BIG_PICKLE):
            encontradas.append(ruta)
    return encontradas


def _copia_de_memoria(destino: Path) -> Path:
    """Copia memoria/ a un directorio temporal y devuelve la raiz de la copia.

    La copia conserva la estructura para que las vigias que buscan 'memoria/...'
    encuentren algo, pero nunca la ruta real.
    """
    raiz_copia = destino / "raiz"
    raiz_copia.mkdir(parents=True, exist_ok=True)
    if MEMORIA_REAL.is_dir():
        shutil.copytree(MEMORIA_REAL, raiz_copia / "memoria", dirs_exist_ok=True)
    else:
        (raiz_copia / "memoria").mkdir(parents=True, exist_ok=True)
    return raiz_copia


def _correr_vigia_con_copia(vigia: Path, raiz_copia: Path) -> subprocess.CompletedProcess:
    """Corre una vigia apuntando a la copia de memoria/ via variables de entorno.

    Se pasan varias variables porque cada vigia puede leer una distinta; la idea es
    que ninguna caiga en la ruta fija. Si la vigia no las respeta, escribira en la
    real y el assert final de esta vigia lo detectara.
    """
    entorno = dict(os.environ)
    entorno["VUC_RAIZ"] = str(raiz_copia)
    entorno["VUC_MEMORIA"] = str(raiz_copia / "memoria")
    entorno["VUC_REGISTRO_BIG_PICKLE"] = str(
        raiz_copia / "memoria" / "registro_big_pickle.jsonl"
    )
    entorno["BIG_PICKLE_REGISTRO"] = str(
        raiz_copia / "memoria" / "registro_big_pickle.jsonl"
    )
    entorno["PYTHONPATH"] = str(raiz_copia) + os.pathsep + entorno.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(vigia), "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=str(raiz_copia),
        env=entorno,
        capture_output=True,
        text=True,
        timeout=300,
    )


def test_ninguna_vigia_toca_la_memoria_real():
    """Corre las vigias de Big Pickle con copia y comprueba que el registro real no cambia.

    Nace ROJA hoy: el assert final falla porque las vigias escriben en el registro real.
    """
    vigias = _vigias_que_importan_a_big_pickle()
    assert vigias, (
        "No se encontro ninguna vigia que importe a Big Pickle. "
        "La medicion del 2026-10-01 dice que hay 10; si no aparecen, el descubrimiento "
        "por funcion esta roto y esta vigia no puede cumplir su papel."
    )

    huella_antes = _huella(REGISTRO_REAL)
    tamano_antes = REGISTRO_REAL.stat().st_size if REGISTRO_REAL.exists() else 0

    with tempfile.TemporaryDirectory(prefix="vigia_big_pickle_") as tmp:
        raiz_copia = _copia_de_memoria(Path(tmp))
        for vigia in vigias:
            _correr_vigia_con_copia(vigia, raiz_copia)

    huella_despues = _huella(REGISTRO_REAL)
    tamano_despues = REGISTRO_REAL.stat().st_size if REGISTRO_REAL.exists() else 0

    assert huella_despues == huella_antes, (
        "El registro real de Big Pickle cambio al correr las vigias. "
        f"Antes: {huella_antes[:16]} ({tamano_antes} bytes). "
        f"Despues: {huella_despues[:16]} ({tamano_despues} bytes). "
        "Las vigias deben usar una copia de memoria/, no la ruta fija. "
        "Ley 23: ninguna comprobacion toca el estado real."
    )
