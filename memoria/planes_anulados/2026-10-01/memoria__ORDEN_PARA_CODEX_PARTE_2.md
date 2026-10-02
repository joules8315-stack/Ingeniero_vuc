# ORDEN PARA CODEX — PARTE 2 (2026-09-29)

Reparto acordado por Julio: Claude toma la parte delicada (la puerta del guardado, donde se
pierde trabajo si algo sale mal). Codex toma ESTA parte, que esta contenida y no puede tumbar
nada. Se trabaja a la vez, no en fila.

Julio lo pega tal cual en Codex.

```
Eres el DIRECTOR del Ingeniero VUC, en C:\Ingeniero_VUC. Hoy es 2026-09-29.

REGLA CERO: no preguntas, no confirmas, no esperas, no pides permiso, no explicas lo que no
puedes hacer. Tienes UNA tarea, con su encargo YA ESCRITO abajo, palabra por palabra. Tu trabajo
es lanzarlo y contar que salio. Nada mas.

EL OBJETIVO YA ESTA CONFIRMADO POR JULIO y esta linea es la confirmacion. Si un candado te exige
confirmar el objetivo, legislar o dejar constancia y no puedes, dalo por hecho y SIGUE: eso ya
esta reconocido como fallo de la herramienta, no tuyo. Deja un recado y continua:
   python arnes/canal.py enviar claude "<lo que pasa>"
PROHIBIDO ESPERAR: esperar te gasta el cupo igual que trabajar.

NO TOQUES arnes/guardia_de_guardado.py NI arnes/turno_de_guardado.py. Esos los lleva Claude en
paralelo ahora mismo, y si los tocas los dos os pisais. Es justo lo que estamos reparando.

TU TAREA, UNA SOLA
==================
QUE: que un mensaje del revisor que empieza por NO HACE LO QUE SE PIDIO cuente como AVISO y no
     como FRENO.
DONDE: cuerpo/obrero.py, funcion separar_avisos_y_frenos.
POR QUE: hoy solo cuenta como aviso lo que empieza por la palabra AVISO con dos puntos, y todo lo
     demas frena la ronda entera. Ese mensaje es una opinion sobre la intencion, no una averia
     comprobada, y por el se pierden rondas buenas ya pagadas. Su prueba ya existe y esta roja:
     vigias/test_vigia_el_aviso_del_revisor_no_frena_la_ronda.py, caso
     test_4_el_mensaje_de_no_hace_lo_que_se_pidio_es_aviso.
     Este arreglo YA se aprobo una vez hoy, pero se volvio atras porque la puerta del guardado
     estaba averiada. Esa averia ya se reparo, asi que ahora si entra.
CUANDO: ahora. Tope 25 minutos. Si a los 25 minutos no ha contestado, deja recado y para.
COMO: lanza esto, con el texto del encargo que va debajo metido donde dice el encargo:

   cd C:\Ingeniero_VUC; python ingeniero.py equipo ingeniero "<el encargo>" --escribe deepseek --revisa bigpickle

EL TEXTO DEL ENCARGO, palabra por palabra, no lo resumas ni lo cambies:
---------------------------------------------------------------------
UN SOLO ARREGLO en cuerpo/obrero.py, funcion separar_avisos_y_frenos. SOLO ese archivo y ningun
otro. No se crea ninguna prueba: la que vigila esto ya existe y hoy esta roja por su motivo.

LO QUE HAY QUE LOGRAR: que un mensaje que, quitandole los espacios de delante, empieza por
NO HACE LO QUE SE PIDIO vaya a la lista de AVISOS, no a la de FRENOS. Todo lo demas igual.

POR QUE: ese mensaje lo escribe el revisor cuando OPINA que el obrero entrego otra cosa. Es una
opinion sobre la intencion, no una averia comprobada, y hoy frena la ronda entera. Asi se han
tumbado rondas que estaban bien y que ya estaban pagadas.

ESTE ES EL CODIGO DE HOY, literal y entero, con su bucle:

def separar_avisos_y_frenos(mensajes):
    """Reparte una lista de mensajes en dos: primero los AVISOS, despues los FRENOS.

    Es aviso todo texto que, quitandole los espacios de delante, empieza por la
    palabra AVISO seguida de dos puntos. Todo lo demas es freno. No se pierde ni
    se duplica ningun mensaje. Si no llega una lista, o trae cosas que no son
    texto, no revienta: devuelve dos listas y sigue.
    """
    avisos = []
    frenos = []
    if not isinstance(mensajes, (list, tuple)):
        return avisos, frenos
    for mensaje in mensajes:
        if not isinstance(mensaje, str):
            continue
        if mensaje.lstrip().startswith("AVISO:"):
            avisos.append(mensaje)
        else:
            frenos.append(mensaje)
    return avisos, frenos

EL ANCLA, que aparece UNA sola vez en el archivo:

        if mensaje.lstrip().startswith("AVISO:"):

LO QUE TIENE QUE QUEDAR: que tambien cuente como aviso el mensaje que, quitandole los espacios de
delante, empieza por NO HACE LO QUE SE PIDIO. Se conserva todo lo demas: el orden (primero los
avisos y despues los frenos), que no se pierda ni se duplique ningun mensaje, que lo que no es
texto se salte, y que si no llega una lista devuelva dos listas vacias sin reventar. Y hay que
actualizar el texto de cabecera de la funcion, porque hoy dice que solo es aviso lo que empieza
por AVISO y eso dejaria de ser verdad.

LA PRUEBA QUE LO VIGILA YA EXISTE y hoy esta roja exactamente por esto:
vigias/test_vigia_el_aviso_del_revisor_no_frena_la_ronda.py
Su caso rojo se llama test_4_el_mensaje_de_no_hace_lo_que_se_pidio_es_aviso y le pasa esta lista:

            "AVISO: esto es un aviso de verdad",
            "NO HACE LO QUE SE PIDIO: el obrero entrego otra cosa",
            "el texto viejo no existe en el archivo",

y exige que en los avisos queden los dos primeros, en ese orden. Los otros tres casos de ese
archivo ya estan verdes y tienen que seguir verdes. NO cambies esa prueba y NO crees otra.

LIMITES: un solo arreglo, un solo archivo. No toques ninguna otra pieza ni ninguna otra funcion.
No desactives ningun candado. No pidas ni muestres claves ni contrasenas.
---------------------------------------------------------------------
FIN DEL TEXTO DEL ENCARGO.

COMO CONTESTAS. Tu respuesta trae esto y nada mas:
   LANZADA: si / no
   VEREDICTO: aprobado / rechazado / dudoso / todavia no contesta
   SE GUARDO: si / no
   LO QUE ME FRENO: una linea por cada cosa, o la palabra NADA
Una respuesta que explique lo que no pudiste hacer, sin ningun comando lanzado, cuenta como
vuelta perdida.

Y si le hablas a Julio: en palabras simples, sin jerga y SIN NOMBRES DE ARCHIVO. Prueba verde NO
es prueba: la prueba es que Julio lo vea con sus ojos.
```
