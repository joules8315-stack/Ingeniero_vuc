# -*- coding: utf-8 -*-

"""Vigia: el material NO se corta a medias.

Medido el 2026-09-19: cuando el paquete no cabia, _filtrar_paquete recortaba
renglones sueltos del final y el que escribe el codigo recibia un trozo que se
acababa a media altura. Como nadie le avisaba, se inventaba el resto, y eso fue
la mitad de los rechazos de ese dia.

Esta vigia comprueba tres cosas sobre cuerpo/obrero.py::_filtrar_paquete:
  1) si un bloque de trozos entra, entra ENTERO (con su renglon final);
  2) si algo se quedo fuera, lo que devuelve trae un aviso con NECESITO_LEER;
  3) si todo cabe, NO aparece ese aviso, porque no falto nada.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from cuerpo import obrero  # noqa: E402


# --- el texto de paquete que se arma a mano ---------------------------------

RELLENO = 20  # renglones de relleno numerados dentro de cada bloque


def _bloque(nombre_archivo, etiqueta):
    """Un bloque de trozos: cabecera ### `archivo` + relleno + renglon final."""
    lineas = ["### `%s`" % nombre_archivo]
    for i in range(1, RELLENO + 1):
        lineas.append("relleno %s numero %d" % (etiqueta, i))
    lineas.append("FIN DEL BLOQUE %s" % etiqueta)
    return lineas


def _paquete_de_prueba():
    """Arma a mano un paquete con titulo, LA LEY QUE MANDA y LOS TROZOS."""
    lineas = []
    lineas.append("# PAQUETE DE PRUEBA")
    lineas.append("")
    lineas.append("## 1. LA LEY QUE MANDA")
    lineas.append("aqui va la ley que manda")
    lineas.append("y un par de renglones debajo")
    lineas.append("")
    lineas.append("## 2. LOS TROZOS")
    lineas += _bloque("uno.py:1-20", "UNO")
    lineas += _bloque("dos.py:1-20", "DOS")
    return "\n".join(lineas)


def _renglones_de_bloque(texto):
    """Devuelve los pares (etiqueta, tiene_final) de los bloques que aparecen."""
    etiquetas = []
    for ln in texto.splitlines():
        if ln.startswith("### `"):
            # la etiqueta es el nombre del archivo de mentira
            etiquetas.append(ln)
    return etiquetas


def test_bloque_que_entra_entra_entero():
    """PRUEBA 1: ningun bloque puede quedar empezado y sin su final."""
    paquete = _paquete_de_prueba()
    # tope pequeno: solo deja entrar mas o menos un bloque
    tope = 400
    salida = obrero._filtrar_paquete(paquete, tope=tope)
    assert isinstance(salida, str), "_filtrar_paquete no devolvio texto"
    # por cada bloque que empieza, tiene que estar su renglon final
    for etiqueta in ("UNO", "DOS"):
        cabecera = "### `%s.py:1-20`" % etiqueta.lower()
        if cabecera in salida:
            final = "FIN DEL BLOQUE %s" % etiqueta
            assert final in salida, (
                "un trozo cortado a medias es lo que hace que el que escribe se invente el resto: "
                "el bloque %s aparece sin su renglon final %r" % (etiqueta, final))


def test_si_falta_algo_avisa_con_necesito_leer():
    """PRUEBA 2: si algo se quedo fuera, tiene que avisar con NECESITO_LEER."""
    paquete = _paquete_de_prueba()
    tope = 400  # tope pequeno: algo se queda fuera
    salida = obrero._filtrar_paquete(paquete, tope=tope)
    assert "NECESITO_LEER" in salida, (
        "si no se avisa, el que escribe cree que lo vio todo: falta el aviso NECESITO_LEER "
        "cuando el material no cabe en el tope")


def test_si_todo_cabe_no_avisa():
    """PRUEBA 3: si todo cabe, NO aparece el aviso, porque no falto nada."""
    paquete = _paquete_de_prueba()
    tope = 100000  # tope grande: cabe todo
    salida = obrero._filtrar_paquete(paquete, tope=tope)
    assert "NECESITO_LEER" not in salida, (
        "no falto nada, asi que no debe aparecer el aviso NECESITO_LEER")


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
