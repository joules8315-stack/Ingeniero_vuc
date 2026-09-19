# -*- coding: utf-8 -*-

"""Vigia: el revisor recibe SOLO lo necesario, nunca el archivo entero.

Orden de Julio A-38 punto 1. El revisor (auditor) no puede tragarse el paquete
completo: si le llega el bulto entero, su respuesta sale cortada y el veredicto
sale roto. Esta vigia comprueba tres cosas:
  1) existe un tope TOPE_REVISOR y no pasa de 12000 letras;
  2) la llamada que arma material_auditor usa el tope (varias lineas) y en el
     modulo no queda el atajo viejo '40000 if auditor';
  3) _filtrar_paquete con un paquete enorme devuelve algo que cabe en el tope.
"""
import os
import sys
import inspect

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from cuerpo import obrero  # noqa: E402


def test_tope_revisor_existe_y_no_pasa_de_12000():
    """El tope del revisor tiene que existir y ser pequeno (<= 12000)."""
    assert hasattr(obrero, "TOPE_REVISOR"), "obrero no tiene TOPE_REVISOR"
    tope = obrero.TOPE_REVISOR
    assert isinstance(tope, int), "TOPE_REVISOR no es un entero: " + repr(tope)
    assert tope <= 12000, "TOPE_REVISOR es demasiado grande: " + str(tope)


def test_la_llamada_que_arma_material_auditor_usa_el_tope():
    """La llamada que arma material_auditor ocupa varias lineas y lleva TOPE_REVISOR.

    Se toma el texto desde 'material_auditor = _filtrar_paquete(' hasta el primer
    ')))' que le sigue, y ese trozo tiene que contener 'TOPE_REVISOR'. Ademas, en
    todo el modulo no puede quedar el atajo viejo '40000 if auditor'.
    """
    fuente = inspect.getsource(obrero)
    marca = "material_auditor = _filtrar_paquete("
    inicio = fuente.find(marca)
    assert inicio != -1, "no aparece la llamada que arma material_auditor"
    fin = fuente.find(")))", inicio)
    assert fin != -1, "no se encontro el cierre ')))' de la llamada a material_auditor"
    trozo = fuente[inicio:fin + 3]
    assert "TOPE_REVISOR" in trozo, (
        "la llamada que arma material_auditor NO usa TOPE_REVISOR: " + trozo[:200])
    assert "40000 if auditor" not in fuente, (
        "queda el atajo viejo '40000 if auditor' en obrero.py")


def test_filtrar_paquete_recorta_al_tope_del_revisor():
    """Un paquete enorme se recorta y cabe en TOPE_REVISOR."""
    renglon = "### `x.py:1-1`  (relevancia 99.0)\n"
    paquete = "## 1. LA LEY QUE MANDA\n" + (renglon * 2000)
    assert len(paquete) >= 60000, "el paquete de prueba no llega a 60000 letras"
    salida = obrero._filtrar_paquete(paquete, archivo="x.py", tope=obrero.TOPE_REVISOR)
    assert isinstance(salida, str), "_filtrar_paquete no devolvio texto"
    assert len(salida) <= obrero.TOPE_REVISOR, (
        "el filtro devolvio mas letras que el tope: " + str(len(salida)))


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f()
                print("  VERDE  " + _n)
            except Exception as e:
                fails += 1
                print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
