# -*- coding: utf-8 -*-
"""Vigia: el cierre del trabajo tiene que pedir el resumen del plan.

Julio, hoy: "una vez se termine de ejecutar el plan, me haces siempre un resumen.
Esta instruccion nunca debe depender de tu memoria: crea programa."

Hoy el resumen depende de que la IA se acuerde. Esta prueba nace ROJA a proposito:
el enganche que la satisface se escribe en la ronda SIGUIENTE.

Casos 1, 2, 3 y 6: leen archivos del proyecto COMO TEXTO (no los importan ni los
ejecutan, porque candado_cierre.py e ingeniero.py hacen cosas al correrlos).
Casos 4 y 5: usan la pieza real arnes/puerta_del_plan.py y la carpeta temporal
de pytest. TIENEN QUE ESTAR VERDES HOY.

Sabotaje prometido: cuando el enganche entre, quien revise lo quita, corre esta
prueba y comprueba que los casos 1, 2, 3 y 6 VUELVEN A ROJO. Si con la cura
quitada alguno sigue verde, la prueba mira a otro nivel que el arreglo.
"""

import os
import sys


# ---------------------------------------------------------------------------
# Montaje de rutas: la carpeta un nivel arriba de vigias/ y la carpeta arnes/.
# ---------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARNES = os.path.join(RAIZ, "arnes")

for _p in (RAIZ, ARNES):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RUTA_CANDADO = os.path.join(ARNES, "candado_cierre.py")
RUTA_INGENIERO = os.path.join(RAIZ, "ingeniero.py")


# ---------------------------------------------------------------------------
# Utilidades de lectura de texto (sin importar ni ejecutar los archivos).
# ---------------------------------------------------------------------------
def _leer_texto(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def _ventana_alrededor(texto, aguja, radio=1200):
    """Devuelve el trozo de texto alrededor de la primera aparicion de aguja.

    Si la aguja no aparece, devuelve cadena vacia. Se usa para comprobar que
    ciertas palabras estan CERCA de donde se nombra a puerta_del_plan.
    """
    i = texto.find(aguja)
    if i < 0:
        return ""
    ini = max(0, i - radio)
    fin = min(len(texto), i + len(aguja) + radio)
    return texto[ini:fin]


# ---------------------------------------------------------------------------
# CASO 1: EL CIERRE LE PREGUNTA A LA PUERTA DEL PLAN. Nace rojo.
# ---------------------------------------------------------------------------
def test_caso_1_el_cierre_le_pregunta_a_la_puerta_del_plan():
    texto = _leer_texto(RUTA_CANDADO)
    assert "puerta_del_plan" in texto, (
        "arnes/candado_cierre.py no nombra a puerta_del_plan en ninguna parte. "
        "Hoy el resumen del plan depende de que la IA se acuerde, que es justo lo "
        "que Julio prohibio: 'esta instruccion nunca debe depender de tu memoria: "
        "crea programa'. El cierre tiene que preguntarle a la puerta del plan."
    )
    assert "puede_cerrar" in texto, (
        "arnes/candado_cierre.py no llama a puede_cerrar. La pieza que sabe si "
        "falta el resumen ya existe y ya esta verde, pero hoy nadie la llama: el "
        "cierre tiene que preguntarle a puede_cerrar antes de dar algo por terminado."
    )


# ---------------------------------------------------------------------------
# CASO 2: LA FALTA DICE COMO ARREGLARLA. Nace rojo.
# ---------------------------------------------------------------------------
def test_caso_2_la_falta_dice_como_arreglarla():
    texto = _leer_texto(RUTA_CANDADO)
    ventana = _ventana_alrededor(texto, "puerta_del_plan")
    assert ventana, (
        "arnes/candado_cierre.py no nombra a puerta_del_plan, asi que no hay "
        "ventana donde buscar la palabra resumen. Sin la falta que diga como "
        "arreglarla, el freno no tendria forma honrada de satisfacerse."
    )
    assert "resumen" in ventana, (
        "Cerca de donde se nombra a puerta_del_plan no aparece la palabra 'resumen'. "
        "La falta que agregue el cierre tiene que traer dentro la palabra resumen "
        "y el comando para apuntarlo, para que quien lea sepa como arreglarla."
    )


# ---------------------------------------------------------------------------
# CASO 3: EXISTE EL COMANDO PARA APUNTAR EL RESUMEN. Nace rojo.
# ---------------------------------------------------------------------------
def test_caso_3_existe_el_comando_para_apuntar_el_resumen():
    texto = _leer_texto(RUTA_INGENIERO)
    assert ("anotar_resumen" in texto) or ("puerta_del_plan" in texto), (
        "ingeniero.py no nombra a anotar_resumen ni a puerta_del_plan. Sin ese "
        "comando, el freno del cierre no tendria forma honrada de satisfacerse, y "
        "un freno asi empuja a saltarselo, que es peor que no tenerlo."
    )


# ---------------------------------------------------------------------------
# CASO 4: SIN PLAN SE CIERRA IGUAL. TIENE QUE ESTAR VERDE HOY.
# ---------------------------------------------------------------------------
def test_caso_4_sin_plan_se_cierra_igual(tmp_path):
    from arnes import puerta_del_plan

    carpeta_vacia = str(tmp_path)
    se_puede, motivo = puerta_del_plan.puede_cerrar(carpeta_vacia)
    assert se_puede is True, (
        "En una carpeta temporal vacia, sin ninguna marca de plan, puede_cerrar "
        "tiene que decir que SI se puede cerrar. Si dijera que no, el arreglo "
        "frenaria todas las vueltas de todos los proyectos y nadie podria cerrar "
        "nada nunca. Motivo devuelto: %r" % (motivo,)
    )


# ---------------------------------------------------------------------------
# CASO 5: CON PLAN APROBADO Y SIN RESUMEN NO SE CIERRA, Y CON RESUMEN SI.
# TIENE QUE ESTAR VERDE HOY.
# ---------------------------------------------------------------------------
def test_caso_5_con_plan_aprobado_sin_resumen_no_se_cierra_y_con_resumen_si(tmp_path):
    from arnes import puerta_del_plan

    carpeta = str(tmp_path)

    # Plan de mentira con los cuatro rotulos que exige la pieza.
    plan = (
        "QUE SE REPARA: el cierre no pide el resumen del plan.\n"
        "COMO SE REPARA: el cierre pregunta a puede_cerrar y agrega la falta.\n"
        "DONDE SE REPARA: arnes/candado_cierre.py, en su funcion main.\n"
        "POR QUE SE REPARA: Julio dijo que el resumen no puede depender de la memoria.\n"
    )

    # aprobar recibe primero el texto del plan y despues la carpeta, y
    # devuelve un diccionario con la clave 'ok' y el numero dentro.
    resultado = puerta_del_plan.aprobar(plan, carpeta)
    assert isinstance(resultado, dict) and "ok" in resultado, (
        "aprobar tiene que devolver un diccionario con la clave 'ok' y el numero "
        "del plan aprobado dentro. Devolvio: %r" % (resultado,)
    )
    numero = resultado["ok"]

    se_puede, motivo = puerta_del_plan.puede_cerrar(carpeta)
    assert se_puede is False, (
        "Con un plan aprobado y sin resumen anotado, puede_cerrar tiene que decir "
        "que NO se puede cerrar. Dijo que si. Motivo: %r" % (motivo,)
    )
    assert "puerta_del_plan" in str(motivo), (
        "El motivo de la falta tiene que nombrar a puerta_del_plan, para que quien "
        "lea sepa de donde viene el freno. Motivo: %r" % (motivo,)
    )

    # anotar_resumen recibe el numero del plan y el texto del resumen.
    puerta_del_plan.anotar_resumen(numero, "Resumen del plan: se hizo lo pedido.", carpeta)

    se_puede_2, motivo_2 = puerta_del_plan.puede_cerrar(carpeta)
    assert se_puede_2 is True, (
        "Con el resumen ya anotado, puede_cerrar tiene que decir que SI se puede "
        "cerrar. Dijo que no. Motivo: %r" % (motivo_2,)
    )


# ---------------------------------------------------------------------------
# CASO 6: SI LA PUERTA DEL PLAN REVIENTA, SE DEJA CERRAR. Nace rojo.
# ---------------------------------------------------------------------------
def test_caso_6_si_la_puerta_del_plan_revienta_se_deja_cerrar():
    # Puerta de mentira: su puede_cerrar lanza un error a proposito.
    class PuertaQueRevienta(object):
        def puede_cerrar(self, carpeta):
            raise RuntimeError("la puerta del plan revienta a proposito")

    puerta = PuertaQueRevienta()

    # El que llama tiene que tratar el problema y dejar pasar: ninguna falta.
    faltas = []
    try:
        se_puede, motivo = puerta.puede_cerrar("/tmp/carpeta_que_no_existe")
        if not se_puede:
            faltas.append(motivo)
    except Exception:
        # Un freno que se rompe no puede dejar el trabajo atrapado sin salida.
        pass

    assert faltas == [], (
        "Al preguntarle a una puerta del plan que revienta, no tiene que quedar "
        "ninguna falta: el que llama tiene que tratar el problema y dejar pasar. "
        "Un freno que se rompe no puede dejar el trabajo atrapado sin salida."
    )

    # Y esa manera de tratarlo tiene que estar escrita en arnes/candado_cierre.py:
    # cerca de donde nombra a puerta_del_plan tiene que haber un intento protegido.
    texto = _leer_texto(RUTA_CANDADO)
    ventana = _ventana_alrededor(texto, "puerta_del_plan")
    assert ventana, (
        "arnes/candado_cierre.py no nombra a puerta_del_plan, asi que no hay "
        "ventana donde buscar el intento protegido. El enganche todavia no existe."
    )
    assert ("try:" in ventana) or ("except" in ventana), (
        "Cerca de donde se nombra a puerta_del_plan no hay un intento protegido "
        "(try/except). Si la puerta del plan revienta, el cierre tiene que dejar "
        "cerrar en vez de dejar el trabajo atrapado sin salida."
    )
