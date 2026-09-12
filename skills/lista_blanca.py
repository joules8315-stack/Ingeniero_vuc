"""skills/lista_blanca.py — LA LISTA BLANCA DE HERRAMIENTAS DE MANO.

Julio la autorizo SOLO con tres candados y dijo que nada se cuele por ahi nunca,
y que se programe para no meter IA.

Que es: la lista de HERRAMIENTAS DE MANO, las piezas que se lanzan a proposito y
que por eso el contador de dormidas NO debe contar.

Que NO es: una puerta trasera. Es una CUENTA, no un juicio. No entra ninguna IA.
La misma pregunta da siempre la misma respuesta.

Los tres candados (los tres, siempre, y diciendo SIEMPRE el motivo):
  1. la pieza existe en disco;
  2. el porque viene con contenido;
  3. el quien viene con contenido;
  y ademas la pieza tiene que poder lanzarse (traer el arranque propio de Python).

Persistencia: un archivo propio dentro de memoria/, con puerta de desvio por
variable de entorno para que las pruebas no toquen la lista real.
"""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# RUTAS Y PUERTA DE DESVIO
# ---------------------------------------------------------------------------

# Raiz del Ingeniero: este archivo vive en <raiz>/skills/lista_blanca.py
_RAIZ_INGENIERO = Path(__file__).resolve().parent.parent

# Variable de entorno que desvia la lista a un archivo de pruebas.
# Si NO esta puesta, se usa la lista real dentro de memoria/.
VARIABLE_DE_DESVIO = "INGENIERO_LISTA_BLANCA"

# Nombre del archivo propio dentro de memoria/.
NOMBRE_ARCHIVO = "lista_blanca.json"


def _ruta_lista(raiz: Optional[Path] = None) -> Path:
    """Devuelve la ruta del archivo de la lista blanca.

    Orden de decision (determinista, sin IA):
      1. si la variable de entorno VARIABLE_DE_DESVIO trae algo, se usa ESA ruta;
      2. si no, se usa <raiz>/memoria/lista_blanca.json, donde <raiz> es la
         raiz que se pase o, si no se pasa, la raiz del Ingeniero.
    """
    desvio = os.environ.get(VARIABLE_DE_DESVIO, "").strip()
    if desvio:
        return Path(desvio)
    base = Path(raiz) if raiz is not None else _RAIZ_INGENIERO
    return base / "memoria" / NOMBRE_ARCHIVO


def _leer_crudo(ruta: Path) -> Dict[str, Any]:
    """Lee el archivo de la lista. Si no existe o esta roto, devuelve vacio.

    Nunca revienta: una lista ilegible se trata como lista vacia, y se dice.
    """
    if not ruta.exists():
        return {"piezas": []}
    try:
        with ruta.open("r", encoding="utf-8") as f:
            datos = json.load(f)
    except (OSError, ValueError):
        return {"piezas": []}
    if not isinstance(datos, dict):
        return {"piezas": []}
    piezas = datos.get("piezas")
    if not isinstance(piezas, list):
        piezas = []
    return {"piezas": piezas}


def _escribir_crudo(ruta: Path, datos: Dict[str, Any]) -> None:
    """Escribe el archivo de la lista, creando la carpeta si hace falta."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2, sort_keys=True)


# ---------------------------------------------------------------------------
# CANDADO 1: LA PIEZA EXISTE
# ---------------------------------------------------------------------------

def _existe(ruta_pieza: str) -> bool:
    """Candado 1: la pieza tiene que existir en disco."""
    if not ruta_pieza or not str(ruta_pieza).strip():
        return False
    return Path(ruta_pieza).is_file()


# ---------------------------------------------------------------------------
# CANDADO 2: LA PIEZA SE PUEDE LANZAR (trae el arranque propio de Python)
# ---------------------------------------------------------------------------

def se_puede_lanzar(ruta: str) -> bool:
    """Mira si el archivo trae el arranque propio de Python.

    "Arranque propio de Python" quiere decir: el archivo se puede ejecutar
    directamente, o sea que trae el bloque

        if __name__ == "__main__":
            ...

    Se comprueba leyendo el arbol del codigo (ast), no buscando texto a ojo:
    asi no se cuela un comentario que lo mencione ni una cadena que lo imite.

    Devuelve True solo si el archivo existe, es Python legible y trae ese bloque.
    """
    if not _existe(ruta):
        return False
    try:
        fuente = Path(ruta).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    try:
        arbol = ast.parse(fuente)
    except SyntaxError:
        return False

    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.If):
            continue
        prueba = nodo.test
        # Forma 1: if __name__ == "__main__":
        if isinstance(prueba, ast.Compare):
            izquierda = prueba.left
            if isinstance(izquierda, ast.Name) and izquierda.id == "__name__":
                for comparador in prueba.comparators:
                    if isinstance(comparador, ast.Constant) and comparador.value == "__main__":
                        return True
        # Forma 2: if "__main__" == __name__:
        if isinstance(prueba, ast.Compare):
            izquierda = prueba.left
            if isinstance(izquierda, ast.Constant) and izquierda.value == "__main__":
                for comparador in prueba.comparators:
                    if isinstance(comparador, ast.Name) and comparador.id == "__name__":
                        return True
    return False


# ---------------------------------------------------------------------------
# CANDADOS 3 y 4: EL PORQUE Y EL QUIEN VIENEN CON CONTENIDO
# ---------------------------------------------------------------------------

def _texto_lleno(valor: Any) -> bool:
    """True si el valor trae contenido de verdad (no vacio, no solo espacios)."""
    if valor is None:
        return False
    return bool(str(valor).strip())


# ---------------------------------------------------------------------------
# LA PUERTA: puede_entrar
# ---------------------------------------------------------------------------

def puede_entrar(ruta: str, porque: str, quien: str) -> Tuple[bool, str]:
    """Devuelve una pareja (si_se_puede, motivo).

    Rechaza, y SIEMPRE dice el motivo, cuando:
      - la pieza no existe;
      - el porque viene vacio;
      - el quien viene vacio;
      - la pieza no se puede lanzar.

    Es una CUENTA, no un juicio: no entra ninguna IA y la misma pregunta da
    siempre la misma respuesta.
    """
    if not _texto_lleno(ruta):
        return (False, "no entra: la ruta de la pieza viene vacia")
    if not _existe(ruta):
        return (False, "no entra: la pieza no existe en disco: {0}".format(ruta))
    if not _texto_lleno(porque):
        return (False, "no entra: el porque viene vacio")
    if not _texto_lleno(quien):
        return (False, "no entra: el quien viene vacio")
    if not se_puede_lanzar(ruta):
        return (
            False,
            "no entra: la pieza no se puede lanzar, no trae el arranque propio de Python: {0}".format(ruta),
        )
    return (True, "entra: la pieza existe, se puede lanzar, y trae porque y quien")


# ---------------------------------------------------------------------------
# LISTAR
# ---------------------------------------------------------------------------

def listadas(raiz: Optional[str] = None) -> List[Dict[str, Any]]:
    """Devuelve las piezas que estan en la lista blanca.

    Si se pasa raiz, se usa esa raiz para localizar el archivo de la lista
    (salvo que la variable de desvio este puesta, que manda ella).
    """
    base = Path(raiz) if raiz is not None else None
    datos = _leer_crudo(_ruta_lista(base))
    piezas = datos.get("piezas", [])
    # Copia ordenada por nombre de ruta, para que la respuesta sea siempre igual.
    limpias: List[Dict[str, Any]] = []
    for pieza in piezas:
        if isinstance(pieza, dict):
            limpias.append(dict(pieza))
    limpias.sort(key=lambda p: str(p.get("ruta", "")))
    return limpias


# ---------------------------------------------------------------------------
# ANOTAR (solo mete si pasa los candados)
# ---------------------------------------------------------------------------

def anotar(ruta: str, porque: str, quien: str, raiz: Optional[str] = None) -> Tuple[bool, str]:
    """Mete una pieza en la lista blanca SOLO si pasa los candados.

    Devuelve (si_se_pudo, motivo). Si no pasa los candados, NO se escribe nada
    y se dice por que. Si ya estaba anotada, se actualiza el porque y el quien
    (la lista es una cuenta, no un historial).
    """
    se_puede, motivo = puede_entrar(ruta, porque, quien)
    if not se_puede:
        return (False, motivo)

    base = Path(raiz) if raiz is not None else None
    destino = _ruta_lista(base)
    datos = _leer_crudo(destino)
    piezas = [p for p in datos.get("piezas", []) if isinstance(p, dict)]

    ruta_normal = str(Path(ruta).resolve())
    nueva = {
        "ruta": ruta_normal,
        "porque": str(porque).strip(),
        "quien": str(quien).strip(),
    }

    cambiada = False
    for i, pieza in enumerate(piezas):
        if str(pieza.get("ruta", "")) == ruta_normal:
            piezas[i] = nueva
            cambiada = True
            break
    if not cambiada:
        piezas.append(nueva)

    piezas.sort(key=lambda p: str(p.get("ruta", "")))
    _escribir_crudo(destino, {"piezas": piezas})
    return (True, "anotada: {0}".format(ruta_normal))


# ---------------------------------------------------------------------------
# SACAR
# ---------------------------------------------------------------------------

def sacar(nombre: str, raiz: Optional[str] = None) -> Tuple[bool, str]:
    """Saca una pieza de la lista blanca.

    Acepta el nombre tal cual o la ruta completa: se compara por el nombre del
    archivo y por la ruta resuelta. Devuelve (si_se_saco, motivo).
    """
    if not _texto_lleno(nombre):
        return (False, "no se saca: el nombre viene vacio")

    base = Path(raiz) if raiz is not None else None
    destino = _ruta_lista(base)
    datos = _leer_crudo(destino)
    piezas = [p for p in datos.get("piezas", []) if isinstance(p, dict)]

    objetivo = str(nombre).strip()
    objetivo_resuelto = ""
    try:
        objetivo_resuelto = str(Path(objetivo).resolve())
    except OSError:
        objetivo_resuelto = ""

    quedan: List[Dict[str, Any]] = []
    sacadas = 0
    for pieza in piezas:
        ruta_pieza = str(pieza.get("ruta", ""))
        coincide = (
            ruta_pieza == objetivo
            or ruta_pieza == objetivo_resuelto
            or Path(ruta_pieza).name == objetivo
        )
        if coincide:
            sacadas += 1
        else:
            quedan.append(pieza)

    if sacadas == 0:
        return (False, "no se saca: no estaba en la lista: {0}".format(objetivo))

    quedan.sort(key=lambda p: str(p.get("ruta", "")))
    _escribir_crudo(destino, {"piezas": quedan})
    return (True, "sacada: {0} ({1} entrada/s)".format(objetivo, sacadas))


# ---------------------------------------------------------------------------
# REVISAR (las que ya no deberian estar)
# ---------------------------------------------------------------------------

def revisar(raiz: Optional[str] = None) -> List[Dict[str, Any]]:
    """Devuelve las listadas que YA NO deberian estar.

    Una pieza ya no deberia estar cuando perdio su motivo o su forma de
    lanzarse: porque vacio, quien vacio, pieza que ya no existe, o pieza que
    ya no trae el arranque propio de Python.

    Si esta limpia, devuelve lista vacia.
    """
    sospechosas: List[Dict[str, Any]] = []
    for pieza in listadas(raiz):
        ruta = str(pieza.get("ruta", ""))
        porque = pieza.get("porque", "")
        quien = pieza.get("quien", "")
        se_puede, motivo = puede_entrar(ruta, porque, quien)
        if not se_puede:
            copia = dict(pieza)
            copia["motivo"] = motivo
            sospechosas.append(copia)
    sospechosas.sort(key=lambda p: str(p.get("ruta", "")))
    return sospechosas


# ---------------------------------------------------------------------------
# TEXTO (leerla en palabras de Julio)
# ---------------------------------------------------------------------------

def texto(raiz: Optional[str] = None) -> str:
    """Devuelve la lista blanca leida en palabras de Julio.

    Sin adornos y sin IA: lo que hay, contado claro.
    """
    piezas = listadas(raiz)
    lineas: List[str] = []
    lineas.append("LISTA BLANCA — HERRAMIENTAS DE MANO")
    lineas.append("")
    lineas.append(
        "Estas son las piezas que se lanzan a proposito. Por eso el contador de"
    )
    lineas.append(
        "dormidas NO las cuenta. No es una puerta trasera: es una cuenta."
    )
    lineas.append("")
    if not piezas:
        lineas.append("No hay ninguna pieza anotada.")
        return "\n".join(lineas)

    lineas.append("Hay {0} pieza(s) anotada(s):".format(len(piezas)))
    lineas.append("")
    for i, pieza in enumerate(piezas, start=1):
        lineas.append("{0}. {1}".format(i, pieza.get("ruta", "")))
        lineas.append("   porque: {0}".format(pieza.get("porque", "")))
        lineas.append("   quien : {0}".format(pieza.get("quien", "")))
        lineas.append("")

    sospechosas = revisar(raiz)
    if sospechosas:
        lineas.append("OJO: {0} pieza(s) ya no deberian estar aqui:".format(len(sospechosas)))
        for pieza in sospechosas:
            lineas.append("   - {0} ({1})".format(pieza.get("ruta", ""), pieza.get("motivo", "")))
    else:
        lineas.append("La lista esta limpia: todas siguen teniendo motivo y forma de lanzarse.")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# ARRANQUE PROPIO DE PYTHON
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(texto())
