# -*- coding: utf-8 -*-
"""VIGIA 16 — EL PROTOCOLO DE JULIO SE CUMPLE SOLO (2026-08-20).

  Julio: "Falta que actues segun protocolos, ya eso lo he dicho miles de veces... crea los
   putos disparadores, lo que tengas que hacer."

EL PROTOCOLO YA ESTABA ESCRITO desde el 2026-07-28 (`PROTOCOLO_DEL_CHAT.md`), con este fin
textual suyo: "yo solo digo hagamos esto y el lo hace, sin que yo repita". Y aun asi, el mismo
dia 2026-08-20 se incumplieron sus DOS leyes duras:
  · lenguaje simple  -> se le hablo de archivos .py, de programas de prueba y de guardados
  · confirmar el objetivo antes de construir -> se construyo sin esperar su "si"

La leccion, y es la de todo el dia: **lo que se ejecuta solo se cumple; lo que depende de que
alguien se acuerde, no.** Por eso el protocolo pasa de documento a disparador.
"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import pytest
import candado_protocolo as cp


def _correr(arg, payload, entorno=None):
    env = dict(os.environ)
    env.pop("PYTEST_CURRENT_TEST", None)
    if entorno:
        env.update(entorno)
    p = subprocess.run([sys.executable, os.path.join(AQUI, "arnes", "candado_protocolo.py"), arg],
                       input=json.dumps(payload), capture_output=True, text=True,
                       env=env, timeout=120)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


@pytest.fixture(autouse=True)
def _limpio(tmp_path, monkeypatch):
    monkeypatch.setattr(cp, "DICHO", str(tmp_path / "dichos.json"))
    monkeypatch.setattr(cp, "CONTADOR", str(tmp_path / "bloqueos"))
    yield


# ─── 1) ¿SE DA CUENTA DE QUE JULIO REPITE? ─────────────────────────────────────
def test_detecta_que_julio_repite():
    """El termometro del sistema entero. Antes marcaba CERO habiendo repetido 4 veces."""
    d = cp._leer_dichos()
    d.append("primero buscas via canonica, despues el origen del fallo, analizas y miras como lograrlo")
    cp._guardar_dichos(d)
    si, antes, p = cp.repite("el orden no es correcto: primero via canonica, despues el origen "
                             "del fallo, analizar y ver como lograrlo")
    assert si, "Julio repitio lo mismo y no se dio cuenta (parecido %s)" % p
    assert antes


def test_no_confunde_una_orden_nueva_con_una_repeticion():
    """Si marca repeticion en todo, el aviso se vuelve ruido y se ignora."""
    d = cp._leer_dichos()
    d.append("primero buscas via canonica y despues el origen del fallo")
    cp._guardar_dichos(d)
    si, _, _ = cp.repite("ahora quiero que las fotos las descargue el usuario y no automatico")
    assert not si, "dijo que repetia algo que no tiene nada que ver"


def test_un_saludo_corto_no_cuenta_como_repeticion():
    si, _, _ = cp.repite("si")
    assert not si


# ─── 2) ¿FRENA LA JERGA PROHIBIDA ANTES DE QUE LE LLEGUE A JULIO? ──────────────
def test_frena_la_jerga_prohibida():
    """LEY DURA del protocolo: Julio no es tecnico y lo ha repetido con enojo."""
    malo = ("Ya arregle el hook en app_web.html, corri pytest y hice el commit; "
            "el service worker cachea el manifest.")
    fuera = cp._jerga_en(malo)
    assert len(fuera) >= 4, "no vio la jerga: %s" % fuera
    assert "commit" in fuera and any(x.endswith(".html") for x in fuera)


def test_deja_pasar_una_respuesta_en_palabras_normales():
    bueno = ("Ya lo arregle: la pantalla ahora abre sin internet y guarda tus informes "
             "en el celular hasta que vuelva la senal.")
    assert cp._jerga_en(bueno) == [], "estorba una respuesta que ya estaba bien escrita"


def test_el_candado_de_salida_bloquea_de_verdad():
    code, txt = _correr("salida", {"last_assistant_message":
                                   "corri pytest y el commit del hook fallo en app_web.html"})
    assert code == 2, "dejo pasar una respuesta llena de jerga"
    assert "JERGA PROHIBIDA" in txt


def test_el_candado_de_salida_no_estorba_lo_bien_escrito():
    code, _ = _correr("salida", {"last_assistant_message":
                                 "Listo: ya puedes entrar sin internet desde la pantalla de inicio."})
    assert code == 0


# ─── 3) ¿EXIGE CONFIRMAR EL OBJETIVO ANTES DE CONSTRUIR? ───────────────────────
def test_no_deja_construir_algo_nuevo_sin_confirmar_el_objetivo(tmp_path, monkeypatch):
    """OJO: si Julio ya dijo "si" hace poco, el semaforo esta puesto y el candado NO bloquea
    (correctamente). La prueba tiene que mirar el caso en que NO hay "si", asi que se aparta
    el semaforo real. Fallo de la propia prueba, detectado el 2026-08-20."""
    monkeypatch.setenv("INGENIERO_SEMAFORO_TEST", str(tmp_path / "no_existe"))
    nuevo = str(tmp_path / "cosa_nueva.py")
    code, txt = _correr("construir", {"tool_input": {"file_path": nuevo}})
    assert code == 2, "dejo construir algo nuevo sin haber confirmado el objetivo con Julio"
    assert "objetivo" in txt.lower()


def test_no_estorba_al_reparar_algo_que_ya_existe():
    """La ley es sobre CONSTRUIR cosas nuevas, no sobre arreglar lo que ya hay."""
    code, _ = _correr("construir", {"tool_input": {
        "file_path": os.path.join(AQUI, "ingeniero.py")}})
    assert code == 0, "bloqueo una reparacion normal: eso estorba"


# ─── 4) NINGUN CANDADO PUEDE DEJAR A JULIO ATRAPADO ────────────────────────────
def test_el_interruptor_de_emergencia_los_apaga(tmp_path):
    nuevo = str(tmp_path / "otra_cosa.py")
    marca = str(tmp_path / "aut_off")
    open(marca, "w", encoding="utf-8").close()           # autorizacion de Julio (fecha fresca)
    code, _ = _correr("construir", {"tool_input": {"file_path": nuevo}},
                      {"INGENIERO_AUTORIZACION_TEST": marca})
    assert code == 0, "la autorizacion de Julio no apago el candado del protocolo"


def test_no_bloquea_mas_de_dos_veces_seguidas():
    salidas = [_correr("salida", {"last_assistant_message": "pytest commit hook"})[0]
               for _ in range(3)]
    assert 0 in salidas, "bloquea siempre: dejaria a Julio atrapado (%s)" % salidas
