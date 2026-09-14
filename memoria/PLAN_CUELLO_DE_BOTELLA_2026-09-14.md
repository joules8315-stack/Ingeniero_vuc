# PLAN PARA EL CUELLO DE BOTELLA — 2026-09-14

Estado: **APROBADO POR JULIO el 2026-09-14** ("si, acepto"). Los puntos 7 a 13 se anadieron despues de su
aprobacion (salen de sus propias palabras que el resumen habia dejado fuera, y de la medicion del sueño del PC):
se le informaron en la misma respuesta.
Base: `memoria/FORENSE_BIG_PICKLE_2026-09-14.md` + medicion de Claude del mismo dia.

## A. MEDICION (hecha con busquedas en las conversaciones y registros, sin IA)

### A1. Aviso de memoria
- Frenos en las 3 conversaciones grandes (11 al 14 sept): **964**.
- Veces que despues la IA mando **la MISMA accion identica** y paso: **890 (92%)**.
  -> En 9 de cada 10 frenos el aviso no cambio nada: solo costo una vuelta pagada.
- Causa de fondo: las 68 lecciones se disparan por **palabras** que aparecen en la accion, no por el
  peligro real. Ejemplo vivo de hoy: un programa de medicion fue frenado por la leccion "el juez del cerebro".
- El contador dice `frenos_falsos=0` porque **nadie mide los falsos**: solo sube cuando frena.
- Ojo: las conversaciones repiten algunos mensajes; el numero absoluto puede estar inflado, la proporcion no.

### A2. Un cambio por ronda
- No hay ley que lo pida. Es como se construyo: el aplicador recibe **un solo pedazo** (texto viejo -> nuevo)
  y el comando equipo lo llama **una vez** por ronda (`ingeniero.py:427`, `cuerpo/aplicador.py:151-157`).
- Nada tecnico impide aplicar varios pedazos juntos, todos o ninguno.

### A3. Revisor
- Rondas 12-14 sept: 91 -> 43 aprobadas, 13 rechazadas por la IA revisora, **34 rechazadas por el programa**.
- Motivos del programa (74 leidos en las conversaciones):
  - **54% "NO HACE LO QUE SE PIDIO"**: compara palabras del encargo con el pedazo. Como el encargo describe
    el arreglo COMPLETO y cada ronda lleva UN pedazo, las palabras de los otros pedazos "faltan" y frena.
    -> **Probablemente falsos en su mayoria, y nacen del punto A2.** Ya se parcho 4 veces (08, 13, 13, 14 sept): se parcha el sintoma.
  - **31% "USA UN NOMBRE QUE NO EXISTE"**: mezclado. Hubo reales (una ronda con 16 errores de nombre) y falsos ya parchados. Falta caso por caso.
  - **15% vacio / humo / codigo roto**: justos.
- Causa de fondo: **los candados no anotan por que frenaron ni si acertaron**. Sin eso nadie sabe cuales son falsos.

### A4. Pruebas
- 134 vigias corren **una detras de otra** en cada guardado. No esta instalado nada para correrlas en paralelo.

## B. DECISIONES DE JULIO (2026-09-14) — la intencion de las leyes

1. **Vigia que nace roja**: nace roja solo para probar que el candado muerde. Se repara, se pone verde,
   el equipo comprueba que es lo pedido y aprueba, **y ahi se guarda**. "No se guarda con roja" habla
   del guardado final, no del nacimiento. No hay contradiccion: son momentos distintos.
2. **El copista es parte del equipo**: es una herramienta del equipo para no gastar. Lo que copia lo
   aprobado por el equipo cuenta como trabajo del equipo.
3. **Leyes**: se leen por su intencion, revisando que el flujo sea acorde; asi se encuentra la armonia.
4. **Esperar pruebas**: es tonto detenerse. Se lanzan todas las pruebas a la vez si se puede; se
   clasifican: la que pasa se guarda; la que no pasa se busca por que (sintaxis, herramienta, IA sin
   contexto, vacio por codigo nuevo...). Si es problema real se repara; si es problema tonto se repite.
5. **Causa raiz general**: muchos "pensadores" sin metodo que asumen, inventan y no piden la memoria.
   Todo lo que se pueda se convierte en **programa** (operaciones fijas, skills). El metodo:
   requerimiento -> analisis pidiendo la informacion -> raiz(es) -> legislar, candado, vigias (y vigia de
   no romper), nace conectado, en los archivos exactos -> herramientas -> repartir -> ejecutar ->
   supervisar -> aprobar (tras reparar la roja de nacimiento) -> guardar, o volver a buscar la raiz.

## C. PLAN (orden propuesto, cada paso con su vigia; ninguno quita un candado protector)

0. **Todo freno anota por que freno y si acerto** (se mira despues si la accion se repitio igual o si la prueba paso). Sin esto no hay causa raiz.
1. **Varios cambios en una ronda**: una aprobacion lleva la lista completa de pedazos; se aplican todos o ninguno.
2. **Revisor mira el arreglo completo**, no pedazo por pedazo -> desaparece la mayoria de "no hace lo que se pidio".
3. **Aviso de memoria sale del camino**: las lecciones viajan dentro del paquete ANTES de trabajar (cero vueltas).
   Solo frena una leccion que se pueda comprobar con un programa (ej.: "pytest dentro de pytest").
4. **Pruebas en paralelo + clasificador automatico** de por que fallo + tiempo limite (nunca mas 3 horas colgada) + reintento solo si es fallo tonto. Mientras corren, el equipo sigue con otras tareas.
5. **Armonia de leyes** segun B1-B3 (estados de la vigia: nacio roja -> verde -> aprobada -> guardada; copista = equipo; carpeta del ayudante con canal).
6. **El metodo de B5 como programa fijo** que une las piezas que ya existen; la IA solo llena los huecos que exigen escribir, y el programa rechaza lo que no venga del material.

### Anadido (lo que el resumen habia dejado fuera)
7. **Que el PC no se duerma mientras corren las pruebas** (ver A5). El programa del guardado le pide a Windows
   mantenerse despierto solo mientras corre, y lo suelta al terminar. No se toca la configuracion de energia de Julio.
8. **Preguntar en vez de asumir, por programa**: si falta un dato, el programa exige `PREGUNTA_REQUERIDA` o
   `NECESITO_LEER`; una respuesta que nombra algo que no esta en el material se rechaza sola (`NO_ENCONTRADO`).
9. **Cada papel del equipo con instrucciones fijas (skill)**: obrero, revisor, medidor, copista. Nadie hace "lo que le da la gana".
10. **Pasos c.3.1 a c.3.5 y c.4 del metodo, uno por uno en el programa**: legislar, candado, vigias + vigia de no romper,
    nace conectado, solo en los archivos exactos, y buscar la herramienta antes de crear.
11. **Registros limpios**: "lo que Julio ya dijo" y el candado de legislar no toman texto del sistema ni resumenes como
    ordenes, y existe el estado "espera aprobacion de Julio".
12. **Las otras 2 leyes que chocan** (forense parte 2, pares 1 y 4): "nunca codigo sin equipo" frente a "puede reparar";
    "nada de nombres de archivo" frente a "decir que archivo". Se armonizan por su intencion.
13. **Regla permanente**: toda mejora futura se pregunta primero "¿esto lo puede hacer un programa en vez de una IA?".

## A5. Por que un guardado tardo 47 minutos (medido en el registro de Windows)
- El PC **se durmio por inactividad** a las 12:42 y desperto a las 13:25 (43 min) con las pruebas a medio correr.
  Trabajo real: unos 4-5 min.
- Coinciden igual los otros guardados lentos: 12-sep 13:07 (48 min, durmio 45), 13-sep 22:39 (1h19, durmio 75),
  14-sep 08:33 (44 min, durmio 40).
- Los dos de 3 horas (13-sep 04:15 y 04:17) **no** coinciden con sueño: siguen siendo "guardia colgada" (forense). Sin explicar aun.
