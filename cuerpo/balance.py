# -*- coding: utf-8 -*-
"""Balance del trabajo: cuenta cuantos trabajos hizo el equipo y cuantos a mano, las rondas y el gasto de la tanda."""
import json
import os


def _ruta(nombre):
    """Devuelve la ruta del cuaderno, usando la variable de entorno si esta puesta."""
    var = {
        "BALANCE.log": "INGENIERO_BALANCE_BALANCE",
        "TRABAJOS_DEL_EQUIPO.log": "INGENIERO_BALANCE_EQUIPO",
        "GASTO.json": "INGENIERO_BALANCE_GASTO",
    }.get(nombre)
    if var and os.environ.get(var):
        return os.environ[var]
    return os.path.join("memoria", nombre)


def _leer_balance():
    """Cuenta equipo y a_mano desde el cuaderno de balance."""
    ruta = _ruta("BALANCE.log")
    equipo = 0
    a_mano = 0
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith("equipo | "):
                    equipo += 1
                elif linea.startswith("a_mano | "):
                    a_mano += 1
    except (FileNotFoundError, OSError):
        pass
    return equipo, a_mano


def _leer_rondas():
    """Cuenta las rondas del equipo: cada renglon con letras es una ronda."""
    ruta = _ruta("TRABAJOS_DEL_EQUIPO.log")
    rondas = 0
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                if any(c.isalpha() for c in linea):
                    rondas += 1
    except (FileNotFoundError, OSError):
        pass
    return rondas


def _leer_gasto():
    """Lee el gasto de la tanda desde GASTO.json."""
    ruta = _ruta("GASTO.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos.get("contador", 0)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return 0


def reparto(proyecto=None):
    """Devuelve el reparto: equipo, a_mano, rondas_equipo y gasto_tanda."""
    equipo, a_mano = _leer_balance()
    rondas = _leer_rondas()
    gasto = _leer_gasto()
    return {
        "equipo": equipo,
        "a_mano": a_mano,
        "rondas_equipo": rondas,
        "gasto_tanda": gasto,
    }


def texto(proyecto=None):
    """Devuelve el balance en palabras simples para Julio."""
    r = reparto()
    return (
        f"El equipo hizo {r['equipo']} trabajos y a mano se hicieron {r['a_mano']}. "
        f"Las rondas del equipo fueron {r['rondas_equipo']} y el gasto de la tanda es {r['gasto_tanda']}."
    )


def apuntar(clase, trabajo):
    """Anade un renglon al cuaderno de balance. Si no se puede, se queda callada."""
    if clase not in ("equipo", "a_mano"):
        return
    ruta = _ruta("BALANCE.log")
    try:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(f"{clase} | {trabajo}\n")
    except OSError:
        pass
