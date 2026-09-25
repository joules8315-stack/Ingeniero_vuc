import json
import re
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


def _leer_entrada():
    datos = sys.stdin.read()
    if not datos:
        return ""
    try:
        cargado = json.loads(datos)
    except Exception:
        return datos
    if isinstance(cargado, dict):
        for clave in ("orden", "texto", "comando", "cmd", "command"):
            if clave in cargado and isinstance(cargado[clave], str):
                return cargado[clave]
        return datos
    if isinstance(cargado, str):
        return cargado
    return datos


def _autorizado():
    # Fallo del 2026-09-25: se adivinaba el nombre de la funcion en vez de mirarlo en
    # arnes/autorizacion.py. La prueba que lo destapa es
    # test_vigia_el_candado_respeta_la_llave_de_julio.
    try:
        sys.path.insert(0, str(RAIZ))
        from arnes import autorizacion  # type: ignore
    except Exception:
        return False
    try:
        if autorizacion.autorizada():
            return True
    except Exception:
        return False
    return False


def _archivos_py(texto):
    return re.findall(r"[A-Za-z0-9_./\\-]+\.py", texto)


def _trozos_codigo(texto):
    """Saca los trozos que parecen codigo de un texto.

    FRENO FALSO (2026-09-25, el mismo dia que se creo): antes bastaba un
    parentesis suelto o un signo de igualdad suelto para tomar un trozo por
    codigo, asi que una frase normal en espanol que menciona un archivo entre
    parentesis ya se tomaba por codigo y frenaba una orden buena.

    Por que se afino: un parentesis o una igualdad no son senales de que
    empiece una instruccion; aparecen en cualquier frase. Se quitaron esas dos
    senales y ahora un trozo cuenta como codigo SOLO si empieza por una palabra
    reservada del lenguaje que abre una instruccion, o si termina con el signo
    de dos puntos.

    NO VOLVER A ENSANCHAR: no anadir senales sueltas como parentesis, igualdad,
    comas ni comillas; eso vuelve a frenar ordenes buenas.
    """
    trozos = []
    for linea in texto.splitlines():
        limpia = linea.strip()
        if not limpia:
            continue
        if limpia.endswith(":"):
            trozos.append(limpia)
            continue
        primera = limpia.split()[0]
        if primera in ("if", "elif", "else", "def", "class", "for", "while", "return", "with", "import", "from", "try", "except", "finally", "raise", "yield", "assert", "pass", "break", "continue", "del", "global", "nonlocal", "lambda", "async", "await"):
            trozos.append(limpia)
    return trozos


def _mensaje_error():
    return (
        "El ancla tiene que ser UN renglon exacto y unico.\n"
        "Copia un solo renglon del archivo, tal cual aparece, y que ese renglon "
        "aparezca UNA sola vez en el archivo.\n"
        "Para comprobarlo, abre la terminal en la carpeta del proyecto y escribe:\n"
        "  findstr /n /c:\"el renglon que quieres usar\" nombre_del_archivo.py\n"
        "Si sale mas de un numero de linea, ese renglon no sirve: busca otro que salga una sola vez.\n"
    )


def main():
    texto = _leer_entrada()
    if "ingeniero.py equipo" not in texto:
        return 0
    if _autorizado():
        return 0
    archivos = _archivos_py(texto)
    trozos = _trozos_codigo(texto)
    for trozo in trozos:
        if "\n" in trozo:
            sys.stderr.write(_mensaje_error())
            return 2
        encontrado = False
        for nombre in archivos:
            ruta = Path(nombre)
            if not ruta.is_absolute():
                ruta = RAIZ / nombre
            try:
                contenido = ruta.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if contenido.count(trozo) == 1:
                encontrado = True
                break
        if not encontrado:
            sys.stderr.write(_mensaje_error())
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
