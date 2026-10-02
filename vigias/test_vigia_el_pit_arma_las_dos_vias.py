# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_pit_arma_las_dos_vias.py

VIGIA — EL PIT ARMA LAS DOS VIAS (CONTRATO_LAS_DOS_VIAS, Julio 2026-10-01).

QUE VIGILA:
  Que al lanzar al equipo, el capataz arme DOS entregas separadas:
    - la GUIA (el texto del encargo, lo que hay que hacer), y
    - el CODIGO (el programa de las dos vias, el trozo .py que hay que tocar),
  y las entregue POR SEPARADO, en vez de mandar solo el texto del encargo.

COMO LO VIGILA (sin mirar el texto del codigo, ejecutando de verdad):
  Se llama a cuerpo.capataz.lanzar_al_equipo con una orden que trae 'encargo' y 'pieza',
  en una carpeta temporal, y se comprueba con un assert que el capataz deja DOS
  entregas separadas (guia y codigo) y que el codigo lleva el programa de la pieza.

NACE ROJA HOY:
  Porque lanzar_al_equipo solo pasa orden['encargo'] al subproceso y los campos
  'pieza' y 'repara' de la orden nunca llegan. Si la pieza aun no existe, el
  import falla y la prueba nace roja por ese import, que es lo que se pide.

PASA CUANDO:
  El capataz arma la guia y el codigo por separado y los entrega en dos sitios
  distintos (por ejemplo, dos archivos o dos claves distintas en el resultado).
"""
import os
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


# ---------------------------------------------------------------------------
# Ayudas: se arma una orden de mentira y una pieza .py de mentira, en una
# carpeta temporal, para no tocar el estado real del proyecto.
# ---------------------------------------------------------------------------

PROGRAMA_DE_LA_PIEZA = (
    "# -*- coding: utf-8 -*-\n"
    "def sumar(a, b):\n"
    "    return a + b\n"
)


def _orden_de_mentira(carpeta, pieza_relativa):
    """Devuelve una orden con encargo (guia) y pieza (codigo) bien separados."""
    return {
        "id": "VIGIA-DOS-VIAS-1",
        "encargo": "Arregla la funcion sumar para que devuelva la suma.",
        "pieza": pieza_relativa,
        "repara": "sumar devuelve mal",
        "crear": False,
    }


def _escribir_pieza(carpeta, pieza_relativa, contenido):
    ruta = os.path.join(carpeta, pieza_relativa)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def _entregas_del_capataz(resultado):
    """Saca del resultado las DOS entregas separadas: guia y codigo.

    Se aceptan varias formas razonables de nombrarlas, porque lo que importa
    es que vayan SEPARADAS, no como se llamen las claves.
    """
    if not isinstance(resultado, dict):
        return (None, None)
    guia = None
    codigo = None
    for clave in ("guia", "guía", "encargo", "texto_guia"):
        if clave in resultado and resultado[clave]:
            guia = resultado[clave]
            break
    for clave in ("codigo", "código", "pieza", "texto_codigo", "programa"):
        if clave in resultado and resultado[clave]:
            codigo = resultado[clave]
            break
    return (guia, codigo)


def _archivos_de_entrega(carpeta):
    """Busca en la carpeta temporal los archivos de entrega que deje el capataz.

    Se aceptan nombres con 'guia' y con 'codigo' (o 'pieza'), en cualquier
    combinacion de mayusculas y separadores.
    """
    guia = None
    codigo = None
    for nombre in os.listdir(carpeta):
        bajo = nombre.lower()
        ruta = os.path.join(carpeta, nombre)
        if not os.path.isfile(ruta):
            continue
        if "guia" in bajo and guia is None:
            guia = ruta
        if ("codigo" in bajo or "pieza" in bajo) and codigo is None:
            codigo = ruta
    return (guia, codigo)


# ---------------------------------------------------------------------------
# LA PRUEBA UNICA
# ---------------------------------------------------------------------------

def test_el_pit_arma_las_dos_vias_y_las_entrega_por_separado():
    """Al lanzar al equipo, el capataz arma guia y codigo y los entrega aparte.

    Se ejecuta de verdad (carpeta temporal, sin tocar el estado real) y se
    comprueba con un assert que hay DOS entregas separadas: la guia con el
    texto del encargo y el codigo con el programa de la pieza.
    """
    from cuerpo import capataz

    with tempfile.TemporaryDirectory() as carpeta:
        pieza_relativa = os.path.join("piezas", "sumar.py")
        _escribir_pieza(carpeta, pieza_relativa, PROGRAMA_DE_LA_PIEZA)
        orden = _orden_de_mentira(carpeta, pieza_relativa)

        resultado = capataz.lanzar_al_equipo(
            "proyecto_de_prueba",
            orden,
            tope_segundos=1,
            carpeta=carpeta,
        )

        guia, codigo = _entregas_del_capataz(resultado)
        if guia is None or codigo is None:
            ruta_guia, ruta_codigo = _archivos_de_entrega(carpeta)
            if guia is None and ruta_guia is not None:
                with open(ruta_guia, encoding="utf-8", errors="replace") as f:
                    guia = f.read()
            if codigo is None and ruta_codigo is not None:
                with open(ruta_codigo, encoding="utf-8", errors="replace") as f:
                    codigo = f.read()

        assert guia is not None, (
            "el capataz no entrego la GUIA por separado: "
            "solo manda el texto del encargo mezclado"
        )
        assert codigo is not None, (
            "el capataz no entrego el CODIGO por separado: "
            "los campos pieza y repara de la orden nunca llegan"
        )
        assert guia != codigo, (
            "la guia y el codigo son la misma entrega: "
            "no se armaron las dos vias por separado"
        )
        assert "sumar" in codigo, (
            "el codigo entregado no lleva el programa de la pieza: "
            "no es el programa de las dos vias"
        )
        assert "Arregla la funcion sumar" in guia, (
            "la guia entregada no lleva el texto del encargo"
        )
