# -*- coding: utf-8 -*-
"""VIGIA — LA LISTA BLANCA NO ES UNA PUERTA TRASERA. NUNCA.

JULIO, 2026-09-11, decidiendo:
    "Si, que la lista blanca solo sirva para esa pieza que dijiste, lo demas no. Legislalo, pon
     candado, vigilalo y que se cumpla, que nada se cuele por alli, NUNCA, que no sea una puerta
     trasera, nunca. Mira si se puede programar, para no introducir IA."

DE DONDE SALE: el contador de piezas dormidas necesitaba poder perdonar a las HERRAMIENTAS DE
MANO, las que se lanzan a proposito y por eso nadie las llama desde el codigo. Sin eso, su lista
nunca llegaria a cero y opencode se quedo parado siete horas y media esperando la decision.

PERO UNA LISTA BLANCA ES UNA PUERTA TRASERA. Si ahi se puede meter cualquier cosa, deja de
contarse, nadie la enchufa nunca, y el contador vuelve a mentir. Seria la enfermedad de este dia
entero —algo que se pierde en silencio— pero entrando por detras Y CON PERMISO.

MEDIDO ANTES DE DECIDIR: de las nueve piezas dormidas del negocio, SOLO UNA se puede lanzar a
mano (el compilador del mapa). Las otras OCHO no tienen ni forma de arrancarse: no son
herramientas, son trabajo sin terminar. La lista blanca resuelve 1 de 9, no 9.

LOS TRES CANDADOS, y ninguno se negocia:
  1. SOLO ENTRA LO QUE DE VERDAD SE PUEDE LANZAR. Lo comprueba una MAQUINA mirando el archivo,
     no la palabra de nadie. Es una cuenta: no entra ninguna IA.
  2. CADA UNA ESCRIBE POR QUE ESTA Y QUIEN LA LANZA. Sin motivo escrito, no entra.
  3. ESTA VIGIA. Si una listada deja de poder lanzarse, o alguien mete una sin motivo, ROJA.

COMO SE PRUEBA: se EJECUTA el camino real contra casas de mentira. No se busca ninguna palabra
dentro de ningun archivo, no se llama a ningun cerebro, y el resultado es el mismo las mil veces.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)


def _lb():
    """La pieza, cargada POR SU SITIO y no por su nombre.

    CHOQUE DE NOMBRES CAZADO EL 2026-09-11: en esta casa hay DOS cosas llamadas igual, la carpeta
    skills/ y el archivo cuerpo/skills.py. Cuando otra prueba carga el archivo, el nombre queda
    ocupado y "from skills import lista_blanca" deja de encontrar nada. Por eso estas cinco
    vigias pasaban solas y fallaban con la suite entera: el clasico verde de mentira al reves.

    Se carga por la RUTA del archivo, que no se puede confundir con nada. Y asi la prueba deja de
    depender de en que orden corran las demas, que es lo que exige una vigia que no miente.
    """
    import importlib.util
    ruta = os.path.join(AQUI, "skills", "lista_blanca.py")
    if not os.path.exists(ruta):
        pytest.fail(
            "NO EXISTE skills/lista_blanca.py. Sin el, o el contador miente (cuenta como dormida "
            "una herramienta de mano) o hay que perdonar a mano, que es la puerta trasera que "
            "Julio prohibio.")
    spec = importlib.util.spec_from_file_location("lista_blanca_por_su_sitio", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_una_pieza_QUE_SE_PUEDE_LANZAR_y_con_motivo_entra(tmp_path):
    """El caso bueno: el compilador del mapa. Se lanza a mano y se dice por que."""
    lb = _lb()
    pieza = tmp_path / "compilar_mapa.py"
    pieza.write_text("def compilar():\n    return 1\n\n\nif __name__ == '__main__':\n"
                     "    compilar()\n", encoding="utf-8")
    ok, motivo = lb.puede_entrar(str(pieza), porque="se lanza a mano al sellar", quien="Julio")
    assert ok, "no dejo entrar a una herramienta que SI se puede lanzar y trae su motivo: %s" % motivo


def test_lo_que_NO_SE_PUEDE_LANZAR_NO_entra_jamas(tmp_path):
    """LOS OCHO CASOS DE HOY. No son herramientas: son trabajo sin terminar."""
    lb = _lb()
    pieza = tmp_path / "director.py"
    pieza.write_text("def armar_plan():\n    return {}\n", encoding="utf-8")
    ok, motivo = lb.puede_entrar(str(pieza), porque="es una herramienta, de verdad",
                                 quien="quien sea")
    assert not ok, (
        "SE COLO POR LA PUERTA TRASERA. Esa pieza NO SE PUEDE LANZAR: no es una herramienta de "
        "mano, es trabajo sin terminar. Si entra, deja de contarse y NADIE LA ENCHUFA NUNCA, que "
        "es exactamente lo que Julio prohibio para siempre")
    assert motivo, "la rechazo sin decir por que"


def test_SIN_MOTIVO_ESCRITO_no_entra(tmp_path):
    """Segundo candado: sin decir por que esta y quien la lanza, no entra."""
    lb = _lb()
    pieza = tmp_path / "medir.py"
    pieza.write_text("if __name__ == '__main__':\n    print(1)\n", encoding="utf-8")
    ok, _ = lb.puede_entrar(str(pieza), porque="", quien="Julio")
    assert not ok, "entro sin motivo escrito: manana nadie sabra por que esta ahi"
    ok, _ = lb.puede_entrar(str(pieza), porque="se lanza a mano", quien="")
    assert not ok, "entro sin decir QUIEN la lanza"


def test_LA_LISTA_DE_VERDAD_esta_limpia():
    """El estado real de la casa: ninguna listada puede haber dejado de poder lanzarse.

    Esta es la que muerde con el tiempo: hoy una pieza se lanza a mano, manana alguien le quita
    esa puerta y la lista la sigue perdonando en silencio. Aqui se pone ROJA.
    """
    lb = _lb()
    malas = lb.revisar()
    assert not malas, (
        "HAY PIEZAS EN LA LISTA BLANCA QUE YA NO DEBERIAN ESTAR. O dejaron de poder lanzarse, o "
        "no dicen por que estan. Cada una de estas es una pieza que dejo de contarse y que nadie "
        "va a enchufar nunca: %s" % malas)


def test_NO_ENTRA_NINGUNA_IA_en_esta_decision(tmp_path):
    """Julio: 'mira si se puede programar, para no introducir IA'. Se puede: es una cuenta.

    Se comprueba EJECUTANDO: se le da la misma pieza cinco veces y tiene que contestar lo mismo
    las cinco. Un juicio de IA no da siempre lo mismo; una cuenta si.
    """
    lb = _lb()
    pieza = tmp_path / "x.py"
    pieza.write_text("if __name__ == '__main__':\n    print(1)\n", encoding="utf-8")
    respuestas = {lb.puede_entrar(str(pieza), porque="se lanza a mano", quien="Julio")[0]
                  for _ in range(5)}
    assert len(respuestas) == 1, (
        "la misma pregunta da respuestas distintas: eso es un juicio, no una cuenta, y aqui "
        "Julio pidio expresamente que fuera un programa")
