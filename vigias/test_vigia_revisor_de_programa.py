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


def test_no_acusa_nombres_importados_mas_arriba(tmp_path):
    """NACE ROJA: el revisor mira solo el trozo nuevo y acusa de NO EXISTE a nombres que si
    estan importados mas arriba en el archivo. Asi freno una ronda buena diciendo que os y sys
    no existian."""
    r = _revisor()
    archivo = tmp_path / "con_imports.py"
    archivo.write_text("import os\nimport sys\n\n\ndef f():\n    return 1\n", encoding="utf-8")
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "def f():\n    return 1\n",
        "texto_nuevo": "def f():\n    return os.path.join('a', sys.argv[0])\n",
    }
    fallos = r.revisar(propuesta, tarea="que f use la ruta")
    assert not any("NO EXISTE" in str(f) for f in fallos), (
        "Acuso de no existir nombres que estan importados mas arriba en el archivo; asi frena "
        "trabajo bueno. Dijo: %s" % fallos)


def test_sigue_cazando_un_nombre_que_no_esta_en_ningun_sitio(tmp_path):
    """Debe seguir verde: un nombre que no se importa en ningun sitio del archivo tiene que
    seguir siendo cazado, porque en cuanto se corra revienta."""
    r = _revisor()
    archivo = tmp_path / "sin_re.py"
    archivo.write_text("import os\n\n\ndef f(t):\n    return t\n", encoding="utf-8")
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "def f(t):\n    return t\n",
        "texto_nuevo": "def f(t):\n    return re.sub('a', 'b', t)\n",
    }
    fallos = r.revisar(propuesta, tarea="que f cambie letras")
    assert any("re" in str(f) and "NO EXISTE" in str(f) for f in fallos), (
        "Dejo pasar un nombre que no se importa en ningun sitio del archivo; en cuanto se corra, "
        "revienta")


def test_crear_un_archivo_nuevo_no_frena_por_palabras_de_contexto(tmp_path):
    r = _revisor()
    nuevo_archivo = tmp_path / "vigia_nueva_que_no_existe.py"
    propuesta = {
        "archivo": str(nuevo_archivo),
        "texto_viejo": "",
        "texto_nuevo": "def test_algo():\n    assert 1 == 1\n",
    }
    tarea = ("Crear la vigia nueva. Hoy el guardia hace subprocess.run con capture_output y "
             "timeout_largo, y la funcion _vigias devuelve paso y mensaje.")
    fallos = r.revisar(propuesta, tarea=tarea)
    assert not any("NO HACE LO QUE SE PIDIO" in str(f) for f in fallos), (
        "Freno la creacion de un archivo nuevo por palabras que el encargo solo usa para contar "
        "como esta hoy otro archivo; asi se tiran rondas buenas ya aprobadas. Dijo: " + str(fallos))


def test_no_acusa_de_roto_un_trozo_que_acaba_donde_empieza_la_funcion_siguiente(tmp_path):
    """NACE ROJA (2026-09-14): el trozo suelto parece incompleto, pero el archivo completo queda bien."""
    r = _revisor()
    archivo = tmp_path / "con_dos_funciones.py"
    archivo.write_text("def a():\n    return 1\n\n\ndef b():\n    return 2\n", encoding="utf-8")
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "def b():",
        "texto_nuevo": "def c():\n    return 3\n\n\ndef b():",
    }
    fallos = r.revisar(propuesta, tarea="anadir la funcion c antes de b")
    assert not any("QUEDA ROTO" in str(f) for f in fallos), (
        "Acuso de roto un trozo que dentro del archivo completo queda bien; asi se tiro una "
        "reparacion ya aprobada el 2026-09-14. Dijo: " + str(fallos))


def test_sigue_cazando_un_archivo_que_de_verdad_queda_roto(tmp_path):
    """Debe seguir verde: si el archivo completo queda roto, se frena."""
    r = _revisor()
    archivo = tmp_path / "se_rompe.py"
    archivo.write_text("def a():\n    return 1\n", encoding="utf-8")
    propuesta = {
        "archivo": str(archivo),
        "texto_viejo": "    return 1\n",
        "texto_nuevo": "    return (1\n",
    }
    fallos = r.revisar(propuesta, tarea="cambiar lo que devuelve a")
    assert any("QUEDA ROTO" in str(f) for f in fallos), (
        "Dejo pasar un cambio que deja el archivo completo roto; en cuanto se corra, revienta. Dijo: " + str(fallos))
