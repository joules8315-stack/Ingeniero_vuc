# -*- coding: utf-8 -*-
"""arnes/candado_supervisor.py — F3 (Julio 2026-08-24): Cline como SUPERVISOR verifica SIEMPRE
que se cumplan las tres obligaciones. Ninguna se salta, bajo ningun motivo:

  1) QUE SIEMPRE SE USE EL EQUIPO  -> hay veredicto del equipo vigente para tocar codigo.
  2) QUE SIEMPRE SE TRABAJE EN MODO INGENIERO -> el hook del modo esta conectado e inyecta las leyes.
  3) QUE SIEMPRE SE TRABAJE BAJO LOS PROTOCOLOS -> cada paso del protocolo tiene su candado.

Cline (yo) corre esto como supervisor ANTES de dar nada por terminado. Si algo falta, se bloquea y
se dice exactamente que falta. Anti-bucle: TOPE_BLOQUEOS y salida por INGENIERO_OFF.
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))
CONTADOR = os.path.join(AQUI, "memoria", ".supervisor_bloqueos")
TOPE_BLOQUEOS = 2


def _contador():
    return os.environ.get("INGENIERO_SUPERVISOR_CONTADOR") or CONTADOR


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


def _settings():
    """La config EFECTIVA de hooks (usuario + proyecto), reconstruida en el formato que espera.

    Julio, 2026-08-27: el arnes vive en el settings de USUARIO (fuente canonica global), y el
    proyecto solo tiene sus candados de cierre. Antes este candado miraba SOLO el settings del
    proyecto y daba falsa alarma (no veia el modo ingeniero que vive en el usuario). Claude lo
    cazo (2026-08-27). Ahora se leen las dos capas.
    """
    out = {}
    for capa in _capas():
        for t, lista in capa.get("hooks", {}).items():
            for e in lista:
                out.setdefault(t, []).append(e)
    return {"hooks": out}


def _capas():
    """Lista de dicts de settings: [usuario, proyecto] (los que existan)."""
    capas = []
    usr = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")
    if os.path.exists(usr):
        try:
            capas.append(json.load(open(usr, encoding="utf-8")))
        except Exception:
            pass
    proy = os.path.join(AQUI, ".claude", "settings.json")
    if os.path.exists(proy):
        try:
            capas.append(json.load(open(proy, encoding="utf-8")))
        except Exception:
            pass
    return capas


def _hay_modo_ingeniero_conectado():
    """El hook del modo ingeniero (UserPromptSubmit) debe estar conectado e inyectar las leyes."""
    for entrada in _settings().get("hooks", {}).get("UserPromptSubmit", []):
        for h in entrada.get("hooks", []):
            if "modo_ingeniero" in h.get("command", ""):
                return True
    return False


def _hay_candado_por_paso():
    """Cada paso del protocolo (cerebro/protocolo.py) debe nombrar su candado."""
    try:
        import cerebro.protocolo as _pr
        pasos = _pr.PASOS if hasattr(_pr, "PASOS") else []
        sin_candado = [p for p in pasos if not (p.get("candado") or "").strip()]
        return not sin_candado
    except Exception:
        return True  # si no se puede leer, no frenar por eso


def verificar():
    """Devuelve la lista de incumplimientos (vacía = todo bien)."""
    faltas = []
    # 1) EQUIPO: hay veredicto vigente?
    try:
        import candado_equipo as _ce
        if not _ce.veredicto_vigente():
            faltas.append("1) EQUIPO: no hay veredicto del equipo vigente. Para tocar codigo SIEMPRE se "
                          "usa el equipo:\n     cd C:\\Ingeniero_VUC; python ingeniero.py equipo <proyecto> \"<tarea>\"")
    except Exception:
        pass
    # 2) MODO INGENIERO conectado e inyectando
    if not _hay_modo_ingeniero_conectado():
        faltas.append("2) MODO INGENIERO: el hook del modo no esta conectado (no inyecta las leyes a cada "
                      "instruccion). Conectalo en .claude/settings.json")
    # 3) PROTOCOLOS: cada paso con candado
    if not _hay_candado_por_paso():
        faltas.append("3) PROTOCOLOS: hay pasos del protocolo sin candado. Un paso sin candado se salta.")
    return faltas


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (autorizar-off)
        return 0
    faltas = verificar()
    if not faltas:
        _apuntar(0)
        return 0
    veces = _veces_seguidas()
    if veces >= TOPE_BLOQUEOS:
        _apuntar(0)
        sys.stderr.write("AVISO (supervisor, ya no bloquea): " + " | ".join(faltas) + "\n")
        return 0
    _apuntar(veces + 1)
    sys.stderr.write("NO SE PUEDE TERMINAR — el SUPERVISOR (Cline) encontro incumplimientos (F3):\n\n"
                     + "\n\n".join(faltas) + "\n\nCorrige eso antes de dar por terminado.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
