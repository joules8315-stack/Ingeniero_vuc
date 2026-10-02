import os
import tempfile

import pytest


# Variable de entorno que apunta al registro de Big Pickle.
# El archivo de ajustes comunes de las vigias (conftest) debe fijarla,
# para cada prueba, a una carpeta temporal, igual que hace con las otras
# variables de prueba.
VARIABLE_REGISTRO = "BIG_PICKLE_REGISTRO"


def test_las_pruebas_apuntan_a_un_registro_temporal(tmp_path):
    """El registro de Big Pickle debe vivir en una carpeta temporal durante las pruebas.

    Se ejecuta una prueba hija con pytest y se comprueba, con un assert,
    que dentro de esa prueba la variable del registro apunta a una carpeta
    temporal y no a la ruta real del proyecto.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivo_hijo = tmp_path / "test_hijo_registro_temporal.py"
    archivo_hijo.write_text(
        "import os\n"
        "\n"
        "\n"
        "def test_dentro_del_hijo():\n"
        "    valor = os.environ.get('" + VARIABLE_REGISTRO + "')\n"
        "    assert valor, 'la variable del registro no esta fijada'\n"
        "    assert os.path.isabs(valor), 'la ruta del registro no es absoluta'\n"
        "    assert 'tmp' in valor.lower() or 'temp' in valor.lower(), (\n"
        "        'la ruta del registro no apunta a una carpeta temporal: ' + valor\n"
        "    )\n",
        encoding="utf-8",
    )

    resultado = pytest.main(
        [
            str(archivo_hijo),
            "-p",
            "no:cacheprovider",
            "-q",
        ]
    )

    assert resultado == 0, (
        "el archivo de ajustes comunes de las vigias no fija "
        + VARIABLE_REGISTRO
        + " a una carpeta temporal para cada prueba"
    )
