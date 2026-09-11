# -*- coding: utf-8 -*-
"""VIGIA — UNA VIGIA NO MIENTE POR EL NOMBRE.

EL FALLO, y es de los que dejan pasar lo que si se rompio:
Una vigia lee el codigo de un archivo .py del proyecto (con open(...).read() o con un helper
_vivo que devuelve el texto) y luego afirma con un assert que 'tal palabra esta en ESE texto'.
Si ese archivo leido tiene MAS DE UNA funcion 'def ' a nivel de modulo, hay VARIOS CAMINOS
dentro del mismo archivo. Que la palabra aparezca en el texto NO prueba que el camino prometido
se haya probado: la palabra puede estar en OTRA funcion, en un comentario, en un docstring o en
una rama que nadie ejecuta. La vigia se llama 'test_vigia_X' pero miente por el nombre: dice
que vigila X y en realidad solo mira que la letra X exista en algun sitio del archivo.

LA CURA: cazar el par (lee_archivo_py, assert_final_in). Si el archivo leido tiene mas de un
'def ' a nivel de modulo, el par queda MARCADO. La vigia nace ROJA de proposito mientras haya
mentirosas: NO se anaden excepciones para que pase. Solo se exceptuan los casos donde la
palabra ES el contrato (comprobar que un comando existe en el despachador 'if cmd ==' de
ingeniero.py, o que un import existe): ahi la palabra no promete un camino, promete presencia.

ESTA VIGIA VIGILA A LOS VIGILANTES: si manana alguien escribe otra vigia que lee un archivo
con varios caminos y afirma 'algo in texto', esta vigia lo caza antes de que vuelva a mentir.
"""
import os
import re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Los archivos que se leen para buscar el par (lee_archivo_py, assert_final_in).
# Se escanean las vigias del proyecto, que es donde vive el vicio.
CARPETA_VIGIAS = os.path.join(AQUI, "vigias")

# EXCEPCIONES LEGITIMAS: aqui la palabra ES el contrato, no promete un camino.
# Cada una con su por que escrito. NO se anaden mas para que la vigia pase.
EXCEPCIONES = [
    # (vigia, archivo_leido, por_que)
    (
        "test_vigia_el_despachador_no_pierde_comandos.py",
        "ingeniero.py",
        "Aqui la palabra ES el contrato: se comprueba que un comando existe en el "
        "despachador 'if cmd ==' de ingeniero.py. No se promete un camino, se promete "
        "presencia en la tabla de despacho. Que ingeniero.py tenga varios 'def ' es "
        "irrelevante: el contrato es que el comando este listado.",
    ),
    (
        "test_vigia_los_imports_no_se_pierden.py",
        "ingeniero.py",
        "Aqui la palabra ES el contrato: se comprueba que un import existe en el archivo. "
        "Un import no es un camino, es una dependencia declarada. Que el archivo tenga "
        "varios 'def ' no cambia que el import este o no este.",
    ),
]


def _vivo(rel):
    """Devuelve el codigo de un archivo del proyecto sin docstrings ni comentarios.

    Mismo helper que usa test_vigia_una_vigia_recien_nacida_no_es_averia.py: quita
    docstrings (triples comillas) y comentarios (#) para que la deteccion no se
    confunda con texto que no es codigo.
    """
    ruta = os.path.join(AQUI, *rel.split("/"))
    if not os.path.exists(ruta):
        return ""
    with open(ruta, encoding="utf-8") as f:
        codigo = f.read()
    codigo = re.sub(r'"""(?:.|\n)*?"""', " ", codigo)
    codigo = re.sub(r"'''(?:.|\n)*?'''", " ", codigo)
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in codigo.splitlines())


def _defs_a_nivel_de_modulo(codigo):
    """Cuenta las funciones 'def ' a nivel de modulo (columna 0).

    Solo cuentan las que empiezan en la columna 0: las anidadas dentro de otra
    funcion o clase no son caminos de modulo distintos.
    """
    n = 0
    for ln in codigo.splitlines():
        if re.match(r"^def\s+\w+\s*\(", ln):
            n += 1
    return n


def _lee_archivo_py(codigo_vigia):
    """Detecta si la vigia lee el contenido de un .py del proyecto.

    Devuelve la ruta relativa del archivo leido, o None si no lee ninguno.
    Reconoce dos formas: open(...).read() sobre un .py, y el helper _vivo(...)
    que devuelve el codigo de un archivo del proyecto.
    """
    # Forma 1: open("...py").read() o open(os.path.join(...)).read()
    m = re.search(r'open\([^)]*\.py[^)]*\)\s*\.read\(\)', codigo_vigia)
    if m:
        # Intentar sacar la ruta relativa del literal
        lit = re.search(r'["\']([^"\']+\.py)["\']', m.group(0))
        if lit:
            return lit.group(1).replace("\\", "/")
        return "<open .py dinamico>"
    # Forma 2: _vivo("ruta/al/archivo.py")
    m = re.search(r'_vivo\(\s*["\']([^"\']+\.py)["\']\s*\)', codigo_vigia)
    if m:
        return m.group(1).replace("\\", "/")
    return None


def _assert_final_in(codigo_vigia):
    """Detecta si la vigia hace un assert con 'algo in <texto>'.

    Devuelve True si hay un assert que comprueba pertenencia ('in') sobre el texto
    leido. Es la firma de la mentira por nombre: la palabra aparece, el camino no
    se probo.
    """
    for ln in codigo_vigia.splitlines():
        s = ln.strip()
        if s.startswith("assert ") and " in " in s:
            return True
    return False


def _es_excepcion(vigia, archivo_leido):
    """True si el par (vigia, archivo_leido) esta en la lista de excepciones."""
    for v, a, _por_que in EXCEPCIONES:
        if v == vigia and a == archivo_leido:
            return True
    return False


def _marcados():
    """Devuelve la lista de pares (vigia, archivo_leido) que MIENTEN POR NOMBRE.

    Un par miente si: la vigia lee un .py del proyecto, hace un assert con 'in'
    sobre ese texto, y el archivo leido tiene MAS DE UNA funcion 'def ' a nivel de
    modulo (varios caminos). La palabra aparece pero el camino prometido no se
    probo. Los pares en EXCEPCIONES no se marcan: ahi la palabra ES el contrato.
    """
    marcados = []
    if not os.path.isdir(CARPETA_VIGIAS):
        return marcados
    for nombre in sorted(os.listdir(CARPETA_VIGIAS)):
        if not (nombre.startswith("test_vigia_") and nombre.endswith(".py")):
            continue
        codigo_vigia = _vivo("vigias/" + nombre)
        if not codigo_vigia:
            continue
        archivo_leido = _lee_archivo_py(codigo_vigia)
        if not archivo_leido:
            continue
        if not _assert_final_in(codigo_vigia):
            continue
        codigo_leido = _vivo(archivo_leido)
        if not codigo_leido:
            continue
        if _defs_a_nivel_de_modulo(codigo_leido) <= 1:
            continue
        if _es_excepcion(nombre, archivo_leido):
            continue
        marcados.append((nombre, archivo_leido))
    return marcados


def test_ninguna_vigia_miente_por_el_nombre():
    """Ninguna vigia lee un .py con varios caminos y afirma 'algo in texto'.

    Si hay mentirosas, esta vigia queda ROJA de proposito: nace roja porque el
    vicio existe. NO se anaden excepciones para que pase. La lista de marcados va
    en el mensaje del assert para que se vea quien miente y sobre que archivo.
    """
    marcados = _marcados()
    assert not marcados, (
        "VIGIAS QUE MIENTEN POR EL NOMBRE (leen un .py con mas de un 'def ' a nivel "
        "de modulo y afirman 'algo in texto'): " + repr(marcados)
    )


def test_las_excepciones_tienen_su_por_que():
    """Cada excepcion legitima trae escrito su por que.

    Una excepcion sin por que es una puerta abierta: manana nadie sabe si era
    legitima o si se colo para que la vigia pasara.
    """
    for v, a, por_que in EXCEPCIONES:
        assert v and a and por_que and len(por_que.strip()) > 20, (
            "EXCEPCION SIN POR QUE ESCRITO: " + repr((v, a, por_que))
        )


def test_el_detector_reconoce_la_mentira():
    """El detector reconoce la firma de la mentira por nombre.

    Se le da un codigo de mentira fabricado y debe marcarlo: lee un .py, hace
    assert con 'in', y el archivo leido tiene varios 'def ' a nivel de modulo.
    """
    codigo_mentiroso = (
        "def test_vigia_x():\n"
        "    codigo = _vivo('ingeniero.py')\n"
        "    assert 'trabaja' in codigo\n"
    )
    archivo_leido = _lee_archivo_py(codigo_mentiroso)
    assert archivo_leido == "ingeniero.py", (
        "EL DETECTOR NO RECONOCE EL PAR (lee_archivo_py, assert_final_in): "
        + repr(archivo_leido)
    )
    assert _assert_final_in(codigo_mentiroso), (
        "EL DETECTOR NO RECONOCE EL ASSERT CON 'in' SOBRE EL TEXTO LEIDO"
    )
    codigo_leido = _vivo("ingeniero.py")
    assert _defs_a_nivel_de_modulo(codigo_leido) > 1, (
        "ingeniero.py deberia tener mas de un 'def ' a nivel de modulo: "
        + repr(_defs_a_nivel_de_modulo(codigo_leido))
    )
