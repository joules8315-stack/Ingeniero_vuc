import importlib.util
import os
import sys
import tempfile
import unittest


# Ruta de la pieza que se vigila, cargada por RUTA y no por nombre de paquete.
# Hay dos proyectos con carpetas que se llaman igual y por nombre se agarra la equivocada.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
RUTA_PIEZA = os.path.join(RAIZ, "arnes", "cuaderno_de_la_ronda.py")

# Cuaderno de verdad del proyecto: la prueba NUNCA debe tocarlo.
RUTA_CUADERNO_REAL = os.path.join(RAIZ, "memoria", "HUELLAS_QUE_FALLARON.jsonl")


def cargar_pieza_por_ruta(ruta):
    # Carga un archivo .py por su ruta completa. Si no existe, lanza ImportError
    # con un mensaje en palabras simples: la pieza no existe todavia.
    if not os.path.isfile(ruta):
        raise ImportError(
            "La pieza no existe todavia: " + ruta +
            ". Esta vigia nace ROJA a proposito hasta que se escriba."
        )
    nombre = "cuaderno_de_la_ronda_bajo_prueba"
    especificacion = importlib.util.spec_from_file_location(nombre, ruta)
    if especificacion is None or especificacion.loader is None:
        raise ImportError("No se pudo cargar la pieza por su ruta: " + ruta)
    modulo = importlib.util.module_from_spec(especificacion)
    sys.modules[nombre] = modulo
    especificacion.loader.exec_module(modulo)
    return modulo


def tamano_si_existe(ruta):
    # Devuelve el tamano del archivo, o -1 si no existe. Sirve para comprobar
    # que el cuaderno de verdad no crecio ni un byte durante la prueba.
    if not os.path.isfile(ruta):
        return -1
    return os.path.getsize(ruta)


class TestVigiaElCuadernoEstaConectadoALaRonda(unittest.TestCase):

    def setUp(self):
        # Carpeta aparte para que la pieza escriba ahi y no en la memoria real.
        # Lo unico que se sustituye es la CARPETA donde se escribe.
        self.carpeta = tempfile.mkdtemp(prefix="vigia_cuaderno_ronda_")
        self.raiz_falsa = self.carpeta
        self.tamano_real_antes = tamano_si_existe(RUTA_CUADERNO_REAL)

    def tearDown(self):
        # Nada que borrar a mano: la carpeta es temporal. Pero se comprueba
        # que el cuaderno de verdad no cambio, pase lo que pase.
        tamano_real_despues = tamano_si_existe(RUTA_CUADERNO_REAL)
        self.assertEqual(
            self.tamano_real_antes,
            tamano_real_despues,
            "El cuaderno de verdad del proyecto cambio durante la prueba. "
            "Una prueba NUNCA debe escribir en la memoria real."
        )

    def test_caso_1_la_pieza_existe_y_tiene_sus_dos_funciones(self):
        # Vigila: la pieza existe y tiene antes_de_lanzar y despues_de_la_ronda.
        pieza = cargar_pieza_por_ruta(RUTA_PIEZA)
        self.assertTrue(
            hasattr(pieza, "antes_de_lanzar"),
            "Falta la funcion antes_de_lanzar en la pieza."
        )
        self.assertTrue(
            hasattr(pieza, "despues_de_la_ronda"),
            "Falta la funcion despues_de_la_ronda en la pieza."
        )
        self.assertTrue(callable(getattr(pieza, "antes_de_lanzar")))
        self.assertTrue(callable(getattr(pieza, "despues_de_la_ronda")))

    def test_caso_2_un_camino_nuevo_no_figura_como_fallido(self):
        # Vigila: un camino que nadie intento nunca no figura como fallido.
        pieza = cargar_pieza_por_ruta(RUTA_PIEZA)
        encargo = "encargo de mentira que nadie intento nunca"
        pieza_tocada = "arnes/pieza_de_mentira_nueva.py"
        resultado = pieza.antes_de_lanzar(encargo, pieza_tocada, self.raiz_falsa)
        self.assertIsInstance(resultado, dict)
        self.assertIn("ya_fallo", resultado)
        self.assertIn("motivo", resultado)
        self.assertFalse(resultado["ya_fallo"])
        self.assertEqual(resultado["motivo"], "")

    def test_caso_3_un_camino_que_fallo_queda_apuntado_y_se_reconoce(self):
        # Vigila: lo que falla queda apuntado y despues se reconoce con su motivo.
        pieza = cargar_pieza_por_ruta(RUTA_PIEZA)
        encargo = "encargo de mentira que si fallo"
        pieza_tocada = "arnes/pieza_de_mentira_que_fallo.py"
        motivo = "motivo de mentira: la pieza no compilaba"
        apuntado = pieza.despues_de_la_ronda(
            encargo, pieza_tocada, motivo, self.raiz_falsa
        )
        self.assertTrue(apuntado, "La ronda fallida no quedo apuntada.")
        resultado = pieza.antes_de_lanzar(encargo, pieza_tocada, self.raiz_falsa)
        self.assertTrue(resultado["ya_fallo"])
        self.assertEqual(resultado["motivo"], motivo)

    def test_caso_4_una_ronda_que_salio_bien_no_se_apunta(self):
        # Vigila: una ronda que salio bien NO se apunta como camino fallido.
        pieza = cargar_pieza_por_ruta(RUTA_PIEZA)
        encargo = "encargo de mentira que salio bien"
        pieza_tocada = "arnes/pieza_de_mentira_que_salio_bien.py"
        ruta_cuaderno_falso = os.path.join(
            self.raiz_falsa, "memoria", "HUELLAS_QUE_FALLARON.jsonl"
        )
        tamano_antes = tamano_si_existe(ruta_cuaderno_falso)
        apuntado = pieza.despues_de_la_ronda(
            encargo, pieza_tocada, "", self.raiz_falsa
        )
        self.assertFalse(apuntado, "Una ronda buena no debe apuntarse.")
        tamano_despues = tamano_si_existe(ruta_cuaderno_falso)
        self.assertEqual(
            tamano_antes,
            tamano_despues,
            "El cuaderno crecio aunque la ronda salio bien."
        )

    def test_caso_5_la_pieza_no_escribe_en_el_cuaderno_de_verdad(self):
        # Vigila: la pieza escribe en la carpeta que se le pasa, no en la memoria real.
        pieza = cargar_pieza_por_ruta(RUTA_PIEZA)
        encargo = "encargo de mentira para el caso cinco"
        pieza_tocada = "arnes/pieza_de_mentira_caso_cinco.py"
        motivo = "motivo de mentira para el caso cinco"
        pieza.despues_de_la_ronda(encargo, pieza_tocada, motivo, self.raiz_falsa)
        tamano_real_despues = tamano_si_existe(RUTA_CUADERNO_REAL)
        self.assertEqual(
            self.tamano_real_antes,
            tamano_real_despues,
            "La pieza escribio en el cuaderno de verdad del proyecto. "
            "Eso ya costo caro dos veces: 27 de 32 errores aprendidos perdidos "
            "y 535 apariciones de un dato de mentira en el diccionario."
        )


if __name__ == "__main__":
    unittest.main()
