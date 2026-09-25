def test_el_candado_frena_un_ancla_de_varios_renglones():
    """Comprueba que el candado arnes/candado_ancla.py rechaza un fragmento de varios renglones
    y acepta uno de un solo renglón que aparece una única vez en el archivo."""
    import json
    import subprocess
    import sys
    from pathlib import Path

    candado_path = Path(__file__).parents[1] / "arnes" / "candado_ancla.py"
    assert candado_path.is_file(), f"Falta el candado {candado_path}"
    def _correr(texto):
        return subprocess.run(
            [sys.executable, str(candado_path)],
            input=json.dumps({"comando": texto}),
            capture_output=True,
            text=True,
        )

    sys.path.insert(0, str(Path(__file__).parents[1]))
    from arnes import autorizacion as _autorizacion
    if _autorizacion.autorizada():
        return
    if autorizacion.is_file() and "Julio" in autorizacion.read_text(encoding="utf-8"):
        import pytest
        pytest.skip("Julio abrio la llave: el candado se abre a proposito")

    ancla = 'def _archivos_py(texto):'

    # Caso uno: texto con las palabras ingeniero.py equipo, nombra el candado y trae un renglon
    # copiado tal cual que aparece una sola vez. El candado deja pasar (codigo cero).
    texto_uno = (
        "ingeniero.py equipo\n"
        "arnes/candado_ancla.py\n"
        f"{ancla}\n"
    )
    r_uno = _correr(texto_uno)
    assert r_uno.returncode == 0, r_uno.stderr

    # Caso dos: el mismo texto pero con un trozo con pinta de codigo que no aparece en ningun
    # archivo nombrado. El candado frena (codigo dos).
    texto_dos = (
        "ingeniero.py equipo\n"
        "arnes/candado_ancla.py\n"
        f"{ancla}\n"
        "def funcion_inventada_que_no_existe():\n"
    )
    r_dos = _correr(texto_dos)
    assert r_dos.returncode == 2, r_dos.stderr

    # Caso tres: una frase normal en espanol que nombra un archivo entre parentesis y no trae
    # codigo. El candado deja pasar (codigo cero).
    texto_tres = "Revisa el archivo (arnes/candado_ancla.py) cuando puedas.\n"
    r_tres = _correr(texto_tres)
    assert r_tres.returncode == 0, r_tres.stderr


def test_vigia_el_candado_respeta_la_llave_de_julio(monkeypatch):
    """Fallo del 2026-09-25: el candado arnes/candado_ancla.py pregunta por cuatro
    nombres que no existen (julio_autorizo, autorizo_julio, autorizado, julio_autoriza)
    y nunca por la funcion autorizada de arnes.autorizacion, asi que no respeta la
    llave de Julio. Esta prueba nace roja a proposito."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parents[1]))
    from arnes import autorizacion as _autorizacion
    from arnes import candado_ancla as _candado_ancla

    monkeypatch.setattr(_autorizacion, "autorizada", lambda: True)
    assert _candado_ancla._autorizado() is True