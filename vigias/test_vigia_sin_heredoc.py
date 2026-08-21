# -*- coding: utf-8 -*-
"""VIGIA 26 — NO SE ESCRIBE CODIGO DESDE LA TERMINAL (Julio, 2026-08-21).

  "por que mierdas sigues usando heredoc, si siempre te dana el proceso, o por lo menos eso veo;
   si no te sirve desechala y busca otra, a menos que no sea un fallo recurrente, sino esporadico."

ES RECURRENTE: SIETE veces. La ultima, ese mismo dia, partiendo en dos una vigia recien escrita.

QUE PASA EXACTAMENTE: la terminal se come las barras invertidas antes de que el texto llegue al
archivo. Un \\n escrito para que quede literal se convierte en un salto de linea de verdad, y una
linea de codigo queda partida por la mitad. **No avisa de nada**: el archivo queda roto y con
buena pinta, y el fallo aparece mucho despues, en otro sitio, pareciendo otra cosa.

Estaba apuntado en la memoria con aviso y aun asi se repitio, porque un aviso se puede ignorar.
Por eso deja de ser un aviso y pasa a ser un candado.

SE CAZA POR LO QUE HACE, NO POR EL NOMBRE (regla de Julio): da igual que sea heredoc, echo,
printf o lo que se invente; si mete texto con barras invertidas dentro de un archivo, se frena.
"""
import json
import os
import subprocess
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _correr(cmd, herramienta="Bash"):
    r = subprocess.run(
        [sys.executable, os.path.join(AQUI, "arnes", "candado_terminal.py")],
        input=json.dumps({"tool_name": herramienta, "tool_input": {"command": cmd}}),
        capture_output=True, text=True, cwd=AQUI)
    return r.returncode, (r.stderr or "")


# ─── FRENA LO QUE ROMPE ───────────────────────────────────────────────────────
def test_frena_el_heredoc_con_barras():
    """EL CASO REAL: esto es lo que partio la vigia en dos."""
    code, err = _correr("cat > x.py <<'PY'\nprint('a\\nb')\nPY")
    assert code == 2, "deja escribir codigo con barras desde la terminal: eso rompe archivos"
    assert "terminal" in err.lower()


def test_frena_el_replace_con_barras():
    """La otra forma con la que se rompio: un replace con \\n dentro de un heredoc."""
    code, _ = _correr("python - <<'EOF'\ns = s.replace('a\\n', 'b')\nEOF")
    assert code == 2


def test_frena_aunque_cambie_de_herramienta():
    """Por lo que HACE, no por el nombre: echo y printf rompen igual."""
    for cmd in ("echo 'linea1\\nlinea2' > salida.py",
                "printf 'a\\nb' > cosa.js"):
        code, _ = _correr(cmd)
        assert code == 2, "se colo por otra puerta: %s" % cmd


def test_tambien_en_powershell():
    code, _ = _correr("echo 'a\\nb' > x.py", herramienta="PowerShell")
    assert code == 2, "la misma rendija abierta en la otra terminal"


def test_el_aviso_dice_que_hacer_en_su_lugar():
    _, err = _correr("cat > x.py <<'PY'\nprint('a\\nb')\nPY")
    assert "herramienta de escribir" in err or "editar" in err, \
        "frena pero no dice la alternativa, y entonces se acaba apagando"


# ─── NO ESTORBA ───────────────────────────────────────────────────────────────
def test_deja_pasar_lo_que_no_rompe():
    """Un candado que frena de mas se acaba apagando, y eso es peor que no tenerlo."""
    for cmd in ("python -m pytest -q vigias/",
                "git status",
                "python ingeniero.py equipo ingeniero \"algo\"",
                "cat > notas.py <<'PY'\nprint(1)\nPY"):
        code, _ = _correr(cmd)
        assert code == 0, "estorba: frena algo que no rompe nada: %s" % cmd


def test_tiene_interruptor_de_emergencia():
    txt = open(os.path.join(AQUI, "arnes", "candado_terminal.py"), encoding="utf-8").read()
    assert "INGENIERO_OFF" in txt
