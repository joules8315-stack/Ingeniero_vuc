# -*- coding: utf-8 -*-
"""arnes/candado_commit.py — F8 (punto i): COMMIT SIEMPRE, nada se pierde.

Julio, 2026-08-24 (punto i): "Debe quedar siempre guardado el trabajo, haciendo commit, sin
excusas, no se debe perder nunca el trabajo, ni ninguna instrucción que yo dé."

Este candado (hook Stop) avisa/bloquea si se tocó código y NO se hizo commit: para que el trabajo no
quede sin guardar. El guardado lo hace git (con la guardia de guardado); aquí solo se recuerda y se
exige. Anti-bucle y salida por autorizacion, para no encerrar a Julio.
"""
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTADOR = os.path.join(AQUI, "memoria", ".commit_bloqueos")
TOPE_BLOQUEOS = 2


def _contador():
    return os.environ.get("INGENIERO_COMMIT_CONTADOR") or CONTADOR


def _veces_seguidas():
    try:
        cuando, n = open(_contador(), encoding="utf-8").read().split("|")
        if time.time() - float(cuando) > 600:
            return 0
        return int(n)
    except Exception:
        return 0


def _apuntar(n):
    os.makedirs(os.path.dirname(_contador()), exist_ok=True)
    open(_contador(), "w", encoding="utf-8").write("%f|%d" % (time.time(), n))


def _cambios_sin_commit():
    """True si hay archivos modificados sin commitear (trabajo que se puede perder)."""
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=AQUI,
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            return False
        for linea in r.stdout.splitlines():
            estado = linea[:2].strip()
            if estado and not linea.endswith("GUARDIA.log") and "memoria/" not in linea:
                return True
        return False
    except Exception:
        return False


def main():
    import autorizacion
    if autorizacion.autorizada():
        return 0
    if not _cambios_sin_commit():
        _apuntar(0)
        return 0
    veces = _veces_seguidas()
    if veces >= TOPE_BLOQUEOS:
        _apuntar(0)
        sys.stderr.write("AVISO (commit, ya no bloquea): hay trabajo sin commitear. Guárdalo pronto.\n")
        return 0
    _apuntar(veces + 1)
    # MEDICION DE CANDADOS (Claude, 2026-08-25): apuntar lo que este candado cazo de verdad
    # (bloquear trabajo sin commitear = evito que se pierda). Para que la revision de los 8 dias
    # no vea una tabla de ceros.
    try:
        import candados_medicion
        candados_medicion.apuntar("commit", "cazo")
    except Exception:
        pass
    sys.stderr.write(
        "NO SE PUEDE TERMINAR — F8 (punto i): hay trabajo sin commitear (se puede perder).\n"
        "  Guárdalo ahora y vuelve a terminar.\n"
        "     git add -A; git commit -m \"<que se hizo>\"\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
