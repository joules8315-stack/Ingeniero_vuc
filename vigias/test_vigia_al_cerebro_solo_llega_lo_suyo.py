# -*- coding: utf-8 -*-
"""VIGIA FUERTE — AL CEREBRO SOLO LE LLEGA LO SUYO. NUNCA EL BULTO ENTERO.

JULIO LO HA REPETIDO VARIAS VECES, y la ultima con razon y enfado (2026-09-09):
"Quedamos que se dividiria, para que solo la parte que le toque al cerebro llegue al cerebro,
lo que es de programar a programar, y otra vez la misma cosa: que llega completo todo el
llamado. Crea vigia fuerte, legisla bien, pon candados que sirvan, y asegurate de que no se
vuelva a olvidar."

EL FALLO, MEDIDO CON NUMEROS EL MISMO DIA:
   se mandaron            7.575 letras
   al cerebro le llegaron 35.845 letras
   se le pegaron encima   28.000 letras que nadie pidio
Con ese tamano NO LE CABE A NINGUNO de los cuatro cerebros gratis (aguantan entre 19.000 y
30.314). Se les salta a los cuatro EN SILENCIO, contesta el de pago, y como no queda nadie mas,
SE JUZGA A SI MISMO. Y encima juzgo mal: dijo que el archivo tenia "errores de sintaxis graves"
cuando compila perfecto y sus vigias pasan.

POR QUE SE OLVIDA UNA Y OTRA VEZ, que es lo que hay que cortar de raiz:
La cura EXISTE. Se llama arnes/asignador.py, sabe recortar dejando lo necesario y sabe elegir
un cerebro al que le quepa. Se construyo el 2026-09-08. Y NO LA LLAMA NADIE: cero invocaciones
desde ingeniero.py, cuerpo/ y cerebro/. Es la misma enfermedad de las 22 piezas dormidas de la
aplicacion de marketing: legislado, construido, y sin enchufar.

POR ESO ESTA VIGIA NO COMPRUEBA QUE LA LEY ESTE ESCRITA. Comprueba que SE CUMPLE:
  1. que quien manda trabajo a un cerebro llama al asignador;
  2. que lo que sale NUNCA pasa del tope que aguantan los gratis;
  3. que al recortar NO se tira lo que hace falta;
  4. y que si no le cabe a nadie, SE DICE Y NO SE GASTA.

LEYES: CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md y CONTRATO_SIN_OBJETIVO_NO_SE_PIDE_NADA.md
"""
import os
import re
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

# Lo que de verdad aguanta el mas pequeno de los cerebros gratis, medido.
TOPE_GRATIS = 19000


def _vivo(ruta):
    """El codigo sin comentarios ni textos de documentacion: solo lo que se ejecuta."""
    with open(ruta, encoding="utf-8") as f:
        codigo = f.read()
    codigo = re.sub(r'"""(?:.|\n)*?"""', " ", codigo)
    codigo = re.sub(r"'''(?:.|\n)*?'''", " ", codigo)
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in codigo.splitlines())


def _fn_resolver():
    """Devuelve el codigo VIVO (sin comentarios ni docstrings) de LA FUNCION resolver.

    Es la Regla 2 del CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO.md: cuando no se puede ejecutar
    (resolver dispara a un cerebro real y eso cuesta), se mira LA FUNCION, nunca el archivo.
    Un archivo con varios caminos no prueba nada: basta que OTRO camino (equipo) llame al
    asignador para que la palabra aparezca y esta vigia se ponga verde mintiendo. Justo lo que
    paso y lo que esta vigia existe para impedir.

    Y se quitan los comentarios y las explicaciones: un comentario que diga "hay que llamar al
    asignador" es exactamente el pañito de agua tibia que esto viene a matar. Solo cuenta lo que
    resolver EJECUTA de verdad.
    """
    import ingeniero
    import inspect
    src = inspect.getsource(ingeniero.resolver)
    src = re.sub(r'"""(?:.|\n)*?"""', " ", src)
    src = re.sub(r"'''(?:.|\n)*?'''", " ", src)
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in src.splitlines())


def test_quien_manda_trabajo_a_un_cerebro_llama_al_asignador():
    """La cura existe desde el 2026-09-08 y resolver no la llamaba: mandaba el bulto entero.

    Se comprueba DENTRO de resolver, no en todo ingeniero.py (que tiene varios caminos y el
    mando equipo tambien usa el asignador: un assert sobre el archivo entero es verde de
    mentira). Se exige que, en resolver, se recorte con el asignador ANTES de llamar al obrero.
    """
    src = _fn_resolver()
    # 1) el recorte ocurre DENTRO de resolver (no en cualquier sitio del archivo)
    assert "asignador" in src, (
        "resolver no llama al asignador. Sigue mandando el bulto entero al cerebro: se mandaron "
        "7.575 letras y llegaron 35.845, no le cupo a ninguno de los cuatro gratis, contesto el "
        "de pago y se juzgo a si mismo. Y esto se mide DENTRO de resolver, porque mirar todo el "
        "archivo era el verde de mentira que esta vigia viene a matar.")
    # 2) recorta dejando solo lo necesario (armar_encargo), no solo lo nombra
    assert "armar_encargo" in src, (
        "resolver nombra el asignador pero no recorta el paquete con el. Nombrarlo no sirve: el "
        "bulto entero seguiria llegando al cerebro. Tiene que pasarlo por armar_encargo.")
    # 3) el recorte va ANTES de entregarselo al obrero (el orden es la prueba de que sirve)
    pos_recorte = src.find("armar_encargo")
    pos_obrero = src.find("obrero.trabajar")
    assert -1 < pos_recorte < pos_obrero, (
        "el recorte del asignador va DESPUES de llamar al obrero, o no esta. Recortar por detras "
        "no sirve: el bulto entero ya se mando. El orden es la prueba de que el recorte protege.")


def test_lo_que_sale_nunca_pasa_del_tope_de_los_gratis():
    """Si pasa del tope, se salta a todos los gratis EN SILENCIO y lo paga Julio."""
    import asignador
    fallo = asignador.leer_el_fallo(
        "FAILED vigias/test_x.py::test_algo\nE   AssertionError: NO SALE EL EMBUDO\n")
    encargo = asignador.armar_encargo(fallo, material="x" * 200000)
    assert len(encargo) <= TOPE_GRATIS, (
        "EL ENCARGO SALIO CON %d LETRAS y el mas pequeno de los gratis aguanta %d. Con eso se "
        "les salta a todos sin decir nada y acaba pagandolo el de pago."
        % (len(encargo), TOPE_GRATIS))


def test_al_recortar_no_se_tira_lo_que_hace_falta():
    """Recortar por lo bruto es trampa: cabe y no sirve para nada."""
    import asignador
    lo_necesario = "def armar_datos(perfil, preguntar=None, metricas_reales=None):"
    fallo = asignador.leer_el_fallo(
        "FAILED vigias/test_x.py::test_algo\nE   AssertionError: NO SALE EL EMBUDO\n")
    material = ("relleno que no hace falta\n" * 5000) + lo_necesario
    encargo = asignador.armar_encargo(fallo, material=material)
    assert lo_necesario in encargo, (
        "CUPO PERO SE DEJO FUERA LO QUE HACIA FALTA. Se tiro justo el trozo que hay que "
        "reparar: el encargo cabe y no sirve de nada. Primero se guarda lo necesario y el "
        "relleno es lo que se recorta.")


def test_si_no_le_cabe_a_nadie_se_dice_y_no_se_gasta():
    """Callarse es lo que hacia el sistema viejo, y por eso se pagaba de mas."""
    import asignador
    quien, motivo = asignador.elegir_cerebro(letras=5000000)
    assert quien is None, (
        "IBA A MANDAR UN ENCARGO QUE NO LE CABE A NADIE. Eso es tirar el dinero: se les salta "
        "a todos y contesta el de pago, que tampoco puede con el.")
    assert motivo, "no dijo POR QUE no se puede: callarse es justo lo que hacia el sistema viejo"
