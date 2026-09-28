import os
import sys

# Arranque: la carpeta un nivel arriba de vigias y la carpeta cuerpo, para poder
# importar cuerpo.obrero sin depender de como se lance pytest.
_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_AQUI)
_CUERPO = os.path.join(_RAIZ, "cuerpo")
for _ruta in (_RAIZ, _CUERPO):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from cuerpo.obrero import _nombres_de_funcion_del_texto, falta_en_el_material


TEXTO_ENCARGO = (
    "En comprobar_pasos, sacar la llamada a pytest a una funcion propia"
)


def test_sin_conocidas_no_pide_la_funcion_publica():
    """Hoy, sin pasar conocidas, un nombre normal no se reconoce."""
    nombres = _nombres_de_funcion_del_texto(TEXTO_ENCARGO)
    assert "comprobar_pasos" not in nombres


def test_con_conocidas_si_pide_la_funcion_publica():
    """Con conocidas, las palabras del texto que estan en la coleccion vuelven."""
    conocidas = {"comprobar_pasos", "otro_nombre_uno", "otro_nombre_dos"}
    nombres = _nombres_de_funcion_del_texto(TEXTO_ENCARGO, conocidas)
    assert "comprobar_pasos" in nombres
    assert "otro_nombre_uno" not in nombres
    assert "otro_nombre_dos" not in nombres


def test_lo_de_siempre_sigue_funcionando():
    """Los nombres con raya baja vuelven aunque no se pase conocidas."""
    nombres = _nombres_de_funcion_del_texto("hay que tocar _prompt_obrero")
    assert "_prompt_obrero" in nombres


def test_no_se_exige_una_funcion_que_no_existe():
    """Con conocidas en posicion, el aviso nombra la que existe y NO la inventada."""
    from cuerpo.obrero import falta_en_el_material

    material = "el material trae cuerpo/obrero.py y nada mas"
    encargo = "En falta_en_el_material, sacar la llamada a _raya_baja_inventada a una funcion propia"

    avisos_con = falta_en_el_material(material, encargo, {"falta_en_el_material"})
    assert any("falta_en_el_material" in aviso for aviso in avisos_con)
    assert not any("_raya_baja_inventada" in aviso for aviso in avisos_con)

    avisos_sin = falta_en_el_material(material, encargo)
    assert any("_raya_baja_inventada" in aviso for aviso in avisos_sin)


def test_el_obrero_le_pasa_las_conocidas_a_la_comprobacion():
    """El obrero entrega a falta_en_el_material la lista de funciones que existen de verdad."""
    import os
    import re

    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cuerpo", "obrero.py")
    texto = open(ruta, encoding="utf-8").read()
    patron = re.compile(r"falta_en_el_material\s*\(([^)]*)\)", re.S)
    llamadas = [m for m in patron.finditer(texto)
                if not texto[max(0, m.start() - 4):m.start()].endswith("def ")]
    assert llamadas, "no aparece ninguna llamada a falta_en_el_material en cuerpo/obrero.py"
    assert any(len([a for a in re.split(r",(?![^\[\]{}()]*[\]})])", m.group(1)) if a.strip()]) >= 3
               for m in llamadas), \
        "ninguna llamada a falta_en_el_material le pasa TRES argumentos (las conocidas)"


def test_falta_en_el_material_avisa_solo_con_conocidas():
    """Con conocidas avisa que falta la funcion; sin conocidas no dice nada de ella."""
    material = "el material trae cuerpo/capataz.py y nada mas"
    encargo = "En comprobar_pasos, sacar la llamada a pytest a una funcion propia"

    avisos_con = falta_en_el_material(material, encargo, {"comprobar_pasos"})
    assert any("comprobar_pasos" in aviso for aviso in avisos_con)

    avisos_sin = falta_en_el_material(material, encargo)
    assert not any("comprobar_pasos" in aviso for aviso in avisos_sin)
