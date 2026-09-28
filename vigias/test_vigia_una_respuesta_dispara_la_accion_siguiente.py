import os
import sys
import json
import importlib


# Arranque: meter en sys.path la carpeta un nivel arriba de vigias y la carpeta arnes.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_VIGIAS = _AQUI
_RAIZ = os.path.dirname(_VIGIAS)
_ARNES = os.path.join(_RAIZ, "arnes")
for _p in (_RAIZ, _ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)


RUTA_PROGRAMA = os.path.join(_ARNES, "medir_disparadores_que_faltan.py")


def _cargar_programa():
    """Importa el programa dentro de la prueba, desde su ruta en disco."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "medir_disparadores_que_faltan", RUTA_PROGRAMA
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _llamada(clase, quien, cuando, segundos):
    return {
        "clase": clase,
        "quien": quien,
        "cuando": cuando,
        "segundos": segundos,
    }


def _cuatro_llamadas():
    return [
        _llamada("reparar", "uno", "2026-09-01T10:00:00", 10),
        _llamada("auditar", "dos", "2026-09-01T10:00:30", 20),
        _llamada("reparar", "uno", "2026-09-01T10:20:00", 60),
        _llamada("auditar", "dos", "2026-09-01T10:30:00", 30),
    ]


def test_el_programa_no_llama_a_ninguna_ia():
    with open(RUTA_PROGRAMA, "r", encoding="utf-8") as f:
        texto = f.read()
    prohibidas = [
        "obrero",
        "bigpickle",
        "deepseek",
        "claude",
        "requests",
        "urllib",
        "http",
    ]
    bajo = texto.lower()
    for palabra in prohibidas:
        assert palabra not in bajo, "el programa menciona: " + palabra


def test_los_huecos_salen_con_sus_segundos():
    programa = _cargar_programa()
    huecos = programa.huecos(_cuatro_llamadas(), 120)
    assert len(huecos) == 2
    primero = huecos[0]
    segundo = huecos[1]
    assert primero["segundos_perdidos"] == 1110
    assert primero["clase_antes"] == "auditar"
    assert primero["clase_despues"] == "reparar"
    assert segundo["segundos_perdidos"] == 570
    assert segundo["clase_antes"] == "reparar"
    assert segundo["clase_despues"] == "auditar"
    claves = {
        "cuando_termino",
        "clase_antes",
        "quien_antes",
        "cuando_empezo_la_siguiente",
        "clase_despues",
        "quien_despues",
        "segundos_perdidos",
    }
    for h in huecos:
        assert set(h.keys()) == claves


def test_un_hueco_chico_no_cuenta():
    programa = _cargar_programa()
    huecos = programa.huecos(_cuatro_llamadas(), 120)
    for h in huecos:
        assert h["segundos_perdidos"] != 10


def test_las_ordenes_que_podian_salir_solas():
    programa = _cargar_programa()
    ordenes = [
        {"id": "A", "estado": "hecha", "depende": []},
        {"id": "B", "estado": "pendiente", "depende": []},
        {"id": "C", "estado": "pendiente", "depende": ["A"]},
        {"id": "D", "estado": "pendiente", "depende": ["C"]},
        {"id": "E", "estado": "hecha", "depende": []},
    ]
    salen = programa.ordenes_listas_y_paradas(ordenes)
    ids = sorted(o["id"] for o in salen)
    assert ids == ["B", "C"]


def test_deja_el_documento_en_la_carpeta_memoria(tmp_path):
    programa = _cargar_programa()
    memoria = tmp_path / "memoria"
    memoria.mkdir()
    cuaderno = memoria / "CUADERNO_DE_LLAMADAS.jsonl"
    with open(cuaderno, "w", encoding="utf-8") as f:
        for llamada in _cuatro_llamadas():
            f.write(json.dumps(llamada) + "\n")
    ordenes = memoria / "ORDENES.json"
    with open(ordenes, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"id": "A", "estado": "hecha", "depende": []},
                {"id": "B", "estado": "pendiente", "depende": []},
            ],
            f,
        )
    resultado = programa.medir(str(tmp_path))
    documento = memoria / "MEDIDA_DISPARADORES_QUE_FALTAN.md"
    assert documento.exists()
    assert set(resultado.keys()) == {"huecos", "ordenes_paradas"}
