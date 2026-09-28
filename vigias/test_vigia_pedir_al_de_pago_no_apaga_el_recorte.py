# -*- coding: utf-8 -*-

"""VIGIA: pedir al de pago NO apaga el recorte del pasillo.

QUE VIGILA, con el hecho medido delante
---------------------------------------
En cuerpo/obrero.py, dentro de _preguntar_con_relevo, hay un filtro que recorta el
encargo a la capacidad real del cerebro mas pequeno que este despierto, y llama para
eso a asignador.recortar_prompt. Ese filtro vive dentro de una condicion que lo APAGA
cuando el trabajo es pesado:

    if turnos and not pesado:
        ...
        _recortado = asignador.recortar_prompt(prompt, _tope_pasillo)

Y 'pesado' se enciende solo en cuanto el que va a escribir es uno de los de pago. Como
todas las rondas se lanzan pidiendo que escriba el de pago, el filtro no se ejecuta
nunca: el encargo viaja con 40.000 letras y a todos los gratis se les salta por tamano.

Medido el 2026-09-28: el cerebro gratis escribio cero de 19 rondas, con el aviso de que
no le cabe en todas, entre 19.950 y 44.605 letras contra 19.042 que aguanta.

LA REGLA CORRECTA, palabras de Julio: el material se corta SIEMPRE a su minima
expresion, y lo pesado solo decide a quien se le pregunta primero, nunca cuanto material
viaja.

ESTA VIGIA NACE ROJA A PROPOSITO
--------------------------------
El arreglo entra en la ronda siguiente. En esta ronda NO se toca cuerpo/obrero.py ni
ningun otro archivo. Por eso test_con_pesado_tambien_se_recorta esta roja hoy: con
pesado=True el recorte no se llama. test_sin_pesado_se_sigue_recortando ya pasa hoy, y
sirve para demostrar que el arreglo no rompe lo que ya funcionaba.

SIN IA, SIN RED, SIN PROCESOS
-----------------------------
Todo el montaje es monkeypatch sobre cuerpo/obrero.py. Despues del recorte, cuotas.rankear
devuelve lista vacia, asi que la funcion vuelve sin llamar a nadie. Y el atajo que llama
a Claude se cambia por uno que revienta, para que quede demostrado que no se llamo.
"""

import os
import sys



# ---------------------------------------------------------------------------
# ARRANQUE: sys.path con la carpeta de arriba de vigias y con la carpeta cuerpo
# ---------------------------------------------------------------------------

AQUI = os.path.dirname(os.path.abspath(__file__))
VIGIAS = AQUI
RAIZ = os.path.dirname(VIGIAS)
CUERPO = os.path.join(RAIZ, "cuerpo")

for _ruta in (RAIZ, CUERPO):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)


# ---------------------------------------------------------------------------
# CONSTANTES DEL CONTRATO
# ---------------------------------------------------------------------------

NOMBRE_DE_MENTIRA = "cerebro_de_mentira"
CAPACIDAD_FALSA = 19042
LETRAS_DEL_ENCARGO = 40000
LETRAS_DEL_RECORTE = 100
APODO_FALSO = "el de mentira"


# ---------------------------------------------------------------------------
# AYUDANTE COMUN DEL MONTAJE
# ---------------------------------------------------------------------------

def _montar(monkeypatch):
    """Monta el escenario entero sobre cuerpo/obrero.py y devuelve (obrero, apuntes).

    Devuelve:
      obrero  -> el modulo cuerpo.obrero ya parcheado
      apuntes -> lista donde el recortar_prompt falso apunta (letras, tope) de cada llamada

    Los cinco pasos del montaje:
      1. asignador.recortar_prompt -> falso que apunta y devuelve texto corto.
      2. obrero.quienes_hay -> falso que devuelve solo [cerebro_de_mentira].
      3. cuotas._capacidad -> 19042; cuotas.ORDEN -> [cerebro_de_mentira];
         cuotas.APODO -> {cerebro_de_mentira: apodo}.
      4. cuotas.rankear -> lista vacia (nadie a quien preguntar: no se gasta nada).
      5. el atajo que llama a Claude -> revienta si alguien lo llama.
    """
    from cuerpo import obrero
    from cuerpo import cuotas

    apuntes = []

    # --- Paso 0: el cerebro prestado devuelve pareja no vacia ---
    def prestar_cerebro_falso(*args, **kwargs):
        return object(), ""

    monkeypatch.setattr(obrero, "prestar_cerebro", prestar_cerebro_falso)

    # --- Paso 1: el recortador falso ---
    def recortar_prompt_falso(texto, tope):
        apuntes.append((len(texto), tope))
        return "x" * LETRAS_DEL_RECORTE

    monkeypatch.setattr(obrero.asignador, "recortar_prompt", recortar_prompt_falso)

    # --- Paso 2: quienes_hay falso ---
    def quienes_hay_falso():
        return [NOMBRE_DE_MENTIRA]

    monkeypatch.setattr(obrero, "quienes_hay", quienes_hay_falso)

    # --- Paso 3: cuotas (capacidad, ORDEN, APODO) ---
    def capacidad_falsa(quien):
        return CAPACIDAD_FALSA

    monkeypatch.setattr(cuotas, "_capacidad", capacidad_falsa)
    monkeypatch.setattr(cuotas, "ORDEN", [NOMBRE_DE_MENTIRA])
    monkeypatch.setattr(cuotas, "APODO", {NOMBRE_DE_MENTIRA: APODO_FALSO})

    # --- Paso 4: rankear falso, lista vacia ---
    def rankear_falso(turnos, tamano):
        return []

    monkeypatch.setattr(cuotas, "rankear", rankear_falso)

    # --- Paso 5: el atajo que llama a Claude revienta si alguien lo llama ---
    def claude_prohibido(*args, **kwargs):
        raise AssertionError(
            "no se debia llamar al atajo de Claude en esta prueba: "
            "el montaje deja a rankear sin cerebros para que nadie sea preguntado"
        )

    for _nombre in ("_preguntar_a_claude", "preguntar_a_claude", "_claude",
                    "_llamar_a_claude", "_atajo_claude"):
        if hasattr(obrero, _nombre):
            monkeypatch.setattr(obrero, _nombre, claude_prohibido)

    return obrero, apuntes


# ---------------------------------------------------------------------------
# PRUEBA 1: con pesado=True TAMBIEN se recorta  (HOY ROJA, a proposito)
# ---------------------------------------------------------------------------

def test_con_pesado_tambien_se_recorta(monkeypatch):
    """Con pesado=True el recorte del pasillo SI se llama, con el tope medido.

    Hoy esta roja: el filtro vive dentro de 'if turnos and not pesado', asi que con
    pesado=True no se ejecuta y la lista de apuntes queda vacia.
    """
    obrero, apuntes = _montar(monkeypatch)

    texto = "a" * LETRAS_DEL_ENCARGO

    obrero._preguntar_con_relevo(texto, 0.2, pesado=True)

    assert apuntes, (
        "con pesado=True el recorte NO se llamo: el filtro del pasillo esta apagado "
        "y el encargo viaja entero (medido: 40.000 letras contra 19.042 que aguanta un gratis)"
    )
    assert apuntes[0][1] == CAPACIDAD_FALSA, (
        "el recorte se llamo con tope %r y debia llamarse con %d"
        % (apuntes[0][1], CAPACIDAD_FALSA)
    )


# ---------------------------------------------------------------------------
# PRUEBA 2: sin pesado se SIGUE recortando  (ya pasa hoy)
# ---------------------------------------------------------------------------

def test_sin_pesado_se_sigue_recortando(monkeypatch):
    """Con pesado=False el recorte tambien se llama, con el mismo tope.

    Esta prueba ya deberia pasar hoy, y sirve para demostrar que el arreglo no rompe
    lo que ya funcionaba.
    """
    obrero, apuntes = _montar(monkeypatch)

    texto = "a" * LETRAS_DEL_ENCARGO

    obrero._preguntar_con_relevo(texto, 0.2, pesado=False)

    assert apuntes, (
        "sin pesado el recorte NO se llamo: se rompio lo que ya funcionaba"
    )
    assert apuntes[0][1] == CAPACIDAD_FALSA, (
        "el recorte se llamo con tope %r y debia llamarse con %d"
        % (apuntes[0][1], CAPACIDAD_FALSA)
    )
