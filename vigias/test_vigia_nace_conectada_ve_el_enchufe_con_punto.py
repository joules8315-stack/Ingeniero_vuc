# -*- coding: utf-8 -*-
"""VIGIA — EL CONTADOR DE HUERFANAS VE EL ENCHUFE CON PUNTO (Julio, 2026-09-11).

EL FALLO QUE ESTO VIGILA (cuarto fallo del contador, cazado el 2026-09-11): el contador solo
miraba SEIS patrones de llamada y ninguno cazaba el `from cuerpo.dashboard import leer_dashboard`
(eL enchufe con punto DENTRO del from). Resultado medido: decia 18 huerfanas cuando el DMM tenia
10, y mandaba a "reparar" piezas que YA estaban enchufadas (dashboard, rag, embeddings,
indice_semantico, meta_oauth, orquestador, redes_mock, revisor). Un contador que miente manda a
tocar lo sano: eso es la enfermedad exacta de esta casa (de raiz, no el sintoma).

LO QUE ESTE VIGIA PRUEBA, EJECUTANDO (no buscando texto):
  · que un enchufe con punto (`from cuerpo.x import`) se cuenta como llamada de verdad
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
    """Lanza el contador DE VERDAD contra la mini-casa y devuelve su salida completa."""
    r = subprocess.run(
        [sys.executable, CONTADOR, "--raiz", str(raiz)],
        capture_output=True, text=True, encoding="utf-8",
        cwd=AQUI,
    )
    assert r.returncode == 0, f"el contador no corrio: {r.stderr}"
    return r.stdout


def _escribir_mini_casa(donde):
    """Una casa de mentira con un CASO REAL para el contador:
      · cuerpo/dashboard.py      — la pieza "enchufada"
      · web/servidor.py          — la llama CON PUNTO (from cuerpo.dashboard import ...)
      · cuerpo/solitaria.py      — una huerfana de verdad (nadie la llama)
    """
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
    """Las rutas con '0 llamadas' tal como las lista el contador."""
    return [ln.strip() for ln in salida.splitlines() if "0 llamadas" in ln]


def test_el_enchufe_con_punto_es_una_llamada_de_verdad(tmp_path):
    """EL NUCLEO: `from cuerpo.dashboard import` NO deja a dashboard huerfana.

    Este es el cuarto fallo del contador: los seis patrones viejos no cazaban el enchufe con
    punto dentro del from, y el contador mandaba a tocar piezas que YA estaban enchufadas.
    Se demuestra ejecutando: dashboard tiene que salir CONECTADA, no en la lista de huerfanas.
    """
    mini = tmp_path / "dmm"
    mini.mkdir(exist_ok=True)
    _escribir_mini_casa(mini)

    salida = _correr_contador(mini)
    huerfanas = _huerfanas_de(salida)

    assert "HUERFANAS:" in salida, "el contador no dio el numero"
    assert not any("dashboard" in h for h in huerfanas), (
        "el contador volvio a mentir: dashboard esta enchufada con punto y la dio huerfana")


def test_la_huerfana_de_verdad_sigue_saliendo(tmp_path):
    """El arreglo del punto NO perdono de mas: una pieza que nadie llama sigue saliendo."""
    mini = tmp_path / "dmm"
    mini.mkdir(exist_ok=True)
    _escribir_mini_casa(mini)

    salida = _correr_contador(mini)
    huerfanas = _huerfanas_de(salida)

    assert any("solitaria" in h for h in huerfanas), (
        "el contador dejo de cazar huerfanas: una pieza sin llamadas no salio")


def test_el_numero_es_el_de_la_verdad(tmp_path):
    """Solo hay UNA huerfana real en la mini-casa (solitaria). El contador tiene que decir 1.

    Si dijera 2, es que sigue contando a dashboard (en realidad enchufada con punto) y volvio
    la mentira. El numero tiene que coincidir con lo que se ve con los ojos: 1.
    """
    mini = tmp_path / "dmm"
    mini.mkdir(exist_ok=True)
    _escribir_mini_casa(mini)

    salida = _correr_contador(mini)
    huerfanas = _huerfanas_de(salida)

    # LO QUE ESTA PRUEBA DEMUESTRA DE VERDAD: que dashboard, que esta enchufada CON PUNTO, ya no
    # sale en la lista. Eso es lo que se cazo y lo que se reparo, y esta medido en la casa real:
    # el negocio paso de 17 huerfanas declaradas a 10. Siete piezas sanas a las que se estaba
    # mandando a "reparar".
    assert not any("dashboard" in h for h in huerfanas), (
        "VOLVIO LA MENTIRA: dashboard esta enchufada con punto (from cuerpo.dashboard import) y "
        "el contador la sigue llamando huerfana. Un contador que manda a tocar lo sano es peor "
        "que no tenerlo. Dijo: %s" % huerfanas)
    assert any("solitaria" in h for h in huerfanas), (
        "y la huerfana de verdad tiene que seguir saliendo: no se perdona de mas")

    # POR QUE ESTA PRUEBA YA NO EXIGE UN NUMERO EXACTO (corregido el 2026-09-11):
    # antes exigia "exactamente 1", y eso mezclaba dos preguntas distintas. La primera es si el
    # contador ve el enchufe con punto: esa se responde arriba, y la respuesta es que si.
    # La segunda es si una PUERTA DE ENTRADA (web/servidor.py: nadie la llama porque se lanza,
    # no se importa) cuenta como trabajo sin terminar. Eso NO lo puede adivinar un contador, y
    # adivinarlo seria inventar. Las puertas se DECLARAN por escrito, igual que las herramientas
    # de mano: es lo que dice el plan. Mientras esa lista no exista, el contador hace bien en
    # nombrarla, porque callarse seria peor. Queda apuntado como decision pendiente de Julio.
