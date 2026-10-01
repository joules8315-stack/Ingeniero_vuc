import unittest
import os
import importlib.util
import shutil
import tempfile
import json

# Ruta de la pieza que se vigila
RUTA_PIEZA = 'arnes/bucle_del_plan.py'

class TestVigiaElBucleAprendeDelRechazo(unittest.TestCase):
    def setUp(self):
        # Crear un entorno de pruebas aislado
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Limpiar el entorno de pruebas
        shutil.rmtree(self.test_dir)

    def _cargar_pieza(self):
        # Regla: Cargar la pieza por RUTA, no por nombre de paquete
        if not os.path.exists(RUTA_PIEZA):
            raise ImportError('La pieza arnes/bucle_del_plan.py no existe todavia')
        
        spec = importlib.util.spec_from_file_location('bucle_del_plan', RUTA_PIEZA)
        modulo = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(modulo)
        except Exception as e:
            raise ImportError('No se pudo cargar la pieza: ' + str(e))
        return modulo

    def test_01_interfaz_existe(self):
        # CASO 1: la pieza existe y tiene las funciones publicas requeridas
        pieza = self._cargar_pieza()
        self.assertTrue(hasattr(pieza, 'listar_encargos'), 'Falta funcion listar_encargos')
        self.assertTrue(hasattr(pieza, 'extraer_motivos_rechazo'), 'Falta funcion extraer_motivos_rechazo')
        self.assertTrue(hasattr(pieza, 'insertar_motivos_en_encargo'), 'Falta funcion insertar_motivos_en_encargo')
        self.assertTrue(hasattr(pieza, 'correr_bucle'), 'Falta funcion correr_bucle para el caso 5')

    def test_02_orden_alfabetico_nombres(self):
        # CASO 2: los encargos salen EN ORDEN por nombre, no por fecha
        pieza = self._cargar_pieza()
        
        # Crear archivos con nombres desordenados
        nombres_creacion = ['paso_1b.txt', 'paso_0a.txt', 'paso_1a.txt']
        for nombre in nombres_creacion:
            ruta = os.path.join(self.test_dir, nombre)
            with open(ruta, 'w') as f:
                f.write('contenido del encargo')

        lista_rutas = pieza.listar_encargos(self.test_dir)
        nombres_obtenidos = [os.path.basename(p) for p in lista_rutas]
        
        # El orden correcto es 0a, 1a, 1b
        self.assertEqual(nombres_obtenidos, ['paso_0a.txt', 'paso_1a.txt', 'paso_1b.txt'])

    def test_03_extraer_motivos_reales(self):
        # CASO 3: saca los motivos de un rechazo de verdad desde una ficha
        pieza = self._cargar_pieza()
        
        ficha_mentira = os.path.join(self.test_dir, 'rechazo_archivado.json')
        datos_rechazo = {
            'auditoria': {
                'motivos': ['La propuesta NO trae texto_nuevo', 'Falta el import os']
            }
        }
        with open(ficha_mentira, 'w') as f:
            json.dump(datos_rechazo, f)

        motivos = pieza.extraer_motivos_rechazo(ficha_mentira)
        self.assertEqual(len(motivos), 2)
        self.assertIn('La propuesta NO trae texto_nuevo', motivos)
        self.assertIn('Falta el import os', motivos)

    def test_04_reemplazo_no_acumulacion(self):
        # CASO 4: pega el rechazo y lo REEMPLAZA, no lo acumula
        pieza = self._cargar_pieza()
        
        encargo_base = 'TAREA: Crear archivo X\nMATERIAL: Codigo base'
        
        # Primera tanda de motivos
        motivos_viejos = ['Error viejo 1', 'Error viejo 2']
        encargo_con_rechazo_1 = pieza.insertar_motivos_en_encargo(encargo_base, motivos_viejos)
        
        self.assertIn('Error viejo 1', encargo_con_rechazo_1)
        
        # Segunda tanda de motivos (debe borrar los viejos)
        motivos_nuevos = ['Error nuevo A', 'Error nuevo B']
        encargo_con_rechazo_2 = pieza.insertar_motivos_en_encargo(encargo_con_rechazo_1, motivos_nuevos)
        
        self.assertIn('Error nuevo A', encargo_con_rechazo_2)
        self.assertNotIn('Error viejo 1', encargo_con_rechazo_2, 'Los motivos viejos no se borraron')
        
        # Verificar que no hay crecimiento descontrolado (no se acumulan bloques)
        # El tamaño no deberia ser mucho mayor que el original + motivos nuevos
        limite_esperado = len(encargo_base) + len(str(motivos_nuevos)) + 200
        self.assertLess(len(encargo_con_rechazo_2), limite_esperado, 'El encargo esta acumulando basura')

    def test_05_continuar_tras_fallo(self):
        # CASO 5: un paso que no entra NO para el bucle
        pieza = self._cargar_pieza()

        pasos_intentados = []
        
        def lanzador_sustituto(ruta_encargo):
            # El lanzador apunta que paso se intento
            nombre = os.path.basename(ruta_encargo)
            pasos_intentados.append(nombre)
            if 'paso_0' in nombre:
                # El primero falla siempre
                return False, 'Rechazado por el auditor'
            return True, 'Aprobado'

        # Crear dos encargos
        encargos = []
        for n in ['paso_0.txt', 'paso_1.txt']:
            p = os.path.join(self.test_dir, n)
            with open(p, 'w') as f: f.write('tarea')
            encargos.append(p)

        # Ejecutar el bucle con el lanzador inyectado
        # Se asume que correr_bucle recibe la lista y el lanzador
        pieza.correr_bucle(encargos, lanzador=lanzador_sustituto)

        # Verificar que se intentaron AMBOS pasos
        self.assertIn('paso_0.txt', pasos_intentados)
        self.assertIn('paso_1.txt', pasos_intentados)
        self.assertEqual(len(pasos_intentados), 2, 'El bucle se detuvo tras el primer fallo')

if __name__ == '__main__':
    unittest.main()