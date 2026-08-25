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
    # AISLADA DEL PERMISO DE VERDAD (2026-08-25). El candado tiene ahora una via honrada: con un
    # NECESITO_EDITAR vigente para ESE archivo, abre. Es correcto. Pero esta vigia usa app.py de
    # Foto Informe, y si alguien tiene un permiso vivo para app.py (por ejemplo probando el propio
    # candado), la vigia se pone ROJA sin que nada este mal. Medido ese dia: "PERMISO VIGENTE para
    # app.py (quedan 23 min)". Una vigia que depende de lo que haya vivo en la maquina no vale:
    # es la leccion de las vigias inestables. Aqui se le da un permiso DE MENTIRA, vacio, para que
    # siempre mida lo mismo. La exigencia no se afloja: sin veredicto sigue teniendo que bloquear.
    try:
        import permiso_editar
        monkeypatch.setattr(permiso_editar, "RUTA", os.path.join(d, "permiso_de_mentira.json"),
                            raising=False)
    except Exception:
        pass
    monkeypatch.setattr(sys, "stdin", io.StringIO(
        json.dumps({"tool_input": {"file_path": fp}})))
    return candado_equipo.main()


def test_sin_veredicto_bloquea_aunque_no_haya_cerebros(monkeypatch):
    """Tocar codigo en foto_informe SIN veredicto debe BLOQUEAR, aun sin cerebros."""
    rc = _feed(monkeypatch, FOTO)
    assert rc == 2, "debia bloquear (sin equipo) aunque no hubiera cerebros"


def test_con_veredicto_que_cubre_el_archivo_abre(monkeypatch):
    """Con veredicto reciente que cubre el archivo, se abre."""
    rc = _feed(monkeypatch, FOTO, veredicto={"archivos": ["app.py"]})
    assert rc == 0
