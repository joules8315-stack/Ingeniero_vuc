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


# LOS CUADERNOS que los propios candados escriben cada vez que actuan (Julio, 2026-08-31).
# El guardián NO los cuenta como "trabajo sin guardar": se ensucian solos al comprobar, y eso
# es lo que Julio ve como "me pide permiso a cada rato". Solo se ignora ESTO, no el trabajo real.
CUADERNOS_BASE = {
    "guardia.log", "candados_medicion.json", "sin_equipo.log", "diagnostico.json",
    ".veredicto_equipo.json", ".commit_bloqueos", ".protocolo_bloqueos",
    ".avisos_ya_dados.json", ".supervisor_bloqueos", ".comunicacion_bloqueos",
    ".cierres_bloqueados", ".lecturas_sueltas", ".pasado_corriendo", "apagones.log",
    "lo_que_julio_ya_dijo.json", "decisiones_por_nombre.log", "reparto_ia.json",
    "significados.json", ".objetivo_confirmado", ".vigias_corriendo",
    # el cuaderno del candado del companero, creado el 2026-08-31: se olvido anadirlo aqui
    # y por eso el guardian seguia gritando por una libreta que escribia el mismo.
    "decisiones_companero.log",
    # 2026-09-02 (Claude: "el guardian que se muerde la cola"): los candados que se anadieron
    # despues dejaban sus propios apuntes dentro de memoria y el guardian volvia a pedir guardar
    # a cada rato. Son cuadernos de los candados, NO trabajo de Julio: se ignoran igual que los
    # de arriba, pero se quedan en el disco (el rastro que Julio mira sigue ahi).
    "balance.log", "gasto.log", "gasto.json", "trabajos_del_equipo.log",
    "decisiones_candado.log", "aplicaciones.log", "ultimo_trabajo_del_equipo.json",
}


def _es_cuaderno(ruta):
    """True si `ruta` es un cuaderno que escriben los propios candados, no trabajo de verdad.

    El guardián los ignora para no gritar por lo que el mismo ensucia. Pero SOLO estos: el codigo,
    las leyes, las vigias y los paquetes indexados son trabajo de verdad y siguen gritando.
    """
    base = os.path.basename(ruta).lower()
    if base in CUADERNOS_BASE:
        return True
    n = ruta.replace("\\", "/").lower()
    # el canal (mensajes AI-AI), las pruebas reales y los apuntes de llamadas tambien los escriben
    # los candados; no son trabajo que Julio pida guardar, y ensucian en cada corrida.
    return ("/canal/" in n or "/pruebas_real/" in n or "/.git/" in n)


def _cambios_sin_commit():
    """True si hay archivos modificados sin commitear (trabajo que se puede perder).

    NO cuentan los cuadernos que escriben los propios candados (Julio, 2026-08-31): se ensucian
    solos al comprobar y harian gritar al guardián siempre. Solo el trabajo de verdad.
    """
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=AQUI,
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            return False
        for linea in r.stdout.splitlines():
            if not linea or len(linea) < 4:
                continue
            ruta = linea[3:].strip()          # el camino, sin el estado (XX + espacio)
            if not ruta:
                continue
            if _es_cuaderno(ruta):
                continue                       # cuaderno del candado, no trabajo de verdad
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
        candados_medicion.cazado("commit")
    except Exception:
        pass
    sys.stderr.write(
        "NO SE PUEDE TERMINAR — F8 (punto i): hay trabajo sin commitear (se puede perder).\n"
        "  Guárdalo ahora y vuelve a terminar.\n"
        "     git add -A; git commit -m \"<que se hizo>\"\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
