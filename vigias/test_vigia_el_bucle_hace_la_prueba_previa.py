# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_bucle_hace_la_prueba_previa.py

VIGIA: antes de lanzar una orden al equipo, el bucle corre la prueba previa y, si el
codigo no llega, APARTA la orden con el motivo en vez de gastar una llamada.

POR QUE (medido el 2026-10-01): 12 de las 58 ordenes abiertas con pieza .py no nombran
el archivo de su pieza, y a esas el paquete les trae el codigo solo en 1 de 3. Cada una
se manda a una IA de pago sin que nadie compruebe antes por programa que el codigo llega.
Es gasto sin resultado posible.

COMO SE PRUEBA: ejecutando de verdad la funcion del bucle con carpetas temporales, sin
tocar el estado real. No se mira el texto del codigo.

NACE ROJA: hoy la pieza que hace la prueba previa no existe, asi que el import de abajo
falla y la prueba queda roja por ese import. Cuando la reparacion este hecha, la pieza
existira y la prueba pasara.
"""
import os
import sys
import json
import tempfile

import pytest

# La raiz del proyecto es la carpeta que contiene a 'vigias'.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

# ---------------------------------------------------------------------------
# LA PIEZA QUE SE ESPERA. Si aun no existe, el import falla y la prueba nace ROJA
# por el import justo de esa pieza, que es lo que pide la tarea.
# ---------------------------------------------------------------------------
try:
    from cuerpo.bucle import lanzar_orden_al_equipo  # noqa: F401
except Exception as _e_import:
    # Se deja constancia del motivo real del rojo y se relanza para que pytest lo vea.
    raise ImportError(
        "Falta la pieza del bucle que hace la prueba previa antes de lanzar la orden: "
        "cuerpo/bucle.py::lanzar_orden_al_equipo. "
        "Detalle: %r" % (_e_import,)
    )


# ---------------------------------------------------------------------------
# AYUDAS DE PRUEBA: todo en carpetas temporales, nada del estado real.
# ---------------------------------------------------------------------------
def _escribir_pieza(carpeta, nombre, contenido):
    """Deja una pieza .py en el disco de prueba."""
    ruta = os.path.join(carpeta, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def _orden_de_prueba(carpeta, pieza_nombrada):
    """Una orden tal y como la abre el bucle: con su pieza .py declarada."""
    return {
        "id": "orden-de-prueba-001",
        "proyecto": "proyecto-de-prueba",
        "pieza": pieza_nombrada,
        "carpeta": carpeta,
        "texto": "repara lo que haga falta en la pieza declarada",
    }


def _contar_llamadas(registro):
    """Cuantas veces se ha llamado de verdad a la IA de pago."""
    return len(registro.get("llamadas", []))


# ---------------------------------------------------------------------------
# LA PRUEBA QUE MANDA
# ---------------------------------------------------------------------------
def test_el_bucle_hace_la_prueba_previa_y_aparta_si_el_codigo_no_llega():
    """Antes de lanzar la orden, el bucle corre la prueba previa.

    Si el codigo de la pieza NO llega, la orden se APARTA con el motivo y NO se gasta
    ninguna llamada a la IA de pago.
    """
    with tempfile.TemporaryDirectory() as tmp:
        # La pieza declarada por la orden NO existe en el disco: el codigo no llega.
        pieza_que_no_llega = os.path.join(tmp, "pieza_que_no_existe.py")
        assert not os.path.exists(pieza_que_no_llega)

        orden = _orden_de_prueba(tmp, pieza_que_no_llega)

        # Registro de llamadas: si el bucle llama a la IA, aqui queda apuntado.
        registro = {"llamadas": []}

        def ia_de_pago(orden_recibida):
            registro["llamadas"].append(orden_recibida)
            return {"ok": True, "texto": "respuesta de mentira"}

        resultado = lanzar_orden_al_equipo(
            orden,
            enviar=ia_de_pago,
            carpeta_trabajo=tmp,
        )

        # 1) La orden quedo APARTADA, no lanzada.
        assert resultado.get("estado") == "apartada", (
            "La orden debio quedar apartada cuando el codigo no llega; "
            "quedo en estado %r" % (resultado.get("estado"),)
        )

        # 2) Lleva el MOTIVO escrito, no se aparta en silencio.
        motivo = resultado.get("motivo") or ""
        assert motivo.strip(), (
            "La orden apartada tiene que llevar el motivo por el que se aparta; "
            "vino vacio"
        )

        # 3) NO se gasto ninguna llamada a la IA de pago.
        assert _contar_llamadas(registro) == 0, (
            "Se gasto una llamada a la IA de pago con una orden cuyo codigo no llega; "
            "se hicieron %d llamadas" % _contar_llamadas(registro)
        )

        # 4) La prueba previa quedo registrada en el resultado.
        assert resultado.get("prueba_previa") is not None, (
            "El resultado tiene que dejar constancia de que se corrio la prueba previa"
        )


def test_el_bucle_lanza_cuando_el_codigo_si_llega():
    """Contraprueba: si el codigo SI llega, la orden se lanza de verdad.

    Sin esta contraprueba, un bucle que apartara TODO pasaria la prueba anterior sin
    estar bien: hay que demostrar que solo aparta cuando toca.
    """
    with tempfile.TemporaryDirectory() as tmp:
        pieza_que_si_llega = _escribir_pieza(
            tmp,
            "pieza_que_si_llega.py",
            "# -*- coding: utf-8 -*-\nVALOR = 1\n",
        )
        assert os.path.exists(pieza_que_si_llega)

        orden = _orden_de_prueba(tmp, pieza_que_si_llega)
        registro = {"llamadas": []}

        def ia_de_pago(orden_recibida):
            registro["llamadas"].append(orden_recibida)
            return {"ok": True, "texto": "respuesta de mentira"}

        resultado = lanzar_orden_al_equipo(
            orden,
            enviar=ia_de_pago,
            carpeta_trabajo=tmp,
        )

        assert resultado.get("estado") == "lanzada", (
            "Con el codigo presente la orden debio lanzarse; "
            "quedo en estado %r" % (resultado.get("estado"),)
        )
        assert _contar_llamadas(registro) == 1, (
            "Con el codigo presente se esperaba exactamente una llamada; "
            "se hicieron %d" % _contar_llamadas(registro)
        )


def test_el_estado_real_no_se_toca():
    """La prueba corre en carpetas temporales: el estado real queda intacto."""
    ruta_estado_real = os.path.join(RAIZ, "memoria", "ESTADO.json")
    antes = None
    if os.path.exists(ruta_estado_real):
        with open(ruta_estado_real, "rb") as f:
            antes = f.read()

    with tempfile.TemporaryDirectory() as tmp:
        pieza_que_no_llega = os.path.join(tmp, "no_existe.py")
        orden = _orden_de_prueba(tmp, pieza_que_no_llega)
        registro = {"llamadas": []}

        def ia_de_pago(orden_recibida):
            registro["llamadas"].append(orden_recibida)
            return {"ok": True, "texto": "respuesta de mentira"}

        lanzar_orden_al_equipo(orden, enviar=ia_de_pago, carpeta_trabajo=tmp)

    despues = None
    if os.path.exists(ruta_estado_real):
        with open(ruta_estado_real, "rb") as f:
            despues = f.read()

    assert antes == despues, (
        "La prueba toco el estado real (memoria/ESTADO.json); tiene que correr "
        "solo en carpetas temporales"
    )


if __name__ == "__main__":
    sys.exit(pytest.main([os.path.abspath(__file__), "-v"]))
