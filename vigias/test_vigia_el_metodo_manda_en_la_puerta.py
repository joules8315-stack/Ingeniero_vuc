# -*- coding: utf-8 -*-
"""Vigia: el metodo manda en la puerta.

NACE ROJA A PROPOSITO. Mide tres cosas que Julio exigio y que hoy no se cumplen:

  1. El octavo rotulo LE DA A LA APLICACION es obligatorio (rapidez, eficiencia,
     precision, economia). Hoy no se exige y un encargo sin el arranca igual.
  2. Cada frase que devuelve arnes/metodo.revisar dice QUIEN FALLO, escogiendo
     entre cuatro y solo cuatro: herramienta, razonamiento, informacion o reparte.
     Hoy ninguna los nombra.
  3. El comando por el que pasan TODAS las IA llama al metodo ANTES de llamar a
     ningun cerebro. Hoy se llama a mano y por eso depende de la memoria.

Los casos 2 y 5 estan verdes hoy y tienen que seguir verdes: son el freno de mano
para que el arreglo no se pase de apretado y frene encargos buenos.

No escribe en la memoria real del proyecto: la carpeta que se le pasa es la
carpeta temporal que da pytest. Sin red, sin IA, sin lanzar procesos.
"""
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# Arranque: meter en la ruta de busqueda la carpeta de arriba (la raiz del
# proyecto) y la carpeta arnes, a partir de la ruta de este mismo archivo.
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")
for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from arnes import metodo  # noqa: E402


# ---------------------------------------------------------------------------
# Los siete rotulos de hoy y el octavo que entra en la ronda siguiente.
# ---------------------------------------------------------------------------
ROTULOS_DE_HOY = [
    "PROBLEMA",
    "EVIDENCIA",
    "CAMINO",
    "PUEDE DANAR",
    "VIGIA",
    "NO SE TOCA",
    "MANO",
]

ROTULO_NUEVO = "LE DA A LA APLICACION"

# Los cuatro y solo cuatro sospechosos que una frase puede nombrar.
SOSPECHOSOS = ["herramienta", "razonamiento", "informacion", "reparte"]


# ---------------------------------------------------------------------------
# Utilidades para armar los encargos de mentira juntando renglones.
# ---------------------------------------------------------------------------
def _renglon(rotulo, cuerpo):
    """Un rotulo bien puesto: detras de los dos puntos hay mas de tres letras."""
    return "%s: %s" % (rotulo, cuerpo)


def _encargo_con(rotulos):
    """Arma un encargo con los rotulos que se le pasen, cada uno con cuerpo."""
    renglones = []
    for r in rotulos:
        renglones.append(_renglon(r, "contenido suficiente para contar"))
    return "\n".join(renglones)


def _encargo_de_siete():
    """Los SIETE rotulos de hoy, bien puestos, y sin el octavo."""
    return _encargo_con(ROTULOS_DE_HOY)


def _encargo_de_ocho():
    """Los OCHO rotulos, bien puestos."""
    return _encargo_con(ROTULOS_DE_HOY + [ROTULO_NUEVO])


# ---------------------------------------------------------------------------
# CASO 1. El octavo rotulo es obligatorio. NACE ROJO.
# ---------------------------------------------------------------------------
def test_caso_1_el_octavo_rotulo_es_obligatorio(tmp_path):
    encargo = _encargo_de_siete()
    falta = metodo.revisar(encargo, str(tmp_path))
    assert len(falta) == 1, (
        "Un encargo con los siete rotulos de hoy y sin LE DA A LA APLICACION "
        "tiene que devolver EXACTAMENTE una cosa que falta. Hoy devuelve %r. "
        "Si sale vacia, ese encargo arranca aunque no diga que gana la aplicacion."
        % (falta,)
    )
    frase = falta[0].lower()
    assert "aplicacion" in frase or "aplicaci" in frase, (
        "La unica frase que falta tiene que hablar de lo que le da a la aplicacion. "
        "Hoy dice: %r" % (falta[0],)
    )


# ---------------------------------------------------------------------------
# CASO 2. Con los ocho, pasa. VERDE HOY, tiene que seguir verde.
# ---------------------------------------------------------------------------
def test_caso_2_con_los_ocho_pasa(tmp_path):
    encargo = _encargo_de_ocho()
    falta = metodo.revisar(encargo, str(tmp_path))
    assert falta == [], (
        "Un encargo con los ocho rotulos bien puestos tiene que pasar limpio. "
        "Si esto sale rojo, el arreglo se paso de apretado y frena encargos buenos. "
        "Devolvio: %r" % (falta,)
    )


# ---------------------------------------------------------------------------
# CASO 3. Cada frase dice quien fallo. NACE ROJO.
# ---------------------------------------------------------------------------
def test_caso_3_cada_frase_dice_quien_fallo(tmp_path):
    falta = metodo.revisar("", str(tmp_path))
    assert falta, "Un encargo vacio tiene que devolver cosas que faltan."
    for frase in falta:
        baja = frase.lower()
        nombra = [s for s in SOSPECHOSOS if s in baja]
        assert nombra, (
            "Cada frase tiene que nombrar a uno de los cuatro sospechosos "
            "(herramienta, razonamiento, informacion o reparte). "
            "Esta no nombra a ninguno: %r" % (frase,)
        )


# ---------------------------------------------------------------------------
# CASO 4. La cuenta sube a ocho. NACE ROJO.
# ---------------------------------------------------------------------------
def test_caso_4_la_cuenta_sube_a_ocho(tmp_path):
    falta = metodo.revisar("", str(tmp_path))
    assert len(falta) == 8, (
        "Con un encargo vacio la lista tiene que traer OCHO cosas (los ocho "
        "rotulos). Hoy trae %d: %r" % (len(falta), falta)
    )
    for frase in falta:
        assert len(frase) > 15, (
            "Cada frase tiene que medir mas de quince letras. Esta mide %d: %r"
            % (len(frase), frase)
        )


# ---------------------------------------------------------------------------
# CASO 5. Lo que hoy funciona y no puede cambiar. VERDE HOY.
# ---------------------------------------------------------------------------
def test_caso_5_lo_que_hoy_funciona_no_cambia(tmp_path):
    # Nada, vacio, o algo que no es texto: devuelve la lista entera y NO revienta.
    for entrada in (None, "", "   ", 0, 123, [], {}, object()):
        falta = metodo.revisar(entrada, str(tmp_path))
        assert isinstance(falta, list), (
            "revisar(%r) tiene que devolver una lista, no %r"
            % (entrada, type(falta))
        )
        assert len(falta) >= 7, (
            "revisar(%r) tiene que devolver al menos los siete rotulos de hoy. "
            "Devolvio %r" % (entrada, falta)
        )


# ---------------------------------------------------------------------------
# CASO 6. El comando llama al metodo antes que a ningun cerebro. NACE ROJO.
# ---------------------------------------------------------------------------
def test_caso_6_el_comando_llama_al_metodo_antes_que_a_ningun_cerebro():
    ruta = os.path.join(RAIZ, "ingeniero.py")
    assert os.path.exists(ruta), (
        "No encuentro ingeniero.py en %s: sin el no se puede vigilar la puerta." % ruta
    )
    with open(ruta, encoding="utf-8") as f:
        lineas = f.readlines()

    # El sitio donde arranca el comando del equipo: el renglon que comprueba
    # que la orden recibida es la de equipo.
    indice_arranque = None
    for i, linea in enumerate(lineas):
        baja = linea.lower()
        if "cmd" in baja and "equipo" in baja and ("==" in baja or "in " in baja):
            indice_arranque = i
            break
    assert indice_arranque is not None, (
        "No encuentro en ingeniero.py el renglon donde arranca el comando del "
        "equipo (el que comprueba que la orden recibida es la de equipo). "
        "Sin ese ancla no se puede vigilar la puerta."
    )

    # Mas abajo de ese renglon tiene que aparecer una llamada a la pieza del metodo.
    resto = "".join(lineas[indice_arranque + 1:])
    llama_al_metodo = (
        "metodo.revisar" in resto
        or "from arnes import metodo" in resto
        or "import metodo" in resto
        or "arnes.metodo" in resto
    )
    assert llama_al_metodo, (
        "El comando del equipo NO llama a la pieza del metodo antes de llamar "
        "a ningun cerebro. Hoy el metodo se llama a mano, o sea que depende de "
        "la memoria de la IA, y eso es justo lo que Julio prohibio: 'nada nunca "
        "debe depender de tu memoria'. El arreglo tiene que meter la llamada a "
        "arnes/metodo.revisar en el arranque del comando, mas abajo del renglon "
        "%d de ingeniero.py." % (indice_arranque + 1)
    )
