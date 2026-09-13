import json, os, sys

# Añadir ruta del proyecto para importar privacidad
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cuerpo import privacidad

SALTO = chr(10)
ARROBA = chr(64)

def test_decorador_empaquetado_en_json_no_se_tapa():
    codigo = "import pytest" + SALTO + SALTO + ARROBA + "pytest.fixture(autouse=True)" + SALTO + "def f(): pass" + SALTO
    sobre = json.dumps({"texto_nuevo": codigo})
    limpio, n = privacidad.limpiar(sobre)
    assert n == 0, f"Se taparon {n} elementos"
    assert limpio == sobre, "El JSON se modificó"
    assert json.loads(limpio)["texto_nuevo"] == codigo, "El decorador fue alterado"

def test_otros_decoradores_con_punto_tambien_llegan_enteros():
    decoradores = [
        SALTO + ARROBA + "pytest.mark.parametrize('x', [1, 2])" + SALTO,
        SALTO + ARROBA + "app.route('/clientes')" + SALTO,
        SALTO + ARROBA + "functools.lru_cache(maxsize=None)" + SALTO
    ]
    for dec in decoradores:
        sobre = json.dumps({"texto_nuevo": dec})
        limpio, n = privacidad.limpiar(sobre)
        assert n == 0, f"Se taparon {n} elementos"
        assert limpio == sobre, "El JSON se modificó"
        assert json.loads(limpio)["texto_nuevo"] == dec, f"El decorador {dec.strip()} se rompió"

def test_un_correo_de_verdad_se_sigue_tapando_en_texto_normal():
    correo = "maria.perez" + ARROBA + "empresa.es"
    limpio, n = privacidad.limpiar("El cliente escribio desde " + correo)
    assert "maria.perez" not in limpio, "El correo no se tapó en texto normal"
    assert "<CORREO>" in limpio, "El placeholder <CORREO> no apareció"

def test_un_correo_de_verdad_se_sigue_tapando_dentro_de_json_detras_de_un_salto():
    texto = "Datos del cliente:" + SALTO + "juan.gomez" + ARROBA + "gmail.com" + SALTO
    sobre = json.dumps({"x": texto})
    limpio, n = privacidad.limpiar(sobre)
    assert "juan.gomez" not in limpio, "El correo no se tapó dentro de JSON"
    assert "gmail.com" not in limpio, "El dominio del correo no se tapó dentro de JSON"
    assert n >= 1, "No se detectó ningún correo tapado"

def test_un_correo_detras_de_un_tabulador_empaquetado_se_tapa():
    texto = "Datos del cliente:" + chr(9) + "juan.gomez" + ARROBA + "gmail.com" + SALTO
    sobre = json.dumps({"x": texto})
    limpio, n = privacidad.limpiar(sobre)
    assert "juan.gomez" not in limpio, "El correo no se tapó detrás de tabulador"
    assert "gmail.com" not in limpio, "El dominio del correo no se tapó detrás de tabulador"
    assert n >= 1, "No se detectó ningún correo tapado"

def test_un_correo_al_principio_del_texto_se_tapa():
    correo = "ana" + ARROBA + "correo.com"
    limpio, n = privacidad.limpiar(correo + " dijo que si")
    assert correo not in limpio, "El correo al principio del texto no se tapó"
    assert "<CORREO>" in limpio, "El placeholder <CORREO> no apareció"
