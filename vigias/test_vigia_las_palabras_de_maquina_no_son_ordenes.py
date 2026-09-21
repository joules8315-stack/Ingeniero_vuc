# -*- coding: utf-8 -*-
"""vigias/test_vigia_las_palabras_de_maquina_no_son_ordenes.py

Vigia de `parece_una_orden` (arnes/candado_legislar.py).

Julio, 2026-09-20: un renglon que trae palabras de programador NO es una orden suya.
Si el apuntador se traga `monkeypatch`, `subprocess`, `TypeError`, `assert`, `tmp_path`,
un nombre con parentesis vacios o una ruta acabada en `.py`, se llena la lista de
pendientes de legislar con basura y el candado de cierre frena por nada.

La mitad que de verdad importa es la otra: las frases REALES de Julio tienen que seguir
entrando. Recoger de mas se limpia; perder una orden suya, no.

Textos recogidos el 2026-09-20.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from arnes.candado_legislar import parece_una_orden  # noqa: E402


# --- Renglones de maquina: NO son ordenes de Julio -------------------------
# Palabras de programador, nombres con parentesis vacios, rutas .py, avisos de
# maquina y renglones de informe. Todos vienen de material real del 2026-09-20.
NO_SON_ORDEN = [
    # palabras de programador sueltas dentro de un renglon
    "hay que revisar el monkeypatch de la fixture antes de tocar nada",
    "el subprocess se queda colgado cuando no hay timeout",
    "esto lanza un TypeError si le pasas None",
    "pon un assert antes de seguir con la reparacion",
    "la fixture usa tmp_path para no ensuciar el repo",
    # nombre seguido de parentesis vacios
    "revisar parece_una_orden() antes de cerrar",
    "llamar a pendientes() y mirar el resultado",
    "apuntar_lo_que_dijo_julio() no debe tragarse esto",
    # ruta acabada en .py
    "mira arnes/candado_legislar.py y dime que ves",
    "el fallo esta en vigias/test_vigia_via_canonica.py",
    "abre C:/Ingeniero_VUC/arnes/via_canonica.py y comprueba la rama",
    # avisos de maquina
    "<system-reminder>no leas nada mas</system-reminder>",
    "<command-name>/clear</command-name>",
    # renglones de informe con formato
    '"toca": "arnes/candado_legislar.py"',
    "fallo : el candado no bloquea el cierre",
    "diagnostico : el apuntador se traga lo que dicen otras IA",
    # preguntas y saludos
    "¿esto lo has probado ya?",
    "buenos dias",
    # demasiado corto
    "ok",
    "vale",
    "",
    "   ",
]


# --- Frases REALES de Julio: SI son ordenes y tienen que entrar -------------
# Esta mitad es la que de verdad importa: perder una orden suya no se limpia.
SI_SON_ORDEN = [
    "desde ahora tú autorizas o no a Big Pickle cuando vaya a tocar archivos",
    "no quiero que pida autorizaciones, que como no sé qué pide, se pueda colar",
    "todo lo que yo escriba debe ser legislado, todo, absolutamente todo",
    "la orden es clara, siempre, por eso me toca volver a repetir",
    "debe obligarse a que cumpla, que no le quede opción, de igual manera tú",
    "nada queda a la alucinación, a su memoria",
    "no es solo decirle, porque eso implica que el ayudante puede escoger si seguir la instrucción o no",
    "quiero que vigile cuándo Facebook cambia sus reglas",
    "necesita un buzón, y te digo dónde escribir tú la clave",
    "esta herramienta la lanzas tú a mano cuando quieres",
    "dejo fuera de la cuenta de piezas pendientes esa herramienta",
    "apunta esto para legislarlo antes de cerrar el trabajo de hoy",
]


def _fallo(mensaje):
    sys.stderr.write("FALLO: " + mensaje + "\n")


def test_las_palabras_de_maquina_no_son_ordenes():
    """Un renglon con palabras de programador NO puede pasar por orden de Julio."""
    malos = []
    for texto in NO_SON_ORDEN:
        if parece_una_orden(texto):
            malos.append(texto)
    if malos:
        _fallo("estos renglones de maquina se tomaron por ordenes de Julio:\n  - "
               + "\n  - ".join(malos))
        return False
    return True


def test_las_frases_de_julio_siguen_entrando():
    """Las frases reales de Julio SI tienen que seguir entrando. Esta es la mitad que importa."""
    perdidas = []
    for texto in SI_SON_ORDEN:
        if not parece_una_orden(texto):
            perdidas.append(texto)
    if perdidas:
        _fallo("se perdieron ordenes REALES de Julio:\n  - " + "\n  - ".join(perdidas))
        return False
    return True


def test_ninguna_frase_de_julio_lleva_palabra_de_maquina():
    """Control: las frases de Julio no deben colarse por llevar dentro una palabra de maquina.

    Si alguna la lleva, el test de arriba pasaria por el motivo equivocado y no estariamos
    probando lo que creemos.
    """
    sospechosas = [
        "monkeypatch", "subprocess", "TypeError", "assert", "tmp_path",
        ".py", "()",
    ]
    malas = []
    for texto in SI_SON_ORDEN:
        bajo = texto.lower()
        for marca in sospechosas:
            if marca.lower() in bajo:
                malas.append((texto, marca))
    if malas:
        _fallo("frases de Julio contaminadas con marcas de maquina (elige otras):\n  - "
               + "\n  - ".join("%r por %r" % (t, m) for t, m in malas))
        return False
    return True


def test_la_vigia_esta_viva():
    """La vigia tiene que poder importar la funcion que vigila."""
    if not callable(parece_una_orden):
        _fallo("parece_una_orden no es llamable: la vigia no vigila nada")
        return False
    return True


def main():
    pruebas = [
        test_la_vigia_esta_viva,
        test_las_palabras_de_maquina_no_son_ordenes,
        test_las_frases_de_julio_siguen_entrando,
        test_ninguna_frase_de_julio_lleva_palabra_de_maquina,
    ]
    fallos = 0
    for prueba in pruebas:
        try:
            ok = prueba()
        except Exception as e:
            _fallo("%s revento: %r" % (prueba.__name__, e))
            ok = False
        if not ok:
            fallos += 1
        sys.stdout.write(("OK   " if ok else "ROJO ") + prueba.__name__ + "\n")
    if fallos:
        sys.stdout.write("\n%d prueba(s) en rojo.\n" % fallos)
        return 2
    sys.stdout.write("\nTodo verde: las palabras de maquina no son ordenes y las de Julio si.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
