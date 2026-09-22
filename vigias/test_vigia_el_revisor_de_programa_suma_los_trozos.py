# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_revisor_de_programa_suma_los_trozos.py

VIGIA de arnes/revisor_de_programa.py::revisar(propuesta, tarea).

QUE VIGILA
----------
Que el revisor SUMA los trozos de la propuesta antes de juzgar: cuando la tarea pide
cambiar varias funciones y cada trozo trae UNA entera, el revisor no puede mirar cada
trozo suelto y decir que no hace lo que se pidio. Tiene que juntarlos y ver el texto
resultante.

Y que sigue FRENANDO cuando la tarea nombra una pieza que NINGUN trozo toca: si la
tarea dice 'cambia uno_a, uno_b y otro_c' y los trozos solo tocan uno_a y uno_b, el
revisor tiene que avisar con 'NO HACE LO QUE SE PIDIO' y nombrar 'otro_c'.

COMO SE CARGA
-------------
Se carga el modulo por ruta con importlib, igual que hace la vigia hermana
vigias/test_vigia_el_revisor_de_programa_revisa_cada_trozo.py, para no depender de que
el paquete arnes este en el camino de importacion.

NO TOCA NINGUN OTRO ARCHIVO.
"""
import importlib.util
import os
import sys


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_REVISOR = os.path.join(RAIZ, "arnes", "revisor_de_programa.py")

SALTO = "\n"


def _cargar_revisor():
    """Carga arnes/revisor_de_programa.py por ruta y devuelve el modulo."""
    if RAIZ not in sys.path:
        sys.path.insert(0, RAIZ)
    spec = importlib.util.spec_from_file_location(
        "revisor_de_programa_bajo_vigia_suma", RUTA_REVISOR)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _escribir_m(ruta):
    """Escribe m.py con las tres funciones del caso, tal y como pide la tarea."""
    texto = (
        "def uno_a():" + SALTO +
        "    return 1" + SALTO +
        SALTO +
        "def uno_b():" + SALTO +
        "    return 2" + SALTO +
        SALTO +
        "def otro_c():" + SALTO +
        "    return 3" + SALTO
    )
    with open(str(ruta), "w", encoding="utf-8") as f:
        f.write(texto)
    return texto


def _propuesta(ruta):
    """La propuesta del caso: dos trozos, cada uno con la funcion entera.

    El trozo de uno_a la deja devolviendo 10 y el de uno_b la deja devolviendo 20.
    Ningun trozo toca otro_c.
    """
    return {
        "archivo": str(ruta),
        "texto_viejo": "",
        "texto_nuevo": "",
        "cambios": [
            {
                "texto_viejo": "def uno_a():" + SALTO + "    return 1" + SALTO,
                "texto_nuevo": "def uno_a():" + SALTO + "    return 10" + SALTO,
            },
            {
                "texto_viejo": "def uno_b():" + SALTO + "    return 2" + SALTO,
                "texto_nuevo": "def uno_b():" + SALTO + "    return 20" + SALTO,
            },
        ],
    }


def _textos(fallos):
    """Los fallos como lista de textos, sea cual sea la forma en que vengan."""
    if fallos is None:
        return []
    if isinstance(fallos, str):
        return [fallos]
    fuera = []
    for f in fallos:
        if isinstance(f, str):
            fuera.append(f)
        else:
            fuera.append(str(f))
    return fuera


def test_suma_los_trozos_y_no_frena_cuando_la_tarea_los_nombra(tmp_path):
    """(1) La tarea pide uno_a y uno_b; los dos trozos los tocan: no puede frenar."""
    revisor = _cargar_revisor()
    ruta = tmp_path / "m.py"
    _escribir_m(ruta)

    propuesta = _propuesta(ruta)
    tarea = "cambia uno_a y uno_b"

    fallos = revisor.revisar(propuesta, tarea)
    textos = _textos(fallos)

    for t in textos:
        assert "NO HACE LO QUE SE PIDIO" not in t, (
            "el revisor frena cuando los dos trozos SI tocan lo que la tarea pide: %r" % t)


def test_sigue_frenando_si_la_tarea_nombra_una_pieza_que_ningun_trozo_toca(tmp_path):
    """(2) La tarea pide tambien otro_c y ningun trozo la toca: tiene que frenar."""
    revisor = _cargar_revisor()
    ruta = tmp_path / "m.py"
    _escribir_m(ruta)

    propuesta = _propuesta(ruta)
    tarea = "cambia uno_a, uno_b y otro_c"

    fallos = revisor.revisar(propuesta, tarea)
    textos = _textos(fallos)

    hay_freno = any("NO HACE LO QUE SE PIDIO" in t for t in textos)
    assert hay_freno, (
        "el revisor NO frena aunque la tarea nombra otro_c y ningun trozo la toca: %r"
        % (textos,))

    hay_nombre = any("otro_c" in t for t in textos)
    assert hay_nombre, (
        "el revisor frena pero no nombra la pieza que falta (otro_c): %r" % (textos,))
