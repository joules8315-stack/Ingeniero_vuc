# -*- coding: utf-8 -*-
"""arnes/candado_equipo.py — NO SE ESCRIBE CODIGO A SOLAS. SIEMPRE EL EQUIPO.

Julio, 2026-08-21, despues de tener que repetirlo otra vez:
  "pon candado de modo que siempre tengas que trabajar con equipo, y vigias para el arnes, que
   te frene cuando no lo hagas."
  "pon candado para que siempre actues con equipo, modo ingeniero y economico, sin excusa."
  "por no trabajar en equipo ya has gastado 19."

EL AGUJERO QUE TAPA: la regla estaba escrita, en la memoria y en el protocolo, y aun asi se
escribio a solas un guardia entero, tres vigias y cuatro reparaciones. Escrito no es cumplido.
Julio lo pago de su bolsillo. Una regla que depende de que yo me acuerde NO es una regla.

LO QUE EXIGE: para tocar CODIGO tiene que haber un veredicto del equipo RECIENTE que cubra ese
archivo. Uno genera, OTRO distinto audita (4 ojos: nadie se aprueba a si mismo).

  cd C:\\Ingeniero_VUC; python ingeniero.py equipo <proyecto> "<la tarea>"

LO QUE NO ESTORBA (o el candado se vuelve un muro y se acaba apagando, que es peor):
  · los documentos .md          — escribir la ley no es programar
  · archivo nuevo que no existe — crear no es reescribir
  · el propio arnes             — si el candado se rompe, hay que poder arreglarlo

FORTALECIDO (Julio, 2026-08-21): ya NO se deja pasar cuando no hay cerebros. Antes, si los
cerebros estaban agotados, se podia escribir a solas (quedaba apuntado en SIN_EQUIPO.log) y eso
dejaba a foto_informe y a cualquier proyecto SIN VIGILAR. Ahora SIEMPRE se exige el veredicto del
equipo para tocar codigo; si no hay, se BLOQUEA y Julio decide si aprueba. No se escribe a solas,
jamas, en ningun proyecto.

LA LIBRETA, AL REVES (Julio, 2026-08-21): antes se apuntaba lo que se COLABA sin equipo. Con la
puerta de escape cerrada ya no se cuela nada, asi que esa libreta se quedaria vacia para siempre
y no serviria de nada (medido: el archivo no llego a existir NUNCA). Ahora se apunta lo
contrario: CADA VEZ QUE EL CANDADO FRENA. Queda el dia, la hora, el archivo y por que se freno.
Asi Julio ve al final de la semana cuantas veces hubo que pararse y por que, en vez de creerselo.

INVIOLABLE no es que no haya salida: es que TODO deje rastro. La salida a mano sigue siendo suya
(INGENIERO_OFF) y hay una vigia que comprueba que nunca se la quiten.
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))  # para importar autorizacion.py (Julio, 2026-08-24)

VEREDICTO = os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
SIN_EQUIPO = os.path.join(AQUI, "memoria", "SIN_EQUIPO.log")
VIGENCIA_MIN = 90          # un veredicto vale hora y media: lo que dura una tanda de trabajo
CODIGO = (".py", ".js", ".html", ".ts", ".jsx", ".tsx", ".css", ".sql")


def _ruta_veredicto():
    return os.environ.get("INGENIERO_VEREDICTO_TEST") or VEREDICTO


def _ruta_sin_equipo():
    return os.environ.get("INGENIERO_SIN_EQUIPO_TEST") or SIN_EQUIPO


def guardar_veredicto(tarea, archivos, obrero, auditor, veredicto):
    """Lo llama `ingeniero.py equipo` cuando el equipo termina. Es la llave."""
    d = {"cuando": time.time(), "tarea": tarea, "archivos": list(archivos or []),
         "obrero": obrero, "auditor": auditor, "veredicto": veredicto}
    os.makedirs(os.path.dirname(_ruta_veredicto()), exist_ok=True)
    json.dump(d, open(_ruta_veredicto(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d


def veredicto_vigente():
    """El veredicto del equipo si sigue fresco, o None."""
    try:
        d = json.load(open(_ruta_veredicto(), encoding="utf-8"))
    except Exception:
        return None
    if (time.time() - float(d.get("cuando", 0))) > VIGENCIA_MIN * 60:
        return None
    return d


def cubre(d, fp):
    """¿El veredicto habla de ESTE archivo? Un veredicto sobre otra cosa no vale de llave."""
    if not d:
        return False
    base = os.path.basename(fp).lower()
    for a in d.get("archivos", []):
        if os.path.basename(str(a)).lower() == base:
            return True
    return False


def _hay_cerebros():
    try:
        from cuerpo import obrero
        return bool(obrero.quienes_hay())
    except Exception:
        return False


def _apuntar_frenada(fp, por_que):
    """La libreta AL REVES (Julio, 2026-08-21): se apunta cada vez que el candado FRENA.

    Antes se apuntaba lo que se colaba sin equipo; con la puerta de escape cerrada eso ya no
    pasa nunca y la libreta quedaba vacia. Lo util ahora es lo contrario: que Julio pueda ver
    cuantas veces hubo que pararse y por que.

    A prueba de fallos a proposito: si la libreta no se puede escribir, el candado NO se cae.
    Frenar es lo importante; apuntarlo es la prueba, pero no puede tumbar al guardia.
    """
    try:
        os.makedirs(os.path.dirname(_ruta_sin_equipo()), exist_ok=True)
        with open(_ruta_sin_equipo(), "a", encoding="utf-8") as f:
            f.write("%s  %s  (%s)\n" % (time.strftime("%Y-%m-%d %H:%M"), fp[:120], por_que))
    except Exception:
        pass


MENSAJE = (
    "BLOQUEADO: NO SE ESCRIBE CODIGO A SOLAS\n\n"
    "  {fp}\n\n"
    "  Julio tuvo que repetirlo tres veces y le costo dinero. Uno GENERA, otro distinto AUDITA;\n"
    "  yo dirijo y leo el veredicto. Escribirlo yo mismo gasta lo caro para hacer lo barato.\n\n"
    "  Que hacer:\n"
    "     cd C:\\Ingeniero_VUC; python ingeniero.py equipo <proyecto> \"<la tarea>\"\n\n"
    "  Eso deja el veredicto, y con el veredicto este archivo se abre. Los documentos .md,\n"
    "  los archivos nuevos y el propio arnes se pueden tocar siempre.\n")


def main():
    import autorizacion
    # Solo Julio apaga, por comando (autorizar-off) y con autorizacion escrita: candados abiertos.
    if autorizacion.autorizada():
        return 0
    # El interruptor viejo INGENIERO_OFF ya NO basta para apagar: sin autorizacion de Julio,
    # se deja constancia y se sigue bloqueando (Julio, 2026-08-24).
    if os.environ.get("INGENIERO_OFF", "").strip():
        _apuntar_frenada("(INGENIERO_OFF)", "interruptor encendido sin autorizacion previa de Julio")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = str((data.get("tool_input") or {}).get("file_path") or "")
    if not fp:
        return 0
    if os.path.splitext(fp)[1].lower() not in CODIGO:
        return 0                                    # documentos: libres
    if not os.path.exists(fp):
        return 0                                    # crear no es reescribir
    rel = fp.replace("\\", "/").lower()
    if "/arnes/" in rel:
        return 0                                    # hay que poder arreglar el propio candado
    # FORTALECIDO (Julio, 2026-08-21): ya NO se deja pasar sin veredicto aunque no haya cerebros.
    # Antes se escapaba por aqui y dejaba a foto_informe y a cualquier proyecto SIN VIGILAR.
    # Ahora SIEMPRE se exige el veredicto del equipo; si no hay, se BLOQUEA y Julio decide.
    d = veredicto_vigente()
    if cubre(d, fp):
        return 0                                    # el equipo ya lo miro: adelante
    # SIN PUERTA (Julio, 2026-08-26): la salida de emergencia NECESITO_EDITAR / permiso_editar
    # se volvio la ENTRADA PRINCIPAL — todas las IA se salieron por ahi y trabajaron a solas,
    # que es justo lo que este candado existe para impedir. Se quito de raiz. El UNICO que
    # autoriza tocar codigo a solas es Julio (autorizacion), o el veredicto del equipo.
    # Si un archivo grande no cabe en el paquete, la cura NO es una llave: es arreglar el
    # repartidor (diccionario/router) para que el veredicto SI nombre el archivo.
    # LA LIBRETA, AL REVES: queda constancia de CADA frenada, con el motivo exacto.
    _apuntar_frenada(fp, "sin veredicto del equipo" if not d else
                     "el veredicto vigente no habla de este archivo")
    sys.stderr.write(MENSAJE.format(fp=fp))
    # MEDICION (Julio, 2026-08-25): este candado cazo algo real: freno escribir a solas.
    try:
        import candados_medicion
        candados_medicion.cazado("equipo")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
