# -*- coding: utf-8 -*-
"""VIGIA — el diccionario que traduce las palabras de Julio al sitio del codigo.

DE DONDE SALE (2026-08-25). El repartidor no encuentra el codigo cuando Julio describe un
problema, y esta medido: para "al arrancar no se piden los informes diarios y la lista sale
vacia" devolvio TRES pedazos y los tres eran vigias mias; del programa, cero. El motivo no es que
busque mal: es que Julio habla en espanol y de negocio, y el codigo esta en ingles y comprimido.
NUNCA se van a parecer, por mucho que se afine la busqueda.

LA IDEA: cada vez que se declara una causa, el sistema YA obliga a escribir el problema en
palabras de Julio Y el archivo, la funcion y la linea exactos. **Ese par ya existe y ya esta
probado con evidencia.** El diccionario se cosecha de ahi: no hay que sentarse a escribirlo, se
llena solo con el trabajo, y solo guarda parejas demostradas, nunca suposiciones.

CORRECCION DE CLINE, aceptada: un diccionario que sea solo un documento acaba siendo papel viejo.
Tiene que consumirlo el repartidor. Reparto acordado: Claude hace el diccionario, Cline lo
conecta al router con su vigia de uso.

LO PRIMERO QUE HAY QUE ARREGLAR, descubierto al empezar: `memoria/DIAGNOSTICO.json` guarda UNA
sola causa y se sobrescribe. De las cuatro declaradas hoy quedaba una. Sin historia no hay
cosecha: el diccionario naceria vacio para siempre.

ESTA VIGIA NACE ROJA.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import diccionario  # noqa: E402


def _aparte(tmp_path, monkeypatch):
    """El diccionario de mentira vive aparte: NUNCA se toca el de verdad."""
    falso = str(tmp_path / "diccionario_de_mentira.json")
    monkeypatch.setattr(diccionario, "RUTA", falso, raising=False)
    sitio = tmp_path / "app_web.html"
    sitio.write_text("", encoding="utf-8")
    monkeypatch.setattr(diccionario, "AQUI", str(tmp_path), raising=False)
    return falso


def test_aprende_una_pareja(tmp_path, monkeypatch):
    """Lo minimo: guardar que 'esto que dice Julio' vive en 'este sitio del codigo'."""
    _aparte(tmp_path, monkeypatch)
    diccionario.aprender("al arrancar no se piden los informes diarios y la lista sale vacia",
                         "app_web.html", "enterApp", 2092, "foto_informe")
    sitios = diccionario.buscar("los informes no cargan al abrir el programa")
    assert sitios, ("no encuentra el sitio del codigo con palabras PARECIDAS a las de Julio. "
                    "Si solo sirve con las palabras exactas, no sirve para nada: Julio nunca "
                    "repite el problema igual dos veces")
    assert any(s.get("archivo") == "app_web.html" for s in sitios)


def test_no_inventa_cuando_no_sabe(tmp_path, monkeypatch):
    """Ley 2 de Julio: nunca inventar. Si no lo ha aprendido, se calla."""
    _aparte(tmp_path, monkeypatch)
    diccionario.aprender("los informes no cargan", "app_web.html", "enterApp", 2092,
                         "foto_informe")
    assert not diccionario.buscar("el cobro de la suscripcion sale duplicado"), (
        "devolvio un sitio para algo que NUNCA aprendio: eso es inventar, y un diccionario que "
        "inventa es peor que no tenerlo")


def test_guarda_VARIAS_y_no_se_pisan(tmp_path, monkeypatch):
    """El fallo que se encontro al empezar: la causa se sobrescribia y solo quedaba la ultima."""
    _aparte(tmp_path, monkeypatch)
    diccionario.aprender("los informes no cargan al arrancar", "app_web.html", "enterApp", 2092,
                         "foto_informe")
    diccionario.aprender("borrar la asignacion de filas se deshace sola", "app_web.html",
                         "resetRowAssignmentsBtn", 2299, "foto_informe")
    diccionario.aprender("el mando se muere al mostrar la respuesta del equipo", "ingeniero.py",
                         "main", 210, "ingeniero")
    assert len(diccionario.todo()) >= 3, (
        "se perdieron parejas por el camino: si cada una pisa a la anterior, el diccionario "
        "nunca crece y no sirve de nada")


def test_la_misma_cosa_dicha_dos_veces_no_se_duplica(tmp_path, monkeypatch):
    """Julio repite los problemas con otras palabras; el sitio es el mismo."""
    _aparte(tmp_path, monkeypatch)
    diccionario.aprender("los informes no cargan al arrancar", "app_web.html", "enterApp", 2092,
                         "foto_informe")
    diccionario.aprender("los informes no cargan al arrancar", "app_web.html", "enterApp", 2092,
                         "foto_informe")
    sitios = diccionario.buscar("los informes no cargan al arrancar")
    assert len(sitios) == 1, "el mismo sitio guardado dos veces: el diccionario se ensucia solo"


def test_lo_mas_reciente_manda(tmp_path, monkeypatch):
    """Si un problema se reparo en dos sitios distintos, el ultimo es el que vale mas."""
    _aparte(tmp_path, monkeypatch)
    diccionario.aprender("los informes no cargan", "app_web.html", "viejo", 100, "foto_informe")
    diccionario.aprender("los informes no cargan", "app_web.html", "enterApp", 2092,
                         "foto_informe")
    sitios = diccionario.buscar("los informes no cargan")
    assert sitios[0].get("funcion") == "enterApp", (
        "el sitio mas reciente no va primero: se le daria al equipo el sitio viejo")


def test_solo_guarda_lo_PROBADO(tmp_path, monkeypatch):
    """Sin archivo o sin sitio no hay pareja: no se guarda una suposicion."""
    _aparte(tmp_path, monkeypatch)
    for archivo, funcion in (("", "enterApp"), ("app_web.html", ""), ("", "")):
        diccionario.aprender("algo que paso", archivo, funcion, 1, "foto_informe")
    assert not diccionario.todo(), (
        "guardo una pareja sin sitio probado: el diccionario solo vale si cada pareja "
        "salio de una causa demostrada, y si acepta suposiciones envenena al repartidor")


def test_no_hace_falta_mirar_fuera_de_esta_carpeta(tmp_path, monkeypatch):
    """Sin el mapa de proyectos la prueba sigue encontrando el sitio: no depende de fuera."""
    import builtins

    _aparte(tmp_path, monkeypatch)

    de_siempre = builtins.__import__

    def falso_import(nombre, *args, **kwargs):
        if nombre.startswith("cerebro"):
            raise ImportError("el mapa de proyectos esta escondido a proposito")
        return de_siempre(nombre, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", falso_import)

    primero = diccionario.aprender("los informes no cargan", "app_web.html", "viejo", 100,
                                   "foto_informe")
    segundo = diccionario.aprender("los informes no cargan", "app_web.html", "enterApp", 2092,
                                   "foto_informe")

    assert primero and segundo, (
        "sin el mapa de proyectos la prueba deja de encontrar el sitio, o sea que sigue "
        "dependiendo de un archivo de otro proyecto y por eso es inestable")

    sitios = diccionario.buscar("los informes no cargan")
    assert sitios[0].get("funcion") == "enterApp", (
        "el primer sitio que sale no es enterApp: la prueba no esta mirando donde debe")



def test_no_guarda_un_sitio_cuyo_archivo_NO_existe_en_el_disco(tmp_path, monkeypatch):
    """EL VENENO (encargo de Claude a Cline, 2026-08-31): la entrada falsa era
    archivo a.py, funcion f, proyecto p — un sitio que NO existe.

    aprender() dice en su docstring \"sin sitio probado no se guarda nada\" pero NO
    lo comprueba: guarda cualquier archivo, exista o no en el disco. Ese sitio
    fantasma casa con casi cualquier problema (basta 1 palabra) y gana, asi que el
    repartidor recibe un archivo que no existe.
    """
    _aparte(tmp_path, monkeypatch)
    # "foto_informe" es un proyecto real, pero este archivo NO existe ahi.
    ok = diccionario.aprender("un problema que se describe con estas palabras",
                              "archivo_que_no_existe_xyz.py", "funcion_falsa", 1, "foto_informe")
    assert ok is False, (
        "aprender() guardo un sitio cuyo archivo NO existe en el disco. El diccionario debe "
        "prometer menos y cumplir mas: sin sitio probado en el disco no se guarda nada")
    assert not diccionario.todo(), (
        "se guardo un sitio fantasma (archivo que no existe): envenena al repartidor porque casa "
        "con casi cualquier problema y gana")


def test_tambien_dicho_NO_crece_sin_limite(tmp_path, monkeypatch):
    """EL IMAN: una entrada \"aprendida\" de 500 maneras es un iman, no un sitio.

    El veneno tenia 571 apariciones y 27 formas de decirlo. Cada forma nueva lo hace
    casar con mas problemas y ganar. Se queda con las ultimas y se descarta el resto.
    """
    _aparte(tmp_path, monkeypatch)
    # un sitio REAL para que pase la comprobacion de existencia
    import os as _os
    real = _os.path.join(AQUI, "ingeniero.py")
    n = 60
    for i in range(n):
        diccionario.aprender("frase distinta numero %d de este mismo problema" % i,
                             real, "main", 1, "ingeniero")
    datos = diccionario.todo()
    assert datos, "no guardo nada, pero deberia haber guardado el sitio real"
    formas = len(datos[0].get("tambien_dicho") or [])
    assert formas <= 20, (
        "tambien_dicho crecio sin limite: %d formas de decir lo mismo. Un sitio aprendido de "
        "demasiadas maneras es un iman que casa con cualquier problema. Tope a las ultimas." % formas)
