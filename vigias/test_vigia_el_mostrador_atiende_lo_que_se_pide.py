import os
import sys

import pytest


# La marca de "no aparece" y la de "demasiado grande" NUNCA se escriben enteras y
# seguidas en este archivo: se arman juntando trozos, como manda la casa.
MARCA = "NO" + "_" + "ENCONTRADO"
MARCA_GRANDE = "DEMASIADO" + "_" + "GRANDE"


# ---------------------------------------------------------------------------
# Arranque: dejar a la vista la raiz del proyecto y la carpeta arnes.
# ---------------------------------------------------------------------------
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
_ARNES = os.path.join(_RAIZ, "arnes")
for _p in (_RAIZ, _ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ---------------------------------------------------------------------------
# Ayudas: archivos de mentira dentro de la carpeta temporal de pytest.
# ---------------------------------------------------------------------------
def _escribir_archivo_pequeno(carpeta):
    """Archivo de mentira con dos funciones cortas y relleno entre ellas."""
    renglones = [
        "# archivo de mentira para la prueba del mostrador",
        "",
        "def saluda(nombre):",
        "    # primer renglon de saluda",
        "    return 'hola ' + nombre",
        "",
        "",
        "RELLENO_UNO = 1",
        "RELLENO_DOS = 2",
        "RELLENO_TRES = 3",
        "",
        "",
        "def despide(nombre):",
        "    # primer renglon de despide",
        "    return 'adios ' + nombre",
        "",
    ]
    ruta = os.path.join(carpeta, "pequeno.py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(renglones) + "\n")
    return ruta


def _escribir_archivo_grande(carpeta):
    """Archivo de mentira con mas de 300 renglones y dos funciones conocidas."""
    renglones = [
        "# archivo de mentira grande",
        "",
        "def alfa(x):",
        "    return x + 1",
        "",
        "def beta(x):",
        "    return x + 2",
        "",
    ]
    for i in range(320):
        renglones.append("RELLENO_%d = %d" % (i, i))
    ruta = os.path.join(carpeta, "grande.py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(renglones) + "\n")
    return ruta


def _importar_mostrador():
    """Importa la pieza dentro del caso. Si no existe, falla por afirmacion."""
    try:
        import arnes.mostrador as mostrador
    except Exception as exc:
        pytest.fail(
            "la pieza arnes/mostrador.py todavia no existe: "
            "esta prueba nace roja a proposito (" + repr(exc) + ")"
        )
    return mostrador


# ---------------------------------------------------------------------------
# Caso 1: la pieza existe y tiene las tres cosas.
# ---------------------------------------------------------------------------
def test_caso_1_la_pieza_existe():
    mostrador = _importar_mostrador()
    assert hasattr(mostrador, "lo_que_pide")
    assert hasattr(mostrador, "atender")
    assert hasattr(mostrador, "apuntar_atencion")
    assert callable(mostrador.lo_que_pide)
    assert callable(mostrador.atender)
    assert callable(mostrador.apuntar_atencion)


# ---------------------------------------------------------------------------
# Caso 2: se entiende la peticion.
# ---------------------------------------------------------------------------
def test_caso_2_se_entiende_la_peticion():
    mostrador = _importar_mostrador()
    respuesta = (
        "Aqui va mi respuesta.\n"
        "NECESITO_LEER: cerebro/piezas.py: funcion_completa\n"
        "Sigo con la prosa de arriba.\n"
        "Y con mas prosa por aqui.\n"
        "Y un ultimo renglon de prosa.\n"
    )
    peticiones = mostrador.lo_que_pide(respuesta)
    assert isinstance(peticiones, list)
    assert len(peticiones) == 1
    p = peticiones[0]
    assert p["archivo"] == "cerebro/piezas.py"
    assert p["nombre"] == "funcion_completa"


# ---------------------------------------------------------------------------
# Caso 3: dos peticiones y ninguna repetida.
# ---------------------------------------------------------------------------
def test_caso_3_dos_peticiones_y_ninguna_repetida():
    mostrador = _importar_mostrador()
    respuesta = (
        "NECESITO_LEER: uno.py: alfa\n"
        "NECESITO_LEER: dos.py: beta\n"
        "NECESITO_LEER: uno.py: alfa\n"
    )
    peticiones = mostrador.lo_que_pide(respuesta)
    assert isinstance(peticiones, list)
    assert len(peticiones) == 2
    assert peticiones[0]["archivo"] == "uno.py"
    assert peticiones[0]["nombre"] == "alfa"
    assert peticiones[1]["archivo"] == "dos.py"
    assert peticiones[1]["nombre"] == "beta"


# ---------------------------------------------------------------------------
# Caso 4: se entrega la funcion pedida y entera.
# ---------------------------------------------------------------------------
def test_caso_4_se_entrega_la_funcion_pedida_y_entera(tmp_path):
    mostrador = _importar_mostrador()
    _escribir_archivo_pequeno(str(tmp_path))
    peticiones = [{"archivo": "pequeno.py", "nombre": "saluda"}]
    entregado = mostrador.atender(peticiones, str(tmp_path))
    assert isinstance(entregado, str)
    assert "def saluda(nombre):" in entregado
    assert "return 'hola ' + nombre" in entregado


# ---------------------------------------------------------------------------
# Caso 5: y no se entrega nada mas.
# ---------------------------------------------------------------------------
def test_caso_5_y_no_se_entrega_nada_mas(tmp_path):
    mostrador = _importar_mostrador()
    _escribir_archivo_pequeno(str(tmp_path))
    peticiones = [{"archivo": "pequeno.py", "nombre": "saluda"}]
    entregado = mostrador.atender(peticiones, str(tmp_path))
    assert "def despide(nombre):" not in entregado
    assert "return 'adios ' + nombre" not in entregado
    assert "RELLENO_UNO" not in entregado
    assert "RELLENO_DOS" not in entregado
    assert "RELLENO_TRES" not in entregado


# ---------------------------------------------------------------------------
# Caso 6: lo que no esta se dice, no se inventa.
# ---------------------------------------------------------------------------
def test_caso_6_lo_que_no_esta_se_dice_no_se_inventa(tmp_path):
    mostrador = _importar_mostrador()
    _escribir_archivo_pequeno(str(tmp_path))

    peticiones = [{"archivo": "pequeno.py", "nombre": "no_existe_esta_funcion"}]
    entregado = mostrador.atender(peticiones, str(tmp_path))
    assert MARCA in entregado
    assert "def saluda(nombre):" not in entregado
    assert "def despide(nombre):" not in entregado
    assert "RELLENO_UNO" not in entregado

    peticiones2 = [{"archivo": "no_existe_este_archivo.py", "nombre": "saluda"}]
    entregado2 = mostrador.atender(peticiones2, str(tmp_path))
    assert MARCA in entregado2
    assert "def saluda(nombre):" not in entregado2


# ---------------------------------------------------------------------------
# Caso 7: un archivo demasiado grande no se manda entero.
# ---------------------------------------------------------------------------
def test_caso_7_un_archivo_demasiado_grande_no_se_manda_entero(tmp_path):
    mostrador = _importar_mostrador()
    _escribir_archivo_grande(str(tmp_path))
    peticiones = [{"archivo": "grande.py", "nombre": ""}]
    entregado = mostrador.atender(peticiones, str(tmp_path))
    assert MARCA_GRANDE in entregado
    assert "alfa" in entregado
    assert "beta" in entregado
    assert "RELLENO_0 = 0" not in entregado
    assert "RELLENO_100 = 100" not in entregado
    assert "def alfa(x):" not in entregado


# ---------------------------------------------------------------------------
# Caso 8: no revienta con basura, y no se sale de la carpeta.
# ---------------------------------------------------------------------------
def test_caso_8_no_revienta_con_basura_y_no_se_sale_de_la_carpeta(tmp_path):
    mostrador = _importar_mostrador()

    assert mostrador.lo_que_pide("") == []
    assert mostrador.lo_que_pide(None) == []
    assert mostrador.lo_que_pide(123) == []
    assert mostrador.lo_que_pide(["NECESITO_LEER: x.py: y"]) == []

    assert mostrador.atender([], str(tmp_path)) == ""

    # Peticion que sube por carpetas con dos puntos y barra: fuera de la carpeta temporal.
    fuera = ".." + os.sep + ".." + os.sep + "etc" + os.sep + "passwd"
    peticiones = [{"archivo": fuera, "nombre": ""}]
    entregado = mostrador.atender(peticiones, str(tmp_path))
    assert MARCA in entregado
    assert "root:" not in entregado
    assert "/bin/" not in entregado
