import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# SE CARGA POR SU SITIO, NO POR SU NOMBRE.
#
# CHOQUE DE NOMBRES, ya cazado el 2026-09-11 y documentado en la vigia de la lista blanca: en esta
# casa hay DOS cosas llamadas igual, la carpeta skills/ y el archivo cuerpo/skills.py. Cuando otra
# prueba carga el archivo, el nombre queda ocupado y "from skills.algo import ..." deja de
# encontrar nada. Esta vigia nacio con ese import y no fallaba ella sola: TUMBABA LA SUITE ENTERA
# al recogerla, que es mucho peor que una roja.
#
# Cargando por la RUTA no hay confusion posible, y la prueba deja de depender del orden en que
# corran las demas. Una vigia que cambia de color segun quien corra antes no vigila nada.
#
# NO SE TIRO NADA DEL TRABAJO DEL EQUIPO: se repara la linea de carga y se conserva todo lo demas.
import importlib.util as _importlib_util

_RUTA_PIEZA = os.path.join(AQUI, "skills", "rechazo_comprobado.py")
if not os.path.exists(_RUTA_PIEZA):
    import pytest as _pytest
    _pytest.skip(
        "NO EXISTE skills/rechazo_comprobado.py. Sin el, un auditor puede seguir tirando trabajo "
        "ya pagado inventandose los defectos, como paso dos veces el 2026-09-12.",
        allow_module_level=True)
_spec = _importlib_util.spec_from_file_location("rechazo_comprobado_por_su_sitio", _RUTA_PIEZA)
_modulo = _importlib_util.module_from_spec(_spec)
_spec.loader.exec_module(_modulo)
se_sostiene = _modulo.se_sostiene


# Texto de mentira que SI tiene el decorador y NO tiene la palabra CORREO.
# Es el caso real del 2026-09-12: el auditor dijo que faltaba el decorador
# y que existia la linea <CORREO>, y las dos cosas eran mentira.
TEXTO_CON_DECORADOR = (
    "import pytest\n"
    "\n"
    "\n"
    "@pytest.fixture\n"
    "def _libreta_de_mentira():\n"
    "    return {}\n"
)

# Texto de mentira que de verdad NO tiene el decorador.
TEXTO_SIN_DECORADOR = (
    "def _libreta_de_mentira():\n"
    "    return {}\n"
)

# Texto de mentira que de verdad tiene un error de sintaxis.
TEXTO_ROTO = (
    "def algo(:\n"
    "    return 1\n"
)


FALLO_DECORADOR = (
    "Falta el decorador @pytest.fixture encima de la funcion _libreta_de_mentira"
)
FALLO_CORREO = (
    "Existe la linea literal <CORREO> que no es codigo Python valido y provoca error de sintaxis"
)


def test_caza_el_rechazo_del_2026_09_12():
    """El caso real que costo dinero: las dos acusaciones son falsas.

    El texto SI trae @pytest.fixture y NO trae la palabra CORREO, asi que
    ninguna de las dos acusaciones se sostiene contra el texto de verdad.
    """
    fallos = [FALLO_DECORADOR, FALLO_CORREO]
    se_mantiene, explicacion = se_sostiene(TEXTO_CON_DECORADOR, fallos)
    assert se_mantiene is False, (
        "El auditor acuso de que faltaba el decorador @pytest.fixture y de que "
        "existia la palabra CORREO, pero el texto SI tiene el decorador y NO "
        "tiene CORREO. Las dos acusaciones son falsas, asi que el rechazo no "
        "se sostiene y se_sostiene debe devolver falso. Explicacion dada: "
        + repr(explicacion)
    )


def test_un_rechazo_de_verdad_SIGUE_valiendo():
    """Un rechazo verdadero no se puede tapar.

    El texto de verdad NO tiene @pytest.fixture, asi que la acusacion de que
    falta SI se sostiene y se_sostiene debe devolver verdadero. Si esta prueba
    falla, la reparacion seria peor que el fallo: entraria codigo malo.
    """
    fallos = [FALLO_DECORADOR]
    se_mantiene, explicacion = se_sostiene(TEXTO_SIN_DECORADOR, fallos)
    assert se_mantiene is True, (
        "El texto de verdad NO tiene @pytest.fixture, asi que la acusacion de "
        "que falta es cierta y el rechazo debe seguir valiendo. Se esperaba "
        "verdadero y llego falso. Explicacion dada: " + repr(explicacion)
    )


def test_si_no_se_entiende_la_acusacion_manda_el_auditor():
    """Ante la duda no se contradice al auditor.

    La frase no encaja en ningun molde comprobable, asi que se da por buena
    y se_sostiene debe devolver verdadero.
    """
    fallos = ["el diseno no me convence"]
    se_mantiene, explicacion = se_sostiene(TEXTO_CON_DECORADOR, fallos)
    assert se_mantiene is True, (
        "La acusacion 'el diseno no me convence' no se puede comprobar con un "
        "programa gratis, asi que ante la duda manda el auditor y el rechazo "
        "debe darse por bueno. Se esperaba verdadero y llego falso. "
        "Explicacion dada: " + repr(explicacion)
    )


def test_lo_que_no_compila_de_verdad_se_rechaza():
    """Si el texto de verdad no compila, el rechazo se sostiene.

    El texto tiene un error de sintaxis real, asi que la acusacion de error
    de sintaxis es cierta y se_sostiene debe devolver verdadero.
    """
    fallos = ["error de sintaxis"]
    se_mantiene, explicacion = se_sostiene(TEXTO_ROTO, fallos)
    assert se_mantiene is True, (
        "El texto de verdad tiene un error de sintaxis, asi que la acusacion "
        "de error de sintaxis es cierta y el rechazo debe seguir valiendo. "
        "Se esperaba verdadero y llego falso. Explicacion dada: "
        + repr(explicacion)
    )
