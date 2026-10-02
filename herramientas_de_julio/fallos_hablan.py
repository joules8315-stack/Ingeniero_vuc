import sys, os, json
sys.path.insert(0, os.getcwd())
from cuerpo import director
raiz = os.getcwd()
ORIGEN = 'orden de Julio 2026-10-02: los fallos tienen que decir por que fallan'
RAZON = 'Palabras de Julio: de que me sirve que me diga que fallo si no dice por que. Medido el 2026-10-02: 11 ordenes caidas por sabotaje sin causa y todos los informes del perito en blanco.'
def orden(id_, titulo, pieza, vigia, depende, repara, encargo):
    return {'id': id_, 'titulo': titulo, 'pieza': pieza, 'vigia': vigia, 'depende': depende,
            'origen': ORIGEN, 'repara': repara, 'razon': RAZON, 'modo': 'IA', 'encargo': encargo}
VP1 = 'vigias/test_vigia_el_perito_dice_por_que_calla.py'
VS3 = 'vigias/test_vigia_el_sabotaje_dice_por_que_no_freno.py'
VS4 = 'vigias/test_vigia_sabotaje_py_dice_la_causa.py'
VS5 = 'vigias/test_vigia_toda_fallida_guarda_su_razon.py'
lista = [
 orden('V-P1-el_perito_dice_por_que_calla', 'Vigia: el perito dice por que calla', VP1, VP1, [],
  'Hoy, cuando el perito no entrega JSON, el informe sale en blanco y nadie sabe por que.',
  "Escribe la vigia " + VP1 + ". Debe estar ROJA hoy y ponerse verde cuando pedir_al_perito (cuerpo/capataz.py) explique por que calla. Caso 1: se pone en su sitio (monkeypatch) el subprocess.run que usa pedir_al_perito para que devuelva un objeto con returncode=7, stdout vacio y stderr='sin sesion iniciada'; se llama a pedir_al_perito y el motivo devuelto (segundo valor) debe contener 'codigo=7' y 'sin sesion iniciada'. Caso 2: subprocess.run lanza FileNotFoundError('no hay claude'); el motivo debe contener 'FileNotFoundError' y 'no hay claude'. Usa assert, nunca return False. No toca la memoria real ni la red. Mira el trozo de la funcion para ver como localiza el programa y que parametros recibe. Escribe el archivo entero."),
 orden('P1-el_perito_dice_por_que_calla', 'El perito escribe por que calla', 'cuerpo/capataz.py', VP1, ['V-P1-el_perito_dice_por_que_calla'],
  'pedir_al_perito solo mira stdout: si el programa falla, el motivo sale vacio (medido en todos los FORENSE del 2026-10-02).',
  "En cuerpo/capataz.py, funcion pedir_al_perito. Objetivo: que el motivo diga la causa. (1) Si no hay JSON, el motivo pasa a ser 'el perito no devolvio JSON: codigo=' + str(returncode) + ' | stderr=' + primeras 300 letras del error + ' | stdout=' + primeras 200 letras de la salida. (2) Si la llamada lanza una excepcion que no sea TimeoutExpired, el motivo es 'el perito no pudo arrancar: ' + nombre del tipo + ': ' + el mensaje (300 letras). No cambies los reintentos ni lo que devuelve (datos, motivo). Puedes escribir el archivo entero o el trozo."),
 orden('V-S3-el_sabotaje_dice_por_que_no_freno', 'Vigia: el sabotaje dice por que no freno', VS3, VS3, [],
  'Hoy el sabotaje dice solo "la vigia NO freno", sin la causa.',
  "Escribe la vigia " + VS3 + ". Debe estar ROJA hoy. Caso 1: monkeypatch de subprocess.run para que devuelva returncode=1 y stdout 'cuerpo/capataz.py: verde\\nSABOTAJE FALLO\\n'; se llama a capataz.sabotear_la_orden con la orden {'id':'x','vigia':'vigias/x.py','sabotaje':'CLAUDE.md','pieza':'cuerpo/capataz.py'} (CLAUDE.md es un archivo que existe, sirve de sabotaje ficticio). El resultado debe tener ok False y la razon debe contener 'NO freno' y 'verde'. Caso 2: subprocess.run lanza subprocess.TimeoutExpired; la razon debe contener '300'. Usa assert, nunca return False; no toca la memoria real. Escribe el archivo entero."),
 orden('S3-el_sabotaje_dice_por_que_no_freno', 'El sabotaje escribe la causa', 'cuerpo/capataz.py', VS3, ['V-S3-el_sabotaje_dice_por_que_no_freno'],
  'correr_orden_del_sistema devuelve solo el numero y tira lo que sabotaje.py imprimio; el bucle no puede decir cual de las 4 causas fue.',
  "En cuerpo/capataz.py. Objetivo: que sabotear_la_orden diga la causa cuando la vigia no frena. Decidido: una variable de modulo ULTIMA_SALIDA_DEL_SISTEMA (texto, empieza vacia). correr_orden_del_sistema la deja en '' al empezar y al terminar guarda en ella las ultimas 600 letras de stdout+stderr; si pasa el tiempo la deja en 'se paso de 300 s sin terminar'. El numero que devuelve NO cambia (las vigias viejas la ponen en su sitio). sabotear_la_orden, en la rama de fallo, escribe la razon actual seguida de ' CAUSA: ' + ULTIMA_SALIDA_DEL_SISTEMA, o ' CAUSA: sin salida' si esta vacia. Manten el texto actual 'la vigia NO freno'. Puedes escribir el archivo entero o el trozo."),
 orden('V-S4-sabotaje_py_dice_la_causa', 'Vigia: sabotaje.py dice la causa', VS4, VS4, [],
  'sabotaje.py no imprime si la vigia ya estaba roja antes de sabotear, ni explica cada estado.',
  "Escribe la vigia " + VS4 + ". Debe estar ROJA hoy. Con monkeypatch de arnes.sabotaje.sabotear para que devuelva {'sana': False, 'devuelta': True, 'resultados': [{'archivo':'a.py','estado':'roja'}], 'ok': False}, escribe en tmp_path un json con una lista vacia, pon sys.argv = ['sabotaje.py','vigias/x.py', ruta_del_json], llama a arnes.sabotaje.main() y con capsys comprueba que la salida contiene 'YA ESTABA ROJA'. Segundo caso: resultados con estado 'verde' -> la salida contiene 'SIGUE VERDE'. Tercero: estado 'no_encontrado' -> contiene 'VENCIDO'. Usa assert. Escribe el archivo entero."),
 orden('S4-sabotaje_py_dice_la_causa', 'sabotaje.py imprime la causa', 'arnes/sabotaje.py', VS4, ['V-S4-sabotaje_py_dice_la_causa'],
  'El sabotaje falla por 4 causas distintas y solo imprime SABOTAJE FALLO.',
  "En arnes/sabotaje.py, funcion main. Objetivo: antes de la linea final, imprimir la causa. Si sana es False: 'LA VIGIA YA ESTABA ROJA ANTES DEL SABOTAJE: no mide nada'. Por cada resultado con estado 'verde': 'LA VIGIA SIGUE VERDE CON EL CAMBIO DESHECHO: no protege'. Por cada 'no_encontrado': 'EL TEXTO A DESHACER YA NO ESTA EN EL ARCHIVO: sabotaje VENCIDO'. Los codigos de salida no cambian. Puedes escribir el archivo entero."),
 orden('V-S5-toda_fallida_guarda_su_razon', 'Vigia: toda fallida guarda su razon', VS5, VS5, [],
  'El estado dice fallida sin causa.',
  "Escribe la vigia " + VS5 + ". Debe estar ROJA hoy. Con una lista de ordenes en una carpeta temporal y monkeypatch de las funciones que leen y guardan la lista (mira marcar_estado, leer_lista y bucle en cuerpo/capataz.py), simula dos casos: (a) correr_una_orden devuelve {'guardado': False, 'salida': 'VEREDICTO   : RECHAZADO\\n  fallo       : falta la funcion x'}; (b) guardado True y sabotear_la_orden devuelve {'ok': False, 'razon': 'NO freno CAUSA: verde'}. Con forense y recoger_lo_frenado reemplazadas por funciones que no hacen nada, al terminar la ronda la orden debe tener el campo razon_del_fallo: en (a) con 'falta la funcion x' y en (b) con 'CAUSA: verde'. Usa assert; no toca la memoria real. Escribe el archivo entero."),
 orden('S5-toda_fallida_guarda_su_razon', 'Toda orden fallida guarda su razon', 'cuerpo/capataz.py', VS5, ['V-S5-toda_fallida_guarda_su_razon','S3-el_sabotaje_dice_por_que_no_freno'],
  'El estado dice fallida/no_aprobo/sabotaje y no dice por que.',
  "En cuerpo/capataz.py, funciones marcar_estado y bucle. Objetivo: cada vez que una orden pasa a 'fallida', se guarda en la orden el campo razon_del_fallo (maximo 600 letras): para no_aprobo, las lineas de la salida que empiezan con 'fallo' o 'VEREDICTO'; para sabotaje o SIN_TERMINAR, la razon que devuelve la funcion; para forense, el motivo. Decide tu como pasarla (parametro nuevo con valor por defecto en marcar_estado, o lo que veas) sin romper a quienes ya la llaman. Al volver a 'pendiente' o 'hecha' el campo se borra. Puedes escribir el archivo entero."),
]
for o in reversed(lista):
    ok, motivo = director.orden_nueva(raiz, json.dumps(o, ensure_ascii=False))
    print(o['id'], '->', ok, motivo)
