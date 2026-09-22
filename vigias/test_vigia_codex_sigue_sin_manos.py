import json
import os
import re

import pytest


# ---------------------------------------------------------------------------
# VIGIA: CODEX SIGUE SIN MANOS
#
# Codex (la IA de OpenAI que corre en la terminal) puede quedar con manos si su
# configuracion le permite escribir en disco o si sus reglas de aprobacion le
# dejan hacer git add / git commit / git push sin freno. Esta vigia SOLO LEE la
# carpeta .codex del usuario y comprueba cinco cosas:
#
#   1. config.toml tiene sandbox_mode = "read-only"
#   2. config.toml tiene approval_policy = "never"
#   3. rules/default.rules: las UNICAS reglas con decision allow son las que
#      empiezan por "python ingeniero.py" seguidas de arranca, trabaja, equipo
#      o pit; y hay reglas forbidden para git add, git commit y git push
#   4. hooks.json es JSON valido, arriba solo tiene description y hooks, y
#      tiene un gancho PreToolUse para Bash que corre candado_terminal
#   5. el disco C entero NO esta marcado como de confianza en config.toml
#
# NUNCA se abre auth.json (guarda la sesion del usuario).
# Si la carpeta .codex no existe, las pruebas se saltan con pytest.skip.
# ---------------------------------------------------------------------------


HOME = os.path.expanduser("~")
CODEX_DIR = os.path.join(HOME, ".codex")
CONFIG = os.path.join(CODEX_DIR, "config.toml")
RULES = os.path.join(CODEX_DIR, "rules", "default.rules")
HOOKS = os.path.join(CODEX_DIR, "hooks.json")


# ---------------------------------------------------------------------------
# Utilidades de lectura (solo lectura, nunca auth.json)
# ---------------------------------------------------------------------------


def _exigir_carpeta():
    """Si no existe la carpeta .codex, la prueba se salta."""
    if not os.path.isdir(CODEX_DIR):
        pytest.skip("no existe la carpeta .codex del usuario; no hay nada que vigilar")


def _leer_config():
    """Devuelve el texto de config.toml o salta si no existe."""
    _exigir_carpeta()
    if not os.path.isfile(CONFIG):
        pytest.skip("no existe config.toml en la carpeta .codex")
    with open(CONFIG, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _leer_rules():
    """Devuelve el texto de rules/default.rules o salta si no existe."""
    _exigir_carpeta()
    if not os.path.isfile(RULES):
        pytest.skip("no existe rules/default.rules en la carpeta .codex")
    with open(RULES, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _leer_hooks():
    """Devuelve el texto de hooks.json o salta si no existe."""
    _exigir_carpeta()
    if not os.path.isfile(HOOKS):
        pytest.skip("no existe hooks.json en la carpeta .codex")
    with open(HOOKS, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _valor_toml(texto, clave):
    """Saca el valor de una clave TOML simple (clave = valor) del texto.

    Devuelve el valor sin comillas ni espacios, o None si no aparece.
    Se ignoran las lineas comentadas con #.
    """
    patron = re.compile(
        r"^\s*" + re.escape(clave) + r"\s*=\s*(.+?)\s*(?:#.*)?$",
        re.MULTILINE,
    )
    m = patron.search(texto)
    if not m:
        return None
    valor = m.group(1).strip()
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in ("'", '"'):
        valor = valor[1:-1]
    return valor


def _lineas_utiles(texto):
    """Devuelve las lineas no vacias y no comentadas."""
    salida = []
    for linea in texto.splitlines():
        limpia = linea.strip()
        if not limpia or limpia.startswith("#"):
            continue
        salida.append(limpia)
    return salida


# ---------------------------------------------------------------------------
# Prueba 1: sandbox_mode = read-only
# ---------------------------------------------------------------------------


def test_config_sandbox_mode_read_only():
    """Codex debe estar en modo solo lectura; si no, queda con manos."""
    texto = _leer_config()
    valor = _valor_toml(texto, "sandbox_mode")
    assert valor is not None, (
        "FALLO: config.toml no tiene sandbox_mode. Sin esa clave Codex no tiene "
        "modo de solo lectura y quedaria con manos para escribir en disco."
    )
    assert valor == "read-only", (
        "FALLO: sandbox_mode es '%s' y deberia ser 'read-only'. Con ese valor "
        "Codex queda con manos y puede escribir archivos sin freno." % valor
    )


# ---------------------------------------------------------------------------
# Prueba 2: approval_policy = never
# ---------------------------------------------------------------------------


def test_config_approval_policy_never():
    """Codex no debe pedir aprobacion interactiva; si no, queda sin frenos."""
    texto = _leer_config()
    valor = _valor_toml(texto, "approval_policy")
    assert valor is not None, (
        "FALLO: config.toml no tiene approval_policy. Sin esa clave Codex no "
        "tiene politica de aprobacion y quedaria sin frenos."
    )
    assert valor == "never", (
        "FALLO: approval_policy es '%s' y deberia ser 'never'. Con ese valor "
        "Codex queda sin frenos y puede ejecutar sin que nadie apruebe." % valor
    )


# ---------------------------------------------------------------------------
# Prueba 3: reglas allow y forbidden en rules/default.rules
# ---------------------------------------------------------------------------

# Prefijos permitidos para las reglas con decision allow.
# Son las ordenes al equipo, igual que Claude: arranca, trabaja, equipo, pit.
_PREFIJOS_ALLOW = (
    "python ingeniero.py arranca",
    "python ingeniero.py trabaja",
    "python ingeniero.py equipo",
    "python ingeniero.py pit",
)


def _reglas_allow(texto):
    """Devuelve la lista de lineas de reglas con decision allow."""
    allow = []
    for linea in _lineas_utiles(texto):
        # Formato tipico: decision = "allow"  o  allow: ...
        if re.search(r'decision\s*=\s*["\']?allow["\']?', linea, re.IGNORECASE):
            allow.append(linea)
        elif re.match(r'^allow\b', linea, re.IGNORECASE):
            allow.append(linea)
    return allow


def _reglas_forbidden(texto):
    """Devuelve la lista de lineas de reglas con decision forbidden."""
    forbidden = []
    for linea in _lineas_utiles(texto):
        if re.search(r'decision\s*=\s*["\']?forbidden["\']?', linea, re.IGNORECASE):
            forbidden.append(linea)
        elif re.match(r'^forbidden\b', linea, re.IGNORECASE):
            forbidden.append(linea)
    return forbidden


def _texto_regla(linea):
    """Saca el texto de la orden de una linea de regla, sin la parte de decision."""
    # Quita la parte decision = "..."
    limpia = re.sub(r'decision\s*=\s*["\']?\w+["\']?', "", linea, flags=re.IGNORECASE)
    # Quita el prefijo allow/forbidden si va al principio
    limpia = re.sub(r'^(allow|forbidden)\b[:\s]*', "", limpia, flags=re.IGNORECASE)
    return limpia.strip().strip('"\'').strip()


def test_rules_allow_solo_ordenes_al_equipo_y_forbidden_git():
    """Las unicas reglas allow son las ordenes al equipo; git add/commit/push van forbidden."""
    texto = _leer_rules()

    allow = _reglas_allow(texto)
    assert allow, (
        "FALLO: rules/default.rules no tiene ninguna regla con decision allow. "
        "Sin reglas allow Codex no puede dar ordenes al equipo y quedaria sin manos."
    )

    for linea in allow:
        orden = _texto_regla(linea)
        assert orden.startswith(_PREFIJOS_ALLOW), (
            "FALLO: hay una regla allow que no es una orden al equipo: '%s'. "
            "Solo se permite 'python ingeniero.py arranca|trabaja|equipo|pit'. "
            "Con esa regla de mas Codex quedaria con manos." % orden
        )

    forbidden = _reglas_forbidden(texto)
    assert forbidden, (
        "FALLO: rules/default.rules no tiene ninguna regla forbidden. "
        "Sin reglas forbidden Codex quedaria sin frenos para git."
    )

    texto_forbidden = " ".join(_texto_regla(l) for l in forbidden).lower()
    for orden in ("git add", "git commit", "git push"):
        assert orden in texto_forbidden, (
            "FALLO: falta la regla forbidden para '%s'. Sin ella Codex quedaria "
            "sin frenos y podria tocar el repositorio." % orden
        )


# ---------------------------------------------------------------------------
# Prueba 4: hooks.json valido, con solo description y hooks, y PreToolUse/Bash
# ---------------------------------------------------------------------------


def test_hooks_json_valido_con_pre_tool_use_bash():
    """hooks.json debe ser JSON, tener solo description y hooks, y el gancho de Bash."""
    texto = _leer_hooks()

    try:
        datos = json.loads(texto)
    except Exception as e:
        raise AssertionError(
            "FALLO: hooks.json no se puede leer como JSON (%s). Codex ignora el "
            "archivo entero y quedaria sin frenos." % str(e)[:120]
        )

    assert isinstance(datos, dict), (
        "FALLO: hooks.json no es un objeto JSON. Codex ignora el archivo entero "
        "y quedaria sin frenos."
    )

    claves = set(datos.keys())
    sobrantes = claves - {"description", "hooks"}
    assert not sobrantes, (
        "FALLO: hooks.json tiene claves de mas arriba: %s. Codex ignora el archivo "
        "entero si trae otra clave y quedaria sin frenos." % sorted(sobrantes)
    )
    assert "hooks" in claves, (
        "FALLO: hooks.json no tiene la clave 'hooks'. Sin ganchos Codex quedaria sin frenos."
    )

    hooks = datos.get("hooks")
    assert isinstance(hooks, dict), (
        "FALLO: la clave 'hooks' de hooks.json no es un objeto. Codex no podria "
        "enganchar el candado y quedaria sin frenos."
    )

    pre = hooks.get("PreToolUse")
    assert pre is not None, (
        "FALLO: hooks.json no tiene un gancho PreToolUse. Sin ese gancho Codex "
        "quedaria sin frenos antes de usar la terminal."
    )

    # PreToolUse puede ser una lista de ganchos o un solo gancho.
    if isinstance(pre, list):
        ganchos = pre
    else:
        ganchos = [pre]

    encontrado = False
    for gancho in ganchos:
        if not isinstance(gancho, dict):
            continue
        matcher = str(gancho.get("matcher", ""))
        comando = str(gancho.get("command", ""))
        if "Bash" in matcher and "candado_terminal" in comando:
            encontrado = True
            break

    assert encontrado, (
        "FALLO: hooks.json no tiene un gancho PreToolUse para Bash que corra "
        "candado_terminal. Sin ese candado Codex quedaria sin frenos en la terminal."
    )


# ---------------------------------------------------------------------------
# Prueba 5: el disco C entero NO esta marcado como de confianza
# ---------------------------------------------------------------------------


def _lineas_confianza_c(texto):
    """Devuelve las lineas que marcan C: (o C:\\) como de confianza.

    Se busca la clave 'trusted' (o 'trust') con un valor que sea el disco C
    entero: 'C:', 'C:\\', 'C:/', 'c:', etc. No cuenta una subcarpeta como
    'C:\\Ingeniero_VUC' porque esa no es el disco entero.
    """
    patron = re.compile(
        r'^\s*(trusted|trust)\s*=\s*["\']?\s*([cC])\s*:\s*[\\/]?\s*["\']?\s*(?:#.*)?$',
        re.MULTILINE,
    )
    return [m.group(0).strip() for m in patron.finditer(texto)]


def test_disco_c_no_esta_marcado_como_de_confianza():
    """El disco C entero no debe estar de confianza; si lo esta, Codex queda con manos."""
    texto = _leer_config()

    lineas = _lineas_confianza_c(texto)
    assert not lineas, (
        "FALLO: config.toml marca el disco C entero como de confianza: %s. "
        "Con eso Codex queda con manos sobre todo el disco y puede escribir "
        "fuera de su carpeta." % lineas
    )

    # Comprobacion extra: si hay una lista de rutas de confianza, que C: no este
    # suelto dentro de ella (por ejemplo trusted_paths = ["C:\\"]).
    for linea in _lineas_utiles(texto):
        if not re.match(r'^\s*(trusted_paths|trusted_dirs|trusted_folders)\s*=', linea, re.IGNORECASE):
            continue
        # Busca C: o C:\ o C:/ como elemento suelto de la lista.
        if re.search(r'["\']\s*[cC]\s*:\s*[\\/]?\s*["\']', linea):
            raise AssertionError(
                "FALLO: config.toml incluye el disco C entero en una lista de "
                "confianza: '%s'. Con eso Codex queda con manos sobre todo el "
                "disco." % linea
            )
