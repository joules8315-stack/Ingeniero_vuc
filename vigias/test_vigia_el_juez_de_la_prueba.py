import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from arnes.juez_de_la_prueba import juzgar


PIEZA_ROTA = '''def suma(a, b):
    return a - b
'''

PIEZA_BUENA = '''def suma(a, b):
    return a + b
'''

PIEZA_MALA = '''def suma(a, b):
    return a * b
'''

PIEZA_BUENA_ORDEN_CAMBIADO = '''def suma(a, b):
    return b + a
'''

VIGIA = '''import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pieza


def test_suma_da_cinco():
    assert pieza.suma(2, 3) == 5
'''


def _armar_raiz(tmp_path):
    """Arma una raiz de mentira con una pieza rota y una vigia que nace roja."""
    raiz = tmp_path / "raiz"
    raiz.mkdir()
    (raiz / "pieza.py").write_text(PIEZA_ROTA, encoding="utf-8")
    carpeta_vigias = raiz / "vigias"
    carpeta_vigias.mkdir()
    (carpeta_vigias / "test_vigia_suma.py").write_text(VIGIA, encoding="utf-8")
    return raiz


def test_juzgar_arregla_de_verdad(tmp_path):
    """Si el juez no distingue un arreglo real, ninguna reparacion se puede dar por buena."""
    raiz = _armar_raiz(tmp_path)
    ruta_prueba = raiz / "vigias" / "test_vigia_suma.py"
    ruta_pieza = raiz / "pieza.py"

    resultado = juzgar(
        str(raiz),
        str(ruta_prueba),
        str(ruta_pieza),
        PIEZA_ROTA,
        PIEZA_BUENA,
    )

    assert resultado["ok"] is True, (
        "el juez no dio por bueno un arreglo real: si esto falla, ninguna reparacion "
        "verificada puede pasar y el arnes se queda ciego"
    )
    assert resultado["antes_roja"] is True, (
        "el juez no vio que la prueba nacia roja: sin eso no se sabe si el arreglo "
        "cambio algo o la prueba ya pasaba sola"
    )
    assert resultado["despues_verde"] is True, (
        "el juez no vio la prueba en verde tras el arreglo: si esto falla, un arreglo "
        "bueno se rechaza y se pierde el trabajo"
    )
    assert resultado["vuelve_roja"] is True, (
        "el juez no comprobo que al deshacer el arreglo la prueba vuelve a rojo: sin eso "
        "no se distingue un arreglo real de un texto que solo tapa el fallo"
    )

    texto_final = ruta_pieza.read_text(encoding="utf-8")
    assert texto_final == PIEZA_BUENA, (
        "el archivo no quedo con el texto nuevo: si esto falla, el juez dice que arreglo "
        "pero no dejo el arreglo escrito en el disco"
    )


def test_juzgar_no_da_por_bueno_si_ya_estaba_verde(tmp_path):
    """Si el juez no mira como estaba ANTES, cualquier cambio inutil pasa por reparacion."""
    raiz = _armar_raiz(tmp_path)
    ruta_prueba = raiz / "vigias" / "test_vigia_suma.py"
    ruta_pieza = raiz / "pieza.py"

    ruta_pieza.write_text(PIEZA_BUENA, encoding="utf-8")

    resultado = juzgar(
        str(raiz),
        str(ruta_prueba),
        str(ruta_pieza),
        PIEZA_BUENA,
        PIEZA_BUENA_ORDEN_CAMBIADO,
    )

    assert resultado["antes_roja"] is False, (
        "el juez no miro como estaba antes: la prueba ya estaba verde y el juez "
        "la dio por roja"
    )
    assert resultado["ok"] is False, (
        "asi se cuela como reparacion un cambio que no reparo nada: la prueba ya "
        "pasaba sola y el juez lo dio por bueno"
    )


def test_juzgar_no_arregla_nada(tmp_path):
    """Si el juez da por bueno un texto que no arregla, deja pasar reparaciones falsas."""
    raiz = _armar_raiz(tmp_path)
    ruta_prueba = raiz / "vigias" / "test_vigia_suma.py"
    ruta_pieza = raiz / "pieza.py"

    resultado = juzgar(
        str(raiz),
        str(ruta_prueba),
        str(ruta_pieza),
        PIEZA_ROTA,
        PIEZA_MALA,
    )

    assert resultado["ok"] is False, (
        "el juez dio por bueno un texto que no arregla nada: si esto falla, cualquier "
        "cambio que no toque el fallo se acepta como reparacion"
    )
    assert resultado["despues_verde"] is False, (
        "el juez vio la prueba en verde con un texto que no arregla: si esto falla, "
        "el juez confunde un cambio cualquiera con un arreglo real"
    )
