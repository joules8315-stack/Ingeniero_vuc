# -*- coding: utf-8 -*-
"""VIGIA 9 — NADA LENTO (orden 4 de Julio, 2026-08-20).

  "que no sea lento el proceso, ningun proceso debe ser lento, al contrario debe ser rapido y eficaz"

Fallo REAL: el trabajo cruzado tardo 612 segundos (10 minutos) porque el modelo `qwen3.6-27b`
razona demasiado y se caia por timeout con un paquete normal. Medido ese dia:
    qwen/qwen3.6-27b        > 300 s  TIMEOUT
    llama-3.3-70b-versatile    30 s  BIEN
    gemini-2.0-flash           40 s  BIEN

Aqui se vigila lo que se puede medir SIN gastar cuota: que el armado del paquete sea rapido y
que la configuracion no vuelva al modelo lento por descuido.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from cerebro import router, grafo

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPE_PAQUETE = 12.0   # segundos para armar un paquete (con el grafo ya en cache)

# Cuanto tarda una vuelta suelta con la maquina tranquila (medido en la de Julio, 2026-08-21).
# Sirve para saber si la maquina esta ocupada y no confundir "ocupada" con "lento".
REFERENCIA = 0.217


def _carga_de_la_maquina():
    """Cuantas veces mas lenta va la maquina ahora que estando tranquila.

    Ley 23: una comprobacion que falla a veces es peor que ninguna. Esta media SEGUNDOS DE RELOJ,
    asi que con la maquina ocupada se ponia roja sin que nada fuera lento: se cazo corriendo tres
    tandas a la vez (fallo real 2026-08-21). Un rojo falso ensena a ignorar los rojos, y asi es
    como se cuela un rojo de verdad. Ahora el tope se estira con la carga: un rojo aqui significa
    SIEMPRE que va lento de verdad, no que la maquina estuviera liada."""
    t0 = time.time()
    x = 0
    for i in range(3000000):
        x += i * i
    return max(1.0, (time.time() - t0) / REFERENCIA)
LENTOS_CONOCIDOS = ("qwen3.6-27b", "qwen3-32b", "compound-mini", "gpt-oss-20b")


def _hay(a):
    p = grafo.proyectos()
    return a in p and os.path.isdir(p[a]["ruta"])


def test_armar_un_paquete_es_rapido():
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    grafo.cargar("dmm")                      # calentar la cache, como en el uso real
    carga = _carga_de_la_maquina()
    t0 = time.time()
    router.armar("dmm", "el onboarding no guarda el perfil")
    tardo = time.time() - t0
    tope = TOPE_PAQUETE * carga
    assert tardo < tope, (
        f"armar el paquete tardo {tardo:.1f}s (tope {tope:.1f}s; la maquina va {carga:.1f} "
        f"veces mas lenta de lo normal, asi que esto es lentitud DE VERDAD)")


def test_el_grafo_en_cache_es_casi_instantaneo():
    if not _hay("dmm"):
        pytest.skip("dmm no esta")
    grafo.cargar("dmm")
    t0 = time.time()
    g = grafo.cargar("dmm")
    tardo = time.time() - t0
    assert g.get("_de_cache"), "no uso la cache: va a re-escanear en cada llamada"
    assert tardo < 5, f"leer el grafo de cache tardo {tardo:.1f}s"


def test_no_se_volvio_al_modelo_lento():
    """Si alguien vuelve a poner el qwen que razona, esto se pone ROJO antes de que Julio espere
    10 minutos por una respuesta."""
    cfg = os.path.join(AQUI, "arnes", "velocidad.config")
    assert os.path.exists(cfg), "falta arnes/velocidad.config"
    txt = open(cfg, encoding="utf-8").read()
    linea = [l for l in txt.splitlines() if l.strip().startswith("modelo_groq")]
    assert linea, "velocidad.config no dice que modelo usar en Groq"
    valor = linea[0].split("=", 1)[1].strip()
    assert not any(l in valor for l in LENTOS_CONOCIDOS), \
        f"modelo_groq={valor} es de los LENTOS medidos (>300s). Julio: nada lento."


def test_hay_tope_de_tiempo_por_llamada():
    """Sin tope, un cerebro colgado deja a Julio esperando sin fin.

    CORRECCION HONESTA (2026-08-20): esta vigia exigia tope <= 120s y estaba MAL MEDIDA.
    Latencia real, con el MISMO prompt de 20.000 caracteres:
        groq  : 13s / 18s / 34s / >300s     gemini: 5s / 67s / 294s     local: 45s
    No depende del tamano: depende de como este el servidor ajeno. Cortar a 120s no hacia el
    sistema rapido, hacia que FALLARA (tumbaba trabajos que iban a salir bien).
    Lo que de verdad protege a Julio es: (a) que exista tope por llamada, (b) que exista tope
    de ciclo, (c) que el trabajo corra APARTE y no lo deje bloqueado. Eso es lo que se vigila.
    """
    from cuerpo import obrero, cruzado, subagentes
    v = obrero._velocidad()
    assert hasattr(obrero, "_con_tope"), "no existe el tope de tiempo por llamada"
    assert 0 < float(v["tope_segundos"]) <= 600, "el tope por llamada es absurdo o no existe"
    assert cruzado.TOPE_CICLO <= 600, "el ciclo entero puede eternizarse"
    assert hasattr(subagentes, "lanzar"), "el trabajo pesado no corre en proceso aparte"


def test_el_local_es_la_red_de_seguridad():
    """LM Studio no tiene cuota ni latencia caprichosa: si esta encendido, tiene que verse.
    Fallo real 2026-08-20: estaba sirviendo qwen2.5-coder y el Ingeniero no lo veia porque
    exigia una variable de entorno en vez de comprobar el puerto."""
    from cuerpo import obrero
    assert hasattr(obrero, "preguntar_local"), "no hay via directa a LM Studio"
    if obrero._local_responde():
        assert "local" in obrero.quienes_hay(), \
            "LM Studio esta encendido y el Ingeniero no lo ve"


def test_el_reparador_y_el_vigilante_van_en_paralelo():
    """Si van en fila, se tarda el doble sin ganar nada: no dependen uno del otro."""
    from cuerpo import cruzado
    import inspect
    src = inspect.getsource(cruzado.resolver)
    assert "_en_paralelo" in src, "el reparador y el vigilante no van a la vez"
