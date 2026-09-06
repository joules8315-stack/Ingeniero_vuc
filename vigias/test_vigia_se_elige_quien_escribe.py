# -*- coding: utf-8 -*-
"""vigias/test_vigia_se_elige_quien_escribe.py — SE PUEDE ELEGIR QUIEN ESCRIBE.

Pieza 1 del plan aprobado por Julio el 2026-09-06.

EL NUMERO QUE LA JUSTIFICA: al medir el registro del equipo el 2026-09-05 salio que en los
72 trabajos REALES escribio SIEMPRE el de pago, y los cerebros gratis escribieron CERO. No
por malos: porque el mando `equipo` llamaba al obrero SIN pasarle a quien se le pedia, asi
que la peticion se perdia en el camino. Sin esto no se puede medir a los gratis escribiendo,
que es lo que Julio ordeno ("dales tareas reales secundarias, y verifica estado real").

Se comprueba lo que importa, no que el archivo exista:
  1. el mando saca --escribe y --revisa de las palabras del encargo;
  2. esas marcas NO se cuelan dentro de la tarea (si no, el paquete se arma con basura);
  3. el mando se los PASA al obrero (era el fallo: los aceptaba y no los pasaba);
  4. sin marcas, todo sigue como antes.
"""
import os
import re
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANDO = os.path.join(AQUI, "ingeniero.py")


def _texto_del_mando():
    with open(MANDO, encoding="utf-8", errors="ignore") as f:
        return f.read()


def _bloque_del_equipo(texto):
    """El trozo del mando `equipo`, para no juzgar por lo que hay en otros mandos."""
    i = texto.find('if cmd == "equipo"')
    assert i > 0, "no se encuentra el mando equipo"
    return texto[i:i + 4000]


def test_el_mando_entiende_a_quien_se_le_pide():
    """1. Las dos marcas existen en el mando."""
    b = _bloque_del_equipo(_texto_del_mando())
    assert "--escribe" in b, "el mando no entiende --escribe"
    assert "--revisa" in b, "el mando no entiende --revisa"


def test_las_marcas_no_se_cuelan_en_la_tarea():
    """2. La tarea se arma con el RESTO, no con las palabras crudas. Si se colaran, el
    material se armaria buscando piezas llamadas 'groq20b' y saldria basura."""
    b = _bloque_del_equipo(_texto_del_mando())
    assert not re.search(r'tarea\s*=\s*" "\.join\(sys\.argv\[3:\]\)', b), \
        "la tarea sigue armandose con las palabras crudas: las marcas se colarian dentro"


def test_el_mando_SE_LOS_PASA_al_obrero():
    """3. EL CORAZON. El fallo no era aceptarlos: era aceptarlos y no pasarlos.
    Esta es la comprobacion que se pone roja si alguien 'limpia' la reparacion."""
    b = _bloque_del_equipo(_texto_del_mando())
    # OJO: la llamada lleva parentesis DENTRO (_r.a_texto(paq)), asi que no vale cortar en el
    # primer parentesis: se toma hasta el final del renglon (fallo real de esta misma vigia).
    m = re.search(r"_o\.trabajar\((.*)$", b, re.M)
    assert m, "no se encuentra la llamada al obrero en el mando equipo"
    llamada = m.group(1)
    assert "generador" in llamada, "el mando NO le pasa al obrero quien escribe"
    assert "auditor" in llamada, "el mando NO le pasa al obrero quien revisa"


def test_el_obrero_sigue_respetandolos():
    """4. La otra mitad: el obrero tiene que seguir aceptando esos dos datos."""
    with open(os.path.join(AQUI, "cuerpo", "obrero.py"), encoding="utf-8",
              errors="ignore") as f:
        cuerpo = f.read()
    assert re.search(r"def trabajar\([^)]*generador[^)]*auditor", cuerpo), \
        "el obrero ya no acepta generador y auditor"


def test_sin_marcas_todo_sigue_igual():
    """5. Si no se pide a nadie en concreto, el relevo decide como siempre: no se rompe
    el uso normal, que es el 99% de las veces."""
    b = _bloque_del_equipo(_texto_del_mando())
    assert "None" in b or "or None" in b or '"--escribe": None' in b, \
        "sin marcas tiene que quedar vacio para que decida el relevo"
