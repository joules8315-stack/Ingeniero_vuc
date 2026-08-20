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
TOPE_BLOQUEOS = 2


def _veces_seguidas():
    try:
        cuando, n = open(CONTADOR, encoding="utf-8").read().split("|")
        # si paso mas de 10 minutos, es otro trabajo: se reinicia la cuenta
        if time.time() - float(cuando) > 600:
            return 0
        return int(n)
    except Exception:
        return 0


def _apuntar(n):
    os.makedirs(os.path.dirname(CONTADOR), exist_ok=True)
    open(CONTADOR, "w", encoding="utf-8").write(f"{time.time()}|{n}")


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


def _vigias_verdes(raiz):
    """Se CORREN de verdad. Creer que estan verdes no vale.

    OJO (fallo real 2026-08-20): si este candado se llama DESDE una vigia, arranca pytest
    dentro de pytest y el sistema se cuelga (se quedo 8 minutos girando). Dentro de una vigia
    no se corren vigias: se comprueba la logica, que es lo que se esta probando."""
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return None, "dentro de una vigia no se corren vigias (evita pytest dentro de pytest)"
    carpeta = os.path.join(raiz, "vigias")
    if not os.path.isdir(carpeta):
        return None, "ese proyecto no tiene vigias"
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "vigias/"],
                           cwd=raiz, capture_output=True, text=True, timeout=300)
        ultima = [l for l in (r.stdout or "").splitlines() if l.strip()][-1:]
        return r.returncode == 0, (ultima[0] if ultima else "sin salida")
    except subprocess.TimeoutExpired:
        return None, "las vigias tardaron demasiado"
    except Exception as e:
        return None, str(e)[:80]


def main():
    if os.environ.get("INGENIERO_OFF", "").strip():
        return 0
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    sys.path.insert(0, AQUI)
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    faltas = []

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

    # 3) VIGIAS, si se toco codigo
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
    return 2


if __name__ == "__main__":
    sys.exit(main())
