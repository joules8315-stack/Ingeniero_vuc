# -*- coding: utf-8 -*-
"""CANDADO — EL SITIO SE BUSCA POR NOMBRE, NUNCA POR NUMERO DE RENGLON.

Ley: CONTRATO_SE_BUSCA_POR_NOMBRE.md (Julio, 2026-08-31, tras repetirlo muchas veces):
  "Lo que borra todo, que cuenta por lineas... que lo busque por funcion y nombre... si en
   definitiva no se puede buscar por numero, que se elimine esa instruccion."

QUE FRENA, y solo esto (un candado que grita en falso se apaga solo, y entonces no protege nada):

  1. Un numero de renglon ESCRITO A MANO para encontrar codigo.
     Ejemplo real que costo el dia entero:  desde_armar, hasta_armar = 87, 227
     En cuanto alguien anade un renglon mas arriba, ese 87 apunta a otro sitio.

  2. Leer un pedazo de archivo pasandole dos numeros sueltos.
     Ejemplo:  _lineas_de(ruta, 87, 227)   ->  se pregunta por el NOMBRE de la funcion.

  3. Pedirle al equipo un TRAMO de renglones como forma de reparar.
     Ejemplo:  "lineas": "desde-hasta"     ->  un tramo BORRA la funcion entera.

QUE NO FRENA (para no estorbar):
  · documentos, notas y cuadernos: no son codigo.
  · las vigias: tienen que poder NOMBRAR lo prohibido para probar que esta prohibido.
  · el propio arnes: hay que poder reparar un candado roto.
  · lo que Julio autorice con su llave.

Y UNA COSA MAS, aprendida el 2026-08-31 midiendo el candado hermano: si este candado no puede
entender la peticion, FRENA. No se abre. Un candado que se abre solo cuando algo va mal no es un
candado; es una puerta con un cartel.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(AQUI, "memoria", "DECISIONES_POR_NOMBRE.log")

CODIGO = {".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".sh", ".ps1"}

# 1. numeros de renglon escritos a mano:  desde_x, hasta_x = 87, 227
A_MANO = re.compile(r"(?im)^[ \t]*\w*(?:desde|hasta)\w*[ \t]*,[ \t]*\w+[ \t]*=[ \t]*\d+[ \t]*,[ \t]*\d+")

# 2. leer un pedazo pasandole dos numeros sueltos:  _lineas_de(ruta, 87, 227)
DOS_NUMEROS = re.compile(r"(?i)\b\w*lineas_de\w*[ \t]*\([^()]*,[ \t]*\d+[ \t]*,[ \t]*\d+[ \t]*\)")

# 3. pedirle al equipo un tramo:  "lineas": "desde-hasta"
TRAMO_PEDIDO = re.compile(r'(?i)"lineas"[ \t]*:[ \t]*"desde-?\s*hasta"')

MOTIVOS = [
    (A_MANO, "hay un numero de renglon ESCRITO A MANO para encontrar codigo",
     "pregunta por el NOMBRE: piezas.funcion_completa(ruta, \"nombre_de_la_funcion\")"),
    (DOS_NUMEROS, "se lee un pedazo de archivo pasandole dos numeros sueltos",
     "pide la funcion por su nombre; los numeros se corren solos"),
    (TRAMO_PEDIDO, "se le pide al equipo un TRAMO de renglones para reparar",
     "pidele el texto que hay ahora y el texto que debe quedar, no un tramo"),
]

MENSAJE = (
    "\nFRENADO — EL SITIO SE BUSCA POR NOMBRE, NO POR NUMERO\n\n"
    "  En {fp}\n"
    "  {motivo}.\n\n"
    "  Por que: un numero de renglon se corre en cuanto alguien anade algo mas arriba, y un\n"
    "  tramo ('de la 97 a la 136') BORRA la funcion entera aunque solo hubiera que cambiar una\n"
    "  palabra. Es lo que Julio lleva repitiendo, y esta medido: costo 11 vueltas del equipo.\n\n"
    "  Lo que dice: {texto}\n\n"
    "  Hazlo asi: {cura}\n\n"
    "  La ley: CONTRATO_SE_BUSCA_POR_NOMBRE.md\n")


def _apuntar(fp, motivo, texto):
    """La libreta al reves: queda constancia de CADA frenada, con el motivo exacto."""
    try:
        import datetime
        os.makedirs(os.path.dirname(REGISTRO), exist_ok=True)
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write("%s | FRENADO | %s | %s | %s\n"
                    % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), fp, motivo,
                       texto.replace("\n", " ")[:120]))
    except Exception:
        pass


def libre(fp):
    """Sitios donde esto no aplica, y por que."""
    rel = fp.replace("\\", "/").lower()
    if os.path.splitext(rel)[1] not in CODIGO:
        return "no es codigo"
    if "/vigias/" in rel or os.path.basename(rel).startswith("test_"):
        return "es una vigia: tiene que poder nombrar lo prohibido para probarlo"
    if "/arnes/" in rel:
        return "es el propio arnes: hay que poder reparar un candado roto"
    return ""


def revisar(texto):
    """Devuelve (motivo, lo_que_dice, cura) del primer problema, o None si esta limpio."""
    for patron, motivo, cura in MOTIVOS:
        m = patron.search(texto or "")
        if m:
            return motivo, m.group(0).strip(), cura
    return None


def main():
    try:
        import autorizacion
        if autorizacion.autorizada():
            return 0                     # la llave de Julio manda
    except Exception:
        pass

    crudo = sys.stdin.read()
    if not (crudo or "").strip():
        return 0                         # no hay peticion: no hay nada que vigilar
    try:
        data = json.loads(crudo)
    except Exception:
        # NO SE ABRE ANTE EL FALLO. Hay peticion pero no se entiende: se frena y se dice.
        sys.stderr.write("\nFRENADO — no se pudo entender la peticion, y un candado no se abre\n"
                         "  cuando algo va mal. Vuelve a intentarlo.\n")
        _apuntar("(ilegible)", "no se pudo leer la peticion", crudo[:120])
        return 2

    dentro = data.get("tool_input") or {}
    fp = str(dentro.get("file_path") or "")
    if not fp:
        return 0
    porque = libre(fp)
    if porque:
        return 0

    texto = str(dentro.get("content") or dentro.get("new_string") or "")
    hallado = revisar(texto)
    if not hallado:
        return 0

    motivo, dice, cura = hallado
    _apuntar(fp, motivo, dice)
    sys.stderr.write(MENSAJE.format(fp=fp, motivo=motivo, texto=dice, cura=cura))
    try:
        import candados_medicion
        candados_medicion.cazado("por_nombre")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
