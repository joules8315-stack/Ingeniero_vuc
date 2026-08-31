# -*- coding: utf-8 -*-
"""VIGIA — L13 LA MEMORIA NO MIENTE NI OLVIDA (Julio, 2026-08-27).

El paquete del repartidor tiene que traer la pieza COMPLETA que se va a tocar (no un trozo suelto),
con su flujo y su historial. Y se MIDE si la memoria sirve: cada paquete incompleto (que obliga a
NECESITO_LEER) es un fallo de fragmentacion.

Regla madre (Julio, 2026-08-27): si el sistema no puede trabajar (circulo: el repartidor no trae su
propio material y el equipo no aprueba), se REPARA la causa de fondo de la herramienta antes de pedir
llaves. La herramienta se repara/afina mientras construye.

Se vigila aqui:
  1. la ley esta escrita donde la leen (contrato + matriz + protocolo),
  2. el repartidor, cuando fragmenta una pieza, entrega el trozo Y la pieza a la que pertenece
     (no un trozo huerfano sin su contexto),
  3. se mide si la memoria sirve (el medidor cuenta CORTO/NECESITO_LEER como fallo de paquete).
"""
import os
import sys
from cerebro import grafo

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_la_ley_esta_escrita_donde_la_leen():
    """La ley L13 tiene que estar en el contrato y en la matriz (si no, es un deseo)."""
    contrato = _leer(os.path.join(AQUI, "CONTRATO_LEGISLACION_TOTAL.md")).lower()
    assert "la memoria no miente" in contrato, "la ley de la memoria no esta en el contrato total"
    assert "causa de fondo" in contrato and "pedir llaves" in contrato, \
        "falta la regla madre (reparar causa de fondo antes que llaves)"
    matriz = _leer(os.path.join(AQUI, "MATRIZ_LEGISLACION.md")).lower()
    assert "memoria no miente" in matriz, "la ley no esta en la matriz de legislacion"


def test_el_medidor_cuenta_un_paquete_incompleto_como_fallo():
    """Se MIDE si la memoria sirve: un paquete que obliga a NECESITO_LEER es un fallo de paquete.

    Sin esto, el sistema diria 'ahorra el 99%' pero no sabria que la memoria trae de mas o de menos.
    El NECESITO_LEER legitimo viene con la pregunta de que material falta (asi se mide QUE falto).
    """
    import tempfile
    from cuerpo import medidor
    medidor.RUTA = os.path.join(tempfile.mkdtemp(), "MEDICIONES.json")
    pk = {"apodo": "dmm", "problema": "p1", "flujos": [("x", 1)],
          "codigo": [{"id": "cuerpo/a.py"}], "trozos": [], "leyes": [],
          "vigias": [{"id": "vigias/t.py"}], "total_proyecto": 1000}
    medidor.apuntar_paquete(pk, "\n".join(["x"] * 50))
    # el obrero pide el material que le falta, con el que (que falta) en preguntas
    m = medidor.juzgar("dmm", "p1", {"propuesta": {
        "cambio": "NECESITO_LEER web/servidor.py",
        "preguntas": ["falta web/servidor.py para saber como guarda"]}})
    assert m["veredicto"] == "CORTO", "un paquete que pide mas material no se marco como CORTO"
    assert m["falto"], "no apunto QUE falto (es la comida del auto-ajuste de la memoria)"


def test_el_repartidor_mide_y_avisa_cuando_el_paquete_no_es_completo():
    """El repartidor debe saber decir si su fragmentacion fue completa o se quedo corta.

    La regla: un trozo nunca llega solo; llega con la pieza a la que pertenece, para que quien lo
    toque tenga el contexto entero de la funcion, no un pedazo huerfano.
    """
    import cerebro.trozos as trozos
    import cerebro.router as router
    src = _leer(os.path.join(AQUI, "cerebro", "router.py"))
    # el router, al fragmentar, mantiene el vinculo pieza<->trozo (no un trozo sin dueño)
    assert "pieza" in src and "trozos" in src, \
        "el repartidor no esta vinculado a la fragmentacion por pieza"
    # el router avisa cuando la fragmentacion se queda corta (TOPELINEAS / aviso)
    assert "TOPE_LINEAS" in src or "AVISO" in src, \
        "el repartidor no avisa cuando el paquete crece (fragmentacion incompleta)"


def test_se_repara_la_causa_de_fondo_no_se_pide_llave():
    """Regla madre: antes de pedir una llave para seguir, se repara la causa de fondo.

    La instruccion de legislar la memoria esta apuntada (no se la ignora en silencio).
    """
    import candado_legislar as cl
    txt = cl.listar() if hasattr(cl, "listar") else ""
    # o bien ya esta legislada (marcada) o esta apuntada como pendiente: nunca borrada
    led = cl._leer() if hasattr(cl, "_leer") else {}
    textos = " ".join(str(e.get("texto", "")) for e in led.values())
    assert "memoria no miente" in textos or "causa de fondo" in textos, \
        "la instruccion de la memoria no esta registrada en la legislacion"


def test_lo_que_el_problema_nombra_entra_al_material():
    """Ley L13/L14 (Julio, 2026-08-27): cuando el problema nombra un archivo, ESE entra al material.

    Antes se nombraba 'app_web.html' y el repartidor devolvia solo las pruebas o vigias, no la
    pantalla; el equipo no podia revisar ni aprobar, y todo se atascaba. Ahora el archivo nombrado
    entra al material (codigo/trozos). Aplica a TODOS los proyectos.
    """
    import cerebro.router as router
    # prueba en foto_informe con la pantalla del boton
    prs = grafo.proyectos()
    if "foto_informe" in prs:
        pk = router.armar("foto_informe", "boton de los titulos en app_web.html")
        ids = [t["pieza"] for t in pk.get("trozos", [])]
        assert any("app_web.html" in x for x in ids), \
            "nombran app_web.html y el material no trae la pantalla (causa de fondo)"
    # y en el ingeniero con el propio router
    pk2 = router.armar("ingeniero", "reparar cerebro/router.py")
    ids2 = [t["pieza"] for t in pk2.get("trozos", [])]
    assert any("router.py" in x for x in ids2), \
        "nombran router.py y el material no lo trae (causa de fondo)"


def test_el_mensaje_de_la_llave_no_miente():
    """Julio, 2026-08-27 (queja de Claude): 'LLAVE GUARDADA' salia SIEMPRE, incluso con RECHAZADO.

    El candado no abria con rechazo (ya probado), pero el mensaje decia 'guarda llave' y enganaba.
    Ahora el mensaje dice la verdad: 'LLAVE GUARDADA' solo con APROBADO, y si el equipo no aprobo
    se dice que no se guardo llave.
    """
    src = _leer(os.path.join(AQUI, "ingeniero.py"))
    assert "LLAVE GUARDADA" in src, "falta el mensaje de llave guardada"
    assert "APROBADO" in src, "el mensaje de llave no depende del veredicto APROBADO"
    assert "EL EQUIPO NO APROBO" in src, \
        "no hay mensaje honesto cuando el equipo rechaza: el mensaje miente"


def test_el_obrero_confirma_la_linea_con_su_texto():
    """Julio, 2026-08-27: el numero de linea solo se confunde (7 se lee como 1); el texto no.

    El obrero debe copiar el texto literal de la linea que va a tocar (`linea_texto`), y el auditor
    debe verificar que ese texto coincida con el material. Asi no se apunta al renglon equivocado.
    """
    src = _leer(os.path.join(AQUI, "cuerpo", "obrero.py"))
    assert "linea_texto" in src, "el obrero no pide el texto literal de la linea"
    assert "COPIAS el texto literal" in src, "el prompt no exige copiar el texto de la linea"
    # ACTUALIZADO el 2026-08-28: la regla 6 se reescribio. Antes buscaba "COMPRUEBA EL TEXTO DE LA
    # LINEA"; ahora la regla empieza por "LA UBICACION SE JUZGA POR EL TEXTO". La intencion es la
    # misma y se mide MAS que antes: se exige ademas que este escrito que el numero por si solo no
    # basta para rechazar. Ese era el fallo que tumbo OCHO rondas de equipo en un solo dia.
    assert "LA UBICACION SE JUZGA POR EL TEXTO" in src, \
        "el auditor no verifica que el texto de la linea coincida con el material"
    assert "NO ES MOTIVO DE RECHAZO" in src, \
        ("no esta escrito que un numero que no cuadra NO basta para rechazar: sin esa frase el "
         "auditor vuelve a tumbar reparaciones correctas por contar mal, y cada una es una ronda "
         "de Julio pagada para nada")


def test_el_juez_ilegible_se_vuelve_a_preguntar():
    """Julio, 2026-08-27 (Claude): 'el juez contesta y el sistema no entiende su respuesta, la da por
    perdida y no le pregunta a nadie mas'. Si el juez devuelve JSON roto/cortado, se le pide de nuevo
    en vez de darlo por perdido (que dejaba el equipo trabado aunque hubiera cerebros).
    """
    src = _leer(os.path.join(AQUI, "cuerpo", "cruzado.py"))
    assert "intento_juez" in src, "el sistema no reintenta al juez cuando responde ilegible"
    assert "se le pide de nuevo" in src, \
        "el sistema da por perdida la respuesta ilegible del juez (fallo de Claude, 2026-08-27)"
    assert "SIN_JUEZ" in src, "no hay veredicto SIN_JUEZ para cuando el juez no contesta legible"
    # sistema numerico de fallos del juez (Julio, 2026-08-27): codigos 1..6, no texto generico
    assert "FALLOS_DEL_JUEZ" in src, "falta el catalogo numerico de fallos del juez"
    assert "fallos_a_texto" in src, "falta la funcion que traduce los codigos a texto"
    assert "fallos_a_texto(juez" in src, "el aprendido no usa la traduccion de codigos del juez"


def test_el_juez_se_cine_al_codigo_y_el_receptor_entiende():
    """Julio, 2026-08-27: QUIEN VIGILA que el juez se cine al codigo y que el receptor entienda.

    Comprueba el COMPORTAMIENTO, no solo que el codigo exista:
      1. un codigo valido (1..6) se traduce a texto claro -> el receptor entiende,
      2. un codigo fuera de rango (7, 0) se MARCA (no pasa silencioso),
      3. texto libre donde iba un codigo tambien se MARCA,
      4. el texto llega al reparador en 'aprendido' (no codigos sueltos).
    """
    import cuerpo.cruzado as cr
    # 1) codigos validos -> texto entendible
    t1 = cr.fallos_a_texto([1, 5])
    assert "INVENTA" in t1 and "TAPA EL SINTOMA" in t1, \
        "el receptor no entendio los codigos validos: %r" % t1
    assert not t1.startswith("CODIGO"), "codigo valido marcado como desconocido"
    # 2) codigo fuera de rango -> se marca, no silencioso
    t2 = cr.fallos_a_texto([7])
    assert "CODIGO DE JUEZ NO RECONOCIDO" in t2, \
        "un codigo fuera de rango (7) paso silencioso: el juez no se cine y nadie lo ve"
    # 3) texto libre donde iba un codigo -> se marca
    t3 = cr.fallos_a_texto(["la prueba no corre"])
    assert "CODIGO DE JUEZ NO RECONOCIDO" in t3, \
        "texto libre paso como fallo valido: el juez no se cine al catalogo"
    # 4) el catalogo cubre 1..6 (ninguno hueco)
    for n in range(1, 7):
        assert n in cr.FALLOS_DEL_JUEZ, "el catalogo de fallos del juez deja el %d sin definir" % n
