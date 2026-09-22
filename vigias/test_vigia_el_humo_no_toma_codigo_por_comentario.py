from cuerpo import aplicador


def _escribir_m(tmp_path):
    """Escribe tmp_path/m.py con el contenido exacto que pide la vigia."""
    lineas = [
        'def f(texto):',
        '    """',
        '    Ayuda.',
        '    Devuelve algo.',
        '    """',
        '    return texto',
    ]
    ruta = tmp_path / 'm.py'
    ruta.write_text('\n'.join(lineas) + '\n', encoding='utf-8')
    return ruta


def test_el_humo_no_toma_codigo_por_comentario(tmp_path):
    """Un cambio que mete codigo de verdad no puede confundirse con humo.

    El texto_viejo son dos renglones que viven dentro del docstring, pero el
    texto_nuevo anade codigo ejecutable (if not texto: / return None). El
    aplicador tiene que aplicarlo y devolver True.
    """
    ruta = _escribir_m(tmp_path)

    texto_viejo = '    Devuelve algo.\n    """'
    texto_nuevo = (
        '    Devuelve algo.\n'
        '    """\n'
        '    if not texto:\n'
        '        return None'
    )

    propuesta = {
        'archivo': 'm.py',
        'texto_viejo': texto_viejo,
        'texto_nuevo': texto_nuevo,
    }

    ok, mensaje = aplicador.aplicar_cambio(propuesta, raiz=str(tmp_path))

    # (1) el primer valor que devuelve es True
    assert ok is True, f'Se esperaba True y llego {ok!r}: {mensaje}'

    # (2) el archivo ahora contiene el codigo nuevo
    contenido = ruta.read_text(encoding='utf-8')
    assert 'if not texto:' in contenido


def test_un_cambio_que_solo_toca_un_comentario_sigue_siendo_humo(tmp_path):
    """Un cambio que solo mete un comentario con almohadilla sigue devolviendo False."""
    _escribir_m(tmp_path)

    propuesta = {
        'archivo': 'm.py',
        'texto_viejo': '    return texto',
        'texto_nuevo': '    # nota\n    return texto',
    }

    ok, mensaje = aplicador.aplicar_cambio(propuesta, raiz=str(tmp_path))

    # (3) sigue devolviendo False
    assert ok is False, f'Se esperaba False y llego {ok!r}: {mensaje}'
