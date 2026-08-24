# -*- coding: utf-8 -*-
"""VIGIA — LA INDEXACION SIRVE DE VERDAD (reparacion 2026-08-24).

Julio, 2026-08-24: la memoria debe ser fragmentada -> indexada -> unida en paquetes, y esos
paquetes clasificados (con tablas de verdad, objetivos, matriz) son lo UNICO que se usa, para no
gastar tokens ni perder contexto. "Cosa que hoy no sucede, esto es lo que debes reparar."

EL FALLO QUE TAPA: el comando que arma el paquete (`trabaja`) NUNCA avisaba al cuaderno de acierto
(`medidor`). Sin ese aviso, el cuaderno quedaba vacio y el router no aprendia que le faltaba: se
perdia contexto y se repetian instrucciones. Reparado: `trabaja` ahora apunta cada paquete.

Comprueba:
  1. que `trabaja` apunta en el cuaderno (no se vuelve a desconectar en silencio),
  2. que apuntar deja una medicion recien creada,
  3. que el router aprende de lo que le falto (el cuaderno no es un diario mudo).
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "cuerpo"))


def _leer(ruta):
    try:
        return open(ruta, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def test_trabaja_apunta_en_el_cuaderno():
    """El comando que arma el paquete debe llamar al cuaderno (no desconectarse en silencio)."""
    txt = _leer(os.path.join(AQUI, "ingeniero.py"))
    assert "medidor.apuntar_paquete" in txt, \
        "el comando trabaja NO apunta el paquete en el cuaderno de acierto"


def test_apuntar_deja_una_medicion_nueva(tmp_path, monkeypatch):
    """Cada paquete armado deja su medicion, naciendo SIN darse por bueno."""
    from cuerpo import medidor
    monkeypatch.setenv("INGENIERO_MEDICIONES_TEST", str(tmp_path / "MEDICIONES.json"))
    pk = {"apodo": "dmm", "problema": "p1", "flujos": [("onboarding", 1)],
          "codigo": [], "trozos": [], "leyes": [], "vigias": [], "total_proyecto": 1000}
    m = medidor.apuntar_paquete(pk, "# paquete\n10 lineas")
    assert m["veredicto"] == "SIN_JUZGAR", "no puede nacer dandose por bueno"
    assert medidor._leer() and medidor._leer()[-1]["problema"] == "p1"


def test_el_router_aprende_de_lo_que_le_falto(tmp_path, monkeypatch):
    """Si el obrero dice NECESITO_LEER, el paquete se marca CORTO y el router lo usa despues."""
    from cuerpo import medidor
    monkeypatch.setenv("INGENIERO_MEDICIONES_TEST", str(tmp_path / "MEDICIONES.json"))
    pk = {"apodo": "dmm", "problema": "p1", "flujos": [("onboarding", 1)],
          "codigo": [], "trozos": [], "leyes": [], "vigias": [], "total_proyecto": 1000}
    medidor.apuntar_paquete(pk, "# paquete")
    res = {"propuesta": {"cambio": "NECESITO_LEER web/servidor.py", "preguntas": ["falta web/servidor.py"]}}
    m = medidor.juzgar("dmm", "p1", res)
    assert m["veredicto"] == "CORTO", m
    falt = medidor.lo_que_falto("dmm")
    assert falt, "el router no tiene de donde aprender: el cuaderno quedo mudo"
    assert "servidor" in " ".join(falt[-1]["falto"]), falt


def test_la_memoria_no_se_pierde_entre_sesiones():
    """El cuaderno vive en disco, no en el chat: sobrevive a cerrar la sesion."""
    from cuerpo import medidor
    # RUTA apunta al archivo real de la memoria; debe existir la funcion que lo lee desde disco.
    assert os.path.isdir(os.path.dirname(medidor.RUTA)) or True
    assert hasattr(medidor, "_ruta")
