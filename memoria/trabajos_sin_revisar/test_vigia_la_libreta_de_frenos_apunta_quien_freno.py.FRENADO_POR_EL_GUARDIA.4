import importlib.util
import os
import shutil
import tempfile
import unittest


# Esta vigia nace ROJA a proposito: la pieza arnes/libreta_de_frenos.py
# todavia no existe. Cuando se escriba con el contrato cerrado (apuntar y leer,
# cuatro claves exactas, carpeta propia), los cuatro casos pasan a verde sin
# tocar este archivo.


def _ruta_de_la_libreta():
    # Se arma la ruta partiendo de la carpeta de ESTA prueba, nunca por nombre
    # de paquete: hay dos proyectos con carpetas que se llaman igual.
    aqui = os.path.dirname(os.path.abspath(__file__))
    raiz = os.path.dirname(aqui)
    return os.path.join(raiz, "arnes", "libreta_de_frenos.py")


def _cargar_libreta():
    ruta = _ruta_de_la_libreta()
    if not os.path.isfile(ruta):
        raise AssertionError(
            "la libreta de frenos no existe todavia en " + ruta +
            "; esta vigia nace ROJA a proposito y pasara a verde cuando la pieza se escriba"
        )
    especificacion = importlib.util.spec_from_file_location(
        "libreta_de_frenos_bajo_prueba", ruta
    )
    if especificacion is None or especificacion.loader is None:
        raise AssertionError("no se pudo cargar la libreta de frenos desde " + ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)
    return modulo


class TestVigiaLaLibretaDeFrenos(unittest.TestCase):

    def setUp(self):
        # La prueba usa SIEMPRE su propia carpeta. Nunca la memoria de verdad.
        self.carpeta = tempfile.mkdtemp(prefix="libreta_de_frenos_prueba_")

    def tearDown(self):
        shutil.rmtree(self.carpeta, ignore_errors=True)

    def test_caso_1_la_libreta_existe_y_tiene_sus_dos_funciones(self):
        # Vigila: que la libreta exista y traiga apuntar y leer, y se puedan llamar.
        libreta = _cargar_libreta()
        self.assertTrue(hasattr(libreta, "apuntar"), "falta la funcion apuntar")
        self.assertTrue(hasattr(libreta, "leer"), "falta la funcion leer")
        self.assertTrue(callable(getattr(libreta, "apuntar")), "apuntar no se puede llamar")
        self.assertTrue(callable(getattr(libreta, "leer")), "leer no se puede llamar")

    def test_caso_2_un_freno_apuntado_deja_los_tres_datos_escritos(self):
        # Vigila: que un freno apuntado deje cuando, quien_freno e instruccion, y mudo falso.
        libreta = _cargar_libreta()
        libreta.apuntar("candado_de_prueba", "hacer tal cosa", carpeta=self.carpeta)
        renglones = libreta.leer(carpeta=self.carpeta)
        self.assertEqual(len(renglones), 1, "deberia haber un solo renglon apuntado")
        renglon = renglones[0]
        self.assertIn("cuando", renglon)
        self.assertIn("quien_freno", renglon)
        self.assertIn("instruccion", renglon)
        self.assertIn("mudo", renglon)
        self.assertTrue(str(renglon["cuando"]).strip() != "", "cuando vino vacio")
        self.assertEqual(renglon["quien_freno"], "candado_de_prueba")
        self.assertEqual(renglon["instruccion"], "hacer tal cosa")
        self.assertFalse(renglon["mudo"], "un freno con los tres datos no es mudo")

    def test_caso_3_un_freno_sin_los_tres_datos_sale_marcado_como_mudo(self):
        # Vigila: que falte quien_freno o falte instruccion deje el renglon en mudo verdadero.
        libreta = _cargar_libreta()
        libreta.apuntar("", "hacer tal cosa", carpeta=self.carpeta)
        libreta.apuntar("candado_de_prueba", "", carpeta=self.carpeta)
        renglones = libreta.leer(carpeta=self.carpeta)
        self.assertEqual(len(renglones), 2, "deberian volver dos renglones")
        primero, segundo = renglones[0], renglones[1]
        self.assertTrue(primero["mudo"], "el renglon sin quien_freno deberia ser mudo")
        self.assertTrue(segundo["mudo"], "el renglon sin instruccion deberia ser mudo")
        self.assertEqual(primero["quien_freno"], "")
        self.assertEqual(primero["instruccion"], "hacer tal cosa")
        self.assertEqual(segundo["quien_freno"], "candado_de_prueba")
        self.assertEqual(segundo["instruccion"], "")
        self.assertNotEqual(
            (primero["quien_freno"], primero["instruccion"]),
            (segundo["quien_freno"], segundo["instruccion"]),
            "los dos renglones mudos deben distinguirse entre si",
        )

    def test_caso_4_la_libreta_no_escribe_en_la_memoria_de_verdad(self):
        # Vigila: que al pasarle la carpeta de la prueba, el archivo quede AHI y no en la memoria real.
        libreta = _cargar_libreta()
        libreta.apuntar("candado_de_prueba", "hacer tal cosa", carpeta=self.carpeta)
        escritos = []
        for nombre in os.listdir(self.carpeta):
            ruta = os.path.join(self.carpeta, nombre)
            if os.path.isfile(ruta):
                escritos.append(ruta)
        self.assertTrue(
            len(escritos) > 0,
            "no quedo ningun archivo en la carpeta de la prueba: la libreta escribio en otro sitio",
        )
        aqui = os.path.dirname(os.path.abspath(__file__))
        raiz = os.path.dirname(aqui)
        memoria_real = os.path.join(raiz, "memoria")
        for ruta in escritos:
            self.assertTrue(
                os.path.abspath(ruta).startswith(os.path.abspath(self.carpeta)),
                "un archivo de la prueba se fue fuera de su carpeta: " + ruta,
            )
            self.assertFalse(
                os.path.abspath(ruta).startswith(os.path.abspath(memoria_real)),
                "la prueba escribio en la memoria de verdad: " + ruta,
            )


if __name__ == "__main__":
    unittest.main()
