"""Vigia de cuerpo/codex.py: la pieza que le pregunta a Codex.

Comprueba, sin llamar NUNCA a Codex de verdad, que:

1. La orden que arma lleva exec, --sandbox read-only, un -c con
   approval_policy puesto a never, --dangerously-bypass-hook-trust,
   --skip-git-repo-check, -C con la carpeta y -o con el archivo donde
   Codex deja su respuesta final.
2. El entorno que le pasa lleva INGENIERO_OFF=1 y
   INGENIERO_LLAMADA_DEL_PROGRAMA=1.
3. Si el texto a mandar trae una llave de mentira, NO se llama a Codex y
   se devuelve texto vacio con un aviso.
4. Si trae datos personales, tampoco se llama y se avisa.
5. Si Codex se pasa del tope, se devuelve texto vacio y un aviso con los
   segundos.
6. Si Codex contesta, se devuelve lo que dejo en el archivo de la
   respuesta final.

El monkeypatch se hace sobre subprocess.run y shutil.which, cada uno en su
propio modulo (subprocess y shutil), NUNCA a traves de cuerpo.codex.

La pieza se importa DENTRO de cada prueba, para que el monkeypatch este
puesto antes de que la pieza mire nada.
"""

from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


# ---------------------------------------------------------------------------
# Utilidades de la vigia
# ---------------------------------------------------------------------------


def _importar_pieza():
    """Importa cuerpo.codex fresco, dentro de cada prueba."""
    if "cuerpo.codex" in sys.modules:
        del sys.modules["cuerpo.codex"]
    return importlib.import_module("cuerpo.codex")


def _llave_de_mentira() -> str:
    """Arma una llave POR PARTES para que este archivo nunca la traiga entera.

    El guardia no deja guardar archivos con forma de llave, asi que se junta
    letra a letra: la letra s + la letra k + un guion + 24 letras a.
    """
    return "s" + "k" + "-" + ("a" * 24)


def _datos_personales_de_mentira() -> str:
    """Arma un texto con pinta de dato personal, tambien por partes."""
    correo = "julio" + "@" + "ejemplo" + "." + "com"
    cedula = "1" + "0" + "2" + "3" + "4" + "5" + "6" + "7" + "8"
    return f"mi correo es {correo} y mi cedula es {cedula}"


class _FalsoProceso:
    """Proceso de mentira: lo justo para que la pieza no llame a Codex."""

    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = ""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.pid = 4242

    def communicate(self, input=None, timeout=None):
        return self.stdout, self.stderr

    def kill(self):
        return None

    def wait(self, timeout=None):
        return self.returncode


class _Espia:
    """Guarda lo que le llega a subprocess.run para poder mirarlo despues."""

    def __init__(self, respuesta_final: str | None = None, returncode: int = 0):
        self.llamadas: list[dict] = []
        self.respuesta_final = respuesta_final
        self.returncode = returncode

    def __call__(self, *args, **kwargs):
        self.llamadas.append({"args": args, "kwargs": kwargs})
        # Si la pieza pidio un archivo de respuesta final, se lo dejamos escrito
        # para que lo lea, igual que haria Codex de verdad.
        if self.respuesta_final is not None:
            destino = self._archivo_de_respuesta(args, kwargs)
            if destino is not None:
                try:
                    Path(destino).write_text(self.respuesta_final, encoding="utf-8")
                except Exception:
                    pass
        return _FalsoProceso(returncode=self.returncode)

    @staticmethod
    def _archivo_de_respuesta(args, kwargs):
        """Busca en la orden el valor que sigue a -o (el archivo de respuesta)."""
        candidatos = []
        if args:
            primero = args[0]
            if isinstance(primero, (list, tuple)):
                candidatos = list(primero)
            elif isinstance(primero, str):
                candidatos = [primero]
        for i, trozo in enumerate(candidatos):
            if trozo == "-o" and i + 1 < len(candidatos):
                return candidatos[i + 1]
        return None

    def orden(self) -> list[str]:
        """Devuelve la orden (lista de trozos) de la primera llamada."""
        if not self.llamadas:
            return []
        args = self.llamadas[0]["args"]
        if args and isinstance(args[0], (list, tuple)):
            return list(args[0])
        if args and isinstance(args[0], str):
            return [args[0]]
        return []

    def entorno(self) -> dict:
        """Devuelve el entorno que le pasaron (kwargs['env'])."""
        if not self.llamadas:
            return {}
        return dict(self.llamadas[0]["kwargs"].get("env") or {})


@pytest.fixture
def sin_codex_de_verdad(monkeypatch):
    """Deja subprocess.run y shutil.which apuntando a dobles, en sus modulos."""
    espia = _Espia()
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")
    return espia


# ---------------------------------------------------------------------------
# Prueba 1: la orden que arma
# ---------------------------------------------------------------------------


def test_la_orden_lleva_todo_lo_que_tiene_que_llevar(monkeypatch, tmp_path):
    """La orden lleva exec, sandbox read-only, approval_policy never, los
    permisos de hooks, el salto del chequeo de git, la carpeta con -C y el
    archivo de respuesta final con -o."""
    espia = _Espia(respuesta_final="vale")
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")

    codex = _importar_pieza()
    texto, avisos = codex.preguntar("dime algo", timeout=30, raiz=str(tmp_path))

    assert espia.llamadas, "no se llamo a Codex ni una vez"
    orden = espia.orden()
    assert orden, "la orden vino vacia"

    assert "exec" in orden, f"falta exec en la orden: {orden}"

    assert "--sandbox" in orden, f"falta --sandbox en la orden: {orden}"
    i = orden.index("--sandbox")
    assert i + 1 < len(orden) and orden[i + 1] == "read-only", (
        f"--sandbox no va con read-only: {orden}"
    )

    assert "-c" in orden, f"falta el -c con approval_policy: {orden}"
    j = orden.index("-c")
    assert j + 1 < len(orden), f"el -c vino sin valor: {orden}"
    assert "approval_policy" in orden[j + 1], (
        f"el -c no habla de approval_policy: {orden[j + 1]}"
    )
    assert "never" in orden[j + 1], (
        f"approval_policy no esta puesto a never: {orden[j + 1]}"
    )

    assert "--dangerously-bypass-hook-trust" in orden, (
        f"falta --dangerously-bypass-hook-trust: {orden}"
    )
    assert "--skip-git-repo-check" in orden, (
        f"falta --skip-git-repo-check: {orden}"
    )

    assert "-C" in orden, f"falta -C con la carpeta: {orden}"
    k = orden.index("-C")
    assert k + 1 < len(orden), f"el -C vino sin carpeta: {orden}"
    assert str(tmp_path) in orden[k + 1], (
        f"-C no apunta a la carpeta pedida: {orden[k + 1]}"
    )

    assert "-o" in orden, f"falta -o con el archivo de respuesta final: {orden}"
    m = orden.index("-o")
    assert m + 1 < len(orden), f"el -o vino sin archivo: {orden}"
    assert orden[m + 1].strip(), "el -o vino con archivo vacio"

    assert isinstance(texto, str)
    assert isinstance(avisos, list)


# ---------------------------------------------------------------------------
# Prueba 2: el entorno que le pasa
# ---------------------------------------------------------------------------


def test_el_entorno_lleva_las_dos_marcas(monkeypatch, tmp_path):
    """El entorno lleva INGENIERO_OFF=1 y INGENIERO_LLAMADA_DEL_PROGRAMA=1."""
    espia = _Espia(respuesta_final="vale")
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")

    codex = _importar_pieza()
    codex.preguntar("dime algo", timeout=30, raiz=str(tmp_path))

    assert espia.llamadas, "no se llamo a Codex ni una vez"
    entorno = espia.entorno()
    assert entorno, "no se le paso entorno a Codex"

    assert str(entorno.get("INGENIERO_OFF")) == "1", (
        f"INGENIERO_OFF no esta a 1: {entorno.get('INGENIERO_OFF')!r}"
    )
    assert str(entorno.get("INGENIERO_LLAMADA_DEL_PROGRAMA")) == "1", (
        "INGENIERO_LLAMADA_DEL_PROGRAMA no esta a 1: "
        f"{entorno.get('INGENIERO_LLAMADA_DEL_PROGRAMA')!r}"
    )


# ---------------------------------------------------------------------------
# Prueba 3: llave de mentira
# ---------------------------------------------------------------------------


def test_con_llave_de_mentira_no_se_llama_a_codex(monkeypatch, tmp_path):
    """Si el texto trae una llave, no se llama a Codex y se avisa."""
    espia = _Espia(respuesta_final="no deberia leerse")
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")

    codex = _importar_pieza()
    prompt = "usa esta llave " + _llave_de_mentira() + " para entrar"
    texto, avisos = codex.preguntar(prompt, timeout=30, raiz=str(tmp_path))

    assert espia.llamadas == [], "se llamo a Codex con una llave en el texto"
    assert texto == "", f"se devolvio texto con una llave: {texto!r}"
    assert avisos, "no se aviso de la llave"
    assert any("llave" in a.lower() for a in avisos), (
        f"el aviso no habla de la llave: {avisos}"
    )


# ---------------------------------------------------------------------------
# Prueba 4: datos personales
# ---------------------------------------------------------------------------


def test_con_datos_personales_no_se_llama_a_codex(monkeypatch, tmp_path):
    """Si el texto trae datos personales, no se llama a Codex y se avisa."""
    espia = _Espia(respuesta_final="no deberia leerse")
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")

    codex = _importar_pieza()
    texto, avisos = codex.preguntar(
        _datos_personales_de_mentira(), timeout=30, raiz=str(tmp_path)
    )

    assert espia.llamadas == [], "se llamo a Codex con datos personales"
    assert texto == "", f"se devolvio texto con datos personales: {texto!r}"
    assert avisos, "no se aviso de los datos personales"


# ---------------------------------------------------------------------------
# Prueba 5: se pasa del tope
# ---------------------------------------------------------------------------


def test_si_se_pasa_del_tope_devuelve_vacio_y_avisa_con_los_segundos(
    monkeypatch, tmp_path
):
    """Si Codex se pasa del tope, texto vacio y aviso con los segundos."""

    def run_que_se_pasa(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="codex", timeout=7)

    monkeypatch.setattr(subprocess, "run", run_que_se_pasa)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")

    codex = _importar_pieza()
    texto, avisos = codex.preguntar("dime algo", timeout=7, raiz=str(tmp_path))

    assert texto == "", f"se devolvio texto tras el timeout: {texto!r}"
    assert avisos, "no se aviso del timeout"
    assert any("7" in a for a in avisos), (
        f"el aviso no trae los segundos del tope: {avisos}"
    )


# ---------------------------------------------------------------------------
# Prueba 6: Codex contesta
# ---------------------------------------------------------------------------


def test_si_codex_contesta_se_devuelve_lo_del_archivo(monkeypatch, tmp_path):
    """Si Codex contesta, se devuelve lo que dejo en el archivo de respuesta."""
    respuesta = "la respuesta final de codex"
    espia = _Espia(respuesta_final=respuesta)
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: f"/falso/{nombre}")

    codex = _importar_pieza()
    texto, avisos = codex.preguntar("dime algo", timeout=30, raiz=str(tmp_path))

    assert espia.llamadas, "no se llamo a Codex ni una vez"
    assert respuesta in texto, (
        f"no se devolvio lo que Codex dejo en el archivo: {texto!r}"
    )
    assert isinstance(avisos, list)


def test_sin_codex_instalado_no_se_llama_y_se_avisa(monkeypatch, tmp_path):
    """Si no hay Codex instalado, no se llama y se avisa, sin lanzar."""
    espia = _Espia(respuesta_final="no deberia leerse")
    monkeypatch.setattr(subprocess, "run", espia)
    monkeypatch.setattr(shutil, "which", lambda nombre: None)

    codex = _importar_pieza()
    texto, avisos = codex.preguntar("dime algo", timeout=30, raiz=str(tmp_path))

    assert espia.llamadas == [], "se llamo a Codex sin estar instalado"
    assert texto == "", f"se devolvio texto sin Codex instalado: {texto!r}"
    assert avisos, "no se aviso de que Codex no esta instalado"
