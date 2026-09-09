# -*- coding: utf-8 -*-
"""arnes/asignador.py — EL COMPARADOR MANDA. La IA solo entra si sale ROJO, y no siempre.

DE DONDE SALE (Julio, 2026-09-08): "la revision se puede programar, dado que estamos esperando
un resultado especifico. Mejor crear un COMPARADOR: si no se logra, dice que no se logro, y
ahi si entra una IA a ver por que. Para eso debe tener la informacion pertinente de la pieza,
DEPURADA, no informacion irrelevante que haga bulto."

Y: "el que asigna ya debe tener la informacion pertinente completa: saber si la IA tiene
capacidad, si no esta dormida, diciendole claramente este es el resultado que queremos, se hizo
esto y no sirvio por esto, reparalo."

Y, apretando: "no solo que quepa, sino que venga LO NECESARIO, y no con peso innecesario".

LA CONTRADICCION QUE CAZO JULIO ANTES DE QUE ESTO SE CONSTRUYERA, y es la clave de todo:
"si nace roja, lo va a mandar para una IA, y no es asi; debe ser en la segunda vuelta".
El metodo de esta casa dice que LA VIGIA NACE ROJA A PROPOSITO. Si el criterio fuera
"rojo = llamar a una IA", cada prueba nueva dispararia una IA a reparar algo que todavia no
existe. Se estaria pagando por el paso 1 del propio metodo.

TODO LO QUE HAY AQUI SON CUENTAS. Este archivo NO llama a ningun cerebro: solo decide si hace
falta llamar, a quien, y con que. La IA la llama quien reciba esta decision.

LEY: CONTRATO_SIN_OBJETIVO_NO_SE_PIDE_NADA.md (reglas 5 y 6) y
     CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# Lo que aguanta el encargo entero. Los cerebros gratis medidos aguantan 19.042 y 20.169
# letras: con mas, se les salta a TODOS en silencio y acaba escribiendo y revisando el mismo
# cerebro de pago. Medido el 2026-09-08: eso costo dos o tres rondas por cada cambio.
TOPE_LETRAS = 19000

# Cuantas veces se le insiste al mismo cerebro antes de parar y avisar a Julio.
INTENTOS = 3


def leer_el_fallo(salida):
    """Saca de la salida de las pruebas QUE fallo y QUE tenia que pasar.

    EL OBJETIVO NO SE INVENTA: sale del propio mensaje de la vigia, que en esta casa se escribe
    diciendo que tenia que pasar ("NO SALE EL EMBUDO. Con 1000 de alcance y 100 clics ya se
    puede decir que de cada diez que lo vieron, uno entro"). Ese texto ES el objetivo.

    Devuelve {archivo, prueba, objetivo} o None si no se puede leer nada.
    """
    try:
        texto = str(salida or "")
        archivo = prueba = ""
        for linea in texto.splitlines():
            linea = linea.strip()
            if linea.startswith(("FAILED", "ERROR")):
                sin_marca = linea.split(None, 1)[1] if " " in linea else linea
                trozos = sin_marca.split("::")
                archivo = trozos[0].strip().replace("\\", "/")
                if len(trozos) > 1:
                    prueba = trozos[1].split()[0].strip()
                break
        if not archivo:
            return None
        # El objetivo: lo que dice el mensaje de la prueba al fallar.
        objetivo = ""
        for linea in texto.splitlines():
            tira = linea.strip()
            if tira.startswith("E ") or "AssertionError" in tira or "Failed:" in tira:
                objetivo = re.sub(r"^E\s+", "", tira)
                objetivo = re.sub(r"^\w*(AssertionError|Failed):\s*", "", objetivo).strip()
                if objetivo:
                    break
        return {"archivo": archivo, "prueba": prueba, "objetivo": objetivo or texto[:300]}
    except Exception:
        return None


def hay_que_llamar_a_alguien(salida, vigias_nuevas=None):
    """Hace falta una IA, o esta roja es el metodo funcionando?

    LA REGLA QUE CAZO JULIO: una vigia RECIEN NACIDA nace roja A PROPOSITO, porque se escribe
    ANTES que la pieza. Llamar a una IA ahi es pagar por el paso 1 del propio metodo, y encima
    la IA no encontraria nada que reparar: la pieza todavia no existe.

    Se llama SOLO si la vigia roja ya estaba guardada antes (o sea, estaba verde y se rompio).
    La lista de vigias nuevas la sabe el guardado: arnes/guardia_de_guardado.py ya se la
    pregunta a git.
    """
    try:
        fallo = leer_el_fallo(salida)
        if not fallo:
            return False
        nuevas = [str(v).replace("\\", "/") for v in (vigias_nuevas or [])]
        return fallo["archivo"] not in nuevas
    except Exception:
        return False


def elegir_cerebro(letras, evitar=None):
    """A QUIEN se le puede pedir, comprobandolo ANTES de gastar. Devuelve (quien, motivo).

    Se mira, en este orden y todo son cuentas:
      1. quien tiene llave       (cuerpo/obrero.py::quienes_hay)
      2. quien NO esta dormido   (cuerpo/cuotas.py::desperto)
      3. a quien le CABE         (cuerpo/cuotas.py::rankear, con lo MEDIDO, no lo declarado)
    Si no queda nadie, devuelve (None, motivo) y NO se gasta. Callarse y mandarlo igual es lo
    que hacia el sistema viejo: se les saltaba a todos en silencio y lo pagaba el de pago.
    """
    try:
        from cuerpo import cuotas, obrero
        con_llave = [q for q in obrero.quienes_hay() if q != evitar]
        if not con_llave:
            return None, "no hay ningun cerebro con llave puesta"
        despiertos = [q for q in con_llave if cuotas.desperto(q)]
        if not despiertos:
            return None, "todos los cerebros estan dormidos ahora mismo: se espera, no se gasta"
        caben = cuotas.rankear(despiertos, letras)
        if not caben:
            return None, ("el encargo pesa %d letras y no le cabe a ninguno de los que estan "
                          "despiertos: se recorta el encargo, no se gasta la vuelta" % letras)
        return caben[0], "tiene llave, esta despierto y le caben %d letras" % letras
    except Exception as e:
        return None, "no se pudo comprobar quien puede: %s" % str(e)[:90]


def armar_encargo(fallo, material, intento=1):
    """El encargo con LAS TRES COSAS. Depurado, pero SIN perder lo necesario.

    Ley: a nadie se le pide un trabajo sin decirle QUE tiene que conseguir, QUE hay ahora y
    QUE se espera de el.

    Y lo que aprieta Julio: recortar por lo bruto es trampa. Si al recortar se cae justo el
    trozo que hay que reparar, el encargo cabe y NO SIRVE PARA NADA. Por eso el recorte se hace
    por el FINAL del material, que es donde vive el relleno, conservando el trozo de la pieza.
    """
    f = fallo or {}
    cabecera = "\n".join([
        "OBJETIVO: esto es lo que tenia que pasar y no paso.",
        "  " + str(f.get("objetivo") or "(no se pudo leer el mensaje de la prueba)"),
        "",
        "LO QUE HAY: la prueba %s del archivo %s se pone ROJA."
        % (f.get("prueba") or "?", f.get("archivo") or "?"),
        "  Intento numero %d de %d." % (intento, INTENTOS),
        "",
        "TU PAPEL: repararlo. No expliques, repara: di el archivo, el texto de antes y el de",
        "  despues. Si te falta algo del material, escribe NO_ENCONTRADO y pidelo; no inventes.",
        "",
        "EL TROZO DE LA PIEZA:",
    ])
    sitio = TOPE_LETRAS - len(cabecera) - 200
    trozo = str(material or "")
    if len(trozo) > sitio:
        # El relleno esta al principio y lo necesario suele estar donde falla: se conserva el
        # FINAL, que es donde vive el trozo de la pieza. Y se avisa de que se recorto.
        trozo = ("... [se recorto el relleno del principio para que quepa]\n"
                 + trozo[-sitio:])
    return cabecera + "\n" + trozo


def decidir(salida, material="", vigias_nuevas=None, intento=1):
    """La decision entera, de una vez. Devuelve un diccionario que dice que hacer.

    NO llama a ningun cerebro: solo dice si hace falta, a quien, y con que encargo.
    """
    fallo = leer_el_fallo(salida)
    if not fallo:
        return {"llamar": False, "motivo": "no se pudo leer que fallo"}
    if not hay_que_llamar_a_alguien(salida, vigias_nuevas):
        return {"llamar": False, "fallo": fallo,
                "motivo": "esa vigia es NUEVA: nace roja a proposito. No se llama a nadie."}
    if intento > INTENTOS:
        return {"llamar": False, "fallo": fallo,
                "motivo": "van %d intentos y sigue rojo: se para y se le dice a Julio, en vez "
                          "de insistir quemando dinero" % INTENTOS}
    encargo = armar_encargo(fallo, material, intento)
    quien, motivo = elegir_cerebro(len(encargo))
    return {"llamar": bool(quien), "quien": quien, "motivo": motivo,
            "encargo": encargo, "fallo": fallo, "intento": intento}


def informe(d):
    """En palabras simples, para que se vea sin saber de esto."""
    if not d.get("llamar"):
        return "NO SE LLAMA A NADIE: " + str(d.get("motivo") or "")
    return "\n".join([
        "SE LE PIDE A: %s" % d.get("quien"),
        "  por que    : %s" % d.get("motivo"),
        "  intento    : %d de %d" % (d.get("intento", 1), INTENTOS),
        "  el encargo pesa %d letras" % len(d.get("encargo") or ""),
    ])


if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], encoding="utf-8", errors="ignore") as f:
            print(informe(decidir(f.read())))
    else:
        print(__doc__)
    sys.exit(0)
