# -*- coding: utf-8 -*-
"""Vigia de texto: el segundo sitio de aplicacion usa aplicar_propuesta, no aplicar_cambio.

Julio, 2026-09-21: en ingeniero.py habia DOS sitios que aplicaban cambios en disco. El
primero (comando equipo) ya usaba aplicador.aplicar_propuesta. El segundo (el que aplica
lo que el equipo ya aprobo) seguia llamando a aplicador.aplicar_cambio, que es la puerta
vieja. Esta vigia es de TEXTO: abre ingeniero.py y comprueba, con assert, que el texto
viejo YA NO aparece y que el texto nuevo SI aparece.

No toca ningun otro archivo. No importa ingeniero.py (solo lo lee como texto), asi que
no dispara efectos secundarios ni escribe en memorias compartidas.
"""
import os


AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
INGENIERO = os.path.join(RAIZ, "ingeniero.py")

# El texto VIEJO que ya no debe estar: la puerta antigua del segundo sitio.
VIEJO = "_ok2, _msg2 = _ap.aplicar_cambio(_prop, raiz=_raiz2)"

# El texto NUEVO que si debe estar: la puerta buena, la misma que usa el comando equipo.
NUEVO = "_ok2, _msg2 = _ap.aplicar_propuesta(_prop, raiz=_raiz2)"


def _leer_ingeniero():
    """Devuelve el contenido de ingeniero.py como texto, o falla claro si no esta."""
    assert os.path.isfile(INGENIERO), (
        "No encuentro ingeniero.py en %s: la vigia no puede mirar lo que no existe."
        % INGENIERO
    )
    with open(INGENIERO, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def test_el_texto_viejo_ya_no_aparece():
    """El segundo sitio ya NO llama a aplicar_cambio."""
    texto = _leer_ingeniero()
    assert VIEJO not in texto, (
        "El texto viejo sigue en ingeniero.py:\n  %s\n"
        "El segundo sitio debe usar aplicar_propuesta, no aplicar_cambio." % VIEJO
    )


def test_el_texto_nuevo_si_aparece():
    """El segundo sitio SI llama a aplicar_propuesta."""
    texto = _leer_ingeniero()
    assert NUEVO in texto, (
        "Falta el texto nuevo en ingeniero.py:\n  %s\n"
        "El segundo sitio debe aplicar con la misma puerta que el comando equipo." % NUEVO
    )


def test_los_dos_textos_no_conviven():
    """No puede estar el viejo y el nuevo a la vez: seria una sustitucion a medias."""
    texto = _leer_ingeniero()
    tiene_viejo = VIEJO in texto
    tiene_nuevo = NUEVO in texto
    assert not (tiene_viejo and tiene_nuevo), (
        "ingeniero.py tiene el texto viejo Y el nuevo: la sustitucion quedo a medias."
    )
    assert tiene_nuevo, (
        "ingeniero.py no tiene ni el texto viejo ni el nuevo: el segundo sitio desaparecio."
    )
