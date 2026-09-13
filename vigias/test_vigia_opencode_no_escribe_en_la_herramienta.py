import json
import os

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEGOCIO = r"C:\Users\USER\dev\Asesor Marketing"

REGLAS_TERMINAL = [
    "* > *",
    "*>>*",
    "rm *",
    "mv *",
    "cp *",
    "git add*",
    "git commit*",
    "git checkout*",
    "git reset*",
]


def herramienta_cerrada(cfg):
    abierto = []
    permiso = cfg.get("permission") or {}
    if permiso.get("edit") != "deny":
        abierto.append("se puede escribir archivos (edit no es deny)")
    if permiso.get("external_directory") != "deny":
        abierto.append("se puede salir de la carpeta (external_directory no es deny)")
    bash = permiso.get("bash") or {}
    if not isinstance(bash, dict):
        abierto.append("la terminal no tiene reglas")
        return abierto
    for regla in REGLAS_TERMINAL:
        if bash.get(regla) != "deny":
            abierto.append("la terminal permite: " + regla)
    return abierto


def test_la_herramienta_no_deja_escribir_a_opencode():
    cfg = json.load(open(os.path.join(AQUI, "opencode.json"), encoding="utf-8"))
    abierto = herramienta_cerrada(cfg)
    assert not abierto, (
        "la puerta trasera esta abierta otra vez: el ayudante podria escribir en la "
        "herramienta sin equipo; Julio lo prohibio. Abierto: " + str(abierto)
    )


def test_el_negocio_no_deja_tocar_la_herramienta():
    ruta = os.path.join(NEGOCIO, "opencode.json")
    if not os.path.exists(ruta):
        pytest.skip("el negocio no esta en esta maquina")
    ext = (json.load(open(ruta, encoding="utf-8")).get("permission") or {}).get(
        "external_directory"
    ) or {}
    assert isinstance(ext, dict) and ext.get("C:\\Ingeniero_VUC\\*") == "deny", (
        "desde el negocio se podria escribir o leer la herramienta"
    )


def test_la_vigia_caza_un_candado_aflojado():
    flojo = {"permission": {"edit": "allow", "external_directory": "ask", "bash": {"*": "allow"}}}
    abierto = herramienta_cerrada(flojo)
    assert any("edit" in a for a in abierto) and any("git add*" in a for a in abierto), (
        "la vigia no se entera de un candado aflojado, asi no protege nada"
    )