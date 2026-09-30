# -*- coding: utf-8 -*-
"""vigias/test_vigia_la_huerfana_se_empareja_con_su_fecha.py — VIGIA que mide el emparejado
entre la lista de huerfanas (nombres PELADOS) y la historia del proyecto (rutas COMPLETAS).

NACE ROJA A PROPOSITO: el arreglo entra en la ronda SIGUIENTE. Hoy la funcion
emparejar_por_nombre no existe en arnes/candado_nace_enganchada.py, asi que los seis casos
fallan por importacion. En cuanto exista, los seis tienen que quedar verdes.

QUE MIDE: que el candado que cumple la orden de Julio (todo nace enganchado) FRENE de verdad
cuando una pieza huerfana nacio hace poco, y que NO frene por las viejas ni por lo que no se
sabe. Hoy el candado no frena NUNCA porque compara el nombre pelado con la ruta completa, y
parece que funciona: un verde que no prueba nada, que es justo lo que Julio prohibe.

COMO SE MONTA: todos los datos son de mentira y se arman aqui mismo. Las fechas se hacen con
el modulo de fechas de siempre a partir de una fecha fija inventada, NUNCA a partir del dia
de hoy, para que la prueba de siempre el mismo resultado. No se lee ni se escribe ningun
archivo, no hay red, no hay disco, no se lanza ningun proceso, no se llama a ninguna IA.

SABOTAJE: cuando el arreglo entre, quien revise lo deshace, corre la prueba y comprueba que
los casos VUELVEN A ROJO. Sin esa comprobacion, esta vigia no se da por protegida.
"""
import datetime
import os
import sys


# La carpeta de este archivo de prueba (vigias/).
_AQUI = os.path.dirname(os.path.abspath(__file__))

# La carpeta que esta un nivel arriba de vigias/ (la raiz de la casa).
_RAIZ = os.path.dirname(_AQUI)

# La carpeta arnes/ de la casa.
_ARNES = os.path.join(_RAIZ, "arnes")

# Fecha fija inventada: NUNCA el dia de hoy. Todo se mide contra esta.
_FECHA_FIJA = datetime.date(2026, 9, 30)

# El limite: se considera recien nacida la que aparecio en esta fecha o despues.
_LIMITE = datetime.date(2026, 9, 29)

# Fechas de mentira, todas relativas a la fecha fija inventada.
_VIEJA = _FECHA_FIJA - datetime.timedelta(days=30)
_NUEVA = _FECHA_FIJA


def _preparar_ruta_de_busqueda():
    """Mete en la ruta de busqueda la raiz de la casa y la carpeta arnes/, para poder
    importar la pieza DENTRO de cada caso, nunca arriba del archivo."""
    for carpeta in (_RAIZ, _ARNES):
        if carpeta not in sys.path:
            sys.path.insert(0, carpeta)


def _importar_pieza():
    """Importa arnes/candado_nace_enganchada.py DENTRO del caso que lo pida."""
    _preparar_ruta_de_busqueda()
    import candado_nace_enganchada
    return candado_nace_enganchada


def _es_lista(valor):
    """Devuelve verdadero si el valor es una lista (no una tupla, no un texto)."""
    return isinstance(valor, list)


def caso_1_la_funcion_existe():
    """CASO 1: la funcion emparejar_por_nombre existe y se puede llamar.
    Nace rojo: hoy no existe."""
    pieza = _importar_pieza()
    funcion = getattr(pieza, "emparejar_por_nombre", None)
    assert funcion is not None, (
        "No existe emparejar_por_nombre en arnes/candado_nace_enganchada.py. "
        "Sin esa funcion no se puede medir el emparejado y el candado sigue sin frenar nunca."
    )
    assert callable(funcion), (
        "emparejar_por_nombre existe pero no se puede llamar: no es una funcion."
    )


def caso_2_empareja_nombre_pelado_con_ruta_completa():
    """CASO 2: el nombre pelado se empareja con la ruta completa que acaba en ese nombre.
    Nace rojo, y es el caso que mide el fallo: hoy se compara el nombre pelado con la ruta
    completa y NUNCA coinciden, asi que el candado no frena NUNCA y parece que funciona.
    Un verde que no prueba nada es lo que Julio prohibe."""
    pieza = _importar_pieza()
    funcion = getattr(pieza, "emparejar_por_nombre", None)
    assert funcion is not None, (
        "No existe emparejar_por_nombre: por esto el candado no frena NUNCA y parece que "
        "funciona. Un verde que no prueba nada es lo que Julio prohibe."
    )

    nombres = ["puerta_del_plan.py"]
    fechas_por_ruta = {
        "arnes/puerta_del_plan.py": _NUEVA,
    }
    resultado = funcion(nombres, fechas_por_ruta, _LIMITE)

    assert _es_lista(resultado), (
        "emparejar_por_nombre no devolvio una lista: devolvio %r." % (resultado,)
    )
    assert "puerta_del_plan.py" in resultado, (
        "El nombre pelado 'puerta_del_plan.py' NO se emparejo con la ruta completa "
        "'arnes/puerta_del_plan.py' aunque nacio despues del limite. Por esto el candado "
        "no frena NUNCA y parece que funciona: compara el nombre pelado con la ruta "
        "completa y nunca coinciden. Un verde que no prueba nada es lo que Julio prohibe."
    )


def caso_3_lo_viejo_no_cuenta():
    """CASO 3: una pieza que nacio ANTES del limite NO cuenta como recien nacida.
    Nace rojo. Este es el caso que impide volver a frenar por las viejas."""
    pieza = _importar_pieza()
    funcion = getattr(pieza, "emparejar_por_nombre", None)
    assert funcion is not None, (
        "No existe emparejar_por_nombre: no se puede comprobar que lo viejo no cuenta."
    )

    nombres = ["pieza_vieja.py"]
    fechas_por_ruta = {
        "arnes/pieza_vieja.py": _VIEJA,
    }
    resultado = funcion(nombres, fechas_por_ruta, _LIMITE)

    assert _es_lista(resultado), (
        "emparejar_por_nombre no devolvio una lista: devolvio %r." % (resultado,)
    )
    assert resultado == [], (
        "Una pieza que nacio ANTES del limite no puede contar como recien nacida, pero "
        "la lista devuelta trae %r. Si esto pasa, el candado vuelve a frenar por las viejas."
        % (resultado,)
    )


def caso_4_lo_que_no_se_sabe_no_cuenta():
    """CASO 4: si de un nombre no se sabe la fecha, NO es recien nacido.
    Nace rojo. Ante la duda no se frena."""
    pieza = _importar_pieza()
    funcion = getattr(pieza, "emparejar_por_nombre", None)
    assert funcion is not None, (
        "No existe emparejar_por_nombre: no se puede comprobar que lo que no se sabe no cuenta."
    )

    nombres = ["pieza_desconocida.py"]
    fechas_por_ruta = {
        "arnes/otra_pieza.py": _NUEVA,
    }
    resultado = funcion(nombres, fechas_por_ruta, _LIMITE)

    assert _es_lista(resultado), (
        "emparejar_por_nombre no devolvio una lista: devolvio %r." % (resultado,)
    )
    assert resultado == [], (
        "Un nombre que no aparece en ninguna ruta del diccionario no puede contar como "
        "recien nacido, pero la lista devuelta trae %r. Ante la duda no se frena."
        % (resultado,)
    )


def caso_5_si_aparece_en_varias_rutas_manda_la_mas_antigua():
    """CASO 5: si una misma pieza aparece en varias rutas, manda la fecha MAS ANTIGUA,
    porque esa es la de su nacimiento. Nace rojo."""
    pieza = _importar_pieza()
    funcion = getattr(pieza, "emparejar_por_nombre", None)
    assert funcion is not None, (
        "No existe emparejar_por_nombre: no se puede comprobar que manda la fecha mas antigua."
    )

    nombres = ["pieza_repetida.py"]
    fechas_por_ruta = {
        "arnes/pieza_repetida.py": _VIEJA,
        "otra_carpeta/pieza_repetida.py": _NUEVA,
    }
    resultado = funcion(nombres, fechas_por_ruta, _LIMITE)

    assert _es_lista(resultado), (
        "emparejar_por_nombre no devolvio una lista: devolvio %r." % (resultado,)
    )
    assert resultado == [], (
        "Si una pieza aparece en varias rutas, manda la fecha MAS ANTIGUA (su nacimiento), "
        "pero la lista devuelta trae %r. Con la fecha nueva se frenaria por una pieza vieja."
        % (resultado,)
    )


def caso_6_no_revienta_con_basura():
    """CASO 6: con listas vacias, con nada en vez de lista, con un numero, con un diccionario
    de valores que no son fechas y con un limite que no es fecha, devuelve una lista y no
    revienta. Nace rojo porque la funcion no existe."""
    pieza = _importar_pieza()
    funcion = getattr(pieza, "emparejar_por_nombre", None)
    assert funcion is not None, (
        "No existe emparejar_por_nombre: no se puede comprobar que no revienta con basura."
    )

    entradas = [
        ([], {}, _LIMITE),
        (None, {}, _LIMITE),
        (42, {}, _LIMITE),
        (["pieza.py"], {"arnes/pieza.py": "no soy una fecha"}, _LIMITE),
        (["pieza.py"], {"arnes/pieza.py": _NUEVA}, "no soy una fecha"),
        (["pieza.py"], None, None),
    ]

    for nombres, fechas_por_ruta, limite in entradas:
        try:
            resultado = funcion(nombres, fechas_por_ruta, limite)
        except Exception as error:
            raise AssertionError(
                "emparejar_por_nombre reviento con entradas basura "
                "(nombres=%r, fechas=%r, limite=%r): %s"
                % (nombres, fechas_por_ruta, limite, error)
            )
        assert _es_lista(resultado), (
            "Con entradas basura (nombres=%r, fechas=%r, limite=%r) no devolvio una lista: "
            "devolvio %r." % (nombres, fechas_por_ruta, limite, resultado)
        )


def test_caso_1_la_funcion_existe():
    caso_1_la_funcion_existe()


def test_caso_2_empareja_nombre_pelado_con_ruta_completa():
    caso_2_empareja_nombre_pelado_con_ruta_completa()


def test_caso_3_lo_viejo_no_cuenta():
    caso_3_lo_viejo_no_cuenta()


def test_caso_4_lo_que_no_se_sabe_no_cuenta():
    caso_4_lo_que_no_se_sabe_no_cuenta()


def test_caso_5_si_aparece_en_varias_rutas_manda_la_mas_antigua():
    caso_5_si_aparece_en_varias_rutas_manda_la_mas_antigua()


def test_caso_6_no_revienta_con_basura():
    caso_6_no_revienta_con_basura()


def main():
    """Corre los seis casos y dice el resultado. Devuelve 0 si todo verde, 1 si algo rojo."""
    casos = [
        ("1. La funcion existe", caso_1_la_funcion_existe),
        ("2. Empareja nombre pelado con ruta completa", caso_2_empareja_nombre_pelado_con_ruta_completa),
        ("3. Lo viejo no cuenta", caso_3_lo_viejo_no_cuenta),
        ("4. Lo que no se sabe no cuenta", caso_4_lo_que_no_se_sabe_no_cuenta),
        ("5. Si aparece en varias rutas manda la mas antigua", caso_5_si_aparece_en_varias_rutas_manda_la_mas_antigua),
        ("6. No revienta con basura", caso_6_no_revienta_con_basura),
    ]

    fallos = 0
    for titulo, caso in casos:
        try:
            caso()
            print("VERDE  %s" % titulo)
        except AssertionError as error:
            fallos += 1
            print("ROJO   %s" % titulo)
            print("       %s" % error)
        except Exception as error:
            fallos += 1
            print("ROJO   %s" % titulo)
            print("       Fallo por estar mal montada o por error inesperado: %s" % error)

    if fallos:
        print("\n%d caso(s) en ROJO. Esta vigia nace roja a proposito: el arreglo entra en la ronda siguiente." % fallos)
        return 1
    print("\nTodos los casos en VERDE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
