# -*- coding: utf-8 -*-
"""cuerpo/privacidad.py — SOLO CODIGO A LA NUBE. NUNCA DATOS DE CLIENTES.

Julio, 2026-08-21, decidiendolo con los terminos de Google delante: "solo codigo a la nube".

POR QUE, y no es una mania: en el plan GRATIS de Gemini, Google dice literalmente que usa lo que
se le manda para mejorar sus productos, y que **personas** pueden leerlo ("human reviewers may
read, annotate, and process your API input and output"). No hay forma de desactivarlo en el plan
gratis. Sus propios terminos avisan: "Do not submit sensitive, confidential, or personal
information to the Unpaid Services". Comprobado en ai.google.dev/gemini-api/terms el 2026-08-21.

O sea: si en un encargo va el nombre, el telefono o el correo de un cliente de Julio, eso puede
acabar leido por un desconocido. Julio no vende programas: vende informes a empresas. Ese dato no
es suyo, es de su cliente, y por eso no es suyo el riesgo de soltarlo.

QUE HACE: antes de que un encargo salga hacia la nube, tapa lo que parezca dato personal. No lo
borra —eso dejaria el texto sin sentido y el cerebro contestaria cualquier cosa— sino que lo
sustituye por una marca:
   "Llamar a Maria Perez al 600123456"  ->  "Llamar a Maria Perez al <TELEFONO>"

NO ESTORBA AL TRABAJO: el codigo, los nombres de archivo, los numeros de linea, las fechas y los
mensajes de error pasan intactos. Lo que se tapa es justo lo que no hace falta para reparar nada.
"""
import re

# Cada patron busca por lo que el dato ES, no por como se llame el campo: un telefono es un
# telefono aunque su columna se llame "col3". Buscar por nombre de campo se salta la mitad,
# y ademas Julio ya lo dijo: "en vez de buscar por nombre, se busca por lo que hace".
PATRONES = [
    # El nombre puede venir con prefijo (GROQ_API_KEY, MI-TOKEN): por eso no vale un \b delante,
    # que es lo que hacia que "GROQ_API_KEY=..." pasara de largo con la llave a la vista.
    ("<CLAVE>", re.compile(r"(?i)[\w-]*(?:api[_-]?key|apikey|token|password|passwd|clave|secret)"
                           r"\s*[:=]\s*\S+")),
    ("<CORREO>", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")),
    ("<TARJETA>", re.compile(r"(?<![\w.])(?:\d[ -]?){13,19}(?![\w.])")),
    ("<DOCUMENTO>", re.compile(r"\b\d{7,8}[-\s]?[A-Za-z]\b")),
    ("<TELEFONO>", re.compile(r"(?<![\w.])(?:\+\d{1,3}[ -]?)?(?:\d[ -]?){8,13}\d(?![\w.])")),
]

# Lo que NUNCA se tapa aunque lo parezca: son cosas del codigo, no de una persona.
INDULTADO = re.compile(
    r"(?i)(^\s*\d{1,6}\s*$"                   # numero CORTO suelto: una linea, un tamano
    r"|\b20\d\d-\d\d-\d\d\b"                  # fechas
    r"|\bv?\d+\.\d+(\.\d+)?\b"                # versiones
    r"|\b0x[0-9a-f]+\b|#[0-9a-f]{3,8}\b)")    # numeros de color y similares
# OJO con el numero suelto: antes se indultaba CUALQUIER numero suelto, y un telefono es
# justamente eso. Resultado: "600123456" salia entero hacia la nube. Se indulta solo hasta 6
# cifras, que es lo que mide un numero de linea; de ahi para arriba huele a telefono o a
# documento. Lo cazo la propia vigia al nacer roja.


def limpiar(texto):
    """Devuelve (texto_limpio, cuantas_cosas_se_taparon)."""
    if not texto:
        return texto, 0
    tapados = 0

    def _hacer(marca):
        def _f(m):
            nonlocal tapados
            trozo = m.group(0)
            if INDULTADO.search(trozo.strip()):
                return trozo                    # es cosa del codigo: se deja tal cual
            tapados += 1
            return marca
        return _f

    limpio = texto
    for marca, patron in PATRONES:
        limpio = patron.sub(_hacer(marca), limpio)
    return limpio, tapados


def hay_datos_personales(texto):
    """¿Sale algun dato de cliente en este texto?"""
    return limpiar(texto)[1] > 0


def aviso(n):
    return ("PRIVACIDAD: se taparon %d dato(s) personales antes de mandarlo fuera "
            "(ley de Julio: solo codigo a la nube)." % n)
