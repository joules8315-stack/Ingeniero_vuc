# -*- coding: utf-8 -*-
"""VIGIA — NUNCA A SOLAS: sin puertas traseras, y todo queda apuntado.

Ley: CONTRATO_NUNCA_A_SOLAS.md (Julio, 2026-08-28 y 2026-08-31):
  "Que nunca trabajes sin equipo. Absolutamente nunca, que la unica opcion sea trabajo en equipo,
   sin puertas traseras."

LAS 7 PUERTAS DEL CANDADO, MEDIDAS el 2026-08-31 (no supuestas):
  1. La llave de Julio esta puesta               -> pasa   (asi debe ser: es SU llave)
  2. NO SE PUDO LEER LA PETICION                 -> pasa   *** ACCIDENTE, NO EXCEPCION ***
  3. La peticion no trae archivo                 -> pasa   (no hay nada que vigilar)
  4. Es un documento .md                         -> pasa   (si no, no se podria legislar)
  5. EL ARCHIVO NO EXISTE (crear)                -> pasa   *** EL AGUJERO ***
  6. Esta dentro del propio arnes                -> pasa   (hay que poder reparar un candado roto)
  7. Hay veredicto APROBADO que lo cubre         -> pasa   (correcto)

LA PUERTA 2 ES LA PEOR y no estaba vista: el candado hace `try: leer la peticion / except: dejar
pasar`. Si la lectura falla por CUALQUIER motivo, abre entero. Un candado que se abre solo cuando
algo va mal NO es un candado. Y explica lo que no se podia explicar el 2026-08-28: "a veces me deja
pasar y no se por que".

LA PUERTA 5 es por donde se construyo un subsistema entero a solas: la regla decia "no reescribas
solo" y crear no contaba.

ESTAS VIGIAS NACEN ROJAS. No llaman a la red: le dan de comer al candado un caso de mentira y miran
que contesta.
"""
import json
import os
import subprocess
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDADO = os.path.join(AQUI, "arnes", "candado_equipo.py")
REGISTRO = os.path.join(AQUI, "memoria", "DECISIONES_CANDADO.log")

VIGIA_DE_VERDAD = ("import pytest\n"
                   "def test_algo():\n"
                   "    assert 1 == 1\n")


def _preguntarle_al_candado(ruta_archivo=None, contenido=None, entrada_cruda=None):
    """Le pasa al candado un intento de escritura. Devuelve (codigo_de_salida, lo_que_dijo)."""
    env = dict(os.environ)
    env["INGENIERO_AUTORIZACION_TEST"] = os.path.join(AQUI, "memoria", ".no_existe_esta_llave")
    env.pop("INGENIERO_OFF", None)
    if entrada_cruda is None:
        dentro = {"file_path": ruta_archivo}
        if contenido is not None:
            dentro["content"] = contenido
        entrada_cruda = json.dumps({"tool_input": dentro})
    r = subprocess.run([sys.executable, CANDADO], input=entrada_cruda, capture_output=True,
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


# ------------------------------------------------------- PUERTA 2: el candado no se abre solo

def test_si_NO_se_puede_leer_la_peticion_el_candado_FRENA(sin_veredicto):
    """LA PUERTA MAS GRAVE, y no era una excepcion pensada: era un accidente.

    `try: leer / except: dejar pasar`. Si la lectura falla por cualquier motivo, abre entero.
    Un candado que se abre solo cuando algo va mal no es un candado.
    """
    codigo, dijo = _preguntarle_al_candado(entrada_cruda="esto no es json ni de lejos")
    assert codigo == 2, (
        "no se pudo leer la peticion y el candado DEJO PASAR. Se abre solo en cuanto algo va mal, "
        "y eso explica los pases que no se podian explicar.\n%s" % dijo[:300])


def test_una_peticion_vacia_tambien_FRENA(sin_veredicto):
    codigo, _ = _preguntarle_al_candado(entrada_cruda="")
    assert codigo == 2, "con la peticion vacia deja pasar: se abre solo cuando algo va mal"


# ------------------------------------------------------- PUERTA 5: crear tambien es escribir

def test_crear_un_archivo_de_codigo_NUEVO_sin_equipo_se_FRENA(tmp_path, sin_veredicto):
    """EL AGUJERO POR EL QUE SE TRABAJO A SOLAS el 2026-08-28."""
    codigo, dijo = _preguntarle_al_candado(str(tmp_path / "pieza_nueva.py"), "x = 1\n")
    assert codigo == 2, (
        "dejo CREAR un archivo de codigo nuevo sin veredicto del equipo. Por ahi se construyo un "
        "subsistema entero a solas: la regla decia 'no reescribas solo' y crear no contaba.\n%s"
        % dijo[:300])


# ------------------------------------------------------- la vigia nueva SI, pero de verdad

def test_una_vigia_nueva_SI_se_puede_crear(tmp_path, sin_veredicto):
    """El metodo obliga a que la vigia nazca ANTES que la reparacion.

    Si crear necesitara equipo, el metodo se trabaria a si mismo.
    """
    codigo, dijo = _preguntarle_al_candado(str(tmp_path / "test_vigia_algo.py"), VIGIA_DE_VERDAD)
    assert codigo == 0, (
        "freno una vigia nueva de verdad: eso traba el propio metodo de Julio.\n%s" % dijo[:300])


def test_no_basta_con_LLAMARSE_vigia(tmp_path, sin_veredicto):
    """La trampa: cumplir la letra y saltarse el espiritu, que es lo que ya paso una vez."""
    codigo, dijo = _preguntarle_al_candado(
        str(tmp_path / "test_vigia_disfraz.py"), "def esto_es_el_programa():\n    return 7\n")
    assert codigo == 2, (
        "dejo pasar codigo disfrazado de vigia solo por el nombre del archivo.\n%s" % dijo[:300])


def test_sin_contenido_no_se_regala_el_permiso(tmp_path, sin_veredicto):
    """Si no se puede comprobar que es una vigia de verdad, NO se abre."""
    codigo, _ = _preguntarle_al_candado(str(tmp_path / "test_vigia_sin_cuerpo.py"))
    assert codigo == 2, (
        "sin contenido que comprobar dejo pasar igual: eso convierte la excepcion en una puerta")


# ------------------------------------------------------- lo que DEBE seguir pasando

def test_los_documentos_siguen_libres(tmp_path, sin_veredicto):
    codigo, _ = _preguntarle_al_candado(str(tmp_path / "CONTRATO_LO_QUE_SEA.md"), "# ley\n")
    assert codigo == 0, "freno un documento: asi no se podria ni escribir la ley"


def test_el_propio_arnes_sigue_libre(sin_veredicto):
    codigo, _ = _preguntarle_al_candado(CANDADO, "x = 1\n")
    assert codigo == 0, "freno el propio arnes: entonces no se puede reparar un candado roto"


def test_un_RECHAZADO_sigue_sin_abrir(tmp_path, sin_veredicto):
    """Esto ya funcionaba y NO se puede romper al cerrar las puertas."""
    import time
    real = os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
    with open(real, "w", encoding="utf-8") as f:
        json.dump({"cuando": time.time(), "veredicto": "RECHAZADO",
                   "archivos": ["ya_existe.py"]}, f)
    try:
        existente = str(tmp_path / "ya_existe.py")
        with open(existente, "w", encoding="utf-8") as f:
            f.write("x = 1\n")
        codigo, _ = _preguntarle_al_candado(existente, "x = 2\n")
        assert codigo == 2, (
            "un RECHAZADO abrio la puerta: eso es un sello de goma, se le diria a Julio que hubo "
            "equipo cuando el equipo dijo que NO")
    finally:
        if os.path.exists(real):
            os.remove(real)


# ------------------------------------------------------- se apunta lo que DEJA PASAR

def test_el_candado_apunta_tambien_cuando_DEJA_PASAR(tmp_path, sin_veredicto):
    """Sin registro, la unica fuente de si hubo equipo es la palabra de la IA."""
    antes = ""
    if os.path.exists(REGISTRO):
        with open(REGISTRO, encoding="utf-8", errors="replace") as f:
            antes = f.read()
    _preguntarle_al_candado(str(tmp_path / "UN_DOCUMENTO.md"), "# ley\n")
    assert os.path.exists(REGISTRO), (
        "no existe el registro de decisiones: sin el, Julio tiene que creerme en vez de mirarlo")
    with open(REGISTRO, encoding="utf-8", errors="replace") as f:
        ahora = f.read()
    assert len(ahora) > len(antes), "el candado dejo pasar y NO apunto nada"
    assert "UN_DOCUMENTO.md" in ahora, "apunto algo, pero no dice QUE archivo se dejo pasar"


def test_el_registro_dice_POR_QUE(tmp_path, sin_veredicto):
    _preguntarle_al_candado(str(tmp_path / "OTRO_DOCUMENTO.md"), "# ley\n")
    with open(REGISTRO, encoding="utf-8", errors="replace") as f:
        lineas = [ln for ln in f.read().splitlines() if "OTRO_DOCUMENTO.md" in ln]
    assert lineas, "no quedo linea de ese archivo"
    assert len(lineas[-1].split("|")) >= 4, (
        "la linea no trae los cuatro datos (cuando, que archivo, que decidio, por que)")


def test_la_ley_esta_escrita_donde_se_lee():
    ley = os.path.join(AQUI, "CONTRATO_NUNCA_A_SOLAS.md")
    assert os.path.exists(ley), "falta el contrato escrito de esta ley"
    with open(ley, encoding="utf-8", errors="replace") as f:
        texto = f.read().lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")):
        texto = texto.replace(a, b)
    for frase in ("crear tambien es escribir", "nacer roja", "deja pasar"):
        assert frase in texto, "el contrato ya no dice '%s': la ley se esta vaciando" % frase
