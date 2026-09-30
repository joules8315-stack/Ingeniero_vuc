# -*- coding: utf-8 -*-
"""VIGIA — EL MOSTRADOR SALVA LA VUELTA. Nace ROJA a proposito.

Julio lo dijo hoy: "es mejor que el equipo venga en ayuda de la IA, asi como a Claude o
Codex, que piden lo que necesitan y alli esta. Debe ser por programa, que siempre son
rapidos, precisos, economicos y eficientes."

Hoy, en cuerpo/obrero.py, dentro de la vuelta del trabajo, hay un sitio donde la vuelta
SE MUERE antes de llamar a ningun cerebro: cuando se comprueba que al material le falta la
pieza que la tarea nombra, se devuelve un error que empieza por FALTA_MATERIAL y que lleva
dentro una peticion de lectura. Ahi acaba todo: nadie atiende esa peticion y hay que volver
a empezar de cero.

El mostrador que sabe atender esa peticion YA EXISTE y ya esta verde: arnes/mostrador.py.
Y HOY NADIE LO LLAMA desde ahi.

ESTA PRUEBA MIDE EL ARREGLO DE LA RONDA SIGUIENTE:
  a) una funcion NUEVA en cuerpo/obrero.py llamada
         material_con_lo_que_falta(material, faltantes, archivo, raiz)
     que pega al final del material lo que el mostrador haya podido entregar, dentro de un
     bloque que empieza por el renglon LO QUE FALTABA, ATENDIDO POR EL MOSTRADOR.
     Si el mostrador no entrega nada util, devuelve el material TAL CUAL. Nunca revienta.
  b) que en el sitio donde hoy la vuelta se muere devolviendo FALTA_MATERIAL se llame
     PRIMERO a esa funcion.

PROMESA DE SABOTAJE: cuando el arreglo entre, quien revise lo deshace, corre esta prueba y
comprueba que los casos VUELVEN A ROJO. Si con la cura quitada algun caso sigue verde, la
prueba mira a otro nivel que el arreglo y el trabajo se devuelve.

Sin IA, sin red, sin lanzar procesos. Nada se escribe fuera de la carpeta temporal de pytest.
"""
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# ARRANQUE: la raiz del proyecto (un nivel arriba de vigias/) y la carpeta arnes/
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")
OBRERO = os.path.join(RAIZ, "cuerpo", "obrero.py")

for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ---------------------------------------------------------------------------
# EL ARCHIVO DE MENTIRA: se escribe DENTRO de la carpeta temporal que da pytest
# ---------------------------------------------------------------------------
RELLENO = "\n".join("RELLENO_%02d = %d" % (i, i) for i in range(1, 21))

CODIGO_DE_MENTIRA = (
    "# archivo de mentira para la vigia del mostrador\n"
    "\n"
    "def saluda(nombre):\n"
    "    return 'hola ' + str(nombre)\n"
    "\n"
    "\n"
    "def despide(nombre):\n"
    "    return 'adios ' + str(nombre)\n"
    "\n"
    "\n"
    + RELLENO
    + "\n"
)

PRIMER_RENGLON_SALUDA = "def saluda(nombre):"
PRIMER_RENGLON_DESPIDE = "def despide(nombre):"
RENGLON_DEL_BLOQUE = "LO QUE FALTABA, ATENDIDO POR EL MOSTRADOR"


@pytest.fixture()
def archivo_de_mentira(tmp_path):
    """Escribe el archivo de mentira dentro de la carpeta temporal de pytest.

    Devuelve (nombre_del_archivo, carpeta_raiz).
    """
    carpeta = tmp_path / "proyecto_de_mentira"
    carpeta.mkdir()
    ruta = carpeta / "mentira.py"
    ruta.write_text(CODIGO_DE_MENTIRA, encoding="utf-8")
    return "mentira.py", str(carpeta)


def _traer_la_funcion():
    """Importa cuerpo/obrero.py DENTRO del caso y devuelve la funcion nueva.

    Si no se puede importar, o si la funcion todavia no existe, falla por AFIRMACION
    (nunca por reventon): esta prueba nace roja a proposito.
    """
    try:
        from cuerpo import obrero
    except Exception as exc:  # pragma: no cover - hoy no deberia pasar
        pytest.fail(
            "no se pudo importar cuerpo/obrero.py (%s). Esta prueba nace roja a proposito: "
            "mide el arreglo de la ronda siguiente." % exc
        )
    funcion = getattr(obrero, "material_con_lo_que_falta", None)
    assert funcion is not None, (
        "cuerpo/obrero.py todavia NO tiene material_con_lo_que_falta. "
        "Esta prueba nace roja a proposito: mide el arreglo de la ronda siguiente."
    )
    assert callable(funcion), (
        "material_con_lo_que_falta existe pero no se puede llamar. "
        "Esta prueba nace roja a proposito: mide el arreglo de la ronda siguiente."
    )
    return funcion


# ---------------------------------------------------------------------------
# CASO 1 — LA FUNCION NUEVA EXISTE (nace rojo)
# ---------------------------------------------------------------------------
def test_1_la_funcion_nueva_existe():
    funcion = _traer_la_funcion()
    assert callable(funcion), (
        "material_con_lo_que_falta tiene que poder llamarse. "
        "Esta prueba nace roja a proposito."
    )


# ---------------------------------------------------------------------------
# CASO 2 — LO QUE FALTABA APARECE EN EL MATERIAL (nace rojo)
# ---------------------------------------------------------------------------
def test_2_lo_que_faltaba_aparece_en_el_material(archivo_de_mentira):
    funcion = _traer_la_funcion()
    nombre_archivo, raiz = archivo_de_mentira

    material = "MATERIAL DE MENTIRA QUE NO TRAE LA FUNCION saluda\n"
    faltantes = ["falta la funcion saluda en el archivo"]

    devuelto = funcion(material, faltantes, nombre_archivo, raiz)

    assert isinstance(devuelto, str), "la funcion tiene que devolver texto"
    assert len(devuelto) > len(material), (
        "el material devuelto tiene que ser MAS LARGO que el que entro: "
        "lo que faltaba tiene que aparecer pegado al final."
    )
    assert PRIMER_RENGLON_SALUDA in devuelto, (
        "el material devuelto tiene que traer dentro el primer renglon de saluda: %r"
        % PRIMER_RENGLON_SALUDA
    )
    assert RENGLON_DEL_BLOQUE in devuelto, (
        "el material devuelto tiene que traer el renglon que anuncia el bloque del mostrador: %r"
        % RENGLON_DEL_BLOQUE
    )


# ---------------------------------------------------------------------------
# CASO 3 — Y NO APARECE NADA MAS (la mitad importante)
# ---------------------------------------------------------------------------
def test_3_y_no_aparece_nada_mas(archivo_de_mentira):
    funcion = _traer_la_funcion()
    nombre_archivo, raiz = archivo_de_mentira

    material = "MATERIAL DE MENTIRA QUE NO TRAE LA FUNCION saluda\n"
    faltantes = ["falta la funcion saluda en el archivo"]

    devuelto = funcion(material, faltantes, nombre_archivo, raiz)

    assert PRIMER_RENGLON_DESPIDE not in devuelto, (
        "NO puede aparecer la funcion despide: solo viaja la pieza pedida por su nombre. "
        "Esto es lo que impide que el material vuelva a engordar."
    )
    assert "RELLENO_01" not in devuelto, (
        "NO puede aparecer el relleno del archivo: solo viaja la pieza pedida por su nombre."
    )
    assert "RELLENO_20" not in devuelto, (
        "NO puede aparecer el relleno del archivo: solo viaja la pieza pedida por su nombre."
    )


# ---------------------------------------------------------------------------
# CASO 4 — SI NO SE ENCUENTRA, EL MATERIAL NO SE TOCA (nace rojo)
# ---------------------------------------------------------------------------
def test_4_si_no_se_encuentra_el_material_no_se_toca(archivo_de_mentira):
    funcion = _traer_la_funcion()
    nombre_archivo, raiz = archivo_de_mentira

    material = "MATERIAL DE MENTIRA INTACTO\n"
    faltantes = ["falta la funcion que_no_existe_en_el_archivo"]

    devuelto = funcion(material, faltantes, nombre_archivo, raiz)

    assert devuelto == material, (
        "si el mostrador no encuentra nada, el material tiene que volver EXACTAMENTE igual, "
        "letra por letra."
    )


# ---------------------------------------------------------------------------
# CASO 5 — NO REVIENTA (nace rojo porque la funcion no existe; verde en cuanto exista)
# ---------------------------------------------------------------------------
def test_5_no_revienta(archivo_de_mentira):
    funcion = _traer_la_funcion()
    nombre_archivo, raiz = archivo_de_mentira

    material = "MATERIAL DE MENTIRA\n"

    casos = [
        (material, [], nombre_archivo, raiz),
        (material, None, nombre_archivo, raiz),
        (material, ["falta la funcion saluda"], "archivo_que_no_existe.py", raiz),
        (material, ["falta la funcion saluda"], nombre_archivo, os.path.join(raiz, "carpeta_que_no_existe")),
    ]

    for material_entrada, faltantes, archivo, carpeta in casos:
        try:
            devuelto = funcion(material_entrada, faltantes, archivo, carpeta)
        except Exception as exc:
            pytest.fail(
                "material_con_lo_que_falta NO puede reventar nunca (caso %r): %s"
                % ((faltantes, archivo, carpeta), exc)
            )
        assert isinstance(devuelto, str), (
            "en los cuatro casos tiene que devolver un texto, no %r" % type(devuelto)
        )
        assert devuelto == material_entrada, (
            "en los cuatro casos tiene que devolver el material tal cual, sin tocarlo."
        )


# ---------------------------------------------------------------------------
# CASO 6 — EL SITIO DONDE LA VUELTA SE MORIA YA LLAMA AL MOSTRADOR (nace rojo)
# ---------------------------------------------------------------------------
def test_6_el_sitio_donde_la_vuelta_se_moria_ya_llama_al_mostrador():
    assert os.path.isfile(OBRERO), (
        "no se encuentra cuerpo/obrero.py en %s" % OBRERO
    )
    with open(OBRERO, "r", encoding="utf-8", errors="replace") as f:
        texto = f.read()

    renglones = texto.splitlines()

    indice_error = None
    for i, renglon in enumerate(renglones):
        if "FALTA_MATERIAL" in renglon and "_error" in renglon:
            indice_error = i
            break

    assert indice_error is not None, (
        "no se encontro el renglon que devuelve el error que empieza por FALTA_MATERIAL "
        "en cuerpo/obrero.py. Si ese renglon desaparecio, esta prueba mira a otro nivel "
        "que el arreglo y hay que devolver el trabajo."
    )

    # Se busca la llamada MAS ARRIBA de ese renglon, dentro de la misma vuelta del trabajo.
    # La vuelta del trabajo empieza en el 'for _vuelta in range(' mas cercano por encima.
    inicio_vuelta = 0
    for i in range(indice_error - 1, -1, -1):
        if "for _vuelta in range(" in renglones[i]:
            inicio_vuelta = i
            break

    trozo = "\n".join(renglones[inicio_vuelta:indice_error])

    assert "material_con_lo_que_falta" in trozo, (
        "HOY la vuelta se muere devolviendo FALTA_MATERIAL sin que nadie atienda la peticion: "
        "no aparece ninguna llamada a material_con_lo_que_falta mas arriba de ese renglon, "
        "dentro de la misma vuelta del trabajo. Julio pidio que el equipo venga en ayuda de la "
        "IA, que pida lo que necesita y alli este. Esta prueba nace roja a proposito: mide el "
        "arreglo de la ronda siguiente."
    )
