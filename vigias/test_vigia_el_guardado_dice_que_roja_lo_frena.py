# -*- coding: utf-8 -*-
"""VIGIA — EL GUARDADO DICE QUE ROJA LO FRENA (2026-09-29).

Cuando el guardado frena porque hay una prueba roja que YA estaba guardada, el mensaje
que ve la maquina tiene que decir EL NOMBRE de esa prueba. Hoy no lo dice: devuelve el
renglon de resumen de la bateria, que solo cuenta grupos, y por eso se han tirado
trabajos ya aprobados sin saber que los frenaba.

Hecho medido hoy, 2026-09-29: la bateria completa (556,3 s, 24 archivos rojos) frenaba
UNA SOLA, vigias/test_vigia_memoria_completa.py, y el mensaje que veia la maquina era,
tal cual:
    bateria en paralelo: 4 grupos, 4 rojos, 0 cortados por tiempo
El nombre nunca aparecia por ningun lado.

Esta prueba NACE ROJA A PROPOSITO: el arreglo entra en otra ronda. Aqui solo se mide.
"""

import os
import sys

import pytest


# La pieza del guardado importa a sus vecinas por nombre suelto, asi que hay que dejar
# en sys.path la carpeta que esta un nivel arriba de vigias y tambien la carpeta arnes.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_DEL_PROYECTO = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ_DEL_PROYECTO, "arnes")
for _ruta in (RAIZ_DEL_PROYECTO, ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


class _ResultadoFalso:
    """Lo minimo que el guardado mira de una corrida: returncode, stdout y stderr."""

    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class _BateriaFalsa:
    """Bateria de mentira: devuelve una salida con un archivo rojo y su renglon de resumen."""

    def __init__(self, salida):
        self._salida = salida

    def correr(self, *args, **kwargs):
        return _ResultadoFalso(1, stdout=self._salida, stderr="")


def test_el_guardado_dice_que_roja_lo_frena(tmp_path, monkeypatch):
    """Si frena por una roja ya guardada, el mensaje tiene que nombrarla.

    Montaje, todo falseado dentro de la pieza del guardado y nada mas:
      1. La bateria, por una falsa cuyo correr devuelve returncode 1 y un stdout con
         el archivo rojo y, como ultimo renglon, el resumen de la bateria.
      2. La eleccion de vecinas, para que devuelva la carpeta entera de vigias.
      3. subprocess.run dentro de la pieza, para que diga que el archivo YA estaba
         guardado (returncode 0).
    La raiz es una carpeta temporal de pytest con una carpeta vigias dentro, para no
    leer la lista de ordenes ni la foto de rojas conocidas del proyecto de verdad.
    """
    import guardia_de_guardado

    # 1. La bateria falsa: un archivo rojo y el renglon de resumen como ultimo renglon.
    #    La pieza hace `import bateria_en_paralelo` DENTRO de _vigias, asi que el falso
    #    tiene que estar en sys.modules con esa clave, no como atributo de la pieza.
    salida = (
        "FAILED vigias/test_vigia_la_que_frena.py::test_algo\n"
        "bateria en paralelo: 1 grupos, 1 rojos, 0 cortados por tiempo\n"
    )
    monkeypatch.setitem(sys.modules, "bateria_en_paralelo", _BateriaFalsa(salida))

    # 2. Las vecinas: la carpeta entera de vigias, para no salir por el camino de
    #    "solo cambiaron documentos". La pieza hace `vecinas.elegir(raiz)` con vecinas
    #    importado por nombre suelto dentro de _vigias, asi que va en sys.modules.
    class _VecinasFalsas:
        def elegir(self, raiz):
            return ["vigias/"]

    monkeypatch.setitem(sys.modules, "vecinas", _VecinasFalsas())

    # 3. git dice que el archivo YA estaba guardado: returncode 0, sin salida.
    def _run_falso(*args, **kwargs):
        return _ResultadoFalso(0, stdout="", stderr="")

    monkeypatch.setattr(guardia_de_guardado.subprocess, "run", _run_falso)

    # 4. Raiz temporal con una carpeta vigias dentro: nada del estado real del proyecto.
    raiz = tmp_path
    os.makedirs(os.path.join(str(raiz), "vigias"), exist_ok=True)

    deja_pasar, mensaje = guardia_de_guardado._vigias(str(raiz))

    # a) Frena.
    assert deja_pasar is False, (
        "el guardado tenia que frenar por una roja ya guardada, y dejo pasar: %r" % (mensaje,)
    )

    # b) El mensaje nombra la prueba que frena.
    assert "test_vigia_la_que_frena.py" in mensaje, (
        "el mensaje del guardado no dice el nombre de la prueba que lo frena; "
        "mensaje devuelto: %r" % (mensaje,)
    )
