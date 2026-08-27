# -*- coding: utf-8 -*-
"""vigias/test_vigia_equipo_siempre.py — CLAUDE SIEMPRE TRABAJA CON EL EQUIPO.

Julio, 2026-08-21: "fortalece que claude trabaje siempre con el equipo, no lo vigila nada si
trabaja en fotoinforme."

Vigila que el candado del equipo NO deje escribir a solas, NI siquiera cuando no hay cerebros
disponibles (antes se escapaba por ahi y foto_informe quedaba sin vigilar). Con el fortalecido,
tocar codigo SIN veredicto SIEMPRE se bloquea.
"""
import sys, os, json, io, tempfile, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import candado_equipo  # noqa: E402

FOTO = r"C:\Users\USER\dev\Foto_info_repo\Foto_informe--main\app.py"


def _feed(monkeypatch, fp, veredicto=None):
    monkeypatch.setattr(candado_equipo, "_hay_cerebros", lambda: False)  # sin cerebros: el viejo escape
    monkeypatch.setattr(os.path, "exists", lambda p: True)               # el archivo "existe"
    d = tempfile.mkdtemp()
    ruta_ver = os.path.join(d, "v.json")
    if veredicto:
        json.dump({**veredicto, "cuando": time.time()},
                  open(ruta_ver, "w", encoding="utf-8"))
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", ruta_ver)
    monkeypatch.setenv("INGENIERO_SIN_EQUIPO_TEST", os.path.join(d, "sin.log"))
    # (2026-08-26): el permiso de edicion (NECESITO_EDITAR) esta RETIRADO por orden de Julio — ya
    # no hay via honrada que abra sin veredicto. Esta vigia ya no tiene que aislar ninguna llave.
    monkeypatch.setattr(sys, "stdin", io.StringIO(
        json.dumps({"tool_input": {"file_path": fp}})))
    return candado_equipo.main()


def test_sin_veredicto_bloquea_aunque_no_haya_cerebros(monkeypatch):
    """Tocar codigo en foto_informe SIN veredicto debe BLOQUEAR, aun sin cerebros."""
    rc = _feed(monkeypatch, FOTO)
    assert rc == 2, "debia bloquear (sin equipo) aunque no hubiera cerebros"


def test_con_veredicto_que_cubre_el_archivo_abre(monkeypatch):
    """Con APROBADO reciente del equipo que cubre el archivo, se abre.

    (2026-08-27, NO SELLO DE GOMA): antes esta vigia pasaba {"archivos": [...]} SIN campo de
    veredicto y esperaba que abriera — justo el hueco que Julio ordeno cerrar: una puerta que abre
    sin APROBADO real le decian "el equipo lo aprobo" cuando nadie habia auditado. Ahora la llave
    es un APROBADO con 4 ojos; SIN_AUDITAR o RECHAZADO no abren (ver test_vigia_siempre_con_equipo).
    """
    rc = _feed(monkeypatch, FOTO, veredicto={"archivos": ["app.py"], "veredicto": "APROBADO"})
    assert rc == 0
