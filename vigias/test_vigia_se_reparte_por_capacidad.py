# -*- coding: utf-8 -*-
"""VIGIA — SE REPARTE POR CAPACIDAD REAL, NO POR SUPOSICION.

Julio, 2026-09-09, despues de la auditoria de causa raiz:

  "Actualmente: 'No me dijeron que generador usar' = 'trabajo pesado'. Eso esta mal.
   Debe ser: '¿cuanto ocupa realmente este trabajo y que IA puede manejarlo?' Y entonces elegir."

FALLO REAL QUE LA TRAE (medido, no supuesto):
  `cuerpo/obrero.py` -> `pesado_ahora = not generador` y `if len(prompt) > TOPE_PESADO or pesado:`.
  Cuando nadie pide generador —que es el caso NORMAL— el sistema daba el encargo por "pesado" y
  ponia al cerebro de PAGO el primero ANTES de mirar cuanto medía. Medido el 2026-09-09 en vivo:
  dos rondas del equipo pedidas con `--escribe gemini4` las contesto DeepSeek (de pago), y el
  auditor gratis SI contesto. Los gratis llevan 0 de 72 trabajos reales escritos, y no por malos:
  porque nunca se les dio la oportunidad.

COMO SE MIDE (esto es lo importante): con un ESPIA. Se sustituyen las puertas por las que se habla
con los cerebros por una que solo APUNTA a quien se le pidio y contesta al instante. Asi se
comprueba A QUIEN LE TOCA de verdad, sin gastar ni una llamada de verdad.

QUE VIGILA (una prueba por caso de la tabla de la verdad del contrato):
  A/B  lo que SI le cabe a un gratis, no lo contesta el de pago.
  C    al que no aguanta NO se le pide (y al que si aguanta, si).
  D    lo que de verdad no le cabe a NADIE gratis, si cae en el de pago.
  G    sin de pago y sin gratis que aguante: SE PARA (nunca a solas), sin pedirle a nadie.
  5    la ley vieja ("pesado = not generador") no puede volver por descuido.

Ley: `CONTRATO_EL_PASILLO_SE_REPARTA_POR_CAPACIDAD.md`
"""
import inspect
import os
import sys
import types

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from cuerpo import cuotas, obrero  # noqa: E402

GRATIS = ["groq", "groq20b", "gemini", "gemini2", "gemini3", "gemini4"]
CINTURON = GRATIS + ["deepseek"]


def _capacidades(monkeypatch, valores):
    """Deja las capacidades MEDIDAS en los valores que diga la prueba (no en las de hoy)."""
    monkeypatch.setattr(cuotas, "_leer",
                        lambda: {"gasto": {q: {"llamadas": 0, "fallos": 0} for q in CINTURON},
                                 "dormidos": {}})
    monkeypatch.setattr(cuotas, "_medidas", lambda: dict(valores))
    monkeypatch.setattr(cuotas, "apuntar_uso", lambda *a, **k: None)
    monkeypatch.setattr(cuotas, "dormir", lambda *a, **k: None)
    monkeypatch.setattr(cuotas, "apuntar_no_cupo", lambda *a, **k: None)


def _espia(monkeypatch):
    """Sustituye las puertas de los cerebros por una que solo APUNTA a quien se le pidio.

    Todo queda dentro de casa: ni una llamada de verdad, ni una cuota gastada. Tambien se
    sustituye `prestar_cerebro` porque el de verdad intenta levantar el servicio del PC de Julio
    y esta vigia no puede depender de eso ni tardar.
    """
    pedidos = []

    def puerta(nombre):
        def _f(*a, **k):
            pedidos.append(nombre)
            return '{"veredicto": "APROBADO"}'
        return _f

    monkeypatch.setattr(obrero, "_gemini_directo", puerta("gemini"))
    monkeypatch.setattr(obrero, "_deepseek_directo", puerta("deepseek"))
    monkeypatch.setattr(obrero, "preguntar_local", puerta("local"))
    # `raising=False`: el cerebro prestado no siempre trae todas las puertas (OpenRouter se saco de
    # la fila el 2026-09-01). El espia no puede reventar por una puerta que no existe.
    monkeypatch.setattr(obrero, "_openrouter_directo", puerta("router"), raising=False)
    # Cada gratis de Groq se llama con SU modelo, y ese es el unico dato que distingue a groq de
    # groq20b en la llamada (los dos salen por la misma puerta `_preguntar_groq`). Sin esto la
    # vigia no podria decir a CUAL de los dos se le pidio, y el caso C -que exige que se le pida al
    # unico gratis que aguanta ese tamano- no mediria nada.
    modelos_de_prueba = {("modelo_" + q): ("modelo-de-" + q) for q in CINTURON}
    monkeypatch.setattr(obrero, "_velocidad", lambda: dict(modelos_de_prueba, tope_segundos=5))

    def puerta_groq(prompt, modelo=None, temperatura=None):
        quien = {v: k[len("modelo_"):] for k, v in modelos_de_prueba.items()}.get(modelo, "groq?")
        pedidos.append(quien)
        return '{"veredicto": "APROBADO"}'

    monkeypatch.setattr(obrero, "prestar_cerebro",
                        lambda: (types.SimpleNamespace(_preguntar_groq=puerta_groq), None))
    # La vigia mide el REPARTO, no la privacidad. `limpiar` tarda ~1 segundo por cada 1.000
    # letras (medido: 19.500 letras = 19,8 s) y aqui solo estorba.
    from cuerpo import privacidad
    monkeypatch.setattr(privacidad, "limpiar", lambda p: (p, 0))
    return pedidos



def test_AB_lo_que_le_cabe_a_un_gratis_no_lo_contesta_el_de_pago(monkeypatch):
    """El caso NORMAL: sin generador pedido y un encargo que un gratis aguanta.

    19.500 letras: por debajo de lo que aguantan los gratis de la prueba, y por ENCIMA del tope
    declarado de 15.000 que hoy decide sin medir. Era exactamente el agujero.
    """
    _capacidades(monkeypatch, {"groq": 19042, "groq20b": 20169, "gemini": 107349,
                               "gemini2": 194297, "gemini3": 30314, "gemini4": 193689,
                               "local": 12887, "deepseek": 230668})
    monkeypatch.setattr(obrero, "quienes_hay", lambda: list(CINTURON))
    pedidos = _espia(monkeypatch)
    obrero._preguntar_con_relevo("x" * 19500, 0.2)
    assert pedidos, "no se le pidio a nadie: la prueba no mide nada"
    assert pedidos[0] != "deepseek", (
        "un encargo de 19.500 letras, que los gratis SI aguantan, lo contesto el de PAGO. "
        "Es el fallo que dejo a los gratis con 0 de 72 trabajos")


def test_C_al_que_no_aguanta_no_se_le_pide(monkeypatch):
    """19.500 letras: solo groq20b (20.169) aguanta. Ni groq (19.042) ni local (12.887)."""
    _capacidades(monkeypatch, {"groq": 19042, "groq20b": 20169, "gemini": 19000,
                               "gemini2": 19000, "gemini3": 19000, "gemini4": 19000,
                               "local": 12887, "deepseek": 230668})
    monkeypatch.setattr(obrero, "quienes_hay", lambda: list(CINTURON))
    pedidos = _espia(monkeypatch)
    obrero._preguntar_con_relevo("x" * 19500, 0.2)
    assert pedidos and pedidos[0] == "groq20b", (
        "no se le pidio al unico gratis que aguanta ese tamano: %r" % (pedidos,))


def test_D_lo_que_no_le_cabe_a_ningun_gratis_cae_en_el_de_pago(monkeypatch):
    """Lo PESADO de verdad sigue yendo al de pago (la orden de Julio no se tira)."""
    _capacidades(monkeypatch, {"groq": 19042, "groq20b": 20169, "gemini": 30314,
                               "gemini2": 40000, "gemini3": 30314, "gemini4": 50000,
                               "local": 12887, "deepseek": 230668})
    monkeypatch.setattr(obrero, "quienes_hay", lambda: list(CINTURON))
    pedidos = _espia(monkeypatch)
    obrero._preguntar_con_relevo("x" * 60000, 0.2)
    assert pedidos and pedidos[0] == "deepseek", (
        "un encargo que ningun gratis aguanta tiene que ir al de pago: %r" % (pedidos,))


def test_G_sin_de_pago_y_sin_gratis_que_aguante_se_PARA(monkeypatch):
    """Nunca a solas (F2): no se vuelca a los gratis lo que no aguantan. Y no se le pide a nadie."""
    _capacidades(monkeypatch, {q: 19042 for q in GRATIS})
    monkeypatch.setattr(obrero, "quienes_hay", lambda: list(GRATIS))
    pedidos = _espia(monkeypatch)
    txt, quien, avisos = obrero._preguntar_con_relevo("x" * 60000, 0.2, pesado=True)
    assert not pedidos, "se le mando a un gratis lo que no aguanta: %r" % (pedidos,)
    assert txt == "" and quien == "", "se dio por bueno un trabajo que nadie podia hacer"
    assert any("BLOQUEADO F2" in a for a in avisos), \
        "no se para en seco cuando de verdad no le cabe a nadie: %r" % (avisos,)


def test_5_la_ley_vieja_no_puede_volver():
    """`pesado_ahora = not generador` es exactamente el fallo. No puede volver.

    Y no basta con que desaparezca esa linea: el tope declarado tampoco puede volver a decidir,
    ni la capacidad puede dejar de medirse. Por eso se mira tambien el sitio donde de verdad se
    decide (`_preguntar_con_relevo`), no solo donde se calcula la bandera.
    """
    src = inspect.getsource(obrero.trabajar)
    assert "pesado_ahora = not generador" not in src, (
        "volvio la suposicion: 'no me dijeron generador' = 'trabajo pesado'")
    assert "pesado_ahora = not " not in src, (
        "la suposicion volvio por la puerta de atras: el pesado no puede salir de la AUSENCIA de "
        "un generador pedido, solo de que se pida uno de pago o de lo que mide el encargo")
    rele = inspect.getsource(obrero._preguntar_con_relevo)
    assert "cuotas.rankear(turnos" in rele, (
        "_preguntar_con_relevo ya no mide la capacidad para decidir a quien le toca")
    assert "TOPE_PESADO" not in rele, (
        "volvio el tope declarado a mano (15.000 letras) a decidir el reparto sin medir")
