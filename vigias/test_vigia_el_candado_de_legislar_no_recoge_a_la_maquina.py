"""Vigia: el candado de legislar NO debe recoger a la maquina, pero SI debe seguir recogiendo a Julio.

Hecho del 2026-09-20:
    Tras la primera vuelta de la maquina trabajando sola, el candado que recoge las
    ordenes de Julio bloqueo el cierre con 23 lineas que Julio nunca dijo. Eran el
    pedido que la propia maquina le hace a su perito y el informe que ella misma
    escribio. Ahora que la maquina trabaja sola escribe mucho, asi que esa lista
    crecera cada noche. Entonces el que cierra marcara todo como no aplica sin
    leerlo, y el dia que ahi dentro haya una orden de verdad se entierra con el
    resto.

Lo importante de esta vigia NO es que deje fuera a la maquina.
Lo importante es que SIGA recogiendo lo que dice Julio.

Si esta vigia se pone roja porque una frase de Julio dejo de recogerse, es peor
que si se pone roja porque un texto de la maquina se colo: dejar de recoger una
orden de Julio es enterrar su voluntad.
"""

import os
import sys

# Raiz del proyecto: dos dirname sobre el abspath de este propio archivo.
_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_arnes = os.path.join(_raiz, "arnes")

for _p in (_raiz, _arnes):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import candado_legislar  # noqa: E402


# ---------------------------------------------------------------------------
# PRIMERA PRUEBA (la importante): frases de verdad de Julio, tal como el las
# escribe. Todas deben ser recogidas por parece_una_orden.
# ---------------------------------------------------------------------------
FRASES_DE_JULIO = [
    "Repara el candado de legislar que se esta tragando lo que no es mio.",
    "Nunca dejes que la maquina escriba ordenes en mi nombre.",
    "Siempre guarda lo aprobado antes de cerrar la vuelta.",
    "Que el equipo revise antes de guardar nada.",
    "No quites ningun candado sin avisarme.",
]


def test_el_candado_sigue_recogiendo_lo_que_dice_julio():
    """Si una frase de Julio deja de recogerse, esto es peor que recoger ruido."""
    for frase in FRASES_DE_JULIO:
        recogida = candado_legislar.parece_una_orden(frase)
        assert recogida is True, (
            "El candado de legislar dejo de recoger una orden de Julio: "
            "%r. Dejar de recoger una orden de Julio es peor que recoger "
            "ruido de la maquina: la orden se entierra con el resto." % (frase,)
        )


# ---------------------------------------------------------------------------
# SEGUNDA PRUEBA: textos que escribe la propia maquina, tal como salieron ese
# dia. Ninguno debe ser recogido por parece_una_orden.
# ---------------------------------------------------------------------------
TEXTOS_DE_LA_MAQUINA = [
    "Soy el perito del PIT y voy a revisar el encargo que me llego.",
    "Responde solo un objeto JSON con los campos pedidos.",
    '"resultado": "la vuelta se cerro sin incidencias",',
    '"observaciones": "el obrero termino su tarea a tiempo",',
    "VEREDICTO: APROBADO",
    "OBRERO deepseek -> AUDITOR groq",
]


def test_el_ruido_de_la_maquina_no_se_cola_como_orden():
    """La maquina no le da ordenes a Julio: su ruido no debe pasar el candado."""
    for texto in TEXTOS_DE_LA_MAQUINA:
        recogida = candado_legislar.parece_una_orden(texto)
        assert recogida is False, (
            "Se colo como orden de Julio un texto que escribe la maquina: "
            "%r. La maquina no le da ordenes a Julio." % (texto,)
        )
