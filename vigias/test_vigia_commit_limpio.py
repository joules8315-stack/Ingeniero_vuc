# -*- coding: utf-8 -*-
"""VIGIA — LEY L6: TODO QUEDA LIMPIO Y EN COMMIT, Y LO NUEVO SE INDEXA.

Julio, 2026-08-24: "todo debe quedar limpio, en commit, eso ya se hablo, pon candado y crea vigia."
Y lo corregido por Claude: si aparece algo nuevo y nadie lo anota en el indice, se pone rojo.

Comprueba que el guardia de guardado existe (lo ejecuta git, no la IA) y que las leyes nuevas
quedaron escritas e indexadas en el mapa de la forma de trabajo.
"""
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_el_guardia_de_guardado_existe_y_lo_ejecuta_git():
    assert os.path.exists(os.path.join(AQUI, "arnes", "guardia_de_guardado.py")), \
        "no existe el guardia de guardado"
    hook = os.path.join(AQUI, "hooks", "pre-commit")
    assert os.path.exists(hook), "no esta el gancho pre-commit"
    txt = open(hook, encoding="utf-8", errors="ignore").read()
    assert "guardia_de_guardado" in txt, "el gancho no corre el guardia"


def test_las_leyes_nuevas_estan_indexadas():
    """El contrato de legislacion total esta en el mapa de la forma de trabajo."""
    proto = open(os.path.join(AQUI, "cerebro", "protocolo.py"), encoding="utf-8").read()
    assert "CONTRATO_LEGISLACION_TOTAL" in proto or "LEGISLACION_TOTAL" in proto, \
        "la legislacion total no esta indexada en el mapa"


def test_el_guardia_frena_con_rojas():
    """El guardia NO deja guardar dejando algo roto."""
    txt = open(os.path.join(AQUI, "arnes", "guardia_de_guardado.py"), encoding="utf-8").read()
    assert "ROJAS" in txt or "rojas" in txt, "el guardia no frena con pruebas rojas"


def test_el_guardian_no_grita_por_sus_propios_cuadernos():
    """EL GUARDIAN QUE SE MUERDE LA COLA, TERCERA VEZ (2026-09-11).

    Guardar hace correr a los guardianes, y los guardianes escriben en sus cuadernos. Asi que
    al terminar de guardar YA hay cosas sin guardar, y el candado vuelve a frenar: guarde las
    veces que guarde, nunca queda limpio. Es un bucle sin salida.

    Ya se curo dos veces (2026-08-31 y 2026-09-02) anadiendo los cuadernos a la lista de
    perdonados, y las dos veces volvio porque aparecio un cuaderno nuevo y NADIE lo apunto.
    Esta prueba lo caza sola: nombra los cuadernos que el sistema se escribe a si mismo.

    OJO CON LO QUE NO ENTRA AQUI: memoria/ESTADO.json (donde ibamos) NO es un cuaderno de
    candado, es trabajo de verdad, y tiene que seguir gritando. Perdonarlo seria perder el
    sitio por donde ibamos.

    Se EJECUTA el camino real (_es_cuaderno), no se busca ninguna palabra en ningun archivo.
    """
    import sys
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import candado_commit as cc
    suyos = [
        "memoria/CUADERNO_DE_LLAMADAS.jsonl",
        "memoria/MEDICIONES.json",
        "memoria/CANDADOS_MEDICION.json",
        "memoria/DIAGNOSTICO.json",
        "memoria/APLICACIONES.log",
        "memoria/BALANCE.log",
    ]
    olvidados = [r for r in suyos if not cc._es_cuaderno(r)]
    assert not olvidados, (
        "EL GUARDIAN SE MUERDE LA COLA: estos cuadernos los escribe el propio sistema al "
        "guardar, y el candado los cuenta como trabajo sin guardar. Guarde las veces que "
        "guarde, nunca quedara limpio: %s" % olvidados)
    assert not cc._es_cuaderno("memoria/ESTADO.json"), (
        "SE PERDONO DE MAS: donde ibamos NO es un cuaderno de candado, es trabajo de verdad. "
        "Si deja de gritar, se pierde el sitio por donde ibamos.")
