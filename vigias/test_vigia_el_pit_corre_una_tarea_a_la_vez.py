"""Vigia: el pit corre UNA tarea a la vez.

Que vigila
----------
Que `cuerpo.capataz.bucle` siga teniendo `en_paralelo=1` por defecto.

Por que
-------
Medido el 2026-09-21: con dos tareas a la vez, las dos comparten la misma
carpeta de trabajo, y el guardia de una ve el trabajo a medias de la otra.
El guardia entonces no distingue lo que esta terminado de lo que esta a
medio hacer, y da por bueno (o por malo) lo que no le toca.

Cuando se vuelve a 2
--------------------
Solo cuando cada tarea trabaje en su PROPIA COPIA de la carpeta. Mientras
las dos escriban en el mismo sitio, el pit corre una tarea a la vez.

Si esta vigia se pone roja
--------------------------
Alguien subio `en_paralelo` a 2 sin darle a cada tarea su propia copia.
No lo dejes asi: o vuelves a 1, o separas las carpetas primero.
"""

import inspect

from cuerpo import capataz


# El valor por defecto tiene que ser 1: una tarea a la vez.
# Dos a la vez comparten carpeta y el guardia de una ve el trabajo a medias
# de la otra (medido el 2026-09-21).
# Se vuelve a 2 solo cuando cada tarea trabaje en su propia copia.
def test_el_pit_corre_una_tarea_a_la_vez():
    parametros = inspect.signature(capataz.bucle).parameters
    assert 'en_paralelo' in parametros, (
        "capataz.bucle ya no tiene el parametro 'en_paralelo': "
        "la vigia no puede comprobar que el pit corre una tarea a la vez"
    )
    assert parametros['en_paralelo'].default == 1, (
        "capataz.bucle tiene en_paralelo=%r por defecto, y tiene que ser 1: "
        "con dos tareas a la vez comparten la misma carpeta y el guardia de "
        "una ve el trabajo a medias de la otra (medido el 2026-09-21). "
        "Se vuelve a 2 solo cuando cada tarea trabaje en su propia copia."
        % (parametros['en_paralelo'].default,)
    )


if __name__ == '__main__':
    test_el_pit_corre_una_tarea_a_la_vez()
    print('OK: el pit corre una tarea a la vez (en_paralelo=1)')
