# -*- coding: utf-8 -*-
"""Vigia: la cadena trabaja en varias tareas a la vez.

Orden de Julio del 2026-09-28 (maxima prioridad). Ley que manda:
CONTRATO_LA_MULTITAREA_ES_LA_FORMA_DE_TRABAJAR.md.

Esta vigia SUSTITUYE a la vigia vieja
`vigias/test_vigia_el_pit_corre_una_tarea_a_la_vez.py`, que exigia que el segundo
parametro de `cuerpo.capataz.bucle` siguiera siendo uno. Aquella vigia se escribio
como freno provisional mientras no existieran turnos para guardar; con los turnos
ya legislados, ese freno queda retirado y su exigencia queda derogada por esta
vigia. En esta ronda la vigia vieja NO se toca ni se borra: solo queda dicho aqui
que esta la sustituye.

Nace ROJA a proposito en dos de sus tres pruebas (prueba 1 y prueba 3): el cambio
del codigo entra en la ronda siguiente. La prueba 2 debe quedar VERDE hoy porque
la coherencia ya la garantiza la cola.

Sin IA, sin red y sin lanzar procesos de verdad.
"""

import os
import sys


# Arranque: meter en sys.path la carpeta un nivel arriba de `vigias` y la carpeta
# `cuerpo`, usando os.path a partir de la ruta de este mismo archivo.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
_CUERPO = os.path.join(_RAIZ, "cuerpo")
for _p in (_RAIZ, _CUERPO):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ---------------------------------------------------------------------------
# Prueba 1 (HOY ROJA): el mando no se queda en una sola tarea.
# ---------------------------------------------------------------------------
def test_el_mando_pide_varias_a_la_vez(monkeypatch):
    """El mando `pit` de ingeniero.py debe pasar un `en_paralelo` mayor que uno.

    Hoy sale ROJA porque el mando llama a `_cap.bucle(sys.argv[2])` sin pasar el
    segundo parametro, y queda el uno por defecto de la firma.
    """
    import ingeniero
    from cuerpo import capataz

    apuntes = []

    def bucle_falso(proyecto, en_paralelo=1, tope_segundos=900, aviso=print):
        # Apunta el valor de en_paralelo, venga por nombre o en la 2a posicion.
        apuntes.append({
            "proyecto": proyecto,
            "en_paralelo": en_paralelo,
            "tope_segundos": tope_segundos,
        })
        return "texto_de_mentira"

    monkeypatch.setattr(capataz, "bucle", bucle_falso)
    monkeypatch.setattr(
        sys, "argv",
        ["ingeniero.py", "pit", "proyecto_de_mentira"],
    )

    ingeniero.main()

    # Si el falso no se llamo ni una vez, la prueba FALLA diciendolo: nunca
    # puede ponerse verde sin haber medido nada.
    assert len(apuntes) == 1, (
        "el mando no llamo ni una vez a cuerpo.capataz.bucle: "
        "no se midio nada (apuntes=%r)" % (apuntes,)
    )

    valor = apuntes[0]["en_paralelo"]
    assert valor > 1, (
        "el mando sigue corriendo de una en una: en_paralelo=%r; "
        "la multitarea es la forma de trabajar" % (valor,)
    )


# ---------------------------------------------------------------------------
# Prueba 2 (VERDE hoy): la coherencia la garantiza la cola.
# ---------------------------------------------------------------------------
def test_la_cola_garantiza_la_coherencia(monkeypatch):
    """`listas_para_correr` no repite pieza, respeta dependencias y estado."""
    from cuerpo import capataz

    ordenes = [
        # Dos ordenes distintas de la MISMA pieza: no pueden salir las dos.
        {
            "id": "o1",
            "pieza": "pieza_de_mentira_uno.py",
            "estado": "pendiente",
            "depende": [],
        },
        {
            "id": "o2",
            "pieza": "pieza_de_mentira_uno.py",
            "estado": "pendiente",
            "depende": [],
        },
        # Depende de una que NO esta hecha: no puede salir.
        {
            "id": "o3",
            "pieza": "pieza_de_mentira_dos.py",
            "estado": "pendiente",
            "depende": ["o4"],
        },
        # Esta NO esta hecha (sigue pendiente): sirve de dependencia incumplida.
        {
            "id": "o4",
            "pieza": "pieza_de_mentira_tres.py",
            "estado": "pendiente",
            "depende": [],
        },
        # Depende de una que SI esta hecha: puede salir.
        {
            "id": "o5",
            "pieza": "pieza_de_mentira_cuatro.py",
            "estado": "pendiente",
            "depende": ["o6"],
        },
        # Ya esta hecha: sirve de dependencia cumplida.
        {
            "id": "o6",
            "pieza": "pieza_de_mentira_cinco.py",
            "estado": "hecha",
            "depende": [],
        },
    ]

    monkeypatch.setattr(capataz, "leer_lista", lambda: list(ordenes))
    monkeypatch.setattr(capataz, "validar_etiqueta", lambda *a, **k: "")
    monkeypatch.setattr(capataz, "ya_fallo", lambda *a, **k: False)

    resultado = capataz.listas_para_correr()

    # Nada de aserciones que pasen mirando una lista vacia.
    assert isinstance(resultado, list), (
        "listas_para_correr no devolvio una lista: %r" % (resultado,)
    )
    assert len(resultado) >= 2, (
        "la cola no dejo salir al menos dos ordenes: %r" % (resultado,)
    )
    for orden in resultado:
        assert isinstance(orden, dict), (
            "la cola devolvio algo que no es diccionario: %r" % (orden,)
        )

    piezas = [o.get("pieza") for o in resultado]
    assert len(piezas) == len(set(piezas)), (
        "la cola dejo salir dos ordenes de la misma pieza: %r" % (piezas,)
    )

    ids = [o.get("id") for o in resultado]
    assert "o3" not in ids, (
        "la cola dejo salir una orden que espera a una que no esta hecha: %r" % (ids,)
    )

    for orden in resultado:
        assert orden.get("estado") == "pendiente", (
            "la cola dejo salir una orden que no estaba pendiente: %r" % (orden,)
        )


# ---------------------------------------------------------------------------
# Prueba 3 (HOY ROJA): los turnos para guardar.
# ---------------------------------------------------------------------------
def test_los_turnos_para_guardar(monkeypatch, tmp_path):
    """Existe una pieza en `arnes` que da turno para guardar, con tope.

    Hoy sale ROJA porque esa pieza todavia no existe. El nombre del archivo y de
    su funcion los elige esta vigia: `arnes/turno_de_guardado.py` con la funcion
    `turno_de_guardado`. La prueba la nombra, la usa de verdad con dos turnos
    seguidos y falla hoy con un mensaje claro de que todavia no existe.

    Lo que se comprueba cuando exista:
      - el segundo en llegar espera y entra cuando el primero suelta;
      - la espera tiene tope de tiempo;
      - si el tope se pasa, se devuelve fallo con su motivo y NO se espera para
        siempre.
    """
    import importlib

    ruta_pieza = os.path.join(_RAIZ, "arnes", "turno_de_guardado.py")
    assert os.path.isfile(ruta_pieza), (
        "todavia no existe la pieza de turnos para guardar: %s; "
        "sin ella dos guardados a la vez se pisan" % (ruta_pieza,)
    )

    modulo = importlib.import_module("arnes.turno_de_guardado")
    assert hasattr(modulo, "turno_de_guardado"), (
        "la pieza %s no trae la funcion turno_de_guardado" % (ruta_pieza,)
    )

    # El turno se prueba dentro de la carpeta temporal que da pytest, sin tocar
    # el proyecto.
    carpeta = str(tmp_path)

    # Primer turno: entra y suelta.
    with modulo.turno_de_guardado(carpeta, tope_segundos=5) as t1:
        assert t1 is not None, "el primer turno no dio nada"

    # Segundo turno seguido: entra cuando el primero ya solto.
    with modulo.turno_de_guardado(carpeta, tope_segundos=5) as t2:
        assert t2 is not None, "el segundo turno no entro tras soltar el primero"

    # Tope de tiempo: si el tope se pasa, se devuelve fallo con su motivo y NO
    # se espera para siempre.
    with modulo.turno_de_guardado(carpeta, tope_segundos=5):
        ok, motivo = modulo.turno_de_guardado(carpeta, tope_segundos=0)
        assert ok is False, (
            "con el tope pasado el turno deberia devolver fallo, no esperar"
        )
        assert motivo, "el fallo del turno vino sin motivo"
