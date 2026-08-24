# -*- coding: utf-8 -*-
"""VIGIA — la prueba de las 10 vueltas no puede volver a borrarle el texto a Julio.

FALLO REAL (2026-08-24, Foto Informe). La prueba de las 10 vueltas tenia cinco defectos y el
mas grave destruia datos de verdad:

  1. Ponia el texto manual POR DENTRO (asignando el valor del elemento) y en UNA sola casilla.
     Eso no dispara el guardado del MVP; el unico camino que quedaba era la foto del DOM antes
     de generar, que guarda LO QUE VE: una casilla con texto y siete vacias, y borra las siete.
     Es la trampa ya vivida el 2026-07-16 ("una sonda mia borro 7 textos buenos").
  2. Nunca pulsaba el boton de borrar la asignacion de filas, aunque el encargo es "borra Y
     reasigna". Se saltaba justo la mitad donde vive el fallo historico (ley L19).
  3. Comprobaba buscando un digito suelto en todo el texto del Word aplastado: en un informe
     lleno de fechas y numeros eso sale verde SIEMPRE. Una comprobacion que no puede fallar no
     comprueba nada (ley 3 de Julio: vigia verde NO es prueba).
  4. Citaba un contrato que no existe en el repo (ley 2: nunca inventar).
  5. Generaba sin esperar a que la base guardara: el Word salia sin texto y la prueba acusaba
     al programa de su propia prisa. Esto lo cazo el equipo al auditar la reparacion.

ESTA VIGIA SE PONE ROJA si alguien deshace cualquiera de las cinco curas.
Comprobado saboteando: quitando la cura, se pone roja.
"""
import os

import pytest

RAIZ_FOTO = r"C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"
PRUEBA = os.path.join(RAIZ_FOTO, "rv3_prueba_loop_final.py")

if not os.path.exists(PRUEBA):
    pytest.skip("Foto Informe no esta en esta maquina", allow_module_level=True)

CODIGO = open(PRUEBA, encoding="utf-8", errors="ignore").read()


def test_el_texto_se_teclea_en_las_8_casillas():
    """Cura 1: se escribe con page.fill sobre cada casilla, no poniendo el valor por dentro."""
    assert "page.fill(\"[data-manual-row=" in CODIGO or \
           "page.fill(f\"[data-manual-row=" in CODIGO, \
        "ya no se teclea el texto manual: si se pone el valor por dentro, el MVP borra las otras"


def test_se_espera_a_que_se_vean_las_8_antes_de_escribir():
    """Cura 1b: escribir con las otras vacias es lo que las borra."""
    assert "esperar_a_que_se_vean_las_8" in CODIGO, \
        "se quito la espera a que las 8 casillas se vean: asi es como se borraron 7 textos"


def test_no_se_pone_el_valor_por_dentro():
    """Cura 1c: la enfermedad no puede volver disfrazada."""
    sucio = CODIGO.replace(" ", "")
    assert "c[0].value=" not in sucio, \
        "volvio la escritura por dentro de la primera casilla: eso borra las otras siete"


def test_cada_vuelta_BORRA_la_asignacion():
    """Cura 2: el encargo es 'borra Y reasigna'. Sin el boton, media prueba no se hace."""
    assert "resetRowAssignmentsBtn" in CODIGO, \
        "no se pulsa el boton de borrar la asignacion de filas: falta la mitad del encargo"
    assert "borrar_la_asignacion_de_filas" in CODIGO


def test_el_word_se_comprueba_celda_por_celda():
    """Cura 3: nada de buscar letras sueltas en todo el texto."""
    assert "celdas_del_docx" in CODIGO and "texto_en_su_fila" in CODIGO, \
        "volvio la comprobacion que busca en todo el texto: esa no puede fallar nunca"


def test_no_cita_un_contrato_inventado():
    """Cura 4: ley 2 de Julio, nunca inventar."""
    assert "CONTRATO_PRUEBA_LOOP_FINAL" not in CODIGO, \
        "volvio la cita de un contrato que no existe en el repo"


def test_no_genera_antes_de_que_la_base_guarde():
    """Cura 5: teclear no es guardar. Lo pidio el equipo al auditar."""
    assert "esperar_a_que_la_base_guarde_los_8" in CODIGO, \
        "genera sin esperar el guardado: el Word sale sin texto y se culpa al programa"


def test_las_10_vueltas_reparten_distinto_y_se_comprueba():
    """El encargo pide reasignacion DISTINTA cada vuelta, y que no haya que fiarse."""
    assert "reparto_de_cada_vuelta" in CODIGO, \
        "se quito el reparto comprobado: volvemos a fiarnos de una formula"
