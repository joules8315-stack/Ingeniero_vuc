# -*- coding: utf-8 -*-
"""VIGIA — SOLO LAS LLAMADAS QUE HACEN FALTA.

Julio, 2026-08-21: "que haga solo las llamadas que necesite, nada mas, en el tiempo que
necesite, para esperar respuesta."

Ley que la manda: CONTRATO_VELOCIDAD_LLAMADAS.md

QUE PASA HOY (medido, no supuesto):
  - El servidor contesta en 3 milesimas de segundo. NO es lento.
  - Cada viaje a la nube cuesta algo mas de medio segundo, y cada accion dispara VARIOS EN FILA:
    crear informe 4, anadir diario 3, subir foto 3, asignar 2, generar 2.
  - La pantalla pide desde unos 48 sitios distintos; 16 piden lo mismo.

LAS CUATRO FUGAS QUE ESTA VIGIA REPRODUCE:
  1. Al guardar CUALQUIER cosa se borra la libreta de respuestas ENTERA, aunque lo guardado no
     tenga nada que ver.
  2. El reloj despierta cada 12 segundos en TODAS las pantallas, se mire o no.
  3. Al esconder la ventana solo se calla el dictado por voz: el reloj sigue llamando.
  4. Todas las esperas son la misma (25 s), hasta para una lectura que tarda medio segundo.

NACE ROJA a proposito. Esa es su razon de ser: una vigia que no se pone roja con el fallo
delante no protege nada, solo lo aparenta.

DECIDIDO POR JULIO (2026-08-21):
  - La pantalla 4 (fotos) mira cada 5 segundos y SOLO con la ventana a la vista, porque las
    fotos entran desde el celular mientras el informe se arma en el computador.
  - En las demas pantallas, CERO reloj.
  - La espera de LEER baja a 10 segundos. Las de SUBIR (60 s) y GENERAR (120 s) NO se tocan:
    acortarlas corta un guardado por la mitad y Julio pierde el borrador.
"""
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
PANTALLA = os.path.join(AQUI, "app_web.html")


def _pantalla():
    with open(PANTALLA, encoding="utf-8") as f:
        return f.read()


def _numero(texto, nombre):
    m = re.search(nombre + r"\s*=\s*(\d+)", texto)
    return int(m.group(1)) if m else None


# ─── FUGA 4: cada espera dura lo que necesita ─────────────────────────────────
def test_leer_no_espera_lo_mismo_que_guardar():
    """Una lectura tarda medio segundo. Esperarla 25 s es lo contrario de 'el tiempo que necesite'."""
    t = _pantalla()
    lectura = _numero(t, "API_LECTURA_TIMEOUT_MS")
    assert lectura is not None, \
        "no existe una espera propia para LEER: todo espera lo mismo que guardar"
    assert lectura <= 10000, "la espera de leer sigue siendo demasiado larga: %s" % lectura


def test_las_esperas_largas_siguen_intactas():
    """LO PROHIBIDO. Acortar subir o generar corta el guardado y Julio PIERDE EL BORRADOR."""
    t = _pantalla()
    assert _numero(t, "UPLOAD_TIMEOUT_MS") == 60000, \
        "se acorto la espera de SUBIR: Julio puede perder el borrador de una foto"
    assert _numero(t, "GENERATE_TIMEOUT_MS") == 120000, \
        "se acorto la espera de GENERAR: el informe se puede cortar por la mitad"
    assert _numero(t, "API_TIMEOUT_MS") >= 25000, \
        "se acorto la espera general: alcanza tambien a los guardados"


# ─── FUGA 2: el reloj solo donde hace falta ───────────────────────────────────
def test_el_reloj_solo_corre_en_la_pantalla_de_fotos():
    """Hoy despierta en todas las pantallas. Solo hace falta donde entran las fotos del celular."""
    t = _pantalla()
    m = re.search(r"function scheduleAutoSync\(\)\{(.*?)\}", t, re.S)
    assert m, "NO_ENCONTRADO: no esta la funcion que programa el reloj"
    cuerpo = m.group(1)
    assert re.search(r"state\.page\s*\)?\s*!==?\s*4|!==\s*4", cuerpo), \
        "el reloj sigue despertando en TODAS las pantallas: llama unas 300 veces por hora sin que nadie mire"


def test_el_reloj_de_fotos_es_de_cinco_segundos():
    """Decidido por Julio: 5 segundos, y solo en la pantalla de las fotos."""
    t = _pantalla()
    assert _numero(t, "AUTO_SYNC_MS") == 5000, \
        "el reloj no esta en los 5 segundos que decidio Julio: %s" % _numero(t, "AUTO_SYNC_MS")


# ─── FUGA 3: si no la miras, no pregunta ──────────────────────────────────────
def test_al_esconder_la_ventana_se_calla_el_reloj():
    """Comprobado en vivo: hoy al esconderla solo se calla el dictado por voz."""
    t = _pantalla()
    i = t.find("visibilitychange")
    assert i > 0, "NO_ENCONTRADO: no se hace nada al esconder la ventana"
    trozo = t[i:i + 1200]
    assert "stopAutoSync()" in trozo, \
        "al esconder la ventana el reloj sigue llamando a la nube"


def test_al_volver_a_la_ventana_el_reloj_solo_revive_en_la_pantalla_de_fotos():
    """Volver no puede encender el reloj en cualquier pantalla: eso deshace la reparacion."""
    t = _pantalla()
    i = t.find("visibilitychange")
    trozo = t[i:i + 1200]
    j = trozo.find("else")
    assert j > 0, "NO_ENCONTRADO: no se hace nada al volver a la ventana"
    al_volver = trozo[j:]
    if "scheduleAutoSync()" in al_volver:
        assert re.search(r"page\s*\)?\s*===?\s*4", al_volver), \
            "al volver enciende el reloj sin mirar en que pantalla esta"


# ─── FUGA 1: guardar no borra la libreta entera ───────────────────────────────
def test_guardar_no_borra_la_libreta_entera():
    """LA PEOR DE LAS CUATRO. Hoy guardas un titulo y se le olvida hasta la lista de informes."""
    t = _pantalla()
    m = re.search(r'if\(method!=="GET"\)\{(.*?)\}\s*(?:if|const|state|return)', t, re.S)
    assert m, "NO_ENCONTRADO: no esta el trozo que limpia la libreta al guardar"
    trozo = m.group(1)
    assert "apiResponseCache={}" not in trozo.replace(" ", ""), \
        ("al guardar se sigue borrando la libreta ENTERA: la pantalla vuelve a preguntarlo todo "
         "desde cero en la siguiente accion")


def test_hay_borrado_selectivo():
    """Regla 1 de Julio: que borre lo que se pide borrar, unica y exclusivamente."""
    t = _pantalla()
    assert "invalidarLibretaDeEsaRuta" in t or "invalidateCacheForPath" in t, \
        "no existe ninguna forma de olvidar SOLO lo que el guardado toca"
