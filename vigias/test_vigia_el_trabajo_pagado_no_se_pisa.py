"""VIGIA: el trabajo pagado del equipo no se pisa.

Protege contra el fallo medido el 2026-09-12: el comando `equipo` de ingeniero.py
guardaba el resultado entero SIEMPRE en memoria/ULTIMO_TRABAJO_DEL_EQUIPO.json en
modo "w", y la ronda siguiente lo borraba. Asi se perdio la memoria de veredictos
de 24 h APROBADA por el equipo a las 21:18, y hubo que volver a pagarla.

Lo dice Julio, prioridad de raiz:
"Repara primero la herramienta que hace desechar trabajo pago, sin eso cualquier
cosa es estupida, ya que no permite crear nada."

Estas pruebas nacen ROJAS: candado_equipo.guardar_trabajo_pagado todavia no
existe y aplicar-guardado todavia no acepta un trabajo archivado. La cura se
hara despues, con el equipo.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import candado_equipo


def test_dos_rondas_seguidas_no_se_pisan(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_TRABAJOS_TEST", str(tmp_path))
    r1 = {"propuesta": {"archivo": "vigias/uno_de_prueba.py", "codigo": "x = 1\n"},
          "auditoria": {"veredicto": "APROBADO"}}
    r2 = {"propuesta": {"archivo": "cuerpo/dos_de_prueba.py", "codigo": "y = 2\n"},
          "auditoria": {"veredicto": "RECHAZADO"}}
    p1 = candado_equipo.guardar_trabajo_pagado(r1)
    p2 = candado_equipo.guardar_trabajo_pagado(r2)
    assert p1 and p2 and p1 != p2, (
        "la segunda ronda piso a la primera; se pierde trabajo pagado")
    assert os.path.exists(p1) and os.path.exists(p2), (
        "alguna de las dos copias archivadas no quedo en el disco")
    assert json.load(open(p1, encoding="utf-8"))["propuesta"]["archivo"] == "vigias/uno_de_prueba.py", (
        "la copia de la primera ronda no guarda su propia propuesta")
    assert json.load(open(p2, encoding="utf-8"))["propuesta"]["archivo"] == "cuerpo/dos_de_prueba.py", (
        "la copia de la segunda ronda no guarda su propia propuesta")


def test_el_nombre_dice_veredicto_y_archivo(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_TRABAJOS_TEST", str(tmp_path))
    r1 = {"propuesta": {"archivo": "vigias/uno_de_prueba.py", "codigo": "x = 1\n"},
          "auditoria": {"veredicto": "APROBADO"}}
    p1 = candado_equipo.guardar_trabajo_pagado(r1)
    nombre = os.path.basename(p1)
    assert "APROBADO" in nombre, (
        "el nombre del archivo archivado no dice el veredicto")
    assert "uno_de_prueba.py" in nombre, (
        "el nombre del archivo archivado no dice que archivo toca la propuesta")


def test_dos_rondas_en_el_mismo_segundo_tampoco_se_pisan(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_TRABAJOS_TEST", str(tmp_path))
    r1 = {"propuesta": {"archivo": "vigias/uno_de_prueba.py", "codigo": "x = 1\n"},
          "auditoria": {"veredicto": "APROBADO"}}
    p1 = candado_equipo.guardar_trabajo_pagado(r1)
    p2 = candado_equipo.guardar_trabajo_pagado(r1)
    assert p1 != p2, (
        "dos guardados en el mismo segundo devolvieron la misma ruta y uno pisa al otro")
    assert os.path.exists(p1) and os.path.exists(p2), (
        "alguna de las dos copias del mismo segundo no quedo en el disco")


def test_aplicar_guardado_acepta_un_trabajo_archivado(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_TRABAJOS_TEST", str(tmp_path))
    destino = tmp_path / "creado_por_la_prueba.py"
    r = {"propuesta": {"archivo": str(destino), "funcion": "NO_ENCONTRADO", "codigo": "z = 3\n"},
         "auditoria": {"veredicto": "APROBADO"}}
    p = candado_equipo.guardar_trabajo_pagado(r)
    res = subprocess.run(
        [sys.executable, os.path.join(AQUI, "ingeniero.py"),
         "aplicar-guardado", "ingeniero", p],
        cwd=AQUI, capture_output=True, text=True, timeout=180,
        env=dict(os.environ))
    assert destino.exists(), (
        "no se pudo aplicar un trabajo archivado sin volver a pagar. Salida: "
        + (res.stdout or "") + " | " + (res.stderr or ""))
    assert "z = 3" in destino.read_text(encoding="utf-8"), (
        "el archivo aplicado no tiene el codigo del trabajo archivado")


def test_el_ultimo_sigue_existiendo_como_hoy(tmp_path, monkeypatch):
    monkeypatch.setenv("INGENIERO_TRABAJOS_TEST", str(tmp_path))
    r1 = {"propuesta": {"archivo": "vigias/uno_de_prueba.py", "codigo": "x = 1\n"},
          "auditoria": {"veredicto": "APROBADO"}}
    candado_equipo.guardar_trabajo_pagado(r1)
    ultimo = tmp_path / "ULTIMO_TRABAJO_DEL_EQUIPO.json"
    assert ultimo.exists(), (
        "desaparecio ULTIMO_TRABAJO_DEL_EQUIPO.json, que hoy sigue siendo el ultimo trabajo")
    assert json.load(open(str(ultimo), encoding="utf-8"))["propuesta"]["archivo"] == "vigias/uno_de_prueba.py", (
        "ULTIMO_TRABAJO_DEL_EQUIPO.json no tiene la propuesta de la ultima ronda")
