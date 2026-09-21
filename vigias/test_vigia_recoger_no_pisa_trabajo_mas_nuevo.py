"""Vigia: recoger NO pisa un trabajo del proyecto mas nuevo que la copia apartada.

Vigila la funcion recoger de arnes/recoger_los_pedazos.py.

Dos situaciones, montadas en una carpeta temporal cambiando las fechas de los archivos:

  1. La copia apartada es MAS VIEJA que el archivo que hay ahora en el proyecto.
     En ese caso recoger NO debe tocar nada: ni el archivo del proyecto, ni la copia
     apartada. Y debe avisar con una razon que diga que el archivo del proyecto es
     mas nuevo.

  2. La copia apartada es MAS NUEVA que el archivo que hay ahora en el proyecto.
     En ese caso recoger SI debe devolver la copia a su sitio, como hasta hoy, y
     marcar la copia apartada como recogida.

No se toca ningun otro archivo: todo ocurre dentro de una carpeta temporal.
"""

import json
import os
import shutil
import sys
import tempfile
import time
import unittest


# La raiz del proyecto, para poder importar arnes.recoger_los_pedazos.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from arnes import recoger_los_pedazos as rlp  # noqa: E402


# Nombre base del archivo que se va a recoger, sin el sufijo .FRENADO_POR_EL_GUARDIA.
NOMBRE_BASE = "pieza_de_prueba.py"

# Nombre de la copia apartada tal y como la deja el guardia.
NOMBRE_FRENADO = NOMBRE_BASE + rlp.SUFIJO_FRENADO

# Ruta relativa del archivo dentro del proyecto de mentira.
RUTA_EN_PROYECTO = os.path.join("cuerpo", NOMBRE_BASE)

# Contenido de la copia apartada (lo que el guardia freno).
CONTENIDO_APARTADO = "# copia buena apartada por el guardia\nVALOR = 'apartado'\n"

# Contenido que hay ahora en el proyecto.
CONTENIDO_PROYECTO = "# lo que hay ahora en el proyecto\nVALOR = 'proyecto'\n"


class TestVigiaRecogerNoPisaTrabajoMasNuevo(unittest.TestCase):
    """Prueba que recoger respeta el trabajo mas nuevo del proyecto."""

    def setUp(self):
        """Monta una raiz temporal con su memoria y su proyecto de mentira."""
        self.raiz = tempfile.mkdtemp(prefix="vigia_recoger_")
        self.addCleanup(shutil.rmtree, self.raiz, ignore_errors=True)

        # Carpetas de la memoria que usa recoger_los_pedazos.
        self.carpeta_sin_revisar = os.path.join(
            self.raiz, rlp.CARPETA_SIN_REVISAR
        )
        self.carpeta_del_equipo = os.path.join(
            self.raiz, rlp.CARPETA_DEL_EQUIPO
        )
        os.makedirs(self.carpeta_sin_revisar, exist_ok=True)
        os.makedirs(self.carpeta_del_equipo, exist_ok=True)

        # El archivo del proyecto, con su carpeta.
        self.ruta_proyecto = os.path.join(self.raiz, RUTA_EN_PROYECTO)
        os.makedirs(os.path.dirname(self.ruta_proyecto), exist_ok=True)
        with open(self.ruta_proyecto, "w", encoding="utf-8") as f:
            f.write(CONTENIDO_PROYECTO)

        # La copia apartada, con el sufijo que deja el guardia.
        self.ruta_apartada = os.path.join(
            self.carpeta_sin_revisar, NOMBRE_FRENADO
        )
        with open(self.ruta_apartada, "w", encoding="utf-8") as f:
            f.write(CONTENIDO_APARTADO)

        # El aprobado que dice de donde venia la copia. El nombre del aprobado
        # lleva la palabra APROBADO y el nombre base del archivo, para que
        # donde_iba lo encuentre.
        self.ruta_aprobado = os.path.join(
            self.carpeta_del_equipo,
            "APROBADO_" + NOMBRE_BASE + ".json",
        )
        aprobado = {
            "propuesta": {
                "archivo": RUTA_EN_PROYECTO,
            }
        }
        with open(self.ruta_aprobado, "w", encoding="utf-8") as f:
            json.dump(aprobado, f)

    def _poner_fecha(self, ruta, segundos):
        """Pone la fecha de modificacion de un archivo a un instante dado."""
        os.utime(ruta, (segundos, segundos))

    def _leer(self, ruta):
        """Lee un archivo de texto y devuelve su contenido."""
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()

    def test_no_pisa_si_el_proyecto_es_mas_nuevo(self):
        """Si el archivo del proyecto es mas nuevo, recoger no toca nada."""
        ahora = time.time()
        # La copia apartada es MAS VIEJA que el archivo del proyecto.
        self._poner_fecha(self.ruta_apartada, ahora - 3600)
        self._poner_fecha(self.ruta_proyecto, ahora)

        resultado = rlp.recoger(self.raiz, NOMBRE_FRENADO)

        # No se toca nada: ni el archivo del proyecto, ni la copia apartada.
        self.assertFalse(
            resultado.get("ok"),
            "recoger no debe devolver ok cuando el proyecto es mas nuevo: "
            + repr(resultado),
        )
        self.assertEqual(
            self._leer(self.ruta_proyecto),
            CONTENIDO_PROYECTO,
            "el archivo del proyecto no debe cambiar cuando es mas nuevo",
        )
        self.assertTrue(
            os.path.isfile(self.ruta_apartada),
            "la copia apartada no debe desaparecer cuando no se recoge",
        )
        self.assertEqual(
            self._leer(self.ruta_apartada),
            CONTENIDO_APARTADO,
            "la copia apartada no debe cambiar cuando no se recoge",
        )
        # Y se avisa con la razon: el archivo del proyecto es mas nuevo.
        razon = str(resultado.get("razon", "")).lower()
        self.assertIn(
            "mas nuevo",
            razon,
            "la razon debe decir que el archivo del proyecto es mas nuevo: "
            + repr(resultado.get("razon")),
        )

    def test_devuelve_si_la_copia_es_mas_nueva(self):
        """Si la copia apartada es mas nueva, recoger la devuelve como hasta hoy."""
        ahora = time.time()
        # La copia apartada es MAS NUEVA que el archivo del proyecto.
        self._poner_fecha(self.ruta_proyecto, ahora - 3600)
        self._poner_fecha(self.ruta_apartada, ahora)

        resultado = rlp.recoger(self.raiz, NOMBRE_FRENADO)

        self.assertTrue(
            resultado.get("ok"),
            "recoger debe devolver ok cuando la copia es mas nueva: "
            + repr(resultado),
        )
        # La copia buena volvio a su sitio.
        self.assertEqual(
            self._leer(self.ruta_proyecto),
            CONTENIDO_APARTADO,
            "el archivo del proyecto debe tener el contenido de la copia",
        )
        # La copia apartada quedo marcada como recogida, no borrada.
        self.assertFalse(
            os.path.isfile(self.ruta_apartada),
            "la copia apartada ya no debe estar con su nombre original",
        )
        self.assertTrue(
            os.path.isfile(self.ruta_apartada + rlp.SUFIJO_RECOGIDO),
            "la copia apartada debe quedar marcada como recogida",
        )


if __name__ == "__main__":
    unittest.main()
