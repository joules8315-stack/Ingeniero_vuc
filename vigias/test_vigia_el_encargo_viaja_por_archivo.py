import os
import sys

# Arranque: meter en sys.path la carpeta que esta un nivel arriba de vigias,
# para poder importar ingeniero.py y el paquete cerebro.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)


# Texto del encargo con TRES renglones y comillas dobles por dentro.
# El renglon del medio lleva una palabra entre comillas dobles: es justo lo que
# la terminal de Windows se come hoy, asi que la vigia lo mira de frente.
_ENCARGO = (
    'renglon uno sin comillas\n'
    'renglon dos con "palabra" entre comillas dobles\n'
    'renglon tres final\n'
)


def _montar_falso_armar(monkeypatch):
    """Sustituye SOLO cerebro.router.armar por una falsa que apunta el texto.

    Devuelve la lista donde queda apuntado el texto que llego. La falsa
    devuelve un texto cualquiera para que el mando pueda seguir; lo que pase
    despues da igual, porque lo que se vigila es el texto apuntado.
    """
    from cerebro import router as _r

    apuntado = []

    def _armar_falso(proy, tarea):
        apuntado.append(tarea)
        return "paquete de mentira"

    monkeypatch.setattr(_r, "armar", _armar_falso)
    return apuntado


def test_el_encargo_llega_completo_desde_archivo(tmp_path, monkeypatch):
    """Prueba 1 (HOY ROJA): el texto llega COMPLETO desde el archivo.

    Se escribe el encargo en un archivo de la carpeta temporal, se pasa con la
    marca --encargo-archivo y se comprueba que a router.armar le llega
    EXACTAMENTE el contenido del archivo, con sus comillas y sus tres renglones.
    Hoy sale roja porque esa marca no existe: llegaria el nombre de la marca y
    la ruta, no el texto.
    """
    import ingeniero

    ruta_encargo = tmp_path / "encargo.txt"
    ruta_encargo.write_text(_ENCARGO, encoding="utf-8")

    apuntado = _montar_falso_armar(monkeypatch)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingeniero.py",
            "equipo",
            "proyecto_de_mentira",
            "--encargo-archivo",
            str(ruta_encargo),
        ],
    )

    try:
        ingeniero.main()
    except Exception:
        # Si el mando revienta DESPUES de apuntar el texto, da igual: lo que se
        # vigila es el texto que llego, no que el mando termine.
        pass

    assert apuntado, "router.armar no fue llamado: el texto no llego a ninguna parte"
    assert apuntado[0] == _ENCARGO, (
        "el texto del encargo no llego completo desde el archivo; "
        "llego: %r" % (apuntado[0],)
    )


def test_el_encargo_por_argumentos_sigue_funcionando(tmp_path, monkeypatch):
    """Prueba 2 (VERDE HOY): lo de siempre no se rompe.

    Mismo montaje, pero el encargo va escrito en los argumentos como se hace
    hoy. El texto que llega a router.armar tiene que ser ese mismo texto.
    """
    import ingeniero

    apuntado = _montar_falso_armar(monkeypatch)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ingeniero.py",
            "equipo",
            "proyecto_de_mentira",
            "renglon uno sin comillas",
            "renglon dos con",
            "palabra",
            "entre comillas dobles",
            "renglon tres final",
        ],
    )

    try:
        ingeniero.main()
    except Exception:
        pass

    assert apuntado, "router.armar no fue llamado: el texto no llego a ninguna parte"
    assert apuntado[0] == (
        "renglon uno sin comillas renglon dos con palabra entre comillas dobles "
        "renglon tres final"
    ), "el encargo pasado por argumentos no llego como antes; llego: %r" % (apuntado[0],)
