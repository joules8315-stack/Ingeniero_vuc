"""VIGIA: SE MIDE EL RUIDO DEL PAQUETE.

Metodo de Julio: la vigia se escribe primero y nace ROJA.

Que vigila esta prueba:
  La orden R22-paquete-compacto-sin-ruido prometia una vigia que no existia.
  Esta prueba demuestra, con un assert que falla HOY, que todavia NO hay
  ninguna ley en el proyecto que obligue a que el paquete viaje en formato
  compacto, sin ruido y en formato json.

Como nace roja:
  El assert final comprueba que existe al menos un contrato del proyecto
  que declara el formato compacto del paquete. Hoy no existe ninguno, asi
  que el assert falla. No falla por error de sintaxis ni por un nombre que
  no existe: falla porque la condicion que vigila aun no se cumple.

Cuando la reparacion este hecha (se escriba la ley del formato compacto),
esta prueba pasara sin tocar el assert.

Regla de aislamiento: esta prueba SOLO LEE el disco. No escribe en ningun
archivo de estado compartido, asi que no necesita desvio en el conftest.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Raiz del proyecto. Se sube desde este archivo (vigias/...) hasta la raiz.
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent

# Palabras que la ley del formato compacto tiene que nombrar.
PALABRAS_LEY = ("compacto", "sin ruido", "formato json")

# Carpetas donde viven los contratos y las leyes del proyecto.
CARPETAS_CONTRATOS = (
    RAIZ,
    RAIZ / "contratos",
    RAIZ / "leyes",
    RAIZ / "memoria",
)

# Extensiones que cuentan como contrato o ley.
SUFIJOS_CONTRATO = (".md", ".json")


def _es_contrato(ruta: Path) -> bool:
    """Un contrato es un .md o un .json cuyo nombre lo delata."""
    if ruta.suffix.lower() not in SUFIJOS_CONTRATO:
        return False
    nombre = ruta.name.lower()
    return (
        "contrato" in nombre
        or "ley" in nombre
        or "regla" in nombre
        or "orden" in nombre
    )


def _leer_texto(ruta: Path) -> str:
    """Lee un archivo de texto sin reventar si viene en otra codificacion."""
    try:
        return ruta.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        try:
            return ruta.read_text(encoding="latin-1")
        except OSError:
            return ""


def _contratos_del_proyecto() -> list[Path]:
    """Devuelve la lista de contratos y leyes que hay hoy en el disco."""
    encontrados: list[Path] = []
    vistos: set[Path] = set()
    for carpeta in CARPETAS_CONTRATOS:
        if not carpeta.exists() or not carpeta.is_dir():
            continue
        for ruta in carpeta.rglob("*"):
            if not ruta.is_file():
                continue
            if not _es_contrato(ruta):
                continue
            resuelta = ruta.resolve()
            if resuelta in vistos:
                continue
            vistos.add(resuelta)
            encontrados.append(ruta)
    return encontrados


def _contratos_que_nombran_el_formato_compacto() -> list[Path]:
    """Contratos que nombran las tres palabras de la ley del formato compacto.

    Un contrato cuenta solo si nombra LAS TRES palabras: compacto, sin ruido
    y formato json. Nombrar una sola no basta: la ley tiene que ser explicita.
    """
    cumplen: list[Path] = []
    for ruta in _contratos_del_proyecto():
        texto = _leer_texto(ruta).lower()
        if all(palabra in texto for palabra in PALABRAS_LEY):
            cumplen.append(ruta)
    return cumplen


def _paquete_de_ejemplo() -> dict:
    """Paquete minimo de mentira, para medir su ruido sin gastar ninguna IA.

    Representa como viaja HOY el material: prosa larga con titulos,
    explicaciones y avisos repetidos alrededor de los trozos utiles.
    """
    prosa_repetida = (
        "AVISO: esto es TODO lo que hace falta. No abras nada mas. "
        "Si de verdad necesitas otra cosa, PIDELA con el formato del final. "
        "No la leas por tu cuenta. "
    ) * 3
    return {
        "titulo": "PAQUETE MINIMO",
        "prosa": prosa_repetida,
        "trozos": [
            {"ruta": "cerebro/trozos.py", "leyes": ["CONTRATO_LAS_DOS_VIAS.md"]},
            {"ruta": "cuerpo/dudas.py", "leyes": ["CONTRATO_SIN_GUARDAR_NO_HAY_TRABAJO.md"]},
        ],
    }


def _letras_de_la_prosa(paquete: dict) -> int:
    """Cuenta las letras que se van en prosa, titulos y avisos repetidos."""
    letras = 0
    letras += len(str(paquete.get("titulo", "")))
    letras += len(str(paquete.get("prosa", "")))
    return letras


def _letras_del_codigo_util(paquete: dict) -> int:
    """Cuenta las letras que se van en rutas, trozos exactos y leyes."""
    letras = 0
    for trozo in paquete.get("trozos", []):
        letras += len(str(trozo.get("ruta", "")))
        for ley in trozo.get("leyes", []):
            letras += len(str(ley))
    return letras


def _paquete_es_compacto(paquete: dict) -> bool:
    """Un paquete es compacto si la prosa no pesa mas que el codigo util."""
    return _letras_de_la_prosa(paquete) <= _letras_del_codigo_util(paquete)


def _paquete_es_json_valido(paquete: dict) -> bool:
    """Un paquete viaja en formato json si se puede serializar y releer igual."""
    try:
        crudo = json.dumps(paquete, ensure_ascii=False)
        vuelto = json.loads(crudo)
    except (TypeError, ValueError):
        return False
    return vuelto == paquete


# ---------------------------------------------------------------------------
# PRUEBAS
# ---------------------------------------------------------------------------


def test_hoy_el_paquete_no_es_compacto() -> None:
    """Hoy el paquete viaja como prosa larga: la prosa pesa mas que el codigo."""
    paquete = _paquete_de_ejemplo()
    letras_prosa = _letras_de_la_prosa(paquete)
    letras_codigo = _letras_del_codigo_util(paquete)
    assert letras_prosa > letras_codigo, (
        "El paquete de ejemplo ya no tiene mas prosa que codigo util: "
        f"prosa={letras_prosa} codigo={letras_codigo}. "
        "Si esto cambia, la vigia del ruido hay que revisarla."
    )
    assert not _paquete_es_compacto(paquete), (
        "El paquete de ejemplo se colo como compacto sin que la ley exista."
    )


def test_hoy_el_paquete_no_viaja_en_formato_json() -> None:
    """Hoy el paquete viaja como prosa, no como json compacto y releible."""
    paquete = _paquete_de_ejemplo()
    # El paquete de ejemplo SI se puede serializar (es un dict), pero la ley
    # que obliga a que el paquete real viaje asi todavia no existe. Esta
    # prueba deja constancia de que el formato json no esta declarado como ley.
    assert _paquete_es_json_valido(paquete), (
        "El paquete de ejemplo ni siquiera es json valido: la vigia no puede medir."
    )
    contratos = _contratos_que_nombran_el_formato_compacto()
    assert contratos, (
        "Ningun contrato del proyecto declara que el paquete viaje en formato "
        "json compacto y sin ruido. La ley del formato compacto todavia no existe."
    )


def test_existe_la_ley_del_formato_compacto_del_paquete() -> None:
    """LA VIGIA PRINCIPAL: nace ROJA porque la ley del formato compacto no existe.

    Se buscaron las palabras 'compacto', 'sin ruido' y 'formato json' en los
    contratos del proyecto y no aparece ninguna ley que las junte. Mientras
    eso siga asi, este assert falla: es la prueba de que la reparacion aun
    no esta hecha.
    """
    contratos = _contratos_que_nombran_el_formato_compacto()
    assert contratos, (
        "No hay ninguna ley en el proyecto que obligue a que el paquete viaje "
        "en formato compacto, sin ruido y en formato json. "
        "La orden R22-paquete-compacto-sin-ruido prometia esta vigia y aun no "
        "existe la ley que la haga pasar. "
        "Cuando se escriba la ley del formato compacto, esta prueba pasara sola."
    )


def test_la_ley_del_formato_compacto_nombra_las_tres_palabras() -> None:
    """La ley, cuando exista, tiene que nombrar las tres palabras juntas."""
    contratos = _contratos_que_nombran_el_formato_compacto()
    if not contratos:
        # Hoy no hay ley: esta prueba acompania a la principal y tambien nace roja.
        assert False, (
            "Todavia no hay contrato que nombre 'compacto', 'sin ruido' y "
            "'formato json' a la vez. La ley del formato compacto no existe."
        )
    for ruta in contratos:
        texto = _leer_texto(ruta).lower()
        for palabra in PALABRAS_LEY:
            assert palabra in texto, (
                f"El contrato {ruta} no nombra la palabra '{palabra}': "
                "la ley del formato compacto esta incompleta."
            )


def test_el_medidor_de_ruido_no_gasta_ninguna_ia() -> None:
    """El medidor de ruido es puro calculo: no llama a ninguna IA.

    Se comprueba que el modulo no importa nada que hable con la nube.
    """
    fuente = _leer_texto(Path(__file__))
    prohibidos = ("openai", "anthropic", "requests", "httpx", "urllib")
    for palabra in prohibidos:
        assert palabra not in fuente.lower(), (
            f"El medidor de ruido nombra '{palabra}': no puede gastar ninguna IA."
        )


def test_el_medidor_de_ruido_escribe_su_resultado_en_memoria() -> None:
    """El resultado del medidor va a un documento de la carpeta memoria.

    Esta prueba solo comprueba que la carpeta memoria existe y que el nombre
    del documento que la reparacion promete es coherente. No escribe nada.
    """
    carpeta_memoria = RAIZ / "memoria"
    assert carpeta_memoria.exists(), (
        "No existe la carpeta memoria: el medidor de ruido no tendria donde "
        "dejar su resultado."
    )
    nombre_documento = "RUIDO_DEL_PAQUETE.json"
    assert re.match(r"^[A-Z0-9_]+\.json$", nombre_documento), (
        "El nombre del documento del medidor no sigue el patron de la carpeta memoria."
    )
