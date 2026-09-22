"""Vigia: el obrero puede entregar varios trozos del MISMO archivo.

Dos comprobaciones, cada una importa lo suyo dentro de la prueba:

1) La comprobacion de la respuesta del obrero en modo reparar ACEPTA una propuesta que trae
   'archivo' y una lista 'cambios' con 'texto_viejo' y 'texto_nuevo' en cada trozo, aunque no
   traiga 'texto_viejo' ni 'texto_nuevo' sueltos arriba. Se llama a obrero._propuesta_cumple con
   esa propuesta y la clase 'reparar'.

2) obrero._prompt_obrero("material", "tarea", "reparar") devuelve un texto que nombra la clave
   'cambios' y explica que sirve para varios sitios del MISMO archivo.

No toca ningun otro archivo: solo lee cuerpo/obrero.py a traves de sus funciones.
"""

import os
import sys


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


def test_propuesta_cumple_acepta_varios_trozos_en_cambios():
    """Una propuesta de reparar con 'archivo' + lista 'cambios' (cada trozo con texto_viejo y
    texto_nuevo) tiene que ser ACEPTADA, aunque no traiga texto_viejo ni texto_nuevo sueltos."""
    from cuerpo import obrero

    propuesta = {
        "diagnostico": "hay que tocar dos sitios del mismo archivo",
        "archivo": "cuerpo/obrero.py",
        "cambios": [
            {
                "funcion": "_propuesta_cumple",
                "texto_viejo": "if not str(propuesta.get(\"archivo\") or \"\").strip():",
                "texto_nuevo": "if not str(propuesta.get(\"archivo\") or \"\").strip() and not propuesta.get(\"cambios\"):",
            },
            {
                "funcion": "_prompt_obrero",
                "texto_viejo": "TAREA: {tarea}",
                "texto_nuevo": "TAREA: {tarea} (puede traer varios trozos en 'cambios')",
            },
        ],
        "confianza": "alta",
    }

    ok, falta = obrero._propuesta_cumple(propuesta, "reparar")
    assert ok is True, "la propuesta con varios trozos en 'cambios' fue rechazada: %r" % (falta,)
    assert falta == "", "cuando cumple, 'falta' tiene que venir vacio, vino: %r" % (falta,)


def test_prompt_obrero_reparar_nombra_cambios_para_varios_sitios():
    """El encargo de reparar tiene que nombrar la clave 'cambios' y explicar que sirve para
    varios sitios del MISMO archivo."""
    from cuerpo import obrero

    texto = obrero._prompt_obrero("material", "tarea", "reparar")
    assert isinstance(texto, str) and texto.strip(), "_prompt_obrero devolvio un texto vacio"

    bajo = texto.lower()
    assert "cambios" in bajo, "el encargo de reparar NO nombra la clave 'cambios'"

    # Tiene que explicar que sirve para varios sitios del MISMO archivo.
    assert "varios" in bajo, "el encargo NO dice que 'cambios' sirve para varios trozos"
    assert "mismo archivo" in bajo, "el encargo NO dice que los trozos son del MISMO archivo"

    # Y tiene que dejar claro que cada trozo lleva su texto_viejo y su texto_nuevo.
    assert "texto_viejo" in bajo, "el encargo NO menciona texto_viejo dentro de los trozos"
    assert "texto_nuevo" in bajo, "el encargo NO menciona texto_nuevo dentro de los trozos"
