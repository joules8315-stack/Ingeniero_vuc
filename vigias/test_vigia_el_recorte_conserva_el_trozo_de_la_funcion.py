import os
import sys

# La carpeta que esta un nivel arriba de vigias/ es la raiz del proyecto.
# Se calcula a partir de la ruta de ESTE mismo archivo de prueba, con os.path.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

import arnes.asignador as asignador


# ---------------------------------------------------------------------------
# TEXTO DE MENTIRA, armado AQUI juntando renglones de una lista.
# No se usa texto de triple comilla que lleve dentro otras comillas.
# ---------------------------------------------------------------------------

# La cabecera trae, escrito en palabras, la tarea: arreglar app_web.html,
# funcion processPhoto. Esta cabecera NO se puede recortar.
CABECERA = [
    "ENCARGO: arreglar el archivo app_web.html",
    "TAREA: reparar la funcion processPhoto",
    "La funcion processPhoto vive dentro de app_web.html y hay que dejarla buena.",
    "No se toca ningun otro archivo.",
]

# El renglon que declara la funcion pedida. Aparece UNA sola vez en todo el texto.
DECLARACION = "function processPhoto(foto) {"

# Relleno: comentarios normales, para que la seccion tenga volumen de sobra.
RELLENO_ANTES = ["// relleno antes %d" % i for i in range(300)]
RELLENO_DESPUES = ["// relleno despues %d" % i for i in range(300)]

# La seccion del archivo empieza con tres almohadillas, un espacio y el nombre
# del archivo entre tildes invertidas.
APERTURA_SECCION = "### `app_web.html`"

# Renglon que abre el material y renglon que lo cierra.
ABRE_MATERIAL = "===== MATERIAL ====="
CIERRA_MATERIAL = "===== FIN DEL MATERIAL ====="

# Cola corta detras del material.
COLA = [
    "",
    "FIN DEL ENCARGO.",
]


def _armar_texto():
    """Arma el texto de mentira juntando renglones de listas. Determinista."""
    lineas = []
    lineas.extend(CABECERA)
    lineas.append(ABRE_MATERIAL)
    lineas.append(APERTURA_SECCION)
    lineas.extend(RELLENO_ANTES)
    lineas.append(DECLARACION)
    lineas.extend(RELLENO_DESPUES)
    lineas.append(CIERRA_MATERIAL)
    lineas.extend(COLA)
    return "\n".join(lineas)


def _tope_suficiente(texto):
    """Tope bastante menor que el texto, pero con sitio para cabecera, cola y
    un buen trozo del material. Se calcula a partir del texto para que no dependa
    de numeros magicos."""
    largo = len(texto)
    # La mitad del texto: cabe la cabecera, la cola y una buena parte del material,
    # pero NO el texto entero.
    tope = largo // 2
    # Asegurar que el tope es menor que el texto (para que el recorte se dispare).
    if tope >= largo:
        tope = largo - 1
    return tope


def test_el_recorte_conserva_el_trozo_de_la_funcion():
    """CASO 1 (NACE ROJO): el recorte tiene que conservar el renglon que declara
    la funcion pedida.

    Hoy el recorte se queda con el PRINCIPIO de la seccion nombrada y omite el
    trozo que contiene la funcion pedida. Por eso esta prueba nace roja: el
    arreglo entra en otra ronda.
    """
    texto = _armar_texto()
    tope = _tope_suficiente(texto)
    resultado = asignador.recortar_prompt(texto, tope)
    assert DECLARACION in resultado, (
        "el recorte se queda con el PRINCIPIO de la seccion nombrada y omite "
        "el trozo que contiene la funcion pedida: falta el renglon %r" % DECLARACION
    )


def test_el_recorte_no_pasa_del_tope():
    """CASO 2 (VERDE HOY): lo que NO puede cambiar. El resultado no pasa del tope."""
    texto = _armar_texto()
    tope = _tope_suficiente(texto)
    resultado = asignador.recortar_prompt(texto, tope)
    assert len(resultado) <= tope, (
        "el recorte se paso del tope: %d letras para un tope de %d"
        % (len(resultado), tope)
    )


def test_la_cabecera_llega_entera():
    """CASO 3 (VERDE HOY): lo que NO puede cambiar. La cabecera del encargo llega
    entera al resultado, sin recortar, porque recortar la instruccion para ahorrar
    letras seria peor que el ahorro.
    """
    texto = _armar_texto()
    tope = _tope_suficiente(texto)
    resultado = asignador.recortar_prompt(texto, tope)
    cabecera = "\n".join(CABECERA)
    assert resultado.startswith(cabecera), (
        "la cabecera del encargo no llega entera al resultado: se recorto la "
        "instruccion, y eso es peor que el ahorro"
    )


if __name__ == "__main__":
    # Ejecucion directa: corre los tres casos y muestra el resultado.
    fallos = 0
    for nombre, fn in [
        ("caso 1: conserva el trozo de la funcion", test_el_recorte_conserva_el_trozo_de_la_funcion),
        ("caso 2: no pasa del tope", test_el_recorte_no_pasa_del_tope),
        ("caso 3: la cabecera llega entera", test_la_cabecera_llega_entera),
    ]:
        try:
            fn()
            print("OK   %s" % nombre)
        except AssertionError as e:
            fallos += 1
            print("ROJO %s: %s" % (nombre, e))
    sys.exit(1 if fallos else 0)
