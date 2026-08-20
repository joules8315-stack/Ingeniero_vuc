# -*- coding: utf-8 -*-
"""arnes/via_canonica.py — LO PRIMERO QUE SE COMPRUEBA (orden de Julio, 2026-08-20).

  "que todas las rutas, ramas, vias canonicas, siempre se cumplan, que sea lo primero que
   verifique el ingeniero, que este trabajando donde debe, no en una version equivoca,
   y que guarde alli sus commit"

POR QUE EXISTE ESTO — fallo real encontrado ese mismo dia:
    C:\\MVP\\Foto_informe--main                        rama main    ultimo commit 28-MAYO   57 archivos
    C:\\Users\\USER\\dev\\Foto_info_repo\\Foto_informe--main  integration  ultimo commit 23-JULIO 253 archivos
    C:\\Users\\USER\\Foto_informe--main                  (vacia)
El Ingeniero apuntaba a la de MAYO. Todas las pruebas se hicieron contra una version dos meses
vieja. Reparar ahi habria sido tirar el trabajo a la basura: se arregla una copia que nadie usa.

QUE COMPRUEBA, EN ESTE ORDEN:
  1. La ruta declarada EXISTE.
  2. Es un repositorio git y esta en la RAMA declarada.
  3. No hay GEMELOS: otras carpetas con el mismo proyecto. Si los hay, dice cual es el mas
     nuevo y AVISA si el declarado no es ese.
  4. El commit no esta rancio comparado con su gemelo.

Se puede correr solo:  python arnes/via_canonica.py [apodo]
"""
import os, sys, subprocess, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

# Donde buscar copias gemelas. Se busca por NOMBRE de carpeta, que es como se cuelan.
DONDE_BUSCAR = [r"C:\MVP", r"C:\Users\USER\dev", r"C:\Users\USER", r"C:\\"]


def _git(ruta, *args):
    try:
        r = subprocess.run(["git", "-C", ruta] + list(args),
                           capture_output=True, text=True, timeout=20)
        return (r.stdout or "").strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def rama_de(ruta):
    return _git(ruta, "rev-parse", "--abbrev-ref", "HEAD") or "SIN-GIT"


def ultimo_commit(ruta):
    """(hash corto, fecha AAAA-MM-DD) o ('', '')."""
    s = _git(ruta, "log", "-1", "--format=%h|%cs")
    if "|" in s:
        h, f = s.split("|", 1)
        return h, f
    return "", ""


def hay_cambios_sin_guardar(ruta):
    return bool(_git(ruta, "status", "--porcelain"))


def gemelos(ruta_buena):
    """Otras carpetas por ahi con el MISMO nombre: las copias que confunden."""
    nombre = os.path.basename(os.path.normpath(ruta_buena)).lower()
    fuera = []
    vistos = {os.path.normcase(os.path.abspath(ruta_buena))}
    for base in DONDE_BUSCAR:
        if not os.path.isdir(base):
            continue
        try:
            for hijo in os.listdir(base):
                cand = os.path.join(base, hijo)
                if not os.path.isdir(cand):
                    continue
                clave = os.path.normcase(os.path.abspath(cand))
                if hijo.lower() == nombre and clave not in vistos:
                    vistos.add(clave)
                    fuera.append(cand)
                # una carpeta contenedora, como dev\Foto_info_repo\Foto_informe--main
                dentro = os.path.join(cand, os.path.basename(os.path.normpath(ruta_buena)))
                cl2 = os.path.normcase(os.path.abspath(dentro))
                if os.path.isdir(dentro) and cl2 not in vistos:
                    vistos.add(cl2)
                    fuera.append(dentro)
        except Exception:
            continue
    return fuera


def revisar(apodo, ruta, rama_declarada):
    """Devuelve (estado, avisos). estado: OK / AVISO / BLOQUEO."""
    avisos = []

    if not os.path.isdir(ruta):
        return "BLOQUEO", [f"la ruta declarada NO EXISTE: {ruta}",
                           "arreglalo en proyectos.config antes de tocar nada"]

    rama = rama_de(ruta)
    h, fecha = ultimo_commit(ruta)

    if rama == "SIN-GIT":
        avisos.append("no es repositorio git: no se puede guardar el trabajo con commits aqui")
        estado = "AVISO"
    elif rama_declarada and rama != rama_declarada:
        return "BLOQUEO", [
            f"estas en la rama '{rama}' y la canonica es '{rama_declarada}'",
            f'arreglalo: cd "{ruta}"; git switch {rama_declarada}',
            "guardar commits en la rama equivocada es perder el trabajo"]
    else:
        estado = "OK"

    # GEMELOS: la trampa de verdad
    otros = gemelos(ruta)
    if otros:
        mio = fecha or "0000-00-00"
        mas_nuevo, fecha_nuevo = None, mio
        detalle = []
        for o in otros:
            ho, fo = ultimo_commit(o)
            ro = rama_de(o)
            n = len([x for x in os.listdir(o)]) if os.path.isdir(o) else 0
            detalle.append(f"      {o}  [rama {ro} · commit {fo or '-'} · {n} cosas]")
            if fo and fo > fecha_nuevo:
                mas_nuevo, fecha_nuevo = o, fo
        avisos.append(f"HAY {len(otros)} COPIA(S) de este proyecto en el disco:")
        avisos += detalle
        if mas_nuevo:
            estado = "BLOQUEO"
            avisos.append(f"  *** LA COPIA DECLARADA ES MAS VIEJA ({mio}) que {mas_nuevo} ({fecha_nuevo})")
            avisos.append("  *** Reparar aqui seria arreglar una version que nadie usa.")
            avisos.append(f"  *** Decide cual es la buena y ponla en proyectos.config: {apodo} = <ruta> | <rama> | <marca>")
        else:
            avisos.append("  (la declarada es la mas nueva: bien, pero conviene borrar las copias)")

    if hay_cambios_sin_guardar(ruta) and rama != "SIN-GIT":
        avisos.append("hay cambios SIN GUARDAR aqui (git status no esta limpio)")
        if estado == "OK":
            estado = "AVISO"

    return estado, avisos


def revisar_todos(solo=None):
    from cerebro import grafo
    salida = []
    for apodo, d in grafo.proyectos().items():
        if solo and apodo != solo:
            continue
        estado, avisos = revisar(apodo, d["ruta"], d.get("rama", ""))
        salida.append((apodo, d["ruta"], estado, avisos))
    return salida


def texto(solo=None):
    L = ["VIA CANONICA — lo primero que se comprueba (¿estoy trabajando donde debo?)"]
    hay_bloqueo = False
    for apodo, ruta, estado, avisos in revisar_todos(solo):
        marca = {"OK": "[ OK ]", "AVISO": "[AVISO]", "BLOQUEO": "[BLOQUEO]"}[estado]
        L.append(f"  {marca} {apodo:14} {ruta}")
        for a in avisos:
            L.append(f"          {a}")
        if estado == "BLOQUEO":
            hay_bloqueo = True
    if hay_bloqueo:
        L.append("")
        L.append("  *** NO SE TOCA NADA hasta arreglar los BLOQUEO de arriba.")
        L.append("  *** Reparar en la copia equivocada es tirar el trabajo a la basura.")
    return "\n".join(L)


def esta_limpio(solo=None):
    return not any(e == "BLOQUEO" for _, _, e, _ in revisar_todos(solo))


if __name__ == "__main__":
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    print(texto(solo))
    sys.exit(0 if esta_limpio(solo) else 2)
