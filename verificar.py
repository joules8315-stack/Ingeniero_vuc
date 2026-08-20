# -*- coding: utf-8 -*-
"""verificar.py — EL CANDADO CONTRA ASUMIR (orden 7 de Julio, 2026-08-20).

  "Verifica de esto que existe, que falta... Nunca asumas, crea candado para esto."

Lee `ORDENES.md` (cada orden de Julio, textual) y comprueba UNA POR UNA contra el disco.
Nadie —ni Claude, ni Qwen, ni Gemini— puede decir "ya esta" sin que el disco lo confirme.

    python verificar.py            -> la tabla de que existe y que falta
    python verificar.py --vigias   -> ademas corre las vigias nombradas (mas lento, mas seguro)

Lo que Julio tiene que ver con sus ojos sale aparte, marcado, y NUNCA lo marca una IA.
"""
import os, re, sys, subprocess, importlib

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
ORDENES = os.path.join(AQUI, "ORDENES.md")


def _leer_ordenes():
    out = []
    seccion = ""
    for ln in open(ORDENES, encoding="utf-8").read().splitlines():
        s = ln.strip()
        if s.startswith("## "):
            seccion = s[3:].strip()
            continue
        # OJO: acepta T1.1 y tambien M.1 (sin numero antes del punto). Con el patron viejo
        # las tres ordenes que SOLO Julio puede dar por buenas quedaban invisibles, y el
        # verificador decia "0 pendientes de Julio" cuando habia 3. Justo lo que no debe pasar.
        m = re.match(r"^([TM]\d*\.\d+)\s*\|\s*(.+?)\s*\|\s*(.+)$", s)
        if m:
            out.append({"id": m.group(1), "orden": m.group(2),
                        "comprobacion": m.group(3), "seccion": seccion})
    return out


def _comprobar(c, correr_vigias=False):
    """Devuelve (estado, detalle). estado: HECHO / FALTA / JULIO / ROTO."""
    tipo, _, resto = c.partition(":")
    tipo = tipo.strip()

    if tipo == "archivo":
        r = os.path.join(AQUI, resto.strip())
        return ("HECHO", resto.strip()) if os.path.exists(r) else ("FALTA", "no existe " + resto.strip())

    if tipo == "funcion":
        mod, _, fn = resto.partition(":")
        try:
            m = importlib.import_module(mod.strip())
            return ("HECHO", f"{mod}.{fn}") if hasattr(m, fn.strip()) else \
                   ("FALTA", f"{mod} no tiene {fn}")
        except Exception as e:
            return "ROTO", f"{mod}: {str(e)[:70]}"

    if tipo == "texto":
        arch, _, palabra = resto.partition(":")
        r = os.path.join(AQUI, arch.strip())
        if not os.path.exists(r):
            return "FALTA", "no existe " + arch.strip()
        txt = open(r, encoding="utf-8", errors="ignore").read()
        return ("HECHO", f"{arch} dice '{palabra[:28]}'") if palabra.strip() in txt else \
               ("FALTA", f"{arch} no dice '{palabra[:28]}'")

    if tipo == "vigia":
        r = os.path.join(AQUI, "vigias", resto.strip())
        if not os.path.exists(r):
            return "FALTA", "no existe la vigia " + resto.strip()
        if not correr_vigias:
            return "HECHO", resto.strip() + " (existe; con --vigias se comprueba que este verde)"
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "vigias/" + resto.strip()],
                           cwd=AQUI, capture_output=True, text=True)
        return ("HECHO", resto.strip() + " VERDE") if p.returncode == 0 else \
               ("ROTO", resto.strip() + " ROJA")

    if tipo == "manual":
        return "JULIO", resto.strip()

    return "ROTO", "comprobacion no entendida: " + c


def main():
    correr = "--vigias" in sys.argv
    ordenes = _leer_ordenes()
    por_estado = {"HECHO": 0, "FALTA": 0, "ROTO": 0, "JULIO": 0}
    seccion = ""
    faltan = []

    print("VERIFICACION DE LAS ORDENES DE JULIO — nada se da por hecho sin mirar el disco")
    print("=" * 92)
    for o in ordenes:
        if o["seccion"] != seccion:
            seccion = o["seccion"]
            print()
            print("## " + seccion)
        estado, detalle = _comprobar(o["comprobacion"], correr)
        por_estado[estado] = por_estado.get(estado, 0) + 1
        marca = {"HECHO": "[HECHO]", "FALTA": "[ FALTA ]", "ROTO": "[ ROTO ]", "JULIO": "[JULIO]"}[estado]
        print(f"  {marca} {o['id']:6} {o['orden'][:62]}")
        if estado in ("FALTA", "ROTO"):
            print(f"           -> {detalle}")
            faltan.append((o["id"], o["orden"], detalle))

    print()
    print("=" * 92)
    total = len(ordenes) - por_estado["JULIO"]
    print(f"HECHO: {por_estado['HECHO']}/{total}   FALTA: {por_estado['FALTA']}   "
          f"ROTO: {por_estado['ROTO']}   SOLO JULIO PUEDE DARLO POR BUENO: {por_estado['JULIO']}")
    if faltan:
        print()
        print("LO QUE FALTA (esto es lo siguiente, no hay que preguntarselo a nadie):")
        for i, (id_, orden, det) in enumerate(faltan, 1):
            print(f"  {i}. {id_} {orden}")
    if por_estado["JULIO"]:
        print()
        print("NINGUNA IA puede marcar lo de arriba: es la prueba de Julio (ley 5).")
    return 1 if (por_estado["FALTA"] or por_estado["ROTO"]) else 0


if __name__ == "__main__":
    sys.exit(main())
