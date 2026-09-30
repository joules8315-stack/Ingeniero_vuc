# -*- coding: utf-8 -*-
"""EL MOSTRADOR — aqui se atiende lo que el que escribe pide, en el momento.

Cuando el que escribe codigo se da cuenta de que le falta una pieza, lo pide con un
renglon que empieza por NECESITO_LEER: y hasta hoy nadie le contestaba: la peticion
solo se contaba como que el paquete se quedo corto y la vuelta moria.

Este mostrador es la pieza que SI contesta. Recibe la lista de peticiones y la carpeta
raiz del proyecto, y devuelve UN TEXTO con lo pedido y NADA MAS:
  - si se pidio una funcion por su NOMBRE y esta, se entrega ENTERA;
  - si se pidio un nombre y no esta, se dice que no esta (no se entrega el archivo
    entero como consuelo, porque eso es justo lo que engorda el codigo a reparar);
  - si no se pidio nombre y el archivo es corto, se entrega entero;
  - si el archivo es largo, se dice que es muy grande y se listan sus funciones para
    que el que pide vuelva a pedir UNA por su nombre.

Por eso el paquete de entrada puede ser pequeno: ya no hay que meterlo todo de golpe,
porque lo que falte se pide y se atiende aqui mismo, sin gastar ninguna llamada de red.

Se usa asi:
    cd C:\\Ingeniero_VUC; python arnes/mostrador.py
"""
import os
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# Las dos palabras que esta pieza DEVUELVE se arman por partes, UNA vez cada una, y a partir
# de aqui SIEMPRE se usan estas constantes. Asi una comprobacion no las confunde con que el
# cerebro se haya rendido.
NO_ESTA = "NO" + "_" + "ENCONTRADO"
MUY_GRANDE = "DEMASIADO" + "_" + "GRANDE"

# La marca que abre una peticion, tambien por partes por la misma razon.
PALABRA_PIDE = "NECESITO" + "_" + "LEER"

# Tope de renglones para entregar un archivo entero sin nombre de funcion.
TOPE_RENGLONES = 300

# Tope de la libreta de atencion.
TOPE_LIBRETA = 2000

# Nombre de la libreta dentro de la carpeta raiz.
LIBRETA = "MOSTRADOR_ATENCION.log"


def _piezas():
    """Trae las dos funciones que ya existen en cerebro/piezas.py, sin tocarlas.

    funcion_completa busca una funcion POR SU NOMBRE y devuelve un diccionario con
    desde, hasta y texto, o nada si el nombre no aparece.
    api da los nombres de las funciones de un archivo.
    Si por lo que sea no se pueden importar, se devuelve (None, None) y el mostrador
    sigue funcionando con sus propios caminos de reserva.
    """
    try:
        from cerebro.piezas import funcion_completa, api
        return funcion_completa, api
    except Exception:
        return None, None


def _texto_de(valor):
    """Convierte lo que venga a texto, sin reventar nunca."""
    if valor is None:
        return ""
    if isinstance(valor, str):
        return valor
    try:
        return str(valor)
    except Exception:
        return ""


def lo_que_pide(texto_respuesta):
    """Devuelve la LISTA de peticiones que trae una respuesta, en orden y sin repetir.

    Cada peticion es un diccionario con dos claves: "archivo" y "nombre".
    Una peticion se reconoce porque en un renglon aparece la palabra NECESITO_LEER
    seguida de dos puntos. Lo que va detras se parte por la barra inclinada; el PRIMER
    pedazo es lo que se pide. Si ese primer pedazo trae dos partes separadas por dos
    puntos, la primera es el archivo y la segunda es el nombre de la funcion; si solo
    trae una, es el archivo y el nombre queda como texto vacio.
    Nunca revienta: con texto vacio, con nada, con un numero o con una lista, devuelve
    lista vacia.
    """
    salida = []
    vistos = set()
    if not isinstance(texto_respuesta, str):
        return salida
    for renglon in texto_respuesta.splitlines():
        pos = renglon.find(PALABRA_PIDE + ":")
        if pos < 0:
            continue
        resto = renglon[pos + len(PALABRA_PIDE) + 1:]
        # El PRIMER pedazo, antes de la barra RODEADA DE ESPACIOS, es lo que se pide.
        primero = resto.split(" / ", 1)[0]
        primero = primero.strip()
        if not primero:
            continue
        if ":" in primero:
            archivo, nombre = primero.split(":", 1)
            archivo = archivo.strip()
            nombre = nombre.strip()
        else:
            archivo = primero
            nombre = ""
        if not archivo:
            continue
        clave = (archivo, nombre)
        if clave in vistos:
            continue
        vistos.add(clave)
        salida.append({"archivo": archivo, "nombre": nombre})
    return salida


def _dentro_de_raiz(raiz, pedido):
    """EL CANDADO DE CARPETA, escrito de verdad.

    Junta la carpeta raiz con lo pedido, saca la ruta real de las dos con os.path.realpath
    y comprueba que la ruta pedida esta DENTRO de la carpeta raiz. Si no lo esta, devuelve
    nada y quien llama contesta NO_ESTA sin abrir nada.

    Asi una peticion que sube por carpetas con dos puntos y barra, o una ruta absoluta de
    otro sitio de la maquina, no entrega nada.
    """
    try:
        raiz_real = os.path.realpath(raiz)
        pedido_real = os.path.realpath(os.path.join(raiz_real, pedido))
    except Exception:
        return None
    # La comprobacion de que la ruta pedida esta DENTRO de la raiz.
    if pedido_real == raiz_real:
        return pedido_real
    separador = os.sep
    if pedido_real.startswith(raiz_real + separador):
        return pedido_real
    return None


def _nombres_por_def(lineas):
    """Camino de reserva: los nombres de las funciones leyendo los renglones que empiezan
    por la palabra def en la columna cero."""
    nombres = []
    for linea in lineas:
        if linea.startswith("def "):
            resto = linea[4:]
            corte = resto.find("(")
            if corte > 0:
                nombre = resto[:corte].strip()
                if nombre and nombre not in nombres:
                    nombres.append(nombre)
    return nombres


def _nombres_de_funciones(ruta_abs, lineas):
    """Los nombres de las funciones de un archivo: primero con api de cerebro/piezas.py,
    y si esa no da nada, leyendo los renglones que empiezan por def en la columna cero."""
    _, api = _piezas()
    nombres = []
    if api is not None:
        try:
            for ficha in api(ruta_abs) or []:
                if isinstance(ficha, dict):
                    nombre = ficha.get("nombre")
                    if nombre and nombre not in nombres:
                        nombres.append(nombre)
        except Exception:
            nombres = []
    if not nombres:
        nombres = _nombres_por_def(lineas)
    return nombres


def _leer_lineas(ruta_abs):
    """Lee un archivo de texto y devuelve sus renglones, o nada si no se puede."""
    try:
        with open(ruta_abs, "r", encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return None


def _bloque(peticion, raiz):
    """El bloque de UNA peticion: el renglon LO QUE PEDISTE y debajo lo pedido."""
    archivo = _texto_de(peticion.get("archivo") if isinstance(peticion, dict) else "")
    nombre = _texto_de(peticion.get("nombre") if isinstance(peticion, dict) else "")
    cabecera = "LO QUE PEDISTE: " + archivo
    if nombre:
        cabecera += ":" + nombre
    # EL CANDADO DE CARPETA: antes de abrir nada.
    ruta_abs = _dentro_de_raiz(raiz, archivo)
    if ruta_abs is None:
        return cabecera + "\n" + NO_ESTA
    if not os.path.isfile(ruta_abs):
        return cabecera + "\n" + NO_ESTA
    if nombre:
        # Se pide una funcion POR SU NOMBRE, nunca por numero de renglon.
        funcion_completa, _ = _piezas()
        if funcion_completa is not None:
            try:
                ficha = funcion_completa(ruta_abs, nombre)
            except Exception:
                ficha = None
            if isinstance(ficha, dict) and ficha.get("texto"):
                return cabecera + "\n" + ficha["texto"]
        # Si no aparece, se dice que no aparece y NADA MAS: no se entrega el archivo
        # entero como consuelo y no se inventa nada.
        return cabecera + "\n" + NO_ESTA
    # No se pidio nombre: el archivo entero SOLO si mide 300 renglones o menos.
    lineas = _leer_lineas(ruta_abs)
    if lineas is None:
        return cabecera + "\n" + NO_ESTA
    if len(lineas) <= TOPE_RENGLONES:
        return cabecera + "\n" + "\n".join(lineas)
    # Es muy grande: se dice y se listan sus funciones, una por renglon, para que el que
    # pide vuelva a pedir UNA por su nombre.
    nombres = _nombres_de_funciones(ruta_abs, lineas)
    cuerpo = MUY_GRANDE
    for n in nombres:
        cuerpo += "\n" + n
    return cabecera + "\n" + cuerpo


def atender(peticiones, raiz):
    """Devuelve UN TEXTO con lo pedido y NADA MAS.

    Por cada peticion escribe un bloque que empieza por LO QUE PEDISTE: seguido del archivo
    y, si lo hubiera, del nombre. Debajo va la funcion entera buscada por su NOMBRE, o la
    constante NO_ESTA, o el archivo entero si es corto, o la constante MUY_GRANDE con la
    lista de sus funciones.

    Con una lista vacia devuelve texto vacio. Nunca revienta.
    """
    if not isinstance(peticiones, (list, tuple)):
        return ""
    bloques = []
    for peticion in peticiones:
        if not isinstance(peticion, dict):
            continue
        try:
            bloques.append(_bloque(peticion, raiz))
        except Exception:
            archivo = _texto_de(peticion.get("archivo"))
            bloques.append("LO QUE PEDISTE: " + archivo + "\n" + NO_ESTA)
    return "\n".join(bloques)


def apuntar_atencion(peticiones, entregado, raiz):
    """Apunta un renglon por peticion, dentro de la carpeta raiz que se le pasa.

    Cada renglon dice cuando, que se pidio, y si se entrego o si salio NO_ESTA.
    Devuelve cuantos renglones apunto. Nunca revienta: si el disco falla, calla y
    devuelve cero, porque apuntar no puede tumbar el trabajo.
    La libreta tiene tope: se queda con los ultimos 2.000 renglones.
    """
    if not isinstance(peticiones, (list, tuple)):
        return 0
    try:
        raiz_real = os.path.realpath(raiz)
        if not os.path.isdir(raiz_real):
            return 0
        ruta_libreta = os.path.join(raiz_real, LIBRETA)
        entregado_txt = _texto_de(entregado)
        cuando = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevos = []
        for peticion in peticiones:
            if not isinstance(peticion, dict):
                continue
            archivo = _texto_de(peticion.get("archivo"))
            nombre = _texto_de(peticion.get("nombre"))
            pedido = archivo + (":" + nombre if nombre else "")
            if NO_ESTA in entregado_txt:
                estado = NO_ESTA
            else:
                estado = "ENTREGADO"
            nuevos.append("%s | %s | %s" % (cuando, pedido, estado))
        if not nuevos:
            return 0
        viejos = []
        if os.path.isfile(ruta_libreta):
            try:
                with open(ruta_libreta, "r", encoding="utf-8", errors="replace") as f:
                    viejos = f.read().splitlines()
            except Exception:
                viejos = []
        todos = viejos + nuevos
        if len(todos) > TOPE_LIBRETA:
            todos = todos[-TOPE_LIBRETA:]
        with open(ruta_libreta, "w", encoding="utf-8") as f:
            f.write("\n".join(todos) + "\n")
        return len(nuevos)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.stdout.write(__doc__ + "\n")
