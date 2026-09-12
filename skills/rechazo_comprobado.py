"""
skills/rechazo_comprobado.py

Comprueba, contando y sin ninguna IA, si las acusaciones con que un auditor
justifica un rechazo se sostienen contra el texto que de verdad entrego el
obrero.

Motivo (2026-09-12): el auditor gratis rechazo dos veces trabajo bueno del
obrero de PAGO inventandose los defectos:
    "Falta el decorador @pytest.fixture encima de la funcion _libreta_de_mentira"
    "Existe la linea literal <CORREO> que no es codigo Python valido"
Las dos eran falsas: el decorador estaba en el renglon 11 y la palabra CORREO
no aparecia en ninguna parte. El texto compilaba. Se tiro trabajo ya pagado.

Regla de oro: basta con que UNA sola acusacion se sostenga (o no se pueda
juzgar) para que el rechazo valga entero. Solo se desmonta el rechazo cuando
TODAS las acusaciones son demostrablemente falsas. Ante la duda manda el
auditor: nunca se deja pasar codigo por si acaso.

La funcion NUNCA lanza: si algo va mal, devuelve True (el rechazo vale).
"""

import ast
import re


# Palabras que indican que la frase dice que ALGO FALTA.
_PALABRAS_FALTA = (
    "falta",
    "faltan",
    "carece",
    "no tiene",
    "no incluye",
    "no esta",
    "ausente",
)

# Palabras que indican que la frase dice que ALGO EXISTE.
_PALABRAS_EXISTE = (
    "existe",
    "hay",
    "contiene",
    "aparece",
    "incluye",
)

# Palabras que indican que la frase habla de que NO COMPILA.
_PALABRAS_SINTAXIS = (
    "sintaxis",
    "no compila",
    "revienta",
    "syntaxerror",
)


# ---------------------------------------------------------------------------
# 1. SACAR DE LA FRASE LO QUE SENALA
# ---------------------------------------------------------------------------

def _sacar_lo_senalado(frase):
    """Devuelve la lista de trozos que la frase senala.

    Primero lo que va entre comillas (dobles o simples). Si no hay comillas,
    las palabras que empiezan por arroba o que llevan guion bajo o punto
    (son nombres de codigo).
    """
    if not isinstance(frase, str):
        return []

    trozos = []

    # Comillas dobles.
    for m in re.finditer(r'"([^"]+)"', frase):
        trozo = m.group(1).strip()
        if trozo:
            trozos.append(trozo)

    # Comillas simples.
    for m in re.finditer(r"'([^']+)'", frase):
        trozo = m.group(1).strip()
        if trozo:
            trozos.append(trozo)

    if trozos:
        return trozos

    # Sin comillas: palabras que empiezan por @ o llevan _ o .
    for palabra in re.findall(r"\S+", frase):
        limpia = palabra.strip(".,;:()[]{}\"'")
        if not limpia:
            continue
        if limpia.startswith("@") or "_" in limpia or "." in limpia:
            trozos.append(limpia)

    return trozos


# ---------------------------------------------------------------------------
# 2. CLASIFICAR LA FRASE
# ---------------------------------------------------------------------------

def _clasificar(frase):
    """Devuelve 'falta', 'existe', 'sintaxis' o None (no se juzga)."""
    if not isinstance(frase, str):
        return None
    bajo = frase.lower()

    # El molde de sintaxis manda si aparece.
    for p in _PALABRAS_SINTAXIS:
        if p in bajo:
            return "sintaxis"

    for p in _PALABRAS_FALTA:
        if p in bajo:
            return "falta"

    for p in _PALABRAS_EXISTE:
        if p in bajo:
            return "existe"

    return None


# ---------------------------------------------------------------------------
# 3. COMPROBAR SI EL TEXTO COMPILA
# ---------------------------------------------------------------------------

def _compila(texto):
    """True si el texto entregado compila con ast.parse. Nunca lanza."""
    try:
        ast.parse(texto)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# 4. JUZGAR UNA SOLA ACUSACION
# ---------------------------------------------------------------------------

def _juzgar_acusacion(frase, texto_bajo, texto_original):
    """Devuelve:
        True  -> la acusacion SE SOSTIENE (o no se puede juzgar).
        False -> la acusacion es demostrablemente FALSA.
    """
    molde = _clasificar(frase)

    # Molde 5: no encaja en ningun molde -> no se juzga, se da por buena.
    if molde is None:
        return True

    if molde == "sintaxis":
        # Si el texto SI compila, la acusacion de sintaxis es falsa.
        if _compila(texto_original):
            return False
        return True

    trozos = _sacar_lo_senalado(frase)

    # Si no se pudo sacar nada que senale, no se juzga: manda el auditor.
    if not trozos:
        return True

    if molde == "falta":
        # Dice que falta. Si TODO lo que senala aparece en el texto -> falsa.
        # Si algo de lo que senala NO aparece -> se sostiene.
        for trozo in trozos:
            if trozo.lower() not in texto_bajo:
                return True
        return False

    if molde == "existe":
        # Dice que existe. Si NADA de lo que senala aparece -> falsa.
        # Si algo aparece -> se sostiene.
        for trozo in trozos:
            if trozo.lower() in texto_bajo:
                return True
        return False

    return True


# ---------------------------------------------------------------------------
# 5. LA FUNCION PUBLICA
# ---------------------------------------------------------------------------

def se_sostiene(texto_entregado, fallos):
    """Comprueba si el rechazo del auditor se sostiene contra el texto real.

    texto_entregado: el texto que entrego el obrero.
    fallos: lista de frases con que el auditor justifica el rechazo.

    Devuelve (verdadero_o_falso, explicacion en palabras simples):
        True  -> el rechazo se sostiene, se tira el trabajo como hasta ahora.
        False -> NINGUNA acusacion se sostiene contra el texto real.

    Nunca lanza: si algo va mal, devuelve True (el rechazo vale).
    """
    try:
        if texto_entregado is None:
            texto_entregado = ""
        if not isinstance(texto_entregado, str):
            texto_entregado = str(texto_entregado)

        if fallos is None:
            fallos = []
        if isinstance(fallos, str):
            fallos = [fallos]
        try:
            fallos = list(fallos)
        except Exception:
            return (True, "no se pudieron leer las acusaciones del auditor; "
                          "ante la duda, el rechazo vale.")

        # Sin acusaciones no hay nada que desmontar: el rechazo vale.
        if not fallos:
            return (True, "el auditor no dejo acusaciones escritas; "
                          "ante la duda, el rechazo vale.")

        texto_bajo = texto_entregado.lower()

        falsas = []
        sostenidas = []

        for frase in fallos:
            try:
                se_sostiene_esta = _juzgar_acusacion(
                    frase, texto_bajo, texto_entregado
                )
            except Exception:
                # Si algo va mal juzgando una, se da por buena.
                se_sostiene_esta = True

            if se_sostiene_esta:
                sostenidas.append(frase)
            else:
                falsas.append(frase)

        # Regla de oro: basta UNA sostenida (o no juzgable) para que valga.
        if sostenidas:
            return (True, "el rechazo se sostiene: al menos una acusacion del "
                          "auditor no se puede desmontar contra el texto real.")

        # Todas falsas: se desmonta el rechazo.
        explicacion = _explicar(falsas)
        return (False, explicacion)

    except Exception:
        # Ante cualquier fallo raro, no se toca el control.
        return (True, "no se pudo comprobar el rechazo; ante la duda, vale.")


# ---------------------------------------------------------------------------
# 6. EXPLICACION PARA JULIO, SIN JERGA
# ---------------------------------------------------------------------------

def _explicar(falsas):
    """Escribe la explicacion en palabras simples a partir de las falsas."""
    partes = []
    for frase in falsas:
        if not isinstance(frase, str):
            frase = str(frase)
        bajo = frase.lower()
        trozos = _sacar_lo_senalado(frase)
        trozo = trozos[0] if trozos else ""

        if "falta" in bajo or "faltan" in bajo or "carece" in bajo \
                or "no tiene" in bajo or "no incluye" in bajo \
                or "no esta" in bajo or "ausente" in bajo:
            if trozo:
                partes.append(
                    "el auditor dijo que faltaba %s y esta en el texto" % trozo
                )
            else:
                partes.append(
                    "el auditor dijo que faltaba algo y eso esta en el texto"
                )
        elif "sintaxis" in bajo or "no compila" in bajo \
                or "revienta" in bajo or "syntaxerror" in bajo:
            partes.append(
                "el auditor dijo que el texto no compila y el texto si compila"
            )
        else:
            if trozo:
                partes.append(
                    "el auditor dijo que habia %s y eso no aparece en ninguna "
                    "parte" % trozo
                )
            else:
                partes.append(
                    "el auditor dijo que habia algo que no aparece en ninguna "
                    "parte"
                )

    if not partes:
        return "ninguna de las acusaciones del auditor se sostiene contra el texto."

    if len(partes) == 1:
        cuerpo = partes[0]
    else:
        cuerpo = "; y ".join(partes)

    return cuerpo + ". Ninguna de las acusaciones se sostiene."
