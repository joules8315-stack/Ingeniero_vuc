"""Vigia H8a: no hay puerta trasera por dentro.

Esta vigia NACE ROJA contra el estado actual del repositorio: hoy no existe
ningun candado que impida (a) que un documento de proyecto sin veredicto pase,
ni (b) que una llamada por terminal importe una pieza interna y ejecute
`registrar` o `cerrar` saltandose el arnes.

Casos que cubre:
  1. Documento de proyecto sin veredicto se frena.
  2. Llamada por terminal que importa una pieza interna y ejecuta `registrar`
     o `cerrar` se frena y queda apuntada con identidad.
  3. Reparar un archivo existente del propio arnes es la unica excepcion.
  4. Ninguna bandera, variable de entorno ni lista puede apagar el candado.

Reglas de esta vigia:
  - Usa el montaje real del paquete (no dobles de mentira).
  - Usa memoria temporal (tmp_path) para no tocar el estado real.
  - No crea ni modifica el candado, la habilidad ni otras piezas.
  - Nace roja: si el candado no existe, las comprobaciones fallan.
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Localizacion del paquete real
# ---------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parents[1]


def _cargar_modulo(ruta: Path, nombre: str):
    """Carga un modulo desde una ruta concreta sin depender del sys.path."""
    if not ruta.exists():
        return None
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    if spec is None or spec.loader is None:
        return None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _buscar_candado():
    """Busca el candado nuevo. Si no existe, devuelve None (y la vigia nace roja)."""
    candidatos = [
        RAIZ / "arnes" / "candado_puerta_trasera.py",
        RAIZ / "arnes" / "candado_no_hay_puerta_trasera_por_dentro.py",
        RAIZ / "candado_puerta_trasera.py",
        RAIZ / "candado_no_hay_puerta_trasera_por_dentro.py",
    ]
    for ruta in candidatos:
        modulo = _cargar_modulo(ruta, "candado_puerta_trasera_bajo_prueba")
        if modulo is not None:
            return modulo
    return None


def _buscar_habilidad():
    """Busca la habilidad que decide si un documento de proyecto tiene veredicto."""
    candidatos = [
        RAIZ / "skills" / "quien_sirve_de_verdad.py",
        RAIZ / "skills" / "documento_de_proyecto_tiene_veredicto.py",
    ]
    for ruta in candidatos:
        modulo = _cargar_modulo(ruta, "habilidad_veredicto_bajo_prueba")
        if modulo is not None:
            return modulo
    return None


# ---------------------------------------------------------------------------
# Caso 1: documento de proyecto sin veredicto se frena
# ---------------------------------------------------------------------------

def test_documento_de_proyecto_sin_veredicto_se_frena(tmp_path: Path):
    """Un documento de proyecto sin veredicto NO puede pasar.

    Nace roja: hoy no existe candado que lo frene.
    """
    candado = _buscar_candado()
    assert candado is not None, (
        "NECESITO_LEER: arnes/candado_puerta_trasera.py / no existe el candado / "
        "decide si un documento de proyecto sin veredicto se frena / "
        "sin el, la vigia nace roja y no puede pasar"
    )

    documento = tmp_path / "PROYECTO_SIN_VEREDICTO.md"
    documento.write_text(
        "# Proyecto\n\nEsto es un documento de proyecto sin veredicto.\n",
        encoding="utf-8",
    )

    # El candado debe exponer una funcion que decida si el documento pasa.
    assert hasattr(candado, "documento_de_proyecto_puede_pasar"), (
        "El candado no expone documento_de_proyecto_puede_pasar"
    )
    resultado = candado.documento_de_proyecto_puede_pasar(str(documento))
    assert resultado is False, (
        "Un documento de proyecto sin veredicto NO puede pasar, y el candado "
        "dijo que si"
    )


# ---------------------------------------------------------------------------
# Caso 2: llamada por terminal que importa pieza interna y ejecuta registrar/cerrar
# ---------------------------------------------------------------------------

def test_llamada_por_terminal_que_importa_pieza_interna_y_registra_se_frena(
    tmp_path: Path,
):
    """Una llamada por terminal que importa una pieza interna y ejecuta
    `registrar` se frena y queda apuntada con identidad.
    """
    candado = _buscar_candado()
    assert candado is not None, (
        "NECESITO_LEER: arnes/candado_puerta_trasera.py / no existe el candado / "
        "decide si una llamada por terminal que importa pieza interna se frena / "
        "sin el, la vigia nace roja"
    )

    # Montaje real: un script que importa una pieza interna y llama a registrar.
    pieza_interna = tmp_path / "pieza_interna.py"
    pieza_interna.write_text(
        textwrap.dedent(
            """
            REGISTROS = []

            def registrar(nombre):
                REGISTROS.append(nombre)
                return nombre
            """
        ),
        encoding="utf-8",
    )

    script = tmp_path / "llamada_terminal.py"
    script.write_text(
        textwrap.dedent(
            f"""
            import sys
            sys.path.insert(0, {str(tmp_path)!r})
            import pieza_interna
            pieza_interna.registrar('algo')
            """
        ),
        encoding="utf-8",
    )

    assert hasattr(candado, "llamada_por_terminal_puede_pasar"), (
        "El candado no expone llamada_por_terminal_puede_pasar"
    )
    resultado = candado.llamada_por_terminal_puede_pasar(
        comando=[sys.executable, str(script)],
        cwd=str(tmp_path),
    )
    assert resultado is False, (
        "Una llamada por terminal que importa pieza interna y ejecuta "
        "registrar debe frenarse"
    )

    # Y debe quedar apuntada con identidad.
    assert hasattr(candado, "ultima_anotacion"), (
        "El candado no expone ultima_anotacion para dejar rastro"
    )
    anotacion = candado.ultima_anotacion()
    assert anotacion is not None, "El candado no dejo anotacion del freno"
    assert "identidad" in anotacion, (
        "La anotacion debe incluir la identidad de quien intento la llamada"
    )


def test_llamada_por_terminal_que_importa_pieza_interna_y_cierra_se_frena(
    tmp_path: Path,
):
    """Igual que el caso anterior pero con `cerrar`."""
    candado = _buscar_candado()
    assert candado is not None, (
        "NECESITO_LEER: arnes/candado_puerta_trasera.py / no existe el candado / "
        "decide si una llamada por terminal que importa pieza interna se frena / "
        "sin el, la vigia nace roja"
    )

    pieza_interna = tmp_path / "pieza_interna.py"
    pieza_interna.write_text(
        textwrap.dedent(
            """
            CERRADOS = []

            def cerrar(nombre):
                CERRADOS.append(nombre)
                return nombre
            """
        ),
        encoding="utf-8",
    )

    script = tmp_path / "llamada_terminal.py"
    script.write_text(
        textwrap.dedent(
            f"""
            import sys
            sys.path.insert(0, {str(tmp_path)!r})
            import pieza_interna
            pieza_interna.cerrar('algo')
            """
        ),
        encoding="utf-8",
    )

    assert hasattr(candado, "llamada_por_terminal_puede_pasar"), (
        "El candado no expone llamada_por_terminal_puede_pasar"
    )
    resultado = candado.llamada_por_terminal_puede_pasar(
        comando=[sys.executable, str(script)],
        cwd=str(tmp_path),
    )
    assert resultado is False, (
        "Una llamada por terminal que importa pieza interna y ejecuta "
        "cerrar debe frenarse"
    )


# ---------------------------------------------------------------------------
# Caso 3: reparar archivo existente del propio arnes es la unica excepcion
# ---------------------------------------------------------------------------

def test_reparar_archivo_existente_del_propio_arnes_es_la_unica_excepcion(
    tmp_path: Path,
):
    """Reparar un archivo existente del propio arnes SI puede pasar."""
    candado = _buscar_candado()
    assert candado is not None, (
        "NECESITO_LEER: arnes/candado_puerta_trasera.py / no existe el candado / "
        "decide la excepcion de reparar archivo del arnes / "
        "sin el, la vigia nace roja"
    )

    archivo_arnes = tmp_path / "arnes" / "pieza_del_arnes.py"
    archivo_arnes.parent.mkdir(parents=True, exist_ok=True)
    archivo_arnes.write_text("# pieza del arnes\n", encoding="utf-8")

    assert hasattr(candado, "reparar_archivo_del_arnes_puede_pasar"), (
        "El candado no expone reparar_archivo_del_arnes_puede_pasar"
    )
    resultado = candado.reparar_archivo_del_arnes_puede_pasar(
        str(archivo_arnes)
    )
    assert resultado is True, (
        "Reparar un archivo existente del propio arnes es la unica excepcion "
        "y debe poder pasar"
    )

    # Y un archivo que NO es del arnes no puede pasar por esa excepcion.
    archivo_ajeno = tmp_path / "otro" / "pieza_ajena.py"
    archivo_ajeno.parent.mkdir(parents=True, exist_ok=True)
    archivo_ajeno.write_text("# pieza ajena\n", encoding="utf-8")
    resultado_ajeno = candado.reparar_archivo_del_arnes_puede_pasar(
        str(archivo_ajeno)
    )
    assert resultado_ajeno is False, (
        "La excepcion es SOLO para archivos del propio arnes"
    )


# ---------------------------------------------------------------------------
# Caso 4: ninguna bandera, variable ni lista puede apagar el candado
# ---------------------------------------------------------------------------

def test_ninguna_bandera_variable_ni_lista_apaga_el_candado(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Aunque se pongan banderas, variables de entorno o listas de permiso,
    el candado sigue frenando.
    """
    candado = _buscar_candado()
    assert candado is not None, (
        "NECESITO_LEER: arnes/candado_puerta_trasera.py / no existe el candado / "
        "decide si banderas o listas pueden apagarlo / "
        "sin el, la vigia nace roja"
    )

    documento = tmp_path / "PROYECTO_SIN_VEREDICTO.md"
    documento.write_text(
        "# Proyecto\n\nDocumento sin veredicto.\n", encoding="utf-8"
    )

    # Bandera de entorno.
    monkeypatch.setenv("INGENIERO_PERMITIR_SIN_VEREDICTO", "1")
    monkeypatch.setenv("INGENIERO_SALTAR_CANDADO", "1")
    monkeypatch.setenv("INGENIERO_MODO_DIOS", "1")

    # Bandera en el propio modulo, si existe.
    for nombre in (
        "PERMITIR_SIN_VEREDICTO",
        "SALTAR_CANDADO",
        "MODO_DIOS",
        "DESACTIVADO",
    ):
        if hasattr(candado, nombre):
            monkeypatch.setattr(candado, nombre, True, raising=False)

    # Lista de permiso, si existe.
    for nombre in ("PERMITIDOS", "EXCEPCIONES", "LISTA_BLANCA"):
        if hasattr(candado, nombre):
            try:
                monkeypatch.setattr(
                    candado, nombre, [str(documento)], raising=False
                )
            except Exception:
                pass

    assert hasattr(candado, "documento_de_proyecto_puede_pasar"), (
        "El candado no expone documento_de_proyecto_puede_pasar"
    )
    resultado = candado.documento_de_proyecto_puede_pasar(str(documento))
    assert resultado is False, (
        "Ninguna bandera, variable ni lista puede apagar el candado"
    )


def test_la_habilidad_de_veredicto_existe_y_es_la_que_decide():
    """La habilidad que decide si un documento tiene veredicto debe existir.

    Nace roja si la habilidad no esta.
    """
    habilidad = _buscar_habilidad()
    assert habilidad is not None, (
        "NECESITO_LEER: skills/quien_sirve_de_verdad.py / no existe la habilidad / "
        "decide si un documento de proyecto tiene veredicto / "
        "sin ella, la vigia nace roja"
    )
    assert hasattr(habilidad, "tiene_veredicto"), (
        "La habilidad no expone tiene_veredicto"
    )


# ---------------------------------------------------------------------------
# Comprobacion de que la vigia nace roja contra el estado actual
# ---------------------------------------------------------------------------

def test_la_vigia_nace_roja_contra_el_estado_actual():
    """Si el candado no existe todavia, esta comprobacion lo deja claro.

    Cuando el candado exista, esta comprobacion pasara a verde sola.
    """
    candado = _buscar_candado()
    if candado is None:
        pytest.fail(
            "La vigia nace ROJA: todavia no existe el candado "
            "arnes/candado_puerta_trasera.py. Hay que crearlo para que "
            "esta vigia pueda pasar a verde."
        )
    assert hasattr(candado, "documento_de_proyecto_puede_pasar")
    assert hasattr(candado, "llamada_por_terminal_puede_pasar")
    assert hasattr(candado, "reparar_archivo_del_arnes_puede_pasar")
