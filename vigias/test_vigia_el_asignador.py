# -*- coding: utf-8 -*-
"""VIGIA — EL ASIGNADOR: el comparador manda, y la IA solo entra si sale ROJO.

DE DONDE SALE (Julio, 2026-09-08): "la revision se puede programar, dado que estamos esperando
un resultado especifico. Mejor crear un COMPARADOR: si no se logra, dice que no se logro, y
ahi si entra una IA a ver por que. Para eso debe tener la informacion pertinente de la pieza,
DEPURADA, no informacion irrelevante que haga bulto."

Y: "el que asigna ya debe tener la informacion pertinente completa: saber si la IA tiene
capacidad, si no esta dormida, diciendole claramente este es el resultado que queremos, se hizo
esto y no sirvio por esto, reparalo."

Y despues, apretando la tuerca: "no solo que quepa, sino que venga LO NECESARIO en el paquete,
y no con peso innecesario".

LO QUE ESTO ARREGLA, medido esa noche: se llamaba a una IA para comprobar cosas que un programa
comprueba gratis, y cuando la IA si hacia falta se le mandaba un encargo VACIO, sin objetivo y
sin datos. Ademas el encargo pesaba 24.000 letras y los cerebros gratis aguantan 19.000-20.000:
se les saltaba a todos EN SILENCIO y acababa escribiendo y revisando el mismo cerebro de pago.

CONTRADICCION QUE CAZO JULIO ANTES DE QUE SE CONSTRUYERA, y es la mas importante de todas:
"si nace roja, lo va a mandar para una IA, y no es asi; debe ser en la segunda vuelta o algo
similar, porque si nace roja lo manda enseguida para la IA, y es lo que NO queremos".
Tenia razon: el metodo de esta casa dice que LA VIGIA NACE ROJA A PROPOSITO. Si el criterio
fuera "rojo = llamar a una IA", cada vez que se escribe una vigia nueva se dispararia una IA a
reparar una pieza que TODAVIA NO EXISTE. Se estaria pagando por el paso 1 del propio metodo.

EL CRITERIO CORRECTO, y la casa YA sabe distinguirlo (arnes/guardia_de_guardado.py::_vigias
pregunta al guardado si la vigia es NUEVA o ya estaba):
   roja RECIEN NACIDA (aun no existe la pieza) -> NO se llama a nadie. Es el metodo, no un fallo
   estaba VERDE y se puso roja                 -> ahi SI: algo se rompio de verdad
   sigue roja TRAS UN INTENTO de arreglo       -> ahi SI, con el mensaje nuevo

ESTA VIGIA COMPRUEBA LAS SIETE COSAS:
  1. que el objetivo se saca del propio mensaje de la vigia roja (no se inventa);
  2. que ANTES de gastar se mira quien puede y quien esta despierto;
  3. que si NADIE puede, se dice y NO se gasta;
  4. que el encargo lleva las TRES cosas (objetivo, lo que hay, y su papel);
  5. que el material va DEPURADO: cabe;
  6. que, cabiendo, TRAE LO NECESARIO: la pieza que fallo tiene que ir dentro;
  7. y que UNA VIGIA RECIEN NACIDA NO LLAMA A NADIE.

LEY: CONTRATO_SIN_OBJETIVO_NO_SE_PIDE_NADA.md y CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md
"""
import os
import sys

import pytest

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

SALIDA_ROJA = """FAILED vigias/test_vigia_del_embudo.py::test_trae_el_embudo_con_datos_reales
E   AssertionError: NO SALE EL EMBUDO. Con 1000 de alcance y 100 clics ya se puede decir que
de cada diez que lo vieron, uno entro. Eso es lo que le sirve al dueno del negocio.
1 failed, 448 passed in 100.00s
"""

EL_TROZO_QUE_HACE_FALTA = "def armar_datos(perfil, preguntar=None, metricas_reales=None):"


def _asignador():
    try:
        import asignador
    except ImportError:
        pytest.fail(
            "NO EXISTE arnes/asignador.py. Sin el, cada vez que una vigia se pone roja hay que "
            "pararse a mirar a mano quien puede repararlo, y se acaba llamando a una IA sin "
            "objetivo y sin datos, que es justo lo que Julio no quiere.")
    return asignador


def test_el_objetivo_sale_del_mensaje_de_la_vigia_no_se_inventa():
    """La vigia roja YA dice que tenia que pasar. De ahi sale el objetivo, no de la imaginacion."""
    a = _asignador()
    fallo = a.leer_el_fallo(SALIDA_ROJA)
    assert fallo, "no supo leer que vigia fallo"
    assert "EMBUDO" in (fallo.get("objetivo") or "").upper(), (
        "EL OBJETIVO NO SALE DEL MENSAJE DE LA VIGIA. Ese mensaje ya dice que tenia que pasar; "
        "si el objetivo se inventa, la IA no tiene contra que comparar.")
    assert "test_trae_el_embudo_con_datos_reales" in (fallo.get("prueba") or ""), (
        "no supo decir QUE prueba fallo")


def test_mira_quien_puede_y_quien_esta_despierto_antes_de_gastar():
    """El paso previo que faltaba: primero se mira si hay alguien, y solo despues se gasta."""
    a = _asignador()
    elegido, motivo = a.elegir_cerebro(letras=15000)
    assert motivo, "no dijo POR QUE eligio a quien eligio"
    if elegido:
        from cuerpo import cuotas
        assert cuotas.desperto(elegido), (
            "ELIGIO UN CEREBRO DORMIDO: %s. Gastar una vuelta en uno agotado es tirar el "
            "trabajo." % elegido)


def test_si_nadie_puede_lo_dice_y_no_gasta():
    """Un encargo gigante no le cabe a nadie. Se dice y no se llama a nadie: no se gasta en balde."""
    a = _asignador()
    elegido, motivo = a.elegir_cerebro(letras=5000000)
    assert elegido is None, (
        "MANDO UN ENCARGO QUE NO LE CABE A NADIE. Eso es lo que pasaba antes: se les saltaba a "
        "todos en silencio y acababa escribiendo y revisando el mismo cerebro de pago.")
    assert motivo, "no dijo por que no se puede: callarse es lo que hacia el sistema viejo"


def test_el_encargo_lleva_las_tres_cosas():
    """Sin objetivo, sin lo que hay y sin su papel, el que trabaja no puede hacer nada."""
    a = _asignador()
    fallo = a.leer_el_fallo(SALIDA_ROJA)
    encargo = a.armar_encargo(fallo, material=EL_TROZO_QUE_HACE_FALTA)
    for marca in ("OBJETIVO", "LO QUE HAY", "TU PAPEL"):
        assert marca in encargo.upper(), (
            "AL ENCARGO LE FALTA '%s'. Ley: a nadie se le pide un trabajo sin decirle que tiene "
            "que conseguir, que hay ahora, y que se espera de el." % marca)


def test_el_material_va_depurado_y_cabe():
    """Julio: informacion pertinente, no informacion irrelevante que haga bulto."""
    a = _asignador()
    fallo = a.leer_el_fallo(SALIDA_ROJA)
    relleno = ("relleno que no hace falta\n" * 2000) + EL_TROZO_QUE_HACE_FALTA
    encargo = a.armar_encargo(fallo, material=relleno)
    assert len(encargo) <= 19000, (
        "EL ENCARGO SALIO CON %d LETRAS. Los cerebros gratis aguantan 19.000-20.000: con mas, "
        "se les salta a todos en silencio y acaba pagandolo el de pago." % len(encargo))


def test_aunque_recorte_trae_lo_necesario():
    """Julio, apretando: no solo que quepa, sino que venga LO NECESARIO.

    Recortar por lo bruto es facil y es trampa: si al recortar se cae justo el trozo que hay
    que reparar, el encargo cabe y NO SIRVE PARA NADA. La IA se quedaria sin lo unico que
    necesitaba, y encima diria NO_ENCONTRADO habiendo pagado la vuelta.
    """
    a = _asignador()
    fallo = a.leer_el_fallo(SALIDA_ROJA)
    relleno = ("relleno que no hace falta\n" * 2000) + EL_TROZO_QUE_HACE_FALTA
    encargo = a.armar_encargo(fallo, material=relleno)
    assert EL_TROZO_QUE_HACE_FALTA in encargo, (
        "CUPO, PERO SE DEJO FUERA LO QUE HACIA FALTA. Recortar por lo bruto tira justo el "
        "trozo que hay que reparar: el encargo cabe y no sirve para nada. Primero se guarda lo "
        "necesario, y el relleno es lo que se recorta.")


def test_una_vigia_recien_nacida_no_llama_a_nadie():
    """LA MAS IMPORTANTE, y la cazo Julio antes de que se construyera.

    El metodo de esta casa dice que la vigia NACE ROJA a proposito: se escribe antes que la
    pieza, para probar que de verdad prueba algo. Si el criterio fuera "rojo = llamar a una
    IA", cada vez que se escribe una vigia nueva se dispararia una IA a reparar algo que
    todavia no existe. Se estaria pagando por el paso 1 del propio metodo, y encima la IA no
    encontraria nada que reparar.

    La casa YA sabe distinguirlo: el guardia de guardado le pregunta al guardado si esa vigia
    es NUEVA (nunca guardada) o si ya estaba. Aqui se exige lo mismo.
    """
    a = _asignador()
    assert a.hay_que_llamar_a_alguien(SALIDA_ROJA, vigias_nuevas=["vigias/test_vigia_del_embudo.py"]) is False, (
        "IBA A LLAMAR A UNA IA POR UNA VIGIA RECIEN NACIDA. Esa roja es el metodo, no un fallo: "
        "la pieza todavia no existe. Llamar ahi es pagar por el paso 1 del propio metodo.")
    assert a.hay_que_llamar_a_alguien(SALIDA_ROJA, vigias_nuevas=[]) is True, (
        "NO IBA A LLAMAR A NADIE ANTE UNA ROJA DE VERDAD. Esa vigia ya estaba guardada y verde: "
        "si ahora esta roja, algo se rompio y ahi SI hace falta una IA.")
