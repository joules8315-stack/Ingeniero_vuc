import json, os, subprocess, sys, hashlib
import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDADO = os.path.join(AQUI, "arnes", "candado_no_repetir.py")


def _correr(tmp_path, monkeypatch, mensaje, ingeniero_off="0"):
    """Corre el candado como programa y devuelve (salida, stderr, cuaderno)."""
    cuaderno = tmp_path / "cuaderno.json"
    log = tmp_path / "log.txt"
    contador = tmp_path / "contador"
    monkeypatch.setenv("INGENIERO_OFF", ingeniero_off)
    monkeypatch.setenv("INGENIERO_CUADERNO_TEST", str(cuaderno))
    monkeypatch.setenv("INGENIERO_LOG_TEST", str(log))
    monkeypatch.setenv("INGENIERO_CONTADOR_TEST", str(contador))
    data = json.dumps({"last_assistant_message": mensaje})
    r = subprocess.run([sys.executable, CANDADO], input=data, capture_output=True, text=True, encoding="utf-8")
    cuaderno_datos = set()
    if cuaderno.exists():
        with open(cuaderno, encoding="utf-8") as f:
            cuaderno_datos = set(json.load(f))
    return r.returncode, r.stderr, cuaderno_datos


def _frase_larga(texto):
    texto = texto.rstrip('.')  # quita el punto final
    while len(texto) <= 60:
        texto += ", " + texto  # repite con comas hasta pasar de 60 letras
    return texto + "."  # un solo punto al final


def test_respuesta_nueva_pasa_y_guarda(tmp_path, monkeypatch):
    frase = _frase_larga("Esto es una frase nueva y larga para probar.")
    salida, _, cuaderno = _correr(tmp_path, monkeypatch, frase)
    assert salida == 0
    assert len(cuaderno) == 1
    assert hashlib.md5(frase.encode("utf-8")).hexdigest() in cuaderno


def test_misma_respuesta_se_frena(tmp_path, monkeypatch):
    frase = _frase_larga("Esto es una frase repetida y larga para probar.")
    _correr(tmp_path, monkeypatch, frase)
    salida, stderr, _ = _correr(tmp_path, monkeypatch, frase)
    assert salida == 2
    assert "NO SE PUEDE TERMINAR" in stderr


def test_frase_corta_repetida_pasa(tmp_path, monkeypatch):
    frase_corta = "Hola, esto es corto."  # menos de 60 letras
    _correr(tmp_path, monkeypatch, frase_corta)
    salida, _, _ = _correr(tmp_path, monkeypatch, frase_corta)
    assert salida == 0


def test_no_frena_mas_de_dos_veces(tmp_path, monkeypatch):
    frase = _frase_larga("Frase para probar el tope de bloqueos.")
    _correr(tmp_path, monkeypatch, frase)  # primera: guarda
    _correr(tmp_path, monkeypatch, frase)  # segunda: bloquea (1)
    _correr(tmp_path, monkeypatch, frase)  # tercera: bloquea (2)
    salida, stderr, _ = _correr(tmp_path, monkeypatch, frase)  # cuarta: aviso, pasa
    assert salida == 0
    assert "AVISO" in stderr


def test_ingeniero_off_siempre_pasa(tmp_path, monkeypatch):
    frase = _frase_larga("Frase que deberia repetir pero INGENIERO_OFF=1.")
    _correr(tmp_path, monkeypatch, frase, ingeniero_off="1")
    salida, _, _ = _correr(tmp_path, monkeypatch, frase, ingeniero_off="1")
    assert salida == 0


def test_cuaderno_guarda_solo_huellas(tmp_path, monkeypatch):
    frase = _frase_larga("Frase cuyo texto no debe aparecer en el cuaderno.")
    _correr(tmp_path, monkeypatch, frase)
    _, _, cuaderno = _correr(tmp_path, monkeypatch, frase)
    for huella in cuaderno:
        assert len(huella) == 32  # md5 hexdigest
        assert frase not in huella
