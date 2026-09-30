"""VIGIA: la lista de cambios tambien se revisa.

NACE ROJA A PROPOSITO. El arreglo entra en la ronda SIGUIENTE.

Hueco medido hoy: la comprobacion que caza a un cerebro que se rindio
(_trae_no_encontrado, en cuerpo/obrero.py) mira CUATRO campos sueltos de la
propuesta (archivo, codigo, texto_viejo, texto_nuevo), pero la plantilla del
obrero permite entregar el trabajo como una LISTA DE CAMBIOS en el campo
'cambios', y esa lista NO se mira. Un trabajo que por los campos sueltos se
rechazaba, entregado dentro de la lista paso sin que la comprobacion lo viera.

Esta prueba mide que la funcion pase a mirar TAMBIEN dentro de la lista:
  - si 'cambios' es una lista, se recorre cada elemento;
  - de cada elemento que sea diccionario se miran su texto_viejo y su texto_nuevo
    con la MISMA regla que ya se aplica a los campos de codigo;
  - si algun elemento delata rendicion, contesta que si;
  - si la lista no esta, esta vacia o trae cosas que no son diccionarios, no pasa
    nada y se sigue como hoy;
  - la funcion sigue sin reventar nunca.

Sin IA, sin red, sin disco, sin lanzar procesos. Todo se arma aqui mismo.
"""

import os
import sys
import unittest


# REGLA OBLIGATORIA DE ESCRITURA: la marca se define UNA sola vez, por partes.
MARCA = "NO" + "_" + "ENCONTRADO"

# Los cuatro nombres de campo que hoy recibe la funcion, igual que quien la llama.
CAMPOS = ("archivo", "codigo", "texto_viejo", "texto_nuevo")


def _raiz():
    """La carpeta que esta un nivel arriba de la carpeta vigias."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(aqui)


def _trae(propuesta):
    """Importa cuerpo/obrero.py DENTRO del caso y llama a la funcion que se mide."""
    raiz = _raiz()
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    from cuerpo import obrero
    return obrero._trae_no_encontrado(propuesta, CAMPOS)


def _propuesta(cambios=None, **sueltos):
    """Propuesta de mentira con los campos sueltos vacios y, si se pide, la lista."""
    p = {
        "archivo": "",
        "codigo": "",
        "texto_viejo": "",
        "texto_nuevo": "",
    }
    p.update(sueltos)
    if cambios is not None:
        p["cambios"] = cambios
    return p


# Un cambio normal de codigo, de unos diez renglones, sin la marca en ninguna parte.
CODIGO_NORMAL_1 = (
    "def sumar(a, b):\n"
    "    total = a + b\n"
    "    return total\n"
    "\n"
    "\n"
    "def restar(a, b):\n"
    "    total = a - b\n"
    "    return total\n"
    "\n"
    "\n"
    "def doblar(a):\n"
    "    return a * 2\n"
)

CODIGO_NORMAL_2 = (
    "def saludar(nombre):\n"
    "    if not nombre:\n"
    "        return 'hola'\n"
    "    return 'hola ' + nombre\n"
    "\n"
    "\n"
    "def despedir(nombre):\n"
    "    if not nombre:\n"
    "        return 'adios'\n"
    "    return 'adios ' + nombre\n"
)

# Un archivo de codigo de mentira, de unos quince renglones, que usa la MARCA
# entre comillas como valor. Es contenido, no rendicion.
CODIGO_LARGO_CON_MARCA = (
    "MARCA = \"" + MARCA + "\"\n"
    "\n"
    "\n"
    "def buscar(texto):\n"
    "    if texto == MARCA:\n"
    "        return True\n"
    "    return False\n"
    "\n"
    "\n"
    "def limpiar(texto):\n"
    "    if not texto:\n"
    "        return MARCA\n"
    "    return texto.strip()\n"
    "\n"
    "\n"
    "def comparar(a, b):\n"
    "    return a == b\n"
)


class TestLaListaDeCambiosTambienSeRevisa(unittest.TestCase):

    def test_1_rendicion_escondida_en_la_lista_se_caza(self):
        """Caso 1: nace ROJO. Una rendicion dentro de la lista tiene que cazarse.

        Por este hueco paso un trabajo de verdad hoy: los campos sueltos iban
        vacios y la rendicion viajaba dentro de la lista de cambios.
        """
        propuesta = _propuesta(cambios=[
            {"texto_viejo": "algo viejo", "texto_nuevo": MARCA},
        ])
        self.assertTrue(
            _trae(propuesta),
            "Por este hueco paso un trabajo de verdad hoy: la rendicion viajaba "
            "dentro de la lista de cambios y la comprobacion no la miro.",
        )

    def test_2_tambien_si_esta_en_el_segundo_elemento(self):
        """Caso 2: nace ROJO. La rendicion puede ir en cualquier elemento."""
        propuesta = _propuesta(cambios=[
            {"texto_viejo": "viejo uno", "texto_nuevo": CODIGO_NORMAL_1},
            {"texto_viejo": "viejo dos", "texto_nuevo": MARCA},
        ])
        self.assertTrue(
            _trae(propuesta),
            "La rendicion en el segundo elemento de la lista tambien tiene que cazarse.",
        )

    def test_3_tambien_si_esta_en_el_texto_viejo_de_un_elemento(self):
        """Caso 3: nace ROJO. El texto viejo de un elemento tambien se mira."""
        propuesta = _propuesta(cambios=[
            {"texto_viejo": MARCA, "texto_nuevo": CODIGO_NORMAL_1},
        ])
        self.assertTrue(
            _trae(propuesta),
            "La rendicion en el texto viejo de un elemento tambien tiene que cazarse.",
        )

    def test_4_un_cambio_normal_en_la_lista_sigue_pasando(self):
        """Caso 4: VERDE HOY. Este es el caso que impide apretar de mas."""
        propuesta = _propuesta(cambios=[
            {"texto_viejo": "viejo uno", "texto_nuevo": CODIGO_NORMAL_1},
            {"texto_viejo": "viejo dos", "texto_nuevo": CODIGO_NORMAL_2},
        ])
        self.assertFalse(
            _trae(propuesta),
            "Un cambio normal entregado por la lista no puede rechazarse.",
        )

    def test_5_un_cambio_largo_que_usa_la_marca_como_contenido_sigue_pasando(self):
        """Caso 5: VERDE HOY. La marca como contenido en un archivo largo no es rendirse."""
        propuesta = _propuesta(cambios=[
            {"texto_viejo": "viejo", "texto_nuevo": CODIGO_LARGO_CON_MARCA},
        ])
        self.assertFalse(
            _trae(propuesta),
            "La marca usada como contenido en un archivo largo no es rendirse.",
        )

    def test_6_no_revienta_con_basura(self):
        """Caso 6: VERDE HOY. Con basura en el campo de la lista contesta que NO y no revienta."""
        basuras = [
            None,
            "un texto cualquiera",
            12345,
            [],
            [1, 2, 3],
            [{}],
        ]
        for basura in basuras:
            with self.subTest(basura=repr(basura)):
                propuesta = _propuesta(cambios=basura)
                try:
                    resultado = _trae(propuesta)
                except Exception as exc:
                    self.fail(
                        "La funcion revento con basura en la lista: %r -> %r"
                        % (basura, exc)
                    )
                self.assertFalse(
                    resultado,
                    "Con basura en la lista tiene que contestar que NO: %r" % (basura,),
                )


if __name__ == "__main__":
    unittest.main()
