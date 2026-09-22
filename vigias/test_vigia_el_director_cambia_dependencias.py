import json

from cuerpo import director


RUTA_ORDENES = ("memoria", "ORDENES.json")


def _escribir_ordenes(base, ordenes):
    """Deja memoria/ORDENES.json dentro de la carpeta temporal de la prueba."""
    carpeta = base / RUTA_ORDENES[0]
    carpeta.mkdir(parents=True, exist_ok=True)
    archivo = carpeta / RUTA_ORDENES[1]
    archivo.write_text(json.dumps(ordenes, ensure_ascii=False), encoding="utf-8")
    return archivo


def _leer_ordenes(base):
    """Devuelve la lista de ordenes tal como quedo en el disco."""
    archivo = base / RUTA_ORDENES[0] / RUTA_ORDENES[1]
    return json.loads(archivo.read_text(encoding="utf-8"))


def _buscar_orden(ordenes, id_orden):
    """Devuelve la orden con ese id, o None si no esta."""
    for orden in ordenes:
        if str(orden.get("id")) == str(id_orden):
            return orden
    return None


def _ordenes_de_prueba():
    """Las dos ordenes que pide la tarea: la 1 depende de la 2, la 2 no depende de nadie."""
    return [
        {"id": "1", "estado": "pendiente", "depende": ["2"]},
        {"id": "2", "estado": "pendiente", "depende": []},
    ]


def test_el_director_cambia_dependencias(tmp_path):
    """El director cambia las dependencias de una orden y archiva otra, sin tocar nada mas."""
    _escribir_ordenes(tmp_path, _ordenes_de_prueba())

    # (1) Cambiar las dependencias de la orden 1: se queda sin dependencias.
    resultado = director.depende(str(tmp_path), "1", [])
    assert resultado[0] is True, "cambiar las dependencias de una orden que existe debe salir bien"
    orden_1 = _buscar_orden(_leer_ordenes(tmp_path), "1")
    assert orden_1 is not None, "la orden 1 tiene que seguir existiendo"
    assert orden_1["depende"] == [], "la orden 1 tiene que quedar con depende []"

    # (2) Un id que no existe: el director dice que no, y no revienta.
    resultado = director.depende(str(tmp_path), "999", [])
    assert resultado[0] is False, "cambiar las dependencias de una orden que no existe debe salir mal"

    # (3) Archivar la orden 2 con su nota.
    director.archivar(str(tmp_path), "2", "x")
    orden_2 = _buscar_orden(_leer_ordenes(tmp_path), "2")
    assert orden_2 is not None, "la orden 2 tiene que seguir existiendo"
    assert orden_2["estado"] == "archivada", "la orden 2 tiene que quedar archivada"
    assert orden_2["nota"] == "x", "la orden 2 tiene que quedar con la nota x"
