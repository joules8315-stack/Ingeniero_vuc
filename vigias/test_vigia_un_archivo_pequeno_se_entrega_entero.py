"""Vigia: un archivo pequeno se entrega entero.

Vigila la funcion NUEVA cerebro/router.py::entregar_enteros_los_cortos.

Que comprueba:
  1. Un archivo corto (<= 600 renglones) que aparece en un pedazo se sustituye
     por UN SOLO pedazo con el archivo ENTERO en 'texto', desde=1 y
     hasta=numero de renglones.
  2. Un archivo largo (> 600 renglones) NO se toca: el pedazo se deja igual.
  3. Si el mismo archivo corto aparece en dos pedazos, solo se entrega UNA vez.
  4. Si el archivo no se puede leer, el pedazo se deja igual.

Los archivos de mentira se montan en una carpeta temporal. NUNCA se toca
ninguna pieza del negocio.

Motivo: se han perdido tres rondas pagadas porque al obrero le llegan trozos
sueltos de archivos cortos y contesta que no encuentra lo que tiene que cambiar.
"""

import os
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)




LIMITE = 600


def _escribir_archivo(ruta, numero_de_renglones):
    """Escribe un archivo de mentira con exactamente N renglones."""
    with open(ruta, "w", encoding="utf-8") as f:
        for i in range(1, numero_de_renglones + 1):
            f.write("renglon %d\n" % i)


def _contar_renglones(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return len(f.readlines())


def _pedazo(pieza, abs_, desde, hasta, texto):
    return {
        "pieza": pieza,
        "abs": abs_,
        "desde": desde,
        "hasta": hasta,
        "texto": texto,
    }


def test_un_archivo_corto_se_entrega_entero():
    """Un archivo de ~100 renglones se sustituye por el archivo ENTERO."""
    with tempfile.TemporaryDirectory() as tmp:
        corto = os.path.join(tmp, "corto.py")
        _escribir_archivo(corto, 100)

        pedazos = [_pedazo("corto.py", corto, 10, 20, "trozo suelto")]
        codigo = [{"id": "corto.py", "abs": corto}]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        assert isinstance(salida, list), "debe devolver una lista"
        assert len(salida) == 1, "un solo pedazo de entrada -> un solo pedazo de salida"

        p = salida[0]
        assert p["abs"] == corto, "el pedazo debe apuntar al mismo archivo"
        assert p["desde"] == 1, "desde debe valer 1"
        assert p["hasta"] == 100, "hasta debe valer el numero de renglones"

        esperado = open(corto, "r", encoding="utf-8").read()
        assert p["texto"] == esperado, "el texto debe ser el archivo ENTERO"
        assert "trozo suelto" not in p["texto"], "no debe quedar el trozo viejo"


def test_un_archivo_largo_se_deja_igual():
    """Un archivo de mas de 600 renglones NO se toca."""
    with tempfile.TemporaryDirectory() as tmp:
        largo = os.path.join(tmp, "largo.py")
        _escribir_archivo(largo, LIMITE + 50)

        original = _pedazo("largo.py", largo, 10, 20, "trozo suelto")
        pedazos = [dict(original)]
        codigo = [{"id": "largo.py", "abs": largo}]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        assert len(salida) == 1, "un pedazo de un archivo largo sigue siendo un pedazo"
        p = salida[0]
        assert p["desde"] == original["desde"], "desde no debe cambiar"
        assert p["hasta"] == original["hasta"], "hasta no debe cambiar"
        assert p["texto"] == original["texto"], "el texto no debe cambiar"


def test_el_mismo_archivo_corto_solo_se_entrega_una_vez():
    """Si el mismo archivo corto aparece en dos pedazos, solo se entrega una vez."""
    with tempfile.TemporaryDirectory() as tmp:
        corto = os.path.join(tmp, "corto.py")
        _escribir_archivo(corto, 80)

        pedazos = [
            _pedazo("corto.py", corto, 1, 10, "trozo A"),
            _pedazo("corto.py", corto, 20, 30, "trozo B"),
        ]
        codigo = [{"id": "corto.py", "abs": corto}]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        entregados = [p for p in salida if p["abs"] == corto and p["desde"] == 1]
        assert len(entregados) == 1, "el archivo corto debe entregarse UNA sola vez"
        assert entregados[0]["hasta"] == 80, "hasta debe valer el numero de renglones"


def test_un_archivo_que_no_se_puede_leer_se_deja_igual():
    """Si el archivo no existe o no se puede leer, el pedazo se deja igual."""
    with tempfile.TemporaryDirectory() as tmp:
        fantasma = os.path.join(tmp, "no_existe.py")

        original = _pedazo("no_existe.py", fantasma, 5, 15, "trozo suelto")
        pedazos = [dict(original)]
        codigo = [{"id": "no_existe.py", "abs": fantasma}]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        assert len(salida) == 1, "un pedazo ilegible sigue siendo un pedazo"
        p = salida[0]
        assert p["desde"] == original["desde"], "desde no debe cambiar"
        assert p["hasta"] == original["hasta"], "hasta no debe cambiar"
        assert p["texto"] == original["texto"], "el texto no debe cambiar"


def test_mezcla_de_corto_y_largo():
    """Con un corto y un largo a la vez, cada uno recibe su trato."""
    with tempfile.TemporaryDirectory() as tmp:
        corto = os.path.join(tmp, "corto.py")
        largo = os.path.join(tmp, "largo.py")
        _escribir_archivo(corto, 100)
        _escribir_archivo(largo, LIMITE + 1)

        pedazos = [
            _pedazo("corto.py", corto, 3, 9, "trozo corto"),
            _pedazo("largo.py", largo, 3, 9, "trozo largo"),
        ]
        codigo = [
            {"id": "corto.py", "abs": corto},
            {"id": "largo.py", "abs": largo},
        ]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        por_abs = {}
        for p in salida:
            por_abs.setdefault(p["abs"], []).append(p)

        assert len(por_abs[corto]) == 1, "el corto se entrega una vez"
        assert por_abs[corto][0]["desde"] == 1
        assert por_abs[corto][0]["hasta"] == 100

        assert len(por_abs[largo]) == 1, "el largo se deja igual"
        assert por_abs[largo][0]["desde"] == 3
        assert por_abs[largo][0]["hasta"] == 9
        assert por_abs[largo][0]["texto"] == "trozo largo"


def test_el_limite_exacto_de_600_se_entrega_entero():
    """Un archivo de exactamente 600 renglones SI se entrega entero."""
    with tempfile.TemporaryDirectory() as tmp:
        justo = os.path.join(tmp, "justo.py")
        _escribir_archivo(justo, LIMITE)

        pedazos = [_pedazo("justo.py", justo, 1, 5, "trozo suelto")]
        codigo = [{"id": "justo.py", "abs": justo}]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        assert len(salida) == 1
        p = salida[0]
        assert p["desde"] == 1
        assert p["hasta"] == LIMITE
        assert p["texto"] == open(justo, "r", encoding="utf-8").read()


def test_el_limite_mas_uno_se_deja_igual():
    """Un archivo de 601 renglones NO se entrega entero."""
    with tempfile.TemporaryDirectory() as tmp:
        pasado = os.path.join(tmp, "pasado.py")
        _escribir_archivo(pasado, LIMITE + 1)

        original = _pedazo("pasado.py", pasado, 1, 5, "trozo suelto")
        pedazos = [dict(original)]
        codigo = [{"id": "pasado.py", "abs": pasado}]

        salida = entregar_enteros_los_cortos(pedazos, codigo)

        assert len(salida) == 1
        p = salida[0]
        assert p["desde"] == original["desde"]
        assert p["hasta"] == original["hasta"]
        assert p["texto"] == original["texto"]


if __name__ == "__main__":
    test_un_archivo_corto_se_entrega_entero()
    test_un_archivo_largo_se_deja_igual()
    test_el_mismo_archivo_corto_solo_se_entrega_una_vez()
    test_un_archivo_que_no_se_puede_leer_se_deja_igual()
    test_mezcla_de_corto_y_largo()
    test_el_limite_exacto_de_600_se_entrega_entero()
    test_el_limite_mas_uno_se_deja_igual()
    print("vigia un_archivo_pequeno_se_entrega_entero: OK")
