import ast
import os
import sys

import pytest


AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


# ---------------------------------------------------------------------------
# LA LEY QUE VIGILA ESTA PRUEBA
#
# El revisor (el auditor de IA) devuelve en su JSON la marca 'invento_algo' y la
# lista 'que_invento' (cuerpo/obrero.py, lineas 222-223 del prompt del auditor).
# Hoy, cuando esa marca viene encendida, el trabajo se descarta entero sin que
# ningun PROGRAMA compruebe si los nombres de 'que_invento' estan de verdad
# declarados dentro del codigo que la propuesta trae.
#
# CREAR NO ES INVENTAR: si la reparacion crea una constante o una funcion con
# ese nombre, ese nombre NO es un invento, es la reparacion haciendo su trabajo.
# Un programa debe quitar de 'que_invento' los nombres que aparezcan declarados
# en el codigo de la propuesta ANTES de descartar nada.
#
# Esta prueba nace ROJA: hoy no existe ese programa. Cuando la reparacion este
# hecha (exista la funcion que comprueba y limpie la lista), la prueba pasa.
# ---------------------------------------------------------------------------


# Nombre exacto que la reparacion debe crear. Se escribe aqui para que la prueba
# lo busque en el codigo de la propuesta. Si la reparacion lo llama distinto,
# esta prueba lo dira con un assert, no con un error de sintaxis.
NOMBRE_DE_LA_FUNCION_QUE_COMPRUEBA = "comprobar_invento_contra_el_codigo"


# ---------------------------------------------------------------------------
# AYUDANTES: leer el codigo de la propuesta y ver que declara
# ---------------------------------------------------------------------------


def _nombres_declarados_en_codigo(codigo):
    """Devuelve el conjunto de nombres que un texto de codigo Python DECLARA.

    Declarar es: definir una funcion (def), una clase (class), o asignar un
    nombre a nivel de modulo o dentro de una funcion (constante o variable).
    Se usa ast para no confundir 'usar' con 'declarar'.
    """
    declarados = set()
    try:
        arbol = ast.parse(codigo)
    except SyntaxError:
        return declarados
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            declarados.add(nodo.name)
        elif isinstance(nodo, ast.Assign):
            for objetivo in nodo.targets:
                for nombre in ast.walk(objetivo):
                    if isinstance(nombre, ast.Name):
                        declarados.add(nombre.id)
        elif isinstance(nodo, ast.AnnAssign):
            if isinstance(nodo.target, ast.Name):
                declarados.add(nodo.target.id)
    return declarados


def _codigo_de_la_propuesta(propuesta):
    """Junta todo el codigo que la propuesta trae, venga como venga."""
    trozos = []
    if not isinstance(propuesta, dict):
        return ""
    for clave in ("texto_nuevo", "codigo"):
        valor = propuesta.get(clave)
        if isinstance(valor, str) and valor.strip():
            trozos.append(valor)
    cambios = propuesta.get("cambios")
    if isinstance(cambios, list):
        for cambio in cambios:
            if isinstance(cambio, dict):
                for clave in ("texto_nuevo", "codigo"):
                    valor = cambio.get(clave)
                    if isinstance(valor, str) and valor.strip():
                        trozos.append(valor)
    return "\n\n".join(trozos)


# ---------------------------------------------------------------------------
# LA PRUEBA
# ---------------------------------------------------------------------------


def test_el_programa_quita_de_que_invento_lo_que_la_propuesta_declara():
    """Un PROGRAMA, no el revisor, decide si un nombre de que_invento es invento.

    Se le da una propuesta que CREA una constante y una funcion nuevas, y un
    revisor que las marca como invento. El programa debe quitarlas de la lista
    porque aparecen DECLARADAS en el codigo de la propuesta.
    """
    from cuerpo import obrero

    comprobar = getattr(obrero, NOMBRE_DE_LA_FUNCION_QUE_COMPRUEBA, None)
    assert comprobar is not None, (
        "falta el programa que comprueba la marca invento_algo contra el codigo "
        "de la propuesta: cuerpo/obrero.py no tiene "
        + NOMBRE_DE_LA_FUNCION_QUE_COMPRUEBA
    )

    propuesta = {
        "archivo": "cuerpo/ejemplo.py",
        "texto_nuevo": (
            "MARGEN_POR_DEFECTO = 0.15\n"
            "\n"
            "def calcular_margen(base):\n"
            "    return base * MARGEN_POR_DEFECTO\n"
        ),
    }
    auditoria = {
        "veredicto": "RECHAZADO",
        "invento_algo": True,
        "que_invento": ["MARGEN_POR_DEFECTO", "calcular_margen", "archivo_que_no_existe.py"],
    }

    limpia = comprobar(auditoria, propuesta)

    assert isinstance(limpia, dict), "el programa debe devolver la auditoria ya limpia"
    quedan = list(limpia.get("que_invento") or [])
    assert "MARGEN_POR_DEFECTO" not in quedan, (
        "la constante SI aparece declarada en el codigo de la propuesta: no es invento"
    )
    assert "calcular_margen" not in quedan, (
        "la funcion SI aparece declarada en el codigo de la propuesta: no es invento"
    )
    assert "archivo_que_no_existe.py" in quedan, (
        "lo que de verdad no aparece en el codigo de la propuesta SI sigue siendo invento"
    )


def test_sin_nombres_que_limpiar_la_marca_se_apaga():
    """Si no queda ningun nombre inventado, la marca invento_algo se apaga."""
    from cuerpo import obrero

    comprobar = getattr(obrero, NOMBRE_DE_LA_FUNCION_QUE_COMPRUEBA, None)
    assert comprobar is not None, (
        "falta el programa que comprueba la marca invento_algo contra el codigo "
        "de la propuesta: cuerpo/obrero.py no tiene "
        + NOMBRE_DE_LA_FUNCION_QUE_COMPRUEBA
    )

    propuesta = {
        "archivo": "cuerpo/ejemplo.py",
        "texto_nuevo": "def calcular_margen(base):\n    return base\n",
    }
    auditoria = {
        "veredicto": "RECHAZADO",
        "invento_algo": True,
        "que_invento": ["calcular_margen"],
    }

    limpia = comprobar(auditoria, propuesta)

    assert not limpia.get("que_invento"), "la lista debe quedar vacia"
    assert limpia.get("invento_algo") is False, (
        "si no queda ningun nombre inventado, la marca invento_algo debe apagarse"
    )


def test_el_ayudante_reconoce_lo_declarado_y_no_lo_usado():
    """El ayudante distingue declarar de usar: 'usar' no es declarar."""
    codigo = (
        "import os\n"
        "CONSTANTE_NUEVA = 1\n"
        "def funcion_nueva():\n"
        "    return CONSTANTE_NUEVA\n"
        "class ClaseNueva:\n"
        "    pass\n"
    )
    declarados = _nombres_declarados_en_codigo(codigo)
    assert "CONSTANTE_NUEVA" in declarados
    assert "funcion_nueva" in declarados
    assert "ClaseNueva" in declarados
    assert "os" not in declarados, "importar no es declarar un nombre nuevo"


def test_el_ayudante_junta_el_codigo_de_los_cambios():
    """El codigo de la propuesta puede venir en 'cambios': tambien cuenta."""
    propuesta = {
        "cambios": [
            {"texto_nuevo": "NOMBRE_EN_UN_CAMBIO = 2\n"},
            {"codigo": "def otra_funcion_nueva():\n    return 2\n"},
        ]
    }
    codigo = _codigo_de_la_propuesta(propuesta)
    declarados = _nombres_declarados_en_codigo(codigo)
    assert "NOMBRE_EN_UN_CAMBIO" in declarados
    assert "otra_funcion_nueva" in declarados
