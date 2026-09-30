"""LA PUERTA DEL PLAN (Julio, 2026-09-30).

Julio lo dijo asi: "lo unico que debe cambiar es que siempre se le debe decir los 4
que en el plan, pero yo solo apruebo aca, como trabajamos hasta ahora. Debes
asegurarte de la seguridad. Y una vez se termine de ejecutar el plan, me haces
siempre un resumen. Esta instruccion nunca debe depender de tu memoria: crea
programa."

Los cuatro son: QUE SE REPARA, COMO SE REPARA, DONDE SE REPARA y POR QUE SE REPARA.

Esta pieza exige las cuatro respuestas del plan. La aprobacion la da Julio en el
chat, como hasta ahora: NO se pide ni se teclea ninguna clave ni contrasena, y
esta pieza no pide ninguna palabra secreta a nadie. El resumen al terminar es
obligatorio: mientras una marca de plan aprobado siga sin resumen, no se puede
cerrar.

Esta pieza NO apaga ningun candado: solo dice si un plan puede arrancar y si se
puede cerrar. Ninguna de sus funciones lanza nunca: si revienta, el dia que se
enganche frenaria todo.
"""

import hashlib
import os
from datetime import datetime


LAS_CUATRO = (
    "QUE SE REPARA",
    "COMO SE REPARA",
    "DONDE SE REPARA",
    "POR QUE SE REPARA",
)

NOMBRE_DE_LA_MARCA = "PUERTA_DEL_PLAN_APROBACION.json"


def _es_texto(valor):
    """Verdadero solo si lo que llego es texto de verdad."""
    return isinstance(valor, str)


def _renglones_del_rotulo(texto_plan, rotulo):
    """Devuelve los pedazos que van detras de 'ROTULO:' en cada renglon donde
    aparece con sus dos puntos y con al menos TRES letras o numeros detras, en el
    mismo renglon. Se recogen TODOS, no solo el primero, en el orden en que salen.
    """
    pedazos = []
    if not _es_texto(texto_plan):
        return pedazos
    aguja = rotulo + ":"
    for renglon in texto_plan.splitlines():
        pos = renglon.find(aguja)
        if pos < 0:
            continue
        detras = renglon[pos + len(aguja):].strip()
        letras_o_numeros = sum(1 for c in detras if c.isalnum())
        if letras_o_numeros >= 3:
            pedazos.append(detras)
    return pedazos


def _rotulo_puesto(texto_plan, rotulo):
    """Un rotulo cuenta como PUESTO solo si aparece con sus dos puntos y detras,
    en el mismo renglon, hay al menos TRES letras o numeros."""
    return len(_renglones_del_rotulo(texto_plan, rotulo)) > 0


def lo_que_falta(texto_plan):
    """Devuelve una LISTA de frases, una por cada rotulo que falte, en el mismo
    orden de LAS_CUATRO. Lista vacia quiere decir que estan los cuatro.

    Cada frase mide mas de quince letras, trae dentro el rotulo que falta escrito
    tal cual, dice como escribirlo y trae dentro la palabra puerta_del_plan.

    Nunca revienta: si lo que llega no es texto (vacio, nada, un numero, una
    lista), devuelve los CUATRO.
    """
    if not _es_texto(texto_plan):
        return [
            "Falta el rotulo %s: escribelo en su propio renglon como '%s: ...' "
            "para que la puerta_del_plan lo vea." % (rotulo, rotulo)
            for rotulo in LAS_CUATRO
        ]
    faltan = []
    for rotulo in LAS_CUATRO:
        if not _rotulo_puesto(texto_plan, rotulo):
            faltan.append(
                "Falta el rotulo %s: escribelo en su propio renglon como "
                "'%s: ...' para que la puerta_del_plan lo vea." % (rotulo, rotulo)
            )
    return faltan


def numero_del_plan(texto_plan):
    """Devuelve un texto de DOCE letras o numeros que sale SOLO de las cuatro
    respuestas, nunca del resto del plan. Si falta cualquiera de las cuatro,
    devuelve texto vacio.

    Por cada rotulo se recogen TODOS los renglones donde aparece con sus dos puntos
    y con texto detras, en el orden en que aparecen. De cada uno se toma lo que va
    detras de los dos puntos, sin espacios en los extremos. Todo se junta en un
    solo texto, con el nombre del rotulo delante de cada pedazo y un separador
    entre pedazos, y de ese texto se saca una huella y se devuelven sus doce
    primeras letras. Asi, si se agrega un renglon nuevo con una de las cuatro
    respuestas, el numero CAMBIA.
    """
    if not _es_texto(texto_plan):
        return ""
    for rotulo in LAS_CUATRO:
        if not _rotulo_puesto(texto_plan, rotulo):
            return ""
    pedazos = []
    for rotulo in LAS_CUATRO:
        for detras in _renglones_del_rotulo(texto_plan, rotulo):
            pedazos.append("%s=%s" % (rotulo, detras))
    juntado = " | ".join(pedazos)
    huella = hashlib.sha256(juntado.encode("utf-8")).hexdigest()
    return huella[:12]


def _ruta_de_la_marca(raiz):
    return os.path.join(raiz, NOMBRE_DE_LA_MARCA)


def _leer_marca(raiz):
    """Devuelve el diccionario de la marca, o None si no se puede leer."""
    try:
        import json
        ruta = _ruta_de_la_marca(raiz)
        if not os.path.exists(ruta):
            return None
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        if isinstance(datos, dict):
            return datos
        return None
    except Exception:
        return None


def aprobar(texto_plan, raiz):
    """Si falta alguna de las cuatro, devuelve un diccionario con la clave
    '_error' y una frase que nombra a puerta_del_plan, y NO escribe nada.

    Si estan las cuatro, escribe la marca de aprobacion DENTRO de la carpeta raiz
    que se le pasa y devuelve un diccionario con la clave 'ok' y el numero del plan
    dentro. La marca es un archivo con nombre fijo dentro de esa carpeta, con el
    numero, la fecha y la hora, y un sitio para el resumen que empieza vacio. Si la
    carpeta no existe, se crea.
    """
    try:
        faltan = lo_que_falta(texto_plan)
        if faltan:
            return {
                "_error": "la puerta_del_plan no deja aprobar: faltan respuestas del "
                "plan (%s)" % "; ".join(faltan)
            }
        numero = numero_del_plan(texto_plan)
        if not numero:
            return {
                "_error": "la puerta_del_plan no deja aprobar: no se pudo sacar el "
                "numero del plan"
            }
        import json
        if not os.path.isdir(raiz):
            os.makedirs(raiz, exist_ok=True)
        marca = {
            "numero": numero,
            "fecha": datetime.now().isoformat(timespec="seconds"),
            "resumen": "",
        }
        with open(_ruta_de_la_marca(raiz), "w", encoding="utf-8") as f:
            json.dump(marca, f, ensure_ascii=False, indent=2)
        return {"ok": numero}
    except Exception as e:
        return {
            "_error": "la puerta_del_plan no pudo aprobar: %s" % e
        }


def puede_arrancar(texto_plan, raiz):
    """Devuelve DOS cosas: primero si se puede arrancar (verdadero o falso) y
    despues el motivo en palabras simples.

    Los tres casos en que dice falso, y en los tres el motivo trae dentro la
    palabra puerta_del_plan:
      - falta alguna de las cuatro: el motivo dice cuales faltan;
      - estan las cuatro pero no hay marca de aprobacion: el motivo dice que falta
        la APROBACION de Julio, y trae dentro la palabra aprobacion;
      - hay marca pero su numero no coincide con el del texto que llega: el motivo
        dice que el plan CAMBIO despues de aprobado, y trae dentro la palabra
        cambio.

    Dice verdadero solo cuando estan las cuatro y el numero de la marca coincide.
    Nunca revienta: si la carpeta no existe o la marca esta rota, contesta falso
    con su motivo.
    """
    try:
        faltan = lo_que_falta(texto_plan)
        if faltan:
            return False, (
                "la puerta_del_plan no deja arrancar: faltan respuestas del plan "
                "(%s)" % "; ".join(faltan)
            )
        numero = numero_del_plan(texto_plan)
        if not numero:
            return False, (
                "la puerta_del_plan no deja arrancar: no se pudo sacar el numero "
                "del plan"
            )
        marca = _leer_marca(raiz)
        if marca is None:
            return False, (
                "la puerta_del_plan no deja arrancar: falta la aprobacion de Julio "
                "en el chat (no hay marca de aprobacion)"
            )
        if marca.get("numero") != numero:
            return False, (
                "la puerta_del_plan no deja arrancar: el plan cambio despues de "
                "aprobado (el numero de la marca no coincide)"
            )
        return True, "la puerta_del_plan deja arrancar: estan las cuatro y la "
        "aprobacion coincide"
    except Exception as e:
        return False, (
            "la puerta_del_plan no deja arrancar: no se pudo comprobar (%s)" % e
        )


def anotar_resumen(numero, texto, raiz):
    """Apunta ese resumen en la marca de ese numero y devuelve verdadero si lo
    pudo apuntar. Devuelve falso si no hay marca con ese numero, o si el resumen
    llega vacio. Nunca revienta.
    """
    try:
        if not _es_texto(texto) or not texto.strip():
            return False
        if not _es_texto(numero) or not numero:
            return False
        marca = _leer_marca(raiz)
        if marca is None:
            return False
        if marca.get("numero") != numero:
            return False
        import json
        marca["resumen"] = texto
        with open(_ruta_de_la_marca(raiz), "w", encoding="utf-8") as f:
            json.dump(marca, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def puede_cerrar(raiz):
    """Devuelve DOS cosas: si se puede cerrar y el motivo.

    Dice falso mientras exista una marca de plan aprobado cuyo resumen siga vacio,
    y el motivo trae dentro la palabra puerta_del_plan y dice que falta el resumen.
    Dice verdadero si no hay marca, o si la marca ya tiene su resumen apuntado.

    Nunca revienta: si no se puede leer la marca, deja cerrar avisando en el motivo,
    porque un candado que se rompe no puede dejar el trabajo atrapado sin salida.
    """
    try:
        ruta = _ruta_de_la_marca(raiz)
        if not os.path.exists(ruta):
            return True, "la puerta_del_plan deja cerrar: no hay marca de plan "
            "aprobado"
        marca = _leer_marca(raiz)
        if marca is None:
            return True, (
                "la puerta_del_plan deja cerrar: no se pudo leer la marca, y un "
                "candado roto no puede dejar el trabajo atrapado"
            )
        resumen = marca.get("resumen", "")
        if not _es_texto(resumen) or not resumen.strip():
            return False, (
                "la puerta_del_plan no deja cerrar: falta el resumen del plan "
                "aprobado"
            )
        return True, "la puerta_del_plan deja cerrar: el resumen ya esta apuntado"
    except Exception as e:
        return True, (
            "la puerta_del_plan deja cerrar: no se pudo comprobar la marca (%s), y "
            "un candado roto no puede dejar el trabajo atrapado" % e
        )


if __name__ == "__main__":
    print(__doc__)
