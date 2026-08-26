#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_memoria.py — EL FALLO TE AVISA ANTES, NO DESPUES.

Julio, 2026-08-21: "Verifica que se esten guardando los errores y que estes aprendiendo de ellos,
no veo que te llegue ningun paquete recordandote el error... otra vez estas confiando de tu
memoria y es justo lo que debemos combatir."

LO QUE DESCUBRIO: habia 29 fallos guardados y NINGUNO avisaba jamas. La memoria de fallos solo se
consultaba al pedir un paquete, y solo si las palabras del problema coincidian. Pero hay fallos
que no son "un problema con nombre" sino **una accion**: escribir codigo desde la terminal, por
ejemplo. Ese no coincidia con nada, y por eso se repitio SEIS veces en un dia.

LA PRUEBA MAS CLARA: el apunte de ese fallo decia
    "NO VOLVER A: meter codigo con \\n o rutas con \\a dentro de un heredoc"
y **el propio apunte estaba corrompido por el mismo fallo que describia.**

LA REGLA: guardar un fallo no es aprender. Aprender es que el fallo te FRENE la proxima vez.
Por eso cada fallo puede declarar un DISPARADOR: la accion que lo revive. Antes de cada accion
se mira si hay algun fallo con ese disparador, y si lo hay, se recuerda ANTES de cometerlo.

No estorba: solo avisa de lo que viene al caso (si avisa de todo, se vuelve ruido y se ignora),
y siempre dice QUE HACER en su lugar, no solo que esta mal.
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

# Libreta chica y aparte: SOLO recuerda "de esto ya te avise hace un momento".
# NO toca la memoria de errores de verdad (leccion ya vivida: ninguna comprobacion escribe
# encima de la memoria real).
AVISADOS = os.path.join(AQUI, "memoria", ".avisos_ya_dados.json")
DURA_MIN = 20


def _ahora():
    return datetime.now().timestamp()


def _leer_avisados():
    try:
        with open(AVISADOS, encoding="utf-8-sig") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _ya_avisado(huella):
    """¿Se enseño ESTA leccion para ESTA misma accion hace poco?"""
    try:
        cuando = _leer_avisados().get(huella)
        return bool(cuando) and (_ahora() - float(cuando)) < DURA_MIN * 60
    except Exception:
        return False


def _apuntar_aviso(huella):
    """Deja constancia de que se enseño.

    Si NO se puede escribir, no queda constancia y la proxima vez se vuelve a frenar. Este
    candado, cuando algo le falla, se cierra; nunca se abre.
    """
    try:
        dados = _leer_avisados()
        ahora = _ahora()
        dados = {k: v for k, v in dados.items()
                 if isinstance(v, (int, float)) and ahora - float(v) < DURA_MIN * 60}
        dados[huella] = ahora
        os.makedirs(os.path.dirname(AVISADOS), exist_ok=True)
        with open(AVISADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f)
    except Exception:
        pass


def _texto_de_la_accion(data):
    """Que se va a hacer, en texto, para poder compararlo con los disparadores."""
    herr = str(data.get("tool_name") or "")
    ti = data.get("tool_input") or {}
    partes = [herr]
    for clave in ("command", "file_path", "old_string", "new_string", "content",
                  "pattern", "path", "prompt"):
        v = ti.get(clave)
        if isinstance(v, str):
            partes.append(v[:2000])
    return "\n".join(partes)


def _proyecto_que_nombra(texto):
    """El apodo de proyecto que esta por trabajar/consultar en esta accion, o None."""
    m = re.search(r"\b(?:trabaja|equipo|trabajar)\s+([A-Za-z0-9_\.\-]+)", texto, re.I)
    return m.group(1) if m else None


def _en_libreta(nombre):
    """¿El nombre es un apodo de la libreta de direcciones (proyectos.config)?"""
    try:
        from cerebro import grafo
        return str(nombre).lower() in {a.lower() for a in grafo.proyectos()}
    except Exception:
        return False


def revisar(texto):
    """Los fallos ya vividos que esta accion puede revivir."""
    try:
        from cuerpo import fallos
        guardados = fallos._leer()
    except Exception:
        return []
    salen = []
    for f in guardados:
        disp = (f.get("disparador") or "").strip()
        if not disp:
            continue
        try:
            if not re.search(disp, texto, re.I | re.S):
                continue
        except re.error:
            continue
        # AVISOS QUE MIRAN EL PELIGRO, NO EL COMANDO (fallo 45, 2026-08-21):
        # un aviso no debe sonar por el NOMBRE del comando sino por el riesgo real.
        # Este aviso es 'trabajar en un proyecto cuyo nombre NO esta en la libreta':
        # si el proyecto que se nombra SI existe, el peligro de este fallo no aplica.
        if f.get("mira_proyecto"):
            nombre = _proyecto_que_nombra(texto)
            if not nombre or _en_libreta(nombre):
                continue
        salen.append(f)
    return salen[:3]


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (comando autorizar-off)
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    texto = _texto_de_la_accion(data)
    if not texto:
        return 0
    revividos = revisar(texto)
    if not revividos:
        return 0

    partes = ["ESTO YA TE PASO. No lo repitas:", ""]
    for f in revividos:
        veces = f.get("veces", 1)
        cuantas = (" (te ha pasado %d veces)" % veces) if veces > 1 else ""
        partes.append("  * %s%s" % (f["que_paso"][:130], cuantas))
        partes.append("    por que paso : %s" % f["causa_raiz"][:130])
        partes.append("    HAZLO ASI    : %s" % f["cura"][:150])
        partes.append("    NO VUELVAS A : %s" % f["no_volver_a"][:130])
        partes.append("")
    partes.append("  Guardar un fallo no es aprender. Esto es el aviso ANTES de cometerlo otra vez.")

    # AVISAR NO ES TAPIAR (Julio, 2026-08-24, tras perder una tarde entera contra esto).
    #
    # QUE PASABA: este freno paraba SIEMPRE, y para siempre. Una leccion cuyo disparador era el
    # nombre de los dos comandos con los que se pide el material y se llama al equipo dejo
    # tapiado el protocolo ENTERO. Otra, cuyo disparador era el nombre de un archivo roto,
    # impedia repararlo: el recuerdo del fallo impedia arreglar el fallo. Y una tercera freno
    # esta misma reparacion. Es el fallo ya apuntado: "escribir un candado sin una forma honrada
    # de satisfacerlo". Un freno del que no se puede salir no protege: paraliza.
    #
    # QUE HACE AHORA: la PRIMERA vez frena y ensena la leccion, que es lo que Julio pidio — ver
    # el fallo ANTES de cometerlo. Si se insiste con la MISMA accion, se deja pasar: la leccion
    # ya se leyo, y seguir es entonces una decision tomada a sabiendas, no un descuido.
    # No se afloja nada: sigue siendo IMPOSIBLE actuar sin haber visto el aviso primero.
    huella = hashlib.sha1(
        ("|".join(sorted(str(f.get("id", "")) for f in revividos)) + "::" + texto
         ).encode("utf-8", "replace")).hexdigest()

    if _ya_avisado(huella):
        partes.append("")
        partes.append("  (De esto ya te avise hace un momento y vuelves a intentarlo: PASA.")
        partes.append("   Insistir despues de leer el aviso es una decision, no un descuido.)")
        sys.stderr.write("\n".join(partes) + "\n")
        return 0

    _apuntar_aviso(huella)
    partes.append("")
    partes.append("  Si aun asi hay que hacerlo, repite la MISMA accion y pasara.")
    sys.stderr.write("\n".join(partes) + "\n")
    # MEDICION (Julio, 2026-08-25): freno y ensene una leccion ya vivida antes de repetirla.
    try:
        import candados_medicion
        candados_medicion.cazado("memoria")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
