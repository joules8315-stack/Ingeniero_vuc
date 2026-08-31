# -*- coding: utf-8 -*-
"""VIGIA — AL LIMPIAR EL DICCIONARIO NO SE PUEDE BORRAR LO BUENO.

FALLO REAL, cazado el 2026-08-31 al aplicar la cura del diccionario envenenado:

  La cura comprobaba que el archivo existiera en el disco. Bien pensado. Pero solo sabia mirar
  DENTRO del ingeniero, asi que dio por inexistentes los sitios de OTROS proyectos y se llevo por
  delante 4 sitios de verdad de Julio (app_web.html y tres pruebas de foto_informe). De 6 entradas
  quedo 1. Se restauro a tiempo, pero por poco.

  La leccion: una cura que limpia puede hacer MAS dano que la enfermedad. Antes de borrar hay que
  estar seguro, y "no lo encuentro" NO es lo mismo que "no existe".

LO QUE SE MIDE
  1. Un archivo del propio ingeniero se reconoce.
  2. Un archivo REAL de OTRO proyecto (foto_informe, dmm) TAMBIEN se reconoce. Este es el fallo.
  3. Un archivo inventado NO se reconoce.
  4. El diccionario de verdad sigue teniendo sus sitios buenos: no se los comio nadie.
"""
import io
import json
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(AQUI, "arnes") not in sys.path:
    sys.path.insert(0, os.path.join(AQUI, "arnes"))

import diccionario as dic   # noqa: E402


def _proyectos():
    try:
        from cerebro import grafo
        return grafo.proyectos()
    except Exception:
        return {}


def test_reconoce_un_archivo_del_propio_ingeniero():
    assert dic._resolver_archivo("cuerpo/privacidad.py", "ingeniero") is not None, \
        "no reconoce un archivo del propio ingeniero que si existe"


def test_no_reconoce_lo_inventado():
    """Sin esto no serviria de nada: el veneno entro justo por aqui."""
    assert dic._resolver_archivo("a.py", "p") is None, \
        "da por bueno un sitio inventado: por ahi entro el veneno"


def test_reconoce_un_archivo_REAL_DE_OTRO_PROYECTO():
    """EL FALLO. Julio tiene mas de un proyecto, y su memoria habla de todos ellos."""
    proys = _proyectos()
    candidatos = []
    for nombre, datos in proys.items():
        if nombre == "ingeniero":
            continue
        raiz = (datos or {}).get("ruta", "")
        if not raiz or not os.path.isdir(raiz):
            continue
        for base, _, ficheros in os.walk(raiz):
            if ".git" in base:
                continue
            for f in ficheros:
                if f.endswith((".py", ".html", ".js")):
                    candidatos.append((nombre, f))
                    break
            if candidatos:
                break
        if candidatos:
            break

    if not candidatos:
        pytest.skip("no hay otro proyecto con archivos a mano para medirlo")

    proyecto, archivo = candidatos[0]
    assert dic._resolver_archivo(archivo, proyecto) is not None, (
        "no reconoce '%s', que existe de verdad en el proyecto '%s'. Asi se borraron 4 sitios "
        "buenos de Julio: 'no lo encuentro' se trato como 'no existe'" % (archivo, proyecto))


def test_el_diccionario_de_verdad_conserva_sus_sitios_buenos():
    """Se mira el cuaderno de verdad, sin tocarlo: que nadie se haya comido lo de Julio."""
    if not os.path.exists(dic.RUTA):
        pytest.skip("todavia no hay diccionario")
    with io.open(dic.RUTA, encoding="utf-8") as f:
        parejas = json.load(f)
    reales = [p for p in parejas if str(p.get("proyecto", "")) not in ("", "p")]
    assert len(reales) >= 4, (
        "el diccionario se quedo con %d sitios de proyectos de verdad. Habia 5. Algo se los "
        "comio: revisa antes de borrar" % len(reales))
