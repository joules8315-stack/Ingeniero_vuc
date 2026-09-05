# -*- coding: utf-8 -*-
"""VIGIA — nunca se escribe en un proyecto para arreglar otro, ni se crea lo que se iba a cambiar.

Ley: CONTRATO_LO_QUE_DE_VERDAD_IMPORTA.md, ley 1 (Julio, 2026-09-05):
  "Esta fallando otra politica, y es que se verifique que se este trabajando en la via canonica
   correcta, eso es una violacion flagrante."

EL FALLO, MEDIDO ESE MISMO DIA. El equipo aprobo una reparacion para un archivo de Foto Informe.
El sistema anuncio 'APLICADO en disco' y el archivo de Foto Informe no cambio: llevaba nueve dias
sin tocarse. Lo que ocurrio fue peor que no aplicar:

  1. El equipo entrega el nombre del archivo SUELTO, sin su carpeta.
  2. Quien lo escribe resuelve ese nombre desde donde esta el Ingeniero, NO desde el proyecto.
  3. Ahi ese archivo no existia, asi que lo CREO con solo el trozo nuevo dentro.
  4. Y devolvio exito. Arriba se anuncio APLICADO con toda honestidad.

Resultado: un archivo huerfano sembrado en la carpeta equivocada, una copia falsa de un archivo de
otro proyecto, y una reparacion que nadie hizo. La ruta mal resuelta convirtio un error en un
EXITO SILENCIOSO, que es la peor clase de error.

ESTAS VIGIAS NACEN ROJAS. No llaman a la red ni a ningun cerebro: le dan de comer al aplicador
casos de mentira sobre archivos temporales y miran que hace.
"""
import os
import sys
import tempfile

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from cuerpo import aplicador  # noqa: E402


@pytest.fixture
def carpeta():
    d = tempfile.mkdtemp(prefix="vigia_proyecto_")
    yield d


def _archivo(carpeta, nombre, contenido):
    p = os.path.join(carpeta, nombre)
    with open(p, "w", encoding="utf-8") as f:
        f.write(contenido)
    return p


# ------------------------------------------------- lo que SI debe seguir funcionando

def test_un_cambio_normal_se_aplica_igual_que_siempre(carpeta):
    """Antes de apretar nada: lo que ya funcionaba tiene que seguir funcionando."""
    p = _archivo(carpeta, "pieza.py", "def hola():\n    return 1\n")
    ok, msg = aplicador.aplicar_cambio(
        {"archivo": p, "texto_viejo": "return 1", "texto_nuevo": "return 2"})
    assert ok, "dejo de aplicar un cambio normal: %s" % msg
    assert "return 2" in open(p, encoding="utf-8").read(), "dijo que aplico y no aplico"


def test_si_el_texto_viejo_no_esta_lo_dice(carpeta):
    """Esto ya se portaba bien el 2026-09-05 y no se puede perder."""
    p = _archivo(carpeta, "pieza.py", "def hola():\n    return 1\n")
    ok, msg = aplicador.aplicar_cambio(
        {"archivo": p, "texto_viejo": "ESTO NO ESTA", "texto_nuevo": "x"})
    assert not ok, "dijo que aplico un texto que no estaba en el archivo"
    assert "no aparece" in str(msg).lower()


# ------------------------------------------------- EL FALLO DEL 2026-09-05

def test_un_CAMBIO_no_puede_CREAR_un_archivo_que_no_existe(carpeta):
    """LA CAUSA DEL EXITO SILENCIOSO.

    Si la propuesta trae texto_viejo, es un CAMBIO sobre algo que ya existe. Si el archivo no
    esta ahi, la ruta esta mal: NO se crea nada, se avisa. Crearlo convierte un error de ruta en
    un exito, y siembra archivos huerfanos en la carpeta equivocada.
    """
    fantasma = os.path.join(carpeta, "no_existe.py")
    ok, msg = aplicador.aplicar_cambio(
        {"archivo": fantasma, "texto_viejo": "return 1", "texto_nuevo": "return 2"})
    assert not ok, (
        "CREO un archivo que no existia cuando lo que se pedia era CAMBIAR uno. Asi es como el "
        "2026-09-05 nacio un archivo de Foto Informe dentro de la carpeta del Ingeniero y se "
        "anuncio APLICADO")
    assert not os.path.exists(fantasma), "ademas lo dejo escrito en el disco"


def test_el_aviso_dice_QUE_HACER_no_solo_que_fallo(carpeta):
    """Un aviso que no dice que hacer empuja a repetir el error."""
    fantasma = os.path.join(carpeta, "no_existe.py")
    _ok, msg = aplicador.aplicar_cambio(
        {"archivo": fantasma, "texto_viejo": "return 1", "texto_nuevo": "return 2"})
    m = str(msg).lower()
    assert "ruta" in m or "carpeta" in m or "proyecto" in m, (
        "el aviso no apunta a que el problema es la RUTA; sin eso, quien lo lea buscara el fallo "
        "en el sitio equivocado")


def test_despues_de_escribir_se_COMPRUEBA_que_quedo(carpeta):
    """Julio, 2026-09-05: 'si, que el sistema lo compruebe'.

    Se le da un archivo que se puede leer pero NO se puede escribir. Si el aplicador dice que si
    sin comprobar, aqui se cae.
    """
    p = _archivo(carpeta, "solo_lectura.py", "def hola():\n    return 1\n")
    os.chmod(p, 0o444)
    try:
        ok, _msg = aplicador.aplicar_cambio(
            {"archivo": p, "texto_viejo": "return 1", "texto_nuevo": "return 2"})
        quedo = "return 2" in open(p, encoding="utf-8").read()
        assert ok == quedo, (
            "lo que dice y lo que hay en el disco NO coinciden: dijo %s y en el archivo el cambio "
            "%s. Anunciar una escritura que no ocurrio es lo que hace que quien viene detras "
            "trabaje sobre algo que no existe" % (ok, "SI esta" if quedo else "NO esta"))
    finally:
        os.chmod(p, 0o666)


def test_queda_registro_de_cada_aplicacion(carpeta):
    """El 2026-09-05 no habia forma de saber cuantas veces habia pasado esto: no hay libreta."""
    p = _archivo(carpeta, "pieza.py", "def hola():\n    return 1\n")
    aplicador.aplicar_cambio({"archivo": p, "texto_viejo": "return 1", "texto_nuevo": "return 3"})
    libreta = os.path.join(AQUI, "memoria", "APLICACIONES.log")
    assert os.path.exists(libreta), (
        "no hay libreta de lo que se ha aplicado. Sin ella no se puede saber cuantas veces se "
        "anuncio una escritura que no ocurrio, ni donde quedaron los archivos huerfanos")
    with open(libreta, encoding="utf-8", errors="replace") as f:
        ultimas = f.read()
    assert "pieza.py" in ultimas, "la libreta no apunta que archivo se toco"
