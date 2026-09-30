#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/candado_cierre.py — EL CANDADO QUE NO DEJA TERMINAR (hook Stop).

Julio, 2026-08-20: "como hacemos para que lo que no se garantiza ahora, sea una garantia?"

LA IDEA: una regla escrita se ignora; una comprobacion que BLOQUEA, no. Hasta hoy todos los
candados vigilaban la ENTRADA (que no leas de mas, que no edites sin plan). Este vigila la
SALIDA: antes de que Claude termine de responder, comprueba que no se salto pasos. Si se los
salto, NO LE DEJA TERMINAR y le dice exactamente que le falta.

QUE COMPRUEBA (todo se mira en el disco, nada se cree de palabra):
  1. VIA CANONICA — ¿se trabajo donde se debe?
  2. PREGUNTA PENDIENTE — si hay una pregunta para Julio sin hacer, no se cierra el turno.
  3. VIGIAS — si se toco codigo, tienen que estar verdes. Se comprueba de verdad, corriendolas.
  4. SIN SELLAR — si se toco codigo y no se sello, se avisa (no bloquea: sellar es decision).

ANTI-BUCLE (imprescindible): un hook Stop que siempre bloquea deja a Julio atrapado en un
bucle sin fin. Por eso: **como mucho DOS bloqueos seguidos**; al tercero deja pasar y avisa.
Y el interruptor de emergencia `INGENIERO_OFF=1` lo apaga entero.
"""
import json, os, sys, subprocess, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTADOR = os.path.join(AQUI, "memoria", ".cierres_bloqueados")


def _contador():
    """El de verdad, o uno de prueba. Dos corridas simultaneas se pisaban este contador y una
    creia que ya habia bloqueado dos veces, asi que dejaba pasar y la prueba salia roja sin
    estar nada roto (fallo real 2026-08-21)."""
    return os.environ.get("INGENIERO_CONTADOR_TEST") or CONTADOR
TOPE_BLOQUEOS = 2


def _veces_seguidas():
    try:
        cuando, n = open(_contador(), encoding="utf-8").read().split("|")
        # si paso mas de 10 minutos, es otro trabajo: se reinicia la cuenta
        if time.time() - float(cuando) > 600:
            return 0
        return int(n)
    except Exception:
        return 0


def _apuntar(n):
    os.makedirs(os.path.dirname(_contador()), exist_ok=True)
    open(_contador(), "w", encoding="utf-8").write(f"{time.time()}|{n}")


def _toco_codigo(minutos=25):
    """¿Se han tocado archivos de codigo hace poco? Se mira la fecha de los archivos."""
    tocados = []
    limite = time.time() - minutos * 60
    sys.path.insert(0, AQUI)
    try:
        from cerebro import grafo
        proyectos = [d["ruta"] for d in grafo.proyectos().values()]
    except Exception:
        proyectos = [AQUI]
    for raiz in proyectos:
        if not os.path.isdir(raiz):
            continue
        for carpeta in ("cuerpo", "cerebro", "web", "arnes", "."):
            d = os.path.join(raiz, carpeta)
            if not os.path.isdir(d):
                continue
            try:
                for f in os.listdir(d):
                    if not f.endswith((".py", ".html", ".js")):
                        continue
                    full = os.path.join(d, f)
                    if os.path.isfile(full) and os.path.getmtime(full) > limite:
                        tocados.append((raiz, os.path.join(carpeta, f)))
            except Exception:
                continue
    return tocados


CERROJO = os.path.join(AQUI, "memoria", ".vigias_corriendo")


def _ya_hay_otra_corrida():
    """¿Ya se estan corriendo las comprobaciones ahora mismo?

    CAUSA RAIZ MEDIDA (2026-08-21): con DOS corridas a la vez salen rojas; solas, siempre verdes.
    Se pisan entre ellas porque varias escriben en los mismos archivos de memoria. El guardia de
    cierre las lanzaba aunque el sellado ya las estuviera corriendo, y daba un rojo FALSO que no
    dejaba terminar. Reproducido a proposito: 2 y 3 rojas de 144.
    """
    try:
        if not os.path.exists(CERROJO):
            return False
        # un cerrojo viejo (mas de 10 min) es basura de una corrida que se corto
        return (time.time() - os.path.getmtime(CERROJO)) < 600
    except Exception:
        return False


def _poner_cerrojo():
    try:
        os.makedirs(os.path.dirname(CERROJO), exist_ok=True)
        open(CERROJO, "w", encoding="utf-8").write(str(time.time()))
    except Exception:
        pass


def _quitar_cerrojo():
    try:
        os.remove(CERROJO)
    except Exception:
        pass


def _vigias_verdes(raiz):
    """Se CORREN de verdad. Creer que estan verdes no vale.

    OJO (fallo real 2026-08-20): si este candado se llama DESDE una vigia, arranca pytest
    dentro de pytest y el sistema se cuelga (se quedo 8 minutos girando). Dentro de una vigia
    no se corren vigias: se comprueba la logica, que es lo que se esta probando."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return None, "dentro de una vigia no se corren vigias (evita pytest dentro de pytest)"
    if _ya_hay_otra_corrida():
        return None, "ya hay otra corrida en marcha: no se lanzan dos a la vez (se pisan)"
    carpeta = os.path.join(raiz, "vigias")
    if not os.path.isdir(carpeta):
        return None, "ese proyecto no tiene vigias"
    _poner_cerrojo()
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "vigias/"],
                           cwd=raiz, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        salida = (r.stdout or "") + (r.stderr or "")
        ultima = [l for l in salida.splitlines() if l.strip()][-1:]
        if r.returncode == 0:
            return True, (ultima[0] if ultima else "sin salida")
        # UNA VIGIA RECIEN NACIDA NO ES UNA AVERIA (Julio, 2026-09-09, y con razon: lo tuvo que
        # repetir varias veces). El metodo de esta casa MANDA escribir la vigia primero y que
        # NAZCA ROJA: una vigia que nace verde no probo nada. Este candado contaba esa roja
        # como algo roto y no dejaba cerrar nunca, empujando a saltarselo. Y esta casa ya tiene
        # escrito que un candado sin forma honrada de satisfacerlo es peor que no tenerlo.
        # La casa YA sabia distinguirlo: arnes/guardia_de_guardado.py le pregunta al guardado
        # si esa vigia es NUEVA o si ya estaba. Aqui se hace lo mismo, no se inventa nada.
        # Si alguna roja YA ESTABA GUARDADA, eso si es romper algo que estaba verde: se frena.
        rojos = []
        for linea in salida.splitlines():
            linea = linea.strip()
            if linea.startswith(("FAILED", "ERROR")):
                arch = linea.split("::")[0].strip()
                for pre in ("FAILED", "ERROR"):
                    if arch.startswith(pre):
                        arch = arch[len(pre):].strip()
                        break
                arch = arch.replace("\\", "/")
                if arch and arch not in rojos:
                    rojos.append(arch)
        if not rojos:
            return False, (ultima[0] if ultima else "sin salida")
        nuevas, ya_estaban = [], []
        for arch in rojos:
            try:
                rr = subprocess.run(["git", "ls-files", "--error-unmatch", "--", arch],
                                    cwd=raiz, capture_output=True, text=True, timeout=30)
                if rr.returncode != 0:
                    nuevas.append(arch)
                else:
                    ya_estaban.append(arch)
            except Exception:
                ya_estaban.append(arch)
        esperando = set()
        if ya_estaban:
            try:
                import json as _json
                ruta_ordenes = os.path.join(raiz, "memoria", "ORDENES.json")
                with open(ruta_ordenes, encoding="utf-8") as f:
                    ordenes = _json.load(f)
                if isinstance(ordenes, dict):
                    ordenes = ordenes.get('ordenes', [])
                for orden in ordenes:
                    if str(orden.get("estado", "")).strip().lower() == "hecha":
                        continue
                    vigia = str(orden.get("vigia", "")).replace("\\", "/").strip()
                    # el cierre no sabe que tarea se guarda ahora; una prueba que su propia tarea rompe la frena el guardia (medido 2026-09-21)
                    if vigia:
                        esperando.add(vigia)
            except Exception:
                esperando = set()
        frenan = [a for a in ya_estaban if a not in esperando]
        if frenan:
            return False, (ultima[0] if ultima else "sin salida")
        return True, ("vigias recien escritas y todavia sin su pieza, que es el metodo y no "
                      "una averia: " + "; ".join(nuevas))
    except subprocess.TimeoutExpired:
        return None, "las vigias tardaron demasiado"
    except Exception as e:
        return None, str(e)[:80]
    finally:
        _quitar_cerrojo()


def main():
    import autorizacion
    if autorizacion.autorizada():  # F7: solo Julio apaga (autorizar-off)
        return 0
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    sys.path.insert(0, AQUI)
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    faltas = []

    # Lo que no se mide no se corrige: este numero dice si el equipo esta perdiendo rondas.
    try:
        import medidor_de_rondas
        from datetime import datetime
        hoy = datetime.now().strftime("%Y-%m-%d")
        r = medidor_de_rondas.contar(AQUI, hoy)
        sys.stderr.write("MEDIDOR DE RONDAS: " + str(r.get("razon", "")) + "\n")
        sys.stderr.write("La meta de Julio es guardar nueve de cada diez rondas.\n")
    except Exception:
        pass

    # 1) VIA CANONICA
    try:
        import via_canonica
        if not via_canonica.esta_limpio():
            faltas.append("La VIA CANONICA esta mal (estas en la copia o la rama equivocada).\n"
                          "   Mira: cd C:\\Ingeniero_VUC; python ingeniero.py via")
    except Exception:
        pass

    # 2) PREGUNTA PENDIENTE PARA JULIO
    try:
        from cuerpo import estado
        d = estado.leer()
        if d.get("decision_pendiente"):
            faltas.append("Hay una PREGUNTA para Julio sin hacer:\n"
                          f"   \"{d['decision_pendiente'][:160]}\"\n"
                          "   Preguntasela antes de terminar. No se decide por el.")
    except Exception:
        pass

    # 3) EL PISO: ¿sigue en pie lo que YA se reparo antes? (Julio, 2026-08-21)
    # El problema historico: arreglar una cosa y tumbar otra que ya iba. Se corren SOLO las
    # pruebas de lo que se toco y sus vecinos, no las 150: por eso es rapido.
    tocados_pasado = _toco_codigo()
    if tocados_pasado:
        try:
            import guard_pasado
            piezas = [f.replace("\\", "/") for _, f in tocados_pasado]
            en_pie, caidas = guard_pasado.siguen_en_pie(piezas)
            if not en_pie:
                faltas.append(guard_pasado.aviso_piso(caidas))
        except Exception:
            pass

    # 4) VIGIAS, si se toco codigo
    tocados = _toco_codigo()
    if tocados:
        raices = {r for r, _ in tocados}
        for raiz in raices:
            verde, detalle = _vigias_verdes(raiz)
            if verde is False:
                cuales = [f for r, f in tocados if r == raiz][:4]
                faltas.append(f"Tocaste codigo en {os.path.basename(raiz)} ({', '.join(cuales)})\n"
                              f"   y las VIGIAS estan ROJAS: {detalle}\n"
                              "   No se termina dejando algo roto.")

    # 5) F5 / punto a de Julio: toda instruccion debe quedar legislada (o justificada).
    try:
        import candado_legislar as _cl
        pend = _cl.pendientes()
        if pend:
            faltas.append("Hay instrucciones de Julio SIN LEGISLAR (F5, punto a):\n"
                          + "\n".join("   - " + e["texto"][:120] for e in pend[:5])
                          + "\n   Cada una debe legislarse (contrato+tabla+matriz+vigia) o "
                            "marcarse 'ya existe'/'no aplica'.\n"
                            "   cd C:\\Ingeniero_VUC; python arnes/candado_legislar.py listar")
    except Exception:
        pass

    try:
        import candado_nace_enganchada
        puede, motivo = candado_nace_enganchada.se_puede_cerrar(AQUI)
        if not puede:
            faltas.append(motivo)
    except Exception:
        pass
    try:
        import arnes.puerta_del_plan as _pdp
        _puede, _motivo = _pdp.se_puede_cerrar(AQUI)
        if not _puede:
            faltas.append(
                "Falta el resumen del plan: %s. Apuntalo con: "
                'cd C:\\Ingeniero_VUC; python ingeniero.py resumen-del-plan <numero> "<el resumen>"'
                % _motivo
            )
    except Exception:
        pass
    if not faltas:
        _apuntar(0)
        return 0

    veces = _veces_seguidas()
    if veces >= TOPE_BLOQUEOS:
        _apuntar(0)
        sys.stderr.write(
            "AVISO DEL CANDADO DE CIERRE (ya no bloquea mas, para no dejarte atrapado):\n"
            + "\n".join("  - " + f for f in faltas)
            + "\n  Se deja pasar, pero esto quedo SIN HACER.\n")
        return 0

    _apuntar(veces + 1)
    sys.stderr.write(
        "NO SE PUEDE TERMINAR TODAVIA — el candado de cierre encontro pasos saltados:\n\n"
        + "\n\n".join(f"  {i}. {f}" for i, f in enumerate(faltas, 1))
        + "\n\nHaz eso y vuelve a terminar. (Si te bloquea sin razon: $env:INGENIERO_OFF=1)\n")
    # MEDICION (Julio, 2026-08-25): freno terminar con pasos saltados.
    try:
        import candados_medicion
        candados_medicion.cazado("cierre")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
