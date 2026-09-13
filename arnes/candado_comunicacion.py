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
# EL NOMBRE DEL COMPANERO NO SE ESCRIBE A MANO: SE LE PREGUNTA A QUIEN LO SABE.
#
# FALLO CAZADO POR JULIO EL 2026-09-12, y es la TERCERA vez que esta misma enfermedad muerde en
# esta casa. Sus palabras, enfadado y con razon:
#
#     "Ojo, le estas mandando cosas a cline, NO ES A BP, de opencode."
#
# Esta lista decia cline, y obligaba a la direccion a mandarle recados a alguien que ya no
# trabaja, mientras el companero de verdad esperaba en su propio canal. Un recado al que no
# trabaja no es comunicacion: es ruido que ademas da la sensacion de haber avisado.
#
# YA HABIA PASADO IGUAL el 2026-08-31 con el candado del buzon, y la cura quedo escrita entonces:
# "que pregunte por el companero activo a arnes/companero.py, que es el UNICO sitio donde vive esa
# respuesta; no se escribe a mano el nombre del companero dentro de una pieza".
#
# Y ES LA MISMA ENFERMEDAD que perdia 7 de cada 10 ordenes de Julio (una lista de palabras de
# mando escrita a mano) y que la fila de cerebros ordenada a mano. Lo que hay que saber SE LE
# PREGUNTA A QUIEN LO SABE; lo que se congela dentro del codigo envejece en silencio.
#
# ESTO NO DEPENDE DE NINGUNA VARIABLE QUE NADIE PONE, que es el otro fallo ya pagado aqui: le
# pregunta a la pieza, y si esa pieza no contesta, se queda con los de siempre. Cae del lado
# seguro: pedir de mas es ruido, pedir de menos es no avisar a nadie.
def _companero_de_ahora():
    """Quien es HOY el companero. Se lo pregunta a la pieza que lo sabe, nunca se adivina."""
    try:
        import companero
        activo = (companero.activo() or "").strip()
        if activo:
            return activo
    except Exception:
        pass
    return "cline"          # ultimo recurso: mejor pedir uno que no pedir ninguno


DESTINOS = tuple(dict.fromkeys((_companero_de_ahora(), "cline", "4ojos", "deepseek")))


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
        # UN RECADO CONTESTADO YA NO ESTA PENDIENTE, AUNQUE NADIE LO HAYA MARCADO.
        #
        # FALLO CAZADO EL 2026-09-12: la marca "respondido" NO LA PONIA NADIE NUNCA. Ni el canal
        # al enviar, ni ninguna pieza. Asi que un recado se quedaba pendiente PARA SIEMPRE, y el
        # cierre se bloqueaba una y otra vez aunque ya se hubiera contestado tres veces. Julio lo
        # sufrio en directo: "otra vez marcando el puto fallo, REPARALO".
        #
        # Y PEOR: un recado firmado como desconocido no tenia a quien contestarle, asi que era
        # imposible de cerrar por definicion. Una trampa, no un guardian.
        #
        # NO SE ARREGLA CON UNA MARCA QUE ALGUIEN TENGA QUE PONER: asi murio el contador de
        # repeticiones de Julio. Se DEDUCE de lo que ya quedo escrito solo: si esta IA le escribio
        # por el canal a quien mando el recado DESPUES de recibirlo, esta contestado. Y si el
        # recado no trae firma, vale haberle escrito al companero de ahora, que es el unico a
        # quien se puede contestar.
        _de = str(m.get("de", "") or "").strip()
        _a_quien = _de if _de and _de.lower() not in ("?", "desconocido") else _companero_de_ahora()
        if _a_quien and _a_quien != quien and _escribio_a(quien, _a_quien):
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
        # SE CONTESTA A QUIEN ESCRIBIO, NO A UN NOMBRE ESCRITO A MANO.
        #
        # JULIO LO REPITIO, y con razon: "repara que no se envie mas recados a cline, sino a bp,
        # cuantas veces lo tengo que repetir?". Cada repeticion suya es un fallo de esta casa.
        #
        # Este aviso hacia algo absurdo: ENSENABA el nombre de quien habia escrito el recado, y a
        # renglon seguido mandaba contestarle A OTRO, porque el nombre estaba clavado a mano.
        # Resultado: los recados se le mandaban a quien ya no trabaja, mientras el companero de
        # verdad esperaba en su canal. Y ademas daba la sensacion de haber avisado.
        #
        # Es la MISMA enfermedad que perdia 7 de cada 10 ordenes de Julio, que hundia al mejor
        # cerebro en la fila, y que buscaba una funcion por un numero de renglon: algo que hay que
        # SABER, congelado dentro del codigo en vez de preguntarselo a quien lo sabe. Aqui el que
        # lo sabe es el propio recado: lo firma su remitente, y de ahi se saca el nombre.
        _quienes = []
        for _m in pend[:4]:
            _de = str(_m.get("de", "") or "").strip()
            if _de and _de.lower() not in ("?", "desconocido") and _de not in _quienes:
                _quienes.append(_de)
        if not _quienes:
            _quienes = [_companero_de_ahora()]
        faltas.append("Tienes recados en el canal SIN responder (F4):\n"
                      + "\n".join("   - de %s: %s" % (m.get("de", "?"), m.get("texto", "")[:120])
                                  for m in pend[:4])
                      + "\n   Contestale a QUIEN TE ESCRIBIO, antes de terminar:\n"
                      + "\n".join("     python arnes/canal.py enviar %s \"<tu respuesta>\"" % q
                                  for q in _quienes))
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
