"""Vigia: antes de pagar una revision, el archivo cambiado tiene que CARGAR.

Caso real 2026-09-19: un decorador @contextlib.contextmanager a nivel de modulo con
'import contextlib' solo DENTRO de la funcion dejo arnes/candado_equipo.py sin cargar
y se guardo igual. Esta vigia nace roja: prueba no_carga(contenido) de
arnes/revisor_de_programa.py, que devuelve la lista de lo que impide cargar el modulo
(vacia = carga).
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, 'arnes'))
import revisor_de_programa as r


# (1) EL CASO REAL: el decorador usa contextlib a nivel de modulo, pero el import
# esta solo DENTRO de la funcion. Al cargar el modulo, el decorador revienta.
CASO_REAL = (
    'import os\n'
    '\n'
    '@contextlib.contextmanager\n'
    'def f():\n'
    '    import contextlib\n'
    '    yield\n'
)


def test_el_caso_real_del_decorador_sin_import_frena():
    fallos = r.no_carga(CASO_REAL)
    assert isinstance(fallos, list)
    assert fallos, 'el decorador sin import arriba tiene que frenar'
    assert any('contextlib' in str(f) for f in fallos), \
        'algun texto tiene que mencionar contextlib'


def test_con_el_import_arriba_carga():
    contenido = (
        'import contextlib\n'
        '\n'
        '@contextlib.contextmanager\n'
        'def f():\n'
        '    yield\n'
    )
    assert r.no_carga(contenido) == []


def test_un_error_de_sintaxis_frena():
    assert r.no_carga('def f(:\n    pass\n')


def test_un_nombre_usado_dentro_de_una_funcion_no_cuenta():
    # zzz no esta definido, pero solo se usa al LLAMAR a f, no al cargar el modulo.
    assert r.no_carga('def f():\n    return zzz\n') == []


def test_los_nombres_del_modulo_y_de_python_cuentan():
    contenido = (
        'X = 1\n'
        'Y = X + len([])\n'
        'class A(Exception):\n'
        '    pass\n'
    )
    assert r.no_carga(contenido) == []


def test_los_importados_y_los_del_for_cuentan():
    contenido = (
        'from m import a, b as c\n'
        'for i in []:\n'
        '    pass\n'
    )
    assert r.no_carga(contenido) == []
