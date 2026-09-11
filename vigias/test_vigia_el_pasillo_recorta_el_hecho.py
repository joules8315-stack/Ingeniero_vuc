# -*- coding: utf-8 -*-
"""VIGIA DEL HECHO — EL PASILLO RECORTA DE VERDAD, NO LO CUENTA.

Julio, 2026-09-09: "Crea vigia fuerte, legisla bien, pon candados que sirvan, y asegurate
de que no se vuelva a olvidar." Y el expediente de fallos recurrentes: "la prueba mide el
papel, no el hecho".

La vigia vieja media el PAPEL: la palabra `armar_encargo` dentro del codigo fuente. Esta
mide el HECHO: intercepta el pasillo unico (_preguntar_con_relevo), le mete un prompt
GORDO con la pieza a reparar EN EL MEDIO (que es donde viaja el codigo del paquete real) y
comprueba que lo que de verdad le llega al cerebro no pasa del tope medido del gratis mas
pequeno Y que la pieza sigue dentro. Sin internet: la puerta del cerebro se sustituye por
una esponja que solo apunta lo que recibe.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))
from unittest import mock  # noqa: E402

PIEZA = "def armar_datos(perfil, preguntar=None, metricas_reales=None):"
TOPE_GRATIS = 19042    # lo que aguanta de verdad el gratis mas pequeno (groq, medido)


def _prompt_gordo_en_medio():
    """Un prompt de ~100.000 letras con la pieza en el MEDIO, como el paquete real."""
    from cuerpo import obrero
    li = "relleno que no hace falta\n"
    material = ("### la ley que aplica\n" + li * 230 +
                "### `cuerpo/x.py`\n" + PIEZA + "\n    return perfil\n" +
                li * 600 + "### cola sin valor\n")
    return obrero._prompt_obrero(material, "reparar armar_datos en cuerpo/x.py", "reparar")


class _Esponja:
    """La puerta del cerebro: SOLO apunta lo que le llega, no sale a internet."""

    def __init__(self):
        self.que_le_llego = []

    def _preguntar_groq(self, prompt, modelo, temperatura):
        self.que_le_llego.append(prompt)
        return ('{"diagnostico": "x", "archivo": "cuerpo/x.py", "funcion": "armar_datos",'
                '"texto_viejo": "x", "texto_nuevo": "x", "cambio": "x", "codigo": "x",'
                '"vigia": "", "puede_danar": [], "preguntas": [], "confianza": "media"}')


def test_lo_que_de_verdad_llega_al_cerebro_pasa_por_el_recorte_del_pasillo():
    """El hecho: lo que sale del pasillo no pasa del gratis mas pequeno y la pieza sigue ahi."""
    from cuerpo import obrero
    esponja = _Esponja()
    prompt = _prompt_gordo_en_medio()
    assert len(prompt) > TOPE_GRATIS, (
        "el montaje de esta vigia ya no produce un prompt gordo: %d < %d"
        % (len(prompt), TOPE_GRATIS))
    parches = [
        mock.patch.object(obrero, "prestar_cerebro", return_value=(esponja, object())),
        mock.patch.object(obrero, "quienes_hay", return_value=["groq"]),
        mock.patch.object(obrero.cuotas, "fila", return_value=["groq"]),
        mock.patch.object(obrero.cuotas, "rankear", side_effect=lambda d, t: d),
        mock.patch.object(obrero.cuotas, "_capacidad", side_effect=lambda q: TOPE_GRATIS),
        mock.patch.object(obrero.cuotas, "apuntar_uso", return_value=None),
        mock.patch.object(obrero.cuotas, "apuntar_no_cupo", return_value=None),
        mock.patch.object(obrero.cuotas, "dormir", return_value=None),
    ]
    for p in parches:
        p.start()
    try:
        obrero._preguntar_con_relevo(prompt, 0.1, primero="groq")
    finally:
        for p in reversed(parches):
            p.stop()
    assert esponja.que_le_llego, "no salio ninguna llamada: la vigia no midio nada"
    llego = esponja.que_le_llego[0]
    assert len(llego) <= TOPE_GRATIS, (
        "LO QUE DE VERDAD LLEGA AL CEREBRO mide %d letras y el gratis mas pequeno aguanta %d. "
        "El filtro no esta dentro del pasillo: se salta a los gratis en silencio y acaba "
        "escribiendo y revisandose el de pago." % (len(llego), TOPE_GRATIS))
    assert PIEZA in llego, (
        "el recorte tiro la pieza que hay que reparar: cabe y no sirve para nada.")


def test_armar_encargo_conserva_la_pieza_que_va_en_medio():
    """El recorte del asignador es POR PARTES: la pieza viaja en el medio y se conserva."""
    import asignador
    material = ("x" * 25000 + "\n### `cuerpo/x.py`\n" + PIEZA + "\n    return perfil\n"
                + "y" * 25000)
    fallo = asignador.leer_el_fallo(
        "FAILED cuerpo/x.py::test_algo\nE   AssertionError: NO SALE EL EMBUDO\n")
    encargo = asignador.armar_encargo(fallo, material=material)
    assert len(encargo) <= TOPE_GRATIS, (
        "el encargo salio de %d letras: a los gratis no les cabe." % len(encargo))
    assert PIEZA in encargo, (
        "el recorte tiro justo el trozo que hay que reparar: cabe y no sirve de nada.")