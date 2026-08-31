# -*- coding: utf-8 -*-
"""VIGIA — LA PIEZA SE BUSCA POR NOMBRE, NUNCA POR NUMERO DE LINEA.

Julio lo repitio muchas veces y seguia sin repararse (2026-08-31):
  "lo que borra todo, que cuenta por lineas, por que no lo reemplazas, por que lo busque por
   funcion y nombre, para que asi identifique las lineas correctas... si en definitiva no se
   puede buscar por numero, que se elimine esa instruccion y quede buscando por funcion y nombre,
   ya que el numero esta constantemente cambiando."

QUE MEDIMOS (no lo que decimos, lo que hace):
  1. Existe una forma de pedir una funcion POR SU NOMBRE y que llegue COMPLETA.
  2. Si el nombre no existe, se contesta que no esta. NO se inventa un pedazo.
  3. La funcion llega con su sitio REAL (desde/hasta de verdad), no con numeros inventados.
  4. El repartidor ya NO lleva numeros de linea escritos a mano para encontrar `armar`.
  5. Con el archivo cambiado de tamano (se le meten lineas por delante), se sigue acertando.
     Este es EL punto: es lo que rompia el numero fijo.

ESTA VIGIA NACE ROJA. Mide el codigo de verdad, no un texto de contrato.
"""
import io
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from cerebro import piezas   # noqa: E402

ROUTER = os.path.join(AQUI, "cerebro", "router.py")

ARCHIVO_DE_MENTIRA = '''# -*- coding: utf-8 -*-
"""Cabecera del archivo."""
import os


CONSTANTE = 3


def primera(a):
    """La de arriba."""
    if a:
        return 1
    return 0


def armar(proyecto, problema):
    """La que hay que traer entera."""
    x = 1
    for i in range(3):
        x += i
    return {"proyecto": proyecto, "problema": problema, "x": x}


def ultima():
    return "fin"
'''


@pytest.fixture
def archivo(tmp_path):
    p = tmp_path / "falso.py"
    p.write_text(ARCHIVO_DE_MENTIRA, encoding="utf-8")
    return str(p)


def _leer(ruta):
    with io.open(ruta, encoding="utf-8") as f:
        return f.read()


def test_existe_la_forma_de_pedir_una_funcion_por_su_nombre():
    """Sin esto no hay nada que discutir: no se puede buscar por nombre."""
    assert hasattr(piezas, "funcion_completa"), (
        "no existe cerebro/piezas.py::funcion_completa. Mientras no exista, el sistema solo sabe "
        "pedir tramos de lineas, que es lo que borra funciones enteras")


def test_la_funcion_llega_entera(archivo):
    """Entera de verdad: su def y su ultima linea, sin cortar por la mitad."""
    r = piezas.funcion_completa(archivo, "armar")
    assert r, "no encontro la funcion `armar` estando en el archivo"
    t = r["texto"]
    assert t.startswith("def armar("), "no empieza en el def de la funcion pedida"
    assert 'return {"proyecto": proyecto' in t, "la funcion llega CORTADA: le falta el final"
    assert "def ultima" not in t, "se paso de largo: se trajo tambien la funcion siguiente"
    assert "def primera" not in t, "empezo antes de tiempo: se trajo la funcion anterior"


def test_el_sitio_que_dice_es_el_sitio_de_verdad(archivo):
    """Si dice desde/hasta, tienen que ser los de verdad. Un numero inventado es peor que ninguno."""
    r = piezas.funcion_completa(archivo, "armar")
    lineas = _leer(archivo).splitlines()
    assert lineas[r["desde"] - 1].startswith("def armar("), (
        "el `desde` que devuelve no cae en el def de la funcion: son numeros inventados")
    assert "return {" in lineas[r["hasta"] - 1], (
        "el `hasta` que devuelve no cae en la ultima linea de la funcion")
    assert "\n".join(lineas[r["desde"] - 1:r["hasta"]]) == r["texto"], (
        "el texto que devuelve no es el que hay entre desde y hasta: no se puede confiar en el")


def test_si_no_esta_lo_dice_y_no_se_lo_inventa(archivo):
    """Ley de Julio: nunca inventar. Si no esta, se contesta que no esta."""
    assert piezas.funcion_completa(archivo, "no_existe_esta_funcion") is None, (
        "devolvio algo para una funcion que NO existe: eso es inventar")


def test_aunque_el_archivo_cambie_de_tamano_se_sigue_acertando(tmp_path):
    """EL PUNTO DE TODO ESTO. Se le meten 30 lineas por delante: el numero fijo fallaria."""
    p = tmp_path / "crecido.py"
    p.write_text("# linea de relleno\n" * 30 + ARCHIVO_DE_MENTIRA, encoding="utf-8")
    r = piezas.funcion_completa(str(p), "armar")
    assert r, "con el archivo mas largo ya no encuentra la funcion"
    assert r["desde"] > 30, "no siguio a la funcion cuando esta se movio hacia abajo"
    assert 'return {"proyecto": proyecto' in r["texto"], "la trajo cortada tras moverse"


def test_el_repartidor_ya_no_lleva_numeros_escritos_a_mano():
    """Mientras el numero siga escrito a mano, se vuelve a romper al siguiente cambio."""
    src = _leer(ROUTER)
    assert "= 87, 227" not in src, (
        "cerebro/router.py sigue localizando la funcion `armar` con los numeros 87 y 227 escritos "
        "a mano. En cuanto el archivo cambie, apunta al sitio equivocado: es el fallo que Julio "
        "lleva rondas mandando reparar")
    assert "funcion_completa" in src, (
        "el repartidor no busca la funcion por su nombre: sigue sin usar la busqueda por nombre")


def test_el_repartidor_trae_la_funcion_armar_completa_de_verdad():
    """La prueba de arriba mira el texto; esta mira el RESULTADO sobre el archivo real."""
    r = piezas.funcion_completa(ROUTER, "armar")
    assert r, "no encuentra la funcion `armar` en el repartidor de verdad"
    assert r["texto"].startswith("def armar("), "no empieza en el def de `armar`"
    assert r["hasta"] - r["desde"] > 20, (
        "la funcion `armar` llega demasiado corta: se esta cortando por la mitad")
