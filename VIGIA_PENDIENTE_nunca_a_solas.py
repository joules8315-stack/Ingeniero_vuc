# -*- coding: utf-8 -*-
"""VIGIA — NUNCA A SOLAS: crear tambien es escribir, y todo queda apuntado.

Ley: CONTRATO_NUNCA_A_SOLAS.md (Julio, 2026-08-28), tras cazarme por TERCERA vez escribiendo
codigo sin equipo.

FALLO MEDIDO ese dia: el candado del equipo decia "crear no es reescribir" y dejaba pasar cualquier
archivo NUEVO. Por esa puerta se construyo un subsistema entero a solas. La letra se cumplio; el
espiritu no. Y ademas el candado solo apuntaba lo que BLOQUEABA, nunca lo que dejaba pasar, asi que
cuando Julio pregunto "usaste el equipo?" la unica fuente era la memoria de la IA.

Estas vigias NACEN ROJAS: hoy el candado deja pasar los archivos nuevos y no lleva registro.

No llaman a ningun cerebro ni a la red: le dan de comer al candado un caso de mentira y miran que
contesta. Deterministas.
"""
import json
import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDADO = os.path.join(AQUI, "arnes", "candado_equipo.py")
REGISTRO = os.path.join(AQUI, "memoria", "DECISIONES_CANDADO.log")


def _preguntarle_al_candado(ruta_archivo, entorno=None):
    """Le pasa al candado un intento de escritura y devuelve (codigo_de_salida, lo_que_dijo)."""
    env = dict(os.environ)
    env["INGENIERO_AUTORIZACION_TEST"] = os.path.join(AQUI, "memoria", ".no_existe_esta_llave")
    env.pop("INGENIERO_OFF", None)
    env.update(entorno or {})
    entrada = json.dumps({"tool_input": {"file_path": ruta_archivo}})
    r = subprocess.run([sys.executable, CANDADO], input=entrada, capture_output=True,
                       text=True, cwd=AQUI, env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


@pytest.fixture
def sin_veredicto():
    """Aparta el veredicto de verdad para que la prueba no dependa del trabajo real de hoy."""
    real = os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
    guardado = None
    if os.path.exists(real):
        with open(real, encoding="utf-8") as f:
            guardado = f.read()
        os.remove(real)
    yield
    if guardado is not None:
        with open(real, "w", encoding="utf-8") as f:
            f.write(guardado)


# ------------------------------------------------------------------ LEY 1: crear es escribir

def test_crear_un_archivo_de_codigo_NUEVO_sin_equipo_se_FRENA(tmp_path, sin_veredicto):
    """EL AGUJERO POR EL QUE PASE EL 2026-08-28.

    El candado decia "crear no es reescribir" y abria. Por ahi se construyo el portero entero,
    sus vigias y dos forenses, todo a solas.
    """
    nuevo = str(tmp_path / "pieza_nueva.py")          # no existe: es CREAR
    codigo, dijo = _preguntarle_al_candado(nuevo)
    assert codigo == 2, (
        "dejo CREAR un archivo de codigo nuevo sin veredicto del equipo. Ese es el agujero por el "
        "que se trabajo a solas: la regla decia 'no reescribas solo' y crear no contaba.\n%s"
        % dijo[:300])


def test_los_documentos_siguen_libres(tmp_path, sin_veredicto):
    """La ley y la memoria se escriben en documentos. Bloquearlos impediria legislar."""
    codigo, _ = _preguntarle_al_candado(str(tmp_path / "CONTRATO_LO_QUE_SEA.md"))
    assert codigo == 0, "freno un documento: asi no se podria ni escribir la ley"


def test_el_propio_arnes_sigue_libre(sin_veredicto):
    """Hay que poder reparar los candados, o el sistema no se puede arreglar a si mismo."""
    codigo, _ = _preguntarle_al_candado(os.path.join(AQUI, "arnes", "candado_equipo.py"))
    assert codigo == 0, "freno el propio arnes: entonces no se puede reparar un candado roto"


# ------------------------------------------------------------------ LEY 2: la vigia nace roja

def test_una_vigia_nueva_SI_se_puede_crear(tmp_path, sin_veredicto):
    """El metodo de Julio obliga a escribir la vigia ANTES de la reparacion.

    Si crear necesitara equipo, el metodo se trabaria a si mismo.
    """
    codigo, dijo = _preguntarle_al_candado(str(tmp_path / "test_vigia_algo_nuevo.py"))
    assert codigo == 0, (
        "freno la creacion de una vigia nueva: el metodo de Julio exige que la vigia nazca "
        "PRIMERO, asi que esto trabaria el propio metodo.\n%s" % dijo[:300])


def test_no_basta_con_LLAMARSE_vigia_para_colar_codigo(tmp_path, sin_veredicto):
    """La trampa del 2026-08-28: cumplir la letra y saltarse el espiritu.

    Si vale con el nombre, se le pone el nombre correcto a cualquier cosa y se cuela igual.
    """
    trampa = str(tmp_path / "test_vigia_pero_esto_es_el_programa.py")
    with open(trampa, "w", encoding="utf-8") as f:
        f.write("def esto_no_es_una_vigia():\n    return 'programa disfrazado'\n")
    codigo, dijo = _preguntarle_al_candado(trampa)
    assert codigo == 2, (
        "dejo pasar codigo disfrazado de vigia solo por el nombre del archivo. Es la MISMA trampa "
        "de la ley 1: cumplir la letra y saltarse el espiritu.\n%s" % dijo[:300])


# ------------------------------------------------------------------ LEY 3: se apunta lo que pasa

def test_el_candado_apunta_tambien_cuando_DEJA_PASAR(tmp_path, sin_veredicto):
    """EL FALLO: solo apuntaba los bloqueos. Cuando abria, no dejaba rastro.

    Por eso, cuando Julio pregunto "usaste el equipo?", la unica fuente era mi memoria.
    """
    antes = ""
    if os.path.exists(REGISTRO):
        with open(REGISTRO, encoding="utf-8", errors="replace") as f:
            antes = f.read()
    doc = str(tmp_path / "UN_DOCUMENTO.md")
    _preguntarle_al_candado(doc)
    assert os.path.exists(REGISTRO), (
        "no existe el registro de decisiones: sin el, la unica fuente de si hubo equipo es la "
        "palabra de la IA, y eso es justo lo que Julio no quiere")
    with open(REGISTRO, encoding="utf-8", errors="replace") as f:
        ahora = f.read()
    assert len(ahora) > len(antes), (
        "el candado dejo pasar y NO apunto nada. Un candado sin registro de lo que permite no se "
        "puede auditar: vale tanto como la palabra del vigilado")
    assert "UN_DOCUMENTO.md" in ahora, "apunto algo, pero no dice QUE archivo se dejo pasar"


def test_el_registro_dice_POR_QUE_se_dejo_pasar(tmp_path, sin_veredicto):
    _preguntarle_al_candado(str(tmp_path / "OTRO_DOCUMENTO.md"))
    with open(REGISTRO, encoding="utf-8", errors="replace") as f:
        lineas = [ln for ln in f.read().splitlines() if "OTRO_DOCUMENTO.md" in ln]
    assert lineas, "no quedo linea de ese archivo"
    assert len(lineas[-1].split("|")) >= 4, (
        "la linea no trae los cuatro datos (cuando, que archivo, que decidio, por que): sin el "
        "porque, Julio ve que paso pero no si estuvo bien")


# ------------------------------------------------------------------ lo que ya funcionaba, sigue

def test_un_RECHAZADO_sigue_sin_abrir(tmp_path, sin_veredicto):
    """Esto ya funcionaba y NO se puede romper al tocar el candado."""
    import time
    real = os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
    with open(real, "w", encoding="utf-8") as f:
        json.dump({"cuando": time.time(), "veredicto": "RECHAZADO",
                   "archivos": ["ya_existe.py"]}, f)
    try:
        existente = str(tmp_path / "ya_existe.py")
        with open(existente, "w", encoding="utf-8") as f:
            f.write("x = 1\n")
        codigo, _ = _preguntarle_al_candado(existente)
        assert codigo == 2, (
            "un RECHAZADO abrio la puerta: eso es un sello de goma, se le diria a Julio que hubo "
            "equipo cuando el equipo dijo que NO")
    finally:
        if os.path.exists(real):
            os.remove(real)


def test_la_ley_esta_escrita_donde_se_lee():
    ley = os.path.join(AQUI, "CONTRATO_NUNCA_A_SOLAS.md")
    assert os.path.exists(ley), "falta el contrato escrito de esta ley"
    with open(ley, encoding="utf-8", errors="replace") as f:
        texto = f.read().lower()
    for frase in ("crear tambien es escribir", "nacer roja", "deja pasar", "solo una cosa llega"):
        assert frase in texto, "el contrato ya no dice '%s': la ley se esta vaciando" % frase
