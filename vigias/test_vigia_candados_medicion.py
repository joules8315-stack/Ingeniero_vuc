# -*- coding: utf-8 -*-
"""VIGIA — el contador de candados cuenta bien, y ALGUIEN lo llama.

DE DONDE SALE (Julio, 2026-08-25): "no vamos a ver los candados mensual, sino semanal, cada 8
dias los evaluamos". Y antes: que cada candado lleve cuenta de cuantas veces caza algo de verdad
Y de cuantas veces frena algo legitimo.

POR QUE LAS DOS CUENTAS: el peor candado no es el que no caza nada. Es el que caza poco y frena
mucho en falso, porque **ensena a ignorar los avisos**, y ese habito se contagia a los que si
sirven. Caso medido ese dia: un aviso salto unas veinte veces y no cazo ni un error real; se
llevo cerca de un tercio del trabajo.

Y LA COMPROBACION QUE MAS IMPORTA — que alguien lo llame:
La memoria de fallos ya tiene apuntado esto, con nombre y fecha: "el contador de veces que Julio
repite marcaba CERO habiendo repetido cuatro veces el mismo dia; solo subia si alguien lo
apuntaba a mano". Al escribir esta vigia se comprobo que el contador de candados tenia el MISMO
defecto: existia y NADIE lo llamaba. Dentro de 8 dias Julio habria mirado una tabla de ceros y
habria concluido que ningun candado sirve, que es lo contrario de la verdad.

Un contador que hay que acordarse de subir no mide: adorna.

QUIEN LA ESCRIBE Y POR QUE: el contador es de Cline. Se le aviso por el canal de que su pieza
estaba sin vigia y de que la casa quedaba en rojo, ofreciendole escribirla yo. Sin respuesta y
con el trabajo parado, se aplica la regla recien legislada (CONTRATO_DOS_TRABAJANDO, punto 1):
"si no hay respuesta y el trabajo urge, se dice 'la empiezo yo, avisame si ya la tienes'".
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

import candados_medicion  # noqa: E402

ARNES = os.path.join(AQUI, "arnes")


def _aparte(tmp_path, monkeypatch):
    """La cuenta de mentira vive aparte: NUNCA se toca la de verdad."""
    monkeypatch.setattr(candados_medicion, "RUTA",
                        str(tmp_path / "cuenta_de_mentira.json"), raising=False)


def test_cuenta_las_cazadas(tmp_path, monkeypatch):
    _aparte(tmp_path, monkeypatch)
    candados_medicion.apuntar("memoria", "cazo")
    candados_medicion.apuntar("memoria", "cazo")
    e = candados_medicion._leer().get("memoria", {})
    assert e.get("cazadas") == 2, "no cuenta las veces que un candado tuvo razon"


def test_cuenta_los_frenos_en_falso(tmp_path, monkeypatch):
    """La cuenta que protege el tiempo de Julio."""
    _aparte(tmp_path, monkeypatch)
    candados_medicion.apuntar("memoria", "freno_falso")
    e = candados_medicion._leer().get("memoria", {})
    assert e.get("frenos_falsos") == 1, (
        "no cuenta las frenadas en falso. Sin ese numero no se puede ver cual candado solo "
        "estorba, que es justo lo que Julio quiere mirar cada 8 dias")


def test_las_dos_cuentas_NO_se_pisan(tmp_path, monkeypatch):
    """Si una borra a la otra, la revision de los 8 dias decide sobre datos falsos."""
    _aparte(tmp_path, monkeypatch)
    candados_medicion.apuntar("equipo", "cazo")
    candados_medicion.apuntar("equipo", "freno_falso")
    candados_medicion.apuntar("equipo", "cazo")
    e = candados_medicion._leer().get("equipo", {})
    assert e.get("cazadas") == 2 and e.get("frenos_falsos") == 1, (
        "las dos cuentas se pisan: %r" % (e,))


def test_cada_candado_lleva_SU_cuenta(tmp_path, monkeypatch):
    """Sumarlos todos no sirve: hay que saber CUAL sobra."""
    _aparte(tmp_path, monkeypatch)
    candados_medicion.apuntar("memoria", "freno_falso")
    candados_medicion.apuntar("equipo", "cazo")
    d = candados_medicion._leer()
    assert d.get("memoria", {}).get("frenos_falsos") == 1
    assert d.get("equipo", {}).get("cazadas") == 1
    assert d.get("memoria", {}).get("cazadas", 0) == 0, (
        "la cuenta de un candado se le esta sumando a otro")


def test_el_resumen_se_puede_leer_sin_datos(tmp_path, monkeypatch):
    """El primer dia no hay nada apuntado. Eso no puede reventar."""
    _aparte(tmp_path, monkeypatch)
    assert isinstance(candados_medicion.resumen(), str), (
        "el resumen revienta cuando todavia no hay nada apuntado")


def test_ALGUIEN_lo_llama():
    """La comprobacion que de verdad decide si esto mide o adorna.

    Ya esta apuntado en la memoria de fallos: un contador que solo sube si alguien se acuerda de
    subirlo marca CERO aunque la cosa haya pasado cuatro veces. Si ningun candado lo llama, la
    revision de los 8 dias vera una tabla de ceros y concluira que ningun candado sirve.

    Y NO BASTA con que lo llame uno (debilidad apuntada 2026-08-25): los candados que de verdad
    frenan deben apuntar su cazada justo donde bloquean. Si uno queda sin cablear, la tabla de
    los 8 dias vuelve a mentir (deja de contar lo que ese candado caza) y nadie lo nota.
    """
    OBLIGATORIOS = [
        ("candado_commit.py", "commit"),
        ("candado_equipo.py", "equipo"),
        ("candado_memoria.py", "memoria"),
        ("candado_prueba_real.py", "prueba_real"),
        ("candado_preguntar.py", "preguntar"),
        ("candado_legislar.py", "legislar"),
        ("candado_cierre.py", "cierre"),
        ("candado_terminal.py", "terminal"),
        ("candado_archivo_del_veredicto.py", "archivo_del_veredicto"),
    ]
    fallan = []
    for nombre, clave in OBLIGATORIOS:
        ruta = os.path.join(ARNES, nombre)
        if not os.path.isfile(ruta):
            fallan.append("%s (no existe)" % nombre)
            continue
        try:
            with open(ruta, encoding="utf-8", errors="replace") as f:
                contenido = f.read()
        except Exception:
            fallan.append("%s (no se puede leer)" % nombre)
            continue
        if ('cazado("%s")' % clave) not in contenido:
            fallan.append("%s no llama cazado(%r)" % (nombre, clave))
    assert not fallan, (
        "el contador de candados miente si un candado que frena no apunta su cazada justo donde "
        "bloquea. Sin eso la revision de los 8 dias deja de contar lo que ese candado caza y "
        "nadie lo nota. Estos no estan cableados: %s" % "; ".join(fallan))
