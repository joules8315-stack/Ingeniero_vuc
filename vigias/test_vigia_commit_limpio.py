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


def test_una_regla_y_no_una_lista_perdona_las_notas_nuevas():
    """EL GUARDIAN SE MUERDE LA COLA, CUARTA VEZ (2026-09-14). Tres curas anadieron nombres a mano
    y el bucle volvio con cada nota nueva. Esta prueba exige una REGLA: cualquier nota oculta o
    registro nuevo de la raiz de memoria se perdona, aunque nadie lo apunte; el trabajo no."""
    import sys
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import candado_commit as cc
    notas = [
        "memoria/.legislacion_pendiente.json",
        "memoria/RESPUESTAS.json",
        "memoria/.veredictos_recientes.jsonl",
        "memoria/.buzon_bloqueos",
        "memoria/INDICE_METODO.json",
        "memoria/.nota_que_aun_no_existe",
        "memoria/REGISTRO_QUE_AUN_NO_EXISTE.log",
    ]
    no_perdonadas = [r for r in notas if not cc._es_cuaderno(r)]
    assert not no_perdonadas, (
        "EL GUARDIAN SE MUERDE LA COLA OTRA VEZ: estas notas las escriben los candados y cuentan "
        "como trabajo sin guardar; con una lista a mano volvera con cada nota nueva: %s" % no_perdonadas)
    trabajo = [
        "memoria/ESTADO.json",
        "memoria/continuacion_2026-09-13.md",
        "memoria/trabajos_del_equipo/2026-09-14_043642_APROBADO_guardia_de_guardado.py.json",
        "memoria/trabajos_sin_revisar/big_pickle.patch",
        "memoria/paquetes/.oculto_de_prueba.md",
        "arnes/candado_commit.py",
        "vigias/.oculta.log",
    ]
    perdonado_de_mas = [r for r in trabajo if cc._es_cuaderno(r)]
    assert not perdonado_de_mas, (
        "SE PERDONO DE MAS: esto es trabajo de verdad (donde ibamos, trabajo pagado, codigo) y "
        "tiene que seguir exigiendo guardarse: %s" % perdonado_de_mas)


def test_ninguna_prueba_escribe_en_los_cuadernos_de_verdad():
    """LA CAUSA DE FONDO DEL GUARDIAN QUE SE MUERDE LA COLA (2026-09-11).

    MEDIDO ESE DIA, no supuesto: se tomo la huella de seis cuadernos, se corrieron los 661
    guardianes sin tocar nada mas, y CINCO DE SEIS habian cambiado. Los guardianes escriben en
    la memoria DE VERDAD.

    Y esta casa YA TIENE ESA LEY ESCRITA, de un fallo que costo 27 de 32 errores aprendidos:
    "no volver a dejar que una prueba escriba en la memoria de verdad". Se curo para unas cosas
    (el contexto, la casa, el contador del protocolo, la llave de Julio y el cuaderno del
    equipo) y NUNCA para estas. Las dos curas del 31-ago y del 02-sep fueron PERDONAR los
    cuadernos en el candado de guardar: eso tapa el sintoma, no cierra el grifo.

    Esta prueba cierra el grifo y lo vigila. Mira DONDE APUNTA cada cuaderno mientras se
    prueba: si apunta a la memoria de verdad, ROJA.
    """
    import sys
    sys.path.insert(0, AQUI)
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    from cuerpo import cuaderno as _cua
    import candados_medicion as _cm
    import candado_diagnostico as _cd
    import candado_memoria as _cmem
    import candado_prueba_real as _cpr
    real = os.path.join(AQUI, "memoria").lower().replace("\\", "/")
    sitios = {
        "el cuaderno de llamadas": _cua.RUTA,
        "la medicion de los candados": _cm.RUTA,
        "el diagnostico": _cd.RUTA,
        "los avisos ya dados": _cmem.AVISADOS,
        "las pruebas reales": _cpr.PRUEBAS,
        "las aplicaciones del copista": os.environ.get("INGENIERO_APLICACIONES", ""),
    }
    tocan = [n for n, r in sitios.items()
             if (not str(r)) or str(r).lower().replace("\\", "/").startswith(real)]
    assert not tocan, (
        "UNA PRUEBA ESTA ESCRIBIENDO EN LA MEMORIA DE VERDAD, que es justo lo que esta casa "
        "tiene prohibido desde que costo 27 de 32 errores aprendidos. Ademas es lo que hace "
        "que el guardian se muerda la cola: guardar ensucia, y por eso nunca queda limpio. "
        "Apuntan a lo real: %s" % tocan)
