# -*- coding: utf-8 -*-
"""VIGIA — EL OJO 2: EL REVISOR DE PROGRAMA. Caza lo mecanico SIN gastar ni una IA.

TURNO 1 DEL PLAN (Julio, 2026-09-08). Nace de DOS fallos medidos EL MISMO DIA, los dos con
dos cerebros delante y ninguno los vio:

  1. El equipo escribio una prueba que REVENTABA en la primera linea: usaba una herramienta
     que no habia importado. La aprobo un cerebro DISTINTO, con "confianza alta". Se corrio
     y fallo: NameError. Un programa lo caza leyendo el codigo, en un segundo.
  2. El equipo RECHAZO por invento las constantes que el propio encargo le mandaba definir.
     La cura de ese fallo existia desde el 2026-09-06 y era UN PARRAFO que intenta convencer
     al auditor. El auditor lo leyo y rechazo igual.

LA LEY QUE HACE CUMPLIR (CONTRATO_CUENTA_O_JUICIO.md, Julio 2026-09-07):
lo que se puede comprobar con una CUENTA no se le manda a un cerebro. Y de lo que el auditor
rechazo en un dia, casi todo era cuenta:
    "texto viejo y nuevo son identicos"   -> comparar
    "usa un nombre que no existe"         -> leer el codigo
    "no implementa lo que se pidio"       -> buscar un nombre
    "es una regresion total"              -> ESO SI es juicio, y se queda para la IA

EL PROGRAMA SE SUMA, NO SUSTITUYE: el auditor de IA sigue siendo obligatorio para el juicio.
Lo que cambia es que lo mecanico deja de depender de que un cerebro se fije.

ESTA VIGIA NACE ROJA A PROPOSITO: arnes/revisor_de_programa.py todavia no existe.
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _revisor():
    try:
        import revisor_de_programa
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/revisor_de_programa.py (el ojo 2). Sin el, lo mecanico depende "
            "de que un cerebro se fije, y el 2026-09-08 quedo medido que no se fija: dos "
            "cerebros aprobaron codigo que revienta en la primera linea.")
    return revisor_de_programa


def test_caza_el_nombre_que_no_existe():
    """El fallo real del 2026-09-08: usa `re` sin haberlo importado. Dos cerebros lo aprobaron."""
    r = _revisor()
    propuesta = {
        "archivo": "vigias/ejemplo.py",
        "texto_viejo": "import os\n",
        "texto_nuevo": "import os\n\ndef f(t):\n    return re.sub('a', 'b', t)\n",
    }
    fallos = r.revisar(propuesta, tarea="cambiar el filtro")
    assert any("re" in str(f) for f in fallos), (
        "NO CAZO el nombre que no existe. Es el fallo exacto del 2026-09-08: el codigo usa "
        "una herramienta que nunca se importo y revienta en cuanto se corre.")


def test_caza_el_humo():
    """Cambio que solo toca comentarios: no repara nada y se hace pasar por reparacion."""
    r = _revisor()
    propuesta = {
        "archivo": "x.py",
        "texto_viejo": "def f():\n    # viejo\n    return 1\n",
        "texto_nuevo": "def f():\n    # nuevo comentario\n    return 1\n",
    }
    fallos = r.revisar(propuesta, tarea="reparar f")
    assert fallos, "NO CAZO EL HUMO: el cambio solo toca comentarios y no repara nada"


def test_caza_que_no_hace_lo_que_se_pidio():
    """Se pide tocar una funcion y el cambio ni la menciona."""
    r = _revisor()
    propuesta = {
        "archivo": "x.py",
        "texto_viejo": "def otra():\n    return 1\n",
        "texto_nuevo": "def otra():\n    return 2\n",
    }
    fallos = r.revisar(propuesta, tarea="reparar la funcion calcular_precio")
    assert any("calcular_precio" in str(f) for f in fallos), (
        "NO CAZO que la propuesta no toca lo que el encargo pedia")


def test_caza_la_sintaxis_rota():
    """Si el archivo queda roto, no puede aplicarse."""
    r = _revisor()
    propuesta = {
        "archivo": "x.py",
        "texto_viejo": "def f():\n    return 1\n",
        "texto_nuevo": "def f(:\n    return 1\n",
    }
    assert r.revisar(propuesta, tarea="reparar f"), "NO CAZO que el codigo queda roto"


def test_deja_pasar_lo_bueno():
    """Un candado que frena lo legitimo ensena a ignorar todos los candados."""
    r = _revisor()
    propuesta = {
        "archivo": "x.py",
        "texto_viejo": "def calcular_precio(x):\n    return x\n",
        "texto_nuevo": "def calcular_precio(x):\n    return round(x * 1.19, 2)\n",
    }
    fallos = r.revisar(propuesta, tarea="que calcular_precio sume el impuesto")
    assert not fallos, (
        "FRENO EN FALSO una reparacion buena: %s. Un candado que frena lo legitimo es peor "
        "que no tenerlo, porque ensena a ignorarlos todos." % fallos)


def test_no_opina_solo_cuenta():
    """El programa NO juzga si la reparacion es buena idea: eso es juicio y le toca a la IA."""
    r = _revisor()
    assert hasattr(r, "revisar"), "el revisor tiene que ofrecer revisar(propuesta, tarea)"
    doc = (r.__doc__ or "").lower()
    assert "cuenta" in doc and "juicio" in doc, (
        "el revisor tiene que decir POR ESCRITO que solo hace cuentas y que el juicio sigue "
        "siendo del auditor de IA: el programa SE SUMA, NO SUSTITUYE")


def test_caza_lo_que_se_borra():
    """EL AGUJERO MEDIDO EL 2026-09-11: el revisor vigila que lo NUEVO este bien, pero NO
    vigila que lo VIEJO siga ahi.

    Asi desaparecio la puerta del jefe que coordina del DMM sin que nadie dijera nada: ni el
    revisor, ni el que aplica los cambios, ni el copista miran los borrados. Las 526 vigias
    siguieron verdes.

    Se EJECUTA el camino real (revisar). No se busca ninguna palabra dentro de ningun archivo:
    eso es lo que prohibe CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO.
    """
    r = _revisor()
    propuesta = {
        "archivo": "x.py",
        "texto_viejo": "def alfa():\n    return 1\n\n\ndef beta():\n    return 2\n\n\ndef gamma():\n    return 3\n",
        "texto_nuevo": "def alfa():\n    return 1\n\n\ndef beta():\n    return 2\n",
    }
    fallos = r.revisar(propuesta, tarea="tocar alfa")
    assert fallos, (
        "NO FRENO: el texto nuevo hace DESAPARECER la funcion gamma y el revisor no dijo nada. "
        "Ese es el agujero exacto por el que el 2026-09-11 se perdio la puerta del jefe que "
        "coordina, con las 526 vigias en verde.")
    assert any("gamma" in str(f) for f in fallos), (
        "FRENO, pero no dijo QUE se pierde. Avisar sin nombrar lo que desaparece no sirve: el "
        "nombre es lo unico que deja decidir si el borrado es querido o es un destrozo. "
        "Dijo: %s" % fallos)


def test_no_frena_por_rutas_ni_nombres_de_contexto(tmp_path):
    """Frenada en falso medida el 2026-09-13; la ruta de la herramienta y el nombre del plan
    frenaban rondas buenas."""
    r = _revisor()
    archivo = tmp_path / "vigia_de_prueba.py"
    archivo.write_text("import pytest\n\n\ndef test_uno():\n    assert True\n", encoding="utf-8")
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "import pytest\n",
        "texto_nuevo": "import pytest\nimport os\n",
    }
    tarea = (
        "en la carpeta C:\\Ingeniero_VUC, segun PLAN_DE_RAIZ_2026-09-13.md, anadir import os; "
        "hoy falla test_vigia_otra_de_contexto y lo cuida candado_de_contexto")
    fallos = r.revisar(propuesta, tarea=tarea)
    assert not any("NO HACE LO QUE SE PIDIO" in str(f) for f in fallos), (
        "Freno en falso por palabras de contexto que no estan en el archivo; un candado que "
        "frena lo legitimo ensena a ignorarlos todos. Dijo: %s" % fallos)


def test_sigue_cazando_lo_que_esta_en_el_archivo(tmp_path):
    """Debe quedar verde tras la cura: lo que SI esta en el archivo se sigue cazando."""
    r = _revisor()
    archivo = tmp_path / "precios_de_prueba.py"
    archivo.write_text(
        "def calcular_precio(x):\n    return x\n\n\ndef otra():\n    return 1\n",
        encoding="utf-8")
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "def otra():\n    return 1\n",
        "texto_nuevo": "def otra():\n    return 2\n",
    }
    fallos = r.revisar(propuesta, tarea="reparar la funcion calcular_precio")
    assert any("calcular_precio" in str(f) for f in fallos), (
        "Se pidio tocar una funcion que SI esta en el archivo y el cambio ni la menciona; eso "
        "hay que seguir cazandolo")
