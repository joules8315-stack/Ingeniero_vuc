import os
import sys

import pytest


# La carpeta que esta un nivel arriba de 'vigias' es la raiz del proyecto.
# Se calcula a partir de la ruta de ESTE archivo de prueba, sin depender del cwd.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from cerebro import piezas  # noqa: E402


# ---------------------------------------------------------------------------
# Caso 1: funcion de JavaScript SANGRADA y ENTERA EN UN SOLO RENGLON.
# Nace ROJO: hoy la pieza exige margen izquierdo y solo reconoce 'def '/'class '.
# ---------------------------------------------------------------------------
def test_caso1_funcion_js_sangrada_en_un_solo_renglon(tmp_path):
    archivo = tmp_path / "app_web.html"
    archivo.write_text(
        "<html>\n"
        "<script>\n"
        "    async function processPhoto(file,num){const d=new Date();return d}\n"
        "</script>\n"
        "</html>\n",
        encoding="utf-8",
    )

    resultado = piezas.funcion_completa(str(archivo), "processPhoto")

    assert resultado is not None, (
        "HOY la pieza contesta que NO aparece, aunque processPhoto SI esta en el "
        "archivo: es una funcion de JavaScript sangrada con cuatro espacios y entera "
        "en un solo renglon. Esta es la causa medida de las cuatro vueltas muertas "
        "de Foto Informe (processPhoto, captureDesktopPhoto, handlePhotos)."
    )
    assert "processPhoto" in resultado["texto"], (
        "El tramo devuelto tiene que contener el nombre pedido; hoy devuelve un tramo "
        "que no lo contiene."
    )


# ---------------------------------------------------------------------------
# Caso 2: funcion de JavaScript repartida en VARIOS renglones, tambien sangrada.
# Nace ROJO por la misma causa: sangria + lenguaje no reconocido.
# ---------------------------------------------------------------------------
def test_caso2_funcion_js_en_varios_renglones(tmp_path):
    archivo = tmp_path / "app_web.html"
    archivo.write_text(
        "<html>\n"
        "<script>\n"
        "    function captureDesktopPhoto() {\n"
        "        const canvas = document.createElement('canvas');\n"
        "        return canvas.toDataURL();\n"
        "    }\n"
        "</script>\n"
        "</html>\n",
        encoding="utf-8",
    )

    resultado = piezas.funcion_completa(str(archivo), "captureDesktopPhoto")

    assert resultado is not None, (
        "HOY la pieza contesta que NO aparece, aunque captureDesktopPhoto SI esta: "
        "es una funcion de JavaScript sangrada con cuatro espacios. Misma causa que "
        "el caso 1."
    )
    assert resultado["desde"] == 3, (
        "El tramo tiene que EMPEZAR en el renglon donde se declara la funcion "
        "(renglon 3 del archivo de mentira)."
    )
    assert resultado["hasta"] == 6, (
        "El tramo tiene que TERMINAR en el renglon de la llave de cerrar "
        "(renglon 6 del archivo de mentira)."
    )
    assert "captureDesktopPhoto" in resultado["texto"], (
        "El texto devuelto tiene que contener la declaracion."
    )
    assert "canvas.toDataURL" in resultado["texto"], (
        "El texto devuelto tiene que contener el ultimo renglon del cuerpo."
    )


# ---------------------------------------------------------------------------
# Caso 3: funcion de JavaScript declarada como asignacion de funcion de flecha,
# tambien sangrada. Nace ROJO por la misma causa.
# ---------------------------------------------------------------------------
def test_caso3_funcion_js_de_flecha_sangrada(tmp_path):
    archivo = tmp_path / "app_web.html"
    archivo.write_text(
        "<html>\n"
        "<script>\n"
        "    const handlePhotos = (files) => {\n"
        "        return files.map(f => f.name);\n"
        "    };\n"
        "</script>\n"
        "</html>\n",
        encoding="utf-8",
    )

    resultado = piezas.funcion_completa(str(archivo), "handlePhotos")

    assert resultado is not None, (
        "HOY la pieza contesta que NO aparece, aunque handlePhotos SI esta: es una "
        "funcion de flecha asignada a un nombre, sangrada con cuatro espacios. "
        "Misma causa que los casos 1 y 2."
    )
    assert "handlePhotos" in resultado["texto"], (
        "El tramo devuelto tiene que contener el nombre pedido."
    )


# ---------------------------------------------------------------------------
# Caso 4: LO QUE NO PUEDE CAMBIAR. Funcion normal de Python, pegada al margen,
# con cuerpo sangrado. Hoy ya esta VERDE y tiene que seguir verde.
# ---------------------------------------------------------------------------
def test_caso4_python_pegado_al_margen_sigue_funcionando(tmp_path):
    archivo = tmp_path / "modulo.py"
    archivo.write_text(
        "import os\n"
        "\n"
        "def saludar(nombre):\n"
        "    saludo = 'hola ' + nombre\n"
        "    return saludo\n"
        "\n"
        "def despedir(nombre):\n"
        "    return 'adios ' + nombre\n",
        encoding="utf-8",
    )

    resultado = piezas.funcion_completa(str(archivo), "saludar")

    assert resultado is not None, (
        "Una funcion normal de Python pegada al margen TIENE que seguir "
        "encontrandose: este caso ya estaba verde hoy."
    )
    assert resultado["desde"] == 3, "Tiene que empezar en el renglon del def."
    assert resultado["hasta"] == 5, (
        "Tiene que terminar en el ultimo renglon sangrado del cuerpo."
    )
    assert "def saludar" in resultado["texto"]
    assert "return saludo" in resultado["texto"]
    assert "def despedir" not in resultado["texto"], (
        "No puede tragarse la funcion siguiente."
    )


# ---------------------------------------------------------------------------
# Caso 5: LO QUE NO PUEDE CAMBIAR. Nombre que no existe: devuelve nada, sin
# reventar. Hoy ya esta VERDE y tiene que seguir verde.
# ---------------------------------------------------------------------------
def test_caso5_nombre_inexistente_devuelve_nada(tmp_path):
    archivo = tmp_path / "modulo.py"
    archivo.write_text(
        "def existente():\n"
        "    return 1\n",
        encoding="utf-8",
    )

    resultado = piezas.funcion_completa(str(archivo), "no_existe_esta_funcion")

    assert resultado is None, (
        "Si el nombre no aparece, la pieza tiene que contestar que no aparece, "
        "sin reventar."
    )
