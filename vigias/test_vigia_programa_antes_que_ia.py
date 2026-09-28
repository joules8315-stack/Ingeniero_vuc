"""Vigia: el programa que mide lo que puede hacer un programa, ANTES que la IA.

Esta vigia NACE ROJA A PROPOSITO: el programa que vigila todavia no existe.
Se escribe en la ronda siguiente, y asi lo manda la ley de que la vigia nace
antes que el cambio.

Contrato que la vigia exige, tal cual, al programa
arnes/medir_lo_que_puede_hacer_un_programa.py:

  - leer_cuaderno(ruta) -> lista de diccionarios, uno por renglon legible,
    saltando en silencio los renglones rotos, y lista vacia si el archivo no esta.
  - agrupar(lista) -> diccionario cuya clave es la clase de la llamada (texto
    'sin_nombre' cuando la clase viene vacia) y cuyo valor es otro diccionario
    con estas cinco claves exactas: llamadas, segundos, letras, sin_provecho,
    segundos_sin_provecho. 'letras' suma el campo tamano. 'sin_provecho' cuenta
    las llamadas cuyo resultado NO es ok. 'segundos_sin_provecho' suma los
    segundos de esas mismas.
  - medir(raiz) -> lee memoria/CUADERNO_DE_LLAMADAS.jsonl dentro de esa raiz,
    escribe memoria/MEDIDA_PROGRAMA_ANTES_QUE_IA.md dentro de esa misma raiz y
    devuelve lo que dio agrupar.

Cuatro pruebas, todas en tmp_path, sin red y sin lanzar procesos. El programa se
importa dentro de cada prueba.
"""

import importlib.util
import json
import sys
from pathlib import Path


# --- Arranque de sys.path, igual que en las otras vigias de la carpeta vigias ---
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


RUTA_PROGRAMA = RAIZ / "arnes" / "medir_lo_que_puede_hacer_un_programa.py"


# Palabras que el programa NO puede nombrar, ni como import ni como llamada.
PALABRAS_PROHIBIDAS = [
    "obrero",
    "bigpickle",
    "deepseek",
    "claude",
    "requests",
    "urllib",
    "http",
]


# Los seis renglones del cuaderno de mentira: cinco buenos y uno roto.
RENGLONES_BUENOS = [
    {"cuando": "2026-09-27T10:00:00", "quien": "medidor", "tamano": 100,
     "vuelta": 1, "clase": "reparar", "resultado": "ok", "segundos": 10},
    {"cuando": "2026-09-27T10:01:00", "quien": "medidor", "tamano": 200,
     "vuelta": 1, "clase": "reparar", "resultado": "vacio", "segundos": 20},
    {"cuando": "2026-09-27T10:02:00", "quien": "medidor", "tamano": 300,
     "vuelta": 1, "clase": "auditar", "resultado": "ok", "segundos": 30},
    {"cuando": "2026-09-27T10:03:00", "quien": "medidor", "tamano": 400,
     "vuelta": 1, "clase": "auditar", "resultado": "error", "segundos": 40},
    {"cuando": "2026-09-27T10:04:00", "quien": "medidor", "tamano": 50,
     "vuelta": 1, "clase": "", "resultado": "ok", "segundos": 5},
]

RENGLON_ROTO = "esto no es json ni de lejos {{{ roto"


def _cargar_programa():
    """Importa el programa que vigila esta vigia, dentro de la prueba."""
    if not RUTA_PROGRAMA.exists():
        raise AssertionError(
            "Falta el programa que esta vigia exige: "
            "arnes/medir_lo_que_puede_hacer_un_programa.py. "
            "Esta vigia nace roja a proposito: el programa se escribe en la "
            "ronda siguiente."
        )
    especificacion = importlib.util.spec_from_file_location(
        "medir_lo_que_puede_hacer_un_programa", RUTA_PROGRAMA
    )
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


def _escribir_cuaderno_de_mentira(raiz):
    """Deja el cuaderno de mentira en memoria/CUADERNO_DE_LLAMADAS.jsonl."""
    carpeta = Path(raiz) / "memoria"
    carpeta.mkdir(parents=True, exist_ok=True)
    cuaderno = carpeta / "CUADERNO_DE_LLAMADAS.jsonl"
    lineas = [json.dumps(renglon, ensure_ascii=False) for renglon in RENGLONES_BUENOS]
    lineas.append(RENGLON_ROTO)
    cuaderno.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return cuaderno


def test_el_programa_no_llama_a_ninguna_ia():
    """El programa no nombra ninguna IA ni ninguna puerta de red."""
    assert RUTA_PROGRAMA.exists(), (
        "Falta el programa que esta vigia exige: "
        "arnes/medir_lo_que_puede_hacer_un_programa.py"
    )
    texto = RUTA_PROGRAMA.read_text(encoding="utf-8").lower()
    for palabra in PALABRAS_PROHIBIDAS:
        assert palabra not in texto, (
            "El programa nombra '%s', y no puede nombrarlo ni como import "
            "ni como llamada." % palabra
        )


def test_las_cuentas_salen_bien(tmp_path):
    """Las cuentas por clase salen exactas sobre el cuaderno de mentira."""
    programa = _cargar_programa()
    cuaderno = _escribir_cuaderno_de_mentira(tmp_path)

    leidos = programa.leer_cuaderno(str(cuaderno))
    cuentas = programa.agrupar(leidos)

    reparar = cuentas["reparar"]
    assert reparar["llamadas"] == 2
    assert reparar["segundos"] == 30
    assert reparar["letras"] == 300
    assert reparar["sin_provecho"] == 1
    assert reparar["segundos_sin_provecho"] == 20

    auditar = cuentas["auditar"]
    assert auditar["llamadas"] == 2
    assert auditar["segundos"] == 70
    assert auditar["letras"] == 700
    assert auditar["sin_provecho"] == 1
    assert auditar["segundos_sin_provecho"] == 40

    sin_nombre = cuentas["sin_nombre"]
    assert sin_nombre["llamadas"] == 1
    assert sin_nombre["segundos"] == 5
    assert sin_nombre["letras"] == 50
    assert sin_nombre["sin_provecho"] == 0
    assert sin_nombre["segundos_sin_provecho"] == 0


def test_deja_el_documento_en_la_carpeta_memoria(tmp_path):
    """medir deja el documento en memoria/ y su texto nombra las clases."""
    programa = _cargar_programa()
    _escribir_cuaderno_de_mentira(tmp_path)

    programa.medir(str(tmp_path))

    documento = Path(tmp_path) / "memoria" / "MEDIDA_PROGRAMA_ANTES_QUE_IA.md"
    assert documento.exists(), "medir no dejo el documento en memoria/"
    texto = documento.read_text(encoding="utf-8")
    assert "reparar" in texto
    assert "auditar" in texto


def test_un_renglon_roto_no_tumba_la_medida(tmp_path):
    """Un renglon roto se salta en silencio: quedan cinco renglones legibles."""
    programa = _cargar_programa()
    cuaderno = _escribir_cuaderno_de_mentira(tmp_path)

    leidos = programa.leer_cuaderno(str(cuaderno))

    assert len(leidos) == 5
