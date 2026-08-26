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
    python ingeniero.py duda "<lo que no se>" --proyecto dmm
                                                     -> busca la respuesta ANTES de preguntar
    python ingeniero.py fallos                       -> lo que ya nos paso, para no repetirlo
    python ingeniero.py cuotas                       -> a que cerebro le toca ahora
    python ingeniero.py buscar-skill "<que necesitas>"     -> ¿ya existe? (propia/proyectos/libreria)
    python ingeniero.py crear-skill <nombre> "<que hace>"  -> la crea el cerebro GRATIS
    python ingeniero.py vigias dmm                   -> corre las vigias del proyecto
    python ingeniero.py mapa                         -> refresca el mapa
    python ingeniero.py proyectos                    -> a quien atiende
"""
import os, sys, subprocess, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

# MOSTRAR NO PUEDE TUMBAR UN TRABAJO YA HECHO (fallo real 2026-08-25).
# Se lanzo al equipo, el equipo CONTESTO, y el mando murio al IMPRIMIR la respuesta:
#   UnicodeEncodeError: 'charmap' codec can't encode character ' ' in position 1178
# La consola de Windows usa cp1252 y la respuesta traia un espacio fino, que ahi no existe.
# Dos danos, y el segundo es el caro: un traceback en la cara de Julio (fallo ya apuntado), y
# SE PERDIO EL TRABAJO, porque la llave del equipo se guarda DESPUES de imprimir. Un caracter
# invisible costo la llamada entera y hubo que pagarla otra vez.
# Ahora, si un caracter no se puede dibujar, se dibuja como se pueda; pero no se tira lo hecho.
for _salida in ("stdout", "stderr"):
    try:
        getattr(sys, _salida).reconfigure(errors="replace")
    except Exception:
        pass
from cerebro import router, grafo          # noqa: E402
from cuerpo import estado, obrero, cuotas, fallos, subagentes, consejeros, dudas, skills as hab  # noqa: E402
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
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        try:
            import candado_prueba_real as _pr
            _ev = _pr.hay_prueba_real(d.get("proyecto"), d.get("problema"))
        except Exception:
            _ev = None
        if not _ev:
            print("PARADO: falta la PRUEBA REAL interna (con el equipo, con Playwright) que")
            print("       demuestre que el objetivo se cumple. NO se le pide a Julio que pruebe todavia.")
            print("       Cuando este lista y en verde: python arnes/candado_prueba_real.py marcar <proyecto> \"<objetivo>\"")
        else:
            print("SIGUIENTE PASO: la prueba real interna esta en verde y con equipo. Pedirle a")
            print("   Julio que pruebe CON SUS OJOS: python ingeniero.py pedir-prueba")
    else:
        print("SIGUIENTE PASO: sellar el cambio y limpiar el estado.")
    return 0


def trabaja(apodo, problema):
    pk = router.armar(apodo, problema)
    txt = router.a_texto(pk)
    # INDEXACION (reparacion 2026-08-24): cada paquete se apunta en el cuaderno de acierto.
    # Sin esto el router nunca aprende que le falta, y se repiten las instrucciones y se pierde
    # contexto. Antes esto solo lo hacia el subagente, no este comando (fallo real 2026-08-24).
    try:
        from cuerpo import medidor
        medidor.apuntar_paquete(pk, txt)
    except Exception:
        pass
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
    # FALLO REAL (2026-08-24): si el proyecto no tenia carpeta `vigias/`, esto se rendia y el
    # paso "vigias antes/despues" del protocolo quedaba EN BLANCO. Foto Informe las tiene
    # sueltas en la raiz (test_vigia_*.py), asi que en todo un dia de reparaciones nunca se
    # supo de que color estaban antes ni despues. Un paso del protocolo que no se puede
    # cumplir no se cumple: se salta y nadie lo nota.
    carpeta = os.path.join(raiz, "vigias")
    if os.path.isdir(carpeta):
        objetivo = ["vigias/"]
    else:
        objetivo = sorted(f for f in os.listdir(raiz)
                          if f.startswith("test_vigia_") and f.endswith(".py"))
        if not objetivo:
            print(f"NO_ENCONTRADO: {apodo} no tiene vigias (ni carpeta vigias/ ni "
                  f"test_vigia_*.py en la raiz)")
            return 1
        print(f"  ({apodo} no tiene carpeta vigias/: se corren sus {len(objetivo)} "
              f"test_vigia_*.py de la raiz)")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"] + objetivo,
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
    if cmd == "equipo" and len(sys.argv) >= 4:
        # SIEMPRE EL EQUIPO (Julio, 2026-08-21, tras repetirlo tres veces y pagarlo).
        # Uno genera, OTRO distinto audita. Claude dirige y lee el veredicto: nada mas.
        # Deja la llave que abre el candado de escribir codigo.
        import sys as _s
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        from cerebro import router as _r
        from cuerpo import obrero as _o
        import candado_equipo as _ce
        proy, tarea = sys.argv[2], " ".join(sys.argv[3:])
        paq = _r.armar(proy, tarea)
        # el TEXTO, no la caja: trabajar espera el texto del paquete (fix 2026-08-24)
        res = _o.trabajar(_r.a_texto(paq), tarea)
        # PRIMERO SE GUARDA, DESPUES SE ENSENA (fallo real 2026-08-25).
        # Antes se imprimia justo aqui y la llave se guardaba al final. El equipo contesto, el
        # print murio por un caracter que la consola de Windows no sabia dibujar, y el trabajo YA
        # PAGADO se perdio entero: no se guardo nada y hubo que volver a llamar. Lo que cuesta
        # dinero se asegura ANTES de ensenarlo. Mostrar es lo ultimo y ya no puede tumbar nada.
        if "_error" in res:
            print(_o.veredicto_corto(res))
            return 1
        prop = res.get("propuesta") or {}
        tocados = prop.get("archivo") or prop.get("archivos") or []
        if isinstance(tocados, str):
            tocados = [tocados]
        # tambien valen las piezas que el paquete trajo: es lo que el equipo tuvo delante.
        # FALLO REAL (2026-08-24): esto buscaba "piezas" y el paquete NO usa ese nombre, usa
        # "fichas" (medido: fichas=39, piezas=None). Como el obrero gratis casi siempre devuelve
        # NO_ENCONTRADO en proyectos grandes, la llave quedaba en ['NO_ENCONTRADO'] y no abria
        # nada: no se podia tocar ni una vigia recien escrita del mismo proyecto. El candado del
        # equipo se volvia un muro en vez de una puerta con llave.
        for clave in ("fichas", "piezas"):
            for pz in (paq.get(clave) if isinstance(paq, dict) else []) or []:
                pid = pz.get("id") if isinstance(pz, dict) else str(pz)
                if pid and pid not in tocados:
                    tocados.append(pid)
        _ce.guardar_veredicto(tarea, tocados, res.get("obrero"), res.get("auditor"),
                              (res.get("auditoria") or {}).get("veredicto", "?"))
        # Ya esta a salvo. AHORA se ensena, y si mostrar falla, no se pierde nada.
        try:
            print(_o.veredicto_corto(res))
        except Exception as _e:
            print("(el veredicto llego y quedo guardado, pero no se pudo mostrar entero: %s)"
                  % str(_e)[:90])
        print()
        print("LLAVE GUARDADA: se puede escribir en %d archivo(s) durante %d min."
              % (len(tocados), _ce.VIGENCIA_MIN))
        return 0

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
    if cmd == "duda" and len(sys.argv) >= 3:
        args = sys.argv[2:]; proy = None
        if "--proyecto" in args:
            i = args.index("--proyecto"); proy = args[i+1]; args = args[:i] + args[i+2:]
        d = " ".join(args)
        r = dudas.resolver(d, proy)
        print(dudas.informe(r))
        if r["hay_que_preguntar"]:
            dudas.apuntar_pregunta(d, proy)
            print()
            print(dudas.formular(d, r))
            print("  (apuntada: el candado de cierre no deja terminar hasta hacersela a Julio)")
        return 0
    if cmd in ("ruta", "mapa-trabajo"):
        from cerebro import protocolo
        print(protocolo.mapa())
        return 0
    if cmd == "paso":
        from cerebro import protocolo
        print(protocolo.ahora())
        return 0
    if cmd == "metodo" and len(sys.argv) >= 3:
        from cerebro import protocolo
        for r in protocolo.buscar_en_el_metodo(" ".join(sys.argv[2:])):
            print("  [%s] %-34s %s" % (r["proyecto"], r["donde"], r["titulo"][:70]))
        return 0
    if cmd == "causa" and len(sys.argv) >= 3:
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candado_diagnostico as cd
        a = sys.argv[2:]
        def _v(n):
            return a[a.index(n) + 1] if n in a and len(a) > a.index(n) + 1 else ""
        r = cd.declarar(a[0], _v("--archivo"), _v("--funcion"), _v("--linea"),
                        _v("--evidencia"), _v("--cambio"), _v("--sintoma"))
        if "_error" in r:
            print(r["_error"])
            return 1
        if "_aviso" in r:
            print("CAUSA RAIZ declarada, PERO:\n  " + r["_aviso"])
        else:
            print("CAUSA RAIZ declarada. Ya se puede reparar.")
        return 0
    if cmd == "protocolo":
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candado_diagnostico as cd
        print(open(os.path.join(AQUI, "PROTOCOLO_UNICO.md"), encoding="utf-8")
              .read().split("## LOS 8 PASOS")[0])
        pasos = [
            ("1 ¿Estoy donde debo?", "via_canonica.py"),
            ("2 Buscar solo lo necesario", "read_gate.py"),
            ("3 Causa raiz, no sintoma", "candado_diagnostico.py"),
            ("4 Agotar las fuentes antes de preguntar", "candado_preguntar.py"),
            ("5 Confirmar el objetivo antes de construir", "candado_protocolo.py"),
            ("6 Plan cerrado y reparacion minima", "edit_gate_universal.py"),
            ("7 La prueba la manda la realidad", "candado_cierre.py"),
            ("8 Legislar, sellar y aprender", "../sellar.sh"),
        ]
        print("LOS 8 PASOS Y SU CANDADO:")
        falta = 0
        for nombre, arch in pasos:
            hay = os.path.exists(os.path.join(AQUI, "arnes", arch))
            if not hay:
                falta += 1
            print("  [%s] %-44s %s" % ("OK " if hay else "FALTA", nombre, arch))
        print()
        print(cd.texto())
        if falta:
            print()
            print("*** %d paso(s) SIN candado. Un paso sin candado es un paso que se salta." % falta)
        return 0 if not falta else 2
    if cmd == "objetivo-confirmado":
        # LA LLAVE QUE EL CANDADO YA OFRECIA Y NO EXISTIA.
        # Es la segunda vez que pasa (la primera fue NECESITO_EDITAR): un candado que manda usar
        # una llave inexistente no protege, ATRAPA, y empuja a apagar el arnes entero, que es
        # justo lo peor. Un candado sin forma honrada de cumplirlo esta mal puesto.
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candado_protocolo as _cp
        sem = _cp._semaforo()
        os.makedirs(os.path.dirname(sem), exist_ok=True)
        que = " ".join(sys.argv[2:]).strip()
        open(sem, "w", encoding="utf-8").write(
            time.strftime("%Y-%m-%d %H:%M") + "  " + (que or "(objetivo confirmado con Julio)"))
        print("OBJETIVO CONFIRMADO. Se puede construir durante 3 horas.")
        if que:
            print("  lo que Julio consigue: " + que)
        return 0
    if cmd == "necesito-editar" and len(sys.argv) >= 3:
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import permiso_editar
        a = sys.argv[2:]
        def _v(n):
            return a[a.index(n) + 1] if n in a and len(a) > a.index(n) + 1 else ""
        r = permiso_editar.dar(a[0], _v("--motivo"), _v("--vigia"), _v("--dana"))
        print(r["_error"] if "_error" in r else
              "PERMISO dado para " + r["nombre"] + " (30 min). Queda apuntado.")
        return 1 if "_error" in r else 0
    if cmd == "autorizar-off":
        # SOLO Julio apaga los candados, por este comando y con autorizacion escrita (2026-08-24).
        # Antes bastaba prender INGENIERO_OFF y cualquiera los apagaba en silencio.
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import autorizacion
        motivo = " ".join(sys.argv[2:]).strip() or "autorizado por Julio"
        marca = autorizacion.autorizar(motivo)
        print("CANDADOS APAGADOS por autorizacion de Julio (vigente 24h).")
        print("  motivo: " + motivo)
        print("  evidencia: " + marca)
        return 0
    if cmd == "permisos":
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import permiso_editar
        print(permiso_editar.texto()); return 0
    if cmd == "medir":
        from cuerpo import medidor, respuestas
        print(medidor.texto(sys.argv[2] if len(sys.argv) > 2 else None))
        print()
        print(respuestas.texto())
        return 0
    if cmd == "respondio" and len(sys.argv) >= 3:
        # se apunta QUE se pregunto y QUE contesto Julio; nace SIN EVALUAR
        from cuerpo import respuestas, estado
        p, _, r = " ".join(sys.argv[2:]).partition("::")
        n = respuestas.apuntar(p.strip(), r.strip())
        estado.respondida(p.strip())
        print("apuntada la respuesta #%d (SIN evaluar todavia)" % n["id"])
        if n["repitio_a"]:
            print("  *** OJO: Julio ya habia explicado esto. Las anteriores quedan NO_SIRVIO:")
            for x in n["repitio_a"]:
                print("      - " + x[:90])
        return 0
    if cmd in ("respuesta-ok", "respuesta-mal", "respuesta-aclarar") and len(sys.argv) >= 3:
        from cuerpo import respuestas
        # ACLARAR no es NO_SIRVIO (Julio, 2026-08-20): la respuesta era CORRECTA, solo hay que
        # argumentarla de otra manera. Confundirlas hace que se cambie lo que ya estaba bien.
        res = {"respuesta-ok": "SIRVIO", "respuesta-mal": "NO_SIRVIO",
               "respuesta-aclarar": "ACLARAR"}[cmd]
        r = respuestas.evaluar(" ".join(sys.argv[2:]), res, "lo dijo Julio")
        print(("marcada como " + res) if r else "NO_ENCONTRADO: no hay ninguna respuesta asi")
        return 0
    if cmd == "probado" and len(sys.argv) >= 4:
        # SOLO Julio marca esto (Ley 5): ninguna IA puede darlo por bueno
        from cuerpo import medidor
        m = medidor.marcar_prueba_humana(sys.argv[2], " ".join(sys.argv[3:]))
        print("marcado como PROBADO POR JULIO" if m else "NO_ENCONTRADO: no hay medicion de eso")
        return 0
    if cmd == "pruebareal":
        # B2 (legislacion 2026-08-24): deja la evidencia de una prueba real interna.
        return subprocess.call([sys.executable,
                                os.path.join(AQUI, "arnes", "candado_prueba_real.py"),
                                "marcar"] + sys.argv[2:])
    if cmd == "pedir-prueba":
        # B2: pedirle a Julio que pruebe con sus ojos SOLO si hay prueba real fresca, verde y con equipo.
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candado_prueba_real as _pr
        from cuerpo import estado as _estado
        d = _estado.leer()
        if not _pr.hay_prueba_real(d.get("proyecto"), d.get("problema")):
            sys.stderr.write(_pr.MENSAJE)
            return 2
        print("LISTO: la prueba real interna esta en verde y con equipo. Pedirle a Julio que pruebe con sus ojos.")
        return 0
    if cmd == "fallos":
        print(fallos.texto()); return 0
    if cmd == "verificar":
        return subprocess.call([sys.executable, os.path.join(AQUI, "verificar.py")]
                               + [a for a in sys.argv[2:]])
    if cmd == "cuotas":
        print(cuotas.estado_texto()); return 0
    if cmd in ("candados-medicion", "medir-candados"):
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import candados_medicion
        print(candados_medicion.resumen()); return 0
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
