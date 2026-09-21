# -*- coding: utf-8 -*-
"""vigias/test_vigia_el_registro_del_candado_no_miente.py — EL REGISTRO DE DECISIONES NO MIENTE.

Julio, 2026-09-20: el candado apunta en memoria/DECISIONES_CANDADO.log TODO lo que decide, lo
que frena Y lo que deja pasar. Pero la funcion que escribe ese registro (_apuntar_frenada, en
arnes/candado_equipo.py) decide la palabra mirando SOLO si el motivo empieza por "DEJO PASAR".

Hoy hay decisiones que DEJAN PASAR y cuyo motivo NO empieza por "DEJO PASAR":
  · "documento libre"                          (un .md no es codigo: se deja pasar)
  · "veredicto del equipo cubre el archivo"    (el equipo ya lo miro: se deja pasar)

Si el registro las apunta como FRENO, el registro MIENTE: dice que el candado paro cuando en
realidad dejo trabajar. Esta vigia comprueba que esas dos decisiones quedan apuntadas como
DEJO PASAR en la linea del registro.

COMO NO ENSUCIA EL REGISTRO DE VERDAD:
  · monkeypatch sobre _ruta_sin_equipo  -> la libreta al reves va a tmp_path
  · monkeypatch sobre la ruta del registro -> se reescribe el modulo para que AQUI apunte a
    tmp_path, asi memoria/DECISIONES_CANDADO.log del proyecto NO se toca.

No toca ningun otro archivo: solo lee el registro temporal que la propia prueba crea.
"""
import os
import sys

import pytest


# La raiz del proyecto es la carpeta que contiene a `arnes/` y a `vigias/`.
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)


# ---------------------------------------------------------------------------
# Utilidades de la vigia
# ---------------------------------------------------------------------------

def _cargar_candado():
    """Importa arnes/candado_equipo.py sin depender de que ya este importado."""
    import importlib
    return importlib.import_module("arnes.candado_equipo")


def _lineas_del_registro(ruta_registro):
    """Devuelve las lineas no vacias del registro de decisiones."""
    if not os.path.exists(ruta_registro):
        return []
    with open(ruta_registro, "r", encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]


def _ultima_linea(ruta_registro):
    """Devuelve la ultima linea escrita en el registro, o "" si no hay ninguna."""
    lineas = _lineas_del_registro(ruta_registro)
    return lineas[-1] if lineas else ""


def _preparar_registro_temporal(monkeypatch, tmp_path):
    """Desvia la libreta al reves Y el registro de decisiones a tmp_path.

    Devuelve la ruta del registro temporal para poder leerlo.

    Se hace de dos formas porque son dos cosas distintas:
      1) _ruta_sin_equipo() es una funcion: se sustituye por una que devuelve un archivo
         dentro de tmp_path (monkeypatch.setattr sobre el modulo).
      2) La ruta del registro se calcula dentro de _apuntar_frenada con
         os.path.join(AQUI, "memoria", "DECISIONES_CANDADO.log"): para desviarla se cambia
         el atributo AQUI del modulo a tmp_path, de modo que el join caiga en la carpeta
         temporal. Asi NO se toca memoria/DECISIONES_CANDADO.log del proyecto.
    """
    candado = _cargar_candado()

    # 1) La libreta al reves -> tmp_path
    ruta_libreta = tmp_path / "SIN_EQUIPO.log"
    monkeypatch.setattr(candado, "_ruta_sin_equipo", lambda: str(ruta_libreta))

    # 2) El registro de decisiones -> tmp_path/memoria/DECISIONES_CANDADO.log
    monkeypatch.setattr(candado, "AQUI", str(tmp_path))

    return str(tmp_path / "memoria" / "DECISIONES_CANDADO.log")


# ---------------------------------------------------------------------------
# Las dos pruebas que pide la tarea
# ---------------------------------------------------------------------------

def test_documento_libre_se_apunta_como_dejo_pasar(monkeypatch, tmp_path):
    """Un documento libre DEJA PASAR: el registro tiene que decir DEJO PASAR, no FRENO.

    Un .md no es codigo: el candado lo deja pasar. Si el registro lo apunta como FRENO,
    el registro miente y Julio no puede auditar por donde se trabajo de verdad.
    """
    candado = _cargar_candado()
    ruta_registro = _preparar_registro_temporal(monkeypatch, tmp_path)

    candado._apuntar_frenada("C:/Ingeniero_VUC/notas/ley.md", "documento libre")

    linea = _ultima_linea(ruta_registro)
    assert linea, "el registro de decisiones quedo vacio: no se apunto nada"
    assert "DEJO PASAR" in linea, (
        "un documento libre DEJA PASAR y el registro tiene que decirlo; "
        "la linea quedo asi: %r" % linea
    )
    assert "FRENO" not in linea, (
        "el registro apunto FRENO para una decision que deja pasar: %r" % linea
    )
    assert "documento libre" in linea, (
        "el motivo tiene que quedar en el registro; la linea quedo asi: %r" % linea
    )


def test_veredicto_del_equipo_cubre_el_archivo_se_apunta_como_dejo_pasar(monkeypatch, tmp_path):
    """Un veredicto del equipo que cubre el archivo DEJA PASAR: el registro lo tiene que decir.

    Cuando el equipo ya miro el archivo, el candado deja trabajar. Esa decision es un DEJO PASAR
    aunque su motivo no empiece por esas palabras. Si el registro la apunta como FRENO, miente.
    """
    candado = _cargar_candado()
    ruta_registro = _preparar_registro_temporal(monkeypatch, tmp_path)

    candado._apuntar_frenada(
        "C:/Ingeniero_VUC/arnes/candado_equipo.py",
        "veredicto del equipo cubre el archivo",
    )

    linea = _ultima_linea(ruta_registro)
    assert linea, "el registro de decisiones quedo vacio: no se apunto nada"
    assert "DEJO PASAR" in linea, (
        "un veredicto del equipo que cubre el archivo DEJA PASAR y el registro tiene que decirlo; "
        "la linea quedo asi: %r" % linea
    )
    assert "FRENO" not in linea, (
        "el registro apunto FRENO para una decision que deja pasar: %r" % linea
    )
    assert "veredicto del equipo cubre el archivo" in linea, (
        "el motivo tiene que quedar en el registro; la linea quedo asi: %r" % linea
    )


# ---------------------------------------------------------------------------
# Comprobaciones de apoyo: el registro no se ensucia y el formato se respeta
# ---------------------------------------------------------------------------

def test_el_registro_de_verdad_no_se_toca(monkeypatch, tmp_path):
    """La prueba escribe en tmp_path: memoria/DECISIONES_CANDADO.log del proyecto no cambia.

    Es la leccion del diccionario envenenado: una prueba NUNCA puede escribir en la memoria
    de verdad. Aqui se comprueba que la ruta desviada es la temporal y que la de verdad no
    se crea ni se modifica por culpa de esta vigia.
    """
    candado = _cargar_candado()
    ruta_registro = _preparar_registro_temporal(monkeypatch, tmp_path)

    ruta_de_verdad = os.path.join(AQUI, "memoria", "DECISIONES_CANDADO.log")
    existia_antes = os.path.exists(ruta_de_verdad)
    tam_antes = os.path.getsize(ruta_de_verdad) if existia_antes else None

    candado._apuntar_frenada("C:/Ingeniero_VUC/notas/ley.md", "documento libre")

    assert os.path.exists(ruta_registro), "la prueba no escribio en su registro temporal"
    assert os.path.abspath(ruta_registro).startswith(os.path.abspath(str(tmp_path))), (
        "el registro temporal no esta dentro de tmp_path: %r" % ruta_registro
    )
    if existia_antes:
        assert os.path.getsize(ruta_de_verdad) == tam_antes, (
            "la prueba escribio en el registro de verdad: %r" % ruta_de_verdad
        )
    else:
        assert not os.path.exists(ruta_de_verdad), (
            "la prueba creo el registro de verdad: %r" % ruta_de_verdad
        )


def test_la_linea_del_registro_tiene_los_cuatro_datos(monkeypatch, tmp_path):
    """El registro guarda cuatro datos separados por barra: cuando | archivo | que | por que.

    Sin los cuatro datos no se puede auditar. Esta comprobacion evita que un cambio futuro
    deje el registro a medias y nadie se entere.
    """
    candado = _cargar_candado()
    ruta_registro = _preparar_registro_temporal(monkeypatch, tmp_path)

    candado._apuntar_frenada("C:/Ingeniero_VUC/notas/ley.md", "documento libre")

    linea = _ultima_linea(ruta_registro)
    partes = [p.strip() for p in linea.split("|")]
    assert len(partes) == 4, (
        "la linea del registro tiene que tener cuatro datos separados por barra; "
        "quedo asi: %r" % linea
    )
    cuando, archivo, que, motivo = partes
    assert cuando, "falta la fecha en la linea del registro: %r" % linea
    assert archivo, "falta el archivo en la linea del registro: %r" % linea
    assert que in ("DEJO PASAR", "FRENO"), (
        "la decision tiene que ser DEJO PASAR o FRENO; quedo: %r" % que
    )
    assert motivo, "falta el motivo en la linea del registro: %r" % linea


def test_un_freno_de_verdad_sigue_apuntandose_como_freno(monkeypatch, tmp_path):
    """Control: un motivo que NO deja pasar se sigue apuntando como FRENO.

    Sin este control, una vigia que solo mira los DEJO PASAR podria pasar aunque el registro
    hubiera dejado de distinguir. Aqui se comprueba que la palabra FRENO sigue existiendo.
    """
    candado = _cargar_candado()
    ruta_registro = _preparar_registro_temporal(monkeypatch, tmp_path)

    candado._apuntar_frenada(
        "C:/Ingeniero_VUC/arnes/candado_equipo.py",
        "FRENO: crear codigo nuevo sin veredicto del equipo",
    )

    linea = _ultima_linea(ruta_registro)
    assert "FRENO" in linea, (
        "un freno de verdad tiene que seguir apuntandose como FRENO; quedo: %r" % linea
    )
    assert "DEJO PASAR" not in linea, (
        "un freno de verdad no puede apuntarse como DEJO PASAR; quedo: %r" % linea
    )


def test_la_libreta_al_reves_tambien_va_a_temporal(monkeypatch, tmp_path):
    """La libreta al reves (SIN_EQUIPO.log) tambien se desvia a tmp_path.

    _apuntar_frenada escribe DOS sitios: la libreta al reves y el registro de decisiones.
    Los dos tienen que ir a la carpeta temporal o la prueba ensucia el proyecto.
    """
    candado = _cargar_candado()
    _preparar_registro_temporal(monkeypatch, tmp_path)

    candado._apuntar_frenada("C:/Ingeniero_VUC/notas/ley.md", "documento libre")

    ruta_libreta = tmp_path / "SIN_EQUIPO.log"
    assert ruta_libreta.exists(), (
        "la libreta al reves no se escribio en tmp_path: %r" % str(ruta_libreta)
    )
    contenido = ruta_libreta.read_text(encoding="utf-8")
    assert "documento libre" in contenido, (
        "la libreta al reves no guardo el motivo; quedo: %r" % contenido
    )


if __name__ == "__main__":
    # Permite lanzar la vigia a mano: python vigias/test_vigia_el_registro_del_candado_no_miente.py
    sys.exit(pytest.main([os.path.abspath(__file__), "-v"]))
