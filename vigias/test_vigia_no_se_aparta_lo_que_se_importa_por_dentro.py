# -*- coding: utf-8 -*-
"""vigias/test_vigia_no_se_aparta_lo_que_se_importa_por_dentro.py

VIGIA de arnes/revisor_de_programa.py.

QUE VIGILA
-----------
Que el revisor FRENE una prueba nueva que hace monkeypatch.setattr sobre un modulo
pidiendo un nombre que ese modulo NO importa arriba del archivo. El caso tipico:
un archivo que hace 'import shutil' DENTRO de una funcion, y una prueba nueva que
intenta apartar 'shutil' con monkeypatch.setattr(modulo, 'shutil', falso). Eso
revienta al correr y no mide nada: el nombre no existe en el modulo a nivel de
archivo, asi que setattr falla con AttributeError.

Y que NO FRENE cuando el nombre SI esta importado arriba del archivo.

COMO SE MONTA
-------------
Todo en una carpeta temporal: un modulo de mentira y una prueba de mentira. No se
toca ningun archivo del proyecto.

POR QUE NACE
------------
La cuenta 3b del revisor (importar arriba algo que no existe en su modulo) ya existe
en el codigo, pero no tenia vigia propia. Una reparacion sin vigia que se ponga roja
al sabotearla no esta protegida.
"""
import os
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from arnes import revisor_de_programa  # noqa: E402


# ---------------------------------------------------------------------------
# Utilidades para montar los archivos de mentira en una carpeta temporal
# ---------------------------------------------------------------------------

def _escribir(ruta, texto):
    """Escribe un archivo de texto, creando la carpeta si hace falta."""
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


def _propuesta(ruta, viejo, nuevo):
    """Arma la propuesta tal como la espera el revisor."""
    return {"archivo": ruta, "texto_viejo": viejo, "texto_nuevo": nuevo}


# ---------------------------------------------------------------------------
# CASO 1 — FRENA: monkeypatch.setattr sobre un nombre que el modulo NO importa arriba
# ---------------------------------------------------------------------------

def test_frena_monkeypatch_sobre_nombre_no_importado_arriba():
    """El modulo importa shutil DENTRO de una funcion, no arriba.

    La prueba nueva hace monkeypatch.setattr(modulo, 'shutil', falso). Eso revienta
    con AttributeError y no mide nada. El revisor tiene que FRENARLO y explicarlo.
    """
    with tempfile.TemporaryDirectory() as tmp:
        ruta_mod = os.path.join(tmp, "modulo_de_mentira.py")
        ruta_prueba = os.path.join(tmp, "test_prueba_de_mentira.py")

        # El modulo: shutil se importa DENTRO de la funcion, no arriba.
        _escribir(ruta_mod, (
            "# -*- coding: utf-8 -*-\n"
            "def copiar_algo(origen, destino):\n"
            "    import shutil\n"
            "    shutil.copy(origen, destino)\n"
        ))

        # La prueba vieja: existe, pero no toca shutil.
        viejo = (
            "# -*- coding: utf-8 -*-\n"
            "import modulo_de_mentira\n"
            "\n"
            "def test_copiar_algo():\n"
            "    assert modulo_de_mentira is not None\n"
        )
        _escribir(ruta_prueba, viejo)

        # La prueba nueva: aparta shutil con monkeypatch, pero el modulo no lo importa arriba.
        nuevo = (
            "# -*- coding: utf-8 -*-\n"
            "import modulo_de_mentira\n"
            "\n"
            "def test_copiar_algo(monkeypatch):\n"
            "    monkeypatch.setattr(modulo_de_mentira, 'shutil', None)\n"
            "    assert modulo_de_mentira is not None\n"
        )

        fallos = revisor_de_programa.revisar(
            _propuesta(ruta_prueba, viejo, nuevo),
            tarea="anadir prueba que aparta shutil en modulo_de_mentira",
        )

        assert fallos, (
            "El revisor NO freno una prueba que aparta 'shutil' en un modulo que no lo "
            "importa arriba. Esa prueba revienta con AttributeError y no mide nada."
        )
        texto = " ".join(fallos).lower()
        assert "shutil" in texto, (
            "El revisor freno, pero no dijo que el nombre que se aparta ('shutil') no "
            "existe en el modulo. Fallos: %r" % (fallos,)
        )


# ---------------------------------------------------------------------------
# CASO 2 — NO FRENA: el nombre SI esta importado arriba del archivo
# ---------------------------------------------------------------------------

def test_no_frena_monkeypatch_sobre_nombre_si_importado_arriba():
    """El modulo importa shutil ARRIBA. Apartarlo con monkeypatch es legitimo.

    El revisor NO debe frenar: el nombre existe en el modulo a nivel de archivo.
    """
    with tempfile.TemporaryDirectory() as tmp:
        ruta_mod = os.path.join(tmp, "modulo_de_mentira.py")
        ruta_prueba = os.path.join(tmp, "test_prueba_de_mentira.py")

        # El modulo: shutil importado ARRIBA.
        _escribir(ruta_mod, (
            "# -*- coding: utf-8 -*-\n"
            "import shutil\n"
            "\n"
            "def copiar_algo(origen, destino):\n"
            "    shutil.copy(origen, destino)\n"
        ))

        viejo = (
            "# -*- coding: utf-8 -*-\n"
            "import modulo_de_mentira\n"
            "\n"
            "def test_copiar_algo():\n"
            "    assert modulo_de_mentira is not None\n"
        )
        _escribir(ruta_prueba, viejo)

        nuevo = (
            "# -*- coding: utf-8 -*-\n"
            "import modulo_de_mentira\n"
            "\n"
            "def test_copiar_algo(monkeypatch):\n"
            "    monkeypatch.setattr(modulo_de_mentira, 'shutil', None)\n"
            "    assert modulo_de_mentira is not None\n"
        )

        fallos = revisor_de_programa.revisar(
            _propuesta(ruta_prueba, viejo, nuevo),
            tarea="anadir prueba que aparta shutil en modulo_de_mentira",
        )

        # Se mira solo lo que tiene que ver con el nombre que se aparta: el revisor puede
        # frenar por otras cuentas legitimas (por ejemplo, si la tarea nombra algo que no
        # aparece). Lo que NO puede es acusar a 'shutil' de no existir.
        acusaciones_shutil = [f for f in fallos if "shutil" in f.lower()]
        assert not acusaciones_shutil, (
            "El revisor FRENO en falso: 'shutil' SI esta importado arriba del modulo, "
            "asi que apartarlo con monkeypatch es legitimo. Fallos: %r" % (fallos,)
        )


# ---------------------------------------------------------------------------
# CASO 3 — NO FRENA si el modulo no se puede leer (cuando no se puede comprobar, se calla)
# ---------------------------------------------------------------------------

def test_no_frena_si_el_modulo_no_se_puede_leer():
    """Si el modulo no existe o no se puede leer, el revisor NO debe acusar.

    Cuando no se puede comprobar, callar es mas honrado que gritar.
    """
    with tempfile.TemporaryDirectory() as tmp:
        ruta_prueba = os.path.join(tmp, "test_prueba_de_mentira.py")

        viejo = (
            "# -*- coding: utf-8 -*-\n"
            "import modulo_que_no_existe\n"
            "\n"
            "def test_algo():\n"
            "    assert True\n"
        )
        _escribir(ruta_prueba, viejo)

        nuevo = (
            "# -*- coding: utf-8 -*-\n"
            "import modulo_que_no_existe\n"
            "\n"
            "def test_algo(monkeypatch):\n"
            "    monkeypatch.setattr(modulo_que_no_existe, 'shutil', None)\n"
            "    assert True\n"
        )

        fallos = revisor_de_programa.revisar(
            _propuesta(ruta_prueba, viejo, nuevo),
            tarea="anadir prueba que aparta shutil en modulo_que_no_existe",
        )

        acusaciones_shutil = [f for f in fallos if "shutil" in f.lower()]
        assert not acusaciones_shutil, (
            "El revisor acuso a 'shutil' cuando el modulo no se puede leer: no se puede "
            "comprobar, asi que debe callar. Fallos: %r" % (fallos,)
        )


if __name__ == "__main__":
    test_frena_monkeypatch_sobre_nombre_no_importado_arriba()
    test_no_frena_monkeypatch_sobre_nombre_si_importado_arriba()
    test_no_frena_si_el_modulo_no_se_puede_leer()
    print("vigia no_se_aparta_lo_que_se_importa_por_dentro: OK")
