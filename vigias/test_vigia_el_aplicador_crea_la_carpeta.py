"""Vigia: el aplicador crea la carpeta cuando el archivo nuevo va dentro de una carpeta que no existe.

Fallo real: al crear un archivo nuevo cuya carpeta padre no existe, open() falla con
FileNotFoundError y el aplicador devuelve False. La creacion de archivos nuevos debe
funcionar tanto si la carpeta ya existe como si hay que crearla.

Se prueba la funcion de cuerpo/aplicador.py que contiene el mensaje "Archivo creado.",
igual que lo hace vigias/test_vigia_aplicador.py, con raiz=str(tmp_path).
"""

import os

from cuerpo import aplicador


def test_crea_archivo_nuevo_en_carpeta_que_no_existe(tmp_path):
    """Un archivo nuevo dentro de carpetas que no existen se crea, y las carpetas tambien."""
    relativo = os.path.join("carpeta_nueva", "sub", "x.txt")
    propuesta = {"archivo": relativo, "codigo": "hola"}
    ok, msg = aplicador.aplicar_cambio(propuesta, raiz=str(tmp_path))
    assert ok, "no creo el archivo nuevo en carpeta que no existe: " + str(msg)
    destino = tmp_path / "carpeta_nueva" / "sub" / "x.txt"
    assert destino.exists(), "no quedo el archivo en disco"
    assert destino.read_text(encoding="utf-8") == "hola", "el contenido no es hola"


def test_crea_archivo_nuevo_en_carpeta_que_ya_existe(tmp_path):
    """Un archivo nuevo dentro de una carpeta que ya existe sigue funcionando igual."""
    (tmp_path / "carpeta_existente").mkdir()
    relativo = os.path.join("carpeta_existente", "y.txt")
    propuesta = {"archivo": relativo, "codigo": "hola"}
    ok, msg = aplicador.aplicar_cambio(propuesta, raiz=str(tmp_path))
    assert ok, "no creo el archivo nuevo en carpeta existente: " + str(msg)
    destino = tmp_path / "carpeta_existente" / "y.txt"
    assert destino.exists(), "no quedo el archivo en disco"
    assert destino.read_text(encoding="utf-8") == "hola", "el contenido no es hola"
