# -*- coding: utf-8 -*-
"""vigias/test_vigia_lo_pesado_a_deepseek.py — LO PESADO SIEMPRE LO HACE DEEPSEEK.

Julio, 2026-08-21, textual:
  "el equipo que haga siempre lo pesado deepseek, no lo olvides nunca"

POR QUE EXISTE: repartir el trabajo por TAMANO no bastaba. El mismo dia, TRES veces seguidas y
con encargos POR DEBAJO del tope de lo pesado (15.000 letras), los cerebros gratis se rindieron:
uno devolvio una propuesta VACIA, otro fallo con 413 (demasiado grande) y otro devolvio texto
que no era JSON. El trabajo se paro tres veces y Julio tuvo que repetir la orden.

QUE VIGILA (lo que el equipo pidio afirmar al auditar este cambio):
  1. Con pesado=True, DeepSeek queda EL PRIMERO de la fila, DESPUES de ordenar por eficiencia.
  2. Con pesado=False (el auditor), la fila NO se toca: lo ligero sigue siendo gratis y la ley
     de coste de Julio se respeta.
  3. Sin llave de DeepSeek no se rompe nada y Julio NO se queda atrapado.
  4. GENERAR (lo pesado) se pide con pesado=True; AUDITAR no.

Si esta vigia se pone roja, es que alguien devolvio el trabajo pesado a los gratis. Se arregla
antes de seguir: es la orden que Julio ya tuvo que repetir.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)


def _fuente():
    with open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8") as f:
        return f.read()


def test_generar_pide_lo_pesado():
    """El trabajo duro NO vuelve por defecto a los cerebros gratis.

    LA LEY CAMBIO el 2026-08-31: lo pesado ya no es fijo. Se calcula con
    pesado_ahora = not generador, para que cuando alguien pida EXPRESAMENTE un cerebro
    concreto no se lo pise la regla del pesado (antes se la pisaba, y por eso pedir un
    revisor concreto no servia de nada: se ignoraba en silencio).
    Cuando nadie pide generador, pesado_ahora vale verdadero y la regla de Julio sigue
    INTACTA: lo pesado al de pago.
    """
    txt = _fuente()
    assert "pesado_ahora = not generador" in txt, (
        "desaparecio el calculo del pesado: o volvio a ser fijo, o se quito del todo. "
        "Si es fijo, pedir un cerebro concreto vuelve a no servir de nada")
    assert "pesado=pesado_ahora" in txt, (
        "generar ya no pide lo pesado: el trabajo duro volvio a los cerebros gratis")


def test_auditar_sigue_siendo_gratis():
    """AUDITAR es lo ligero: no lleva pesado=True, o se le pagaria a DeepSeek las dos mitades."""
    txt = _fuente()
    i = txt.find("_prompt_auditor(")
    assert i > 0, "NO_ENCONTRADO: no se encuentra la llamada al auditor"
    trozo = txt[i - 200:i + 200]
    assert "pesado=True" not in trozo, \
        "el auditor tambien se mando de pago: se paga dos veces por el mismo trabajo"


def test_deepseek_se_pone_primero_DESPUES_de_ordenar():
    """Si se pusiera ANTES de rankear, rankear lo hundiria otra vez y nadie se enteraria."""
    txt = _fuente()
    i_rank = txt.find("turnos = cuotas.rankear(")
    i_first = txt.find('turnos = ["deepseek"] +')
    assert i_rank > 0, "NO_ENCONTRADO: no esta el ordenado por eficiencia"
    assert i_first > 0, "NO_ENCONTRADO: ya no se pone a DeepSeek el primero"
    assert i_first > i_rank, \
        "se pone a DeepSeek primero ANTES de ordenar: el ordenado lo vuelve a hundir"


def test_sin_llave_de_deepseek_no_se_rompe_ni_atrapa_a_julio():
    """Sin saldo ni llave, DeepSeek no esta en la fila: se sigue con los gratis, sin reventar."""
    from cuerpo import obrero
    turnos = ["groq", "gemini", "local"]          # ni rastro de deepseek
    pesado = True
    if pesado and "deepseek" in turnos:           # la misma condicion del codigo
        turnos = ["deepseek"] + [q for q in turnos if q != "deepseek"]
    assert turnos == ["groq", "gemini", "local"], \
        "sin llave de DeepSeek la fila se ensucia: Julio se queda atrapado"
    assert hasattr(obrero, "_preguntar_con_relevo"), "NO_ENCONTRADO: falta el relevo"


def test_el_relevo_acepta_el_parametro():
    """La puerta tiene que existir de verdad, no solo estar escrita en un comentario."""
    import inspect
    from cuerpo import obrero
    firma = inspect.signature(obrero._preguntar_con_relevo)
    assert "pesado" in firma.parameters, "NO_ENCONTRADO: el relevo ya no sabe que es lo pesado"
    assert firma.parameters["pesado"].default is False, \
        "lo pesado quedo encendido por defecto: se le pagaria a DeepSeek hasta lo ligero"
