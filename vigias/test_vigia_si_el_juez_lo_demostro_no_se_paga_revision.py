"""Vigia: si el juez ya demostro la prueba, no se paga revision.

Vigila UNA sola cosa de la funcion `auditar` de cuerpo/obrero.py:

    cuando la propuesta trae la marca '_juez_de_la_prueba' con texto dentro,
    `auditar` NO le pregunta a ninguna IA y devuelve por su cuenta el
    veredicto APROBADO.

Motivo (orden de Julio A-39): correr la prueba es CUENTA, no JUICIO. Si el
juez ya demostro que la prueba estaba roja antes del cambio, verde despues y
roja al deshacerlo, pagar una IA para que confirme lo mismo es gastar sin
ganar. El programa ya lo sabe; que lo diga el.

Por que nace ROJA a proposito:

    Hoy `auditar` solo METE el texto del juez en el material del auditor y
    sigue preguntandole a la IA. La IA cobra (o gasta cupo) por confirmar algo
    que un programa ya demostro. Esta vigia exige el atajo: si hay
    '_juez_de_la_prueba' con texto, no se llama a `_preguntar_con_relevo` y
    el veredicto sale APROBADO por cuenta propia. Mientras ese atajo no
exista, la vigia se pone roja. Roja aqui es la senal correcta: senala el
    gasto que la orden A-39 manda cortar.

La vigia es determinista y sin red: sustituye `_preguntar_con_relevo` por una
funcion falsa que solo apunta que la llamaron. Si la lista queda vacia, nadie
pago revision. Si queda con algo, se le pregunto a una IA algo que el juez ya
habia demostrado.
"""

import os
import sys

# La raiz del proyecto se calcula desde este mismo archivo: vigias/ -> raiz.
_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ARNES = os.path.join(_RAIZ, "arnes")
for _ruta in (_RAIZ, _ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from cuerpo import obrero  # noqa: E402


# La razon que el juez de la prueba deja escrita cuando ya demostro el cambio.
RAZON_DEL_JUEZ = (
    "la prueba estaba roja antes del cambio, quedo verde con el cambio "
    "y volvio a roja al deshacerlo"
)

# La propuesta que trae la marca del juez con texto dentro.
PROPUESTA_CON_JUEZ = {
    "archivo": "cuerpo/ejemplo_del_juez.py",
    "texto_viejo": "def sumar(a, b):\n    return a - b\n",
    "texto_nuevo": "def sumar(a, b):\n    return a + b\n",
    "_juez_de_la_prueba": RAZON_DEL_JUEZ,
}


def test_si_el_juez_lo_demostro_no_se_paga_revision(monkeypatch):
    """Si el juez ya demostro la prueba, auditar no llama a ninguna IA.

    Se sustituye `_preguntar_con_relevo` por una funcion falsa que apunta cada
    llamada en una lista y devuelve una tupla de tres cosas (texto, quien,
    avisos), como la de verdad. Si la lista queda vacia, nadie pago revision.
    """
    llamadas = []

    def _preguntar_con_relevo_falso(prompt, temperatura, evitar=None, primero=None,
                                    pesado=False, clase="", vuelta=0):
        llamadas.append({
            "prompt": prompt,
            "temperatura": temperatura,
            "evitar": evitar,
            "primero": primero,
            "pesado": pesado,
            "clase": clase,
            "vuelta": vuelta,
        })
        return ("", "", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", _preguntar_con_relevo_falso)

    paquete = "paquete corto de prueba para la vigia del juez"
    auditoria, quien_reviso, avisos = obrero.auditar(paquete, PROPUESTA_CON_JUEZ)

    assert llamadas == [], (
        "se le pregunto a una IA algo que el juez ya habia demostrado: "
        "correr la prueba es cuenta, no juicio (orden de Julio A-39). "
        "Llamadas hechas: %r" % (llamadas,)
    )

    assert isinstance(auditoria, dict), (
        "auditar debe devolver la auditoria como diccionario, no %r" % (auditoria,)
    )
    assert auditoria.get("veredicto") == "APROBADO", (
        "si el juez ya demostro la prueba, el veredicto debe ser APROBADO "
        "por cuenta propia, no %r" % (auditoria.get("veredicto"),)
    )
