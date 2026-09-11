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


def hay_trabajo_del_copista(minutos=90):
    """El copista aplico un cambio hace poco y salio BIEN?

    JULIO, 2026-09-11: "Que el copista cuente, esa es mi decision."

    POR QUE NACE: dos leyes suyas se estaban pisando y dejaban el cierre sin salida honrada.
    Una dice que LA FOTOCOPIA NO SE PAGA (si el cambio ya viene decidido al detalle lo aplica
    el copista, gratis, porque llamar al equipo es pagar por una fotocopiadora). La otra dice
    que SIN VEREDICTO DEL EQUIPO NO SE CIERRA. Se cumplian las dos por separado y aun asi no
    se podia terminar. Julio decidio que el trabajo del copista CUENTA.

    POR QUE ES SEGURO DESDE HOY: el revisor del arnes ya trae la cuenta 5 (2026-09-11), asi que
    una aplicacion que se lleve por delante alguna pieza se frena y se dice con nombre. Antes
    de eso, dejar pasar al copista a ciegas si habria sido un riesgo.

    NO ES UN SELLO DE GOMA. Solo abre si la aplicacion es RECIENTE y salio BIEN, y NO cuenta lo
    que aplican las pruebas en carpetas temporales: si contara, bastaria con correr los
    guardianes para abrirse la puerta a si mismo, que es exactamente el verde de mentira que
    esta casa lleva meses cazando.

    ES UNA CUENTA, NO UN JUICIO: se lee la libreta y se mira la fecha. NUNCA lanza.
    """
    import datetime
    ruta = (os.environ.get("INGENIERO_APLICACIONES")
            or os.path.join(AQUI, "memoria", "APLICACIONES.log"))
    try:
        with open(ruta, encoding="utf-8", errors="replace") as f:
            lineas = f.readlines()[-300:]
    except Exception:
        return False
    limite = datetime.datetime.now() - datetime.timedelta(minutes=minutos)
    for linea in reversed(lineas):
        partes = [p.strip() for p in linea.split("|")]
        if len(partes) < 3 or partes[1] != "OK":
            continue
        sitio = partes[2].lower()
        if "temp" in sitio or "tmp" in sitio:
            continue
        try:
            cuando = datetime.datetime.fromisoformat(partes[0])
        except Exception:
            continue
        if cuando >= limite:
            return True
    return False


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
    # 1) EQUIPO: hay veredicto vigente? Solo si se toco codigo hace poco.
    try:
        from candado_cierre import _toco_codigo
        if _toco_codigo(90):
            try:
                import candado_equipo as _ce
                # JULIO 2026-09-11: "Que el copista cuente, esa es mi decision." El veredicto
                # del equipo O el trabajo del copista. Cualquiera de los dos vale: con el
                # segundo se cumple la ley de que la fotocopia no se paga.
                if not _ce.veredicto_vigente() and not hay_trabajo_del_copista(90):
                    faltas.append("1) EQUIPO: no hay veredicto del equipo vigente. Para tocar codigo SIEMPRE se "
                                  "usa el equipo:\n     cd C:\\Ingeniero_VUC; python ingeniero.py equipo <proyecto> \"<tarea>\"")
            except Exception:
                pass
    except Exception:
        # Si no se puede saber si se toco codigo, se exige el veredicto igual.
        try:
            import candado_equipo as _ce
            # Mismo criterio que arriba: vale el veredicto del equipo O el trabajo del copista.
            if not _ce.veredicto_vigente() and not hay_trabajo_del_copista(90):
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
