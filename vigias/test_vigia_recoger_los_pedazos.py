"""Vigia de arnes/recoger_los_pedazos.py.

Cuando el guardia no deja guardar un trabajo aprobado, la copia buena se aparta en
memoria/trabajos_sin_revisar con el final .FRENADO_POR_EL_GUARDIA. Hoy Claude la devuelve
a su sitio A MANO decenas de veces por noche, y eso es mecanico, o sea que se programa
(orden A-39 de Julio del 2026-09-20).

Esta pieza nace ROJA porque arnes/recoger_los_pedazos.py todavia no existe. Cuando exista,
comprobara tres cosas:
  1. Que la funcion pedazos lista los archivos acabados en .FRENADO_POR_EL_GUARDIA.
  2. Que la funcion recoger devuelve la copia buena a su sitio y limpia el apartado.
  3. Que sin saber de donde venia la copia NO se toca nada.
"""

import json
import os
import sys

# La raiz del proyecto: dos dirname sobre el abspath de este mismo archivo.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARNES = os.path.join(RAIZ, "arnes")

if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
if ARNES not in sys.path:
    sys.path.insert(0, ARNES)

import recoger_los_pedazos


SUFIJO_FRENADO = ".FRENADO_POR_EL_GUARDIA"


def _armar_casa(tmp_path):
    """Arma una casa de mentira con la copia apartada, el aprobado y el cuerpo original.

    Devuelve el texto de la ruta de esa casa.
    """
    casa = os.path.join(str(tmp_path), "casa")

    sin_revisar = os.path.join(casa, "memoria", "trabajos_sin_revisar")
    os.makedirs(sin_revisar, exist_ok=True)
    with open(os.path.join(sin_revisar, "pieza.py" + SUFIJO_FRENADO), "w", encoding="utf-8") as f:
        f.write("nuevo")

    del_equipo = os.path.join(casa, "memoria", "trabajos_del_equipo")
    os.makedirs(del_equipo, exist_ok=True)
    aprobado = {"propuesta": {"archivo": "cuerpo/pieza.py"}}
    with open(os.path.join(del_equipo, "2026-09-20_000000_APROBADO_pieza.py.json"), "w", encoding="utf-8") as f:
        json.dump(aprobado, f)

    cuerpo = os.path.join(casa, "cuerpo")
    os.makedirs(cuerpo, exist_ok=True)
    with open(os.path.join(cuerpo, "pieza.py"), "w", encoding="utf-8") as f:
        f.write("viejo")

    return casa


def _leer(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def test_pedazos_lista_la_copia_frenada(tmp_path):
    """La funcion pedazos devuelve una lista con un solo nombre acabado en el sufijo."""
    casa = _armar_casa(tmp_path)
    nombres = recoger_los_pedazos.pedazos(casa)
    assert isinstance(nombres, list), (
        "pedazos no devolvio una lista: si el programa no ve la copia apartada, el trabajo "
        "aprobado se queda apartado y alguien tiene que ir a buscarlo a mano")
    assert len(nombres) == 1, (
        "pedazos devolvio %d nombres y solo hay una copia apartada: si el programa no ve la "
        "copia buena, el trabajo aprobado se queda apartado y alguien tiene que ir a buscarlo "
        "a mano" % len(nombres))
    assert nombres[0].endswith(SUFIJO_FRENADO), (
        "el nombre devuelto no acaba en %s: si el programa no reconoce la copia apartada, el "
        "trabajo aprobado se queda apartado y alguien tiene que ir a buscarlo a mano" % SUFIJO_FRENADO)


def test_recoger_devuelve_la_copia_a_su_sitio(tmp_path):
    """Recoger devuelve la copia buena a su sitio y limpia el apartado."""
    casa = _armar_casa(tmp_path)
    resultado = recoger_los_pedazos.recoger(casa, "pieza.py" + SUFIJO_FRENADO)

    assert isinstance(resultado, dict) and resultado.get("ok") is True, (
        "recoger no devolvio ok verdadero: si el programa no devuelve la copia buena a su "
        "sitio, el trabajo aprobado se queda apartado y alguien tiene que ir a buscarlo a mano")

    cuerpo = os.path.join(casa, "cuerpo", "pieza.py")
    assert _leer(cuerpo) == "nuevo", (
        "cuerpo/pieza.py sigue sin la copia buena: si el programa no devuelve la copia buena a "
        "su sitio, el trabajo aprobado se queda apartado y alguien tiene que ir a buscarlo a mano")

    sin_revisar = os.path.join(casa, "memoria", "trabajos_sin_revisar")
    restos = [n for n in os.listdir(sin_revisar) if n.endswith(SUFIJO_FRENADO)]
    assert restos == [], (
        "todavia quedan copias apartadas %r: si el programa no devuelve la copia buena a su "
        "sitio, el trabajo aprobado se queda apartado y alguien tiene que ir a buscarlo a mano" % restos)


def test_sin_saber_de_donde_venia_no_se_toca_nada(tmp_path):
    """Sin el aprobado que dice de donde venia, recoger falla y no toca el cuerpo."""
    casa = _armar_casa(tmp_path)

    del_equipo = os.path.join(casa, "memoria", "trabajos_del_equipo")
    os.remove(os.path.join(del_equipo, "2026-09-20_000000_APROBADO_pieza.py.json"))

    resultado = recoger_los_pedazos.recoger(casa, "pieza.py" + SUFIJO_FRENADO)

    assert isinstance(resultado, dict) and resultado.get("ok") is False, (
        "recoger no devolvio ok falso cuando nadie sabe de donde venia la copia: si el programa "
        "no devuelve la copia buena a su sitio, el trabajo aprobado se queda apartado y alguien "
        "tiene que ir a buscarlo a mano")

    razon = resultado.get("razon")
    assert isinstance(razon, str) and razon.strip() != "", (
        "recoger no explico por que no pudo devolver la copia: si el programa no devuelve la "
        "copia buena a su sitio, el trabajo aprobado se queda apartado y alguien tiene que ir "
        "a buscarlo a mano")

    cuerpo = os.path.join(casa, "cuerpo", "pieza.py")
    assert _leer(cuerpo) == "viejo", (
        "cuerpo/pieza.py se toco sin saber de donde venia la copia: si el programa no devuelve "
        "la copia buena a su sitio, el trabajo aprobado se queda apartado y alguien tiene que "
        "ir a buscarlo a mano")
