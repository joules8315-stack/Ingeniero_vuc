"""Mide los puntos donde llego una respuesta y el paso siguiente no salio solo.

Nace de la orden R16 y de la definicion de economico que dio Julio el 2026-09-27,
punto 5: que todo este conectado y que las respuestas tengan disparadores.

Este programa NO gasta ni una llamada a ninguna IA y NO toca la red. Solo lee el
cuaderno de llamadas y el archivo de ordenes que ya estan escritos en disco, y
saca las cuentas.

Contrato que cumple, tal cual lo exige
vigias/test_vigia_una_respuesta_dispara_la_accion_siguiente.py:

  - huecos(llamadas, tope=120) -> lista ordenada de mayor a menor por
    segundos_perdidos, solo con los huecos iguales o mayores que el tope. Cada
    hueco trae siete claves exactas: cuando_termino, clase_antes, quien_antes,
    cuando_empezo_la_siguiente, clase_despues, quien_despues, segundos_perdidos.
    En el cuaderno el campo cuando es la hora en que la llamada TERMINO y el
    campo segundos es lo que duro, asi que empezo en cuando menos segundos. Se
    ordena por hora antes de medir y se salta en silencio la llamada con hora
    ilegible.
  - ordenes_listas_y_paradas(ordenes) -> las ordenes con estado pendiente cuya
    lista depende esta vacia o tiene todas sus ordenes en estado hecha.
  - medir(raiz) -> lee memoria/CUADERNO_DE_LLAMADAS.jsonl y memoria/ORDENES.json
    dentro de esa raiz, escribe memoria/MEDIDA_DISPARADORES_QUE_FALTAN.md dentro
    de esa misma raiz y devuelve un diccionario con dos claves exactas: huecos y
    ordenes_paradas.
"""

import json
import sys
from pathlib import Path


# --- Arranque de sys.path, igual que en los otros programas de la carpeta arnes ---
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


# Se reutiliza el lector de cuaderno que ya existe, para no escribir dos veces lo mismo.
from arnes.medir_lo_que_puede_hacer_un_programa import leer_cuaderno


# Nombres de los archivos que se leen y del documento que se escribe.
NOMBRE_CUADERNO = "CUADERNO_DE_LLAMADAS.jsonl"
NOMBRE_ORDENES = "ORDENES.json"
NOMBRE_DOCUMENTO = "MEDIDA_DISPARADORES_QUE_FALTAN.md"

# Tope por defecto, en segundos, para considerar que un hueco es un disparador que falto.
TOPE_POR_DEFECTO = 120

# Cuantos huecos se listan en la tabla del documento.
CUANTOS_EN_LA_TABLA = 20

# Texto que se usa cuando un campo viene vacio.
SIN_NOMBRE = "sin_nombre"


# --- Utilidades internas ---


def _texto(valor):
    """Devuelve el valor como texto, o SIN_NOMBRE si viene vacio o no es texto."""
    if valor is None:
        return SIN_NOMBRE
    if isinstance(valor, str):
        limpio = valor.strip()
        return limpio if limpio else SIN_NOMBRE
    return str(valor)


def _hora(valor):
    """Devuelve el valor como numero, o None si no se puede leer como hora."""
    from datetime import datetime
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        try:
            return datetime.strptime(valor.strip(), "%Y-%m-%d %H:%M:%S").timestamp()
        except (ValueError, TypeError):
            return None
    return None


def _segundos(valor):
    """Devuelve el valor como numero de segundos, o 0.0 si no se puede leer."""
    if isinstance(valor, bool):
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        try:
            return float(valor.strip())
        except (ValueError, TypeError):
            return 0.0
    return 0.0


# --- Piezas del contrato ---


def huecos(llamadas, tope=TOPE_POR_DEFECTO):
    """Devuelve los huecos entre llamadas que llegan o pasan del tope.

    Recibe la lista de llamadas del cuaderno y un tope en segundos (120 por
    defecto). En el cuaderno el campo cuando es la hora en que la llamada
    TERMINO y el campo segundos es lo que duro, asi que empezo en
    cuando menos segundos. El hueco es lo que pasa entre una llamada que
    termina y la siguiente que empieza.

    Se ordena por hora antes de medir y se salta en silencio la llamada con
    hora ilegible. Devuelve una lista ordenada de mayor a menor por
    segundos_perdidos, solo con los huecos iguales o mayores que el tope.
    """
    from datetime import datetime
    if not isinstance(llamadas, list):
        return []

    # Se queda solo con las llamadas que tienen hora legible.
    legibles = []
    for llamada in llamadas:
        if not isinstance(llamada, dict):
            continue
        termino = _hora(llamada.get("cuando"))
        if termino is None:
            continue
        legibles.append((termino, llamada))

    # Se ordena por hora antes de medir.
    legibles.sort(key=lambda par: par[0])

    encontrados = []
    for indice in range(len(legibles) - 1):
        termino_antes, antes = legibles[indice]
        termino_despues, despues = legibles[indice + 1]

        empezo_antes = termino_antes - _segundos(antes.get("segundos"))
        empezo_despues = termino_despues - _segundos(despues.get("segundos"))

        perdidos = empezo_despues - termino_antes
        if perdidos < tope:
            continue

        cuando_termino_texto = _texto(antes.get("cuando"))
        try:
            cuando_empezo_texto = datetime.fromtimestamp(empezo_despues).strftime("%Y-%m-%d %H:%M:%S")
        except TypeError:
            cuando_empezo_texto = ""

        encontrados.append(
            {
                "cuando_termino": cuando_termino_texto,
                "clase_antes": _texto(antes.get("clase")),
                "quien_antes": _texto(antes.get("quien")),
                "cuando_empezo_la_siguiente": cuando_empezo_texto,
                "clase_despues": _texto(despues.get("clase")),
                "quien_despues": _texto(despues.get("quien")),
                "segundos_perdidos": perdidos,
            }
        )

    encontrados.sort(key=lambda h: h["segundos_perdidos"], reverse=True)
    return encontrados


def ordenes_listas_y_paradas(ordenes):
    """Devuelve las ordenes pendientes cuyas dependencias ya estan hechas.

    Recibe la lista de ordenes. Devuelve las que tienen estado pendiente y cuya
    lista depende esta vacia o tiene todas sus ordenes en estado hecha. Son los
    sitios donde el paso siguiente podia salir solo y nadie lo dio.
    """
    if not isinstance(ordenes, list):
        return []

    por_id = {}
    for orden in ordenes:
        if not isinstance(orden, dict):
            continue
        identificador = orden.get("id")
        if identificador is None:
            continue
        por_id[identificador] = orden

    listas = []
    for orden in ordenes:
        if not isinstance(orden, dict):
            continue
        if _texto(orden.get("estado")) != "pendiente":
            continue

        depende = orden.get("depende")
        if depende is None:
            depende = []
        if not isinstance(depende, list):
            continue

        if len(depende) == 0:
            listas.append(orden)
            continue

        todas_hechas = True
        for identificador in depende:
            anterior = por_id.get(identificador)
            if anterior is None:
                todas_hechas = False
                break
            if _texto(anterior.get("estado")) != "hecha":
                todas_hechas = False
                break

        if todas_hechas:
            listas.append(orden)

    return listas


# --- Documento ---


def _tabla_huecos(lista_huecos):
    """Arma la tabla con los huecos mas grandes, con su hora y sus minutos."""
    lineas = []
    lineas.append("| hora en que termino | que se pidio antes | que se pidio despues | minutos perdidos |")
    lineas.append("| --- | --- | --- | --- |")
    for hueco in lista_huecos[:CUANTOS_EN_LA_TABLA]:
        minutos = hueco["segundos_perdidos"] / 60.0
        lineas.append(
            "| %s | %s | %s | %.2f |"
            % (
                hueco["cuando_termino"],
                hueco["clase_antes"],
                hueco["clase_despues"],
                minutos,
            )
        )
    return lineas


def _documento(lista_huecos, lista_paradas):
    """Arma el texto del documento. Solo numeros: no saca conclusiones."""
    lineas = []
    lineas.append("# MEDIDA — DISPARADORES QUE FALTAN")
    lineas.append("")
    lineas.append(
        "Nace de la orden R16 y de la definicion de economico que dio Julio el "
        "2026-09-27, punto 5: que todo este conectado y que las respuestas tengan "
        "disparadores."
    )
    lineas.append("")
    lineas.append(
        "Esta medida se saca del cuaderno de llamadas y del archivo de ordenes que "
        "ya estan en disco. No gasta ninguna llamada a ninguna IA y no toca la red."
    )
    lineas.append("")

    lineas.append("## Los veinte huecos mas grandes")
    lineas.append("")
    if lista_huecos:
        lineas.extend(_tabla_huecos(lista_huecos))
    else:
        lineas.append("No hay huecos que lleguen al tope.")
    lineas.append("")

    total_segundos = 0.0
    for hueco in lista_huecos:
        total_segundos += hueco["segundos_perdidos"]
    lineas.append("## Suma total de minutos perdidos en todos los huecos")
    lineas.append("")
    lineas.append("Total de minutos perdidos: %.2f" % (total_segundos / 60.0))
    lineas.append("")

    lineas.append("## Ordenes que estaban listas y paradas")
    lineas.append("")
    if lista_paradas:
        for orden in lista_paradas:
            lineas.append(
                "- %s — %s" % (_texto(orden.get("id")), _texto(orden.get("titulo")))
            )
    else:
        lineas.append("No hay ordenes listas y paradas.")
    lineas.append("")

    return "\n".join(lineas)


# --- Pieza principal ---


def medir(raiz):
    """Lee el cuaderno y las ordenes de esa raiz, escribe el documento y devuelve las cuentas.

    Lee memoria/CUADERNO_DE_LLAMADAS.jsonl y memoria/ORDENES.json dentro de esa
    raiz, escribe memoria/MEDIDA_DISPARADORES_QUE_FALTAN.md dentro de esa misma
    raiz y devuelve un diccionario con dos claves exactas: huecos y
    ordenes_paradas.
    """
    raiz = Path(raiz)
    carpeta = raiz / "memoria"
    carpeta.mkdir(parents=True, exist_ok=True)

    camino_cuaderno = carpeta / NOMBRE_CUADERNO
    camino_ordenes = carpeta / NOMBRE_ORDENES
    camino_documento = carpeta / NOMBRE_DOCUMENTO

    llamadas = leer_cuaderno(camino_cuaderno)
    lista_huecos = huecos(llamadas)

    ordenes = []
    if camino_ordenes.exists():
        try:
            texto = camino_ordenes.read_text(encoding="utf-8")
            leido = json.loads(texto)
            if isinstance(leido, list):
                ordenes = leido
        except (OSError, ValueError, TypeError):
            ordenes = []

    lista_paradas = ordenes_listas_y_paradas(ordenes)

    camino_documento.write_text(
        _documento(lista_huecos, lista_paradas), encoding="utf-8"
    )

    return {"huecos": lista_huecos, "ordenes_paradas": lista_paradas}


# --- Arranque directo ---


def _main():
    """Mide la carpeta que esta un nivel arriba de la carpeta arnes."""
    raiz = Path(__file__).resolve().parent.parent
    resultado = medir(raiz)
    documento = raiz / "memoria" / NOMBRE_DOCUMENTO
    print("Documento escrito en: %s" % documento)
    print("Huecos encontrados: %d" % len(resultado["huecos"]))
    print("Ordenes listas y paradas: %d" % len(resultado["ordenes_paradas"]))


if __name__ == "__main__":
    _main()
