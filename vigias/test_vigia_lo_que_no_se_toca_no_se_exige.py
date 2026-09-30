"""Vigia: lo que el encargo dice que NO SE TOCA no se exige dentro del cambio.

NACE ROJA A PROPOSITO. El arreglo entra en la ronda siguiente: antes de buscar
las palabras con raya baja, la pieza debe quitarle al texto del encargo el
apartado que empieza por 'NO SE TOCA:' y acaba en el primer renglon posterior
que empieza por una palabra en MAYUSCULAS seguida de dos puntos, o por un
renglon solo de signos de igual, o al acabarse el texto.

Hoy, sin ese arreglo, los casos 1 y 2 fallan (rojos) y los casos 3, 4 y 5
pasan (verdes). Si al quitar el arreglo algun caso sigue verde, la prueba
mira a otro nivel y el trabajo se devuelve.

No lee ni escribe archivos de verdad: las propuestas y los encargos son de
mentira y se arman aqui mismo. Sin IA, sin red, sin disco, sin procesos.
"""

import os
import sys
import unittest


# ---------------------------------------------------------------------------
# Arranque: se mete en la ruta de busqueda la carpeta un nivel arriba de
# 'vigias' y tambien la carpeta 'arnes'. La pieza se importa DENTRO de cada
# caso, nunca arriba del archivo.
# ---------------------------------------------------------------------------
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
_ARNES = os.path.join(_RAIZ, "arnes")
for _ruta in (_RAIZ, _ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# ---------------------------------------------------------------------------
# Utilidades de montaje. Todo es de mentira: nada toca el disco.
# ---------------------------------------------------------------------------

# Nombre de archivo que NO existe en el disco, para que la pieza no lo lea.
_ARCHIVO_INEXISTENTE = "no_existe_esta_pieza_de_mentira_para_la_vigia.py"


def _propuesta_de_mentira():
    """Propuesta con las claves archivo, texto_viejo y texto_nuevo.

    Los dos textos son trozos de codigo distintos entre si (para que no salte
    el aviso de HUMO) y NO llevan dentro el nombre que se va a nombrar en el
    encargo. El archivo no existe en el disco.
    """
    viejo = (
        "def sumar(a, b):\n"
        "    resultado = a + b\n"
        "    return resultado\n"
        "\n"
        "def restar(a, b):\n"
        "    resultado = a - b\n"
        "    return resultado\n"
        "\n"
        "def doblar(x):\n"
        "    return x * 2\n"
    )
    nuevo = (
        "def sumar(a, b):\n"
        "    total = a + b\n"
        "    return total\n"
        "\n"
        "def restar(a, b):\n"
        "    total = a - b\n"
        "    return total\n"
        "\n"
        "def doblar(x):\n"
        "    return x + x\n"
    )
    return {
        "archivo": _ARCHIVO_INEXISTENTE,
        "texto_viejo": viejo,
        "texto_nuevo": nuevo,
    }


def _fallos_que_nombran(fallos, nombre):
    """Devuelve los fallos que empiezan por NO HACE LO QUE SE PIDIO y traen
    dentro el nombre de la pieza. Los demas fallos se ignoran: esta prueba
    mide SOLO ese apartado."""
    prefijo = "NO HACE LO QUE SE PIDIO"
    encontrados = []
    for fallo in fallos or []:
        texto = str(fallo)
        if texto.startswith(prefijo) and nombre in texto:
            encontrados.append(texto)
    return encontrados


def _revisar(propuesta, tarea):
    """Importa la pieza DENTRO del caso y llama a revisar."""
    from arnes import revisor_de_programa
    return revisor_de_programa.revisar(propuesta, tarea)


# ---------------------------------------------------------------------------
# Casos
# ---------------------------------------------------------------------------

class TestLoQueNoSeTocaNoSeExige(unittest.TestCase):

    # ------------------------------------------------------------------
    # CASO 1 — NACE ROJO.
    # Un nombre dentro del apartado de lo que NO se toca no se exige.
    # ------------------------------------------------------------------
    def test_nombre_dentro_de_lo_que_no_se_toca_no_se_exige(self):
        pieza = "_propuesta_cumple"
        encargo = (
            "Reparar el calculo del pedido para que cuadre con lo facturado.\n"
            "\n"
            "NO SE TOCA:\n"
            "- %s, que comprueba que el pedido esta completo.\n"
            "- el resto del flujo de campana.\n"
            "\n"
            "Al terminar, deja el resultado en el mismo sitio.\n"
        ) % pieza
        fallos = _revisar(_propuesta_de_mentira(), encargo)
        encontrados = _fallos_que_nombran(fallos, pieza)
        self.assertEqual(
            encontrados,
            [],
            "Hoy, por esto, hubo que quitar del encargo la proteccion del vecino "
            "para que el trabajo pasara: el revisor por programa exige '%s' aunque "
            "el encargo solo la nombre dentro del apartado NO SE TOCA. "
            "Fallos encontrados: %r" % (pieza, encontrados),
        )

    # ------------------------------------------------------------------
    # CASO 2 — NACE ROJO.
    # El apartado acaba donde empieza el siguiente, y dentro del siguiente
    # SI se sigue exigiendo.
    # ------------------------------------------------------------------
    def test_el_apartado_acaba_donde_empieza_el_siguiente(self):
        pieza_protegida = "_propuesta_cumple"
        pieza_exigida = "_cuadrar_totales"
        encargo = (
            "Reparar el calculo del pedido para que cuadre con lo facturado.\n"
            "\n"
            "NO SE TOCA:\n"
            "- %s, que comprueba que el pedido esta completo.\n"
            "\n"
            "LO QUE HAY QUE TOCAR:\n"
            "- %s, que hoy redondea mal.\n"
            "\n"
            "Al terminar, deja el resultado en el mismo sitio.\n"
        ) % (pieza_protegida, pieza_exigida)
        fallos = _revisar(_propuesta_de_mentira(), encargo)
        encontrados = _fallos_que_nombran(fallos, pieza_exigida)
        self.assertTrue(
            encontrados,
            "El apartado de lo que NO se toca acaba donde empieza el siguiente "
            "renglon en mayusculas con dos puntos, asi que '%s' SI se sigue "
            "exigiendo. Si no aparece su fallo, el arreglo se comio medio "
            "encargo. Fallos: %r" % (pieza_exigida, fallos),
        )

    # ------------------------------------------------------------------
    # CASO 3 — VERDE HOY.
    # Fuera de ese apartado se sigue exigiendo.
    # ------------------------------------------------------------------
    def test_fuera_de_ese_apartado_se_sigue_exigiendo(self):
        pieza = "_cuadrar_totales"
        encargo = (
            "Reparar el calculo del pedido para que cuadre con lo facturado.\n"
            "Hay que tocar %s, que hoy redondea mal.\n"
            "Al terminar, deja el resultado en el mismo sitio.\n"
        ) % pieza
        fallos = _revisar(_propuesta_de_mentira(), encargo)
        encontrados = _fallos_que_nombran(fallos, pieza)
        self.assertTrue(
            encontrados,
            "Sin apartado de lo que NO se toca, '%s' se sigue exigiendo. "
            "Este caso impide aflojarlo de mas. Fallos: %r" % (pieza, fallos),
        )

    # ------------------------------------------------------------------
    # CASO 4 — VERDE HOY.
    # Sin ese apartado todo sigue igual: dos piezas, dos fallos.
    # ------------------------------------------------------------------
    def test_sin_ese_apartado_todo_sigue_igual(self):
        pieza_a = "_cuadrar_totales"
        pieza_b = "_revisar_redondeo"
        encargo = (
            "Reparar el calculo del pedido para que cuadre con lo facturado.\n"
            "Hay que tocar %s y tambien %s.\n"
            "Al terminar, deja el resultado en el mismo sitio.\n"
        ) % (pieza_a, pieza_b)
        fallos = _revisar(_propuesta_de_mentira(), encargo)
        encontrados_a = _fallos_que_nombran(fallos, pieza_a)
        encontrados_b = _fallos_que_nombran(fallos, pieza_b)
        self.assertTrue(
            encontrados_a,
            "Falta el fallo de '%s'. Fallos: %r" % (pieza_a, fallos),
        )
        self.assertTrue(
            encontrados_b,
            "Falta el fallo de '%s'. Fallos: %r" % (pieza_b, fallos),
        )

    # ------------------------------------------------------------------
    # CASO 5 — VERDE HOY.
    # No revienta con basura.
    # ------------------------------------------------------------------
    def test_no_revienta_con_basura(self):
        propuesta = _propuesta_de_mentira()
        casos = [
            "",
            None,
            42,
            "NO SE TOCA:\n",
        ]
        for tarea in casos:
            with self.subTest(tarea=repr(tarea)):
                resultado = _revisar(propuesta, tarea)
                self.assertIsInstance(
                    resultado,
                    list,
                    "Con tarea=%r la pieza debe devolver una lista, no %r"
                    % (tarea, type(resultado)),
                )


if __name__ == "__main__":
    unittest.main()
