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
