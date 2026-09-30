"""Vigia de la puerta del plan.

Esta prueba NACE ROJA A PROPOSITO: la pieza que vigila, arnes/puerta_del_plan.py,
se escribe en la ronda SIGUIENTE. Aqui solo se entrega la prueba.

Regla dura de montaje: la importacion de la pieza va DENTRO de cada caso, nunca
arriba del archivo. Si va arriba y la pieza no existe, el archivo entero revienta
al recogerlo y deja ciega a toda la bateria. Cada caso falla con una afirmacion
(assert), nunca con un reventon.

Sin IA, sin red, sin lanzar procesos. Todo lo que se escribe va a la carpeta
temporal que pytest da a cada caso.
"""

import os
import sys

import pytest


# ---------------------------------------------------------------------------
# Montaje de rutas: la carpeta que esta un nivel arriba de vigias y la carpeta
# arnes, para que la pieza se pueda importar cuando exista.
# ---------------------------------------------------------------------------

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
_ARNES = os.path.join(_RAIZ, "arnes")

for _ruta in (_RAIZ, _ARNES):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# ---------------------------------------------------------------------------
# Utilidades de la prueba
# ---------------------------------------------------------------------------

_ROTULOS = (
    "QUE SE REPARA",
    "COMO SE REPARA",
    "DONDE SE REPARA",
    "POR QUE SE REPARA",
)


def _importar_pieza():
    """Importa arnes/puerta_del_plan.py DENTRO del caso.

    Si la pieza todavia no existe, falla con una afirmacion (rojo por
    afirmacion, nunca por reventon).
    """
    try:
        import puerta_del_plan  # noqa: F401
    except Exception as exc:  # pragma: no cover - camino rojo esperado hoy
        pytest.fail(
            "la pieza arnes/puerta_del_plan.py todavia no existe: "
            "esta prueba nace roja a proposito (" + repr(exc) + ")"
        )
    return puerta_del_plan


def _plan_de_mentira(rotulos_con_texto, rotulos_vacios=()):
    """Arma un texto de plan juntando renglones de una lista.

    rotulos_con_texto: iterable de rotulos que llevan texto detras.
    rotulos_vacios: iterable de rotulos que llevan los dos puntos y nada detras.
    """
    renglones = []
    for rotulo in _ROTULOS:
        if rotulo in rotulos_vacios:
            renglones.append(rotulo + ":")
        elif rotulo in rotulos_con_texto:
            renglones.append(rotulo + ": se repara el trozo que falla en el arnes")
    return "\n".join(renglones)


def _plan_completo():
    return _plan_de_mentira(_ROTULOS)


# ---------------------------------------------------------------------------
# Caso 1: la pieza existe y tiene las seis cosas
# ---------------------------------------------------------------------------

def test_la_pieza_existe_y_tiene_las_seis_cosas():
    pieza = _importar_pieza()

    assert hasattr(pieza, "LAS_CUATRO"), (
        "a la pieza le falta LAS_CUATRO"
    )
    assert tuple(pieza.LAS_CUATRO) == _ROTULOS, (
        "LAS_CUATRO no trae los cuatro rotulos exactos en el orden pedido"
    )

    for nombre in (
        "lo_que_falta",
        "numero_del_plan",
        "aprobar",
        "puede_arrancar",
        "puede_cerrar",
        "anotar_resumen",
    ):
        assert hasattr(pieza, nombre), (
            "a la pieza le falta " + nombre
        )
        assert callable(getattr(pieza, nombre)), (
            nombre + " no es algo que se pueda llamar"
        )


# ---------------------------------------------------------------------------
# Caso 2: sin los cuatro no arranca, y dice cual falta
# ---------------------------------------------------------------------------

def test_sin_los_cuatro_no_arranca_y_dice_cual_falta(tmp_path):
    pieza = _importar_pieza()

    plan = _plan_de_mentira(
        ("QUE SE REPARA", "COMO SE REPARA", "POR QUE SE REPARA")
    )

    falta = pieza.lo_que_falta(plan)
    assert isinstance(falta, list), "lo_que_falta debe devolver una lista"
    assert len(falta) == 1, (
        "con tres rotulos puestos debe faltar exactamente uno, no "
        + str(len(falta))
    )
    frase = falta[0]
    assert "DONDE SE REPARA" in frase, (
        "la frase que falta debe hablar de DONDE SE REPARA"
    )
    assert "puerta_del_plan" in frase, (
        "la frase que falta debe nombrar a puerta_del_plan"
    )

    puede, motivo = pieza.puede_arrancar(plan, str(tmp_path))
    assert puede is False, "sin el rotulo de donde se repara no se puede arrancar"
    assert "puerta_del_plan" in str(motivo), (
        "el motivo debe nombrar a puerta_del_plan"
    )


# ---------------------------------------------------------------------------
# Caso 3: un rotulo vacio no cuenta como puesto
# ---------------------------------------------------------------------------

def test_un_rotulo_vacio_no_cuenta_como_puesto():
    pieza = _importar_pieza()

    plan = _plan_de_mentira(
        ("QUE SE REPARA", "COMO SE REPARA", "POR QUE SE REPARA"),
        rotulos_vacios=("DONDE SE REPARA",),
    )

    falta = pieza.lo_que_falta(plan)
    assert isinstance(falta, list), "lo_que_falta debe devolver una lista"
    assert len(falta) == 1, (
        "un rotulo con los dos puntos y nada detras sigue contando como que falta"
    )
    assert "DONDE SE REPARA" in falta[0], (
        "el que falta debe ser DONDE SE REPARA"
    )


# ---------------------------------------------------------------------------
# Caso 4: con los cuatro pero sin aprobacion, no arranca
# ---------------------------------------------------------------------------

def test_con_los_cuatro_pero_sin_aprobacion_no_arranca(tmp_path):
    pieza = _importar_pieza()

    plan = _plan_completo()

    puede, motivo = pieza.puede_arrancar(plan, str(tmp_path))
    assert puede is False, (
        "con los cuatro puestos pero sin aprobacion no se puede arrancar"
    )
    texto_motivo = str(motivo)
    assert "aprob" in texto_motivo.lower(), (
        "el motivo debe decir que falta la aprobacion de Julio"
    )
    assert "puerta_del_plan" in texto_motivo, (
        "el motivo debe nombrar a puerta_del_plan"
    )


# ---------------------------------------------------------------------------
# Caso 5: aprobado arranca, y si se cambia el plan ya no
# ---------------------------------------------------------------------------

def test_aprobado_arranca_y_si_se_cambia_el_plan_ya_no(tmp_path):
    pieza = _importar_pieza()

    plan = _plan_completo()
    raiz = str(tmp_path)

    resultado = pieza.aprobar(plan, raiz)
    assert isinstance(resultado, dict), "aprobar debe devolver un diccionario"
    assert "ok" in resultado, "aprobar debe devolver la clave ok"
    assert "_error" not in resultado, (
        "con los cuatro puestos aprobar no debe devolver _error"
    )

    puede, _motivo = pieza.puede_arrancar(plan, raiz)
    assert puede is True, "un plan aprobado con los cuatro debe poder arrancar"

    plan_cambiado = plan + "\nQUE SE REPARA: se repara otra cosa distinta del arnes"
    puede2, motivo2 = pieza.puede_arrancar(plan_cambiado, raiz)
    assert puede2 is False, (
        "si el plan cambia despues de aprobado ya no se puede arrancar"
    )
    texto_motivo = str(motivo2)
    assert "cambi" in texto_motivo.lower(), (
        "el motivo debe decir que el plan cambio despues de aprobado"
    )
    assert "puerta_del_plan" in texto_motivo, (
        "el motivo debe nombrar a puerta_del_plan"
    )


# ---------------------------------------------------------------------------
# Caso 6: sin resumen no se cierra
# ---------------------------------------------------------------------------

def test_sin_resumen_no_se_cierra(tmp_path):
    pieza = _importar_pieza()

    plan = _plan_completo()
    raiz = str(tmp_path)

    resultado = pieza.aprobar(plan, raiz)
    assert "ok" in resultado, "el plan debe quedar aprobado para este caso"
    numero = resultado["ok"]

    puede, motivo = pieza.puede_cerrar(raiz)
    assert puede is False, (
        "con un plan aprobado y sin resumen apuntado no se puede cerrar"
    )
    assert "puerta_del_plan" in str(motivo), (
        "el motivo debe nombrar a puerta_del_plan"
    )

    apuntado = pieza.anotar_resumen(numero, "resumen de lo que paso", raiz)
    assert apuntado, "anotar_resumen debe devolver que si lo pudo apuntar"

    puede2, _motivo2 = pieza.puede_cerrar(raiz)
    assert puede2 is True, (
        "con el resumen apuntado ya se puede cerrar"
    )


# ---------------------------------------------------------------------------
# Caso 7: no revienta con basura
# ---------------------------------------------------------------------------

def test_no_revienta_con_basura():
    pieza = _importar_pieza()

    basura = ("", None, 7, ["QUE SE REPARA"])

    for cosa in basura:
        falta = pieza.lo_que_falta(cosa)
        assert isinstance(falta, list), (
            "lo_que_falta debe devolver una lista incluso con basura"
        )
        assert len(falta) == 4, (
            "con basura lo_que_falta debe devolver los cuatro"
        )

        numero = pieza.numero_del_plan(cosa)
        assert numero == "", (
            "con basura numero_del_plan debe devolver texto vacio"
        )
