import os
import json
from typing import Any, Dict


def _ruta_cuaderno(raiz: str) -> str:
    """Devuelve la ruta completa del archivo de cuaderno dentro del *raiz*.
    Se usa un nombre oculto para evitar colisiones con otros archivos del proyecto.
    """
    return os.path.join(raiz, ".cuaderno_ronda.json")


def _cargar_cuaderno(raiz: str) -> Dict[str, Any]:
    """Carga el cuaderno desde disco.
    Si el archivo no existe o está corrupto, se devuelve un diccionario vacío.
    """
    ruta = _ruta_cuaderno(raiz)
    if not os.path.isfile(ruta):
        return {}
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # En caso de error (p.e. JSON inválido) se ignora y se empieza de cero.
        return {}


def _guardar_cuaderno(raiz: str, datos: Dict[str, Any]) -> None:
    """Guarda el cuaderno en disco de forma atómica.
    Se escribe en un archivo temporal y luego se renombra para evitar corrupciones.
    """
    ruta = _ruta_cuaderno(raiz)
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    os.replace(tmp, ruta)


def _clave(encargo: Any, pieza: Any) -> str:
    """Construye una clave única para el par (encargo, pieza).
    Se convierte a cadena JSON para soportar objetos complejos.
    """
    return json.dumps([encargo, pieza], ensure_ascii=False)


def antes_de_lanzar(encargo: Any, pieza: Any, raiz: str) -> Dict[str, Any]:
    """Devuelve información previa a lanzar la pieza.

    - ``ya_fallo``: ``True`` si previamente se registró un fallo para este
      ``encargo``/``pieza``.
    - ``guia``: texto del motivo del fallo anterior (vía de la guía). Vacío si
      nunca falló.
    - ``codigo``: siempre cadena vacía, cumpliendo la Ley de las Dos Vías.
    """
    datos = _cargar_cuaderno(raiz)
    clave = _clave(encargo, pieza)
    motivo = datos.get(clave, "")
    return {
        "ya_fallo": bool(motivo),
        "guia": motivo,
        "codigo": "",
    }


def despues_de_la_ronda(encargo: Any, pieza: Any, motivo: str, raiz: str) -> bool:
    """Registra el motivo de un fallo después de ejecutar la ronda.

    Si ``motivo`` es una cadena vacía, no se escribe nada y se devuelve ``False``.
    En caso contrario se almacena el motivo y se devuelve ``True``.
    """
    if not motivo:
        return False
    datos = _cargar_cuaderno(raiz)
    clave = _clave(encargo, pieza)
    datos[clave] = motivo
    _guardar_cuaderno(raiz, datos)
    return True
