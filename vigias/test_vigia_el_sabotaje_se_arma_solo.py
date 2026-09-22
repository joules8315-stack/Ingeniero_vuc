import json

from cuerpo import capataz


# ---------------------------------------------------------------------------
# Ayudantes de la vigia.
#
# La vigia comprueba que capataz.armar_sabotaje(orden, raiz=None) arma el
# sabotaje a partir del ULTIMO trabajo APROBADO de la pieza que dice la orden.
# El sabotaje es una lista de objetos con:
#   - 'archivo': la pieza que se toca
#   - 'viejo'  : el texto que hay que dejar (lo que la propuesta aprobada puso)
#   - 'nuevo'  : el texto que hay que poner (lo que habia antes del cambio)
# Es decir: deshace el cambio aprobado.
# ---------------------------------------------------------------------------


CARPETA_TRABAJOS = ('memoria', 'trabajos_del_equipo')
CARPETA_SABOTAJES = ('memoria', 'sabotajes')


def _carpeta_trabajos(tmp_path):
    """Devuelve (y crea) tmp_path/memoria/trabajos_del_equipo."""
    carpeta = tmp_path
    for trozo in CARPETA_TRABAJOS:
        carpeta = carpeta / trozo
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def _escribir_trabajo_aprobado(tmp_path, nombre, propuesta):
    """Deja un trabajo APROBADO en memoria/trabajos_del_equipo con la propuesta dada."""
    carpeta = _carpeta_trabajos(tmp_path)
    ruta = carpeta / nombre
    ruta.write_text(json.dumps({'propuesta': propuesta}), encoding='utf-8')
    return ruta


def _ruta_sabotaje(tmp_path, orden):
    """Convierte el campo 'sabotaje' de la orden en una ruta dentro de tmp_path."""
    return tmp_path / orden['sabotaje']


def _leer_sabotaje(tmp_path, orden):
    """Lee el archivo de sabotaje y devuelve la lista que hay dentro."""
    ruta = _ruta_sabotaje(tmp_path, orden)
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def _orden(pieza='pieza.py', sabotaje='memoria/sabotajes/nueve.json'):
    """La orden de la tarea: id 9, la pieza y donde va el sabotaje."""
    return {'id': '9', 'pieza': pieza, 'sabotaje': sabotaje}


# ---------------------------------------------------------------------------
# (1) Con un trabajo APROBADO normal, el sabotaje deshace el cambio aprobado.
# ---------------------------------------------------------------------------


def test_arma_el_sabotaje_y_deshace_el_cambio_aprobado(tmp_path):
    _escribir_trabajo_aprobado(
        tmp_path,
        '2026-09-21_100000_APROBADO_pieza.py.json',
        {
            'archivo': 'pieza.py',
            'texto_viejo': 'return 1',
            'texto_nuevo': 'return 2',
        },
    )
    orden = _orden()

    resultado = capataz.armar_sabotaje(orden, raiz=str(tmp_path))

    assert resultado is True
    ruta = _ruta_sabotaje(tmp_path, orden)
    assert ruta.exists()
    lista = _leer_sabotaje(tmp_path, orden)
    assert isinstance(lista, list)
    assert len(lista) == 1
    objeto = lista[0]
    assert objeto['archivo'] == 'pieza.py'
    # El cambio aprobado puso 'return 2'; el sabotaje tiene que devolver 'return 1'.
    assert objeto['viejo'] == 'return 2'
    assert objeto['nuevo'] == 'return 1'


# ---------------------------------------------------------------------------
# (2) Si la propuesta trae una lista 'cambios' con dos trozos, el sabotaje
#     tiene dos objetos y cada uno deshace su trozo.
# ---------------------------------------------------------------------------


def test_arma_un_objeto_por_cada_trozo_de_la_lista_cambios(tmp_path):
    _escribir_trabajo_aprobado(
        tmp_path,
        '2026-09-21_100000_APROBADO_pieza.py.json',
        {
            'archivo': 'pieza.py',
            'cambios': [
                {'texto_viejo': 'a', 'texto_nuevo': 'b'},
                {'texto_viejo': 'c', 'texto_nuevo': 'd'},
            ],
        },
    )
    orden = _orden()

    resultado = capataz.armar_sabotaje(orden, raiz=str(tmp_path))

    assert resultado is True
    lista = _leer_sabotaje(tmp_path, orden)
    assert isinstance(lista, list)
    assert len(lista) == 2
    assert lista[0]['archivo'] == 'pieza.py'
    assert lista[0]['viejo'] == 'b'
    assert lista[0]['nuevo'] == 'a'
    assert lista[1]['archivo'] == 'pieza.py'
    assert lista[1]['viejo'] == 'd'
    assert lista[1]['nuevo'] == 'c'


# ---------------------------------------------------------------------------
# (3) Si la propuesta no trae texto_viejo (pieza creada entera), no hay nada
#     que deshacer: devuelve False y NO crea el archivo de sabotaje.
# ---------------------------------------------------------------------------


def test_sin_texto_viejo_no_arma_nada(tmp_path):
    _escribir_trabajo_aprobado(
        tmp_path,
        '2026-09-21_100000_APROBADO_pieza.py.json',
        {
            'archivo': 'pieza.py',
            'texto_nuevo': 'def pieza():\n    return 2\n',
        },
    )
    orden = _orden()

    resultado = capataz.armar_sabotaje(orden, raiz=str(tmp_path))

    assert resultado is False
    assert not _ruta_sabotaje(tmp_path, orden).exists()


# ---------------------------------------------------------------------------
# (4) Si no hay ningun trabajo APROBADO de la pieza, devuelve False.
# ---------------------------------------------------------------------------


def test_sin_trabajo_aprobado_no_arma_nada(tmp_path):
    # Hay un trabajo de la pieza, pero NO esta aprobado.
    _escribir_trabajo_aprobado(
        tmp_path,
        '2026-09-21_100000_PENDIENTE_pieza.py.json',
        {
            'archivo': 'pieza.py',
            'texto_viejo': 'return 1',
            'texto_nuevo': 'return 2',
        },
    )
    orden = _orden()

    resultado = capataz.armar_sabotaje(orden, raiz=str(tmp_path))

    assert resultado is False
    assert not _ruta_sabotaje(tmp_path, orden).exists()
