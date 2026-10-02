"""VIGIA: el bucle no se detiene porque una orden falle tres veces del mismo tipo.

Lo que se vigila (palabras de Julio, 2026-10-01):
    "una serie de pasos logicos que desbloquee todo el trabajo, no que se
    detenga cada instante".

Medido hoy: el bucle termina con PARADO cuando una orden falla tres veces
igual en la misma pieza, y con NADA SE PUEDE CORRER cuando falla la primera.
Una falla aislada detiene todo el trabajo.

Lo que TIENE que pasar cuando la reparacion este hecha:
  1. Una orden que falla TRES VECES DEL MISMO TIPO en la misma pieza se marca
     como APARTADA, con su motivo y su expediente.
  2. Solo quedan fuera las ordenes que DEPENDEN de la apartada.
  3. El bucle CONTINUA con la siguiente orden corrible.
  4. El bucle solo termina si no queda ninguna corrible o si DeepSeek no tiene
     saldo.
  5. Al final se imprime un resumen de las ordenes apartadas y por que.

Esta vigia NACE ROJA: hoy el bucle se para. Se prueba EJECUTANDO el bucle de
verdad, con carpetas temporales y con un DeepSeek de mentira que contesta
siempre lo mismo (nada de llamadas reales, nada de estado real).

Regla de la casa: una vigia inestable no vale para nada. Aqui TODO es
determinista: el cerebro de mentira contesta lo que le digamos, y el estado
vive en un tmp_path que se borra solo.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# 1. LOCALIZAR LA PIEZA DEL BUCLE
# ---------------------------------------------------------------------------
# La pieza aun no existe (por eso esta vigia nace roja). Se busca por los
# nombres razonables del bucle y, si no aparece, se falla con un assert claro
# que dice QUE pieza falta, en vez de un ImportError ciego.

CANDIDATOS_BUCLE = (
    "arnes.bucle",
    "arnes.bucle_ordenes",
    "arnes.el_bucle",
    "cuerpo.bucle",
    "cuerpo.bucle_ordenes",
    "bucle",
    "bucle_ordenes",
)

NOMBRES_FUNCION_BUCLE = (
    "correr_bucle",
    "ejecutar_bucle",
    "correr_ordenes",
    "ejecutar_ordenes",
    "bucle",
    "correr",
)


def _cargar_pieza_del_bucle():
    """Devuelve (modulo, nombre_de_la_funcion) del bucle, o falla con assert.

    Si la pieza no existe todavia, el assert explica que falta. Eso es
    exactamente lo que queremos: la vigia nace ROJA por un assert, no por un
    error raro de importacion.
    """
    modulo = None
    for nombre in CANDIDATOS_BUCLE:
        try:
            modulo = importlib.import_module(nombre)
            break
        except ImportError:
            continue

    assert modulo is not None, (
        "FALTA LA PIEZA DEL BUCLE: no existe ningun modulo de "
        f"{CANDIDATOS_BUCLE!r}. Sin el bucle no se puede vigilar que no se "
        "detenga por fallos. Esta vigia nace ROJA a proposito."
    )

    for nombre_funcion in NOMBRES_FUNCION_BUCLE:
        if callable(getattr(modulo, nombre_funcion, None)):
            return modulo, nombre_funcion

    assert False, (
        f"La pieza {modulo.__name__!r} existe pero no expone ninguna funcion "
        f"de bucle entre {NOMBRES_FUNCION_BUCLE!r}. No se puede ejecutar el "
        "bucle para vigilarlo."
    )


# ---------------------------------------------------------------------------
# 2. DEEPSEEK DE MENTIRA (determinista, sin red, sin llaves)
# ---------------------------------------------------------------------------
# Nunca se llama a DeepSeek de verdad. El cerebro de mentira contesta SIEMPRE
# lo mismo: un fallo del tipo que le pidamos. Asi la vigia es estable.


class DeepSeekDeMentira:
    """Contesta siempre lo mismo. Cuenta las llamadas. No toca la red."""

    def __init__(self, respuesta: str = "FALLO_DEL_MISMO_TIPO") -> None:
        self.respuesta = respuesta
        self.llamadas = 0
        self.sin_saldo = False

    def preguntar(self, *args, **kwargs) -> str:
        self.llamadas += 1
        if self.sin_saldo:
            raise RuntimeError("DeepSeek sin saldo")
        return self.respuesta

    # Alias por si la pieza usa otro nombre.
    def llamar(self, *args, **kwargs) -> str:
        return self.preguntar(*args, **kwargs)

    def completar(self, *args, **kwargs) -> str:
        return self.preguntar(*args, **kwargs)


# ---------------------------------------------------------------------------
# 3. EL ESCENARIO: tres ordenes, una falla tres veces, otra depende de ella
# ---------------------------------------------------------------------------
# Piezas y ordenes:
#   - pieza P1: orden A (falla 3 veces del mismo tipo) -> se aparta
#   - pieza P1: orden B (depende de A)                  -> se queda fuera
#   - pieza P2: orden C (independiente, corrible)       -> TIENE que correr
#
# Si el bucle se para al apartar A, C nunca corre y la vigia se pone roja.


def _escribir_ordenes(tmp_path: Path) -> Path:
    """Escribe el plan de ordenes en una carpeta temporal. Nada real."""
    plan = {
        "ordenes": [
            {
                "id": "A",
                "pieza": "P1",
                "tipo": "reparar",
                "depende_de": [],
                "corrible": True,
            },
            {
                "id": "B",
                "pieza": "P1",
                "tipo": "reparar",
                "depende_de": ["A"],
                "corrible": True,
            },
            {
                "id": "C",
                "pieza": "P2",
                "tipo": "reparar",
                "depende_de": [],
                "corrible": True,
            },
        ]
    }
    ruta = tmp_path / "ordenes.json"
    ruta.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return ruta


# ---------------------------------------------------------------------------
# 4. LA VIGIA
# ---------------------------------------------------------------------------


def test_el_bucle_no_se_detiene_por_fallos(tmp_path, capsys):
    """El bucle aparta la orden que falla 3 veces y SIGUE con la corrible.

    Nace ROJA: hoy el bucle se para con PARADO y C nunca corre.
    """
    modulo, nombre_funcion = _cargar_pieza_del_bucle()
    correr_bucle = getattr(modulo, nombre_funcion)

    ruta_ordenes = _escribir_ordenes(tmp_path)
    cerebro = DeepSeekDeMentira(respuesta="FALLO_DEL_MISMO_TIPO")

    # Se ejecuta el bucle de verdad, con estado en tmp_path y cerebro de
    # mentira. Nada real se toca.
    resultado = correr_bucle(
        ruta_ordenes=ruta_ordenes,
        cerebro=cerebro,
        carpeta_estado=tmp_path / "estado",
        max_fallos_mismo_tipo=3,
    )

    # --- 1. La orden A quedo APARTADA, con motivo y expediente -------------
    apartadas = _leer_apartadas(resultado)
    ids_apartadas = {a["id"] for a in apartadas}
    assert "A" in ids_apartadas, (
        "La orden A fallo tres veces del mismo tipo en la misma pieza y NO "
        f"quedo apartada. Apartadas: {ids_apartadas!r}. El bucle se paro en "
        "vez de apartarla y seguir."
    )
    apartada_a = next(a for a in apartadas if a["id"] == "A")
    assert apartada_a.get("motivo"), (
        "La orden A quedo apartada pero SIN motivo escrito. Julio pidio que "
        "se sepa por que se aparta cada orden."
    )
    assert apartada_a.get("expediente"), (
        "La orden A quedo apartada pero SIN expediente. Sin expediente no se "
        "puede revisar despues que paso."
    )

    # --- 2. Solo queda fuera la que DEPENDE de A (la B) --------------------
    assert "B" in ids_apartadas, (
        "La orden B depende de A y A quedo apartada, asi que B tenia que "
        f"quedar fuera. Apartadas: {ids_apartadas!r}."
    )
    assert "C" not in ids_apartadas, (
        "La orden C es independiente y corrible: NO tenia que quedar "
        f"apartada. Apartadas: {ids_apartadas!r}."
    )

    # --- 3. El bucle CONTINUO con la siguiente corrible (la C) -------------
    corridas = _leer_corridas(resultado)
    assert "C" in corridas, (
        "El bucle NO continuo con la siguiente orden corrible: la C no "
        f"corrio. Corridas: {corridas!r}. El bucle se detuvo al apartar A, "
        "que es justo lo que Julio prohibio."
    )

    # --- 4. El bucle NO termino por el fallo, sino por no quedar corribles -
    assert resultado.get("termino_por") != "PARADO", (
        "El bucle termino con PARADO por el fallo de A. Tenia que seguir "
        "hasta que no quedara ninguna corrible."
    )
    assert resultado.get("termino_por") in ("SIN_CORRIBLES", "SIN_SALDO"), (
        "El bucle termino por un motivo que no es 'no quedan corribles' ni "
        f"'DeepSeek sin saldo': {resultado.get('termino_por')!r}."
    )

    # --- 5. Al final se imprime el resumen de apartadas y por que ----------
    salida = capsys.readouterr().out
    assert "A" in salida and "apartada" in salida.lower(), (
        "Al final del bucle NO se imprimio un resumen de las ordenes "
        "apartadas y por que. Salida capturada: "
        f"{salida!r}"
    )


# ---------------------------------------------------------------------------
# 5. LECTURA DEL RESULTADO (tolerante a la forma, estricta en el fondo)
# ---------------------------------------------------------------------------

def _leer_apartadas(resultado) -> list[dict]:
    """Saca la lista de apartadas del resultado, sea dict o atributo."""
    if isinstance(resultado, dict):
        crudo = resultado.get("apartadas", [])
    else:
        crudo = getattr(resultado, "apartadas", [])
    return [_normalizar_apartada(a) for a in crudo]


def _normalizar_apartada(a) -> dict:
    if isinstance(a, dict):
        return a
    return {
        "id": getattr(a, "id", None),
        "motivo": getattr(a, "motivo", None),
        "expediente": getattr(a, "expediente", None),
    }


def _leer_corridas(resultado) -> list[str]:
    """Saca los ids de las ordenes que SI corrieron."""
    if isinstance(resultado, dict):
        crudo = resultado.get("corridas", [])
    else:
        crudo = getattr(resultado, "corridas", [])
    ids = []
    for c in crudo:
        if isinstance(c, dict):
            ids.append(c.get("id"))
        else:
            ids.append(getattr(c, "id", c))
    return ids


# ---------------------------------------------------------------------------
# 6. LA OTRA CARA: si DeepSeek no tiene saldo, el bucle SI termina
# ---------------------------------------------------------------------------
# Julio lo dijo: el bucle termina solo si no queda ninguna corrible o si
# DeepSeek no tiene saldo. Esta prueba fija esa segunda salida para que la
# reparacion no se pase de lista y siga para siempre.


def test_el_bucle_termina_si_deepseek_no_tiene_saldo(tmp_path):
    """Sin saldo, el bucle para. Es la unica parada legitima por fallo."""
    modulo, nombre_funcion = _cargar_pieza_del_bucle()
    correr_bucle = getattr(modulo, nombre_funcion)

    ruta_ordenes = _escribir_ordenes(tmp_path)
    cerebro = DeepSeekDeMentira()
    cerebro.sin_saldo = True

    resultado = correr_bucle(
        ruta_ordenes=ruta_ordenes,
        cerebro=cerebro,
        carpeta_estado=tmp_path / "estado",
        max_fallos_mismo_tipo=3,
    )

    assert resultado.get("termino_por") == "SIN_SALDO", (
        "Con DeepSeek sin saldo el bucle tenia que terminar con SIN_SALDO, "
        f"y termino con {resultado.get('termino_por')!r}."
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
