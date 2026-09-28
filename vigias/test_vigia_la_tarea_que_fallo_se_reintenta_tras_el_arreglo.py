import json
import os

from cuerpo import capataz


# ---------------------------------------------------------------------------
# VIGIA: la tarea que fallo se reintenta tras el arreglo
#
# NACE ROJA A PROPOSITO. La funcion reintentar_tras_el_arreglo todavia NO
# existe en cuerpo/capataz.py: se agrega en la ronda siguiente. Esta vigia
# se escribe ANTES del cambio, como manda la ley.
#
# Que vigila:
#   reintentar_tras_el_arreglo(id_orden, id_arreglo) -> bool
#     - Si la orden existe y esta fallida: la deja pendiente, con
#       fallos_seguidos 0 y anade id_arreglo a su lista depende.
#     - Borra de HUELLAS_QUE_FALLARON.jsonl el renglon cuya huella es la de
#       esa orden, y conserva los demas renglones tal cual.
#     - Si la orden no existe: devuelve False y no toca ningun archivo.
#
# No llama a ninguna IA, no lanza procesos y solo escribe en tmp_path.
# ---------------------------------------------------------------------------


def _preparar(tmp_path, monkeypatch):
    """Arma un proyecto de mentira dentro de tmp_path y apunta capataz ahi.

    Deja:
      <tmp>/cuerpo/capataz.py        (archivo falso, solo para __file__)
      <tmp>/memoria/ORDENES.json
      <tmp>/memoria/HUELLAS_QUE_FALLARON.jsonl

    Devuelve (ruta_ordenes, ruta_huellas, orden_5, huella_5, huella_otra).
    """
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir()
    archivo_capataz = carpeta_cuerpo / 'capataz.py'
    archivo_capataz.write_text('# falso, solo para que __file__ apunte aqui\n', encoding='utf-8')

    # capataz.__file__ decide donde vive la carpeta memoria (sube dos niveles).
    monkeypatch.setattr(capataz, '__file__', str(archivo_capataz))

    carpeta_memoria = tmp_path / 'memoria'
    carpeta_memoria.mkdir()

    orden_5 = {
        'id': 5,
        'estado': 'fallida',
        'paso_fallido': 'guardia',
        'fallos_seguidos': 1,
        'depende': [],
        'encargo': 'arreglar el guardia de la orden cinco',
        'pieza': 'cuerpo/capataz.py',
    }
    huella_5 = capataz.huella_de(orden_5)

    # Otra orden distinta, para que su huella sea distinta de la de la orden 5.
    orden_otra = {
        'id': 9,
        'estado': 'fallida',
        'paso_fallido': 'otro',
        'fallos_seguidos': 2,
        'depende': [],
        'encargo': 'otra cosa que no tiene nada que ver',
        'pieza': 'cuerpo/otra_pieza.py',
    }
    huella_otra = capataz.huella_de(orden_otra)
    assert huella_otra != huella_5

    ruta_ordenes = carpeta_memoria / 'ORDENES.json'
    ruta_ordenes.write_text(
        json.dumps([orden_5], ensure_ascii=False),
        encoding='utf-8',
    )

    renglon_5 = json.dumps({'huella': huella_5, 'tipo': 'guardia'}, ensure_ascii=False)
    renglon_otra = json.dumps({'huella': huella_otra, 'tipo': 'otro'}, ensure_ascii=False)
    ruta_huellas = carpeta_memoria / 'HUELLAS_QUE_FALLARON.jsonl'
    ruta_huellas.write_text(renglon_5 + '\n' + renglon_otra + '\n', encoding='utf-8')

    return ruta_ordenes, ruta_huellas, orden_5, huella_5, huella_otra, renglon_otra


def _leer_ordenes(ruta_ordenes):
    with open(ruta_ordenes, encoding='utf-8') as f:
        return json.load(f)


def _leer_renglones(ruta_huellas):
    with open(ruta_huellas, encoding='utf-8') as f:
        return [linea for linea in f.read().splitlines() if linea.strip() != '']


def test_reintentar_tras_el_arreglo_deja_la_orden_pendiente(tmp_path, monkeypatch):
    """Prueba 1: la orden 5 queda pendiente, sin fallos y con 5-F1 en depende."""
    ruta_ordenes, ruta_huellas, orden_5, huella_5, huella_otra, renglon_otra = _preparar(tmp_path, monkeypatch)

    resultado = capataz.reintentar_tras_el_arreglo(5, '5-F1')

    assert resultado is True
    ordenes = _leer_ordenes(ruta_ordenes)
    orden = None
    for o in ordenes:
        if isinstance(o, dict) and o.get('id') == 5:
            orden = o
            break
    assert orden is not None
    assert orden.get('estado') == 'pendiente'
    assert orden.get('fallos_seguidos') == 0
    assert '5-F1' in orden.get('depende', [])


def test_reintentar_tras_el_arreglo_borra_la_huella_de_la_orden(tmp_path, monkeypatch):
    """Prueba 2: la huella de la orden 5 desaparece; el otro renglon queda igual."""
    ruta_ordenes, ruta_huellas, orden_5, huella_5, huella_otra, renglon_otra = _preparar(tmp_path, monkeypatch)

    resultado = capataz.reintentar_tras_el_arreglo(5, '5-F1')

    assert resultado is True
    renglones = _leer_renglones(ruta_huellas)
    huellas = []
    for linea in renglones:
        dato = json.loads(linea)
        huellas.append(dato.get('huella'))
    assert huella_5 not in huellas
    assert renglon_otra in renglones


def test_reintentar_tras_el_arreglo_con_id_inexistente_no_cambia_nada(tmp_path, monkeypatch):
    """Prueba 3: id que no existe devuelve False y no toca ningun archivo."""
    ruta_ordenes, ruta_huellas, orden_5, huella_5, huella_otra, renglon_otra = _preparar(tmp_path, monkeypatch)

    antes_ordenes = ruta_ordenes.read_text(encoding='utf-8')
    antes_huellas = ruta_huellas.read_text(encoding='utf-8')

    resultado = capataz.reintentar_tras_el_arreglo(999, '999-F1')

    assert resultado is False
    assert ruta_ordenes.read_text(encoding='utf-8') == antes_ordenes
    assert ruta_huellas.read_text(encoding='utf-8') == antes_huellas
