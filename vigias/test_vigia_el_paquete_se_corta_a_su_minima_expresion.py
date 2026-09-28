# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_paquete_se_corta_a_su_minima_expresion.py

VIGIA QUE NACE ROJA A PROPOSITO (2026-09-28).

Hecho medido: un paquete real pesaba 42.859 letras y los trozos de codigo eran 30.327.
De los siete trozos que viajaron solo tres hacian falta, 15.151 letras. El 49 por ciento
era relleno, y 2.504 letras iban duplicadas porque un trozo estaba contenido dentro de
otro trozo del mismo archivo.

Julio lo resumio asi: todo material se corta a su minima expresion, completa y que
funcione, y despues se busca la IA idonea.

Esta vigia exige DOS funciones nuevas de cerebro/router.py:

  - quitar_contenidos(trozos): devuelve otra lista sin los trozos que esten contenidos
dentro de otro trozo de la MISMA pieza. Un trozo esta contenido cuando tiene el mismo
valor de pieza que otro y su desde es mayor o igual y su hasta es menor o igual que los
de ese otro. Se queda el que contiene y se va el contenido. Dos trozos de piezas
distintas nunca se estorban. El orden de los que quedan no cambia. Nunca lanza.

  - recortar_por_presupuesto(trozos, tope): devuelve los trozos que caben en ese tope,
tomandolos de mayor a menor puntaje y sumando la longitud de su texto. El de mayor
puntaje se queda SIEMPRE, aunque el solo ya pase del tope. Los que no caben se quedan
fuera. Nunca lanza.

En esta ronda las dos funciones NO se escriben: la vigia nace antes que el cambio.
Por eso las importaciones van DENTRO de cada prueba y las cinco pruebas deben salir
ROJAS con ImportError hasta que cerebro/router.py las tenga.

Reglas de la prueba: trozos de mentira hechos a mano dentro de la propia prueba, sin
leer ningun archivo del proyecto, sin escribir en ninguna carpeta, sin red y sin llamar
a ninguna IA. Los nombres de pieza de mentira son pieza_de_mentira_uno.py y
pieza_de_mentira_dos.py, para que no se confundan nunca con un archivo de verdad.
"""
import os
import sys

# Arranque: la carpeta que esta un nivel arriba de la carpeta vigias entra en sys.path,
# para que se pueda importar cerebro.router como paquete del proyecto.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

PIEZA_UNO = "pieza_de_mentira_uno.py"
PIEZA_DOS = "pieza_de_mentira_dos.py"


def _trozo(pieza, desde, hasta, texto, puntaje):
    """Trozo de mentira con las cinco claves del contrato: pieza, desde, hasta, texto, puntaje."""
    return {"pieza": pieza, "desde": desde, "hasta": hasta,
            "texto": texto, "puntaje": puntaje}


def test_el_trozo_contenido_no_viaja():
    """Prueba 1: dos trozos de la misma pieza, uno dentro de otro. Queda solo el que contiene."""
    from cerebro.router import quitar_contenidos

    grande = _trozo(PIEZA_UNO, 100, 200, "texto grande de mentira", 10)
    chico = _trozo(PIEZA_UNO, 120, 150, "texto chico de mentira", 99)

    quedan = quitar_contenidos([grande, chico])

    assert len(quedan) == 1
    assert quedan[0]["desde"] == 100
    assert quedan[0]["hasta"] == 200


def test_dos_trozos_separados_se_quedan_los_dos():
    """Prueba 2: dos trozos de la misma pieza que no se solapan. Se quedan los dos."""
    from cerebro.router import quitar_contenidos

    primero = _trozo(PIEZA_UNO, 1, 50, "texto primero de mentira", 10)
    segundo = _trozo(PIEZA_UNO, 60, 90, "texto segundo de mentira", 20)

    quedan = quitar_contenidos([primero, segundo])

    assert len(quedan) == 2
    assert quedan[0]["desde"] == 1
    assert quedan[1]["desde"] == 60


def test_los_numeros_de_otra_pieza_no_estorban():
    """Prueba 3: numeros parecidos pero piezas distintas. Se quedan los dos."""
    from cerebro.router import quitar_contenidos

    uno = _trozo(PIEZA_UNO, 100, 200, "texto de la pieza uno", 10)
    dos = _trozo(PIEZA_DOS, 120, 150, "texto de la pieza dos", 20)

    quedan = quitar_contenidos([uno, dos])

    assert len(quedan) == 2
    assert quedan[0]["pieza"] == PIEZA_UNO
    assert quedan[1]["pieza"] == PIEZA_DOS


def test_solo_cabe_lo_que_entra_en_el_tope():
    """Prueba 4: tres trozos de 1000 letras con tope 2500. Entran los dos de mayor puntaje."""
    from cerebro.router import recortar_por_presupuesto

    alto = _trozo(PIEZA_UNO, 1, 10, "a" * 1000, 99)
    medio = _trozo(PIEZA_UNO, 20, 30, "b" * 1000, 50)
    bajo = _trozo(PIEZA_UNO, 40, 50, "c" * 1000, 10)

    quedan = recortar_por_presupuesto([alto, medio, bajo], 2500)

    assert len(quedan) == 2
    assert quedan[0]["puntaje"] == 99
    assert quedan[1]["puntaje"] == 50
    assert all(t["puntaje"] != 10 for t in quedan)


def test_el_de_mayor_puntaje_se_queda_aunque_no_quepa():
    """Prueba 5: un solo trozo de 5000 letras con tope 1000. Se queda igual."""
    from cerebro.router import recortar_por_presupuesto

    unico = _trozo(PIEZA_UNO, 1, 10, "d" * 5000, 99)

    quedan = recortar_por_presupuesto([unico], 1000)

    assert len(quedan) == 1
    assert quedan[0]["puntaje"] == 99
    assert len(quedan[0]["texto"]) == 5000
