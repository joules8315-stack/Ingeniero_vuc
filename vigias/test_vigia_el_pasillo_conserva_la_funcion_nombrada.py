"""Vigia: la ley de Julio 'se conserva siempre lo que el problema nombra' se cumple ENTERA.

Hoy (2026-09-29) solo protege nombres de ARCHIVO. Medido en vivo: ante el encargo
"Arreglar app_web.html, funcion processPhoto, y tambien captureDesktopPhoto" la pieza
contestaba unicamente app_web, app_web.html; processPhoto no aparecia, y cuatro vueltas
seguidas de Foto Informe murieron porque al obrero le llego el tramo 2273-2312 en lugar
de processPhoto (renglon 2381 de un archivo de 2.462 renglones).

Esta prueba NACE ROJA A PROPOSITO: vigila dos piezas que todavia NO existen en
arnes/asignador.py:

    identificadores(texto)
        Conjunto de NOMBRES DE FUNCION O DE COSA que el texto nombra, en minusculas.
        Cuenta toda palabra de 3+ letras con mayuscula en medio (processPhoto) o raya
        baja en medio (separar_avisos), y ademas la palabra justo detras de "funcion",
        "funcion" con tilde, "def" o "class". No cuenta palabras comunes del idioma
        ni nombres de archivo (eso ya lo da _nombres).

    trozo_que_contiene(texto, aguja, presupuesto)
        Pedazo del texto, de como maximo `presupuesto` letras, que CONTIENE la aguja,
        con contexto por delante y por detras a partes iguales. Si la aguja no esta,
        devuelve el principio del texto hasta el presupuesto (lo que se hace hoy).

Sin IA, sin red, sin lanzar procesos, sin escribir fuera de la carpeta temporal de
pytest y sin tocar la memoria real del proyecto. Determinista.
"""

import os
import sys

import pytest


# --- Arranque: meter en sys.path la carpeta un nivel arriba de vigias/ -------------
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)


# --- Importar la pieza vigilada (arnes/asignador.py) ------------------------------
# Se importa DENTRO de la prueba para que la roja de hoy se lea de un vistazo y diga
# exactamente cual de las dos piezas falta.
import arnes.asignador as asignador  # noqa: E402


# --- Caso 0: las dos piezas existen -----------------------------------------------
def test_las_dos_piezas_existen():
    """Assert claro: si falta alguna, el mensaje dice cual."""
    assert hasattr(asignador, "identificadores"), (
        "FALTA identificadores() en arnes/asignador.py: la ley de Julio solo protege "
        "nombres de ARCHIVO, no nombres de FUNCION (medido: processPhoto no aparecia)."
    )
    assert hasattr(asignador, "trozo_que_contiene"), (
        "FALTA trozo_que_contiene() en arnes/asignador.py: cuando una seccion no cabe "
        "se queda con su PRINCIPIO, y asi processPhoto (renglon 2381) queda fuera."
    )
    assert callable(asignador.identificadores)
    assert callable(asignador.trozo_que_contiene)


# --- Caso 1: reconoce la funcion nombrada -----------------------------------------
def test_reconoce_la_funcion_nombrada():
    """'funcion processPhoto' tiene que salir como identificador, en minusculas."""
    texto = "Arreglar app_web.html, funcion processPhoto"
    ids = asignador.identificadores(texto)
    assert "processphoto" in ids, (
        "identificadores() no reconocio processPhoto en %r; devolvio %r" % (texto, ids)
    )
    # Todo lo devuelto va en minusculas.
    for nombre in ids:
        assert nombre == nombre.lower(), (
            "identificadores() devolvio %r sin pasar a minusculas" % (nombre,)
        )


def test_reconoce_la_funcion_nombrada_con_tilde_y_camelcase():
    """Tambien con 'funcion' con tilde y con mayuscula en medio (captureDesktopPhoto)."""
    texto = "Arreglar app_web.html, funcion processPhoto, y tambien captureDesktopPhoto"
    ids = asignador.identificadores(texto)
    assert "processphoto" in ids, (
        "identificadores() no reconocio processPhoto en %r; devolvio %r" % (texto, ids)
    )
    assert "capturedesktopphoto" in ids, (
        "identificadores() no reconocio captureDesktopPhoto en %r; devolvio %r"
        % (texto, ids)
    )


def test_reconoce_raya_baja_en_medio():
    """Una palabra con raya baja en medio (separar_avisos) tambien es identificador."""
    ids = asignador.identificadores("hay que revisar separar_avisos y ya")
    assert "separar_avisos" in ids, (
        "identificadores() no reconocio separar_avisos; devolvio %r" % (ids,)
    )


# --- Caso 2: no confunde palabras normales ----------------------------------------
def test_no_confunde_palabras_normales():
    """Frase en castellano llano: ningun identificador."""
    texto = "arreglar la pantalla del celular porque no guarda"
    ids = asignador.identificadores(texto)
    assert ids == set(), (
        "identificadores() saco identificadores de una frase normal %r: %r"
        % (texto, ids)
    )


def test_no_cuenta_nombres_de_archivo():
    """Los nombres de archivo ya los da _nombres; identificadores() no los repite."""
    ids = asignador.identificadores("Arreglar app_web.html y nada mas")
    assert "app_web" not in ids, (
        "identificadores() conto el nombre de archivo app_web.html; devolvio %r" % (ids,)
    )
    assert "app_web.html" not in ids, (
        "identificadores() conto el nombre de archivo app_web.html; devolvio %r" % (ids,)
    )


# --- Caso 3: conserva el trozo que contiene lo pedido -----------------------------
def test_conserva_el_trozo_que_contiene_lo_pedido():
    """Con relleno delante y detras, el pedazo devuelto TIENE que contener la aguja."""
    aguja = "def procesarFoto"
    relleno_antes = ("linea de relleno que no importa nada\n" * 200)
    relleno_despues = ("mas relleno que tampoco importa nada\n" * 200)
    texto = relleno_antes + aguja + "\n" + relleno_despues
    presupuesto = 400  # mucho menor que el texto entero
    assert len(texto) > presupuesto * 5, "el texto de mentira tiene que ser largo"

    trozo = asignador.trozo_que_contiene(texto, aguja, presupuesto)
    assert aguja in trozo, (
        "trozo_que_contiene() devolvio un pedazo que NO contiene %r; "
        "devolvio %r..." % (aguja, trozo[:120])
    )
    assert len(trozo) <= presupuesto, (
        "trozo_que_contiene() devolvio %d letras, mas que el presupuesto %d"
        % (len(trozo), presupuesto)
    )


def test_conserva_el_trozo_con_contexto_a_los_dos_lados():
    """Deja contexto por delante y por detras de la aguja, a partes iguales."""
    aguja = "def procesarFoto"
    texto = ("A" * 500) + aguja + ("B" * 500)
    presupuesto = 200
    trozo = asignador.trozo_que_contiene(texto, aguja, presupuesto)
    assert aguja in trozo, "el trozo no contiene la aguja: %r" % (trozo,)
    antes = trozo.index(aguja)
    despues = len(trozo) - antes - len(aguja)
    assert antes > 0, "no dejo contexto por delante de la aguja: %r" % (trozo,)
    assert despues > 0, "no dejo contexto por detras de la aguja: %r" % (trozo,)


# --- Caso 4: si no esta la aguja, no revienta -------------------------------------
def test_si_no_esta_la_aguja_no_revienta():
    """Aguja ausente: devuelve el principio del texto, sin fallar."""
    texto = "contenido de mentira " * 100
    presupuesto = 120
    trozo = asignador.trozo_que_contiene(texto, "aguja_que_no_existe", presupuesto)
    assert isinstance(trozo, str)
    assert len(trozo) <= presupuesto, (
        "sin aguja, trozo_que_contiene() devolvio %d letras, mas que %d"
        % (len(trozo), presupuesto)
    )
    assert trozo == texto[:presupuesto], (
        "sin aguja, trozo_que_contiene() debe devolver el principio del texto"
    )


def test_si_no_esta_la_aguja_con_texto_corto_no_revienta():
    """Texto mas corto que el presupuesto y aguja ausente: devuelve el texto entero."""
    texto = "corto"
    trozo = asignador.trozo_que_contiene(texto, "no_esta", 1000)
    assert trozo == texto


if __name__ == "__main__":
    sys.exit(pytest.main([os.path.abspath(__file__), "-q"]))
