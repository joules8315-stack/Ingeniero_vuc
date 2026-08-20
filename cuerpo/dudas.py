# -*- coding: utf-8 -*-
"""cuerpo/dudas.py — BUSCAR PRIMERO, PREGUNTAR DESPUES (Ley 16, Julio 2026-08-20).

  "No me puedes entender al 100%, pero si puedes hacer preguntas que te lleven a esa
   comprension. Legisla que siempre las hagas, pero que primero busque en los repositorios
   la respuesta; solo cuando no la halle, pregunte. Siempre debe hacerlas, aun mas si pierde
   el contexto."

EL ORDEN IMPORTA, y este es:
  1. LOS CONTRATOS      — ¿ya esta legislado? Es la ley: si lo dice, no se pregunta.
  2. LA MEMORIA DE FALLOS — ¿ya tropezamos aqui? Lo aprendido vale mas que una opinion nueva.
  3. EL CODIGO          — ¿lo responde una pieza que ya existe? (grafo + trozos)
  4. EL ESTADO          — ¿lo decidimos hace un rato y se me olvido?
  5. Y SOLO ENTONCES    — se le pregunta a Julio, en palabras simples.

POR QUE: preguntar sin haber buscado le hace perder el tiempo a Julio y rompe su ley madre
("nunca asumas, consulta los documentos primero y si no resuelven, SIEMPRE pregunta").
Pero callarse una duda es peor: ahi es donde se asume, y asumir es lo que rompe cosas.

La pregunta que sale de aqui se apunta en el ESTADO, y el `arnes/candado_cierre.py` NO DEJA
TERMINAR el turno mientras siga sin hacerse. Asi la pregunta no se pierde ni "se olvida".
"""
import os, sys, re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)


def _en_contratos(duda, proyecto=None, k=3):
    """1) ¿Lo dice ya la ley? Los contratos mandan sobre cualquier opinion."""
    from cerebro import grafo, trozos as _t
    hallados = []
    apodos = [proyecto] if proyecto else list(grafo.proyectos())
    for apodo in apodos:
        try:
            g = grafo.cargar(apodo)
        except Exception:
            continue
        leyes = [p for p in g["piezas"] if p["rol"] in ("CONTRATO", "MATRIZ", "PROTOCOLO")]
        if not leyes:
            continue
        try:
            b = _t.Buscador(leyes)
        except Exception:
            continue
        for r in b.buscar_estricto(duda, k=2, minimo=5.0):
            hallados.append({"donde": f"{apodo} :: {r['direccion']}",
                             "texto": r["texto"][:600], "puntaje": r["puntaje"],
                             "fuente": "CONTRATO"})
    return sorted(hallados, key=lambda x: -x["puntaje"])[:k]


def _en_fallos(duda, proyecto=None):
    """2) ¿Ya tropezamos con esta piedra?"""
    from cuerpo import fallos
    out = []
    for f in fallos.parecidos(duda, proyecto or "", k=2):
        out.append({"donde": f"memoria de fallos ({f['fecha']})",
                    "texto": f"{f['que_paso']}\n  causa: {f['causa_raiz']}\n  "
                             f"NO VOLVER A: {f['no_volver_a']}",
                    "puntaje": 5.0, "fuente": "FALLO YA VIVIDO"})
    return out


def _en_codigo(duda, proyecto=None, k=3):
    """3) ¿Lo responde una pieza que ya existe?"""
    from cerebro import grafo, trozos as _t
    hallados = []
    apodos = [proyecto] if proyecto else list(grafo.proyectos())
    for apodo in apodos:
        try:
            g = grafo.cargar(apodo)
        except Exception:
            continue
        codigo = [p for p in g["piezas"] if p["rol"] in ("CUERPO", "CODIGO", "CEREBRO", "WEB")]
        if not codigo:
            continue
        try:
            b = _t.Buscador(codigo)
        except Exception:
            continue
        for r in b.buscar_estricto(duda, k=2, minimo=6.0):
            hallados.append({"donde": f"{apodo} :: {r['direccion']}",
                             "texto": r["texto"][:600], "puntaje": r["puntaje"],
                             "fuente": "CODIGO"})
    return sorted(hallados, key=lambda x: -x["puntaje"])[:k]


def _en_el_estado(duda):
    """4) ¿Lo decidimos hace un rato? (pasa mas de lo que parece tras perder contexto)

    Mismo criterio que en todo lo demas (leccion aprendida TRES veces el 2026-08-20): hacen
    falta AL MENOS DOS palabras distintivas en comun. Con una sola, la palabra "pregunta" hacia
    que cualquier apunte del historial pareciera la respuesta, y se daba por resuelta una duda
    que nadie habia contestado."""
    from cuerpo import estado
    from cerebro.trozos import Buscador
    d = estado.leer()
    palabras = {w for w in re.split(r"[^\wáéíóúñ]+", duda.lower())
                if len(w) > 3 and w not in Buscador.COMUNES}
    if len(palabras) < 2:
        return []
    out = []
    for h in d.get("historial", [])[-30:]:
        txt = f"{h.get('campo','')} {h.get('a','')}".lower()
        suyas = {w for w in re.split(r"[^\wáéíóúñ]+", txt)
                 if len(w) > 3 and w not in Buscador.COMUNES}
        comunes = palabras & suyas
        if len(comunes) >= 2:
            out.append({"donde": f"lo decidimos el {h.get('cuando','?')}",
                        "texto": f"{h.get('campo')}: {h.get('a')}",
                        "puntaje": 4.0 + len(comunes), "fuente": "YA DECIDIDO"})
    return out[-2:]


def _responde_de_verdad(duda, candidatos):
    """¿Alguno de estos textos RESPONDE la duda, o solo comparte palabras?

    Un buscador por palabras NO puede saberlo: solo sabe si las palabras aparecen. Por eso el
    ultimo filtro lo hace un cerebro GRATIS, y con muy poco material (los candidatos, no el
    repo), asi que cuesta ~3 segundos y cero dinero.
    Si el cerebro no esta disponible, se elige el lado SEGURO: preguntarle a Julio.
    """
    if not candidatos:
        return []
    try:
        from cuerpo import obrero
        if not obrero.quienes_hay():
            return []                      # sin cerebro -> mejor preguntar que suponer
        trozos_txt = "\n\n".join(
            "[%d] (%s — %s)\n%s" % (i, c["fuente"], c["donde"], c["texto"][:700])
            for i, c in enumerate(candidatos[:5]))
        prompt = (
            "Di cuales de estos textos RESPONDEN la pregunta de abajo. Que aparezcan palabras\n"
            "parecidas NO basta: tiene que responderla de verdad.\n"
            "Si ninguno la responde, devuelve la lista vacia. Es MEJOR decir que ninguno\n"
            "responde que dar por buena una respuesta que no lo es.\n\n"
            "PREGUNTA: " + duda + "\n\nTEXTOS:\n" + trozos_txt + "\n\n"
            'Responde SOLO JSON: {"responden": [numeros], "por_que": "una frase"}')
        txt, _, _ = obrero._preguntar_con_relevo(prompt, 0.1)
        d = obrero._json_de(txt or "")
        nums = d.get("responden") or []
        return [candidatos[i] for i in nums if isinstance(i, int) and 0 <= i < len(candidatos)]
    except Exception:
        return []                          # ante la duda, se pregunta


def resolver(duda, proyecto=None, juzgar=True):
    """Busca en los cuatro sitios, en orden. Devuelve lo hallado y si hay que preguntar."""
    pasos = []
    for nombre, fn in (("contratos", _en_contratos), ("fallos", _en_fallos),
                       ("codigo", _en_codigo), ("estado", lambda d, p=None: _en_el_estado(d))):
        try:
            r = fn(duda, proyecto)
        except Exception as e:
            r = []
            pasos.append({"paso": nombre, "error": str(e)[:80]})
        if r:
            pasos.append({"paso": nombre, "hallado": r})
    hallado = [h for p in pasos for h in p.get("hallado", [])]
    # ULTIMO FILTRO: que un cerebro diga si alguno RESPONDE de verdad (no solo "se parece").
    juzgado = None
    if juzgar and hallado:
        juzgado = _responde_de_verdad(duda, hallado)
        hallado = juzgado
    return {"duda": duda, "proyecto": proyecto, "pasos": pasos, "hallado": hallado,
            "juzgado": juzgado is not None, "hay_que_preguntar": not hallado}


def formular(duda, resultado=None):
    """La pregunta para Julio: simple, sin jerga, y diciendo QUE se busco ya.
    Preguntar sin decir donde se busco parece pereza; diciendolo, es un informe."""
    r = resultado or resolver(duda)
    if not r["hay_que_preguntar"]:
        return ""
    donde = [p["paso"] for p in r["pasos"]]
    buscado = ", ".join(donde) if donde else "los contratos, los fallos, el codigo y el estado"
    return (f"PREGUNTA_REQUERIDA: {duda}\n"
            f"  (ya lo busque en {buscado} y no esta escrito en ningun sitio; "
            f"por eso te lo pregunto en vez de suponerlo)")


def informe(r):
    """Lo que lee Claude: corto, y con la FUENTE de cada respuesta."""
    L = [f"DUDA: {r['duda']}"]
    if not r["hallado"]:
        L.append("  NO_ENCONTRADO en contratos, fallos, codigo ni estado.")
        L.append("  -> HAY QUE PREGUNTARLE A JULIO. No se supone.")
        return "\n".join(L)
    L.append(f"  RESUELTA sin molestar a Julio ({len(r['hallado'])} fuentes):")
    for h in r["hallado"][:4]:
        L.append(f"  [{h['fuente']}] {h['donde']}")
        primera = h["texto"].strip().splitlines()[0][:110] if h["texto"].strip() else ""
        L.append(f"      {primera}")
    return "\n".join(L)


def apuntar_pregunta(duda, proyecto=None):
    """Deja la pregunta en el ESTADO. El candado de cierre no deja terminar hasta hacerla."""
    from cuerpo import estado
    r = resolver(duda, proyecto)
    if not r["hay_que_preguntar"]:
        return r
    d = estado.leer()
    ya = d.get("decision_pendiente", "")
    nueva = (ya + " | " if ya else "") + duda
    estado.apuntar(decision_pendiente=nueva[:400])
    return r
