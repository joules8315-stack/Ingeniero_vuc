# CONTRATO DE LOS CUATRO OBJETIVOS ORQUESTADOS

> Documento de ley. No es codigo. En esta ronda no se toca ningun archivo `.py`.
> Orden de Julio del 2026-09-28, dada despues de la ley de la multitarea y apoyada en ella.

---

## LA LEY, EN POCAS FRASES

1. Los cuatro objetivos del proyecto (rapidez, precision, economia y eficiencia) se declaran por escrito como **flujos**, no como ideas sueltas. Un objetivo que no esta declarado no se puede repartir ni medir.
2. Cada trabajo de la lista dice **a que objetivo sirve** y **a que flujo pertenece**. Sin eso, la reparacion nace suelta.
3. Se trabaja **a la vez pero orquestado**: un agente por objetivo, y la coherencia la pone la cola, no la buena voluntad.
4. Cada objetivo tiene **un numero que lo mide**, y lo mide un programa, no una opinion. El agente de un objetivo se juzga por su numero, no por su relato.
5. Antes de sellar cualquier trabajo, incluida una reparacion, se pasa la **puerta de regresion**: ninguno de los cuatro numeros puede empeorar.
6. La **interaccion entre flujos se comprueba**, no se supone: al tocar una pieza se corren las vigias de su flujo y de los flujos con los que se relaciona.
7. Cada pieza se tiene en cuenta **como un flujo**, y tambien **como interactua con los demas**, de modo que no se entorpezcan ni rompan piezas o flujos que ya funcionan.
8. Donde un programa pueda hacer el trabajo, lo hace el programa y no la IA.
9. Quien dirige ordena las modificaciones segun lo que se vaya corrigiendo, y ese orden se escribe **en la lista de trabajos, nunca en la conversacion**.

---

## REGLAS NUMERADAS

### Regla 1. Los cuatro objetivos son flujos declarados

Rapidez, precision, economia y eficiencia existen **escritos**, cada uno con las piezas que reune y las leyes que lo mandan. Un objetivo que no esta declarado no se puede repartir ni medir.

### Regla 2. Cada trabajo dice su objetivo y su flujo

Todo trabajo de la lista tiene que decir, en la propia lista:

- a que objetivo sirve (rapidez, precision, economia o eficiencia);
- a que flujo pertenece.

Sin esas dos cosas, la reparacion nace suelta y no se le puede dar un objetivo a un agente.

**Evidencia medida el 2026-09-28:** un trabajo de la lista dice su pieza, de que depende y que vigia lo protege, pero no hay ningun sitio donde diga su objetivo.

### Regla 3. Un agente por objetivo, y la coherencia la pone la cola

Cada agente se encarga de **un solo** objetivo y lo afina. La coherencia entre agentes no la pone la buena voluntad: la pone la cola, que ya sabe que no puede ir junto.

Dos trabajos del mismo flujo **no corren a la vez**, aunque toquen archivos distintos, porque un flujo es una unidad de sentido, no un archivo.

### Regla 4. Cada objetivo tiene un numero, y lo mide un programa

| Objetivo | Numero que lo mide |
|---|---|
| Rapidez | minutos de reloj por trabajo cerrado |
| Precision | de cada cien rondas, cuantas mueren o se rechazan |
| Economia | cuantos trabajos escribio el cerebro gratis, y cuantos dolares se gastaron |
| Eficiencia | que parte del reloj se fue **dentro** de las IA |

**Evidencia medida el 2026-09-28:** la parte del reloj que se fue dentro de las IA fue del **15 por ciento**.

El agente de un objetivo se juzga por su numero, no por su relato.

### Regla 5. Puerta de regresion

Un trabajo **no se sella** si alguno de los cuatro numeros empeora, ademas de lo que ya se exige:

- las vigias vecinas del mismo color;
- ninguna vecina en rojo.

Hoy solo se miran las vigias. Por eso un cambio puede dejar todo verde y volver el sistema mas lento o mas caro sin que nadie lo note. Esto es lo que Julio pide cuando dice que lo nuevo no rompa lo que ya sirve.

### Regla 6. La interaccion entre flujos se comprueba

Al tocar una pieza se corren las vigias de **su flujo** y de **los flujos con los que ese flujo se relaciona**, no solo las del archivo vecino.

Lo que hoy existe es la vecindad por archivo. **Falta la vecindad por asunto.**

### Regla 7. El disparador con tope medido aplica a todas las capas

Cada espera del proyecto tiene su tope sacado de lo medido, y pasarse es fallo. Esto ya es ley en `CONTRATO_TOPE_MEDIDO_Y_CORTE_A_MINIMA_EXPRESION.md`. Aqui se deja dicho que **aplica a todas las capas por igual**, no solo a la que se este reparando.

### Regla 8. Donde pueda un programa, no lo hace la IA

Donde un programa pueda hacer el trabajo, lo hace el programa y no la IA, porque sale mas preciso, mas rapido y mas barato. Esto ya es ley en `CONTRATO_MENOS_IA_MAS_PROGRAMA`. Aqui se deja dicho que es parte del objetivo de **precision**, no solo del de economia.

### Regla 9. El orden de las modificaciones vive en la lista, no en el chat

Quien dirige ordena las modificaciones segun lo que se vaya corrigiendo, y ese orden se escribe **en la lista de trabajos, nunca en la conversacion**. Una decision que vive solo en el chat no la respeta la maquina.

**Evidencia medida el 2026-09-28:** un trabajo que Julio habia frenado fue tomado igual por la cadena, porque el freno vivia solo en la conversacion.

---

## LOS DOS EJEMPLOS DE JULIO, QUE FIJAN EL SENTIDO

### Ejemplo de rapidez

Correr varias tareas ya mejora la rapidez. Pero dentro de rapidez esta ademas:

- que la IA no demore una hora;
- que responda por disparador;
- que el maximo sean diez o quince minutos segun las mediciones;
- que eso se aplique a **todas las capas del proyecto** en situaciones similares.

### Ejemplo de precision

La precision depende de:

- la indexacion de la memoria;
- que el repartidor encuentre el bloque correspondiente;
- que se reemplacen las IA por programas donde se pueda, porque el programa es mas preciso, mas rapido y mas economico.

---

## TABLA DE LOS CUATRO OBJETIVOS

Una fila por objetivo. Donde algo todavia no exista, se escribe **FALTA**, sin inventar nombres: eso es justamente lo que hay que construir.

| Objetivo | Que lo mide (el numero) | Donde se mide | Que ley manda | Que candado frena | Que vigia comprueba |
|---|---|---|---|---|---|
| Rapidez | minutos de reloj por trabajo cerrado | FALTA | `CONTRATO_TOPE_MEDIDO_Y_CORTE_A_MINIMA_EXPRESION.md` | FALTA | FALTA |
| Precision | de cada cien rondas, cuantas mueren o se rechazan | FALTA | `CONTRATO_MENOS_IA_MAS_PROGRAMA` | FALTA | FALTA |
| Economia | cuantos trabajos escribio el cerebro gratis, y cuantos dolares se gastaron | FALTA | FALTA | FALTA | FALTA |
| Eficiencia | que parte del reloj se fue dentro de las IA | FALTA | FALTA | FALTA | FALTA |

---

## COMO SE COMPRUEBA

1. **Objetivos declarados.** Se comprueba que los cuatro objetivos estan escritos como flujos, con sus piezas y sus leyes. Si alguno no esta declarado, no se puede repartir ni medir.
2. **Trabajo con objetivo y flujo.** Se comprueba que cada trabajo de la lista dice a que objetivo sirve y a que flujo pertenece. Si le falta, no se reparte.
3. **Un agente por objetivo.** Se comprueba que cada agente tiene asignado un solo objetivo.
4. **Coherencia por cola.** Se comprueba que dos trabajos del mismo flujo no corren a la vez, aunque toquen archivos distintos.
5. **Numero por objetivo.** Se comprueba que cada objetivo tiene su numero y que lo mide un programa, no una opinion.
6. **Puerta de regresion.** Se comprueba que ninguno de los cuatro numeros empeora antes de sellar un trabajo, ademas de las vigias vecinas del mismo color y de que ninguna vecina este en rojo.
7. **Interaccion entre flujos.** Se comprueba que al tocar una pieza se corren las vigias de su flujo y de los flujos con los que se relaciona, no solo las del archivo vecino.
8. **Tope medido en todas las capas.** Se comprueba que cada espera del proyecto tiene su tope sacado de lo medido y que pasarse es fallo.
9. **Programa antes que IA.** Se comprueba que donde un programa pueda hacer el trabajo, lo hace el programa.
10. **Orden en la lista.** Se comprueba que el orden de las modificaciones vive en la lista de trabajos y no en la conversacion.

---

## LO QUE ESTE CONTRATO NO HACE

Este contrato no toca ningun archivo `.py`. Es un documento de ley. Las reparaciones de las piezas que hoy incumplen van en otra ronda, y quien las haga tiene que citar este contrato.

---

## PREGUNTAS ABIERTAS

- PREGUNTA_REQUERIDA: donde se mide hoy cada uno de los cuatro numeros, y con que programa. En el material no aparece ningun sitio ni ningun programa que los mida, por eso la tabla lleva FALTA en la columna "donde se mide".
- PREGUNTA_REQUERIDA: que candado frena hoy cada objetivo. En el material no aparece ningun candado por objetivo, por eso la tabla lleva FALTA en la columna "que candado frena".
- PREGUNTA_REQUERIDA: que vigia comprueba hoy cada objetivo. En el material solo se nombran las vigias vecinas por archivo, no por flujo ni por objetivo, por eso la tabla lleva FALTA en la columna "que vigia comprueba".
- PREGUNTA_REQUERIDA: que ley manda hoy sobre economia y sobre eficiencia. En el material no aparece ninguna ley que las mande, por eso esas celdas llevan FALTA.
- PREGUNTA_REQUERIDA: como se relaciona cada flujo con los demas, para poder correr la vecindad por asunto. En el material no aparece ese mapa de relaciones.
