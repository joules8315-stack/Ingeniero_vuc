#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_cierre_dice_el_medidor.py — EL MEDIDOR DE RONDAS NACE CONECTADO.

Julio, 2026-09-08 (Regla 6 del contrato de crear pieza nueva):

    "Por que siguen cosas desconectadas, y lo mejor, POR QUE NACEN DESCONECTADAS.
     Legisla: nada puede crearse y quedar huerfano."

    "La pieza no esta terminada hasta que algo la llama."

QUE VIGILA ESTA VIGIA
---------------------
Que el medidor de rondas NO nazca huerfano: que el candado de cierre lo nombre de verdad
en su codigo, y que nombre tambien la funcion que usa (contar). Una pieza que existe pero
que nadie llama no sirve de nada: es exactamente el fallo medido el 2026-09-08, cuando
25 de 38 contratos y 11 habilidades estaban escritos y con CERO llamadas.

COMO LO COMPRUEBA (sin ejecutar nada, solo leyendo texto)
--------------------------------------------------------
PRUEBA 1: se lee arnes/candado_cierre.py como texto y se comprueba que aparece la palabra
          medidor_de_rondas.
PRUEBA 2: en ese mismo texto se comprueba que aparece tambien la palabra contar, que es la
          funcion del medidor que se usa.

La ruta del archivo vigilado se arma desde la carpeta de esta propia vigia: se sube un
nivel (la raiz del proyecto) y se entra en arnes. Asi la vigia funciona aunque el proyecto
se mueva de sitio.

Las dos pruebas leen el archivo con codificacion utf-8 y con errors puesto en replace, para
que un byte raro no tumbe la lectura.
"""

import os


# La carpeta de esta vigia (vigias/), su padre es la raiz del proyecto.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CANDADO_CIERRE = os.path.join(RAIZ, "arnes", "candado_cierre.py")


def _leer_candado_cierre():
    """Lee arnes/candado_cierre.py entero como texto.

    Se lee con utf-8 y errors='replace' para que ningun byte raro impida la lectura:
    lo que se comprueba es que el texto NOMBRA al medidor, no que el archivo sea bonito.
    """
    with open(CANDADO_CIERRE, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def test_el_cierre_nombra_al_medidor_de_rondas():
    """PRUEBA 1: el candado de cierre nombra al medidor de rondas.

    Si el candado de cierre no nombra al medidor, el medidor nace huerfano: existe el
    archivo pero nadie lo llama. Una pieza que nadie llama no sirve de nada.
    """
    texto = _leer_candado_cierre()
    assert "medidor_de_rondas" in texto, (
        "El candado de cierre (arnes/candado_cierre.py) NO nombra al medidor de rondas "
        "(no aparece 'medidor_de_rondas'). Una pieza que nadie llama no sirve de nada: "
        "el medidor nace huerfano y al terminar nadie dice en voz alta cuanto se perdio."
    )


def test_el_cierre_usa_la_funcion_contar_del_medidor():
    """PRUEBA 2: el candado de cierre usa la funcion contar del medidor.

    No basta con nombrar la pieza: hay que usar su funcion. Si no aparece 'contar', el
    medidor esta escrito pero su funcion no se llama desde el flujo.
    """
    texto = _leer_candado_cierre()
    assert "contar" in texto, (
        "El candado de cierre (arnes/candado_cierre.py) NO usa la funcion 'contar' del "
        "medidor de rondas. Nombrar la pieza no es conectarla: si su funcion no se llama, "
        "el medidor sigue huerfano y al terminar nadie dice cuanto se perdio."
    )


if __name__ == "__main__":
    test_el_cierre_nombra_al_medidor_de_rondas()
    test_el_cierre_usa_la_funcion_contar_del_medidor()
    print("VIGIA VERDE: el candado de cierre nombra al medidor de rondas y usa contar.")
