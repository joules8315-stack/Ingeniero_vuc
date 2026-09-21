"""Vigia: varios trozos de un archivo en una sola ronda.

Vigila la funcion NUEVA aplicar_propuesta, que vivira en cuerpo/aplicador.py junto a
aplicar_cambio y aplicar_cambios. La funcion decide sola:

  - si la propuesta trae la clave 'cambios' (lista de diccionarios con texto_viejo y
    texto_nuevo), aplica TODOS esos trozos sobre el archivo de la clave 'archivo' de la
    propuesta usando aplicar_cambios, poniendole a cada trozo ese archivo si no trae el suyo;
  - si no trae 'cambios', hace lo mismo que aplicar_cambio.

Devuelve lo mismo que ellas: una pareja (ok, mensaje).

Motivo medido: el equipo solo puede cambiar un trozo por ronda porque aplicar_cambios existe
pero nadie la llama, y eso ha costado decenas de rondas pagadas.

MUY IMPORTANTE: cuerpo/aplicador.py anota cada aplicacion en el registro de verdad con su
funcion _apuntar_log. En cada prueba se cambia _apuntar_log por una que no hace nada, con
monkeypatch, para que la prueba no escriba en la memoria de verdad.

Se importa aplicar_propuesta DENTRO de cada prueba, no arriba del archivo, para no dejar
ciega a la bateria mientras no exista.
"""

import os
import sys

import pytest


# La raiz del proyecto (la carpeta que contiene 'cuerpo' y 'vigias') se pone en sys.path
# para poder importar cuerpo.aplicador desde cualquier sitio desde donde se lance pytest.
_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)


def _sin_log(monkeypatch):
    """Sustituye _apuntar_log por una que no hace nada.

    Se importa cuerpo.aplicador aqui dentro (no arriba) y se parchea su _apuntar_log para
    que ninguna prueba escriba en memoria/APLICACIONES.log, que es el registro de verdad.
    """
    import cuerpo.aplicador as aplicador

    monkeypatch.setattr(aplicador, "_apuntar_log", lambda *a, **k: None)
    return aplicador


def _escribir_archivo_mentira(tmp_path, nombre="mentira.py", contenido=None):
    """Crea un archivo de mentira dentro de la carpeta temporal y devuelve su ruta."""
    if contenido is None:
        contenido = (
            "# archivo de mentira para la vigia\n"
            "UNO = 1\n"
            "DOS = 2\n"
            "TRES = 3\n"
        )
    ruta = tmp_path / nombre
    ruta.write_text(contenido, encoding="utf-8")
    return str(ruta)


def test_tres_trozos_en_cambios_se_aplican_los_tres(tmp_path, monkeypatch):
    """Con tres trozos en 'cambios' se aplican los tres de una sola vez."""
    aplicador = _sin_log(monkeypatch)
    from cuerpo.aplicador import aplicar_propuesta

    ruta = _escribir_archivo_mentira(tmp_path)
    propuesta = {
        "archivo": ruta,
        "cambios": [
            {"texto_viejo": "UNO = 1", "texto_nuevo": "UNO = 10"},
            {"texto_viejo": "DOS = 2", "texto_nuevo": "DOS = 20"},
            {"texto_viejo": "TRES = 3", "texto_nuevo": "TRES = 30"},
        ],
    }

    ok, mensaje = aplicar_propuesta(propuesta, raiz=str(tmp_path))

    assert ok is True, mensaje
    texto = open(ruta, "r", encoding="utf-8").read()
    assert "UNO = 10" in texto
    assert "DOS = 20" in texto
    assert "TRES = 30" in texto
    assert "UNO = 1\n" not in texto
    assert "DOS = 2\n" not in texto
    assert "TRES = 3\n" not in texto


def test_si_un_trozo_no_aparece_no_se_aplica_ninguno(tmp_path, monkeypatch):
    """Si uno de los trozos no aparece en el archivo, no se aplica NINGUNO y queda igual."""
    aplicador = _sin_log(monkeypatch)
    from cuerpo.aplicador import aplicar_propuesta

    ruta = _escribir_archivo_mentira(tmp_path)
    antes = open(ruta, "r", encoding="utf-8").read()

    propuesta = {
        "archivo": ruta,
        "cambios": [
            {"texto_viejo": "UNO = 1", "texto_nuevo": "UNO = 10"},
            {"texto_viejo": "NO_EXISTE_ESTO = 99", "texto_nuevo": "NO_EXISTE_ESTO = 100"},
            {"texto_viejo": "TRES = 3", "texto_nuevo": "TRES = 30"},
        ],
    }

    ok, mensaje = aplicar_propuesta(propuesta, raiz=str(tmp_path))

    assert ok is False, mensaje
    despues = open(ruta, "r", encoding="utf-8").read()
    assert despues == antes, "el archivo no puede cambiar si un trozo falla"
    assert "UNO = 10" not in despues
    assert "TRES = 30" not in despues


def test_sin_cambios_se_aplica_texto_viejo_y_texto_nuevo(tmp_path, monkeypatch):
    """Sin la clave 'cambios' se comporta como aplicar_cambio: usa texto_viejo y texto_nuevo."""
    aplicador = _sin_log(monkeypatch)
    from cuerpo.aplicador import aplicar_propuesta

    ruta = _escribir_archivo_mentira(tmp_path)
    propuesta = {
        "archivo": ruta,
        "funcion": "?",
        "texto_viejo": "DOS = 2",
        "texto_nuevo": "DOS = 22",
    }

    ok, mensaje = aplicar_propuesta(propuesta, raiz=str(tmp_path))

    assert ok is True, mensaje
    texto = open(ruta, "r", encoding="utf-8").read()
    assert "DOS = 22" in texto
    assert "DOS = 2\n" not in texto


def test_trozos_sin_archivo_usan_el_de_la_propuesta(tmp_path, monkeypatch):
    """Los trozos que no traen 'archivo' usan el archivo de la propuesta."""
    aplicador = _sin_log(monkeypatch)
    from cuerpo.aplicador import aplicar_propuesta

    ruta = _escribir_archivo_mentira(tmp_path)
    propuesta = {
        "archivo": ruta,
        "cambios": [
            {"texto_viejo": "UNO = 1", "texto_nuevo": "UNO = 11"},
            {"texto_viejo": "TRES = 3", "texto_nuevo": "TRES = 33"},
        ],
    }

    ok, mensaje = aplicar_propuesta(propuesta, raiz=str(tmp_path))

    assert ok is True, mensaje
    texto = open(ruta, "r", encoding="utf-8").read()
    assert "UNO = 11" in texto
    assert "TRES = 33" in texto
    assert "DOS = 2" in texto, "lo que no se toca debe quedar igual"
