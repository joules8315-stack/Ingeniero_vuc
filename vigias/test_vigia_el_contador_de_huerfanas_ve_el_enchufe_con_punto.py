# -*- coding: utf-8 -*-
"""VIGIA — EL CONTADOR DE HUERFANAS VE EL ENCHUFE CON PUNTO (Julio, 2026-09-11).

EL FALLO QUE ESTO VIGILA (cuarto fallo del contador, cazado el 2026-09-11): el contador solo
miraba SEIS patrones de llamada y ninguno cazaba el `from cuerpo.dashboard import ...` (el
enchufe con punto DENTRO del from). Resultado medido: decia 18 huerfanas cuando el DMM tenia 10,
y mandaba a "reparar" piezas que YA estaban enchufadas (dashboard, rag, embeddings,
indice_semantico, meta_oauth, orquestador, redes_mock, revisor). Un contador que miente manda a
tocar lo sano: y tocar lo sano es exactamente la enfermedad de esta casa (de raiz, no el sintoma).

LO QUE ESTE VIGIA PRUEBA, EJECUTANDO (no buscando texto):
  · que un enchufe con punto (`from cuerpo.dashboard import`) se cuenta como llamada de verdad
  · que una pieza genuinamente huerfana SIGUE saliendo (el contador no perdono de mas)
  · que el numero de huerfanas es el real, comparado con la VERDAD de la mini-casa de prueba

Nunca toca la casa real: levanta su propia mini-casa en una carpeta temporal y le apunta el
contador con --raiz. La prueba es que el numero que devuelve es el que se ve con los ojos.
"""
import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTADOR = os.path.join(AQUI, "skills", "nace_conectada.py")


def _correr_contador(raiz):
    r = subprocess.run(
        [sys.executable, CONTADOR, "--raiz", str(raiz)],
        capture_output=True, text=True, encoding="utf-8",
        cwd=AQUI,
    )
    assert r.returncode == 0, f"el contador no corrio: {r.stderr}"
    return r.stdout


def _escribir_mini_casa(donde):
    (donde / "cuerpo").mkdir(exist_ok=True)
    (donde / "web").mkdir(exist_ok=True)
    (donde / "cuerpo" / "dashboard.py").write_text(
        "def leer_dashboard():\n    return {}\n", encoding="utf-8")
    (donde / "cuerpo" / "solitaria.py").write_text(
        "def nadie_me_llama():\n    return 1\n", encoding="utf-8")
    (donde / "web" / "servidor.py").write_text(
        "from cuerpo.dashboard import leer_dashboard\n\n"
        "def servir():\n    return leer_dashboard()\n", encoding="utf-8")


def _huerfanas_de(salida):
    return [ln.strip() for ln in salida.splitlines() if "0 llamadas" in ln]


def test_el_enchufe_con_punto_es_una_llamada_de_verdad(tmp_path):
    """EL NUCLEO: `from cuerpo.dashboard import` NO deja a dashboard huerfana.

    Este es el cuarto fallo del contador: los seis patrones viejos no cazaban el enchufe con
    punto dentro del from, y el contador mandaba a reparar lo que ya estaba enchufado. Se
    demuestra ejecutando: dashboard tiene que salir CONECTADA, no en la lista de huerfanas.
    """
    _escribir_mini_casa(tmp_path)

    salida = _correr_contador(tmp_path)
    huerfanas = _huerfanas_de(salida)

    assert "HUERFANAS:" in salida, "el contador no dio el numero"
    assert not any("dashboard" in h for h in huerfanas), (
        "el contador volvio a mentir: dashboard esta enchufada con punto y la dio huerfana")


def test_la_huerfana_de_verdad_sigue_saliendo(tmp_path):
    """El arreglo del punto NO perdono de mas: una pieza que nadie llama sigue saliendo."""
    _escribir_mini_casa(tmp_path)

    salida = _correr_contador(tmp_path)
    huerfanas = _huerfanas_de(salida)

    assert any("solitaria" in h for h in huerfanas), (
        "el contador dejo de cazar huerfanas: una pieza sin llamadas no salio")


def test_el_numero_es_el_de_la_verdad(tmp_path):
    """La mini-casa tiene DOS huerfanas reales: solitaria y servidor (a servidor nadie lo llama).
    El contador tiene que decir 2, NI MAS NI MENOS. Y dashboard tiene que estar FUERA de la lista
    aunque su nombre aparece escrito con punto dentro del from: ese era el enchufe que el contador
    no veia y por el que mandaba a reparar lo que no estaba roto.
    """
    _escribir_mini_casa(tmp_path)

    salida = _correr_contador(tmp_path)
    primera = next(ln for ln in salida.splitlines() if ln.startswith("HUERFANAS:"))
    n = int(primera.split(":")[1].split("de")[0].strip())
    huerfanas = _huerfanas_de(salida)

    # dashboard NO puede estar: esta enchufada con punto (from cuerpo.dashboard import)
    assert not any("dashboard" in h for h in huerfanas), (
        "el contador volvio a mentir: dashboard esta enchufada con punto y la dio huerfana")
    # y el numero tiene que ser el de la verdad, contado con los ojos: 2
    assert n == 2, (
        f"el contador dice {n} huerfanas y la verdad de la mini-casa es 2 (solitaria y servidor, "
        f"a los dos nadie los llama; dashboard esta enchufada con punto)")
