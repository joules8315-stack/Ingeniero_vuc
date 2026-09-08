# -*- coding: utf-8 -*-
"""VIGIA — LO QUE JULIO VE EN PANTALLA ES LO QUE LA MAQUINA USA POR DENTRO.

FALLO REAL MEDIDO (2026-09-08): el mapa de maquina `mapa/MAPA_INGENIERO.json` estaba
regenerado el 2026-09-07 a las 11:35, y el mapa que Julio LEE, `mapa/MAPA_INGENIERO.md`,
llevaba congelado desde el 2026-08-20 a las 12:29. DIECIOCHO DIAS de diferencia.

POR QUE IMPORTA, y no es un detalle de fechas: el apartado 10 del mapa legible se titula
"LO QUE NO EXISTE (lo que hay que construir)" y le lista a Julio cinco piezas QUE YA
EXISTEN desde hace semanas (el que arma el paquete, el candado de lectura, CLAUDE.md, el
estado guardado y el cerebro propio del Ingeniero). O sea: el mapa le estaba mandando a
construir lo que ya tiene. Ahi esta una raiz de la repetidera medida el 2026-09-08 (el
mismo fallo reparado 25, 27 y 22 veces).

CAUSA RAIZ: `mapa/inventario.py` escribe el .json y termina. `mapa/compilar_mapa.py` es
quien lo pasa a limpio al .md, y es un programa SUELTO que hay que acordarse de lanzar a
mano. Un paso que depende de que alguien se acuerde no se hace: eso ya esta escrito en la
memoria de fallos de esta casa con otras palabras ("un contador que hay que acordarse de
subir no mide: adorna").

LEY QUE HACE CUMPLIR — punto 9 del PLAN CERRADO v2 (Julio, 2026-09-08):
  "Todo estado que el Ingeniero muestre como actual debe corresponder al mismo estado
   canonico que utiliza la maquina. Un mapa, memoria, indice, pantalla o informe obsoleto
   NO PUEDE presentarse como estado actual."

ES UNA CUENTA, NO UN JUICIO (CONTRATO_CUENTA_O_JUICIO.md, Julio 2026-09-07): comparar dos
fechas y comprobar que un programa deja al dia a otro son cuentas. Por eso esta vigia no
llama a ningun cerebro: la hace un programa, gratis y sin equivocarse.
"""
import os
import re

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(AQUI, "mapa")
DE_MAQUINA = os.path.join(MAPA, "MAPA_INGENIERO.json")
LEGIBLE = os.path.join(MAPA, "MAPA_INGENIERO.md")
QUIEN_CUENTA = os.path.join(MAPA, "inventario.py")


def test_el_mapa_legible_no_es_mas_viejo_que_el_de_maquina():
    """Lo que Julio lee no puede tener fecha anterior a lo que la maquina usa."""
    if not os.path.exists(DE_MAQUINA) or not os.path.exists(LEGIBLE):
        pytest.skip("en esta maquina no estan los dos mapas: no se falsea un verde")
    de_maquina = os.path.getmtime(DE_MAQUINA)
    legible = os.path.getmtime(LEGIBLE)
    dias = (de_maquina - legible) / 86400.0
    assert legible >= de_maquina, (
        "EL MAPA QUE VE JULIO ESTA CADUCADO: el legible es %.1f dias mas viejo que el de "
        "maquina. Julio lee una foto vieja mientras la maquina trabaja con otra. "
        "Lo arregla mapa/compilar_mapa.py, que tiene que correr solo al terminar de contar."
        % dias)


def test_el_que_cuenta_deja_el_legible_al_dia_sin_que_nadie_se_acuerde():
    """Contar tiene que dejar el mapa legible al dia SOLO. Sin segundo comando a mano.

    No se comprueba leyendo el codigo: se corre de verdad al que cuenta y se mira si el
    legible quedo al dia. Si hace falta acordarse de un segundo paso, esta prueba lo caza.
    """
    if not os.path.exists(QUIEN_CUENTA):
        pytest.skip("no esta el que cuenta en esta maquina: no se falsea un verde")
    with open(QUIEN_CUENTA, encoding="utf-8") as f:
        codigo = f.read()
    # Solo se quitan los textos entre TRIPLES comillas y los comentarios. NO se puede quitar
    # lo que va entre comillas sueltas: ahi vive justo el nombre que se busca, porque el que
    # cuenta llama al que pasa a limpio pasandole su nombre entre comillas.
    vivo = re.sub(r'"""(?:.|\n)*?"""', ' ', codigo)
    vivo = re.sub(r"'''(?:.|\n)*?'''", ' ', vivo)
    vivo = '\n'.join(re.sub(r'#.*$', '', ln) for ln in vivo.splitlines())
    assert 'compilar_mapa' in vivo, (
        "EL QUE CUENTA NO LLAMA AL QUE PASA A LIMPIO: pasar el mapa a limpio vuelve a ser un "
        "programa suelto que hay que acordarse de lanzar, y por eso llego a tener 18 dias de "
        "retraso. Contar y pasar a limpio son el MISMO acto.")
    assert vivo.find('json.dump') < vivo.find('compilar_mapa'), (
        "se pasa a limpio ANTES de escribir el mapa de maquina: copiaria el viejo")
