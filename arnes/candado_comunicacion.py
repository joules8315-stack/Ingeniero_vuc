# -*- coding: utf-8 -*-
"""arnes/candado_comunicacion.py — F4 (Julio 2026-08-24): Claude se comunica SIEMPRE con Cline y DeepSeek.

Julio, 2026-08-24: "crea todo para que la comunicacion entre Claude y tu (Cline) sea fluida, sin
vacilaciones, sin opciones. Claude se debe comunicar siempre con tigo y con deepseek, en primera
instancia, y para hacer cualquier cosa que le mande a realizar."

El CANAL (canal.py) deja mensajes en disco pero era PASIVO y NO estaba conectado: Claude nunca veia
lo que Cline/DeepSeek le dejaban. Este candado (hook Stop) hace que:
  · si hay mensajes en el canal PARA ESTA IA sin responder, NO se puede terminar sin contestarlos.
  · exige comunicacion con Cline y DeepSeek: si hizo trabajo y no escribio por el canal a
    'cline'/'4ojos' ni a 'deepseek', se bloquea y se le dice que se comunique.

Anti-bucle (como todos los candados): TOPE_BLOQUEOS seguidos y salida por INGENIERO_OFF, para que
ningun candado encierre a Julio.
"""
import glob
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANDEJA = os.path.join(AQUI, "memoria", "canal")
CONTADOR = os.path.join(AQUI, "memoria", ".comunicacion_bloqueos")
TOPE_BLOQUEOS = 2
DESTINOS = ("cline", "4ojos", "deepseek")


def _quien():
    return (os.environ.get("INGENIERO_QUIEN", "") or "desconocido").strip()


def _bandeja():
    return os.environ.get("INGENIERO_CANAL_TEST") or BANDEJA


def _ruta_contador():
    return os.environ.get("INGENIERO_COMUNICACION_CONTADOR") or CONTADOR


def _veces_seguidas():
    try:
        cuando, n = open(_ruta_contador(), encoding="utf-8").read().split("|")
        if time.time() - float(cuando) > 600:
            return 0
        return int(n)
    except Exception:
        return 0


def _apuntar(n):
    os.makedirs(os.path.dirname(_ruta_contador()), exist_ok=True)
    open(_ruta_contador(), "w", encoding="utf-8").write("%f|%d" % (time.time(), n))


def mensajes_pendientes(quien):
    """Mensajes del canal dirigidos a esta IA (o a todos) SIN responder."""
    out = []
    if not os.path.isdir(BANDEJA):
        return out
    for ruta in sorted(glob.glob(os.path.join(BANDEJA, "*.json"))):
        try:
            m = json.load(open(ruta, encoding="utf-8"))
        except Exception:
            continue
        destino = str(m.get("para", "")).strip()
        if destino not in (quien, "*", "todos", "todas"):
            continue
        if m.get("respondido"):
            continue
        out.append(m)
    return out


def _escribio_a(quien, destino, minutos=90):
    """¿Esta IA envio un mensaje a `destino` por el canal hace poco?"""
    limite = time.time() - minutos * 60
    if not os.path.isdir(BANDEJA):
        return False
    for ruta in glob.glob(os.path.join(BANDEJA, "*.json")):
        try:
            m = json.load(open(ruta, encoding="utf-8"))
            ts = os.path.getmtime(ruta)
        except Exception:
            continue
        if m.get("de") == quien and str(m.get("para", "")).strip() in (destino, "*", "todos"):
            if ts > limite:
                return True
    return False


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (autorizar-off)
        return 0
    qu = _quien()
    pend = mensajes_pendientes(qu)
    faltas = []
    if pend:
        faltas.append("Tienes mensajes de Cline/DeepSeek en el canal SIN responder (F4):\n"
                      + "\n".join("   - de %s: %s" % (m.get("de", "?"), m.get("texto", "")[:120])
                                  for m in pend[:4])
                      + "\n   Responde por el canal antes de terminar:\n"
                        "     cd C:\\Ingeniero_VUC; python arnes/canal.py enviar cline \"<tu respuesta>\"")
    # Comunicacion obligatoria con el companero activo y DeepSeek (Julio 2026-08-24): si hizo trabajo y no
    # escribio por el canal al companero actual ni a deepseek, se le exige.
    try:
        import companero
        companero_activo = companero.activo()
    except Exception:
        companero_activo = "cline"  # respaldo: lista de ahora
    if qu in ("claude",) and not (_escribio_a(qu, companero_activo) or _escribio_a(qu, "4ojos")) and not _escribio_a(qu, "deepseek"):
        faltas.append("F4: Claude debe comunicarse SIEMPRE con " + companero_activo + " y con DeepSeek, en primera\n"
                      "   instancia, para cualquier cosa. No escribiste por el canal. Hazlo:\n"
                      "     cd C:\\Ingeniero_VUC; python arnes/canal.py enviar " + companero_activo + " \"<estado>\"\n"
                      "     cd C:\\Ingeniero_VUC; python arnes/canal.py enviar deepseek \"<encargo>\"")
    if not faltas:
        _apuntar(0)
        return 0
    veces = _veces_seguidas()
    if veces >= TOPE_BLOQUEOS:
        _apuntar(0)
        sys.stderr.write("AVISO (comunicacion, ya no bloquea mas): " + " | ".join(faltas) + "\n")
        return 0
    _apuntar(veces + 1)
    sys.stderr.write("NO SE PUEDE TERMINAR — candado de comunicacion (F4):\n\n" + "\n\n".join(faltas)
                     + "\n\nHazlo y vuelve a terminar.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
