# -*- coding: utf-8 -*-
"""vigias/test_vigia_ruta_de_acceso.py — SUPER VIGIA DE LA RUTA DE ACCESO.

Ley: CONTRATO_RUTA_DE_ACCESO.md (Julio, 2026-09-06):
  "Cuando pidas permiso debe haber una ruta clara de lo que se va a tocar, para que no toque
   nada mas, y esto lo define el plan. Una vez aprobado el plan, este debe tener todo lo que
   necesita acceso, y pedir acceso para eso unicamente."

Se comprueba lo que de verdad importa, no que el archivo exista:
  1. SIN plan aprobado, el candado NO estorba (si no, la herramienta quedaria inservible).
  2. CON plan aprobado, lo que esta en la lista PASA.
  3. CON plan aprobado, lo que NO esta en la lista SE FRENA.
  4. BLINDAJE: frena aunque los candados esten APAGADOS por autorizacion de Julio.
  5. No se cuela por el nombre suelto: 'cuotas.py' no abre 'otra/cuotas.py'.
  6. Una ruta CERRADA deja de mandar.
  7. Una ruta CADUCADA deja de mandar.
  8. El freno deja RASTRO: un candado que frena en silencio no se puede medir.
"""
import json
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import candado_ruta_de_acceso as cra  # noqa: E402

CANDADO = os.path.join(AQUI, "arnes", "candado_ruta_de_acceso.py")


def _pedir(archivo, ruta_test, apagados=False):
    """Corre el candado de verdad, como lo corre la herramienta. Devuelve el codigo de salida."""
    entorno = dict(os.environ)
    entorno["INGENIERO_RUTA_ACCESO_TEST"] = str(ruta_test)
    if apagados:
        # Se simula que Julio autorizo apagar los candados.
        entorno["INGENIERO_OFF"] = "1"
    peticion = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": archivo}})
    r = subprocess.run([sys.executable, CANDADO], input=peticion, capture_output=True,
                       text=True, encoding="utf-8", errors="ignore", env=entorno, timeout=60)
    return r.returncode, (r.stderr or "")


def _abrir_ruta(tmp_path, piezas, estado="abierta", desde=None):
    d = {"plan": "plan de prueba", "motivo": "vigia",
         "piezas": list(piezas), "estado": estado,
         "desde": time.time() if desde is None else desde}
    f = tmp_path / "RUTA_DE_ACCESO.json"
    f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return f


def test_sin_plan_no_estorba(tmp_path):
    """1. Sin plan aprobado no puede frenar nada: mandan los demas candados."""
    vacio = tmp_path / "no_existe.json"
    codigo, _ = _pedir(os.path.join(AQUI, "cualquier_cosa.py"), vacio)
    assert codigo == 0, "sin plan aprobado, la ruta de acceso no debe estorbar"


def test_lo_del_plan_pasa(tmp_path):
    """2. Lo que el plan declaro se puede tocar."""
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py", "arnes/medir_capacidad.py"])
    codigo, _ = _pedir(os.path.join(AQUI, "cuerpo", "cuotas.py"), f)
    assert codigo == 0, "lo que el plan declaro tiene que pasar"


def test_lo_de_fuera_se_frena(tmp_path):
    """3. Lo que el plan NO declaro se frena. Es el corazon de la ley."""
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py"])
    codigo, aviso = _pedir(os.path.join(AQUI, "cerebro", "router.py"), f)
    assert codigo == 2, "tocar fuera del plan tiene que frenarse"
    assert "RUTA DE ACCESO" in aviso
    assert "cuotas.py" in aviso, "el aviso debe DECIR que si se puede tocar"


def test_frena_aunque_los_candados_esten_apagados(tmp_path):
    """4. EL BLINDAJE. La autorizacion de Julio no es barra libre: es permiso para LO QUE EL
    PLAN DIJO. Sin esto, la ley del 2026-09-06 no sirve de nada."""
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py"])
    codigo, _ = _pedir(os.path.join(AQUI, "cerebro", "router.py"), f, apagados=True)
    assert codigo == 2, "con los candados apagados TAMBIEN se frena lo que el plan no incluye"


def test_no_se_cuela_por_el_nombre_suelto(tmp_path):
    """5. Se compara la RUTA, no el nombre: si no, un archivo con el mismo nombre en otra
    carpeta entraria de gorra."""
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py"])
    codigo, _ = _pedir(os.path.join(AQUI, "otra_carpeta", "cuotas.py"), f)
    assert codigo == 2, "el mismo nombre en otra carpeta NO esta permitido"


def test_una_ruta_cerrada_no_manda(tmp_path):
    """6. Terminado el plan, se cierra la ruta y vuelve el regimen normal."""
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py"], estado="cerrada")
    codigo, _ = _pedir(os.path.join(AQUI, "cerebro", "router.py"), f)
    assert codigo == 0, "una ruta cerrada no puede seguir mandando"


def test_una_ruta_caducada_no_manda(tmp_path):
    """7. Un plan olvidado no puede bloquear la casa para siempre."""
    viejo = time.time() - (cra.VIGENCIA_H + 5) * 3600
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py"], desde=viejo)
    codigo, _ = _pedir(os.path.join(AQUI, "cerebro", "router.py"), f)
    assert codigo == 0, "una ruta caducada no puede seguir mandando"


def test_el_freno_deja_rastro(tmp_path):
    """8. Frenar en silencio es lo mismo que no medir. Tiene que quedar apuntado."""
    f = _abrir_ruta(tmp_path, ["cuerpo/cuotas.py"])
    antes = os.path.getsize(cra.CUADERNO) if os.path.exists(cra.CUADERNO) else 0
    _pedir(os.path.join(AQUI, "cerebro", "router.py"), f)
    despues = os.path.getsize(cra.CUADERNO) if os.path.exists(cra.CUADERNO) else 0
    assert despues > antes, "cada freno tiene que dejar rastro en el cuaderno"


def test_la_ley_esta_escrita():
    """La ley existe y no es solo codigo: si se borra el contrato, esto se pone rojo."""
    ley = os.path.join(AQUI, "CONTRATO_RUTA_DE_ACCESO.md")
    assert os.path.exists(ley), "falta CONTRATO_RUTA_DE_ACCESO.md"
    texto = open(ley, encoding="utf-8", errors="ignore").read().lower()
    assert "ruta" in texto and "plan" in texto
