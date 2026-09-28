"""Vigia: el aviso del revisor NO frena la ronda.

Nace ROJA a proposito. El cambio del codigo entra en rondas siguientes; en esta
ronda no se toca ningun otro archivo.

Hecho medido (2026-09-28): el revisor por programa tumbo un cambio ya aprobado
por el auditor del equipo con el motivo 'NO HACE LO QUE SE PIDIO: el encargo
habla de soltar_turno y esa palabra no aparece'. Era falso: el encargo nombraba
esas piezas como explicacion, no para cambiarlas. La cuenta adivina INTENCION y
la intencion es juicio, no cuenta (CONTRATO_CUENTA_O_JUICIO).

Lo que hay que lograr: que el revisor pueda decir algo SIN frenar. Un mensaje
que empiece por 'AVISO:' es un aviso: se dice, se ve y NO corta la ronda. Todo
lo demas sigue frenando igual.

Las tres pruebas son por COMPORTAMIENTO, sin IA, sin red y sin lanzar procesos.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo.obrero import separar_avisos_y_frenos


def test_4_el_mensaje_de_no_hace_lo_que_se_pidio_es_aviso():
    """Nace ROJA a proposito: la reparacion va en cuerpo/obrero.py, no aqui.

    Hoy separar_avisos_y_frenos solo mira si el texto empieza por 'AVISO:'.
    El mensaje que empieza por 'NO HACE LO QUE SE PIDIO:' se clasifica como
    freno y corta rondas buenas. Debe salir como AVISO: el programa cuenta,
    el juicio de la intencion no es suyo (CONTRATO_CUENTA_O_JUICIO).
    """
    mensajes = [
        "AVISO: esto es un aviso de verdad",
        "NO HACE LO QUE SE PIDIO: el obrero entrego otra cosa",
        "el texto viejo no existe en el archivo",
    ]
    avisos, frenos = separar_avisos_y_frenos(mensajes)
    assert avisos == [
        "AVISO: esto es un aviso de verdad",
        "NO HACE LO QUE SE PIDIO: el obrero entrego otra cosa",
    ], "el mensaje de NO HACE LO QUE SE PIDIO debe salir como aviso, no como freno"
    assert frenos == ["el texto viejo no existe en el archivo"]
    assert len(avisos) + len(frenos) == len(mensajes), "ningun mensaje se pierde ni se duplica"
import sys


# Arranque: meter en sys.path la carpeta que esta un nivel arriba de vigias,
# la carpeta cuerpo y la carpeta arnes, a partir de la ruta de este archivo.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
for _ruta in (_RAIZ, os.path.join(_RAIZ, "cuerpo"), os.path.join(_RAIZ, "arnes")):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# El renglon del corte, tal cual vive hoy en cuerpo/obrero.py. Mientras siga
# ahi, el aviso sigue cortando la ronda.
_RENGLON_DEL_CORTE = "if _fallos_prog and _vuelta < 3:"


# El archivo de verdad que se lee (no se toca) para la prueba 3.
_ARCHIVO_DE_VERDAD = os.path.join(_RAIZ, "cuerpo", "obrero.py")


def test_1_separar_avisos_y_frenos_reparte_por_comportamiento():
    """Prueba 1, hoy ROJA: existe en cuerpo/obrero.py una funcion publica que
    reparte una lista de mensajes en dos: los avisos y los frenos.

    Se llama con tres mensajes: uno que empieza por AVISO y dos puntos, otro
    que empieza igual pero con espacios delante, y otro que es un freno normal.
    Los dos primeros salen como avisos y el tercero como freno, y ninguno se
    pierde ni se duplica.
    """
    import obrero

    assert hasattr(obrero, "separar_avisos_y_frenos"), (
        "cuerpo/obrero.py todavia no tiene la funcion publica "
        "separar_avisos_y_frenos: sin ella el aviso del revisor sigue "
        "cortando la ronda"
    )

    aviso_limpio = "AVISO: el encargo nombraba soltar_turno como explicacion, no para cambiarla"
    aviso_con_espacios = "   AVISO: esto tambien es un aviso y no debe frenar"
    freno_normal = "NO HACE LO QUE SE PIDIO: falta el texto viejo"

    mensajes = [aviso_limpio, aviso_con_espacios, freno_normal]
    avisos, frenos = obrero.separar_avisos_y_frenos(mensajes)

    assert avisos == [aviso_limpio, aviso_con_espacios], (
        "los mensajes que empiezan por AVISO y dos puntos (con o sin espacios "
        "delante) tienen que salir como avisos; salieron: %r" % (avisos,)
    )
    assert frenos == [freno_normal], (
        "el mensaje que no empieza por AVISO tiene que salir como freno; "
        "salieron: %r" % (frenos,)
    )

    # Ninguno se pierde ni se duplica.
    assert len(avisos) + len(frenos) == len(mensajes), (
        "no se puede perder ni duplicar ningun mensaje: entraron %d y "
        "salieron %d" % (len(mensajes), len(avisos) + len(frenos))
    )
    assert sorted(avisos + frenos) == sorted(mensajes), (
        "los mensajes que salen tienen que ser exactamente los que entraron"
    )


def test_2_el_corte_ya_no_usa_la_lista_cruda():
    """Prueba 2, hoy ROJA: el corte ya no usa la lista cruda.

    Se lee el texto de cuerpo/obrero.py y se comprueba que el renglon del
    corte, ese que dice si hay fallos del programa y la vuelta es menor que
    tres, YA NO aparece tal cual, porque el corte tiene que mirar solo los
    frenos. Es una comprobacion sobre el hecho y no sobre un nombre: mientras
    ese renglon siga ahi, el aviso sigue cortando la ronda.
    """
    with open(_ARCHIVO_DE_VERDAD, "r", encoding="utf-8") as f:
        texto = f.read()

    assert _RENGLON_DEL_CORTE not in texto, (
        "cuerpo/obrero.py todavia tiene el renglon del corte %r: mientras "
        "siga ahi, el aviso del revisor sigue cortando la ronda"
        % _RENGLON_DEL_CORTE
    )


def test_3_un_freno_de_verdad_sigue_frenando_y_no_se_marca_como_aviso():
    """Prueba 3, tiene que quedar VERDE hoy: no se afloja lo que si sirve.

    Un freno de verdad sigue frenando y NO se marca como aviso. Se llama a la
    funcion revisar del revisor con una propuesta de mentira cuyo texto viejo
    NO existe en el archivo que dice cambiar (la cuenta mas barata y mas segura
    del revisor), usando como archivo una pieza de verdad del proyecto que solo
    se lee y no se toca. Se comprueba que devuelve al menos un mensaje y que
    ninguno empieza por AVISO y dos puntos.
    """
    import revisor_de_programa

    propuesta = {
        "archivo": "cuerpo/obrero.py",
        "texto_viejo": "ESTE_TEXTO_VIEJO_NO_EXISTE_EN_EL_ARCHIVO_DE_VERDAD_2026_09_28",
        "texto_nuevo": "# texto nuevo de mentira para la prueba\n",
    }
    tarea = "prueba de comportamiento: un freno de verdad sigue frenando"

    mensajes = revisor_de_programa.revisar(propuesta, tarea)

    assert isinstance(mensajes, list), (
        "revisar tiene que devolver una lista de textos; devolvio: %r" % (type(mensajes),)
    )
    assert len(mensajes) >= 1, (
        "un texto viejo que no existe en el archivo tiene que producir al "
        "menos un mensaje de freno; devolvio la lista vacia"
    )

    for mensaje in mensajes:
        assert not str(mensaje).lstrip().startswith("AVISO:"), (
            "un freno de verdad no se puede marcar como aviso; salio: %r"
            % (mensaje,)
        )
