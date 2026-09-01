# -*- coding: utf-8 -*-
"""CANDADO — NO SE LE MANDA TRABAJO AL REEMPLAZO POR COSTUMBRE.

Ley: CONTRATO_EL_COMPANERO.md (Julio, 2026-08-31):
  "De ahora en adelante todo es con continue"
  "solo si se bloquea continue, solo si eso pasa, o falla, no responde como es, trabajas
   nuevamente con cline"

POR QUE FRENA Y NO SOLO AVISA: ya paso con el equipo. La regla estaba escrita en la memoria y en
el protocolo, y aun asi Julio tuvo que repetirla TRES veces, porque dependia de que la IA se
acordara. Lo unico que se cumple es lo que frena.

Y aqui el olvido cuesta doble: se le manda el trabajo al de siempre por costumbre, el companero
nuevo no se estrena nunca, y encima parece que se avanzo.

COMO SE ABRE, DE FORMA HONRADA (esto es a proposito): se declara que el activo no pudo, con el
motivo, y entonces se puede acudir al reemplazo durante un rato. Un candado sin salida honrada
empuja a saltarselo, y eso es peor que no tenerlo.
"""
import datetime
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REGISTRO = os.path.join(AQUI, "memoria", "DECISIONES_COMPANERO.log")

MENSAJE = (
    "\nFRENADO — EL COMPANERO DE AHORA ES {activo}, NO {otro}\n\n"
    "  Le estabas mandando trabajo a {otro}, que quedo de REEMPLAZO.\n"
    "  Por que: {por_que}\n\n"
    "  Julio lo dijo asi: todo es con {activo}, y a {otro} se acude SOLO si {activo} se bloquea,\n"
    "  falla o no responde como es. Y aun asi, dejando dicho el motivo.\n\n"
    "  Si de verdad {activo} no puede, se declara y entonces se abre:\n"
    "     python -c \"import sys;sys.path.insert(0,'arnes');import companero;"
    "companero.declarar_que_no_pudo('{activo}','<el motivo>')\"\n\n"
    "  La ley: CONTRATO_EL_COMPANERO.md\n")


def _apuntar(a_quien, motivo):
    """La libreta al reves: queda constancia de cada frenada."""
    try:
        os.makedirs(os.path.dirname(REGISTRO), exist_ok=True)
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write("%s | FRENADO | hacia %s | %s\n"
                    % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), a_quien, motivo))
    except Exception:
        pass


# Palabras de MANDAR. Sin una de estas cerca, nombrar a alguien no es mandarle trabajo.
VERBOS_DE_MANDAR = ("enviar(", "enviar (", "canal.enviar", "asignar(", "reparto.asignar",
                    "encargo para", "tarea para", "le mando", "mandarle", "pidele",
                    "que lo haga", "que se encargue")


def _a_quien_le_habla(texto, nombres):
    """El primer nombre al que de verdad se le esta MANDANDO algo. No basta con nombrarlo.

    OJO, cazado el 2026-08-31: al principio bastaba con que el nombre apareciera, y este mismo
    candado freno la escritura de la PRUEBA que comprueba que ese esta retirado. Nombrar a
    alguien no es darle trabajo. Un candado que grita en falso se acaba apagando, y entonces
    no protege nada.
    """
    llano = (texto or "").lower()
    if not any(v in llano for v in VERBOS_DE_MANDAR):
        return ""                          # no se le esta mandando nada a nadie
    for n in nombres:
        if not n:
            continue
        for forma in ("'%s'" % n, '"%s"' % n, " %s " % n, "para %s" % n, "a %s" % n):
            if forma in llano:
                return n
    return ""


def main():
    try:
        import autorizacion
        if autorizacion.autorizada():
            return 0                       # la llave de Julio manda
    except Exception:
        pass

    crudo = sys.stdin.read()
    if not (crudo or "").strip():
        return 0                           # no hay peticion: nada que vigilar
    try:
        data = json.loads(crudo)
    except Exception:
        # NO SE ABRE ANTE EL FALLO. Hay peticion pero no se entiende: se frena y se dice.
        sys.stderr.write("\nFRENADO — no se pudo entender la peticion, y un candado no se abre\n"
                         "  cuando algo va mal. Vuelve a intentarlo.\n")
        _apuntar("(ilegible)", "no se pudo leer la peticion")
        return 2

    try:
        import companero
    except Exception:
        return 0                           # sin la pieza no hay nada que comparar: no se estorba

    dentro = data.get("tool_input") or {}

    # EL PROPIO ARNES SE PUEDE TOCAR SIEMPRE, igual que en los candados hermanos. Si no, este
    # mismo candado impide RETIRAR a alguien (el texto nombra al retirado) y no habria forma de
    # cumplir una orden de Julio. Cazado el 2026-08-31: freno el retiro de cline que el pidio,
    # y para arreglarlo habia que tocarlo a el, que tambien se frenaba. Un candado que se muerde
    # la cola acaba apagado.
    ruta = str(dentro.get("file_path") or "").replace("\\", "/").lower()
    if "/arnes/" in ruta or "/vigias/" in ruta:
        return 0

    texto = " ".join(str(dentro.get(k) or "") for k in ("command", "content", "new_string"))
    if not texto.strip():
        return 0

    # PRIMERO LOS RETIRADOS: a esos no se les manda trabajo NUNCA, ni aunque el activo falle.
    # Julio: "No uses mas a cline, no lo uses". El retiro no tiene salida honrada; la reserva si.
    try:
        nombres_retirados = [str(r.get("quien", "")).lower() for r in companero.retirados()]
    except Exception:
        nombres_retirados = []
    retirado = _a_quien_le_habla(texto, nombres_retirados)
    if retirado:
        por_que = ""
        try:
            por_que = companero.por_que_retirado(retirado)
        except Exception:
            pass
        _apuntar(retirado, "esta RETIRADO: no se le manda trabajo nunca")
        sys.stderr.write(
            "\nFRENADO — %s ESTA RETIRADO, NO SE LE MANDA TRABAJO\n\n"
            "  Julio lo retiro: %s\n\n"
            "  Esto NO tiene salida: un retirado no vuelve porque el de ahora falle. Si el\n"
            "  companero de ahora (%s) no puede, se le dice a Julio; no se acude al retirado.\n\n"
            "  La ley: CONTRATO_EL_COMPANERO.md\n"
            % (retirado, por_que or "lo mando Julio", companero.activo() or "(nadie)"))
        try:
            import candados_medicion
            candados_medicion.cazado("companero")
        except Exception:
            pass
        return 2

    nombres_reemplazo = [str(r.get("quien", "")).lower() for r in companero.reservas()]
    a_quien = _a_quien_le_habla(texto, nombres_reemplazo)
    if not a_quien:
        return 0                           # no se le habla a ningun reemplazo: adelante

    if companero.puede_acudir_a_la_reserva():
        return 0                           # consta que el activo no pudo: esta permitido

    activo = companero.activo() or "(nadie)"
    por_que = companero.por_que_reserva(a_quien) or "lo mando Julio"
    _apuntar(a_quien, "el companero de ahora es %s y no consta que no pudiera" % activo)
    sys.stderr.write(MENSAJE.format(activo=activo, otro=a_quien, por_que=por_que))
    try:
        import candados_medicion
        candados_medicion.cazado("companero")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
