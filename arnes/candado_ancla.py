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
    try:
        sys.path.insert(0, str(RAIZ))
        from arnes import autorizacion  # type: ignore
    except Exception:
        return False
    for nombre in ("julio_autorizo", "autorizo_julio", "autorizado", "julio_autoriza"):
        funcion = getattr(autorizacion, nombre, None)
        if callable(funcion):
            try:
                if funcion():
                    return True
            except Exception:
                continue
    return False


def _archivos_py(texto):
    return re.findall(r"[A-Za-z0-9_./\\-]+\.py", texto)


def _trozos_codigo(texto):
    trozos = []
    for linea in texto.splitlines():
        limpia = linea.strip()
        if not limpia:
            continue
        if limpia.endswith(":"):
            trozos.append(limpia)
            continue
        if "=" in limpia:
            trozos.append(limpia)
            continue
        if "(" in limpia or ")" in limpia:
            trozos.append(limpia)
            continue
        primera = limpia.split()[0]
        if primera in ("if", "def", "for", "return", "with", "import"):
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
