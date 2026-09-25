import json

from cuerpo import capataz


# Campos de una orden valida, copiados de una orden real de memoria/ORDENES.json.
# 'depende' va como lista vacia y 'modo' tiene que ser PROGRAMA o IA.
def _orden_de_ejemplo(id_orden, origen, encargo):
    return {
        'id': id_orden,
        'origen': origen,
        'repara': 'nada',
        'pieza': 'cuerpo/capataz.py',
        'depende': [],
        'modo': 'PROGRAMA',
        'razon': 'prueba de la vigia',
        'encargo': encargo,
    }


def _preparar(monkeypatch, tmp_path, lista_inicial):
    """Deja capataz apuntando a una memoria de mentira dentro de tmp_path.

    No se toca open: se cambia capataz.__file__ para que la carpeta del
    proyecto que calcula agregar_orden caiga en tmp_path/cuerpo/capataz.py,
    y asi la lista se escriba en tmp_path/memoria/ORDENES.json.
    """
    carpeta_cuerpo = tmp_path / 'cuerpo'
    carpeta_cuerpo.mkdir(parents=True, exist_ok=True)
    archivo_falso = carpeta_cuerpo / 'capataz.py'
    archivo_falso.write_text('# copia de mentira para la prueba\n', encoding='utf-8')
    monkeypatch.setattr(capataz, '__file__', str(archivo_falso))

    carpeta_memoria = tmp_path / 'memoria'
    carpeta_memoria.mkdir(parents=True, exist_ok=True)
    ruta_ordenes = carpeta_memoria / 'ORDENES.json'
    ruta_ordenes.write_text(json.dumps(lista_inicial, indent=2, ensure_ascii=False), encoding='utf-8')

    monkeypatch.setattr(capataz, 'leer_lista', lambda: list(lista_inicial))
    monkeypatch.setattr(capataz, 'ya_fallo', lambda orden: False)
    return ruta_ordenes


def _leer_ordenes(ruta_ordenes):
    with open(ruta_ordenes, encoding='utf-8') as f:
        return json.load(f)


def test_orden_forense_queda_la_primera(monkeypatch, tmp_path):
    """Una orden nueva con origen que empieza por 'forense:' queda la PRIMERA."""
    orden_a = _orden_de_ejemplo('A', 'humano', 'encargo A')
    orden_b = _orden_de_ejemplo('B', 'humano', 'encargo B')
    ruta_ordenes = _preparar(monkeypatch, tmp_path, [orden_a, orden_b])

    nueva = _orden_de_ejemplo('C', 'forense:A', 'encargo C')
    ok, motivo = capataz.agregar_orden(nueva)
    assert ok is True, motivo

    lista = _leer_ordenes(ruta_ordenes)
    assert lista[0]['id'] == 'C'
    assert lista[1]['id'] == 'A'
    assert lista[2]['id'] == 'B'


def test_orden_normal_queda_la_ultima(monkeypatch, tmp_path):
    """Una orden nueva con otro origen queda la ULTIMA, como hoy."""
    orden_a = _orden_de_ejemplo('A', 'humano', 'encargo A')
    orden_b = _orden_de_ejemplo('B', 'humano', 'encargo B')
    ruta_ordenes = _preparar(monkeypatch, tmp_path, [orden_a, orden_b])

    nueva = _orden_de_ejemplo('C', 'humano', 'encargo C')
    ok, motivo = capataz.agregar_orden(nueva)
    assert ok is True, motivo

    lista = _leer_ordenes(ruta_ordenes)
    assert lista[0]['id'] == 'A'
    assert lista[1]['id'] == 'B'
    assert lista[2]['id'] == 'C'
