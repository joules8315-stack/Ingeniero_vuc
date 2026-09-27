# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_guardia_se_acuerda_de_las_rojas_de_antes.py

NACE DE UN FALLO REPETIDO 95 VECES: el guardia de guardado frena el guardado porque
hay pruebas que YA estaban rojas ANTES de este trabajo, y tira trabajo aprobado.

Esta vigia nace ROJA a proposito: hoy el guardia todavia no lee ni escribe el apunte
de las rojas conocidas (memoria/.rojas_conocidas.json). Cuando el guardia aprenda a
leerlo (para no frenar por una roja de antes) y a escribirlo (para apuntar las rojas
de ahora al dejar pasar), esta vigia se pondra verde.

Es autocontenida: no importa otras vigias. Carga el guardia por ruta con importlib,
monta una raiz de mentira en tmp_path, y sustituye subprocess.run DENTRO del modulo
del guardia para no tocar el disco ni la red de verdad.
"""
import importlib.util
import json
import os
import subprocess
import sys


# ---------------------------------------------------------------------------
# CARGA DEL GUARDIA
# ---------------------------------------------------------------------------
def _cargar_guardia():
    """Carga arnes/guardia_de_guardado.py como modulo, por ruta, sin depender
    de que este en sys.path ni de otras vigias."""
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(raiz, "arnes", "guardia_de_guardado.py")
    spec = importlib.util.spec_from_file_location("guardia_de_guardado_bajo_prueba", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# ---------------------------------------------------------------------------
# RAIZ DE MENTIRA
# ---------------------------------------------------------------------------
def _preparar_raiz(tmp_path, ordenes):
    """Crea dentro de tmp_path una raiz con:
      - vigias/test_roja.py  (una prueba que falla)
      - memoria/ORDENES.json (la lista de ordenes que se le pase)
    Devuelve la ruta de la raiz como texto.
    """
    raiz = os.path.join(str(tmp_path), "raiz")
    vigias = os.path.join(raiz, "vigias")
    memoria = os.path.join(raiz, "memoria")
    os.makedirs(vigias, exist_ok=True)
    os.makedirs(memoria, exist_ok=True)

    with open(os.path.join(vigias, "test_roja.py"), "w", encoding="utf-8") as f:
        f.write(
            "# -*- coding: utf-8 -*-\n"
            "def test_roja():\n"
            "    assert False, 'esta prueba nace roja a proposito'\n"
        )

    with open(os.path.join(memoria, "ORDENES.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(ordenes))

    return raiz


# ---------------------------------------------------------------------------
# DOBLE DE subprocess.run DENTRO DEL GUARDIA
# ---------------------------------------------------------------------------
def _parchear_subprocess(monkeypatch, guardia, guardados_en_head, returncode_pytest, salida_pytest):
    """Sustituye subprocess.run DENTRO del modulo cargado del guardia.

    - Si la orden es una lista que contiene 'pytest': devuelve un CompletedProcess
      con el returncode y la salida que se le den.
    - Si la orden es ['git', 'cat-file', '-e', 'HEAD:<archivo>']: devuelve returncode 0
      cuando ese archivo esta en guardados_en_head, y 1 cuando no.
    - Cualquier otra orden: returncode 0 y salida vacia.
    """
    guardados = set(guardados_en_head or [])

    def _run_falso(cmd, *args, **kwargs):
        # Normalizar a lista de textos.
        if isinstance(cmd, (list, tuple)):
            partes = [str(p) for p in cmd]
        else:
            partes = str(cmd).split()

        # pytest
        if any("pytest" in p for p in partes):
            return subprocess.CompletedProcess(
                args=partes,
                returncode=returncode_pytest,
                stdout=salida_pytest,
                stderr="",
            )

        # git cat-file -e HEAD:<archivo>
        if len(partes) >= 4 and partes[0] == "git" and partes[1] == "cat-file" and partes[2] == "-e":
            ref = partes[3]
            if ref.startswith("HEAD:"):
                archivo = ref[len("HEAD:"):].replace("\\", "/")
                rc = 0 if archivo in guardados else 1
                return subprocess.CompletedProcess(
                    args=partes, returncode=rc, stdout="", stderr=""
                )

        # Cualquier otra orden: pasa sin ruido.
        return subprocess.CompletedProcess(
            args=partes, returncode=0, stdout="", stderr=""
        )

    monkeypatch.setattr(guardia.subprocess, "run", _run_falso)

    # Que el guardia use vigias/ por defecto: vecinas.elegir devuelve None.
    try:
        import vecinas  # noqa: F401
        monkeypatch.setattr(vecinas, "elegir", lambda raiz: None)
    except Exception:
        # Si vecinas no esta disponible, el guardia ya cae a vigias/ por defecto.
        pass


# ---------------------------------------------------------------------------
# CASO 1: una roja conocida de antes NO frena
# ---------------------------------------------------------------------------
def test_una_roja_conocida_de_antes_no_frena(tmp_path, monkeypatch):
    """Si la prueba roja ya estaba apuntada como conocida de antes, el guardia
    tiene que DEJAR PASAR: no la rompio este trabajo."""
    guardia = _cargar_guardia()
    raiz = _preparar_raiz(tmp_path, ordenes=[])

    # El apunte de las rojas conocidas de antes.
    memoria = os.path.join(raiz, "memoria")
    os.makedirs(memoria, exist_ok=True)
    with open(os.path.join(memoria, ".rojas_conocidas.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(["vigias/test_roja.py"]))

    salida = "FAILED vigias/test_roja.py - AssertionError: esta prueba nace roja a proposito\n"
    _parchear_subprocess(
        monkeypatch,
        guardia,
        guardados_en_head={"vigias/test_roja.py"},
        returncode_pytest=1,
        salida_pytest=salida,
    )

    paso, mensaje = guardia._vigias(raiz)

    assert paso is True, (
        "una prueba ya roja de antes no la rompio este trabajo y no debe frenar; "
        "el guardia devolvio: %r" % (mensaje,)
    )
    assert mensaje, "el guardia debe explicar por que deja pasar"
    texto = str(mensaje).lower()
    assert ("roja" in texto or "rojo" in texto or "conocida" in texto or "antes" in texto), (
        "el mensaje debe explicar que una prueba ya roja de antes no la rompio este "
        "trabajo y no debe frenar; mensaje: %r" % (mensaje,)
    )


# ---------------------------------------------------------------------------
# CASO 2: al dejar pasar, se apuntan las rojas de ahora
# ---------------------------------------------------------------------------
def test_al_dejar_pasar_se_apuntan_las_rojas_de_ahora(tmp_path, monkeypatch):
    """Si el guardia deja pasar por una roja nueva, tiene que APUNTARLA en
    memoria/.rojas_conocidas.json para no volver a frenar por ella."""
    guardia = _cargar_guardia()
    raiz = _preparar_raiz(tmp_path, ordenes=[])

    salida = "FAILED vigias/test_roja.py - AssertionError: esta prueba nace roja a proposito\n"
    _parchear_subprocess(
        monkeypatch,
        guardia,
        guardados_en_head=set(),  # nada guardado en HEAD: la roja es nueva
        returncode_pytest=1,
        salida_pytest=salida,
    )

    paso, mensaje = guardia._vigias(raiz)
    assert paso is True, (
        "una roja nueva sin pieza aun debe dejar pasar; el guardia devolvio: %r" % (mensaje,)
    )

    ruta_apunte = os.path.join(raiz, "memoria", ".rojas_conocidas.json")
    assert os.path.isfile(ruta_apunte), (
        "al dejar pasar, el guardia tiene que apuntar las rojas de ahora en "
        "memoria/.rojas_conocidas.json"
    )
    with open(ruta_apunte, encoding="utf-8") as f:
        contenido = json.loads(f.read())
    assert "vigias/test_roja.py" in contenido, (
        "el apunte tiene que incluir la roja de ahora; contenido: %r" % (contenido,)
    )
