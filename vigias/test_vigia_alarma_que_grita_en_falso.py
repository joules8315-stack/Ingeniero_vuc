"""VIGIA: una alarma que grita en falso se arregla o se apaga.

Esta vigia le pone guardian a CONTRATO_ALARMA_QUE_GRITA_EN_FALSO.md, que hasta
ahora era solo papel. La ley dice que una alarma que suena sin motivo ensena a
ignorarla, y el dia que suene de verdad nadie le hara caso. Por eso los candados
se evaluan cada ocho dias y hay que poder ver, de un vistazo, cuantas cazadas y
cuantos frenos en falso lleva cada candado.

El fallo que esta vigia impide repetir: la forma de apuntar un freno en falso
existia en arnes/candados_medicion.py, pero NADIE la usaba nunca. Resultado:
todos los candados marcaban cero frenos en falso y la ley no podia dispararse
jamas. Es el mismo fallo del contador de veces que Julio repite, que marcaba
cero habiendo repetido cuatro veces el mismo dia.

Notas de carga:
- arnes/candados_medicion.py se carga POR SU RUTA con importlib y con nombre
  propio, porque en esta casa hay una carpeta llamada skills y un archivo
  llamado cuerpo skills que chocan de nombre al importar por paquete.
- El registro se desvia con la variable de entorno que ya usa esa pieza, para
  no tocar el registro real de Julio.
"""

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


# ---------------------------------------------------------------------------
# Carga de la pieza por su ruta, con nombre propio.
# ---------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
RUTA_CANDADOS = RAIZ / "arnes" / "candados_medicion.py"

# Nombre propio para no chocar con la carpeta skills ni con el archivo cuerpo
# skills que andan sueltos por el arbol.
NOMBRE_MODULO = "candados_medicion_vigia_alarma"


def _cargar_candados():
    """Carga arnes/candados_medicion.py por su ruta, con nombre propio.

    No se usa 'import arnes.candados_medicion' a proposito: en esta casa hay
    una carpeta skills y un archivo cuerpo skills que chocan de nombre, y el
    import por paquete puede resolver al equivocado. Cargar por ruta con
    importlib y un nombre unico evita ese choque.
    """
    if not RUTA_CANDADOS.exists():
        raise AssertionError(
            "No encuentro arnes/candados_medicion.py en {}. Sin esa pieza no "
            "se puede medir ningun candado, y sin medir no hay ley que valga."
            .format(RUTA_CANDADOS)
        )

    if NOMBRE_MODULO in sys.modules:
        return sys.modules[NOMBRE_MODULO]

    spec = importlib.util.spec_from_file_location(NOMBRE_MODULO, str(RUTA_CANDADOS))
    if spec is None or spec.loader is None:
        raise AssertionError(
            "No he podido preparar la carga de {} por su ruta. La pieza existe "
            "pero importlib no la reconoce como modulo.".format(RUTA_CANDADOS)
        )

    modulo = importlib.util.module_from_spec(spec)
    sys.modules[NOMBRE_MODULO] = modulo
    spec.loader.exec_module(modulo)
    return modulo


# ---------------------------------------------------------------------------
# Desvio del registro: no tocar el registro real de Julio.
# ---------------------------------------------------------------------------

# La pieza ya usa una variable de entorno para decidir donde vive su registro.
# Aqui se prueban varios nombres plausibles y se fija el que la pieza lea de
# verdad, para no depender de que alguien se acuerde de ponerla a mano.
NOMBRES_DE_ENTORNO_DEL_REGISTRO = (
    "CANDADOS_MEDICION_REGISTRO",
    "CANDADOS_REGISTRO",
    "ARNES_CANDADOS_REGISTRO",
    "VUC_CANDADOS_REGISTRO",
)


def _desviar_registro(directorio_temporal):
    """Apunta el registro de candados a un archivo temporal.

    Devuelve el nombre de la variable de entorno que se ha usado. Se prueban
    varios nombres porque la pieza puede leer cualquiera de ellos; el que
    exista en el modulo se respeta, y si no existe ninguno se usa el primero
    como convencion de esta vigia.

    Esto es obligatorio: si la vigia escribiera en el registro real de Julio,
    estaria ensuciando la cuenta de verdad con datos de prueba, y la ley no
    podria distinguir una alarma real de un ruido de test.
    """
    ruta_registro = os.path.join(directorio_temporal, "registro_candados_de_prueba.json")

    modulo = _cargar_candados()
    elegido = None
    for nombre in NOMBRES_DE_ENTORNO_DEL_REGISTRO:
        if hasattr(modulo, nombre) or nombre in os.environ:
            elegido = nombre
            break
    if elegido is None:
        elegido = NOMBRES_DE_ENTORNO_DEL_REGISTRO[0]

    os.environ[elegido] = ruta_registro
    return elegido, ruta_registro


# ---------------------------------------------------------------------------
# Utilidades para hablar con la pieza sin saber de antemano como se llama todo.
# ---------------------------------------------------------------------------


def _buscar_llamable(modulo, nombres):
    """Devuelve el primer atributo llamable que exista con alguno de esos nombres."""
    for nombre in nombres:
        candidato = getattr(modulo, nombre, None)
        if callable(candidato):
            return nombre, candidato
    return None, None


def _apuntar_cazada(modulo, candado):
    """Apunta una cazada por el camino real de la pieza.

    SE LLAMA POR SU NOMBRE DE VERDAD (corregido el 2026-09-12): la pieza ofrece apuntar(quien,
    tipo), no una funcion distinta por cada tipo. La primera version de esta vigia iba probando
    nombres inventados (apuntar_cazada, registrar_cazada...) y como ninguno existia, acusaba a la
    pieza de no ofrecer nada. La pieza SI lo ofrece: se comprobo apuntando dos frenos en falso de
    verdad el mismo dia. Buscar a ciegas por nombres parecidos es adivinar, y adivinar acusa a lo
    sano, que es justo lo que esta casa lleva dos dias cazando.
    """
    funcion = getattr(modulo, "apuntar", None)
    if funcion is None:
        raise AssertionError(
            "La pieza arnes/candados_medicion.py no ofrece apuntar(quien, tipo). Sin poder "
            "apuntar cazadas, un candado que funciona no deja rastro, y la ley no puede saber "
            "si el candado sirve o solo hace ruido."
        )
    return "apuntar", funcion(candado, "cazo")


def _apuntar_freno_en_falso(modulo, candado):
    """Apunta un freno en falso por el camino real de la pieza.

    Esta es la funcion que importa: existia y nadie la usaba, asi que todos
    los candados marcaban cero frenos en falso y la ley no podia dispararse
    jamas. Es el mismo fallo del contador de veces que Julio repite.
    """
    funcion = getattr(modulo, "apuntar", None)
    if funcion is None:
        raise AssertionError(
            "La pieza arnes/candados_medicion.py no ofrece apuntar(quien, tipo). Si no se puede "
            "apuntar un freno en falso, todos los candados marcaran cero para siempre y la ley "
            "de la alarma que grita en falso no podra dispararse nunca. Es el mismo fallo del "
            "contador de veces que Julio repite, que marcaba cero habiendo repetido cuatro."
        )
    return "apuntar", funcion(candado, "freno_falso")


def _leer_resumen(modulo):
    """Lee el resumen de todos los candados por el camino real de la pieza."""
    nombre, funcion = _buscar_llamable(
        modulo,
        (
            # tabla() PRIMERO: devuelve los numeros para comparar. resumen() devuelve TEXTO para
            # leerlo, que sirve para mirarlo pero no para aplicar la ley. Se anadio tabla() el
            # 2026-09-12 justo porque la ley no se podia aplicar sin poder comparar los dos
            # numeros de cada candado.
            "tabla",
            "resumen",
            "leer_resumen",
            "dame_resumen",
            "resumen_de_candados",
            "estado_de_candados",
            "tabla_de_candados",
        ),
    )
    if funcion is None:
        raise AssertionError(
            "La pieza arnes/candados_medicion.py no ofrece ninguna forma de "
            "leer el resumen de los candados. Sin resumen no hay forma de ver "
            "de un vistazo cuantas cazadas y cuantos frenos en falso lleva "
            "cada candado, y la ley no se puede aplicar."
        )
    return nombre, funcion()


def _extraer_par_de_numeros(entrada):
    """Saca (cazadas, frenos_en_falso) de una entrada del resumen.

    Acepta diccionarios con nombres variados y tambien tuplas o listas de dos
    numeros. Devuelve None si no encuentra los dos numeros.
    """
    if isinstance(entrada, dict):
        claves_cazadas = (
            "cazadas",
            "cazada",
            "aciertos",
            "acierto",
            "verdaderos",
            "positivos",
            "positivos_verdaderos",
        )
        claves_falsos = (
            "frenos_en_falso",
            "freno_en_falso",
            "falsos",
            "falso",
            "falsos_positivos",
            "falso_positivo",
            "frenos_falsos",
        )
        cazadas = None
        falsos = None
        for clave in claves_cazadas:
            if clave in entrada:
                cazadas = entrada[clave]
                break
        for clave in claves_falsos:
            if clave in entrada:
                falsos = entrada[clave]
                break
        if cazadas is not None and falsos is not None:
            return int(cazadas), int(falsos)
        return None

    if isinstance(entrada, (tuple, list)) and len(entrada) == 2:
        try:
            return int(entrada[0]), int(entrada[1])
        except (TypeError, ValueError):
            return None

    return None


def _normalizar_resumen(resumen):
    """Convierte el resumen en un diccionario {candado: (cazadas, frenos_en_falso)}.

    Acepta un diccionario de candado -> entrada, o una lista de entradas con
    el nombre del candado dentro. Si no se puede normalizar, devuelve None.
    """
    normalizado = {}

    if isinstance(resumen, dict):
        for candado, entrada in resumen.items():
            par = _extraer_par_de_numeros(entrada)
            if par is None:
                return None
            normalizado[str(candado)] = par
        return normalizado

    if isinstance(resumen, (list, tuple)):
        for entrada in resumen:
            if not isinstance(entrada, dict):
                return None
            nombre = None
            for clave in ("candado", "nombre", "pieza", "id"):
                if clave in entrada:
                    nombre = str(entrada[clave])
                    break
            if nombre is None:
                return None
            par = _extraer_par_de_numeros(entrada)
            if par is None:
                return None
            normalizado[nombre] = par
        return normalizado

    return None


# ---------------------------------------------------------------------------
# Base comun de las pruebas: cada una con su registro desviado.
# ---------------------------------------------------------------------------


class BaseVigiaAlarmaQueGritaEnFalso(unittest.TestCase):
    """Base que aisla el registro y carga la pieza por su ruta."""

    def setUp(self):
        self._directorio = tempfile.TemporaryDirectory()
        self.addCleanup(self._directorio.cleanup)
        self.variable_de_entorno, self.ruta_registro = _desviar_registro(
            self._directorio.name
        )
        self.modulo = _cargar_candados()

    def tearDown(self):
        os.environ.pop(self.variable_de_entorno, None)


# ---------------------------------------------------------------------------
# PRUEBA UNO: se puede apuntar una cazada y el numero sube.
# ---------------------------------------------------------------------------


class TestSePuedeApuntarUnaCazada(BaseVigiaAlarmaQueGritaEnFalso):

    def test_apuntar_una_cazada_sube_el_numero(self):
        """Una cazada apuntada tiene que verse en el resumen.

        Si apuntar una cazada no sube el numero, el candado que SI funciona
        no deja rastro, y la ley no puede distinguir un candado util de uno
        que solo hace ruido.
        """
        candado = "candado_de_prueba_cazada"

        _, antes = _leer_resumen(self.modulo)
        normalizado_antes = _normalizar_resumen(antes)
        if normalizado_antes is None:
            normalizado_antes = {}
        cazadas_antes = normalizado_antes.get(candado, (0, 0))[0]

        _apuntar_cazada(self.modulo, candado)

        _, despues = _leer_resumen(self.modulo)
        normalizado_despues = _normalizar_resumen(despues)
        self.assertIsNotNone(
            normalizado_despues,
            "El resumen de candados no se puede leer como una tabla de "
            "candado -> (cazadas, frenos en falso). Sin eso no hay forma de "
            "comprobar que apuntar una cazada sube el numero.",
        )
        self.assertIn(
            candado,
            normalizado_despues,
            "He apuntado una cazada en '{}' y el candado no aparece en el "
            "resumen. Apuntar una cazada tiene que dejar rastro visible."
            .format(candado),
        )
        cazadas_despues = normalizado_despues[candado][0]
        self.assertEqual(
            cazadas_despues,
            cazadas_antes + 1,
            "He apuntado una cazada en '{}' y el numero no ha subido: "
            "antes {} y despues {}. Si apuntar una cazada no sube el numero, "
            "el candado que si funciona no deja rastro y la ley no puede "
            "saber si sirve o solo hace ruido."
            .format(candado, cazadas_antes, cazadas_despues),
        )


# ---------------------------------------------------------------------------
# PRUEBA DOS: se puede apuntar un freno en falso y el numero sube.
# Esta es la que importa.
# ---------------------------------------------------------------------------


class TestSePuedeApuntarUnFrenoEnFalso(BaseVigiaAlarmaQueGritaEnFalso):

    def test_apuntar_un_freno_en_falso_sube_el_numero(self):
        """Un freno en falso apuntado tiene que verse en el resumen.

        Esta es la prueba que importa. La forma de apuntar un freno en falso
        existia en la pieza y NADIE la usaba nunca, asi que todos los candados
        marcaban cero frenos en falso y la ley no podia dispararse jamas. Es
        el mismo fallo del contador de veces que Julio repite, que marcaba
        cero habiendo repetido cuatro veces el mismo dia.
        """
        candado = "candado_de_prueba_freno_en_falso"

        _, antes = _leer_resumen(self.modulo)
        normalizado_antes = _normalizar_resumen(antes)
        if normalizado_antes is None:
            normalizado_antes = {}
        falsos_antes = normalizado_antes.get(candado, (0, 0))[1]

        _apuntar_freno_en_falso(self.modulo, candado)

        _, despues = _leer_resumen(self.modulo)
        normalizado_despues = _normalizar_resumen(despues)
        self.assertIsNotNone(
            normalizado_despues,
            "El resumen de candados no se puede leer como una tabla de "
            "candado -> (cazadas, frenos en falso). Sin eso no hay forma de "
            "comprobar que apuntar un freno en falso sube el numero.",
        )
        self.assertIn(
            candado,
            normalizado_despues,
            "He apuntado un freno en falso en '{}' y el candado no aparece "
            "en el resumen. Si apuntar un freno en falso no deja rastro, "
            "todos los candados marcaran cero para siempre y la ley de la "
            "alarma que grita en falso no podra dispararse nunca."
            .format(candado),
        )
        falsos_despues = normalizado_despues[candado][1]
        self.assertEqual(
            falsos_despues,
            falsos_antes + 1,
            "He apuntado un freno en falso en '{}' y el numero no ha subido: "
            "antes {} y despues {}. Esto es exactamente el fallo que la ley "
            "quiere impedir: si apuntar un freno en falso no sube el numero, "
            "todos los candados marcaran cero frenos en falso y la ley no "
            "podra dispararse jamas. Es el mismo fallo del contador de veces "
            "que Julio repite, que marcaba cero habiendo repetido cuatro "
            "veces."
            .format(candado, falsos_antes, falsos_despues),
        )


# ---------------------------------------------------------------------------
# PRUEBA TRES: existe una forma de leer el resumen y dice los dos numeros.
# ---------------------------------------------------------------------------


class TestElResumenDiceLosDosNumeros(BaseVigiaAlarmaQueGritaEnFalso):

    def test_el_resumen_dice_los_dos_numeros_de_cada_candado(self):
        """El resumen tiene que dar, por cada candado, cazadas y frenos en falso.

        Sin los dos numeros juntos no se puede aplicar la ley: una alarma que
        grita en falso se arregla o se apaga, y para saber cual grita hay que
        poder comparar sus cazadas con sus frenos en falso.
        """
        candado = "candado_de_prueba_resumen"
        _apuntar_cazada(self.modulo, candado)
        _apuntar_freno_en_falso(self.modulo, candado)

        _, resumen = _leer_resumen(self.modulo)
        normalizado = _normalizar_resumen(resumen)
        self.assertIsNotNone(
            normalizado,
            "El resumen de candados no se puede leer como una tabla de "
            "candado -> (cazadas, frenos en falso). Sin los dos numeros "
            "juntos no se puede aplicar la ley: una alarma que grita en "
            "falso se arregla o se apaga, y para saber cual grita hay que "
            "poder comparar sus cazadas con sus frenos en falso.",
        )
        self.assertIn(
            candado,
            normalizado,
            "He apuntado una cazada y un freno en falso en '{}' y el candado "
            "no aparece en el resumen. El resumen tiene que decir los dos "
            "numeros de cada candado."
            .format(candado),
        )
        cazadas, falsos = normalizado[candado]
        self.assertGreaterEqual(
            cazadas,
            1,
            "El resumen de '{}' no dice las cazadas (dice {}). El resumen "
            "tiene que decir los dos numeros de cada candado."
            .format(candado, cazadas),
        )
        self.assertGreaterEqual(
            falsos,
            1,
            "El resumen de '{}' no dice los frenos en falso (dice {}). El "
            "resumen tiene que decir los dos numeros de cada candado."
            .format(candado, falsos),
        )


# ---------------------------------------------------------------------------
# PRUEBA CUATRO: un candado con mas frenos en falso que cazadas se distingue.
# ---------------------------------------------------------------------------


class TestSeDistingueElCandadoQueGritaEnFalso(BaseVigiaAlarmaQueGritaEnFalso):

    def test_un_candado_con_mas_frenos_en_falso_que_cazadas_se_distingue(self):
        """El candado que grita en falso tiene que poder senalarse.

        Ese es el que hay que arreglar o apagar segun la ley. Si no se puede
        distinguir, la ley no tiene a quien aplicarse y el contrato vuelve a
        ser solo papel.
        """
        candado_sano = "candado_de_prueba_sano"
        candado_que_grita = "candado_de_prueba_que_grita"

        # El sano: mas cazadas que frenos en falso.
        _apuntar_cazada(self.modulo, candado_sano)
        _apuntar_cazada(self.modulo, candado_sano)
        _apuntar_cazada(self.modulo, candado_sano)
        _apuntar_freno_en_falso(self.modulo, candado_sano)

        # El que grita: mas frenos en falso que cazadas.
        _apuntar_cazada(self.modulo, candado_que_grita)
        _apuntar_freno_en_falso(self.modulo, candado_que_grita)
        _apuntar_freno_en_falso(self.modulo, candado_que_grita)
        _apuntar_freno_en_falso(self.modulo, candado_que_grita)

        _, resumen = _leer_resumen(self.modulo)
        normalizado = _normalizar_resumen(resumen)
        self.assertIsNotNone(
            normalizado,
            "El resumen de candados no se puede leer como una tabla de "
            "candado -> (cazadas, frenos en falso). Sin eso no se puede "
            "distinguir el candado que grita en falso, que es justo el que "
            "hay que arreglar o apagar segun la ley.",
        )
        self.assertIn(
            candado_sano,
            normalizado,
            "El candado sano '{}' no aparece en el resumen.".format(candado_sano),
        )
        self.assertIn(
            candado_que_grita,
            normalizado,
            "El candado que grita en falso '{}' no aparece en el resumen."
            .format(candado_que_grita),
        )

        cazadas_sano, falsos_sano = normalizado[candado_sano]
        cazadas_grita, falsos_grita = normalizado[candado_que_grita]

        self.assertGreater(
            cazadas_sano,
            falsos_sano,
            "El candado sano '{}' deberia tener mas cazadas ({}) que frenos "
            "en falso ({}). Si no, la prueba no esta midiendo lo que cree."
            .format(candado_sano, cazadas_sano, falsos_sano),
        )
        self.assertGreater(
            falsos_grita,
            cazadas_grita,
            "El candado '{}' deberia tener mas frenos en falso ({}) que "
            "cazadas ({}). Si no, la prueba no esta midiendo lo que cree."
            .format(candado_que_grita, falsos_grita, cazadas_grita),
        )

        # Y ahora lo que importa: que se puedan distinguir el uno del otro.
        self.assertNotEqual(
            (cazadas_sano, falsos_sano),
            (cazadas_grita, falsos_grita),
            "Los dos candados de prueba tienen los mismos numeros. La prueba "
            "no esta midiendo lo que cree.",
        )
        self.assertTrue(
            falsos_grita > cazadas_grita and cazadas_sano > falsos_sano,
            "No se puede distinguir el candado que grita en falso del sano. "
            "El que grita en falso es el que hay que arreglar o apagar segun "
            "la ley, y si no se distingue, la ley no tiene a quien "
            "aplicarse y el contrato vuelve a ser solo papel.",
        )


if __name__ == "__main__":
    unittest.main()
