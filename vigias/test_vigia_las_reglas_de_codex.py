import os
import importlib.util


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_REGLAS = os.path.join(RAIZ, "config", "codex", "default.rules")
RUTA_INSTALADOR = os.path.join(RAIZ, "arnes", "instalar_reglas_codex.py")


def _leer_reglas():
    with open(RUTA_REGLAS, "r", encoding="utf-8") as f:
        return f.read()


def _lineas_allow(texto):
    """Devuelve las lineas que llevan decision="allow"."""
    salida = []
    for linea in texto.splitlines():
        if 'decision="allow"' in linea:
            salida.append(linea.strip())
    return salida


def _lineas_forbidden(texto):
    """Devuelve las lineas que llevan decision="forbidden"."""
    salida = []
    for linea in texto.splitlines():
        if 'decision="forbidden"' in linea:
            salida.append(linea.strip())
    return salida


def _cargar_instalador():
    """Carga arnes/instalar_reglas_codex.py por ruta, sin depender del paquete."""
    spec = importlib.util.spec_from_file_location("instalar_reglas_codex", RUTA_INSTALADOR)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_las_reglas_de_codex_existen():
    assert os.path.isfile(RUTA_REGLAS), "falta config/codex/default.rules"


def test_allow_son_exactamente_cinco_y_las_de_ingeniero():
    texto = _leer_reglas()
    allow = _lineas_allow(texto)
    assert len(allow) == 5, "se esperaban 5 lineas con decision=\"allow\", hay %d" % len(allow)
    esperadas = [
        "python ingeniero.py arranca",
        "python ingeniero.py trabaja",
        "python ingeniero.py equipo",
        "python ingeniero.py pit",
        "python ingeniero.py director",
    ]
    for esperada in esperadas:
        encontrada = False
        for linea in allow:
            if esperada in linea:
                encontrada = True
                break
        assert encontrada, "falta la regla allow para: %s" % esperada


def test_forbidden_para_git_peligroso():
    texto = _leer_reglas()
    forbidden = _lineas_forbidden(texto)
    assert forbidden, "no hay ninguna linea con decision=\"forbidden\""
    prohibidos = ["git add", "commit", "push", "reset", "restore", "checkout"]
    for prohibido in prohibidos:
        encontrado = False
        for linea in forbidden:
            if prohibido in linea:
                encontrado = True
                break
        assert encontrado, "falta la regla forbidden para: %s" % prohibido


def test_instalar_copia_y_guarda_antes(tmp_path):
    modulo = _cargar_instalador()
    origen = tmp_path / "origen.rules"
    destino = tmp_path / "destino.rules"
    origen.write_text("reglas nuevas\n", encoding="utf-8")
    destino.write_text("reglas viejas\n", encoding="utf-8")

    resultado = modulo.instalar(str(origen), str(destino))
    assert resultado is True, "la primera llamada debia copiar y devolver True"
    assert destino.read_text(encoding="utf-8") == "reglas nuevas\n"
    antes = tmp_path / "destino.rules.antes"
    assert antes.is_file(), "no se guardo la copia .antes"
    assert antes.read_text(encoding="utf-8") == "reglas viejas\n"

    resultado2 = modulo.instalar(str(origen), str(destino))
    assert resultado2 is False, "la segunda llamada debia devolver False porque ya eran iguales"
