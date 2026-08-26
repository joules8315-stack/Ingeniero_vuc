# -*- coding: utf-8 -*-
"""VIGIA — el paquete trae EL CODIGO, no solo las pruebas que hablan del fallo.

FALLO REAL (2026-08-25). Julio lo cazo con una pregunta: "¿y por que vas a tocar 16 mil lineas?
si ese no es el contrato, solo un pedazo".
Tenia razon: para reparar el arranque hacian falta ~10 lineas del programa. Pero el paquete traia
TRES pedazos y los tres eran de las vigias que YO acababa de escribir, ninguno del programa.

POR QUE PASABA: los pedazos se puntuan por parecido de palabras. Una vigia escribe el problema
con las palabras de Julio en su cabecera, asi que gana siempre. El repartidor se devolvia a si
mismo su propio texto, y el codigo donde vive el fallo no aparecia.

CONSECUENCIA: no se podia reparar. El candado de equipo solo abre los archivos que el equipo tuvo
delante, y el programa nunca estaba delante. Un candado sin forma honrada de cumplirse.

LA REGLA: una prueba que DESCRIBE un fallo no es donde VIVE el fallo. Las pruebas siguen entrando
en el paquete (son contexto util), pero no pueden tapar al codigo.

ESTA VIGIA NACE ROJA.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from cerebro import grafo, router  # noqa: E402

# RESUELTO (2026-08-25) con el diccionario (arnes/diccionario.py + router): el repartidor ahora
# COSECHA de cada causa raiz la pareja "palabras de Julio <-> codigo exacto", asi que foto_informe
# ya trae la pantalla (app_web.html) ademas de las vigias. El caso de DMM sigue siendo exigencia
# dura, porque alli el codigo SI esta escrito en el idioma del problema.
# Un problema de CONDUCTA del programa, dicho como lo diria Julio.
CASOS = [
    pytest.param("foto_informe",
                 "al arrancar no se piden los informes diarios y la lista sale vacia"),
    pytest.param("dmm", "el onboarding no guarda el perfil de la empresa"),
]


def _es_prueba(nombre):
    n = os.path.basename(str(nombre or "")).lower()
    return (n.startswith("test_") or n.startswith("rv3_vigia") or n.startswith("rv3_prueba")
            or n.startswith("rv3_aislar") or "/vigias/" in str(nombre).replace("\\", "/").lower())


@pytest.mark.parametrize("apodo,problema", CASOS, ids=["foto_informe", "dmm"])
def test_el_paquete_trae_al_menos_un_pedazo_de_codigo(apodo, problema):
    prs = grafo.proyectos()
    if apodo not in prs or not os.path.isdir(prs[apodo]["ruta"]):
        pytest.skip("%s no esta en esta maquina" % apodo)

    pk = router.armar(apodo, problema)
    trozos = pk.get("trozos") or []
    assert trozos, "el paquete no trae ni un pedazo: no se puede reparar nada"

    de_codigo = [t for t in trozos if not _es_prueba(t.get("pieza"))]
    de_prueba = [t for t in trozos if _es_prueba(t.get("pieza"))]

    assert de_codigo, (
        "el paquete de %r trae %d pedazo(s) y TODOS son de pruebas (%s). Una prueba que "
        "describe el fallo no es donde vive el fallo: asi no se puede reparar, y el candado de "
        "equipo no abrira nunca el archivo del programa."
        % (problema, len(trozos), ", ".join(sorted({str(t.get("pieza")) for t in de_prueba})[:3])))


@pytest.mark.parametrize("apodo,problema", CASOS, ids=["foto_informe", "dmm"])
def test_las_pruebas_no_copan_el_paquete(apodo, problema):
    """Que entren, pero que no lo llenen: si mas de la mitad son pruebas, tapan al codigo."""
    prs = grafo.proyectos()
    if apodo not in prs or not os.path.isdir(prs[apodo]["ruta"]):
        pytest.skip("%s no esta en esta maquina" % apodo)

    trozos = (router.armar(apodo, problema).get("trozos") or [])
    if not trozos:
        pytest.skip("sin pedazos, ya lo dice la otra comprobacion")
    de_prueba = [t for t in trozos if _es_prueba(t.get("pieza"))]
    assert len(de_prueba) * 2 <= len(trozos), (
        "de %d pedazos, %d son de pruebas: estan tapando al codigo donde vive el fallo"
        % (len(trozos), len(de_prueba)))
