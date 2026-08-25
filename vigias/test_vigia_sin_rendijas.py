# -*- coding: utf-8 -*-
"""VIGIA 18 — NINGUNA RENDIJA PARA LEER SIN CONTROL (Julio, 2026-08-20).

  "No solo tapa la ventana, sino cada rendija por donde te puedas colar; no sirve de nada gastar
   mi tiempo en una IA que no me va a ayudar, por el contrario me hace perder tiempo."

EL AGUJERO, medido ese dia: el arnes vigilaba TRES puertas (abrir archivo, editar, preguntar) y
habia SIETE formas de leer un proyecto entero sin que nadie lo viera. Por una de ellas —buscar
desde la terminal— se hizo el diagnostico completo del MVP: **cero paquetes minimos pedidos**
y decenas de lecturas sueltas sobre un archivo de 16.845 lineas.

La regla: **leer es leer, da igual con que herramienta.** Todas las vias de lectura pasan por
el mismo control, y ese control exige el paquete minimo despues de unas pocas busquedas.
"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest

MVP = r"C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"


def _correr(payload, entorno=None):
    env = dict(os.environ)
    env.pop("PYTEST_CURRENT_TEST", None)
    env["INGENIERO_SIN_PAQUETE_TEST"] = "1"      # se simula que NO hay paquete vigente
    import tempfile
    env["INGENIERO_APAGONES_TEST"] = os.path.join(tempfile.gettempdir(), "apagones_prueba.log")
    if entorno:
        env.update(entorno)
    p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_terminal.py")],
                       input=json.dumps(payload), capture_output=True, text=True,
                       env=env, timeout=120)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


def _orden(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


# ─── LAS RENDIJAS, UNA POR UNA ────────────────────────────────────────────────
@pytest.mark.parametrize("orden", [
    'grep -n "def create_report" "%s/app.py"' % MVP,
    'sed -n "13616,13700p" "%s/app.py"' % MVP,
    'head -50 "%s/app_web.html"' % MVP,
    'tail -80 "%s/app.py"' % MVP,
    'cat "%s/offline.html"' % MVP,
    'python -c "print(open(r\'%s/app.py\').read()[:5000])"' % MVP,
])
def test_ninguna_orden_de_terminal_lee_sin_control(orden):
    """Cada una de estas leia el proyecto sin que nadie lo viera."""
    from candado_terminal import TOPE_SIN_PAQUETE, _guardar_cuenta
    _guardar_cuenta(TOPE_SIN_PAQUETE)          # ya se agotaron las de cortesia
    code, txt = _correr(_orden(orden))
    assert code == 2, "esta via lee el proyecto sin control: %s" % orden[:70]
    assert "paquete" in txt.lower()


def test_NI_UNA_lectura_sin_paquete():
    """Julio lo endurecio el 2026-08-20: "que SIEMPRE pida el paquete minimo y sea inviolable".
    CERO lecturas de cortesia. No hacen falta: el paquete se pide solo con el problema en
    palabras, sin necesidad de haber buscado antes."""
    from candado_terminal import _guardar_cuenta, TOPE_SIN_PAQUETE
    assert TOPE_SIN_PAQUETE == 0, "hay lecturas de cortesia: Julio pidio CERO"
    _guardar_cuenta(0)
    code, _ = _correr(_orden('grep -n "def health" "%s/app.py"' % MVP))
    assert code == 2, "dejo pasar la PRIMERA lectura sin paquete"


def test_con_paquete_vigente_no_estorba(monkeypatch):
    """Si se esta trabajando bien (con paquete), no se cuenta nada.

    SE PONIA EN ROJO SOLA (fallo real 2026-08-22): el candado mira si hay algun paquete de menos
    de 8 horas, y esta prueba no creaba ninguno. Pasaba si alguien habia trabajado hace poco y
    fallaba al dia siguiente sin que nadie tocara una linea. Es el patron ya apuntado de la
    prueba que depende del reloj. Ahora se fabrica SU PROPIO paquete y lo borra al terminar:
    nace con la hora de hoy, asi que ya no depende de lo que hiciera nadie ayer.
    """
    import os as _os
    from candado_terminal import _guardar_cuenta, TOPE_SIN_PAQUETE, AQUI
    carpeta = _os.path.join(AQUI, "memoria", "paquetes")
    _os.makedirs(carpeta, exist_ok=True)
    mio = _os.path.join(carpeta, "_paquete_de_prueba_sin_rendijas.md")
    with open(mio, "w", encoding="utf-8") as f:
        f.write("# paquete de prueba, se borra solo\n")
    try:
        _guardar_cuenta(TOPE_SIN_PAQUETE + 5)
        code, _ = _correr(_orden('grep -n "x" "%s/app.py"' % MVP),
                          {"INGENIERO_SIN_PAQUETE_TEST": ""})
        assert code == 0, "estorba aun teniendo el paquete vigente"
    finally:
        try:
            _os.remove(mio)
        except OSError:
            pass


def test_no_estorba_lo_que_no_lee_proyectos():
    """git, las pruebas y las medidas tienen que pasar siempre."""
    from candado_terminal import _guardar_cuenta, TOPE_SIN_PAQUETE
    for orden in ('git status --porcelain',
                  'python -m pytest -q vigias/',
                  'curl -s http://127.0.0.1:8000/health'):
        _guardar_cuenta(TOPE_SIN_PAQUETE + 5)
        code, _ = _correr(_orden(orden))
        assert code == 0, "estorba una orden que no lee ningun proyecto: %s" % orden


def test_no_estorba_trabajar_en_el_propio_ingeniero():
    """Arreglar el Ingeniero no es explorar un proyecto ajeno."""
    from candado_terminal import _guardar_cuenta, TOPE_SIN_PAQUETE
    _guardar_cuenta(TOPE_SIN_PAQUETE + 5)
    code, _ = _correr(_orden('grep -n "def main" "%s/ingeniero.py"' % AQUI))
    assert code == 0, "bloqueo trabajar en el propio Ingeniero"


def test_el_interruptor_de_emergencia_lo_apaga(monkeypatch):
    from candado_terminal import _guardar_cuenta, TOPE_SIN_PAQUETE
    _guardar_cuenta(TOPE_SIN_PAQUETE + 5)
    import tempfile
    marca = os.path.join(tempfile.gettempdir(), "aut_off_f7.log")
    open(marca, "w", encoding="utf-8").close()           # autorizacion de Julio (fecha fresca)
    monkeypatch.setenv("INGENIERO_AUTORIZACION_TEST", marca)   # auto-restaura al terminar
    code, _ = _correr(_orden('grep -n "x" "%s/app.py"' % MVP), {})
    assert code == 0, "la autorizacion de Julio no apago el candado"


# ─── que TODAS las vias esten declaradas y vigiladas ──────────────────────────
def test_estan_declaradas_todas_las_vias_de_lectura():
    """Si aparece una via nueva y nadie la declara, vuelve a haber rendija."""
    import candado_terminal as ct
    for palabra in ("grep", "sed", "head", "tail", "cat", "python", "get-content", "select-string"):
        assert ct.LECTORAS.search(palabra) or palabra in ct.__doc__.lower(), \
            "la via '%s' no esta declarada como forma de leer" % palabra
