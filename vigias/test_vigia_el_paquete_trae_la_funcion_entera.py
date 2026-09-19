# -*- coding: utf-8 -*-
"""VIGIA — el paquete trae la FUNCION ENTERA, no un pedazo suelto.

Ley: CONTRATO_SE_BUSCA_POR_NOMBRE.md (Julio, 2026-08-31) y el diagnostico del 2026-09-05.

Julio, 2026-09-05: "el gran problema que veo es que estos son repos muy grandes y no tienes el
contexto... ese es el objetivo de la memoria y del repartidor, que no has podido resolver".

EL FALLO, MEDIDO. El repartidor elige trozos por PARECIDO DE PALABRAS en ventanas de 40 renglones.
Las palabras no saben donde empieza ni donde acaba una funcion, asi que entrega pedazos huerfanos:
  · pidiendo la funcion que escribe la casilla, trajo las lineas 1-80 del archivo (la portada),
    y la funcion estaba en la 5300;
  · pidiendo la funcion cortar, trajo las lineas 1-40 y 129-168, y cortar estaba en la 54;
  · el auditor rechazo tres rondas diciendo que se usaban cosas inventadas, y esas cosas estaban
    declaradas en lineas que el paquete nunca le enseño.

CONSECUENCIA MEDIDA: 2 de 70 trabajos del equipo sirvieron (3%). La mayoria se cae por material
incompleto, y cada ronda se paga igual.

Y LO PEOR: la solucion YA ESTA CONSTRUIDA. `piezas.funcion_completa(ruta, nombre)` devuelve la
funcion entera buscandola por su nombre. Pero el repartidor la usa en UN SOLO SITIO, con el nombre
'armar' escrito a mano, para repararse a si mismo. Todo lo demas sigue recibiendo ventanas de 40
renglones. La propia memoria del sistema lo dice: "queda pendiente" generalizarlo.

ESTA VIGIA NACE ROJA: la funcion que generaliza eso no existe todavia.

No llama a la red ni a ningun cerebro: le da trozos de mentira y mira que devuelve.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from cerebro import router  # noqa: E402

CODIGO_DE_MENTIRA = '''import os

TOPE = 40


def pequena():
    return 1


def la_que_importa(a, b):
    """Esta es la que hay que traer entera."""
    total = 0
    for x in range(a):
        total += x
    if total > b:
        total = b
    return total


def otra():
    return 2
'''


@pytest.fixture
def pieza(tmp_path):
    p = tmp_path / "pieza_falsa.py"
    p.write_text(CODIGO_DE_MENTIRA, encoding="utf-8")
    return {"id": "pieza_falsa.py", "abs": str(p), "rol": "codigo"}


def _trozo(pieza, desde, hasta):
    lineas = CODIGO_DE_MENTIRA.splitlines()
    return {"pieza": pieza["id"], "abs": pieza["abs"], "rol": pieza["rol"],
            "desde": desde, "hasta": hasta,
            "texto": "\n".join(lineas[desde - 1:hasta]), "puntaje": 10.0}


def test_un_trozo_que_cae_DENTRO_de_una_funcion_se_trae_entera(pieza):
    """EL FALLO EXACTO: el trozo empieza a mitad de la funcion y no se ve ni el def."""
    # Las lineas 14-16 caen dentro de la_que_importa, sin su cabecera ni su final.
    salida = router.completar_funciones([_trozo(pieza, 14, 16)], [pieza])
    junto = " ".join(t["texto"] for t in salida)
    assert "def la_que_importa" in junto, (
        "el paquete entrega un pedazo de la funcion SIN su cabecera. Asi el auditor no ve donde "
        "empieza, cree que se usan cosas inventadas, y rechaza reparaciones correctas")
    assert "return total" in junto, (
        "el paquete corta la funcion antes de su final: el obrero tiene que adivinar el resto y "
        "por eso se lo inventa")


def test_NO_se_arrastran_las_funciones_vecinas(pieza):
    """Traer de mas tambien cuesta dinero: se trae la funcion, no el archivo entero."""
    salida = router.completar_funciones([_trozo(pieza, 14, 16)], [pieza])
    junto = " ".join(t["texto"] for t in salida)
    assert "def otra" not in junto, "se trajo tambien la funcion de al lado: eso es gastar de mas"
    assert "def pequena" not in junto, "se trajo tambien la funcion de arriba"


def test_lo_de_fuera_de_toda_funcion_se_respeta(pieza):
    """Las importaciones y las constantes de arriba no estan dentro de ninguna funcion.

    No se tocan: se dejan tal cual, porque son justo lo que el auditor necesita ver para no creer
    que algo esta inventado.
    """
    salida = router.completar_funciones([_trozo(pieza, 1, 3)], [pieza])
    junto = " ".join(t["texto"] for t in salida)
    assert "import os" in junto and "TOPE" in junto, (
        "se perdio la cabecera del archivo, que es lo que evita que el auditor crea que las cosas "
        "estan inventadas")


def test_no_se_duplica_si_ya_venia_entera(pieza):
    """Si el trozo ya trae la funcion completa, no se anade otra vez."""
    salida = router.completar_funciones([_trozo(pieza, 11, 19)], [pieza])
    junto = "\n".join(t["texto"] for t in salida)
    assert junto.count("def la_que_importa") == 1, (
        "la misma funcion aparece dos veces en el paquete: eso es pagar el doble por lo mismo")


def test_dos_trozos_de_la_MISMA_funcion_se_juntan_en_una(pieza):
    """Dos pedazos de la misma funcion son la misma funcion, no dos."""
    salida = router.completar_funciones([_trozo(pieza, 13, 14), _trozo(pieza, 17, 18)], [pieza])
    junto = "\n".join(t["texto"] for t in salida)
    assert junto.count("def la_que_importa") == 1, (
        "la funcion se entrego dos veces por venir en dos pedazos: se paga dos veces lo mismo")


def test_si_la_pieza_no_se_puede_leer_no_revienta(tmp_path):
    """Un fallo al leer NO puede tumbar el paquete entero: se devuelve lo que habia."""
    fantasma = {"id": "no_existe.py", "abs": str(tmp_path / "no_existe.py"), "rol": "codigo"}
    t = {"pieza": "no_existe.py", "abs": fantasma["abs"], "rol": "codigo",
         "desde": 1, "hasta": 3, "texto": "algo", "puntaje": 1.0}
    salida = router.completar_funciones([t], [fantasma])
    assert salida and salida[0]["texto"] == "algo", (
        "al no poder leer una pieza se perdio el trozo que ya se tenia")


def test_el_obrero_recibe_todos_los_archivos_que_nombra_la_tarea():
    """Si la tarea nombra varios archivos, el obrero tiene que recibir los trozos de TODOS."""
    from cuerpo import obrero
    paquete = "\n".join([
        "# PAQUETE",
        "## 1. LA LEY QUE MANDA",
        "ley",
        "## 3. LOS TROZOS",
        "### `cuerpo/a.py` relevancia 1.0",
        "TEXTO_DE_A",
        "### `cuerpo/b.py` relevancia 0.5",
        "TEXTO_DE_B",
        "### `cuerpo/c.py` relevancia 0.2",
        "TEXTO_DE_C",
    ])
    s = obrero._filtrar_paquete(paquete, archivo=["cuerpo/a.py", "cuerpo/b.py"], tope=100000)
    assert "TEXTO_DE_A" in s, "falta el trozo del primer archivo que la tarea nombra"
    assert "TEXTO_DE_B" in s, "falta el trozo del segundo archivo que la tarea nombra"
    assert "TEXTO_DE_C" not in s, "se colo un archivo que la tarea no nombro"
    s1 = obrero._filtrar_paquete(paquete, archivo="cuerpo/b.py", tope=100000)
    assert "TEXTO_DE_B" in s1, "falta el trozo del archivo que la tarea nombra"
    assert "TEXTO_DE_A" not in s1, "se colo un archivo que la tarea no nombro"
