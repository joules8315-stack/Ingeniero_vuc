import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo.obrero import falta_en_el_material


# Material de prueba: trae la ruta cuerpo/obrero.py con su codigo dentro.
# Se arma por partes para que el texto de la prueba no dependa de nada externo.
MATERIAL = (
    "===== MATERIAL =====\n"
    "### cuerpo/obrero.py:73-157\n"
    "def falta_en_el_material(material, encargo):\n"
    "    return []\n"
    "===== FIN DEL MATERIAL =====\n"
)


def test_el_sitio_citado_no_es_un_archivo_que_falte():
    # Caso 1: el encargo cita un SITIO del codigo (ruta + dos puntos + renglon).
    # Es la misma ruta que ya esta en el material, asi que no falta nada.
    encargo = "revisa cuerpo/obrero.py:1290 y dime si el aviso es correcto"
    faltantes = falta_en_el_material(MATERIAL, encargo)
    assert faltantes == [], (
        "el aviso de un revisor citaba un sitio del codigo y la vuelta murio "
        "diciendo que faltaba material; la lista debe salir vacia: " + repr(faltantes)
    )


def test_la_ruta_que_de_verdad_no_esta_si_se_avisa():
    # Caso 2: el encargo nombra una ruta que de verdad no esta en el material.
    # El aviso de verdad no se afloja: la lista NO sale vacia.
    encargo = "revisa cuerpo/no_existe_esta_pieza.py y dime que le falta"
    faltantes = falta_en_el_material(MATERIAL, encargo)
    assert faltantes != [], (
        "una ruta que de verdad no esta en el material tiene que avisarse; "
        "la lista salio vacia"
    )


def test_la_ruta_limpia_sigue_saliendo_vacia():
    # Caso 3: el encargo nombra la ruta limpia, sin dos puntos ni renglon.
    # Es como se porta hoy: la lista sale vacia.
    encargo = "revisa cuerpo/obrero.py y dime si el aviso es correcto"
    faltantes = falta_en_el_material(MATERIAL, encargo)
    assert faltantes == [], (
        "la ruta limpia ya esta en el material y no debe avisarse: " + repr(faltantes)
    )


if __name__ == "__main__":
    test_el_sitio_citado_no_es_un_archivo_que_falte()
    test_la_ruta_que_de_verdad_no_esta_si_se_avisa()
    test_la_ruta_limpia_sigue_saliendo_vacia()
    print("prueba ejecutada")
