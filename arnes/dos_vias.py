"""arnes/dos_vias.py — LAS DOS VIAS: EL CODIGO VIAJA LIMPIO, LA GUIA VA APARTE.

Ley: CONTRATO_LAS_DOS_VIAS (Julio, 2026-10-01).

Que hace esta pieza, sin IA y sin lanzar nunca:

  1. armar_guia_y_codigo(orden) -> (guia, codigo)
     Dada una orden (dict), devuelve DOS textos separados:
       - la GUIA: objetivo, donde (pieza y funciones de la orden), motivo exacto
         del fallo anterior (leido del mensaje de la vigia roja y de los motivos
         del ultimo rechazo) y lo que NO se debe repetir.
       - el CODIGO: la funcion completa de la pieza, LITERAL, tal como la
         entrego el mostrador. Si no cabe entera, se parte por funcion; nunca
         se recorta.

  2. hay_mezcla(guia, codigo) -> bool
     Dice si la guia se colo dentro del codigo o el codigo dentro de la guia.

  3. vigia_dos_vias(guia, codigo) -> dict
     Cubre las CUATRO filas de la tabla de verdad de CONTRATO_LAS_DOS_VIAS:
       fila 1: guia aparte y codigo limpio            -> pasa=True
       fila 2: guia dentro del codigo                 -> pasa=False
       fila 3: codigo dentro de la guia               -> pasa=False
       fila 4: una sola via (falta guia o codigo)     -> pasa=False

Reglas duras que respeta esta pieza:
  - Sin IA. Solo texto y comparaciones.
  - Nunca lanza: toda entrada rara se devuelve como resultado, no como excepcion.
  - No se inventa el codigo: se toma LITERAL de la orden (campos 'codigo',
    'codigo_literal', 'funcion', 'pieza_texto' o 'texto_pieza').
  - Si el codigo no cabe entero, se parte por funcion (nunca se recorta).
  - Nada de sorted() sobre llaves de la orden: se itera en el orden en que
    vienen, que es estable y no puede lanzar por tipos mezclados.

Fallo anterior que esta pieza NO debe repetir:
  - Los guardas 'and not' de las dos detecciones de mezcla hacian que las filas
    2 y 3 de CONTRATO_LAS_DOS_VIAS devolvieran pasa=True, aprobando paquetes
    Exactly que la ley debe rechazar.
  - Un sorted() sobre llaves de la orden podia lanzar si las llaves no eran
    comparables entre si.
"""

from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# Constantes de la ley
# ---------------------------------------------------------------------------

#: Campos de la orden donde puede venir el codigo LITERAL de la pieza.
CAMPOS_CODIGO = (
    "codigo",
    "codigo_literal",
    "funcion",
    "pieza_texto",
    "texto_pieza",
)

#: Campos de la orden donde puede venir el nombre de la pieza.
CAMPOS_PIEZA = (
    "pieza",
    "archivo",
    "ruta",
    "fichero",
)

#: Campos de la orden donde puede venir el objetivo.
CAMPOS_OBJETIVO = (
    "objetivo",
    "que_se_repara",
    "problema",
    "encargo",
)

#: Campos de la orden donde puede venir el motivo del fallo anterior.
CAMPOS_MOTIVO = (
    "motivo",
    "motivos",
    "motivo_rechazo",
    "motivos_ultimo_rechazo",
    "mensaje_vigia_roja",
    "vigia_roja",
    "fallo_anterior",
)

#: Campos de la orden donde puede venir lo que NO se debe repetir.
CAMPOS_NO_REPETIR = (
    "no_repetir",
    "no_volver_a",
    "prohibido",
)

#: Campos de la orden donde puede venir la lista de funciones de la pieza.
CAMPOS_FUNCIONES = (
    "funciones",
    "funciones_de_la_orden",
    "nombres_funciones",
)

#: Marcas que abren y cierran la GUIA dentro de un texto.
MARCA_GUIA_INI = "<<<GUIA>>>"
MARCA_GUIA_FIN = "<<<FIN_GUIA>>>"

#: Marcas que abren y cierran el CODIGO dentro de un texto.
MARCA_CODIGO_INI = "<<<CODIGO>>>"
MARCA_CODIGO_FIN = "<<<FIN_CODIGO>>>"

#: Cabeceras legibles que usa la guia.
CAB_OBJETIVO = "OBJETIVO:"
CAB_DONDE = "DONDE:"
CAB_MOTIVO = "MOTIVO DEL FALLO ANTERIOR:"
CAB_NO_REPETIR = "LO QUE NO SE DEBE REPETIR:"

#: Tope por defecto de letras para un bloque de codigo. Si no cabe, se parte
#: por funcion; NUNCA se recorta.
TOPE_CODIGO_POR_DEFECTO = 20000


# ---------------------------------------------------------------------------
# Utilidades internas (nunca lanzan)
# ---------------------------------------------------------------------------


def _texto(valor):
    """Convierte cualquier cosa a texto sin lanzar.

    None -> "". Listas y tuplas se unen con saltos de linea. Cualquier otra
    cosa se pasa por str() dentro de un try/except.
    """
    if valor is None:
        return ""
    if isinstance(valor, str):
        return valor
    if isinstance(valor, (list, tuple)):
        trozos = []
        for elemento in valor:
            trozos.append(_texto(elemento))
        return "\n".join(t for t in trozos if t)
    try:
        return str(valor)
    except Exception:
        return ""


def _primero_no_vacio(orden, campos):
    """Devuelve el primer campo no vacio de la orden, en el orden dado.

    Itera en el orden de 'campos' (una tupla fija), NUNCA sobre las llaves de
    la orden. Asi no hay sorted() ni comparaciones entre llaves que puedan
    lanzar.
    """
    if not isinstance(orden, dict):
        return ""
    for campo in campos:
        if campo in orden:
            valor = _texto(orden.get(campo))
            if valor.strip():
                return valor
    return ""


def _lista_funciones(orden):
    """Devuelve la lista de funciones de la orden, sin lanzar.

    Acepta lista, tupla o texto separado por comas o saltos de linea. Si no
    hay nada, devuelve lista vacia.
    """
    if not isinstance(orden, dict):
        return []
    crudo = None
    for campo in CAMPOS_FUNCIONES:
        if campo in orden:
            crudo = orden.get(campo)
            break
    if crudo is None:
        return []
    if isinstance(crudo, (list, tuple)):
        salida = []
        for elemento in crudo:
            texto = _texto(elemento).strip()
            if texto:
                salida.append(texto)
        return salida
    texto = _texto(crudo)
    if not texto.strip():
        return []
    partes = re.split(r"[,\n;]+", texto)
    salida = []
    for parte in partes:
        limpio = parte.strip()
        if limpio:
            salida.append(limpio)
    return salida


def _nombre_pieza(orden):
    """Nombre de la pieza segun la orden, o cadena vacia."""
    return _primero_no_vacio(orden, CAMPOS_PIEZA).strip()


def _objetivo(orden):
    """Objetivo segun la orden, o cadena vacia."""
    return _primero_no_vacio(orden, CAMPOS_OBJETIVO).strip()


def _motivo(orden):
    """Motivo exacto del fallo anterior, o cadena vacia."""
    return _primero_no_vacio(orden, CAMPOS_MOTIVO).strip()


def _no_repetir(orden):
    """Lo que no se debe repetir, o cadena vacia."""
    return _primero_no_vacio(orden, CAMPOS_NO_REPETIR).strip()


def _codigo_literal(orden):
    """Codigo LITERAL de la pieza, tal como lo entrego el mostrador.

    No se adivina ni se reescribe: se toma el texto tal cual viene en la orden.
    """
    return _primero_no_vacio(orden, CAMPOS_CODIGO)


def _partir_por_funcion(codigo, tope):
    """Parte el codigo por funcion si no cabe entero. NUNCA recorta.

    Devuelve una lista de trozos. Cada trozo es una funcion completa (o el
    bloque suelto que no se pudo atribuir a una funcion). La suma de los trozos
    es exactamente el codigo original: no se pierde ni una letra.
    """
    if not codigo:
        return []
    if len(codigo) <= tope:
        return [codigo]

    lineas = codigo.splitlines(keepends=True)
    if not lineas:
        return [codigo]

    # Localiza los inicios de funcion (def/class a columna 0).
    inicios = []
    for indice, linea in enumerate(lineas):
        if re.match(r"^(def|class|async\s+def)\s", linea):
            inicios.append(indice)

    if not inicios:
        # No hay funciones: se parte por bloques de lineas sin recortar.
        trozos = []
        actual = []
        tam = 0
        for linea in lineas:
            if actual and tam + len(linea) > tope:
                trozos.append("".join(actual))
                actual = []
                tam = 0
            actual.append(linea)
            tam += len(linea)
        if actual:
            trozos.append("".join(actual))
        return trozos

    # Cabecera antes de la primera funcion (imports, docstring, etc.).
    trozos = []
    cabecera = "".join(lineas[: inicios[0]])
    if cabecera:
        trozos.append(cabecera)

    # Cada funcion, entera, sin recortar.
    for posicion, inicio in enumerate(inicios):
        if posicion + 1 < len(inicios):
            fin = inicios[posicion + 1]
        else:
            fin = len(lineas)
        trozos.append("".join(lineas[inicio:fin]))

    # Si un trozo suelto sigue pasando el tope, se parte por lineas sin
    # recortar ninguna linea entera.
    salida = []
    for trozo in trozos:
        if len(trozo) <= tope:
            salida.append(trozo)
            continue
        lineas_trozo = trozo.splitlines(keepends=True)
        actual = []
        tam = 0
        for linea in lineas_trozo:
            if actual and tam + len(linea) > tope:
                salida.append("".join(actual))
                actual = []
                tam = 0
            actual.append(linea)
            tam += len(linea)
        if actual:
            salida.append("".join(actual))
    return salida


def _contiene_marca(texto, ini, fin):
    """True si 'texto' lleva el bloque marcado por ini/fin."""
    if not texto:
        return False
    return (ini in texto) and (fin in texto)


def _normalizar_para_comparar(texto):
    """Normaliza un texto para comparar sin depender de espacios."""
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def _una_dentro_de_otra(pequeno, grande):
    """True si 'pequeno' aparece dentro de 'grande' (normalizado).

    Se exige un tamano minimo para no confundir coincidencias triviales.
    """
    if not pequeno or not grande:
        return False
    a = _normalizar_para_comparar(pequeno)
    b = _normalizar_para_comparar(grande)
    if len(a) < 20 or len(b) < 20:
        return False
    return a in b


# ---------------------------------------------------------------------------
# API publica
# ---------------------------------------------------------------------------


def armar_guia_y_codigo(orden, tope_codigo=TOPE_CODIGO_POR_DEFECTO):
    """Arma la GUIA y el CODIGO a partir de una orden.

    Devuelve una tupla (guia, codigo):

      - guia: texto con OBJETIVO, DONDE (pieza y funciones), MOTIVO DEL FALLO
        ANTERIOR (leido del mensaje de la vigia roja y de los motivos del
        ultimo rechazo) y LO QUE NO SE DEBE REPETIR.
      - codigo: la funcion completa de la pieza, LITERAL, tal como la entrego
        el mostrador. Si no cabe entera en 'tope_codigo', se parte por funcion
        y los trozos se unen con una marca de corte; NUNCA se recorta.

    Nunca lanza: si la orden viene vacia o rara, devuelve textos vacios.
    """
    try:
        if not isinstance(orden, dict):
            return ("", "")

        objetivo = _objetivo(orden)
        pieza = _nombre_pieza(orden)
        funciones = _lista_funciones(orden)
        motivo = _motivo(orden)
        no_repetir = _no_repetir(orden)
        codigo_crudo = _codigo_literal(orden)

        # --- GUIA ---------------------------------------------------------
        lineas = []
        lineas.append(MARCA_GUIA_INI)
        lineas.append(CAB_OBJETIVO)
        lineas.append(objetivo if objetivo else "(sin objetivo declarado)")
        lineas.append("")
        lineas.append(CAB_DONDE)
        lineas.append("pieza: " + (pieza if pieza else "(sin pieza declarada)"))
        if funciones:
            lineas.append("funciones de la orden:")
            for nombre in funciones:
                lineas.append("  - " + nombre)
        else:
            lineas.append("funciones de la orden: (ninguna declarada)")
        lineas.append("")
        lineas.append(CAB_MOTIVO)
        lineas.append(motivo if motivo else "(sin motivo registrado)")
        lineas.append("")
        lineas.append(CAB_NO_REPETIR)
        lineas.append(no_repetir if no_repetir else "(sin prohibiciones registradas)")
        lineas.append(MARCA_GUIA_FIN)
        guia = "\n".join(lineas)

        # --- CODIGO -------------------------------------------------------
        if not codigo_crudo:
            codigo = ""
        else:
            trozos = _partir_por_funcion(codigo_crudo, tope_codigo)
            if len(trozos) <= 1:
                codigo = codigo_crudo
            else:
                partes = []
                for indice, trozo in enumerate(trozos, start=1):
                    partes.append(
                        "# --- trozo %d de %d (partido por funcion, sin recortar) ---"
                        % (indice, len(trozos))
                    )
                    partes.append(trozo)
                codigo = "\n".join(partes)

        return (guia, codigo)
    except Exception:
        # La ley dice: nunca lanza. Ante cualquier cosa rara, se devuelve vacio.
        return ("", "")


def hay_mezcla(guia, codigo):
    """Dice si hay mezcla entre las dos vias.

    Devuelve True si:
      - la guia se colo dentro del codigo (marcas de guia en el codigo, o el
        texto de la guia aparece dentro del codigo), o
      - el codigo se colo dentro de la guia (marcas de codigo en la guia, o el
        texto del codigo aparece dentro de la guia).

    Devuelve False si cada via va limpia y aparte.
    Nunca lanza.
    """
    try:
        guia_txt = _texto(guia)
        codigo_txt = _texto(codigo)

        # 1) Marcas cruzadas: la marca de una via dentro de la otra.
        if _contiene_marca(codigo_txt, MARCA_GUIA_INI, MARCA_GUIA_FIN):
            return True
        if _contiene_marca(guia_txt, MARCA_CODIGO_INI, MARCA_CODIGO_FIN):
            return True

        # 2) Cabeceras de la guia dentro del codigo.
        for cabecera in (CAB_OBJETIVO, CAB_DONDE, CAB_MOTIVO, CAB_NO_REPETIR):
            if cabecera in codigo_txt:
                return True

        # 3) El texto de una via aparece dentro de la otra.
        if _una_dentro_de_otra(guia_txt, codigo_txt):
            return True
        if _una_dentro_de_otra(codigo_txt, guia_txt):
            return True

        return False
    except Exception:
        # Ante duda, se declara mezcla: la ley prefiere rechazar a aprobar mal.
        return True


def vigia_dos_vias(guia, codigo):
    """Vigia de las CUATRO filas de CONTRATO_LAS_DOS_VIAS.

    Tabla de verdad:
      fila 1: guia aparte y codigo limpio            -> pasa=True
      fila 2: guia dentro del codigo                 -> pasa=False
      fila 3: codigo dentro de la guia               -> pasa=False
      fila 4: una sola via (falta guia o codigo)     -> pasa=False

    Devuelve un dict con:
      - pasa: bool
      - motivo: texto explicando por que pasa o no
      - fila: numero de fila de la tabla (1..4)

    Nunca lanza.
    """
    try:
        guia_txt = _texto(guia)
        codigo_txt = _texto(codigo)

        tiene_guia = bool(guia_txt.strip())
        tiene_codigo = bool(codigo_txt.strip())

        # Fila 4: una sola via. Falta guia o falta codigo.
        if not tiene_guia and not tiene_codigo:
            return {
                "pasa": False,
                "fila": 4,
                "motivo": "faltan las dos vias: no hay guia ni codigo",
            }
        if not tiene_guia:
            return {
                "pasa": False,
                "fila": 4,
                "motivo": "falta la guia: solo viaja el codigo",
            }
        if not tiene_codigo:
            return {
                "pasa": False,
                "fila": 4,
                "motivo": "falta el codigo: solo viaja la guia",
            }

        # Filas 2 y 3: mezcla entre las dos vias.
        # OJO: aqui NO se usa 'and not'. Si hay mezcla, se rechaza.
        if _contiene_marca(codigo_txt, MARCA_GUIA_INI, MARCA_GUIA_FIN):
            return {
                "pasa": False,
                "fila": 2,
                "motivo": "la guia se colo dentro del codigo (marcas de guia en el codigo)",
            }
        if _contiene_marca(guia_txt, MARCA_CODIGO_INI, MARCA_CODIGO_FIN):
            return {
                "pasa": False,
                "fila": 3,
                "motivo": "el codigo se colo dentro de la guia (marcas de codigo en la guia)",
            }

        for cabecera in (CAB_OBJETIVO, CAB_DONDE, CAB_MOTIVO, CAB_NO_REPETIR):
            if cabecera in codigo_txt:
                return {
                    "pasa": False,
                    "fila": 2,
                    "motivo": "la guia se colo dentro del codigo (cabecera '%s')" % cabecera,
                }

        if _una_dentro_de_otra(guia_txt, codigo_txt):
            return {
                "pasa": False,
                "fila": 2,
                "motivo": "la guia se colo dentro del codigo (texto de la guia dentro del codigo)",
            }
        if _una_dentro_de_otra(codigo_txt, guia_txt):
            return {
                "pasa": False,
                "fila": 3,
                "motivo": "el codigo se colo dentro de la guia (texto del codigo dentro de la guia)",
            }

        # Fila 1: guia aparte y codigo limpio.
        return {
            "pasa": True,
            "fila": 1,
            "motivo": "guia aparte y codigo limpio: las dos vias viajan separadas",
        }
    except Exception as error:
        # Nunca lanza: si algo revienta, se rechaza con motivo.
        return {
            "pasa": False,
            "fila": 0,
            "motivo": "error inesperado en la vigia: %s" % (error,),
        }


# ---------------------------------------------------------------------------
# Prueba de la propia vigia (sin IA, sin llaves, sin red)
# ---------------------------------------------------------------------------


def _prueba_de_la_vigia():
    """Comprueba las cuatro filas de CONTRATO_LAS_DOS_VIAS.

    Se ejecuta solo si se llama a mano. No lanza: devuelve True si todo pasa.
    """
    orden = {
        "objetivo": "Que el paquete lleve el codigo a cambiar y la guia aparte.",
        "pieza": "arnes/dos_vias.py",
        "funciones": ["armar_guia_y_codigo", "hay_mezcla", "vigia_dos_vias"],
        "motivo": "Los guardas 'and not' aprobaban las filas 2 y 3.",
        "no_repetir": "No usar 'and not' en las detecciones de mezcla.",
        "codigo": (
            "def sumar(a, b):\n"
            "    return a + b\n"
        ),
    }

    guia, codigo = armar_guia_y_codigo(orden)

    # Fila 1: guia aparte y codigo limpio -> pasa.
    r1 = vigia_dos_vias(guia, codigo)
    if not r1.get("pasa"):
        return False

    # Fila 2: guia dentro del codigo -> NO pasa.
    codigo_con_guia = codigo + "\n" + guia
    r2 = vigia_dos_vias(guia, codigo_con_guia)
    if r2.get("pasa"):
        return False

    # Fila 3: codigo dentro de la guia -> NO pasa.
    guia_con_codigo = guia + "\n" + codigo
    r3 = vigia_dos_vias(guia_con_codigo, codigo)
    if r3.get("pasa"):
        return False

    # Fila 4: una sola via -> NO pasa.
    r4a = vigia_dos_vias(guia, "")
    if r4a.get("pasa"):
        return False
    r4b = vigia_dos_vias("", codigo)
    if r4b.get("pasa"):
        return False

    # hay_mezcla coherente con la vigia.
    if hay_mezcla(guia, codigo):
        return False
    if not hay_mezcla(guia, codigo_con_guia):
        return False
    if not hay_mezcla(guia_con_codigo, codigo):
        return False

    return True


if __name__ == "__main__":
    print("vigia_dos_vias OK:", _prueba_de_la_vigia())
