# -*- coding: utf-8 -*-
"""ingeniero.py — EL MANDO UNICO del Ingeniero VUC.

Julio no repite instrucciones: dice el problema y el Ingeniero hace el resto del protocolo.

    python ingeniero.py via                          -> ¿estoy en la ruta y rama correctas? (LO PRIMERO)
    python ingeniero.py arranca                      -> donde ibamos
    python ingeniero.py trabaja dmm "el onboarding no guarda el perfil"
    python ingeniero.py resolver dmm "<problema>"    -> lo resuelve el cerebro GRATIS (Qwen+Gemini)
    python ingeniero.py cruzado dmm "<problema>"     -> uno repara, OTRO escribe la vigia, un 3o juzga
    python ingeniero.py resultado                    -> como va / que dijeron (sin esperar)
    python ingeniero.py verificar                    -> que esta hecho y que falta (sin asumir)
    python ingeniero.py consejo "<decision>" --proyecto dmm --porque "<tu razon>"
                                                     -> que opinan OTROS modelos de tu decision
    python ingeniero.py fallos                       -> lo que ya nos paso, para no repetirlo
    python ingeniero.py cuotas                       -> a que cerebro le toca ahora
    python ingeniero.py buscar-skill "<que necesitas>"     -> ¿ya existe? (propia/proyectos/libreria)
    python ingeniero.py crear-skill <nombre> "<que hace>"  -> la crea el cerebro GRATIS
    python ingeniero.py vigias dmm                   -> corre las vigias del proyecto
    python ingeniero.py mapa                         -> refresca el mapa
    python ingeniero.py proyectos                    -> a quien atiende
"""
import os, sys, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from cerebro import router, grafo          # noqa: E402
from cuerpo import estado, obrero, cuotas, fallos, subagentes, consejeros, skills as hab  # noqa: E402
sys.path.insert(0, os.path.join(AQUI, 'arnes'))
import via_canonica                        # noqa: E402


def arranca():
    # LO PRIMERO SIEMPRE: ¿estoy donde debo? (Ley 14)
    print(via_canonica.texto())
    print()
    print(estado.texto())
    print()
    d = estado.leer()
    if d["decision_pendiente"]:
        print("PARADO: hay una pregunta sin responder. No se sigue hasta que Julio conteste.")
    elif not d["problema"]:
        print('SIGUIENTE PASO: python ingeniero.py trabaja <proyecto> "<el problema>"')
    elif not d["vigias_antes"]:
        print(f"SIGUIENTE PASO: correr las vigias ANTES de tocar, para saber de que color estan:")
        print(f"   python ingeniero.py vigias {d['proyecto']} antes")
    elif not d["vigias_despues"]:
        print("SIGUIENTE PASO: reparar SOLO con el paquete vigente (no abrir nada mas),")
        print(f"   y despues: python ingeniero.py vigias {d['proyecto']} despues")
    elif d["prueba_humana"] == "PENDIENTE":
        print("SIGUIENTE PASO: que Julio lo pruebe CON SUS OJOS. Una vigia verde NO cuenta.")
    else:
        print("SIGUIENTE PASO: sellar el cambio y limpiar el estado.")
    return 0


def trabaja(apodo, problema):
    pk = router.armar(apodo, problema)
    txt = router.a_texto(pk)
    os.makedirs(router.PAQUETES, exist_ok=True)
    slug = "".join(c if c.isalnum() else "_" for c in problema.lower())[:40]
    destino = os.path.join(router.PAQUETES, f"{apodo}__{slug}.md")
    open(destino, "w", encoding="utf-8").write(txt)
    n = len(txt.splitlines())

    estado.apuntar(proyecto=apodo, problema=problema, paquete=destino,
                   flujos=[f for f, _ in pk["flujos"]], prueba_humana="PENDIENTE",
                   vigias_antes="", vigias_despues="")

    print(f"PAQUETE  : {destino}")
    print(f"  {n} lineas  (el proyecto tiene {pk['total_proyecto']:,})  "
          f"AHORRO {100 - n*100/max(1,pk['total_proyecto']):.1f}%")
    print(f"  flujos : {', '.join(f'{f}({p})' for f, p in pk['flujos']) or 'NO_ENCONTRADO'}")
    if not pk["leyes"]:
        print("  AVISO  : este asunto NO tiene contrato. Se legisla ANTES de tocar codigo.")
    if not pk["vigias"]:
        print("  AVISO  : este asunto NO tiene vigia. Se escribe la vigia PRIMERO.")
    print(f"  a quien puede danar: {len(pk['dana'])} piezas (van en el paquete)")
    print()
    print("REGLA: se trabaja SOLO con ese paquete. Lo que falte, se PIDE con NECESITO_LEER.")
    return 0


def vigias(apodo, cuando="antes"):
    prs = grafo.proyectos()
    if apodo not in prs:
        print(f"NO_ENCONTRADO: {apodo}")
        return 1
    raiz = prs[apodo]["ruta"]
    carpeta = os.path.join(raiz, "vigias")
    if not os.path.isdir(carpeta):
        print(f"NO_ENCONTRADO: {apodo} no tiene carpeta vigias/")
        return 1
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "vigias/"],
                       cwd=raiz, capture_output=True, text=True)
    ultima = [l for l in (r.stdout or "").splitlines() if l.strip()][-1:]
    resumen = ultima[0] if ultima else "sin salida"
    print(f"VIGIAS de {apodo} ({cuando}): {resumen}")
    estado.apuntar(**{f"vigias_{cuando}": resumen})
    return 0 if r.returncode == 0 else 1


def resolver(apodo, problema):
    """El VOLUMEN lo hace el cerebro GRATIS, no Claude (CONTRATO_MAESTRO_AHORRO).
    Qwen genera -> Gemini audita (4 ojos) -> aqui solo se imprime el VEREDICTO."""
    trabaja(apodo, problema)
    d = estado.leer()
    pk = open(d["paquete"], encoding="utf-8").read()
    print()
    print(cuotas.estado_texto())
    print()
    print("Trabajando... (el cerebro gratis puede tardar unos minutos; no gasta tokens de Claude)")
    r = obrero.trabajar(pk, problema)
    print()
    print(obrero.veredicto_corto(r))
    crudo = os.path.join(os.path.dirname(d["paquete"]), "VEREDICTO_" + os.path.basename(d["paquete"]))
    import json as _j
    open(crudo, "w", encoding="utf-8").write(_j.dumps(r, ensure_ascii=False, indent=1))
    print()
    print("detalle completo (por si hace falta):", crudo)
    p_ = (r.get("propuesta") or {}).get("preguntas") or []
    if p_:
        estado.apuntar(decision_pendiente="; ".join(p_))
        print()
        print("*** PARADO: el obrero necesita que Julio decida algo. Apuntado en el ESTADO.")
    return 0


# Comandos que TOCAN un proyecto: antes de nada, hay que estar donde se debe.
TOCAN_PROYECTO = ("trabaja", "resolver", "cruzado", "vigias", "buscar-skill", "crear-skill")


def _via_ok(cmd, apodo=None):
    """LO PRIMERO (Ley 14): ¿estoy en la ruta y la rama que mandan? Si no, no se toca nada.
    Reparar en la copia equivocada es tirar el trabajo a la basura (fallo real 2026-08-20:
    el Ingeniero apuntaba a una copia de Foto Informe de MAYO habiendo una de JULIO)."""
    if cmd not in TOCAN_PROYECTO:
        return True
    if not via_canonica.esta_limpio(apodo):
        print(via_canonica.texto(apodo))
        print()
        print("PARADO: primero se arregla la via canonica. No se trabaja en la version equivocada.")
        return False
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    apodo = sys.argv[2] if len(sys.argv) > 2 and cmd in TOCAN_PROYECTO else None
    if not _via_ok(cmd, apodo):
        return 2
    if cmd == "via":
        print(via_canonica.texto(sys.argv[2] if len(sys.argv) > 2 else None))
        return 0 if via_canonica.esta_limpio() else 2
    if cmd == "arranca":
        return arranca()
    if cmd == "trabaja" and len(sys.argv) >= 4:
        return trabaja(sys.argv[2], " ".join(sys.argv[3:]))
    if cmd == "resolver" and len(sys.argv) >= 4:
        return resolver(sys.argv[2], " ".join(sys.argv[3:]))
    if cmd == "buscar-skill" and len(sys.argv) >= 3:
        print(hab.informe(hab.buscar(" ".join(sys.argv[2:])))); return 0
    if cmd == "crear-skill" and len(sys.argv) >= 4:
        r = hab.crear(sys.argv[2], " ".join(sys.argv[3:]), forzar="--forzar" in sys.argv)
        if "_error" in r:
            print("NO SE CREO:", r["_error"])
            if r.get("informe"): print(); print(r["informe"])
            return 1
        print("CREADA:", r["creada"], "(la escribio", r["por"] + ")")
        print(r["aviso"]); return 0
    if cmd == "cruzado" and len(sys.argv) >= 4:
        # NO BLOQUEA: se lanza al fondo y Julio sigue con lo suyo. La latencia de los cerebros
        # gratis va de 5s a 305s y no la controlamos; lo que si podemos es no hacerle esperar.
        proy, prob = sys.argv[2], " ".join(sys.argv[3:])
        d = subagentes.lanzar_al_fondo(proy, prob)
        estado.apuntar(proyecto=proy, problema=prob)
        print("LANZADO al fondo. No tienes que esperar aqui.")
        print("  uno repara, OTRO escribe la vigia sin verla, un tercero juzga.")
        print("  suele tardar entre 2 y 10 minutos (depende de como esten los servidores gratis).")
        print()
        print("Mira como va cuando quieras:")
        print("  cd C:\Ingeniero_VUC; python ingeniero.py resultado")
        return 0
    if cmd == "resultado":
        print(subagentes.estado())
        import glob as _g, json as _j
        listos = [f for f in _g.glob(os.path.join(subagentes.SALIDAS, "*.json"))
                  if not os.path.exists(f + ".corriendo")]
        if listos:
            ultimo = max(listos, key=os.path.getmtime)
            print()
            print(subagentes.veredicto(dict(_j.load(open(ultimo, encoding="utf-8")),
                                            archivo=ultimo)))
        return 0
    if cmd == "consejo" and len(sys.argv) >= 3:
        args = sys.argv[2:]
        proy = porque = None
        if "--proyecto" in args:
            i = args.index("--proyecto"); proy = args[i+1]; args = args[:i] + args[i+2:]
        if "--porque" in args:
            i = args.index("--porque"); porque = " ".join(args[i+1:]); args = args[:i]
        print(consejeros.informe(consejeros.consultar(" ".join(args), porque or "", proy)))
        return 0
    if cmd == "fallos":
        print(fallos.texto()); return 0
    if cmd == "verificar":
        return subprocess.call([sys.executable, os.path.join(AQUI, "verificar.py")]
                               + [a for a in sys.argv[2:]])
    if cmd == "cuotas":
        print(cuotas.estado_texto()); return 0
    if cmd == "vigias" and len(sys.argv) >= 3:
        return vigias(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "antes")
    if cmd == "proyectos":
        for a, p in grafo.proyectos().items():
            ok = "OK " if os.path.isdir(p["ruta"]) else "NO "
            print(f"  {ok} {a:14} {p['ruta']}")
        return 0
    if cmd == "mapa":
        return subprocess.call([sys.executable, os.path.join(AQUI, "mapa", "inventario.py")])
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
