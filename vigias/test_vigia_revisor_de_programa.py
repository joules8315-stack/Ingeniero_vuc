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
