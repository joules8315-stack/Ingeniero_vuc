"""Mide lo que hoy se le pide a las IA y cuanto de eso se fue en llamadas sin provecho.

Nace de la orden R15 y de la definicion de economico que dio Julio el 2026-09-27,
punto 1: todo lo que no necesita IA se hace por programa.

Este programa NO gasta ni una llamada a ninguna IA y NO toca la red. Solo lee el
cuaderno de llamadas que ya esta escrito en disco y saca las cuentas.

Contrato que cumple, tal cual lo exige
vigias/test_vigia_programa_antes_que_ia.py:

  - leer_cuaderno(ruta) -> lista de diccionarios, uno por renglon legible,
    saltando en silencio los renglones rotos, y lista vacia si el archivo no esta.
  - agrupar(lista) -> diccionario cuya clave es la clase de la llamada (texto
    'sin_nombre' cuando la clase viene vacia) y cuyo valor es otro diccionario
    con estas cinco claves exactas: llamadas, segundos, letras, sin_provecho,
    segundos_sin_provecho.
  - medir(raiz) -> lee memoria/CUADERNO_DE_LLAMADAS.jsonl dentro de esa raiz,
    escribe memoria/MEDIDA_PROGRAMA_ANTES_QUE_IA.md dentro de esa misma raiz y
    devuelve lo que dio agrupar.
"""

import json
import sys
from pathlib import Path


# --- Arranque de sys.path, igual que en los otros programas de la carpeta arnes ---
RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


# Nombre del cuaderno que se lee y del documento que se escribe.
NOMBRE_CUADERNO = "CUADERNO_DE_LLAMADAS.jsonl"
NOMBRE_DOCUMENTO = "MEDIDA_PROGRAMA_ANTES_QUE_IA.md"

# Texto que se usa cuando la clase viene vacia.
SIN_NOMBRE = "sin_nombre"

# Las cinco cuentas exactas que lleva cada clase.
CLAVES = (
    "llamadas",
    "segundos",
    "letras",
    "sin_provecho",
    "segundos_sin_provecho",
)


def leer_cuaderno(ruta):
    """Devuelve la lista de renglones legibles del cuaderno en esa ruta.

    Un renglon por linea. Los renglones rotos se saltan en silencio. Si el
    archivo no esta, devuelve lista vacia.
    """
    camino = Path(ruta)
    if not camino.exists():
        return []

    leidos = []
    try:
        texto = camino.read_text(encoding="utf-8")
    except OSError:
        return []

    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            renglon = json.loads(linea)
        except (ValueError, TypeError):
            continue
        if isinstance(renglon, dict):
            leidos.append(renglon)
    return leidos


def _numero(valor):
    """Devuelve el valor como numero, o 0 si no se puede leer como numero."""
    if isinstance(valor, bool):
        return 0
    if isinstance(valor, (int, float)):
        return valor
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0


def agrupar(lista):
    """Agrupa los renglones por clase y saca las cinco cuentas de cada clase.

    La clave es la clase de la llamada, o el texto 'sin_nombre' cuando la clase
    viene vacia. El valor es un diccionario con las cinco claves exactas:
    llamadas, segundos, letras, sin_provecho, segundos_sin_provecho.
    """
    cuentas = {}
    for renglon in lista:
        if not isinstance(renglon, dict):
            continue

        clase = renglon.get("clase")
        if clase is None or str(clase).strip() == "":
            clase = SIN_NOMBRE
        else:
            clase = str(clase)

        if clase not in cuentas:
            cuentas[clase] = {clave: 0 for clave in CLAVES}

        cubo = cuentas[clase]
        segundos = _numero(renglon.get("segundos"))
        tamano = _numero(renglon.get("tamano"))
        resultado = renglon.get("resultado")

        cubo["llamadas"] += 1
        cubo["segundos"] += segundos
        cubo["letras"] += tamano
        if resultado != "ok":
            cubo["sin_provecho"] += 1
            cubo["segundos_sin_provecho"] += segundos

    return cuentas


def _minutos(segundos):
    """Devuelve los segundos escritos tambien en minutos, con dos decimales."""
    return round(_numero(segundos) / 60.0, 2)


def _tabla(cuentas):
    """Arma la tabla del documento: una fila por clase, mas la fila de totales."""
    lineas = []
    lineas.append(
        "| clase | llamadas | segundos | minutos | letras | sin_provecho "
        "| segundos_sin_provecho |"
    )
    lineas.append("|---|---|---|---|---|---|---|")

    totales = {clave: 0 for clave in CLAVES}
    for clase in sorted(cuentas):
        cubo = cuentas[clase]
        for clave in CLAVES:
            totales[clave] += cubo[clave]
        lineas.append(
            "| %s | %s | %s | %s | %s | %s | %s |"
            % (
                clase,
                cubo["llamadas"],
                cubo["segundos"],
                _minutos(cubo["segundos"]),
                cubo["letras"],
                cubo["sin_provecho"],
                cubo["segundos_sin_provecho"],
            )
        )

    lineas.append(
        "| TOTAL | %s | %s | %s | %s | %s | %s |"
        % (
            totales["llamadas"],
            totales["segundos"],
            _minutos(totales["segundos"]),
            totales["letras"],
            totales["sin_provecho"],
            totales["segundos_sin_provecho"],
        )
    )
    return lineas


def _lista_por_segundos_sin_provecho(cuentas):
    """Devuelve las clases ordenadas por segundos sin provecho, de mayor a menor."""
    ordenadas = sorted(
        cuentas.items(),
        key=lambda par: (-_numero(par[1]["segundos_sin_provecho"]), par[0]),
    )
    return ordenadas


def _documento(cuentas):
    """Arma el texto del documento. Solo numeros: no saca conclusiones."""
    lineas = []
    lineas.append("# MEDIDA — LO QUE SE LE PIDE A LA IA ANTES QUE A UN PROGRAMA")
    lineas.append("")
    lineas.append(
        "Nace de la orden R15 y de la definicion de economico que dio Julio el "
        "2026-09-27, punto 1: todo lo que no necesita IA se hace por programa."
    )
    lineas.append("")
    lineas.append(
        "Esta medida se saca del cuaderno de llamadas que ya esta en disco. "
        "No gasta ninguna llamada a ninguna IA y no toca la red."
    )
    lineas.append("")
    lineas.append("## Cuentas por clase")
    lineas.append("")
    lineas.extend(_tabla(cuentas))
    lineas.append("")
    lineas.append("## Clases ordenadas por segundos sin provecho (de mayor a menor)")
    lineas.append("")
    lineas.append(
        "Esta es la lista con la que se decidira despues que trabajo se pasa a programa."
    )
    lineas.append("")
    for puesto, (clase, cubo) in enumerate(_lista_por_segundos_sin_provecho(cuentas), 1):
        lineas.append(
            "%s. %s — segundos_sin_provecho: %s | sin_provecho: %s | llamadas: %s"
            % (
                puesto,
                clase,
                cubo["segundos_sin_provecho"],
                cubo["sin_provecho"],
                cubo["llamadas"],
            )
        )
    lineas.append("")
    return "\n".join(lineas)


def medir(raiz):
    """Lee el cuaderno de esa raiz, escribe el documento y devuelve las cuentas.

    Lee memoria/CUADERNO_DE_LLAMADAS.jsonl dentro de esa raiz, escribe
    memoria/MEDIDA_PROGRAMA_ANTES_QUE_IA.md dentro de esa misma raiz y devuelve
    lo que dio agrupar.
    """
    raiz = Path(raiz)
    carpeta = raiz / "memoria"
    carpeta.mkdir(parents=True, exist_ok=True)

    cuaderno = carpeta / NOMBRE_CUADERNO
    documento = carpeta / NOMBRE_DOCUMENTO

    leidos = leer_cuaderno(cuaderno)
    cuentas = agrupar(leidos)

    documento.write_text(_documento(cuentas), encoding="utf-8")
    return cuentas


def main():
    """Cuando se corre solo, mide la raiz de verdad y dice donde quedo el documento."""
    raiz_de_verdad = Path(__file__).resolve().parent.parent
    medir(raiz_de_verdad)
    documento = raiz_de_verdad / "memoria" / NOMBRE_DOCUMENTO
    print("El documento quedo en: %s" % documento)


if __name__ == "__main__":
    main()
