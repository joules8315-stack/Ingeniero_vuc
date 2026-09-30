# -*- coding: utf-8 -*-
"""vigias/test_vigia_solo_frena_la_huerfana_recien_nacida.py — VIGIA QUE NACE ROJO.

Mide el arreglo de la ronda SIGUIENTE sobre arnes/candado_nace_enganchada.py:

  a) los nombres que devuelve la lista de huerfanas traen su terminacion .py;
  b) existe recien_nacidas(raiz, dias=2), que distingue por programa (mirando la
     historia guardada del proyecto) las piezas huerfanas NUEVAS de las VIEJAS;
  c) la funcion que dice si se puede cerrar frena SOLO por las recien nacidas y
     avisa de las viejas con una frase que EMPIEZA por 'AVISO:'.

Promesa de sabotaje: cuando el arreglo entre, quien revise lo deshace, corre esta
prueba y comprueba que los casos 1, 2, 3 y 4 VUELVEN A ROJO.

Sin IA, sin red, sin lanzar procesos. Solo se escribe dentro de la carpeta temporal
que da pytest. Los casos 3 y 4 solo LEEN la carpeta de verdad del proyecto.
"""
import os
import sys


# Ruta de este archivo de prueba.
_AQUI = os.path.dirname(os.path.abspath(__file__))

# La carpeta que esta un nivel arriba de la carpeta vigias: la casa de verdad.
_RAIZ_DE_LA_CASA = os.path.dirname(_AQUI)

# La carpeta arnes, hermana de vigias.
_ARNES = os.path.join(_RAIZ_DE_LA_CASA, "arnes")


def _preparar_arranque():
    """Mete en la ruta de busqueda la casa y la carpeta arnes, sin duplicar."""
    for ruta in (_RAIZ_DE_LA_CASA, _ARNES):
        if ruta not in sys.path:
            sys.path.insert(0, ruta)


def _importar_candado():
    """Importa la pieza DENTRO del caso, nunca arriba del archivo."""
    _preparar_arranque()
    import arnes.candado_nace_enganchada as candado
    return candado


def _carpeta_de_mentira(tmp_path):
    """Crea una carpeta temporal con una carpeta arnes dentro y devuelve su raiz."""
    raiz = tmp_path / "casa_de_mentira"
    (raiz / "arnes").mkdir(parents=True, exist_ok=True)
    return str(raiz)


def _escribir_pieza(raiz, nombre_relativo, contenido=""):
    """Escribe una pieza de mentira dentro de la carpeta temporal."""
    ruta = os.path.join(raiz, nombre_relativo)
    carpeta = os.path.dirname(ruta)
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return ruta


def _nombre_de_una_huerfana(candado, raiz):
    """Devuelve el primer nombre de la lista de huerfanas, o None si esta vacia."""
    lista = candado.huerfanas(raiz)
    if not lista:
        return None
    return lista[0]


# ---------------------------------------------------------------------------
# CASO 1 — LA FUNCION NUEVA EXISTE. Nace rojo: hoy no existe.
# ---------------------------------------------------------------------------
def test_caso_1_la_funcion_nueva_existe(tmp_path):
    candado = _importar_candado()
    assert hasattr(candado, "recien_nacidas"), (
        "Falta recien_nacidas(raiz, dias=2) en arnes/candado_nace_enganchada.py: "
        "sin ella no se puede distinguir una pieza que NACE huerfana de una vieja, "
        "y el candado frena de mas hasta dejar la casa sin poder cerrar."
    )
    assert callable(candado.recien_nacidas), (
        "recien_nacidas existe pero no se puede llamar: tiene que ser una funcion "
        "que reciba la raiz y devuelva la lista de huerfanas NUEVAS."
    )
    raiz = _carpeta_de_mentira(tmp_path)
    resultado = candado.recien_nacidas(raiz)
    assert isinstance(resultado, list), (
        "recien_nacidas tiene que devolver una lista, aunque este vacia."
    )


# ---------------------------------------------------------------------------
# CASO 2 — LOS NOMBRES TRAEN SU TERMINACION. Nace rojo: hoy no acaba en .py.
# ---------------------------------------------------------------------------
def test_caso_2_los_nombres_traen_su_terminacion(tmp_path):
    candado = _importar_candado()
    raiz = _carpeta_de_mentira(tmp_path)
    _escribir_pieza(
        raiz,
        os.path.join("arnes", "pieza_que_nadie_llama.py"),
        "# pieza de mentira que nadie llama\n",
    )
    nombre = _nombre_de_una_huerfana(candado, raiz)
    assert nombre is not None, (
        "La lista de huerfanas vino vacia con una pieza que nadie llama: "
        "la prueba no puede medir la terminacion."
    )
    assert nombre.endswith(".py"), (
        "El nombre de la huerfana tiene que ACABAR en .py para que se sepa de que "
        "archivo se habla; se recibio: %r" % (nombre,)
    )


# ---------------------------------------------------------------------------
# CASO 3 — LA CASA DE VERDAD SE PUEDE CERRAR. Nace rojo: hoy dice que no.
# ---------------------------------------------------------------------------
def test_caso_3_la_casa_de_verdad_se_puede_cerrar():
    candado = _importar_candado()
    se_puede, motivo = candado.se_puede_cerrar(_RAIZ_DE_LA_CASA)
    assert se_puede is True, (
        "La casa de verdad NO puede cerrar porque el candado frena tambien por "
        "piezas VIEJAS que ya estaban huerfanas desde antes. Un candado que bloquea "
        "el cierre entero obliga a apagarlo, y eso ya esta apuntado en esta casa "
        "como un fallo: un candado sin salida honrada empuja a saltarselo. "
        "Motivo devuelto: %r" % (motivo,)
    )


# ---------------------------------------------------------------------------
# CASO 4 — Y AUN ASI AVISA DE LAS VIEJAS. Nace rojo: hoy no hay frase AVISO:.
# ---------------------------------------------------------------------------
def test_caso_4_y_aun_asi_avisa_de_las_viejas():
    candado = _importar_candado()
    se_puede, motivo = candado.se_puede_cerrar(_RAIZ_DE_LA_CASA)
    texto = motivo if isinstance(motivo, str) else str(motivo)
    assert "AVISO:" in texto, (
        "El motivo tiene que traer una frase que EMPIECE por 'AVISO:' para avisar "
        "de las piezas viejas sin frenar el cierre; se recibio: %r" % (texto,)
    )
    assert "huerfana" in texto.lower(), (
        "La frase de AVISO: tiene que hablar de piezas huerfanas; se recibio: %r"
        % (texto,)
    )


# ---------------------------------------------------------------------------
# CASO 5 — NO REVIENTA. Nace rojo porque falta la funcion; luego queda verde.
# ---------------------------------------------------------------------------
def test_caso_5_no_revienta(tmp_path):
    candado = _importar_candado()
    inexistente = os.path.join(str(tmp_path), "no_existe_esta_carpeta")

    for raiz in (inexistente, "", None):
        lista = candado.huerfanas(raiz)
        assert isinstance(lista, list), (
            "huerfanas tiene que devolver una lista aunque la raiz sea %r" % (raiz,)
        )

    for raiz in (inexistente, "", None):
        nuevas = candado.recien_nacidas(raiz)
        assert isinstance(nuevas, list), (
            "recien_nacidas tiene que devolver una lista aunque la raiz sea %r"
            % (raiz,)
        )

    for raiz in (inexistente, "", None):
        se_puede, motivo = candado.se_puede_cerrar(raiz)
        assert se_puede is True, (
            "Ante la duda NO se bloquea: con raiz %r tiene que contestar que SI "
            "se puede cerrar; motivo: %r" % (raiz, motivo)
        )
