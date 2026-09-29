import os
import sys
import inspect

# La carpeta vigias esta un nivel por debajo de la raiz del proyecto.
# Se mete la raiz en sys.path para poder importar cuerpo.capataz.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

import cuerpo.capataz as capataz


class _ProcesoFalso(object):
    """Lo minimo que la funcion mira de un proceso lanzado.

    Si la funcion se queda esperando a que termine, este falso le contesta
    que ya termino bien para que la prueba no se cuelgue.
    """

    def __init__(self):
        self.returncode = 0
        self.pid = 12345

    def wait(self, timeout=None):
        return 0

    def poll(self):
        return 0

    def communicate(self, input=None, timeout=None):
        return (b"", b"")

    def kill(self):
        return None

    def terminate(self):
        return None


class _LanzadorFalso(object):
    """Sustituye a subprocess.Popen dentro de capataz.

    No lanza nada: solo apunta con que argumentos lo llamaron, en particular
    el sitio de trabajo (cwd).
    """

    def __init__(self):
        self.llamadas = []

    def __call__(self, *args, **kwargs):
        self.llamadas.append({"args": args, "kwargs": kwargs})
        return _ProcesoFalso()

    @property
    def ultima(self):
        if not self.llamadas:
            return None
        return self.llamadas[-1]


def _preparar(monkeypatch):
    """Monta el falso y devuelve (lanzador, orden minima)."""
    lanzador = _LanzadorFalso()
    monkeypatch.setattr(capataz.subprocess, "Popen", lanzador)
    orden = {
        "encargo": "una tarea de prueba que no se lanza de verdad",
        "pasos": [],
    }
    return lanzador, orden


def _cwd_de_la_llamada(lanzador):
    """Saca el cwd con que se llamo al lanzador, o None si no hubo llamada."""
    ultima = lanzador.ultima
    if ultima is None:
        return None
    if "cwd" in ultima["kwargs"]:
        return ultima["kwargs"]["cwd"]
    # Por si acaso lo pasaron posicional: Popen(comando, cwd, ...)
    if len(ultima["args"]) >= 2:
        return ultima["args"][1]
    return None


def test_lanzar_al_equipo_acepta_carpeta():
    """La funcion todavia no acepta el parametro carpeta: esta prueba nace roja."""
    firma = inspect.signature(capataz.lanzar_al_equipo)
    assert "carpeta" in firma.parameters, (
        "lanzar_al_equipo TODAVIA NO ACEPTA el parametro 'carpeta'. "
        "Sin ese parametro la tarea no puede trabajar en su propia carpeta "
        "y dos tareas a la vez se pisan el trabajo a medias. "
        "Firma actual: %s" % str(firma)
    )


def test_con_carpeta_trabaja_dentro_de_esa_carpeta(monkeypatch, tmp_path):
    """Con carpeta: el trabajo se lanza DENTRO de esa carpeta."""
    lanzador, orden = _preparar(monkeypatch)
    carpeta = str(tmp_path)

    try:
        capataz.lanzar_al_equipo("proyecto_de_prueba", orden, carpeta=carpeta)
    except TypeError as exc:
        raise AssertionError(
            "lanzar_al_equipo no acepta todavia el parametro 'carpeta': %s" % exc
        )
    except Exception as exc:
        raise AssertionError(
            "El montaje de la prueba reviento al llamar a lanzar_al_equipo: %r" % exc
        )

    assert lanzador.llamadas, (
        "No se llamo al lanzador de procesos: la funcion no lanzo nada."
    )
    cwd = _cwd_de_la_llamada(lanzador)
    assert cwd == carpeta, (
        "Con carpeta, el trabajo debe lanzarse DENTRO de esa carpeta. "
        "Se esperaba cwd=%r y se obtuvo cwd=%r." % (carpeta, cwd)
    )


def test_sin_carpeta_trabaja_en_la_carpeta_principal(monkeypatch):
    """Sin carpeta: todo sigue igual que hoy, en la carpeta principal."""
    lanzador, orden = _preparar(monkeypatch)

    try:
        capataz.lanzar_al_equipo("proyecto_de_prueba", orden)
    except TypeError as exc:
        raise AssertionError(
            "lanzar_al_equipo no acepta todavia el parametro 'carpeta': %s" % exc
        )
    except Exception as exc:
        raise AssertionError(
            "El montaje de la prueba reviento al llamar a lanzar_al_equipo: %r" % exc
        )

    assert lanzador.llamadas, (
        "No se llamo al lanzador de procesos: la funcion no lanzo nada."
    )
    cwd = _cwd_de_la_llamada(lanzador)
    raiz_esperada = os.path.dirname(os.path.dirname(os.path.abspath(capataz.__file__)))
    assert cwd == raiz_esperada, (
        "Sin carpeta, el trabajo debe lanzarse en la carpeta principal. "
        "Se esperaba cwd=%r y se obtuvo cwd=%r." % (raiz_esperada, cwd)
    )
