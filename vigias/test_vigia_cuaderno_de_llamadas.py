# -*- coding: utf-8 -*-
"""VIGIA — EL CUADERNO DE LLAMADAS: CUANDO UN CEREBRO FALLA, EL PROGRAMA LO REGISTRA.

CONTRATO_EL_EQUIPO_ESCRIBE, causa "propuesta vacia" (Julio, 2026-08-24):
   | Propuesta vacia | El cuaderno de llamadas dira si sigue pasando y cuando | pendiente |

LA LEY: "El cuaderno de llamadas dira si sigue pasando y cuando". Y en la MATRIZ:
   | El cuaderno de llamadas | Saber POR QUE falla cada una. Sin esto no se puede decidir nada.

LA MEDIDA QUE LA OBLIGA (2026-09-10, dos veces el mismo dia creando la vigia del DMM):
   OBRERO groq -> AUDITOR gemini4
     aviso  : GPT-OSS 20B (Groq) fallo (no es cuota): contesto vacio
     aviso  : GPT-OSS 20B (Groq) se agoto -> pasa el turno
     vueltas_dadas: 3  |  propuesta ILEGIBLE: el cerebro no devolvio JSON
El gratis se corta en la SALIDA al crear un archivo entero. Sin registro no se distingue
"vacio" de "cortado" de "roto": cada causa tiene su cura, y sin datos se decide a ciegas.

POR QUE ESTA VIGIA NO SE CONFORMA CON NOMBRES: `cuerpo/cuaderno.py` es un PROGRAMA puro
(sin IA). Si nadie lo llama, el cuaderno es un mueble. Se comprueba que el REPETIDOR
(cuerpo/obrero.py::_preguntar_con_relevo, el unico pasillo por donde pasa toda llamada)
le escribe de verdad, y que la escritura SUCEDE (se ve el archivo crecer), no que se nombre.

JULIO, 2026-09-10: "lo que no necesite cerebro, que lo haga un programa, presta atencion."
Esto ES un programa: registrar un fallo no necesita que ninguna IA opine.
"""
import json
import os
import re
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _vivo(src):
    """El codigo sin comentarios ni textos de documentacion: solo lo que se ejecuta."""
    src = re.sub(r'"""(?:.|\n)*?"""', " ", src)
    src = re.sub(r"'''(?:.|\n)*?'''", " ", src)
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in src.splitlines())


def test_el_relevo_real_escribe_en_el_cuaderno_siempre():
    """El pasillo no es un nombre: se mira _preguntar_con_relevo, donde pasan TODAS las llamadas."""
    from cuerpo import obrero
    import inspect
    src = _vivo(inspect.getsource(obrero._preguntar_con_relevo))
    assert "cuaderno.apuntar" in src, (
        "el relevo no escribe en el cuaderno. Sin registro no se sabe si el gratis contesto "
        "VACIO, se CORTÓ o devolvio JSON ROTO: cada causa tiene su cura y sin datos se decide "
        "a ciegas. El cuaderno existe (cuerpo/cuaderno.py) y es un PROGRAMA: falto enchufarlo.")


def test_el_cuaderno_apunta_la_causa_real_no_solo_que_fallo():
    """Un fallo SIN por que no sirve para decidir la cura. Justo lo que pide la ley."""
    from cuerpo import obrero
    import inspect
    src = _vivo(inspect.getsource(obrero._preguntar_con_relevo))
    for campo in ("resultado=", "cuaderno.OK", "cuaderno.VACIO", "cuaderno.ERROR",
                  "cuaderno.NO_CUPO"):
        assert campo in src, (
            "el relevo no registra el RESULTADO exacto de cada intento (%s). "
            "'contesto vacio' no es lo mismo que 'no le cupo' ni que 'JSON roto': "
            "cada causa tiene su cura." % campo)


def test_apuntar_escribe_una_linea_real_devuelta():
    """La escritura SUCEDE, no se supone. Se usa una copia de prueba, nunca el cuaderno real."""
    os.environ["INGENIERO_CUADERNO_TEST"] = os.path.join(
        os.path.dirname(__file__), "_cuaderno_prueba.jsonl")
    try:
        from cuerpo import cuaderno
        cuaderno.apuntar("prueba", tamano=1234, vuelta=2, clase="crear",
                         resultado=cuaderno.VACIO, crudo="texto de prueba")
        filas = [json.loads(ln) for ln in open(cuaderno._ruta(), encoding="utf-8") if ln.strip()]
        assert filas, "el cuaderno no escribio nada: apuntar no esta guardando"
        ult = filas[-1]
        assert ult["quien"] == "prueba"
        assert ult["tamano"] == 1234
        assert ult["vuelta"] == 2
        assert ult["clase"] == "crear"
        assert ult["resultado"] == cuaderno.VACIO
    finally:
        try:
            os.remove(cuaderno._ruta())
        except Exception:
            pass
        os.environ.pop("INGENIERO_CUADERNO_TEST", None)


def test_el_cuaderno_no_rompe_si_falla_el_disco():
    """Apuntar es complemento del trabajo, jamas su verdugo: si el disco falla, calla."""
    os.environ["INGENIERO_CUADERNO_TEST"] = r"Z:\carpeta_que_no_existe\cuaderno.jsonl"
    try:
        from cuerpo import cuaderno
        assert cuaderno.apuntar("x", tamano=1, resultado=cuaderno.OK) is None
    finally:
        os.environ.pop("INGENIERO_CUADERNO_TEST", None)


def test_el_reloj_anota_los_segundos(tmp_path, monkeypatch):
    """El reloj del cuaderno guarda los segundos redondeados, y solo si se midieron."""
    monkeypatch.setenv("INGENIERO_CUADERNO_TEST", str(tmp_path / "c.jsonl"))
    from cuerpo import cuaderno
    cuaderno.apuntar("deepseek", resultado=cuaderno.OK, segundos=2.345)
    cuaderno.apuntar("groq")
    lineas = [json.loads(l) for l in (tmp_path / "c.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert lineas[0]["segundos"] == 2.3
    assert "segundos" not in lineas[1]