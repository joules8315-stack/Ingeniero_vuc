# -*- coding: utf-8 -*-
"""vigias/test_vigia_una_pieza_nueva_nace_enganchada.py — VIGIA QUE NACE ROJA A PROPOSITO.

Mide el candado que aun NO existe: arnes/candado_nace_enganchada.py, y su enganche
dentro de arnes/candado_cierre.py. En esta ronda se entrega SOLO esta prueba; el
arreglo y su enganche entran en la ronda SIGUIENTE, en la MISMA ronda, porque asi
lo ordeno Julio: "Lanza todo lo que falte y que todo nazca enganchado y conectado"
y "que estas instrucciones no dependan de tu memoria".

PROMESA DE SABOTAJE: cuando el arreglo entre, quien revise lo deshace, corre esta
prueba y comprueba que los casos VUELVEN A ROJO. Si con la cura quitada algun caso
sigue verde, esta prueba mira a otro nivel que el arreglo y el trabajo se devuelve.

NO TOCA NADA: no escribe en la memoria del proyecto. Todo lo que escribe va a la
carpeta temporal que da pytest. No importa arnes/candado_cierre.py (hace cosas al
correrlo): lo lee como texto. Sin IA, sin red, sin lanzar procesos.
"""
import os
import sys
import importlib

import pytest


# ---------------------------------------------------------------------------
# ARRANQUE: meter en la ruta de busqueda la carpeta que esta un nivel arriba de
# la carpeta vigias (la raiz de la casa) y tambien la carpeta arnes, usando
# os.path a partir de la ruta de este mismo archivo de prueba.
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")

for _ruta in (RAIZ, ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# ---------------------------------------------------------------------------
# AYUDAS DE MONTAJE
# ---------------------------------------------------------------------------
RUTA_CANDADO = os.path.join(ARNES, "candado_nace_enganchada.py")
RUTA_CIERRE = os.path.join(ARNES, "candado_cierre.py")


def _importar_candado():
    """Importa arnes/candado_nace_enganchada.py DENTRO del caso, nunca arriba.

    Si va arriba y la pieza no existe, el archivo entero revienta al recogerlo y
    deja ciega a toda la bateria. Aqui se intenta importar y, si no se puede, se
    falla con una afirmacion que dice que la pieza todavia no existe y que esta
    prueba nace roja a proposito. Rojo por afirmacion, nunca por reventon.
    """
    try:
        if ARNES not in sys.path:
            sys.path.insert(0, ARNES)
        return importlib.import_module("candado_nace_enganchada")
    except Exception as exc:
        pytest.fail(
            "arnes/candado_nace_enganchada.py todavia no existe o no se puede "
            "importar (%s). Esta prueba nace roja a proposito: el arreglo entra "
            "en la ronda siguiente, junto con su enganche." % exc
        )


def _escribir(ruta, texto):
    """Escribe un archivo de mentira dentro de la carpeta temporal de pytest."""
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta)
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(texto)


def _casa_de_mentira(tmp_path):
    """Crea una carpeta temporal con arnes y vigias dentro, para que se parezca
    a la casa. Devuelve la raiz de esa casa de mentira."""
    raiz = str(tmp_path)
    for nombre in ("arnes", "vigias"):
        carpeta = os.path.join(raiz, nombre)
        if not os.path.isdir(carpeta):
            os.makedirs(carpeta)
    return raiz


# ---------------------------------------------------------------------------
# CASO 1 — LA PIEZA EXISTE, y nace rojo.
# ---------------------------------------------------------------------------
def test_caso_1_la_pieza_existe_y_tiene_las_tres_cosas():
    candado = _importar_candado()
    assert hasattr(candado, "huerfanas"), (
        "arnes/candado_nace_enganchada.py debe tener huerfanas(raiz)."
    )
    assert hasattr(candado, "se_puede_cerrar"), (
        "arnes/candado_nace_enganchada.py debe tener se_puede_cerrar(raiz)."
    )
    assert hasattr(candado, "main"), (
        "arnes/candado_nace_enganchada.py debe tener main()."
    )
    assert callable(candado.huerfanas), "huerfanas debe poder llamarse."
    assert callable(candado.se_puede_cerrar), "se_puede_cerrar debe poder llamarse."
    assert callable(candado.main), "main debe poder llamarse."


# ---------------------------------------------------------------------------
# CASO 2 — UNA PIEZA QUE NADIE LLAMA SE CAZA, y nace rojo.
# ---------------------------------------------------------------------------
def test_caso_2_una_pieza_que_nadie_llama_se_caza(tmp_path):
    candado = _importar_candado()
    raiz = _casa_de_mentira(tmp_path)
    # Dos piezas que se llaman entre ellas: la primera llama a la segunda.
    _escribir(
        os.path.join(raiz, "arnes", "pieza_que_llama.py"),
        "# -*- coding: utf-8 -*-\n"
        "import pieza_llamada\n\n"
        "def correr():\n"
        "    return pieza_llamada.correr()\n",
    )
    _escribir(
        os.path.join(raiz, "arnes", "pieza_llamada.py"),
        "# -*- coding: utf-8 -*-\n\n"
        "def correr():\n"
        "    return 1\n",
    )
    # Tercera pieza a la que NADIE llama: esta es la huerfana.
    _escribir(
        os.path.join(raiz, "arnes", "pieza_huerfana.py"),
        "# -*- coding: utf-8 -*-\n\n"
        "def correr():\n"
        "    return 2\n",
    )

    # OJO AL ORDEN: primero la carpeta, como esta escrito arriba.
    lista = candado.huerfanas(raiz)
    nombres = [os.path.basename(str(x)) for x in lista]
    assert "pieza_huerfana.py" in nombres, (
        "La pieza a la que nadie llama debe salir en la lista de huerfanas. "
        "Lista devuelta: %r" % (lista,)
    )
    assert "pieza_que_llama.py" not in nombres, (
        "La pieza que llama a otra NO es huerfana. Lista devuelta: %r" % (lista,)
    )
    assert "pieza_llamada.py" not in nombres, (
        "La pieza llamada por otra NO es huerfana. Lista devuelta: %r" % (lista,)
    )


# ---------------------------------------------------------------------------
# CASO 3 — NO SE PUEDE CERRAR CON UNA HUERFANA, Y EL MOTIVO LA NOMBRA, y nace rojo.
# ---------------------------------------------------------------------------
def test_caso_3_no_se_puede_cerrar_y_el_motivo_nombra_la_huerfana(tmp_path):
    candado = _importar_candado()
    raiz = _casa_de_mentira(tmp_path)
    _escribir(
        os.path.join(raiz, "arnes", "pieza_que_llama.py"),
        "# -*- coding: utf-8 -*-\n"
        "import pieza_llamada\n\n"
        "def correr():\n"
        "    return pieza_llamada.correr()\n",
    )
    _escribir(
        os.path.join(raiz, "arnes", "pieza_llamada.py"),
        "# -*- coding: utf-8 -*-\n\n"
        "def correr():\n"
        "    return 1\n",
    )
    _escribir(
        os.path.join(raiz, "arnes", "pieza_huerfana.py"),
        "# -*- coding: utf-8 -*-\n\n"
        "def correr():\n"
        "    return 2\n",
    )

    # OJO AL ORDEN: primero la carpeta.
    resultado = candado.se_puede_cerrar(raiz)
    assert isinstance(resultado, tuple) and len(resultado) == 2, (
        "se_puede_cerrar debe devolver DOS cosas: (se_puede, motivo). "
        "Devuelto: %r" % (resultado,)
    )
    se_puede, motivo = resultado
    assert se_puede is False, (
        "Con una pieza huerfana NO se puede cerrar. Devuelto: %r" % (resultado,)
    )
    assert "pieza_huerfana" in str(motivo), (
        "El motivo debe NOMBRAR a la pieza huerfana. Motivo: %r" % (motivo,)
    )
    assert "enganchar" in str(motivo).lower(), (
        "El motivo debe decir las dos maneras de arreglarlo, empezando por "
        "enganchar. Motivo: %r" % (motivo,)
    )


# ---------------------------------------------------------------------------
# CASO 4 — UNA PIEZA QUE ES PUNTO DE ENTRADA NO CUENTA, y nace rojo.
# Este es el caso que impide que nadie pueda cerrar nunca.
# ---------------------------------------------------------------------------
def test_caso_4_punto_de_entrada_no_cuenta_como_huerfana(tmp_path):
    candado = _importar_candado()
    raiz = _casa_de_mentira(tmp_path)
    # Pieza a la que nadie llama, pero que trae dentro el trozo de siempre para
    # poder correrla a mano: es punto de entrada y NO cuenta como huerfana.
    _escribir(
        os.path.join(raiz, "arnes", "pieza_de_entrada.py"),
        "# -*- coding: utf-8 -*-\n\n"
        "def correr():\n"
        "    return 3\n\n"
        "if __name__ == '__main__':\n"
        "    correr()\n",
    )
    # Pieza dentro de la carpeta de pruebas: a esas nadie las llama por su
    # nombre a proposito, asi que tampoco cuentan como huerfanas.
    _escribir(
        os.path.join(raiz, "vigias", "test_pieza_de_prueba.py"),
        "# -*- coding: utf-8 -*-\n\n"
        "def test_algo():\n"
        "    assert True\n",
    )

    # OJO AL ORDEN: primero la carpeta.
    lista = candado.huerfanas(raiz)
    nombres = [os.path.basename(str(x)) for x in lista]
    assert "pieza_de_entrada.py" not in nombres, (
        "Una pieza con el trozo de siempre para correrla a mano es punto de "
        "entrada y NO cuenta como huerfana. Lista devuelta: %r" % (lista,)
    )
    assert "test_pieza_de_prueba.py" not in nombres, (
        "Una pieza dentro de la carpeta de pruebas es punto de entrada y NO "
        "cuenta como huerfana. Lista devuelta: %r" % (lista,)
    )


# ---------------------------------------------------------------------------
# CASO 5 — SIN HUERFANAS SE CIERRA, y nace rojo.
# ---------------------------------------------------------------------------
def test_caso_5_sin_huerfanas_se_cierra(tmp_path):
    candado = _importar_candado()
    raiz = _casa_de_mentira(tmp_path)
    # Todas las piezas se llaman entre ellas: no hay huerfanas.
    _escribir(
        os.path.join(raiz, "arnes", "pieza_uno.py"),
        "# -*- coding: utf-8 -*-\n"
        "import pieza_dos\n\n"
        "def correr():\n"
        "    return pieza_dos.correr()\n",
    )
    _escribir(
        os.path.join(raiz, "arnes", "pieza_dos.py"),
        "# -*- coding: utf-8 -*-\n"
        "import pieza_uno\n\n"
        "def correr():\n"
        "    return pieza_uno.correr()\n",
    )

    # OJO AL ORDEN: primero la carpeta.
    resultado = candado.se_puede_cerrar(raiz)
    assert isinstance(resultado, tuple) and len(resultado) == 2, (
        "se_puede_cerrar debe devolver DOS cosas: (se_puede, motivo). "
        "Devuelto: %r" % (resultado,)
    )
    se_puede, motivo = resultado
    assert se_puede is True, (
        "Sin piezas huerfanas SI se puede cerrar. Devuelto: %r" % (resultado,)
    )


# ---------------------------------------------------------------------------
# CASO 6 — EL CIERRE LE PREGUNTA, Y SI REVIENTA DEJA CERRAR, y nace rojo.
# Se LEE arnes/candado_cierre.py como texto, sin importarlo ni ejecutarlo.
# ---------------------------------------------------------------------------
def test_caso_6_el_cierre_le_pregunta_y_si_revienta_deja_cerrar():
    assert os.path.isfile(RUTA_CIERRE), (
        "No se encuentra arnes/candado_cierre.py para leerlo como texto."
    )
    with open(RUTA_CIERRE, "r", encoding="utf-8") as fh:
        texto = fh.read()

    assert "candado_nace_enganchada" in texto, (
        "Julio ordeno que todo nazca enganchado y que esto no dependa de la "
        "memoria de la IA: arnes/candado_cierre.py debe nombrar a "
        "candado_nace_enganchada dentro de su main, junto a las faltas que ya "
        "junta. Hoy no lo nombra en ninguna parte, y por eso esta prueba nace "
        "roja a proposito."
    )

    # Cerca de donde lo nombra debe haber un intento protegido: si revienta, NO
    # se agrega ninguna falta y se deja cerrar.
    posicion = texto.find("candado_nace_enganchada")
    ventana = texto[max(0, posicion - 400): posicion + 400]
    assert "try:" in ventana, (
        "La pregunta al candado debe ir dentro de un intento protegido: si "
        "revienta, NO se agrega ninguna falta y se deja cerrar. Julio ordeno "
        "que todo nazca enganchado y que esto no dependa de la memoria de la IA."
    )
    assert "except" in ventana, (
        "El intento protegido debe tener su except cerca: si revienta, NO se "
        "agrega ninguna falta y se deja cerrar. Julio ordeno que todo nazca "
        "enganchado y que esto no dependa de la memoria de la IA."
    )
