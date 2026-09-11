# -*- coding: utf-8 -*-
"""conftest.py — NINGUNA COMPROBACION TOCA EL ESTADO DE VERDAD (ley 23, 2026-08-21).

LEY 23: "una comprobacion que falla a veces es peor que ninguna". Ya se curo dos veces por lo
mismo —la memoria de errores y el registro de apagones— y volvio a pasar por un tercer sitio: la
marca de "hilo perdido" era un archivo COMPARTIDO. Una comprobacion la ponia y otra, corriendo a
la vez, se la encontraba puesta: el candado de edicion bloqueaba un contrato que debe poder
escribirse siempre. Sola, verde; en tanda, roja. Rojo falso, y un rojo falso ensena a ignorar los
rojos, que es exactamente como se cuela un rojo de verdad.

La cura no es arreglar el sitio numero tres: es que NINGUNA comprobacion vea nunca el estado real.
Cada prueba trabaja sobre su propia copia, y la copia se va con ella. Vale tambien para los
programas que la prueba lanza aparte, porque heredan estas variables.
"""
import os
import sys
import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


@pytest.fixture(autouse=True)
def _nada_toca_lo_real(tmp_path, monkeypatch):
    """Cada prueba, con su propia copia. Se hereda a los programas que la prueba lance."""
    monkeypatch.setenv("INGENIERO_CONTEXTO_TEST", str(tmp_path / ".contexto_perdido"))
    # LA CASA, DURANTE LAS PRUEBAS, ES LA CARPETA DE USAR Y TIRAR (2026-09-01).
    # Al cerrarle las puertas traseras, el candado de equipo empezo a vigilar el disco entero y
    # frenaba hasta los borradores. Se le acoto a vigilar solo lo que esta en casa... y entonces
    # las pruebas, que escriben en carpetas temporales, quedaron FUERA: el candado las ignoraba y
    # DIECIOCHO comprobaciones salieron verdes sin medir nada. Una verde que no mide es peor que
    # una roja, porque da falsa seguridad. Con esto, durante las pruebas su carpeta ES la casa.
    monkeypatch.setenv("INGENIERO_CASA_TEST", str(tmp_path))
    # El contador de bloqueos del protocolo: tras 2 bloqueos seguidos se abre una valvula de
    # escape para no atascar a Julio. Era compartido, asi que un bloqueo DE VERDAD dejaba la
    # valvula ya abierta y la comprobacion salia roja sin que nada estuviera roto (cuarto sitio
    # con este mismo patron, 2026-08-21).
    monkeypatch.setenv("INGENIERO_CONTADOR_TEST", str(tmp_path / ".protocolo_bloqueos"))
    # La AUTORIZACION de Julio (su llave) tambien es estado REAL: si la tiene puesta (24h), los
    # candados abren de verdad y las vigias que prueban que el candado MUERDE se pondrian rojas en
    # falso (creyendo que el candado fallo cuando en realidad la llave abrio, que es su trabajo).
    # Ley 23 + L15 (2026-08-27): ninguna comprobacion ve el estado real. Cada vigia apunta la
    # autorizacion a su propia copia que no existe, asi prueba que el candado muerde SIN llave,
    # y la llave real de Julio deja de causar rojos falsos. La llave real sigue abriendo (no se toca).
    monkeypatch.setenv("INGENIERO_AUTORIZACION_TEST", str(tmp_path / ".aut_julio_no_existe"))
    # El cuaderno de guardar_veredicto se escribe con AQUI (la carpeta real del proyecto); se
    # desvia a la carpeta de mentira para que ninguna comprobacion ensucie el registro de verdad.
    import candado_equipo as ce
    monkeypatch.setattr(ce, "AQUI", str(tmp_path))
    # LOS CUADERNOS DE VERDAD NO SE TOCAN (2026-09-11, TERCERA vuelta del mismo fallo).
    #
    # MEDIDO ese dia: se tomo la huella de seis cuadernos, se corrieron los 661 guardianes sin
    # tocar nada mas, y CINCO DE SEIS habian cambiado. Las pruebas escribian en la memoria de
    # verdad, que es justo lo que esta casa tiene prohibido desde que costo 27 de 32 errores
    # aprendidos ("no volver a dejar que una prueba escriba en la memoria de verdad").
    #
    # Y ademas era la causa del GUARDIAN QUE SE MUERDE LA COLA: guardar hace correr a los
    # guardianes, los guardianes ensucian los cuadernos, y al terminar de guardar ya hay cosas
    # sin guardar. Se "curo" dos veces (31-ago y 02-sep) PERDONANDO los cuadernos en el candado
    # de guardar. Eso tapa el sintoma. Esto cierra el grifo.
    #
    # OJO CON LO QUE SALIO AL MIRARLO: dos de ellos (el cuaderno de llamadas y las pruebas
    # reales) YA TENIAN su puerta de desvio construida (INGENIERO_CUADERNO_TEST,
    # INGENIERO_PRUEBAS_TEST) y NADIE la habia enchufado nunca. Es la misma enfermedad de las
    # piezas dormidas: construida, con buena intencion, y sin conectar.
    import candado_diagnostico as _cd
    import candado_memoria as _cmem
    import candado_prueba_real as _cpr
    import candados_medicion as _cm
    from cuerpo import cuaderno as _cua
    monkeypatch.setenv("INGENIERO_APLICACIONES", str(tmp_path / "APLICACIONES.log"))
    monkeypatch.setenv("INGENIERO_CUADERNO_TEST", str(tmp_path / "CUADERNO_DE_LLAMADAS.jsonl"))
    monkeypatch.setenv("INGENIERO_PRUEBAS_TEST", str(tmp_path / "pruebas_real"))
    monkeypatch.setattr(_cua, "RUTA", str(tmp_path / "CUADERNO_DE_LLAMADAS.jsonl"))
    monkeypatch.setattr(_cm, "RUTA", str(tmp_path / "CANDADOS_MEDICION.json"))
    monkeypatch.setattr(_cd, "RUTA", str(tmp_path / "DIAGNOSTICO.json"))
    monkeypatch.setattr(_cmem, "AVISADOS", str(tmp_path / ".avisos_ya_dados.json"))
    monkeypatch.setattr(_cpr, "PRUEBAS", str(tmp_path / "pruebas_real"))
    yield
