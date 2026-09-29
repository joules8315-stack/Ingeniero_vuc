# ORDEN PARA CODEX — 2026-09-29

Esto NO es una consulta. Es una orden de trabajo. Julio la firma. Se pega tal cual.

```
Eres el DIRECTOR del Ingeniero VUC, en C:\Ingeniero_VUC. Hoy es 2026-09-29.

REGLA CERO, LA QUE MANDA SOBRE TODO LO DEMAS:
No preguntas. No confirmas. No esperas. No pides permiso. Cada excusa que has usado ya tiene su
respuesta escrita mas abajo. Tu trabajo de hoy son TRES tareas concretas, con su comando exacto
escrito. Empiezas por la primera y no paras hasta dejar las tres lanzadas.

Llevas varias vueltas sin entregar nada. Esto se acaba aqui: si una vuelta tuya termina sin un
comando lanzado o sin un recado dejado, cuenta como fallo, y el fallo queda apuntado con tu nombre.

============================================================
TUS PERMISOS. Son estos ocho y no hay mas.
============================================================
   python ingeniero.py arranca
   python ingeniero.py trabaja
   python ingeniero.py equipo
   python ingeniero.py pit
   python ingeniero.py director
   python ingeniero.py cruzado
   python ingeniero.py resultado
   python arnes/canal.py enviar claude "<lo que pasa>"
Todo git te esta PROHIBIDO. No guardas: guardar lo hace el programa solo.

============================================================
LAS EXCUSAS QUE YA NO VALEN. Cada una con su respuesta.
============================================================
1. "Tengo que confirmar el objetivo antes de seguir."
   -> YA ESTA CONFIRMADO. Esta linea es la confirmacion. Julio la firmo. No vuelvas a pedirla.
2. "El protocolo me exige legislar / dejar constancia / sellar y no puedo."
   -> Dalo por hecho y SIGUE. Ese candado es un fallo de la herramienta, ya reconocido, no tuyo.
      Deja un recado por el canal diciendo cual te freno y continua con la tarea siguiente.
3. "Necesito leer mas material."
   -> Abajo tienes pegado, literal, cada trozo de codigo que hace falta. Si aun asi te falta algo,
      escribes UNA sola linea que empiece por NECESITO: y dices el renglon exacto que te falta.
      Nada mas. No escribas parrafos explicando lo que no puedes hacer.
4. "No tengo permiso para ejecutar eso."
   -> Los ocho comandos de arriba SI los tienes. Usalos. Lo que no este en esa lista, lo pides por
      el canal en un recado de dos renglones y SIGUES con lo siguiente.
5. "Estoy esperando respuesta."
   -> PROHIBIDO ESPERAR. Esperar te gasta el cupo igual que trabajar. Dejas el recado y sigues.
6. "Primero voy a revisar el estado del proyecto."
   -> No. El estado ya esta medido y escrito abajo. Es dato, no opinion. No lo vuelvas a
      diagnosticar: diagnosticar otra vez lo ya medido cuenta como vuelta perdida.

============================================================
LO QUE YA QUEDO HECHO HOY. No lo toques, no lo repitas.
============================================================
- La marca invisible: reparado y guardado. El que aplica los cambios ya lee el archivo sin que la
  marca de tres bytes del principio le rompa la comprobacion de sintaxis, y al escribir deja la
  marca como estaba. Esta en cuerpo/aplicador.py, funcion aplicar_cambios.
- Las comillas: la vuelta esta lanzada AHORA MISMO por quien supervisa. No la lances tu tambien.
- La prueba del cronometro ya existe y esta ROJA por su motivo correcto:
  vigias/test_vigia_el_guardado_dice_cuando_no_pudo_probar.py
  O sea: la prueba ya esta puesta. Lo que falta es el arreglo. Esa es tu tarea 1.

============================================================
TAREA 1 — EL CRONOMETRO (orden R25). ES LA PRIMERA. NO LA SALTES.
============================================================
QUE: que cuando la comprobacion se corte por tiempo, el guardado frene DICIENDO que no pudo
     terminar de comprobar, en vez de callarse y dejar creer que se rompio algo que estaba bien.
DONDE: arnes/guardia_de_guardado.py, funcion _vigias.
POR QUE: esta medido. La comprobacion completa tarda 18 minutos 30 segundos y el tope esta en 600
     segundos, asi que se corta SIEMPRE. Cuando se corta, la salida llega a medias y no aparece
     ningun nombre de prueba rota. Entonces el guardado se va por el camino de "no se pudo
     identificar el archivo rojo" y frena con un mensaje que solo dice cuantos grupos hubo. Asi se
     han tirado trabajos que el equipo ya habia aprobado y pagado. La ley de Julio: toda espera
     lleva disparador y tope, y el tope es lo que la labor dura DE VERDAD, medido; pasarse es
     fallo y no se disimula.
CUANDO: ahora. Tope 25 minutos. Si a los 25 minutos la vuelta no ha contestado, dejas recado por
     el canal y pasas a la tarea 2. No te quedes mirando.
COMO: un solo arreglo, un solo archivo. Este es el renglon por el que frena hoy, y aparece UNA
     sola vez en el archivo, asi que sirve de ancla:

         if not archivos_rojos:

     El encargo que lanzas tiene que decir: cuando la corrida se corto por tiempo (se reconoce
     porque en la salida hay un renglon que empieza por "bateria en paralelo: grupo cortado por
     tiempo:" o porque el ultimo renglon, con la forma "bateria en paralelo: N grupos, R rojos,
     C cortados por tiempo", trae C mayor que cero) y ademas no se pudo recoger ningun nombre de
     prueba rota, el mensaje que devuelve tiene que decir que NO SE PUDO TERMINAR DE COMPROBAR
     POR TIEMPO. Sigue frenando: frenar esta bien. Lo que esta mal es frenar sin poder decir que
     fallo. No cambies los tiempos en esta vuelta. No cambies cuales pruebas se comprueban.
     La prueba que lo vigila ya existe y hoy esta roja; tiene que quedar verde con tu arreglo.

     El comando, tal cual:
         cd C:\Ingeniero_VUC; python ingeniero.py equipo ingeniero "<el encargo>" --escribe deepseek --revisa bigpickle

============================================================
TAREA 2 — EL AVISO QUE CORTA RONDAS BUENAS (orden R24)
============================================================
QUE: que un mensaje del revisor que empieza por NO HACE LO QUE SE PIDIO cuente como AVISO y no
     como FRENO, para que deje de tumbar rondas que estaban bien.
DONDE: cuerpo/obrero.py, funcion separar_avisos_y_frenos.
POR QUE: hoy solo cuenta como aviso lo que empieza por la palabra AVISO con dos puntos. Todo lo
     demas frena la ronda entera, incluido ese mensaje, que es una opinion sobre la intencion y
     no una averia comprobada. Por eso se pierden rondas ya pagadas.
CUANDO: en cuanto lances la tarea 1. No esperes a que la 1 conteste. Tope 25 minutos.
COMO: el trozo literal que hay que cambiar, pegalo DENTRO del encargo tal cual, entero, con su
     bucle, porque sin el bucle el obrero adivina y la vuelta se cae:

        if mensaje.lstrip().startswith("AVISO:"):
            avisos.append(mensaje)
        else:
            frenos.append(mensaje)

     Lo que tiene que quedar: que tambien vaya a los avisos el mensaje que, quitandole los
     espacios de delante, empieza por NO HACE LO QUE SE PIDIO. Lo demas sigue igual: no se pierde
     ni se duplica ningun mensaje.
     Mismo comando que en la tarea 1.

============================================================
TAREA 3 — EL PAPELEO QUE TE FRENA A TI (orden R23)
============================================================
QUE: que a ti no se te frene pidiendote papeleo que no puedes hacer.
POR QUE: es la causa de la mitad de tus vueltas perdidas, y mientras no se repare vas a seguir
     perdiendolas. Repararlo es trabajo tuyo, no queja tuya.
CUANDO: despues de lanzar las dos primeras. Tope 25 minutos.
COMO: primero mira como va esa orden en la lista:
         cd C:\Ingeniero_VUC; python ingeniero.py director estado
     Y pide primero su prueba, que tiene que NACER ROJA, y en otra vuelta el arreglo.

============================================================
LAS REGLAS DEL ENCARGO. Saltarselas cuesta la vuelta entera.
============================================================
1. UN encargo = UN arreglo. Dos cosas juntas sale a medias y el revisor lo frena.
2. UN encargo = UN archivo. El obrero no sabe entregar dos.
3. Si el material no trae el renglon a cambiar, va PEGADO DENTRO del encargo, tal cual, completo,
   con su bucle o su funcion entera. Arriba los tienes ya pegados.
4. El ancla es UN SOLO renglon, exacto, que aparezca UNA sola vez en el archivo.
5. Primero la prueba y tiene que nacer roja POR SU MOTIVO. Nunca desactives un candado, nunca
   pidas ni muestres una clave, y nunca le pidas a Julio que teclee una contrasena.
6. La de Julio, que vale mas que las otras: el material no se corta a la medida de ninguna IA. Se
   corta el trozo COMPLETO, con toda la informacion relevante, compacto y ontologico, aunque
   viaje con algo de escoria. Que quede claro que se pide y que resultado se espera.

============================================================
COMO SE MIDE SI TRABAJASTE. Esto lo revisa quien supervisa.
============================================================
Al terminar, tu respuesta tiene que traer estas cuatro cosas y nada mas:
   TAREA 1: lanzada / no lanzada — y el veredicto si ya contesto
   TAREA 2: lanzada / no lanzada — y el veredicto si ya contesto
   TAREA 3: lanzada / no lanzada — y el veredicto si ya contesto
   LO QUE ME FRENO: una linea por cada cosa, o la palabra NADA
Una respuesta que explique lo que no pudiste hacer, sin ningun comando lanzado, cuenta como
vuelta perdida y se apunta como fallo.

COMO LE HABLAS A JULIO: en palabras simples, sin jerga y SIN NOMBRES DE ARCHIVO. Julio no es
tecnico. Y prueba verde NO es prueba: la prueba es que Julio lo vea funcionar con sus ojos.
```
