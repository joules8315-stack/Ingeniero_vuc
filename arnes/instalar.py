# -*- coding: utf-8 -*-
"""arnes/instalar.py — ENCHUFA el Ingeniero a un proyecto (actual o futuro).

Deja en el proyecto tres cosas, sin tocar su codigo:
  1) CLAUDE.md          — la regla fija: aqui se trabaja con paquete, no leyendo todo
  2) .claude/settings.json — el HOOK del candado de lectura (esto es lo que OBLIGA)
  3) .claude/rules/ahorro.md — el recordatorio, con paths para que casi no pese

Es reversible: `python arnes/instalar.py <proyecto> --quitar`.
No pisa nada: si el proyecto ya tiene CLAUDE.md, agrega su parte al final marcada.
"""
import os, sys, json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
from cerebro import grafo  # noqa: E402

MARCA_INI = "<!-- INGENIERO_VUC:INICIO -->"
MARCA_FIN = "<!-- INGENIERO_VUC:FIN -->"

BLOQUE = MARCA_INI + """
## AHORRO DE TOKENS — lo pone el Ingeniero VUC (C:\Ingeniero_VUC)

**No se lee este proyecto entero. Se pide el paquete minimo.**

Ante cualquier problema, PRIMERO:
```
cd C:\Ingeniero_VUC; python ingeniero.py trabaja {apodo} "<el problema en palabras de Julio>"
```
Eso entrega la ley que manda, las piezas con su boca, los trozos exactos (`archivo:linea-linea`),
las vigias que protegen y a quien se puede danar. Ese paquete es TODO el material permitido.

Si falta algo, se PIDE asi (no se abre por cuenta propia):
```
NECESITO_LEER:
  archivo: <ruta>   motivo: <que responde>   decide: <que desbloquea>   riesgo: <si no lo leo>
```

Leyes: nunca asumir · nunca inventar (`NO_ENCONTRADO`) · vigia verde NO es prueba (la prueba es
que Julio lo vea) · no romper vecinos · hablarle simple y con el comando listo para PowerShell.
""" + MARCA_FIN

REGLA = """---
paths:
  - "**/*.py"
  - "**/*.html"
---
# Antes de abrir un archivo grande

Este proyecto esta enchufado al Ingeniero VUC. Un archivo de miles de lineas no se abre entero:
se pide su trozo. Si el candado te frena, no lo rodees — pide el paquete:

```
cd C:\Ingeniero_VUC; python ingeniero.py trabaja {apodo} "<el problema>"
```
"""


# EL MODO INGENIERO PARA CLINE (Julio, 2026-09-02): "el asunto principal es que todo lo que
# trabaje debe estar en modo ingeniero. No es una sugerencia: asi, y solo asi debe trabajar."
# Se deja en `.clinerules/modo_ingeniero.md` de CADA proyecto, porque Cline lee esas reglas
# dentro del proyecto y asi ningun trabajo se hace fuera del arnes.
CLINE_BLOQUE = """# MODO INGENIERO — reglas fijas de Cline en este proyecto (las pone el Ingeniero VUC).

Toda orden que Julio de aqui arranca por el MODO INGENIERO. El Ingeniero es el arnes de cualquier
IA: toma la orden y repara. No es una sugerencia: asi, y solo asi debe trabajar.

0. NUNCA TRABAJAR A SOLAS (lo mas importante). Para tocar CODIGO, PRIMERO se corre el equipo:
     cd C:\\Ingeniero_VUC; python ingeniero.py equipo {apodo} "<la tarea>"
   Uno GENERA, OTRO distinto AUDITA (nadie se aprueba a si mismo). Si el candado te bloquea,
   NO lo rodees ni lo ignores: pasa por el equipo. No se escribe codigo a solas en ningun proyecto.
1. NUNCA ASUMIR. Si algo no esta escrito, se PREGUNTA (PREGUNTA_REQUERIDA) o se escribe NO_ENCONTRADO.
   Jamas se adivina.
2. NO LEER EL PROYECTO ENTERO. Se pide el paquete minimo:
     cd C:\\Ingeniero_VUC; python ingeniero.py trabaja {apodo} "<el problema>"
   Lo que falte se pide con NECESITO_LEER. El candado de lectura frena lo demas.
3. VIGIA VERDE NO ES PRUEBA: la prueba es que Julio lo vea funcionar con sus ojos. Ninguna IA se
   autocertifica.
4. NO ROMPER VECINOS. Antes de tocar se mira "A QUIEN PUEDE DANAR" del paquete.
5. A JULIO SE LE HABLA SIMPLE, sin jerga, y el comando siempre listo para PowerShell (`;`, no `&&`).
6. SI SE PIERDE EL CONTEXTO, NO SE SIGUE A CIEGAS. Se para y se dice que hacer para retomar.

Cuando Julio mande algo: se arranca por el Ingeniero (paquete + equipo), no por cuenta propia.
"""


def instalar(apodo, quitar=False):
    prs = grafo.proyectos()
    if apodo not in prs:
        print(f"NO_ENCONTRADO: '{apodo}' no esta en proyectos.config")
        return 1
    raiz = prs[apodo]["ruta"]
    if not os.path.isdir(raiz):
        print(f"NO_ENCONTRADO: no existe {raiz}")
        return 1

    # 1) CLAUDE.md
    md = os.path.join(raiz, "CLAUDE.md")
    actual = open(md, encoding="utf-8").read() if os.path.exists(md) else ""
    limpio = actual
    if MARCA_INI in actual:
        limpio = actual[:actual.index(MARCA_INI)] + actual[actual.index(MARCA_FIN) + len(MARCA_FIN):]
    nuevo = limpio.rstrip() if quitar else (limpio.rstrip() + "\n\n" + BLOQUE.format(apodo=apodo) + "\n")
    if nuevo.strip():
        open(md, "w", encoding="utf-8").write(nuevo.lstrip() + "\n")
        print(("QUITADO de " if quitar else "PUESTO en ") + md)
    elif os.path.exists(md):
        os.remove(md); print("BORRADO (quedaba vacio):", md)

    # 2) hook en .claude/settings.json
    d = os.path.join(raiz, ".claude")
    os.makedirs(d, exist_ok=True)
    sj = os.path.join(d, "settings.json")
    cfg = {}
    if os.path.exists(sj):
        try:
            cfg = json.load(open(sj, encoding="utf-8"))
        except Exception:
            cfg = {}
    hooks = cfg.setdefault("hooks", {})
    pre = hooks.setdefault("PreToolUse", [])
    pre = [e for e in pre if "read_gate.py" not in json.dumps(e)]
    if not quitar:
        pre.append({"matcher": "Read", "hooks": [hook_cfg()]})
    hooks["PreToolUse"] = pre
    if not pre:
        hooks.pop("PreToolUse", None)
    if not hooks:
        cfg.pop("hooks", None)
    json.dump(cfg, open(sj, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(("QUITADO el candado de " if quitar else "CANDADO DE LECTURA puesto en ") + sj)

    # 3) regla por ruta
    rd = os.path.join(d, "rules")
    os.makedirs(rd, exist_ok=True)
    rr = os.path.join(rd, "ahorro_ingeniero.md")
    if quitar:
        if os.path.exists(rr):
            os.remove(rr); print("QUITADA la regla", rr)
    else:
        open(rr, "w", encoding="utf-8").write(REGLA.format(apodo=apodo))
        print("REGLA puesta en", rr)

    # 4) EL MODO INGENIERO PARA CLINE (Julio, 2026-09-02): sin esto, Cline no tiene reglas fuera
    #    de Ingeniero_VUC y trabaja sin arnes en los proyectos de Julio. Se deja `.clinerules/`
    #    dentro del proyecto para que Cline SIEMPRE lea el modo ingeniero aqui.
    crd = os.path.join(raiz, ".clinerules")
    os.makedirs(crd, exist_ok=True)
    cr = os.path.join(crd, "modo_ingeniero.md")
    if quitar:
        if os.path.exists(cr):
            os.remove(cr); print("QUITADO modo ingeniero de Cline", cr)
    else:
        open(cr, "w", encoding="utf-8").write(CLINE_BLOQUE.format(apodo=apodo))
        print("MODO INGENIERO DE CLINE puesto en", cr)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("Proyectos:", ", ".join(grafo.proyectos()))
        sys.exit(1)
    sys.exit(instalar(sys.argv[1], "--quitar" in sys.argv))
