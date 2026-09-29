import os
import sys
import types

import pytest


# Arranque: meter en sys.path la carpeta un nivel arriba de vigias/ y la carpeta arnes/,
# porque la pieza del guardado importa a sus vecinas por nombre suelto.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")
for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


class _ResultadoFalso:
    """Imita lo que devuelve bateria_en_paralelo.correr: returncode, stdout, stderr."""

    def __init__(self, returncode, stdout, stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


# Salida que imita una corrida cortada por tiempo: hay un grupo cortado, el ultimo
# renglon es el resumen con cortados > 0, y NO hay ningun renglon FAILED ni ERROR.
SALIDA_CORTADA = (
    "bateria en paralelo: grupo cortado por tiempo: vigias/test_lento.py\n"
    "bateria en paralelo: grupo cortado por tiempo: vigias/test_mas_lento.py\n"
    "bateria en paralelo: 4 grupos, 0 rojos, 2 cortados por tiempo\n"
)


def _bateria_falsa(monkeypatch, modulo_guardia):
    """Sustituye la bateria SOLO dentro de la pieza del guardado.

    Se falsea unicamente el modulo bateria_en_paralelo tal como lo ve el guardado.
    No se lanzan procesos reales.
    """
    falso = types.ModuleType("bateria_en_paralelo")

    def correr(raiz, objetivo, procesos=4, tope=600, env=None, correr_uno=None):
        return _ResultadoFalso(returncode=1, stdout=SALIDA_CORTADA, stderr="")

    falso.correr = correr
    monkeypatch.setitem(sys.modules, "bateria_en_paralelo", falso)
    # Por si el guardado ya lo tenia importado como atributo del modulo.
    if hasattr(modulo_guardia, "bateria_en_paralelo"):
        monkeypatch.setattr(modulo_guardia, "bateria_en_paralelo", falso, raising=False)


def _vecinas_falsas(monkeypatch, modulo_guardia):
    """Si el guardado consulta vecinas, que devuelva la carpeta entera (TODAS).

    Solo se falsea si el modulo realmente expone algo de vecinas; no se inventan
    nombres de funciones que el material no trae.
    """
    for nombre in ("vecinas", "_vecinas"):
        if hasattr(modulo_guardia, nombre):
            falso = types.ModuleType("vecinas")

            def elegir(raiz, *a, **k):
                return None  # None significa correr TODAS

            falso.elegir = elegir
            monkeypatch.setattr(modulo_guardia, nombre, falso, raising=False)
            return


def test_guardado_frena_y_dice_que_no_pudo_terminar_por_tiempo(tmp_path, monkeypatch):
    """Cuando la bateria se corta por tiempo, el guardado debe FRENAR y explicar
    que no pudo TERMINAR de comprobar por tiempo.

    Hoy sale ROJA: el mensaje que devuelve es el resumen de grupos, que no explica
    que no se pudo terminar de comprobar.
    """
    # Importar la pieza que se prueba DENTRO de la prueba.
    import guardia_de_guardado as modulo_guardia

    # Carpeta raiz con una carpeta de vigias dentro, para no salir por el camino
    # de "no hay vigias".
    raiz = tmp_path / "proyecto"
    vigias_dir = raiz / "vigias"
    vigias_dir.mkdir(parents=True)
    (vigias_dir / "test_algo.py").write_text("def test_algo():\n    assert True\n", encoding="utf-8")

    _bateria_falsa(monkeypatch, modulo_guardia)
    _vecinas_falsas(monkeypatch, modulo_guardia)

    paso, mensaje = modulo_guardia._vigias(str(raiz))

    # 1) Debe FRENAR.
    assert paso is False, (
        "el guardado debe frenar cuando la bateria se corta por tiempo; "
        "devolvio paso=%r mensaje=%r" % (paso, mensaje)
    )

    # 2) El mensaje debe explicar que NO se pudo TERMINAR de comprobar por tiempo.
    texto = (mensaje or "").lower()
    assert texto.strip(), "el mensaje no puede venir vacio"

    dice_tiempo = ("tiempo" in texto) or ("agoto" in texto) or ("agot" in texto)
    dice_no_termino = (
        ("no se pudo terminar" in texto)
        or ("no pudo terminar" in texto)
        or ("no se termino" in texto)
        or ("no termino" in texto)
        or ("sin terminar" in texto)
        or ("incomplet" in texto)
        or ("no se pudo comprobar" in texto)
        or ("no se pudo probar" in texto)
    )
    assert dice_tiempo and dice_no_termino, (
        "el mensaje debe decir que no se pudo TERMINAR de comprobar por tiempo; "
        "devolvio: %r" % (mensaje,)
    )

    # 3) No debe afirmar que se rompio algo que antes funcionaba.
    #    Se busca la afirmacion concreta, no la palabra suelta, para no tumbar
    #    un mensaje bueno que use la palabra en otro sentido.
    frases_de_rotura = (
        "se rompio",
        "se ha roto",
        "esta roto",
        "esta rota",
        "algo se rompio",
        "algo que antes funcionaba",
        "dejo de funcionar",
    )
    for frase in frases_de_rotura:
        assert frase not in texto, (
            "el mensaje no debe afirmar que se rompio algo que antes funcionaba; "
            "devolvio: %r" % (mensaje,)
        )

    # 4) Decir solo cuantos grupos quedaron cortados NO basta: el mensaje no puede
    #    ser unicamente el resumen de la bateria.
    resumen_solo = texto.strip().startswith("bateria en paralelo:") and (
        "grupo" in texto and "cortado" in texto and not dice_no_termino
    )
    assert not resumen_solo, (
        "el mensaje no puede ser solo el resumen de grupos; "
        "devolvio: %r" % (mensaje,)
    )
