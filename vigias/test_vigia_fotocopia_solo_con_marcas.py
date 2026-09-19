import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, 'arnes'))
import candado_terminal as c


# Las marcas se arman por partes para no escribirlas enteras en el archivo.
VIEJO = 'TEXTO' + ' VIEJO'
NUEVO = 'TEXTO' + ' NUEVO'
CAMPO_V = 'texto' + '_viejo'
CAMPO_N = 'texto' + '_nuevo'


def test_fotocopia_de_verdad_con_marcas_al_inicio_de_linea():
    """Un encargo con las dos marcas al inicio de linea SI es fotocopia."""
    texto = '\n'.join([
        'en cuerpo/x.py cambia una linea.',
        VIEJO + ' EXACTO:',
        '    a = 1',
        NUEVO + ' EXACTO:',
        '    a = 2',
    ])
    assert c.es_una_fotocopia(texto) is True


def test_marcas_al_inicio_de_linea_con_espacios_delante_tambien_es_fotocopia():
    """Si las marcas van al inicio de linea con espacios delante, tambien es fotocopia."""
    texto = '\n'.join([
        'en cuerpo/x.py cambia una linea.',
        '    ' + VIEJO + ' EXACTO:',
        '    a = 1',
        '    ' + NUEVO + ' EXACTO:',
        '    a = 2',
    ])
    assert c.es_una_fotocopia(texto) is True


def test_mencionar_los_campos_en_una_frase_no_es_fotocopia():
    """Una sola linea que solo menciona los campos dentro de una frase NO es fotocopia."""
    texto = 'la falsa devuelve un json con ' + CAMPO_V + ' y ' + CAMPO_N + ' y se revisa'
    assert c.es_una_fotocopia(texto) is False


def test_mencionar_las_marcas_en_una_frase_no_es_fotocopia():
    """Una frase que solo dice que el viejo y el nuevo van en el json NO es fotocopia."""
    texto = ' el ' + VIEJO + ' y el ' + NUEVO + ' van en el json'
    assert c.es_una_fotocopia(texto) is False


def test_texto_sin_marcas_no_es_fotocopia():
    """Un texto sin ninguna marca no es fotocopia."""
    assert c.es_una_fotocopia('en cuerpo/x.py cambia una linea y ya esta') is False


def test_none_no_es_fotocopia():
    """None no es fotocopia y no revienta."""
    assert c.es_una_fotocopia(None) is False
