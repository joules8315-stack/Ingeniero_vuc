# -*- coding: utf-8 -*-
"""VIGIA — renovar el permiso no puede aflojar la OPCION C de Julio.

Julio eligio (2026-07-16) la opcion de MENOR exposicion: nada de larga vida guardado. Solo el
permiso de ~1 hora. Nada de llave de renovacion, que no caduca y permite tomar la cuenta.

El 2026-08-24 Julio pidio que se le renovara el permiso sin tener que pegar el bloque a mano.
Se hizo (`arnes/renovar_permiso_pruebas.py`), y esta vigia existe para que esa comodidad NO se
convierta en el agujero que la opcion C queria cerrar:

  · que NUNCA guarde la clave ni una llave de renovacion (solo el permiso de una hora);
  · que NUNCA imprima la clave ni el permiso, ni siquiera un trozo;
  · que compruebe que el permiso ABRE la puerta, en vez de darlo por bueno solo por guardarlo;
  · que a Julio no le llegue un error crudo: todo lo que puede fallar va envuelto.
"""
import ast
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIEZA = os.path.join(AQUI, "arnes", "renovar_permiso_pruebas.py")

CODIGO = open(PIEZA, encoding="utf-8", errors="ignore").read()
ARBOL = ast.parse(CODIGO)


def _lo_que_guarda():
    """Los nombres de variable que la pieza llega a GUARDAR en el equipo."""
    fuera = []
    for n in ast.walk(ARBOL):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "guardar" and n.args:
            a = n.args[0]
            fuera.append(a.value if isinstance(a, ast.Constant) else "?")
    return fuera


def test_solo_guarda_el_permiso_de_una_hora():
    guarda = _lo_que_guarda()
    assert guarda, "no guarda nada: entonces no renueva nada"
    for nombre in guarda:
        assert nombre == "FOTO_INFORME_TEST_BEARER", \
            "guarda algo que NO es el permiso de una hora: %r (opcion C: nada de larga vida)" % nombre


def test_nunca_guarda_la_clave_ni_la_llave_de_renovacion():
    for prohibido in ("FOTO_INFORME_TEST_PASSWORD", "FOTO_INFORME_TEST_REFRESH"):
        assert prohibido not in _lo_que_guarda(), \
            "esta guardando %s: eso es justo lo que la opcion C prohibe" % prohibido
    assert "refresh_token" not in CODIGO, \
        "toca la llave de renovacion: no caduca y permite tomar la cuenta de Julio"


def test_no_enseña_la_clave_ni_el_permiso():
    """Ni entera ni un trozo: un permiso a medias en un registro sigue siendo un permiso."""
    for n in ast.walk(ARBOL):
        if not (isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print"):
            continue
        dicho = ast.dump(n)
        for secreto in ("clave", "token", "correo"):
            assert "id='%s'" % secreto not in dicho, \
                "imprime %s: eso acaba en un registro o en la pantalla" % secreto


def test_comprueba_que_el_permiso_abre_la_puerta():
    """Guardar no es servir. Vigia verde NO es prueba (ley 3 de Julio)."""
    assert "Authorization" in CODIGO and "sirve" in CODIGO, \
        "da por bueno el permiso sin comprobar que de verdad abre"


def test_a_julio_no_le_llega_un_error_crudo():
    llamadas_de_red = sum(1 for n in ast.walk(ARBOL)
                          if isinstance(n, ast.Call) and "urlopen" in ast.dump(n.func))
    protegidas = sum(1 for n in ast.walk(ARBOL) if isinstance(n, ast.Try)
                     and any("urlopen" in ast.dump(h) for h in n.body))
    assert protegidas >= llamadas_de_red, \
        "hay llamadas al programa sin envolver: un fallo de red le saltaria a Julio en la cara"
