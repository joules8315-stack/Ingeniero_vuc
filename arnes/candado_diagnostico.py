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


def _conclusion_se_pasa(alcance, evidencia, sintoma):
    """¿La medida dice una PARTE y la conclusion describe el TODO?

    Patron medido 3 veces en 2 dias (Claude, 2026-08-26): '11 de 23 informes limpios, 1-2 celdas
    sueltas' y aun asi se concluyo 'todos rotos' o 'tus 22 informes rotos'. Medida correcta,
    conclusion equivocada. Nadie preguntaba si la explicacion se sostiene.
    Aviso, no candado: no frena, pero obliga a mirarlo (como la coincidencia de 'cambio').
    """
    a = str(alcance or "").lower()
    if not a:
        return False
    # el alcance dice una PARTE: N de M con N<M, o palabras de parte.
    m = re.search(r"(\d+)\s*de\s*(\d+)", a)
    parcial = bool(m and int(m.group(1)) < int(m.group(2)))
    if not parcial and not any(w in a for w in ("algun", "unos", "un par", "pocos", "una parte")):
        return False
    texto = " ".join([str(evidencia or ""), str(sintoma or "")]).lower()
    absoluto = any(w in texto for w in
                   ("todos los", "todas las", "todos", "todas", "todo el", "todo lo", "nada",
                    "ningun", "ninguna", "ninguno", "entero", "completo", "100%", "siempre",
                    "nunca"))
    return absoluto


def declarar(proyecto, archivo, funcion, linea, evidencia, cambio, sintoma="", alcance=""):
    """Guarda la causa raiz. Exige las seis cosas, MAS dos preguntas de criterio.

    `cambio` responde "¿qué cambió entre la medición de antes y la de después?" y debe nombrar UNA
    cosa (si enumera varias, es una coincidencia).
    `alcance` responde "¿cuántos de cuántos?" (p. ej. '1 de 23 informes') para que la conclusion
    sea PROPORCIONAL a la medida. Si la medida dice una parte y se describe el todo, se avisa:
    la conclusion no se sostiene (medida correcta, conclusion equivocada).

    Ambos son AVISO, no candado: no frenan, pero hay que verlos antes de reparar.
    """
    faltan = [n for n, v in (("archivo", archivo), ("funcion", funcion),
                             ("linea", linea), ("evidencia", evidencia),
                             ("cambio", cambio), ("alcance", alcance)) if not v]
    if faltan:
        return {"_error": "falta declarar: " + ", ".join(faltan) +
                          ". Sin eso es INFERIDO, y lo inferido no se repara."}
    d = {"cuando": time.time(), "proyecto": proyecto, "archivo": archivo, "funcion": funcion,
         "linea": str(linea), "evidencia": evidencia, "cambio": cambio, "sintoma": sintoma,
         "alcance": alcance}
    avisos = []
    if _es_coincidencia(cambio):
        d["coincidencia"] = True
        avisos.append("'cambio' nombra mas de una cosa: no es aislar la causa, es una "
                      "coincidencia. Aisla UNA sola cosa.")
    if _conclusion_se_pasa(alcance, evidencia, sintoma):
        d["se_pasa"] = True
        avisos.append("tu conclusion se pasa de tu medida: el alcance dice '%s' pero describes "
                      "el todo como afectado. O se ajusta la conclusion, o se mide de nuevo."
                      % str(alcance)[:80])
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(d, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    _cosechar_para_el_diccionario(proyecto, sintoma, archivo, funcion, linea)
    if avisos:
        return {**d, "_aviso": "OJO: " + " | ".join(avisos)}
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
            "  archivo  : %s\n  funcion  : %s\n  linea    : %s\n  evidencia: %s\n  cambio   : %s\n"
            "  alcance  : %s"
            % (d["proyecto"],
               "  [OJO: aisla UNA cosa]" if d.get("coincidencia") else "",
               d["archivo"], d["funcion"], d["linea"], d["evidencia"][:160],
               str(d.get("cambio"))[:160], str(d.get("alcance"))[:160]))


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
        "--funcion <nombre> --linea <n> --evidencia \"lo que mediste\" --cambio \"que cambio\" "
        "--alcance \"cuantos de cuantos\"\n"
        % os.path.basename(fp))
    return 2


if __name__ == "__main__":
    sys.exit(main())
