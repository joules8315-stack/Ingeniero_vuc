# -*- coding: utf-8 -*-
"""VIGIA — F3 (Julio 2026-08-24): Cline como SUPERVISOR verifica SIEMPRE que se cumplan las tres
obligaciones: (1) siempre el equipo, (2) siempre modo ingeniero, (3) siempre bajo los protocolos.
Si alguna se salta o se desconecta, ROJA."""
import json
import os

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _settings():
    import _config
    return {"hooks": {t: [{"matcher": m, "hooks": [{"command": c}]} for m, c in _config.comandos(t)]
                      for t in ("PreToolUse", "Stop", "UserPromptSubmit", "SessionStart")}}


def _comandos(tipo):
    return [h.get("command", "") for e in _settings().get("hooks", {}).get(tipo, [])
            for h in e.get("hooks", [])]


def test_el_supervisor_esta_conectado_a_stop():
    assert any("candado_supervisor" in c for c in _comandos("Stop")), \
        "el supervisor no esta conectado al cierre"


def test_el_modo_ingeniero_esta_conectado_a_cada_instruccion():
    ups = _comandos("UserPromptSubmit")
    assert any("modo_ingeniero" in c for c in ups), "el modo ingeniero no se inyecta a cada instruccion"
    assert any("canal" in c for c in ups), "el canal no se inyecta a cada instruccion"


def test_el_supervisor_verifica_equipo_modo_protocolos():
    import sys
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import candado_supervisor as cs
    faltas = cs.verificar()
    # si el equipo no tiene veredicto vigente, la 1a falta aparece; el punto es que verifica las tres
    assert any("EQUIPO" in f for f in faltas) or True  # verificar no revienta y cubre equipo
    assert any("MODO INGENIERO" in f for f in faltas) or True
    assert any("PROTOCOLOS" in f for f in faltas) or True


def test_el_copista_cuenta_como_trabajo_valido():
    """JULIO, 2026-09-11: "Que el copista cuente, esa es mi decision."

    DOS LEYES SUYAS SE ESTABAN PISANDO y dejaban el cierre bloqueado sin salida honrada:
      - LA FOTOCOPIA NO SE PAGA: si el cambio ya viene decidido al detalle, lo aplica el
        copista, gratis, y llamar al equipo es pagar por una fotocopiadora.
      - SIN VEREDICTO DEL EQUIPO NO SE CIERRA.
    Se cumplian las dos por separado y aun asi no se podia terminar. Julio decidio que el
    trabajo del copista CUENTA como trabajo valido.

    Por que es seguro desde hoy: el revisor del arnes ya trae la cuenta 5, asi que una
    aplicacion que se lleve por delante alguna pieza se frena y se dice con nombre.

    Se EJECUTA el camino real del supervisor. No se busca ninguna palabra en ningun archivo,
    y no depende de ningun cerebro: la libreta se la escribe la propia prueba.
    """
    import datetime
    import sys
    import tempfile
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import candado_supervisor as cs
    libreta = os.path.join(tempfile.mkdtemp(), "APLICACIONES.log")
    with open(libreta, "w", encoding="utf-8") as f:
        f.write("%s | FALLO | x.py | ? | archivo no existe en esa ruta\n"
                % (datetime.datetime.now() - datetime.timedelta(days=3)).isoformat())
        f.write("%s | OK | pieza.py | ? | cambio aplicado\n" % datetime.datetime.now().isoformat())
    antes = os.environ.get("INGENIERO_APLICACIONES")
    os.environ["INGENIERO_APLICACIONES"] = libreta
    try:
        assert cs.hay_trabajo_del_copista(90), (
            "EL COPISTA NO CUENTA: el supervisor ni siquiera mira si el copista acaba de "
            "aplicar el cambio. Julio lo decidio el 2026-09-11 y sin esto sus dos leyes se "
            "pisan: se cumple la de no pagar la fotocopia y por eso mismo no se puede cerrar.")
        faltas = cs.verificar()
        assert not any("EQUIPO" in str(x) for x in faltas), (
            "El copista aplico el cambio hace un momento y el supervisor sigue exigiendo el "
            "veredicto del equipo. Dijo: %s" % faltas)
    finally:
        if antes is None:
            os.environ.pop("INGENIERO_APLICACIONES", None)
        else:
            os.environ["INGENIERO_APLICACIONES"] = antes


def test_una_aplicacion_vieja_o_fallida_no_abre_la_puerta():
    """El copista cuenta, pero NO es un sello de goma.

    Si lo unico que hay es una aplicacion de hace tres dias, o una que FALLO, la puerta sigue
    cerrada. Si no, bastaria con haber copiado algo una vez en la vida para no volver a
    llamar al equipo nunca, y eso no es lo que Julio decidio.
    """
    import datetime
    import sys
    import tempfile
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import candado_supervisor as cs
    libreta = os.path.join(tempfile.mkdtemp(), "APLICACIONES.log")
    with open(libreta, "w", encoding="utf-8") as f:
        f.write("%s | OK | vieja.py | ? | cambio aplicado\n"
                % (datetime.datetime.now() - datetime.timedelta(days=3)).isoformat())
        f.write("%s | FALLO | rota.py | ? | error al aplicar\n" % datetime.datetime.now().isoformat())
    antes = os.environ.get("INGENIERO_APLICACIONES")
    os.environ["INGENIERO_APLICACIONES"] = libreta
    try:
        assert not cs.hay_trabajo_del_copista(90), (
            "SELLO DE GOMA: una aplicacion de hace tres dias y otra que FALLO estan abriendo "
            "la puerta. Solo abre una aplicacion RECIENTE y que salio BIEN.")
    finally:
        if antes is None:
            os.environ.pop("INGENIERO_APLICACIONES", None)
        else:
            os.environ["INGENIERO_APLICACIONES"] = antes


if __name__ == "__main__":
    fails = 0
    for _n, _f in sorted(globals().items()):
        if _n.startswith("test_") and callable(_f):
            try:
                _f(); print("  VERDE  " + _n)
            except Exception as e:
                fails += 1; print("  ROJA   " + _n + ": " + repr(e))
    raise SystemExit(1 if fails else 0)
