# -*- coding: utf-8 -*-
"""VIGIA — LAS CLAVES NO SE LEEN DESDE LA TERMINAL (seguridad 2026-08-24).

Julio, 2026-08-24: "lo de la variable de entorno... dime claramente que es y como lo reparamos."

EL PROBLEMA: las claves de pago (DeepSeek, Gemini, Groq) viven en las variables de entorno en
texto plano, y un agente podia leerlas con un comando (`echo $env:DEEPSEEK_API_KEY`) sin que nada
lo frenara. Si un mensaje pedia mostrar la clave, salia la real: acceso a la plata y a las cuentas.

LA REPARACION: `candado_terminal.py` ahora BLOQUEA leer variables de entorno (siempre, con o sin
paquete). Esta vigia comprueba que el candado MUERDE y que no estorba lo normal.
"""
import os
import sys
import json
import subprocess

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _correr_terminal(comando):
    p = subprocess.run(
        [sys.executable, os.path.join(AQUI, "arnes", "candado_terminal.py")],
        input=json.dumps({"tool_name": "Bash", "tool_input": {"command": comando}}),
        capture_output=True, text=True, timeout=60)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


def test_bloquea_leer_clave_desde_la_terminal():
    code, txt = _correr_terminal("echo $env:DEEPSEEK_API_KEY")
    assert code == 2, "dejo leer la clave con echo"
    assert "CLAVES" in txt.upper()


def test_bloquea_leer_clave_con_python():
    code, _ = _correr_terminal("python -c \"import os; print(os.environ['DEEPSEEK_API_KEY'])\"")
    assert code == 2, "dejo leer la clave con os.environ"


def test_bloquea_dump_entero_del_entorno():
    code, _ = _correr_terminal("Get-ChildItem env:")
    assert code == 2, "dejo volcar el entorno entero"


def test_no_estorba_los_comandos_normales():
    code, _ = _correr_terminal("git status")
    assert code == 0, "bloqueo un comando normal"


def test_el_env_esta_protegido_por_gitignore():
    git = open(os.path.join(AQUI, ".gitignore"), encoding="utf-8").read()
    assert ".env" in git, "el .env no esta protegido en gitignore"


def test_el_hueco_esta_tapado_en_el_candado():
    txt = open(os.path.join(AQUI, "arnes", "candado_terminal.py"), encoding="utf-8").read()
    assert "ENV_READER" in txt, "el candado de terminal no tiene el freno de claves"
    assert "os.environ" in txt or "printenv" in txt or "$env:" in txt
