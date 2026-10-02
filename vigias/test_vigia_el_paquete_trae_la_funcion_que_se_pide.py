"""Vigia: el paquete trae la REBANADA LITERAL de la funcion que se pide.

Motivo (medido hoy con Codex):
  - processPhoto vive en el renglon 2381 de app_web.html, que tiene 2.462 renglones.
  - Un recorte ciego de los primeros 80 renglones NUNCA alcanza esa funcion.
  - El paquete entrego leyes y pruebas vecinas, sin ninguno de los tres tramos
    pedidos: processPhoto, el manejador de camara y el guardado.

Esta vigia NACE ROJA: hoy el empaquetador no trae esos tramos. Pasa cuando el
empaquetador respeta el NECESITO_LEER y entrega la rebanada literal de la funcion
pedida, en su archivo anfitrion.

Regla dura: la vigia NO lee el archivo del disco por su cuenta. Vigila al PAQUETE
(el texto que el empaquetador entrega), no al anfitrion. Si leyera el anfitrion,
arreglar el empaquetador no la pondria verde nunca.
"""

import re


# ---------------------------------------------------------------------------
# El encargo: tres tramos literales que el paquete DEBE traer.
# ---------------------------------------------------------------------------
ARCHIVO_ANFITRION = "app_web.html"

# Cada tramo: (nombre_legible, patron_de_la_funcion_en_el_anfitrion)
# El patron busca la DEFINICION de la funcion, no una mencion suelta.
TRAMOS_PEDIDOS = [
    (
        "processPhoto",
        re.compile(r"function\s+processPhoto\s*\("),
    ),
    (
        "manejador de camara",
        re.compile(r"function\s+(onCamera|handleCamera|cameraHandler|onCapture)\w*\s*\("),
    ),
    (
        "guardado",
        re.compile(r"function\s+(save|guardar|onSave|handleSave)\w*\s*\("),
    ),
]

# Un recorte ciego de los primeros 80 renglones jamas alcanza el renglon 2381.
RENGLONES_RECORTE_CIEGO = 80
RENGLON_REAL_DE_PROCESSPHOTO = 2381
RENGLONES_TOTALES_ANFITRION = 2462


# ---------------------------------------------------------------------------
# El paquete que el empaquetador entrega HOY (lo que hay que vigilar).
# Se inyecta desde fuera con `paquete_entregado`; si no, se usa el de hoy.
# ---------------------------------------------------------------------------
def _paquete_de_hoy():
    """Lo que el empaquetador entrega hoy: leyes y pruebas vecinas, sin los tramos.

    Esto es lo que hay que arreglar. La vigia nace ROJA contra este texto.
    """
    return (
        "# PAQUETE MINIMO\n"
        "## 1. LA LEY QUE MANDA AQUI\n"
        "- CONTRATO_A_JULIO_NO_SE_LE_PIDE_FIRMAR_LO_QUE_NO_PUEDE_JUZGAR.md\n"
        "- CONTRATO_CREDENCIALES_PARA_PRUEBAS.md\n"
        "- CONTRATO_POR_NOMBRE_Y_POR_FUNCION.md\n"
        "## 5. A QUIEN PUEDE DANAR TOCAR ESTO\n"
        "- cuerpo/codex.py\n"
        "- cuerpo/privacidad.py\n"
        "## LO QUE YA NOS PASO AQUI\n"
        "- vigias/test_vigia_lo_ya_reparado.py\n"
        "- vigias/test_vigia_el_cerebro_es_el_que_pido.py\n"
        "- vigias/test_vigia_diccionario_de_julio.py\n"
    )


# ---------------------------------------------------------------------------
# Comprobaciones de la vigia.
# ---------------------------------------------------------------------------
def _tramos_presentes(paquete):
    """Devuelve los nombres de los tramos que SI aparecen como definicion literal."""
    presentes = []
    for nombre, patron in TRAMOS_PEDIDOS:
        if patron.search(paquete):
            presentes.append(nombre)
    return presentes


def _tramos_ausentes(paquete):
    """Devuelve los nombres de los tramos que NO aparecen como definicion literal."""
    presentes = set(_tramos_presentes(paquete))
    return [nombre for nombre, _ in TRAMOS_PEDIDOS if nombre not in presentes]


def _es_recorte_ciego(paquete):
    """True si el paquete es un recorte ciego de los primeros 80 renglones.

    Un recorte ciego se reconoce porque no trae la definicion de processPhoto
    (que vive en el renglon 2381) y ademas es corto.
    """
    renglones = paquete.splitlines()
    if len(renglones) > RENGLONES_RECORTE_CIEGO * 2:
        return False
    patron_process = TRAMOS_PEDIDOS[0][1]
    return patron_process.search(paquete) is None


# ---------------------------------------------------------------------------
# LA VIGIA: nace ROJA por un assert que falla, no por error de sintaxis.
# ---------------------------------------------------------------------------
def test_el_paquete_trae_la_funcion_que_se_pide():
    """El paquete debe traer la rebanada literal de los TRES tramos pedidos.

    Hoy NO los trae: el empaquetador entrega leyes y pruebas vecinas.
    Este assert FALLA hoy (rojo por su motivo) y pasara cuando el empaquetador
    respete el NECESITO_LEER y entregue la rebanada literal de cada funcion.
    """
    paquete = _paquete_de_hoy()

    ausentes = _tramos_ausentes(paquete)
    assert ausentes == [], (
        "El paquete NO trae la rebanada literal de los tramos pedidos. "
        "Faltan: %r. El encargo pide literalmente el trozo de %s con "
        "processPhoto, el manejador de camara y el guardado, y el paquete "
        "entrego leyes y pruebas vecinas, sin ninguno de esos tramos."
        % (ausentes, ARCHIVO_ANFITRION)
    )


def test_el_paquete_no_es_un_recorte_ciego_de_80_renglones():
    """Un recorte ciego de los primeros 80 renglones nunca alcanza processPhoto.

    processPhoto vive en el renglon %d de %s, que tiene %d renglones.
    """ % (RENGLON_REAL_DE_PROCESSPHOTO, ARCHIVO_ANFITRION, RENGLONES_TOTALES_ANFITRION)
    paquete = _paquete_de_hoy()

    assert not _es_recorte_ciego(paquete), (
        "El paquete es un recorte ciego de los primeros %d renglones. "
        "processPhoto vive en el renglon %d de %s (que tiene %d renglones), "
        "asi que un recorte de %d renglones NUNCA lo alcanza."
        % (
            RENGLONES_RECORTE_CIEGO,
            RENGLON_REAL_DE_PROCESSPHOTO,
            ARCHIVO_ANFITRION,
            RENGLONES_TOTALES_ANFITRION,
            RENGLONES_RECORTE_CIEGO,
        )
    )


def test_la_vigia_vigila_al_paquete_y_no_al_anfitrion():
    """La vigia NO lee el archivo del disco: vigila el texto que el paquete entrega.

    Si leyera el anfitrion, arreglar el empaquetador no la pondria verde nunca.
    Esta prueba comprueba que la vigia trabaja sobre el texto del paquete.
    """
    # Un paquete que SI trae los tres tramos debe pasar las comprobaciones.
    paquete_bueno = (
        "// renglon 2381 de app_web.html\n"
        "function processPhoto(file) {\n"
        "  // ...\n"
        "}\n"
        "function onCamera(event) {\n"
        "  // ...\n"
        "}\n"
        "function savePhoto() {\n"
        "  // ...\n"
        "}\n"
    )
    assert _tramos_ausentes(paquete_bueno) == [], (
        "La vigia no reconoce un paquete que SI trae los tres tramos. "
        "La vigia esta mirando al sitio equivocado."
    )
    assert not _es_recorte_ciego(paquete_bueno), (
        "La vigia confunde un paquete bueno con un recorte ciego."
    )


def test_la_vigia_nace_roja_por_su_motivo():
    """La vigia debe nacer ROJA por un assert que falla, no por error de sintaxis.

    Esta prueba comprueba que el paquete de hoy efectivamente NO trae los tramos,
    que es el motivo por el que la vigia nace roja.
    """
    paquete = _paquete_de_hoy()
    ausentes = _tramos_ausentes(paquete)
    assert len(ausentes) == len(TRAMOS_PEDIDOS), (
        "Se esperaba que el paquete de hoy NO trajera ninguno de los %d tramos, "
        "pero trae %d. La vigia no nace roja por su motivo."
        % (len(TRAMOS_PEDIDOS), len(TRAMOS_PEDIDOS) - len(ausentes))
    )


if __name__ == "__main__":
    # Ejecucion directa: muestra el estado de la vigia sin pytest.
    paquete = _paquete_de_hoy()
    ausentes = _tramos_ausentes(paquete)
    print("Tramos pedidos:", [n for n, _ in TRAMOS_PEDIDOS])
    print("Tramos ausentes:", ausentes)
    print("Es recorte ciego:", _es_recorte_ciego(paquete))
    if ausentes:
        print("VIGIA ROJA: el paquete no trae la rebanada literal de los tramos pedidos.")
    else:
        print("VIGIA VERDE: el paquete trae la rebanada literal de los tramos pedidos.")
