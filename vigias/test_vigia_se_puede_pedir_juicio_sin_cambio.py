# -*- coding: utf-8 -*-
"""VIGIA — SE PUEDE PEDIR UN JUICIO SOBRE TRABAJO YA HECHO, SIN PEDIR NINGUN CAMBIO.

FALLO REAL MEDIDO (2026-09-08), leido en la salida del propio mando, no contado por nadie: se
le pidio al equipo que JUZGARA un enchufe ya aplicado y probado. Su diagnostico decia que
estaba bien puesto y que no rompia vecinos. Y aun asi el VEREDICTO salio RECHAZADO, con este
motivo textual: "la propuesta no realiza ningun cambio: el texto nuevo es identico al texto
viejo". Claro que no cambia nada: NO SE LE PIDIO UN CAMBIO, se le pidio un JUICIO.

O sea: el mando del equipo solo sabe pedir REPARACIONES. No sabe pedir una revision de algo ya
hecho. Y eso deja al supervisor sin poder quedar satisfecho nunca cuando el trabajo se aplico
con arnes/copista.py, que es justo lo que manda la ley de que la fotocopia no se paga.

Y LA PIEZA QUE HACE ESTO YA EXISTE: cuerpo/obrero.py::auditar, escrita literalmente para "esto
ya esta hecho, solo revisalo". Nadie la llama desde fuera. Otra huerfana.

LEY: CONTRATO_CREAR_PIEZA_NUEVA regla 6 (nace conectada o no nace) y
CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA regla 2 (se ahorra la fotocopia, NO la revision).
"""
import os
import re
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)


def test_la_pieza_que_juzga_lo_ya_hecho_existe():
    """cuerpo/obrero.py::auditar es la que sabe revisar sin escribir. Tiene que estar."""
    from cuerpo import obrero
    assert hasattr(obrero, "auditar"), (
        "no esta la pieza que revisa sin escribir; sin ella no hay forma de pedir un juicio")


def test_el_mando_sabe_pedir_juicio_sin_cambio():
    """Tiene que haber una forma de pedir un juicio desde fuera, no solo una reparacion."""
    ruta = os.path.join(AQUI, "ingeniero.py")
    with open(ruta, encoding="utf-8") as f:
        codigo = f.read()
    vivo = re.sub(r'"""(?:.|\n)*?"""', " ", codigo)
    vivo = "\n".join(re.sub(r"#.*$", "", ln) for ln in vivo.splitlines())
    assert 'cmd == "juzga"' in vivo, (
        "EL MANDO NO SABE PEDIR UN JUICIO SOBRE TRABAJO YA HECHO. Solo sabe pedir cambios, y "
        "por eso un trabajo aplicado con el copista NUNCA puede tener veredicto: el equipo lo "
        "rechaza diciendo que no cambia nada, aunque su propio diagnostico diga que esta bien.")
    # CORREGIDO EL 2026-09-09 POR ORDEN DE JULIO. Esta vigia exigia lo contrario de lo que
    # ahora manda la ley: "por que se le pide que juzgue algo que ya esta. Eso es estupido.
    # Debe pasar a EJECUTAR. Lo que debe hacer, a lo sumo, es con un PROGRAMA verificar que el
    # pedido este bien hecho". El bucle: se mandaba a juzgar, el cerebro decia "errores de
    # sintaxis graves", se comprobaba y era FALSO, se volvia a mandar, y otra vez. Tres veces
    # seguidas el mismo dia. Ahora lo comprueba un programa, gratis y en 0,18 segundos.
    # Una vigia que exige lo que la ley prohibe no protege: estorba. Se corrige, no se borra.
    assert "pedido_bien_hecho" in vivo, (
        "EL MANDO YA NO COMPRUEBA QUE EL PEDIDO ESTE BIEN HECHO. Sin eso, o se le vuelve a "
        "preguntar a un cerebro (el bucle que costo dinero y dio veredictos falsos) o no se "
        "comprueba nada.")
    assert "auditar(" not in vivo, (
        "el mando nombra el juicio pero no llama a la pieza que lo hace: seguiria sin servir")
