#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_diagnostico.py — LO INFERIDO NO SE REPARA.

Del PROTOCOLO_MVP.md § 6 (DIAGNOSTICO), palabras de Julio ya escritas hace tiempo:

  "Se repara a quien VIOLA el contrato, no a quien sufre la violacion. Compensar aguas abajo lo
   que otro rompio aguas arriba = PROHIBIDO.
   Causa declarada exige: archivo, funcion, linea, flujo reproducido, evidencia, relacion probada
   con el sintoma. Sin eso = INFERIDO, y lo inferido NO SE REPARA."

POR QUE EXISTE ESTE CANDADO: el 2026-08-20 se iba a INDEXAR el MVP entero como si eso fuera la
reparacion, **sin saber siquiera donde estaba lento**. Julio lo paro en seco: "¿Porque vas a
indexar, ya sabes si es lo que se necesita? ¿Sabes donde es lento el MVP?". La regla estaba
escrita desde antes y no la frenaba nadie.

COMO FUNCIONA: antes de tocar codigo de un proyecto hay que haber DECLARADO la causa raiz:

    python ingeniero.py causa <proyecto> --archivo <ruta> --funcion <nombre> --linea <n> \\
        --evidencia "lo que se midio o se vio, no lo que se supone"

Sin esa declaracion, o si esta rancia (mas de 8 horas), no se toca nada.
No estorba a los documentos ni a las pruebas: solo al codigo.
"""
import json, os, re, sys, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "DIAGNOSTICO.json")
VIGENCIA_HORAS = 8
CODIGO = (".py", ".html", ".js", ".css", ".ts", ".jsx", ".tsx")


def _es_coincidencia(cambio):
    """La causa no aisló UNA cosa: enumera varias (separadores de listas / "y").

    Pregunta de criterio (Claude, 2026-08-25): al declarar una causa hay que responder
    "¿qué cambió entre la medición de antes y la de después?" Si son DOS o más cosas, eso no es
    aislar, es una coincidencia. Es un AVISO, no un candado: no frena, pero obliga a mirarlo.
    """
    c = (cambio or "").lower()
    return any(p in c for p in (",", ";", "+", " y ", " y ademas ", " y tambien ",
                                " ademas ", " ademas de ", " y despues "))


def declarar(proyecto, archivo, funcion, linea, evidencia, cambio, sintoma=""):
    """Guarda la causa raiz. Exige las cinco cosas, MAS la PREGUNTA DE CRITERIO: 'cambio'.

    `cambio` responde "¿qué cambió entre la medición de antes y la de después?" y debe nombrar UNA
    cosa. Si enumera varias, no es aislar: es una coincidencia, y se devuelve un `_aviso` (no
    bloquea, pero hay que verlo antes de reparar).
    """
    faltan = [n for n, v in (("archivo", archivo), ("funcion", funcion),
                             ("linea", linea), ("evidencia", evidencia),
                             ("cambio", cambio)) if not v]
    if faltan:
        return {"_error": "falta declarar: " + ", ".join(faltan) +
                          ". Sin eso es INFERIDO, y lo inferido no se repara."}
    d = {"cuando": time.time(), "proyecto": proyecto, "archivo": archivo, "funcion": funcion,
         "linea": str(linea), "evidencia": evidencia, "cambio": cambio, "sintoma": sintoma}
    if _es_coincidencia(cambio):
        d["coincidencia"] = True
        os.makedirs(os.path.dirname(RUTA), exist_ok=True)
        json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return {**d, "_aviso": ("OJO: 'cambio' nombra mas de una cosa. Eso no es aislar la causa: "
                                "es una coincidencia. Aisla UNA sola cosa, o la reparacion prueba "
                                "de mas y por eso puede fallar.")}
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    _cosechar_para_el_diccionario(proyecto, sintoma, archivo, funcion, linea)
    return d


def _cosechar_para_el_diccionario(proyecto, sintoma, archivo, funcion, linea):
    """Aqui, y solo aqui, existen ya las DOS mitades probadas: lo que dijo Julio y el sitio exacto.

    Se aprovecha para llenar el diccionario que traduce sus palabras al codigo. Se cosecha del
    trabajo; no hay que sentarse a escribirlo, y por eso se llena de verdad. Un diccionario que
    hay que llenar a mano no se llena.

    De donde sale el problema en palabras de Julio: `sintoma` si se declaro, y si no, lo que el
    dijo y quedo apuntado en el ESTADO. Nunca se inventa: si no hay ninguno de los dos, no se
    guarda nada.

    Si algo falla aqui, NO pasa nada: declarar la causa ya quedo hecho arriba. Cosechar no puede
    tumbar el trabajo ya hecho (leccion del 2026-08-25: primero se guarda, despues lo demas).
    """
    try:
        import diccionario
        dicho = str(sintoma or "").strip()
        if not dicho:
            try:
                from cuerpo import estado
                dicho = str((estado.leer() or {}).get("problema") or "").strip()
            except Exception:
                dicho = ""
        if dicho:
            diccionario.aprender(dicho, archivo, funcion, linea, proyecto)
    except Exception:
        pass


def vigente():
    try:
        d = json.load(open(RUTA, encoding="utf-8"))
    except Exception:
        return None
    if time.time() - float(d.get("cuando", 0)) > VIGENCIA_HORAS * 3600:
        return None
    return d


def texto():
    d = vigente()
    if not d:
        return ("CAUSA RAIZ: no hay ninguna declarada (o esta rancia).\n"
                "  Sin causa raiz probada no se toca codigo: lo inferido no se repara.")
    return ("CAUSA RAIZ DECLARADA (%s)%s\n"
            "  archivo  : %s\n  funcion  : %s\n  linea    : %s\n  evidencia: %s\n  cambio   : %s"
            % (d["proyecto"], "  [OJO: coincidencia, aisla UNA cosa]" if d.get("coincidencia") else "",
               d["archivo"], d["funcion"], d["linea"], d["evidencia"][:160], str(d.get("cambio"))[:160]))


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (comando autorizar-off)
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = str((data.get("tool_input") or {}).get("file_path") or "")
    if not fp or not os.path.exists(fp):
        return 0                       # crear algo nuevo no es reparar
    if os.path.splitext(fp)[1].lower() not in CODIGO:
        return 0                       # documentos y contratos: libres
    rel = fp.replace("\\", "/").lower()
    if "/vigias/" in rel or os.path.basename(fp).startswith("test_"):
        return 0                       # las pruebas se escriben ANTES de reparar

    # ¿es de un proyecto declarado?
    try:
        sys.path.insert(0, AQUI)
        from cerebro import grafo
        de_proyecto = any(
            os.path.normcase(os.path.abspath(fp)).startswith(
                os.path.normcase(os.path.abspath(d["ruta"])) + os.sep)
            for d in grafo.proyectos().values())
    except Exception:
        de_proyecto = False
    if not de_proyecto:
        return 0

    if vigente():
        return 0

    sys.stderr.write(
        "BLOQUEADO: VAS A REPARAR SIN HABER PROBADO LA CAUSA\n"
        "  Archivo: %s\n\n"
        "  Regla de Julio, escrita desde hace tiempo:\n"
        "    'Causa declarada exige archivo, funcion, linea, flujo reproducido y evidencia.\n"
        "     Sin eso = INFERIDO, y lo inferido NO SE REPARA.'\n"
        "    'Se repara a quien VIOLA el contrato, no a quien sufre la violacion.'\n\n"
        "  Primero localiza y MIDE el fallo. Cuando lo tengas probado, declaralo:\n"
        "     cd C:\\Ingeniero_VUC; python ingeniero.py causa <proyecto> --archivo <ruta> "
        "--funcion <nombre> --linea <n> --evidencia \"lo que mediste o viste\"\n"
        % os.path.basename(fp))
    return 2


if __name__ == "__main__":
    sys.exit(main())
