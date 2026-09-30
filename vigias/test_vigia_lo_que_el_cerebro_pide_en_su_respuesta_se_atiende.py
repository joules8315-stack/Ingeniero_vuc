# -*- coding: utf-8 -*-
"""VIGIA — LO QUE EL CEREBRO PIDE EN SU RESPUESTA SE ATIENDE (nace ROJA a proposito).

Julio, 2026-09-30:
    "es mejor que el equipo venga en ayuda de la IA, asi como a Claude o Codex, que piden lo
     que necesitan y alli esta. Debe ser por programa."
    "siempre es lo mismo"

El "lo mismo" tiene nombre: el cerebro PIDE lo que le falta, con el formato correcto, y NADIE
LE CONTESTA. La vuelta muere ahi. Hoy paso tres veces: una con el obrero y dos con Codex.

ESTA PRUEBA NACE ROJA A PROPOSITO. El arreglo entra en la ronda SIGUIENTE y en esa misma ronda
queda enganchado. En esta ronda se entrega SOLO este archivo de prueba.

LO QUE MIDE (lo que se escribira en la ronda siguiente):
  a) cuerpo/obrero.py tendra una funcion NUEVA:
         atender_lo_que_pidio(respuesta, paquete, archivo, raiz)
     - le pide al mostrador las peticiones de esa respuesta;
     - sin peticiones: devuelve el paquete TAL CUAL, letra por letra;
     - con peticiones: llama al mostrador y, si trae algo util, pega el texto al final dentro
       de un bloque que empieza por el renglon
       "LO QUE PEDISTE EN TU RESPUESTA, ATENDIDO POR EL MOSTRADOR";
     - si no trae nada util: devuelve el paquete TAL CUAL;
     - NUNCA REVIENTA: ante cualquier problema devuelve el paquete tal cual.
     OJO: el ARCHIVO de cada peticion es el que venga DENTRO de la peticion del cerebro, no el
     que llega en el cuarto dato. El cuarto dato solo se usa si la peticion no dice archivo.
  b) La vuelta del trabajo la llamara antes de apuntar el motivo del rechazo, sobre el PAQUETE.
  c) Se atendera como maximo DOS veces por trabajo.

COMO SE MONTA:
  - La carpeta un nivel arriba de vigias y la carpeta arnes entran en sys.path con os.path.
  - La importacion de cuerpo/obrero.py va DENTRO de cada caso que la use, nunca arriba.
  - El caso 6 LEE cuerpo/obrero.py como texto y NO lo importa.
  - Orden de los datos al llamar: respuesta, paquete, archivo, raiz.

Sin IA, sin red, sin lanzar procesos. Siempre el mismo resultado.
"""
import os
import sys

import pytest


# ---------------------------------------------------------------------------
# ARRANQUE: la carpeta un nivel arriba de vigias y la carpeta arnes en sys.path
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
VIGIAS = AQUI
RAIZ = os.path.dirname(VIGIAS)
ARNES = os.path.join(RAIZ, "arnes")

for _ruta in (RAIZ, ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# ---------------------------------------------------------------------------
# EL ARCHIVO DE MENTIRA: se escribe dentro de la carpeta temporal de pytest
# ---------------------------------------------------------------------------
RELLENO = "\n".join(
    "# relleno linea %02d" % i for i in range(1, 21)
)

CODIGO_DE_MENTIRA = (
    "# -*- coding: utf-8 -*-\n"
    "\n"
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
REGLON_DEL_BLOQUE = "LO QUE PEDISTE EN TU RESPUESTA, ATENDIDO POR EL MOSTRADOR"


@pytest.fixture
def archivo_de_mentira(tmp_path):
    """Escribe el archivo de mentira dentro de la carpeta temporal de pytest."""
    ruta = tmp_path / "mentira_pieza.py"
    ruta.write_text(CODIGO_DE_MENTIRA, encoding="utf-8")
    return str(ruta)


def _importar_obrero():
    """Importa cuerpo/obrero.py DENTRO del caso. Si no puede, falla por afirmacion."""
    try:
        import cuerpo.obrero as obrero
    except Exception as exc:
        pytest.fail(
            "No se pudo importar cuerpo/obrero.py (%s). La funcion atender_lo_que_pidio "
            "todavia no existe: esta prueba nace ROJA a proposito." % exc
        )
    return obrero


def _exigir_funcion(obrero):
    """Exige que exista atender_lo_que_pidio y que se pueda llamar."""
    if not hasattr(obrero, "atender_lo_que_pidio"):
        pytest.fail(
            "cuerpo/obrero.py no tiene atender_lo_que_pidio. La funcion todavia no existe: "
            "esta prueba nace ROJA a proposito."
        )
    funcion = getattr(obrero, "atender_lo_que_pidio")
    if not callable(funcion):
        pytest.fail(
            "atender_lo_que_pidio existe pero no se puede llamar. La funcion todavia no "
            "esta lista: esta prueba nace ROJA a proposito."
        )
    return funcion


def _respuesta_con_peticion(ruta_archivo, nombre_funcion):
    """Arma una respuesta de mentira con un renglon de peticion bien formado.

    Formato: NECESITO_LEER: <archivo>:<nombre> / motivo / que decide / riesgo
    Las cuatro partes separadas por barra rodeada de espacios.
    """
    return (
        "El material no trae el cuerpo completo de la funcion que necesito.\n"
        "NECESITO_LEER: %s:%s / necesito el cuerpo entero de la funcion / "
        "decide el texto_viejo exacto a sustituir / riesgo: reconstruir de memoria ya fallo antes.\n"
        % (ruta_archivo, nombre_funcion)
    )


# ---------------------------------------------------------------------------
# CASO 1 — LA FUNCION NUEVA EXISTE (nace rojo)
# ---------------------------------------------------------------------------
def test_caso_1_la_funcion_nueva_existe():
    obrero = _importar_obrero()
    _exigir_funcion(obrero)


# ---------------------------------------------------------------------------
# CASO 2 — LO PEDIDO APARECE EN EL PAQUETE (nace rojo)
# ---------------------------------------------------------------------------
def test_caso_2_lo_pedido_aparece_en_el_paquete(archivo_de_mentira):
    obrero = _importar_obrero()
    funcion = _exigir_funcion(obrero)

    paquete = "PAQUETE DE MENTIRA SIN LA FUNCION PEDIDA\n"
    respuesta = _respuesta_con_peticion(archivo_de_mentira, "saluda")

    devuelto = funcion(respuesta, paquete, archivo_de_mentira, RAIZ)

    assert isinstance(devuelto, str), (
        "atender_lo_que_pidio debe devolver texto. Hoy el cerebro pide y nadie le contesta: "
        "eso freno tres vueltas hoy, dos de ellas a Codex."
    )
    assert len(devuelto) > len(paquete), (
        "El paquete devuelto tiene que ser MAS LARGO que el que entro: lo pedido debe "
        "aparecer dentro. Hoy el cerebro pide y nadie le contesta: eso freno tres vueltas "
        "hoy, dos de ellas a Codex."
    )
    assert PRIMER_RENGLON_SALUDA in devuelto, (
        "El paquete devuelto tiene que traer el primer renglon de la funcion saluda. Hoy el "
        "cerebro pide y nadie le contesta: eso freno tres vueltas hoy, dos de ellas a Codex."
    )
    assert REGLON_DEL_BLOQUE in devuelto, (
        "El paquete devuelto tiene que traer el renglon que anuncia el bloque: %r. Hoy el "
        "cerebro pide y nadie le contesta: eso freno tres vueltas hoy, dos de ellas a Codex."
        % REGLON_DEL_BLOQUE
    )


# ---------------------------------------------------------------------------
# CASO 3 — Y NO APARECE NADA MAS (nace rojo)
# ---------------------------------------------------------------------------
def test_caso_3_y_no_aparece_nada_mas(archivo_de_mentira):
    obrero = _importar_obrero()
    funcion = _exigir_funcion(obrero)

    paquete = "PAQUETE DE MENTIRA SIN LA FUNCION PEDIDA\n"
    respuesta = _respuesta_con_peticion(archivo_de_mentira, "saluda")

    devuelto = funcion(respuesta, paquete, archivo_de_mentira, RAIZ)

    assert PRIMER_RENGLON_DESPIDE not in devuelto, (
        "No debe aparecer la funcion despide: solo viaja la funcion pedida por su nombre y "
        "entera, y nada mas. Hoy el cerebro pide y nadie le contesta: eso freno tres vueltas "
        "hoy, dos de ellas a Codex."
    )
    assert "# relleno linea" not in devuelto, (
        "No debe aparecer el relleno del archivo: solo viaja la funcion pedida por su nombre "
        "y entera, y nada mas. Hoy el cerebro pide y nadie le contesta: eso freno tres "
        "vueltas hoy, dos de ellas a Codex."
    )


# ---------------------------------------------------------------------------
# CASO 4 — SIN PETICION EL PAQUETE NO SE TOCA (nace rojo)
# ---------------------------------------------------------------------------
def test_caso_4_sin_peticion_el_paquete_no_se_toca(archivo_de_mentira):
    obrero = _importar_obrero()
    funcion = _exigir_funcion(obrero)

    paquete = "PAQUETE DE MENTIRA QUE NO SE DEBE TOCAR\ncon dos renglones\n"
    respuesta = "Aqui va mi respuesta, sin pedir nada de nada.\n"

    devuelto = funcion(respuesta, paquete, archivo_de_mentira, RAIZ)

    assert devuelto == paquete, (
        "Sin peticion, el paquete devuelto tiene que ser EXACTAMENTE igual al que entro, "
        "letra por letra. Hoy el cerebro pide y nadie le contesta: eso freno tres vueltas "
        "hoy, dos de ellas a Codex."
    )


# ---------------------------------------------------------------------------
# CASO 5 — NO REVIENTA (nace rojo)
# ---------------------------------------------------------------------------
def test_caso_5_no_revienta(archivo_de_mentira, tmp_path):
    obrero = _importar_obrero()
    funcion = _exigir_funcion(obrero)

    paquete = "PAQUETE DE MENTIRA\n"
    archivo_que_no_existe = str(tmp_path / "no_existe_jamas.py")
    carpeta_que_no_existe = str(tmp_path / "carpeta_que_no_existe")

    casos = [
        (None, paquete, archivo_de_mentira, RAIZ),
        (12345, paquete, archivo_de_mentira, RAIZ),
        ("", "", archivo_de_mentira, RAIZ),
        ("", paquete, archivo_que_no_existe, RAIZ),
        ("", paquete, archivo_de_mentira, carpeta_que_no_existe),
    ]

    for respuesta, paq, arch, raiz in casos:
        try:
            devuelto = funcion(respuesta, paq, arch, raiz)
        except Exception as exc:
            pytest.fail(
                "atender_lo_que_pidio NUNCA debe reventar: ante cualquier problema devuelve "
                "el paquete tal cual. Revento con respuesta=%r archivo=%r raiz=%r: %s. Hoy el "
                "cerebro pide y nadie le contesta: eso freno tres vueltas hoy, dos de ellas a "
                "Codex." % (respuesta, arch, raiz, exc)
            )
        assert isinstance(devuelto, str), (
            "atender_lo_que_pidio debe devolver siempre un texto, tambien cuando algo va "
            "mal. Hoy el cerebro pide y nadie le contesta: eso freno tres vueltas hoy, dos "
            "de ellas a Codex."
        )
        assert devuelto == paq, (
            "Ante cualquier problema, atender_lo_que_pidio devuelve el paquete TAL CUAL. "
            "Hoy el cerebro pide y nadie le contesta: eso freno tres vueltas hoy, dos de "
            "ellas a Codex."
        )


# ---------------------------------------------------------------------------
# CASO 6 — LA VUELTA YA LA LLAMA (nace rojo)
# ---------------------------------------------------------------------------
def test_caso_6_la_vuelta_ya_la_llama():
    ruta_obrero = os.path.join(RAIZ, "cuerpo", "obrero.py")
    assert os.path.isfile(ruta_obrero), (
        "No se encuentra cuerpo/obrero.py en %r. Hoy el cerebro pide y nadie le contesta: "
        "eso freno tres vueltas hoy, dos de ellas a Codex." % ruta_obrero
    )

    with open(ruta_obrero, "r", encoding="utf-8", errors="replace") as f:
        lineas = f.read().splitlines()

    # Se busca el renglon donde se apunta el motivo del rechazo dentro de la vuelta del trabajo.
    indices_motivo = []
    for i, linea in enumerate(lineas):
        if "motivo" in linea and ("rechaz" in linea.lower() or "apunt" in linea.lower()):
            indices_motivo.append(i)

    assert indices_motivo, (
        "No se encontro en cuerpo/obrero.py el renglon donde se apunta el motivo del rechazo "
        "dentro de la vuelta del trabajo. Hoy el cerebro pide y nadie le contesta: eso freno "
        "tres vueltas hoy, dos de ellas a Codex."
    )

    # Se comprueba que CERCA de ese sitio aparece una llamada a atender_lo_que_pidio.
    VENTANA = 40
    encontrado = False
    for i in indices_motivo:
        desde = max(0, i - VENTANA)
        hasta = min(len(lineas), i + VENTANA + 1)
        for j in range(desde, hasta):
            if "atender_lo_que_pidio" in lineas[j]:
                encontrado = True
                break
        if encontrado:
            break

    assert encontrado, (
        "Hoy el cerebro pide y nadie le contesta: eso freno tres vueltas hoy, dos de ellas a "
        "Codex. La vuelta del trabajo tiene que llamar a atender_lo_que_pidio cerca del sitio "
        "donde apunta el motivo del rechazo, antes de volver a intentar."
    )
