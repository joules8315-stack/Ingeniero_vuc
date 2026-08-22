# -*- coding: utf-8 -*-
"""vigias/test_vigia_fallos_de_verdad_avisan.py — LOS FALLOS APRENDIDOS TIENEN QUE AVISAR.

Julio, 2026-08-21:
  "Legisla sobre todos los fallos para que los tengas siempre presentes, crea vigias para que
   no vuelvan a suceder, legisla junto con esta instruccion."

EL AGUJERO QUE TAPA: guardar un fallo NO es aprenderlo. El 2026-08-21 habia 29 fallos guardados
y NINGUNO frenaba nada, porque les faltaba el DISPARADOR: la huella de lo que HACE la accion que
revive el fallo. Un fallo sin disparador es un diario, no un candado.

Por eso esta vigia no comprueba que los fallos esten guardados (eso es facil y no sirve de nada).
Comprueba que **puedan avisar**, y que las lecciones que a Julio le costo caro no se pierdan.

Si esta vigia se pone roja: alguien borro la memoria de fallos, o metio un fallo mudo, o se
perdio una leccion. Se arregla ANTES de seguir: repetir un fallo ya pagado es lo unico que Julio
ha dicho que no soporta.
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)


def _todos():
    """Lee la memoria de fallos tal cual esta en disco.

    El auditor pidio no usar `_leer` por llevar guion bajo. Se comprobo en el propio taller antes
    de hacerle caso: las vigias de aqui YA miran por dentro cuando hace falta (asi se comprueba
    que el cerebro es el que se pidio, y asi se comprueba que las tildes no rompen la busqueda).
    Era consejo general, no la costumbre de esta casa. Inventar un nombre de funcion que no
    existe —que es lo que se hizo primero— si estuvo mal, y por eso estas cinco pruebas fallaron.
    """
    from cuerpo import fallos
    return fallos._leer()


def test_la_memoria_de_fallos_no_esta_vacia():
    """Si algun dia amanece vacia, es que una comprobacion la piso. Ya paso: 27 perdidos de 32."""
    assert len(_todos()) >= 30, \
        "la memoria de fallos encogio: alguien la piso. NO se sigue hasta recuperarla"


def test_ningun_fallo_es_MUDO():
    """Un fallo sin disparador se guarda pero NUNCA avisa. Es un diario, no un candado."""
    mudos = [f.get("que_paso", "?")[:60] for f in _todos() if not str(f.get("disparador", "")).strip()]
    assert not mudos, \
        "hay %d fallo(s) que nunca van a avisar (sin disparador): %s" % (len(mudos), mudos[:5])


def test_todo_fallo_dice_QUE_NO_VOLVER_A_HACER():
    """La leccion en una frase es lo mas valioso del apunte. Sin ella no se aprendio nada."""
    sin = [f.get("que_paso", "?")[:60] for f in _todos() if not str(f.get("no_volver_a", "")).strip()]
    assert not sin, "hay fallo(s) sin leccion: %s" % sin[:5]


def test_las_lecciones_del_2026_08_21_siguen_ahi():
    """Las ocho que Julio pago con su tiempo ese dia. Cada una se busca por lo que ENSENA, no por
    su titulo: un titulo se reescribe, la leccion no."""
    texto = " ".join(
        (str(f.get("que_paso", "")) + " " + str(f.get("no_volver_a", "")) + " " +
         str(f.get("disparador", "")) + " " + str(f.get("leccion_disparo", ""))).lower()
        for f in _todos())
    lecciones = {
        "trabajar a solas sin el equipo": "equipo",
        "asumir de que proyecto habla Julio": "proyecto",
        "mandar un encargo sin el trozo de codigo": "adjunt",
        "pegar un encargo viejo delante del nuevo": "encargo",
        "dar una cifra a bulto pudiendo medirla": "medid",
        "citar un archivo que ya cambio": "leido hace rato",
        "cerrar sin llamar al supervisor de pago": "sin_auditar",
        "creerle a un cerebro sin mirar el codigo": "sin haberlo comprobado",
    }
    perdidas = [nombre for nombre, marca in lecciones.items() if marca.lower() not in texto]
    assert not perdidas, \
        "se perdieron lecciones que ya costaron caro: %s" % perdidas


def test_el_disparador_es_una_SENAL_y_no_una_frase():
    """FALLO PROPIO del 2026-08-21, el mas fino de todos.

    Se les puso disparador a 24 fallos mudos... en forma de frase bonita en castellano. Parecian
    curados. Pero el candado COMPARA el disparador con el texto de la accion que viene: una frase
    larga no coincide nunca. Seguian tan mudos como antes, y encima ahora lo disimulaban.

    Y no era solo cosa de esta sesion: 7 de los fallos viejos arrastraban el mismo defecto.

    Un disparador tiene que ser una SENAL: trozos cortos separados por barras, de lo que de
    verdad aparece cuando alguien esta a punto de repetir el fallo.
    """
    malos = []
    for f in _todos():
        d = str(f.get("disparador", "")).strip()
        if "|" not in d and len(d.split()) > 4:
            malos.append(" ".join(str(f.get("que_paso", "")).split())[:60])
    assert not malos, (
        "hay %d disparador(es) escritos como FRASE: no van a coincidir con nada y el fallo "
        "sigue mudo aunque lo parezca. Son: %s" % (len(malos), malos[:5]))


def test_ningun_disparador_salta_con_todo():
    """Un aviso que salta siempre se vuelve ruido y se acaba ignorando: peor que no tenerlo.

    Paso de verdad en esta sesion: se puso una senal tan ancha que saltaba al tocar CUALQUIER
    vigia. Las senales que valen son las que aparecen cuando alguien esta a punto de repetir el
    fallo, no las que aparecen en el trabajo de todos los dias.
    """
    demasiado_anchas = {"vigia", "test", "python", "archivo", "codigo", "def", "import", "self"}
    malos = []
    for f in _todos():
        for trozo in str(f.get("disparador", "")).split("|"):
            t = trozo.strip().lower()
            if t and t in demasiado_anchas:
                malos.append(t)
    assert not malos, \
        "hay senales que saltan con casi todo (se vuelven ruido y se ignoran): %s" % sorted(set(malos))


def test_el_disparador_no_es_un_nombre_de_archivo():
    """Julio, 2026-08-21: 'en vez de buscar por nombre, se busca por funcion, por lo que hace,
    asi es mas dificil equivocarse.' Un disparador con nombre de archivo envejece y deja de
    disparar en cuanto alguien renombra algo."""
    import re
    malos = []
    for f in _todos():
        d = str(f.get("disparador", ""))
        if re.search(r"[a-z_]+\.(py|json|html|js|md)\b", d.lower()):
            malos.append(d[:70])
    assert not malos, \
        "hay disparadores atados a un NOMBRE de archivo (envejecen y dejan de avisar): %s" % malos[:5]
