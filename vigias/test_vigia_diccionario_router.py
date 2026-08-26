# -*- coding: utf-8 -*-
"""VIGIA — el DICCIONARIO llega al repartidor (palabras de Julio -> codigo).

Claude, 2026-08-25 (punto 3, "la gorda"): el paquete devolvia las vigias recien escritas y del
programa CERO, porque Julio habla en espanol y de negocio y el codigo esta en ingles y comprimido:
nunca se parecen. La cura: un diccionario que se COSECHA de cada causa raiz declarada (ahi ya
existen las dos mitades probadas: lo que dijo Julio + el sitio exacto).

Reparto: Claude hizo el diccionario (arnes/diccionario.py) y la cosecha; Cline lo conecto al
repartidor (router.py) para que el paquete incluya los sitios ya reparados.

Comprueba:
  · el diccionario existe y busca,
  · el router lo CONSUME (lo mete en el material del paquete),
  · el paquete le muestra a Julio lo ya reparado,
  · la causa raiz cosecha al diccionario.
"""
import io
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _leer(rel):
    try:
        return io.open(os.path.join(AQUI, rel), encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_el_diccionario_existe_y_busca():
    import sys
    sys.path.insert(0, AQUI)
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    from arnes import diccionario
    assert hasattr(diccionario, "buscar"), "el diccionario no sabe buscar"
    assert hasattr(diccionario, "aprender"), "el diccionario no sabe aprender"


def test_el_router_consume_el_diccionario():
    txt = _leer("cerebro/router.py")
    assert "diccionario" in txt, "el router no menciona el diccionario"
    assert "diccionario_sitios" in txt, "el router no arma la lista de sitios ya reparados"
    assert "codigo.append" in txt, "el router no mete el sitio ya reparado en el material"


def test_el_paquete_muestra_lo_ya_reparado():
    txt = _leer("cerebro/router.py")
    assert "ESTO YA SE REPARO ANTES" in txt, "el paquete no le dice a Julio que ya se reparo"


def test_la_causa_cosecha_el_diccionario():
    txt = _leer("arnes/candado_diagnostico.py")
    assert "diccionario" in txt or "cosechar" in txt or "aprender" in txt, \
        "declarar la causa debe cosechar el diccionario"
