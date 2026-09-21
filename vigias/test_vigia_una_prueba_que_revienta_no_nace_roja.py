"""Vigia: una prueba que revienta NO nace roja de verdad.

Vigila comprobar_pasos de cuerpo/capataz.py en el caso de las ordenes que
traen entrega_la_prueba == 'si'.

La ley que manda aqui (CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO): una prueba
que nace ROJA solo vale si el rojo viene de una comprobacion suya que no se
cumplio (AssertionError). Si el rojo viene de un reventon (AttributeError,
ImportError, error de recogida, etc.) la prueba NO esta midiendo nada y el
paso falla. Verde sigue sin valer.

Tres casos:
  1) rojo por AssertionError  -> el paso pasa (devuelve '')
  2) rojo por reventon        -> el paso falla (devuelve 'vigia_verde')
  3) verde                    -> el paso falla (devuelve 'vigia_verde')

Se usa monkeypatch sobre subprocess.run DENTRO de cuerpo/capataz.py para dar
la salida de pytest sin ejecutarlo de verdad.
"""

import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from cuerpo import capataz  # noqa: E402


# ---------------------------------------------------------------------------
# Utilidades de montaje
# ---------------------------------------------------------------------------

def _preparar_ronda(tmp_path, pieza):
    """Deja un trabajo APROBADO valido para que el paso 1 (ronda) NO corte.

    comprobar_pasos mira memoria/trabajos_del_equipo buscando un archivo cuyo
    nombre contenga el basename de la pieza y la palabra APROBADO, y exige que
    traiga 'obrero' y 'auditor' distintos. Sin esto, comprobar_pasos devuelve
    'ronda' antes de llegar a pytest y la vigia no mediria nada.
    """
    carpeta = tmp_path / 'memoria' / 'trabajos_del_equipo'
    carpeta.mkdir(parents=True, exist_ok=True)
    base = os.path.splitext(os.path.basename(pieza))[0]
    ruta = carpeta / (base + '_APROBADO.json')
    ruta.write_text(
        json.dumps({'obrero': 'obrero-1', 'auditor': 'auditor-2'}),
        encoding='utf-8',
    )
    return ruta


def _preparar_pieza(tmp_path, pieza):
    """Crea la pieza en disco y hace que otro .py la nombre por su modulo.

    Asi el paso 2 (aplicada) y el paso 2b (pieza_suelta) no cortan antes de
    llegar al paso 3 (vigia_verde), que es el que queremos medir.
    """
    ruta_pieza = tmp_path / pieza
    ruta_pieza.parent.mkdir(parents=True, exist_ok=True)
    ruta_pieza.write_text('# pieza de prueba\n', encoding='utf-8')
    modulo = os.path.splitext(os.path.basename(pieza))[0]
    otro = tmp_path / 'quien_la_nombra.py'
    otro.write_text('import ' + modulo + '\n', encoding='utf-8')
    return ruta_pieza


def _preparar_vigia(tmp_path, vigia):
    """Crea el archivo de la vigia para que os.path.isfile(ruta_vigia) sea True."""
    ruta_vigia = tmp_path / vigia
    ruta_vigia.parent.mkdir(parents=True, exist_ok=True)
    ruta_vigia.write_text('# vigia de prueba\n', encoding='utf-8')
    return ruta_vigia


def _montar(tmp_path, monkeypatch, salida_pytest, returncode_pytest):
    """Monta el escenario completo y devuelve la orden lista para comprobar_pasos.

    Parchea subprocess.run DENTRO de cuerpo/capataz.py para que la llamada a
    pytest devuelva la salida y el codigo que le pidamos, sin ejecutar nada.
    """
    pieza = 'cuerpo/pieza_de_prueba.py'
    vigia = 'vigias/test_vigia_de_prueba.py'

    _preparar_ronda(tmp_path, pieza)
    _preparar_pieza(tmp_path, pieza)
    _preparar_vigia(tmp_path, vigia)

    # Redirigimos la raiz que usa comprobar_pasos: se calcula como el abuelo
    # del archivo de capataz. Parcheamos os.path.abspath para que devuelva
    # una ruta dentro de tmp_path cuando le pasen el __file__ de capataz.
    ruta_falsa_capataz = str(tmp_path / 'cuerpo' / 'capataz.py')
    abspath_real = os.path.abspath

    def abspath_falso(ruta):
        if os.path.basename(str(ruta)) == 'capataz.py':
            return ruta_falsa_capataz
        return abspath_real(ruta)

    monkeypatch.setattr(capataz.os.path, 'abspath', abspath_falso)

    llamadas = []

    class ResultadoFalso:
        def __init__(self, returncode, stdout, stderr=''):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def run_falso(cmd, *args, **kwargs):
        llamadas.append(list(cmd) if isinstance(cmd, (list, tuple)) else cmd)
        texto = ' '.join(str(c) for c in cmd) if isinstance(cmd, (list, tuple)) else str(cmd)
        if 'pytest' in texto:
            return ResultadoFalso(returncode_pytest, salida_pytest)
        # Cualquier otra llamada (git, comando) no deberia ocurrir en este paso.
        return ResultadoFalso(0, '')

    monkeypatch.setattr(capataz.subprocess, 'run', run_falso)

    orden = {
        'id': 'orden-de-prueba',
        'pieza': pieza,
        'vigia': vigia,
        'entrega_la_prueba': 'si',
    }
    return orden, llamadas


# ---------------------------------------------------------------------------
# Caso 1: rojo por AssertionError -> el paso PASA
# ---------------------------------------------------------------------------

def test_rojo_por_assertion_error_vale(tmp_path, monkeypatch):
    """Una prueba que nace roja porque su comprobacion no se cumplio SI vale."""
    salida = (
        '============================= test session starts ==============================\n'
        'collected 1 item\n'
        '\n'
        'vigias/test_vigia_de_prueba.py F                                            [100%]\n'
        '\n'
        '=================================== FAILURES ===================================\n'
        '__________________________________ test_algo ___________________________________\n'
        '\n'
        '    def test_algo():\n'
        '>       assert 1 == 2\n'
        'E       assert 1 == 2\n'
        '\n'
        'vigias/test_vigia_de_prueba.py:3: AssertionError\n'
        '=========================== short test summary info ============================\n'
        'FAILED vigias/test_vigia_de_prueba.py::test_algo - assert 1 == 2\n'
        '============================== 1 failed in 0.01s ===============================\n'
    )
    orden, llamadas = _montar(tmp_path, monkeypatch, salida, returncode_pytest=1)

    resultado = capataz.comprobar_pasos(orden)

    assert resultado == '', (
        'rojo por AssertionError debe valer (paso superado), pero devolvio: '
        + repr(resultado)
    )
    assert any('pytest' in ' '.join(str(c) for c in l) for l in llamadas), (
        'no se llego a llamar a pytest: la vigia no midio el paso 3'
    )


# ---------------------------------------------------------------------------
# Caso 2: rojo por reventon -> el paso FALLA
# ---------------------------------------------------------------------------

def test_rojo_por_reventon_no_vale(tmp_path, monkeypatch):
    """Una prueba que revienta (AttributeError) NO nace roja de verdad: falla."""
    salida = (
        '============================= test session starts ==============================\n'
        'collected 1 item\n'
        '\n'
        'vigias/test_vigia_de_prueba.py F                                            [100%]\n'
        '\n'
        '=================================== FAILURES ===================================\n'
        '__________________________________ test_algo ___________________________________\n'
        '\n'
        '    def test_algo():\n'
        '>       algo.que_no_existe()\n'
        'E       AttributeError: module \'algo\' has no attribute \'que_no_existe\'\n'
        '\n'
        'vigias/test_vigia_de_prueba.py:3: AttributeError\n'
        '=========================== short test summary info ============================\n'
        'FAILED vigias/test_vigia_de_prueba.py::test_algo - AttributeError: module \'algo\' has no attribute \'que_no_existe\'\n'
        '============================== 1 failed in 0.01s ===============================\n'
    )
    orden, _ = _montar(tmp_path, monkeypatch, salida, returncode_pytest=1)

    resultado = capataz.comprobar_pasos(orden)

    assert resultado == 'vigia_verde', (
        'rojo por reventon NO debe valer: el paso tiene que fallar, pero devolvio: '
        + repr(resultado)
    )


def test_rojo_por_error_de_recogida_no_vale(tmp_path, monkeypatch):
    """Un error al recoger la prueba tampoco es un rojo de verdad: falla."""
    salida = (
        '============================= test session starts ==============================\n'
        'collected 0 items / 1 error\n'
        '\n'
        '==================================== ERRORS ====================================\n'
        '____________________ ERROR collecting vigias/test_vigia_de_prueba.py __________\n'
        'ImportError while importing test module\n'
        'E   ImportError: cannot import name \'algo\' from \'cuerpo.pieza_de_prueba\'\n'
        '=========================== short test summary info ============================\n'
        'ERROR vigias/test_vigia_de_prueba.py\n'
        '=============================== 1 error in 0.01s ===============================\n'
    )
    orden, _ = _montar(tmp_path, monkeypatch, salida, returncode_pytest=2)

    resultado = capataz.comprobar_pasos(orden)

    assert resultado == 'vigia_verde', (
        'un error de recogida NO es un rojo de verdad: el paso tiene que fallar, '
        'pero devolvio: ' + repr(resultado)
    )


# ---------------------------------------------------------------------------
# Caso 3: verde -> el paso FALLA
# ---------------------------------------------------------------------------

def test_verde_no_vale(tmp_path, monkeypatch):
    """Una prueba que ya pasa antes del cambio no demuestra nada: falla."""
    salida = (
        '============================= test session starts ==============================\n'
        'collected 1 item\n'
        '\n'
        'vigias/test_vigia_de_prueba.py .                                            [100%]\n'
        '\n'
        '============================== 1 passed in 0.01s ===============================\n'
    )
    orden, _ = _montar(tmp_path, monkeypatch, salida, returncode_pytest=0)

    resultado = capataz.comprobar_pasos(orden)

    assert resultado == 'vigia_verde', (
        'verde no vale: el paso tiene que fallar, pero devolvio: ' + repr(resultado)
    )
