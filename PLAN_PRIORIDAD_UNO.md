# PLAN UNICO — GENERADO POR PROGRAMA (2026-10-01). No se edita a mano.

> Fuente unica: `memoria/ORDENES.json` (ordenes y su campo `depende`) y `memoria/PLAN_DE_PASOS.json` (pasos).
> Una orden corre solo si las de su `depende` estan `hecha`; la prioridad es el orden de la lista.
> Lo anterior se aparto, sin borrar, en `memoria/planes_anulados/2026-10-01/` (con `INDICE.json`).

## 1. Hallazgos: fallo, causa raiz, reparacion raiz, donde, plan y paso

| # | Fallo | Evidencia medida | Causa raiz | Reparacion raiz | Donde | En que plan estaba | Ordenes | Paso | Que destraba | Meta |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Las vigias danan la memoria real | La corrida vacio memoria/INDICE_METODO.json (2035 lineas); 423 de 1678 lineas de BIGPICKLE.log las escribieron pruebas | Rutas de memoria fijas; el archivo de ajustes de las vigias no aisla toda la carpeta | Cada prueba usa una copia temporal de memoria y una vigia compara antes y despues | vigias/conftest.py; cuerpo/bigpickle.py (RUTA_LOG) | plan nuevo del 2026-10-01 (esta tabla) | N20 | 00 | toda medicion futura (309 vigias) | 0 archivos de memoria cambiados tras correr la bateria |
| 2 | El escritor no recibe el codigo que tiene que cambiar | Prueba sin IA: con el encargo original de H2 el paquete (23267 letras) no trae _preguntar_con_relevo ni el renglon a cambiar. En 58 ordenes abiertas: si el encargo nombra el archivo el paquete trae el codigo en 31 de 31; si no, en 1 de 3; 12 de 58 no lo nombran | El pit manda solo el texto del encargo y el buscador adivina por palabras; los campos pieza y repara de la orden nunca llegan; nadie comprueba antes de gastar | La guia lleva DONDE (archivo y funcion) tomado de la orden; el codigo llega completo por su propia via; prueba previa sin IA antes de gastar | capataz.lanzar_al_equipo; ingeniero.py equipo; obrero.trabajar; arnes/dos_vias.py y arnes/prueba_previa.py (nuevos) | plan nuevo del 2026-10-01 (esta tabla) / ley: CONTRATO_LAS_DOS_VIAS (1-oct, sin ninguna orden hasta hoy) | N28, N27 (la linea DONDE ya se aplica a las ordenes que no nombraban su archivo) | 0c | las respuestas NO_ENCONTRADO y NECESITO_LEER (43 de las 164 mal llamadas vacio) y las 12 ordenes sin archivo nombrado | el paquete trae el codigo en 100% de las ordenes; 0 llamadas gastadas sin el codigo |
| 3 | El pasillo recorta el codigo que si llego | Al tope del cerebro mas pequeno (8000 letras) se pierde codigo que si estaba en 27 de 34 ordenes comprobables; el prompt mediano mide 31989 letras y los 58 pasan de 8000 | _tope_pasillo = min(_capas) y el material engorda con la guia | Tope = el cerebro que mas aguanta; con las dos vias no hay nada que recortar | cuerpo/obrero.py, _preguntar_con_relevo | plan nuevo del 2026-10-01 (esta tabla) / ley: CONTRATO_LAS_DOS_VIAS; CONTRATO_EL_PASILLO_SE_REPARTA_POR_CAPACIDAD | H2, N27 | 0a | 27 ordenes | 0 ordenes con codigo perdido por recorte |
| 4 | El revisor marca como invento lo que la reparacion crea | 25 de 51 fallos no_aprobo | La IA revisora marca nombres nuevos y nada los contrasta por programa | Un programa comprueba si el nombre esta declarado en el propio codigo que la propuesta trae | cuerpo/obrero.py (revision del auditor) | PLAN_PRIORIDAD_UNO.md | R9 | 0b | toda orden que crea un nombre nuevo (casi todas las piezas nuevas del plan) | 0 rechazos por invento falso |
| 5 | Una falla aislada detenia todo el trabajo | Con la cadena en fila una falla bloqueaba 173 de 173 ordenes; con dependencias reales bloquea como maximo 5 de 190 | Dependencias en fila y el bucle termina por 3 fallos iguales o por NADA SE PUEDE CORRER | Solo dependencias reales; el bucle aparta la que falla y sigue | memoria/ORDENES.json (campo depende); capataz.bucle | plan nuevo del 2026-10-01 (esta tabla) | N18 + grafo | 0 | todas las ordenes del plan | el bucle solo termina si no queda nada corrible |
| 6 | No hay multitarea (ley de maxima prioridad del 28-sep sin cumplir) | El comando pit llama a bucle(proyecto) con en_paralelo=1; la vigia 'la cadena trabaja en varias a la vez' esta roja y sin dueno; la copia por orden, los turnos del guardado y el bucle con hilos ya existen | El parametro no se expone, la vigia vieja exige de una en una y R6 estaba en el ultimo paso | Reescribir la vigia vieja con su razon, ley de copias temporales, y R6a/R6 | capataz.bucle; ingeniero.py (comando pit); vigias/test_vigia_el_pit_corre_una_tarea_a_la_vez.py | PLAN_PRIORIDAD_UNO.md / ley: CONTRATO_LA_MULTITAREA_ES_LA_FORMA_DE_TRABAJAR (28-sep, maxima prioridad) | L4, N29, R6a, R6 | 0d | todas las ordenes del plan (hoy se corre 1 a la vez) | 3 o mas ordenes a la vez |
| 7 | Se gasta el saldo de Claude | Solo el perito ejecuta a Claude: 3 intentos de 600 s tras cada orden fallida. Big Pickle gratis desde el 28-sep: mediana 56 s, p95 186 s, maximo 333 s en 239 llamadas buenas | El perito es Claude y no tiene un tiempo medido | Perito = IA gratis; un intento con el tiempo medido del historial (techo 400 s, decision de Julio) | capataz.pedir_al_perito | PLAN_PRIORIDAD_UNO.md, continuacion_2026-09-13.md | N17, N15, 50, 51 | 0e | el forense de las 31 ordenes fallidas | 0 llamadas a Claude; el perito nunca cuelga el bucle |
| 8 | El bucle se detiene por tope en dolares | TOPE_MES_USD y se_paso_del_tope dentro del bucle | Tope en dolares dentro del bucle | Solo se detiene si DeepSeek se queda sin saldo (decision de Julio del 27-sep) | capataz.bucle | PLAN_PRIORIDAD_UNO.md, 02_FORENSE.md | 89, 68 | 0f | todas | 0 paradas por dolares |
| 9 | El guardado pierde trabajo aprobado | 82 veces (FALLOS id 69); la vigia de R1 esta roja; 23 de 93 expedientes son 'guardia' | _vecinas_por_stem devuelve None (corre las 245 vigias) con tope fijo de 900 s | Nunca None; tope medido; si se agota se aparta con motivo | arnes/vecinas.py; arnes/guardia_de_guardado.py | PLAN_PRIORIDAD_UNO.md, PLAN_DE_RAIZ_2026-09-13.md | R1 | 1 | 23 fallos de guardado y los 14 trabajos frenados | 0 trabajos aprobados sin llegar al disco |
| 10 | Una orden fallida no vuelve tras su arreglo | El forense creo R1-F151051 y R1 siguio fallida | El forense no enlaza el arreglo con la orden que fallo | El arreglo pasa a la lista depende de la fallida | capataz.forense | plan nuevo del 2026-10-01 (esta tabla) | N14 | 1b | la cadena de cada orden fallida | 0 fallidas esperando un arreglo ya hecho |
| 11 | La legislacion recoge basura | 126 apuntes pendientes, casi todos pegados de PowerShell | El candado de legislar apunta cada linea y cada cita | Un mensaje es una instruccion; las palabras de maquina no entran | arnes/candado_legislar.py | PLAN_PRIORIDAD_UNO.md, 01_ACUERDOS.md | R10, 30, 31 | 3 | el cierre y la lista de pendientes | 0 apuntes falsos |
| 12 | Recoger pisa trabajo mas nuevo; hay 14 trabajos frenados | Las vigias de 37 y 113 estan rojas | Recoger no compara el contenido | Comparar contenido y no pisar; despues recoger los 14 | arnes/recoger_los_pedazos.py | PLAN_PRIORIDAD_UNO.md, PLAN_DOS_PASOS.md | 37, 113 | 4 | los 14 trabajos ya pagados | 0 trabajos pisados |
| 13 | El mando muere al imprimir y pierde el trabajo pagado | Vigia escrita el 25-ago, roja, sin orden | Guarda despues de imprimir y la consola cp1252 no dibuja algunos caracteres | Guardar antes de imprimir y mostrar con reemplazo | ingeniero.py (comando equipo) | plan nuevo del 2026-10-01 (esta tabla) | N26 | 4 | el trabajo pagado de cada ronda | 0 trabajos perdidos por imprimir |
| 14 | El revisor de programa corta rondas buenas | 17 de 51 fallos no_aprobo; la vigia de R24 esta roja | Un aviso sale como freno y hay reglas que se pisan | El aviso no frena; arreglar los casos medidos | arnes/revisor_de_programa.py | PLAN_PRIORIDAD_UNO.md, 08_FICHA_DEL_PIT.md | R24, 95-F011402, 41, 43, 45 | 5 | 17 fallos | 0 rondas buenas frenadas |
| 15 | Solo un cambio por ronda y no se puede crear sobre un archivo existente | El obrero ofrece 'cambios' solo para el mismo archivo; no_aplico 10 de 93 expedientes | El prompt y el aplicador no admiten varios archivos ni crear sobre uno existente | Varios cambios por ronda en varias funciones y archivos | cuerpo/obrero.py (prompt); cuerpo/aplicador.py | PLAN_PRIORIDAD_UNO.md | 95-F222455, 173-F064924, 46-F061935, 112-F061113 | 6 | toda orden que toca mas de una funcion o archivo | 0 rondas rechazadas por mas de un cambio |
| 16 | El material no llega completo (archivo pequeno, NECESITO_LEER, paquete compacto) | 17 de 79 fallos apuntados son de material; 14 respuestas NO_ENCONTRADO y 29 NECESITO_LEER | El repartidor corta en trozos por parecido de palabras y no atiende lo que la IA pide | Entregar enteros los archivos cortos y atender lo que la IA pide | cerebro/router.py | PLAN_PRIORIDAD_UNO.md, 08_FICHA_DEL_PIT.md | 29, 29-F005530, H3, R22 | 7 | 43 respuestas que piden material | 0 NECESITO_LEER sin atender |
| 17 | Hay vigias que no miden | 9 vigias verdes con pruebas sin assert o que devuelven True/False; sabotaje fallo en 10 de 31 ordenes fallidas | Nacen verdes y nada comprueba que nacieron rojas por su motivo | Sabotaje obligatorio y revisor por programa | arnes/sabotaje.py; capataz.comprobar_pasos | PLAN_PRIORIDAD_UNO.md, 02_FORENSE.md | 63, 64, 38, 39, 24, 25, 32, 33 | 8 | sellar con confianza todo lo demas | 0 vigias verdes que no miden |
| 18 | 'Vacio' no es vacio y nadie lee el cuaderno | 164 de 165 'vacias' eran propuestas incompletas (92 solo diagnostico, 29 otra forma de JSON, 29 texto, 14 NO_ENCONTRADO); Claude y Codex no apuntan; 17,8% de filas sin segundos; solo 1000 filas; sin costo | El codigo marca vacio cuando la propuesta no cumple y no dice que falto; nadie lo lee | Apuntar causa y tamano del pedido; resumen diario que el bucle muestra al arrancar y al parar; el motivo del fallo entra por la guia de la siguiente ronda | cuerpo/obrero.py (trabajar); cuerpo/cuaderno.py; arnes/resumen_del_cuaderno.py | plan nuevo del 2026-10-01 (esta tabla) | N19, N03 | 9 | diagnosticar cualquier fallo con datos | 0 'vacio' falsos; la causa en el 100% de los fallos |
| 19 | El forense casi nunca produce una orden | 9 de 93 expedientes; el juez rechazo 28; el perito no contesto 28; 39 sin analizar | El juez es una IA que no ve el codigo y el perito es Claude | El juez es un programa que ve el codigo; perito gratis | capataz.juzgar_citas | plan nuevo del 2026-10-01 (esta tabla) | N21, N17 | 9 | que cada fallo genere su arreglo | >80% de expedientes con orden nueva |
| 20 | Vigias rojas sin dueno | 38 de 56 vigias no verdes no tienen orden; 19 son comportamiento roto de verdad | Nada convierte una vigia roja en orden | Lector de vigias rojas que crea la orden con las 4 preguntas llenas | arnes/lector_de_rojas.py (nuevo); ingeniero.py vigias; guardia_de_guardado | plan nuevo del 2026-10-01 (esta tabla) | N04 | 9 | 19 reparaciones | 0 vigias rojas sin orden |
| 21 | Todo debe nacer conectado y hay piezas dormidas | 11 piezas dormidas; el contador de huerfanas y el paso 'pieza suelta' del pit dan por conectada a una pieza que solo nombra una vigia; 3 candados dormidos | Basta que cualquier archivo, incluso una vigia, nombre la pieza | Una pieza cuenta como conectada solo si la llama codigo real o esta en los ganchos; el pit no sella una pieza nueva sin llamador | skills/nace_conectada.py; capataz.comprobar_pasos | plan nuevo del 2026-10-01 (esta tabla) / ley: CONTRATO_TODO_ENCHUFADO_NADA_DORMIDO | N06, N06b | 9 | 11 piezas dormidas | 0 piezas huerfanas; cada orden nueva trae su conexion |
| 22 | Ordenes incompletas | 9 ordenes sin campo vigia y 40 con una vigia prometida y sin escribir (de 91 abiertas) | La puerta de las 4 respuestas solo se aplica al cerrar | Rechazar lo incompleto al crear, con DONDE, POR QUE, COMO y resultado esperado | arnes/puerta_del_plan.py; cuerpo/director.py | plan nuevo del 2026-10-01 (esta tabla) | N02, N01 | 9 | 40 ordenes que no se pueden cerrar | 0 ordenes incompletas |
| 23 | La memoria no se actualiza al sellar | Lecciones dormidas; el paquete no las trae; nada deja el estado al dia | No hay programa de sellado ni hora de apuntes | Sellado que actualiza solo; hora de apuntes; linea base antes y despues | arnes/al_sellar.py, cuerpo/hora_de_apuntes.py, arnes/linea_base.py (nuevos) | plan nuevo del 2026-10-01 (esta tabla) | N05, N09, N12 | 9 | aprender de cada fallo | memoria al dia tras cada sello |
| 24 | Demasiados planes y versiones | 47 documentos de plan o estado, 105 copias, 5 duplicadas exactas, 8 hijas del forense, 1223 trabajos guardados (113 versiones de obrero.py) | Cada ronda guarda una version nueva y nada exige un solo plan | Un solo plan generado por programa; lo viejo se aparta sin borrar; vigia del plan unico | PLAN_PRIORIDAD_UNO.md; arnes/un_solo_plan.py (nuevo) | plan nuevo del 2026-10-01 (esta tabla) | N25 | 9 | saber que plan manda | 1 plan; 0 ordenes duplicadas |
| 25 | La espera maxima de 400 s no esta en ninguna orden | Escrito como FALTA en el plan anterior | R3 solo habla de preguntar a la vez | Big Pickle 400 s y sus dos vigias | cuerpo/bigpickle.py | plan nuevo del 2026-10-01 (esta tabla) | N22 | 10 | esperas largas | espera maxima 400 s |
| 26 | Falta la medida unica: Julio pudo hacer su informe hoy | Marcada como lo mas importante y nunca convertida en orden | No hay prueba real automatica | Prueba real con navegador automatico | arnes/prueba_real_del_informe.py (nuevo) | plan nuevo del 2026-10-01 (esta tabla) | N23 | 12b | saber si de verdad sirve | si/no diario |

## 2. Flujo de trabajo medido, etapa por etapa

| Etapa | Quien o que pieza | Numero medido | Orden que lo repara |
|---|---|---|---|
| E0 Entender lo que Julio quiere | ninguno | NO MEDIDO: no existe la pieza | N07 |
| E1 La orden esta completa (4 preguntas y vigia) | puerta del plan solo al cerrar | 9 ordenes sin campo vigia y 40 con vigia sin escribir, de 91 abiertas | N02, N01 |
| E2 Prueba previa: llega el codigo (sin gastar) | no existe | 12 de 58 ordenes no nombran su archivo; con archivo nombrado llega el codigo en 31/31, sin nombrarlo 1/3 | N28 |
| E3 Codigo limpio y guia aparte | no existe (ley del 1-oct sin orden) | NO MEDIDO | N27 |
| E4 Recorte del pasillo | obrero._preguntar_con_relevo | quita codigo que si llego en 27 de 34 ordenes | H2 |
| E5 El escritor responde | DeepSeek, Groq, Gemini | DeepSeek: 467 de 595 llamadas sirvieron (78,5%), mediana 5,2 s; 164 de 1000 filas mal llamadas vacio | N19 |
| E6 Revisor por programa | arnes/revisor_de_programa.py | frena en 17 de 51 no_aprobo | R24, 95-F011402, 41, 43, 45 |
| E7 Auditor IA | Big Pickle | rechazo en 22 y marca invento en 25 de 51 no_aprobo | R9 |
| E8 Aplicador | cuerpo/aplicador.py | no_aplico 10 de 93 fallos | 95-F222455 y las de su grupo |
| E9 Guardado y bateria | arnes/guardia_de_guardado.py | guardia 23 de 93 fallos; 82 veces no dejo guardar | R1 |
| E10 Vigia y sabotaje | capataz.comprobar_pasos | sabotaje fallo en 10 de 31 ordenes fallidas | 63, 64, 38, 39, 24, 25, 32, 33 |
| E11 Sellado y memoria | no existe | NO MEDIDO | N05, N12 |
| E12 Aprender del fallo | forense | 9 de 93 expedientes produjeron una orden | N21, N04, N09 |

## 3. Las cuatro medidas (rapido, preciso, eficiente, economico): hoy y meta

| Termino | Medida | Hoy | Meta | Quien la mueve |
|---|---|---|---|---|
| RAPIDO | Minutos por orden | 90,1 (plan del 25-sep, cuaderno) | menos de 20 | N12 la mide en cada orden |
| RAPIDO | Ordenes a la vez | 1 | 3 o mas | L4, N29, R6a, R6 |
| PRECISO | Rondas aprobadas en la primera | 3 de 13 el 1-oct (CONTRATO_LAS_DOS_VIAS) | 80% o mas | N27, N28 |
| PRECISO | Llamadas que no sirvieron | 18,8% (cuaderno) | menos de 5% | N19 |
| PRECISO | Ordenes cuyo codigo llega al escritor | 32 de 34 comprobables; 12 de 58 sin archivo nombrado | 100% | N28, N27 |
| EFICIENTE | Llamadas a IA por orden | 4,78 (plan del 25-sep) | menos de 2,5 | N28, N27, N19 |
| EFICIENTE | Trabajo aprobado que no llega al disco | 82 veces | 0 | R1 |
| ECONOMICO | Llamadas a Claude | una por cada fallo (perito) | 0 | N17, N15 |
| ECONOMICO | Llamadas gastadas sin el codigo | no medido (12 de 58 ordenes en riesgo) | 0 | N28 |
| ECONOMICO | Costo por orden aprobada | NO MEDIDO: el cuaderno no guarda costo | medido en cada orden | N03, N12 |

## 4. Como se decide cada reparacion (qué, donde, por que, cuando, como)

Cada orden lleva en su encargo QUE SE REPARA, COMO, DONDE y POR QUE; el CUANDO es su paso y su campo `depende`.

## 5. Pasos y ordenes

### Paso 00 Medir sin danar la memoria real
- `N20-ninguna_vigia_toca_la_memoria_real` [pendiente] Las vigias no tocan el estado real: La guardia de la memoria real
- `V-N20-las_pruebas_apuntan_a_un_registro_temporal` [pendiente] Vigia primero: Cada prueba usa su propio registro
- `N20-las_pruebas_apuntan_a_un_registro_temporal` [pendiente] Las vigias no tocan el estado real: Cada prueba usa su propio registro

### Paso 0 El bucle no se detiene por un fallo aislado
- `V-N18-el_bucle_no_se_detiene_por_fallos` [pendiente] Vigia primero: El bucle aparta la que falla y sigue
- `N18-el_bucle_no_se_detiene_por_fallos` [pendiente] El bucle nunca se detiene por una orden que falla: El bucle aparta la que falla y sigue

### Paso 0a El pasillo no recorta al que escribe
- `H2-el-pasillo-no-corta-a-la-medida-del-mas-chico` [pendiente] El material se corta a la medida del que va a escribir, no del cerebro mas pequeno

### Paso 0b Crear no es inventar
- `R9` [pendiente] Crear no es inventar: que lo compruebe un programa

### Paso 0c Que el trabajo llegue al escritor: prueba previa y dos vias
- `V-N28-prueba_previa` [pendiente] Vigia primero: El programa de la prueba previa
- `N28-prueba_previa` [pendiente] Prueba previa sin IA: antes de gastar, se comprueba que el codigo llega: El programa de la — depende de: V-N28-prueba_previa
- `V-N28-el_bucle_hace_la_prueba_previa` [pendiente] Vigia primero: El bucle la hace antes de gastar
- `N28-el_bucle_hace_la_prueba_previa` [pendiente] Prueba previa sin IA: antes de gastar, se comprueba que el codigo llega: El bucle la hace  — depende de: V-N28-el_bucle_hace_la_prueba_previa
- `V-N27-las_dos_vias` [pendiente] Vigia primero: El programa de las dos vias
- `N27-las_dos_vias` [pendiente] Las dos vias por programa: el codigo viaja limpio y la guia va aparte: El programa de las  — depende de: V-N27-las_dos_vias
- `V-N27-el_pit_arma_las_dos_vias` [pendiente] Vigia primero: El pit arma las dos vias
- `N27-el_pit_arma_las_dos_vias` [pendiente] Las dos vias por programa: el codigo viaja limpio y la guia va aparte: El pit arma las dos — depende de: V-N27-el_pit_arma_las_dos_vias
- `V-N27-el_mando_equipo_recibe_las_dos_vias` [pendiente] Vigia primero: El comando equipo recibe las dos vias
- `N27-el_mando_equipo_recibe_las_dos_vias` [pendiente] Las dos vias por programa: el codigo viaja limpio y la guia va aparte: El comando equipo r — depende de: V-N27-el_mando_equipo_recibe_las_dos_vias
- `V-N27-el_obrero_usa_la_via_del_codigo` [pendiente] Vigia primero: El obrero usa la via del codigo y el candado frena la mezcla
- `N27-el_obrero_usa_la_via_del_codigo` [pendiente] Las dos vias por programa: el codigo viaja limpio y la guia va aparte: El obrero usa la vi — depende de: V-N27-el_obrero_usa_la_via_del_codigo

### Paso 0d Multitarea: varias ordenes a la vez
- `V-L4-copias-temporales-por-orden` [pendiente] Vigia primero: Ley: cada orden trabaja en su copia temporal (excepcion a una sola via)
- `L4-copias-temporales-por-orden` [pendiente] Ley: cada orden trabaja en su copia temporal (excepcion a una sola via) — depende de: V-L4-copias-temporales-por-orden
- `N29-la_vigia_vieja_deja_correr_varias` [pendiente] Multitarea: la vigia vieja deja de exigir de una en una: La vigia vieja admite varias a la
- `R6a` [pendiente] El pit corre dos piezas distintas a la vez (la prueba que lo exige ya existe y esta roja)
- `R6` [pendiente] Varias ordenes a la vez, cada una en su copia

### Paso 0e El perito es gratis y no cuelga el bucle
- `V-N17-el_perito_es_gratis` [pendiente] Vigia primero: El perito es una IA gratis
- `N17-el_perito_es_gratis` [pendiente] El perito es gratis: Claude no es el perito por defecto: El perito es una IA gratis — depende de: V-N17-el_perito_es_gratis
- `V-N15-el_perito_tiene_tope_corto` [pendiente] Vigia primero: El perito tiene un tope corto y no reintenta en cadena
- `N15-el_perito_tiene_tope_corto` [pendiente] El perito no cuelga el bucle: El perito tiene un tope corto y no reintenta en cadena — depende de: V-N15-el_perito_tiene_tope_corto
- `50` [pendiente] La vigia de que si el perito no contesta, entra Codex
- `51` [pendiente] Si el perito no contesta, entra Codex — depende de: 50

### Paso 0f El bucle no para por dolares (decision de Julio del 2026-09-27)
- `89` [pendiente] La vigia vieja del loop sigue la orden nueva de Julio: sin tope en dolares
- `68` [pendiente] El loop no para por dolares: para cuando DeepSeek se queda sin saldo — depende de: 89

### Paso 1 El guardado: lo aprobado llega al disco
- `R1` [pendiente] El trabajo aprobado siempre llega al disco

### Paso 1b Una orden que fallo vuelve sola tras su arreglo
- `V-N14-la_fallida_depende_de_su_arreglo` [pendiente] Vigia primero: El forense enlaza la orden con su arreglo
- `N14-la_fallida_depende_de_su_arreglo` [pendiente] La orden que fallo espera a su arreglo y vuelve sola: El forense enlaza la orden con su ar — depende de: V-N14-la_fallida_depende_de_su_arreglo

### Paso 2 Las leyes nuevas (solo documentos)
- `V-L1-el-orden-de-los-pasos-lo-impone-el-programa` [pendiente] Vigia primero: Ley: el orden de los pasos lo impone el programa
- `L1-el-orden-de-los-pasos-lo-impone-el-programa` [pendiente] Ley: el orden de los pasos lo impone el programa — depende de: V-L1-el-orden-de-los-pasos-lo-impone-el-programa
- `V-L2-el-ingeniero-entiende-lo-que-julio-quiere` [pendiente] Vigia primero: Ley: el ingeniero entiende lo que Julio quiere y se repara solo
- `L2-el-ingeniero-entiende-lo-que-julio-quiere` [pendiente] Ley: el ingeniero entiende lo que Julio quiere y se repara solo — depende de: V-L2-el-ingeniero-entiende-lo-que-julio-quiere
- `V-L3-todas-las-ia-trabajan-por-el-canal` [pendiente] Vigia primero: Ley: todas las IA trabajan por el canal
- `L3-todas-las-ia-trabajan-por-el-canal` [pendiente] Ley: todas las IA trabajan por el canal — depende de: V-L3-todas-las-ia-trabajan-por-el-canal

### Paso 3 La legislacion deja de ensuciarse
- `V-R10` [pendiente] Vigia primero: Un mensaje de Julio es UNA instruccion, no veinte
- `R10` [pendiente] Un mensaje de Julio es UNA instruccion, no veinte — depende de: V-R10
- `30` [pendiente] La vigia de que las palabras de maquina no entran como orden de Julio
- `31` [pendiente] Las palabras de maquina no entran como orden de Julio

### Paso 4 Recoger no destruye y el mando no pierde lo pagado
- `37` [pendiente] Recoger los pedazos no pisa trabajo mas nuevo
- `113` [pendiente] Recoger aparta un archivo nuevo rojo en vez de dejarlo suelto
- `N26-el_mando_no_muere_por_un_caracter` [pendiente] El mando no muere por un caracter y no pierde el trabajo pagado: Guardar antes de imprimir

### Paso 5 El revisor no corta rondas buenas
- `R24-el-aviso-no-frena-la-ronda` [pendiente] El mensaje que adivina la intencion avisa, y deja de cortar rondas buenas
- `V-95-F011402` [pendiente] Vigia primero: 95-F011402
- `95-F011402` [pendiente]  — depende de: V-95-F011402
- `41` [pendiente] No se aparta lo que un archivo importa por dentro
- `43` [pendiente] Una prueba nueva no deja ciega a toda la bateria
- `45` [pendiente] Una prueba no puede devolver en vez de afirmar

### Paso 6 Varios cambios por ronda
- `V-95-F222455` [pendiente] Vigia primero: 95-F222455
- `95-F222455` [pendiente]  — depende de: V-95-F222455
- `V-173-F064924` [pendiente] Vigia primero: 173-F064924
- `173-F064924` [pendiente]  — depende de: V-173-F064924
- `V-46-F061935` [pendiente] Vigia primero: 46-F061935
- `46-F061935` [pendiente]  — depende de: V-46-F061935
- `V-112-F061113` [pendiente] Vigia primero: 112-F061113
- `112-F061113` [pendiente]  — depende de: V-112-F061113

### Paso 7 El material llega a la medida
- `29` [pendiente] Un archivo pequeno se entrega entero — depende de: 29-F005530
- `V-29-F005530` [pendiente] Vigia primero: 29-F005530
- `29-F005530` [pendiente]  — depende de: V-29-F005530
- `V-H3-el-empaquetador-respeta-necesito-leer` [pendiente] Vigia primero: Cuando se pide un trozo con NECESITO_LEER, el paquete lo entrega
- `H3-el-empaquetador-respeta-necesito-leer` [pendiente] Cuando se pide un trozo con NECESITO_LEER, el paquete lo entrega — depende de: V-H3-el-empaquetador-respeta-necesito-leer
- `V-R22-paquete-compacto-sin-ruido` [pendiente] Vigia primero: El paquete y la respuesta viajan compactos y sin ruido
- `R22-paquete-compacto-sin-ruido` [pendiente] El paquete y la respuesta viajan compactos y sin ruido — depende de: V-R22-paquete-compacto-sin-ruido

### Paso 8 Las pruebas miden de verdad
- `63` [pendiente] La vigia de que el sabotaje no acepta un texto repetido
- `64` [pendiente] El sabotaje no acepta un texto repetido — depende de: 63
- `38` [pendiente] La vigia de que una prueba que revienta no cuenta como nacida roja
- `24` [pendiente] La vigia de que el pit comprueba solo que la prueba nace roja
- `25` [pendiente] El pit comprueba solo que la prueba nace roja — depende de: 24
- `32` [pendiente] La vigia de que una pieza que no existe se manda como creacion
- `33` [pendiente] Una pieza que no existe se manda como creacion — depende de: 32

### Paso 9 El Ingeniero se repara solo
- `N25-vigia_hay_un_solo_plan` [pendiente] Un solo plan, una reparacion una orden: La guardia del plan unico
- `V-N25-un_solo_plan` [pendiente] Vigia primero: El programa del plan unico
- `N25-un_solo_plan` [pendiente] Un solo plan, una reparacion una orden: El programa del plan unico — depende de: V-N25-un_solo_plan
- `V-N25-el_arranque_vigila_el_plan_unico` [pendiente] Vigia primero: El arranque comprueba el plan unico
- `N25-el_arranque_vigila_el_plan_unico` [pendiente] Un solo plan, una reparacion una orden: El arranque comprueba el plan unico — depende de: V-N25-el_arranque_vigila_el_plan_unico
- `V-N19-el_cuaderno_dice_la_causa` [pendiente] Vigia primero: Una propuesta incompleta se apunta con su causa
- `N19-el_cuaderno_dice_la_causa` [pendiente] El cuaderno dice por que una respuesta no sirvio: Una propuesta incompleta se apunta con s — depende de: V-N19-el_cuaderno_dice_la_causa
- `V-N19-el_resumen_diario_del_cuaderno` [pendiente] Vigia primero: El resumen diario de causas
- `N19-el_resumen_diario_del_cuaderno` [pendiente] El cuaderno dice por que una respuesta no sirvio: El resumen diario de causas — depende de: V-N19-el_resumen_diario_del_cuaderno
- `V-N21-el_juez_del_forense_ve_el_codigo` [pendiente] Vigia primero: El juez del forense es un programa que ve el codigo
- `N21-el_juez_del_forense_ve_el_codigo` [pendiente] El forense no juzga lo que no ve: El juez del forense es un programa que ve el codigo — depende de: V-N21-el_juez_del_forense_ve_el_codigo
- `V-N01-camino_sano` [pendiente] Vigia primero: El programa que revisa el camino
- `N01-camino_sano` [pendiente] El camino del plan no se trunca: El programa que revisa el camino — depende de: V-N01-camino_sano
- `V-N01-el_bucle_llama_al_camino_sano` [pendiente] Vigia primero: El bucle lo llama
- `N01-el_bucle_llama_al_camino_sano` [pendiente] El camino del plan no se trunca: El bucle lo llama — depende de: V-N01-el_bucle_llama_al_camino_sano
- `V-N02-la_orden_completa` [pendiente] Vigia primero: La funcion que dice si una orden esta completa
- `N02-la_orden_completa` [pendiente] Ninguna orden nace incompleta: La funcion que dice si una orden esta completa — depende de: V-N02-la_orden_completa
- `V-N02-orden_nueva_rechaza_lo_incompleto` [pendiente] Vigia primero: Crear una orden pasa por la puerta
- `N02-orden_nueva_rechaza_lo_incompleto` [pendiente] Ninguna orden nace incompleta: Crear una orden pasa por la puerta — depende de: V-N02-orden_nueva_rechaza_lo_incompleto
- `V-N03-el_cuaderno_completo` [pendiente] Vigia primero: El cuaderno guarda todo, por dia
- `N03-el_cuaderno_completo` [pendiente] El cuaderno apunta a todas las IA: El cuaderno guarda todo, por dia — depende de: V-N03-el_cuaderno_completo
- `N03-toda_llamada_a_una_ia_apunta` [pendiente] El cuaderno apunta a todas las IA: La guardia de las llamadas
- `V-N03-codex_apunta_en_el_cuaderno` [pendiente] Vigia primero: Codex apunta
- `N03-codex_apunta_en_el_cuaderno` [pendiente] El cuaderno apunta a todas las IA: Codex apunta — depende de: V-N03-codex_apunta_en_el_cuaderno
- `V-N03-el_perito_apunta_en_el_cuaderno` [pendiente] Vigia primero: El perito apunta
- `N03-el_perito_apunta_en_el_cuaderno` [pendiente] El cuaderno apunta a todas las IA: El perito apunta — depende de: V-N03-el_perito_apunta_en_el_cuaderno
- `V-N03-el_buscador_de_significados_apunta` [pendiente] Vigia primero: El buscador de significados apunta
- `N03-el_buscador_de_significados_apunta` [pendiente] El cuaderno apunta a todas las IA: El buscador de significados apunta — depende de: V-N03-el_buscador_de_significados_apunta
- `V-N04-el_lector_de_vigias_rojas` [pendiente] Vigia primero: El lector de vigias rojas
- `N04-el_lector_de_vigias_rojas` [pendiente] Cada vigia roja dice por que y alguien la atiende: El lector de vigias rojas — depende de: V-N04-el_lector_de_vigias_rojas
- `V-N04-el_comando_vigias_dice_por_que` [pendiente] Vigia primero: El comando de vigias dice por que
- `N04-el_comando_vigias_dice_por_que` [pendiente] Cada vigia roja dice por que y alguien la atiende: El comando de vigias dice por que — depende de: V-N04-el_comando_vigias_dice_por_que
- `V-N04-el_guardado_llama_al_lector` [pendiente] Vigia primero: El guardado llama al lector
- `N04-el_guardado_llama_al_lector` [pendiente] Cada vigia roja dice por que y alguien la atiende: El guardado llama al lector — depende de: V-N04-el_guardado_llama_al_lector
- `V-N04-el_bucle_llama_al_lector` [pendiente] Vigia primero: El bucle llama al lector
- `N04-el_bucle_llama_al_lector` [pendiente] Cada vigia roja dice por que y alguien la atiende: El bucle llama al lector — depende de: V-N04-el_bucle_llama_al_lector
- `V-N06-un_candado_no_conectado_es_huerfano` [pendiente] Vigia primero: Se aprieta el contador de huerfanas
- `N06-un_candado_no_conectado_es_huerfano` [pendiente] Nace conectada de verdad: Se aprieta el contador de huerfanas — depende de: V-N06-un_candado_no_conectado_es_huerfano
- `V-N06-el_pit_no_cuenta_a_las_vigias_como_llamador` [pendiente] Vigia primero: El pit no da por conectada a una pieza que solo nombra una vigia
- `N06-el_pit_no_cuenta_a_las_vigias_como_llamador` [pendiente] Nace conectada de verdad: El pit no da por conectada a una pieza que solo nombra una vigia — depende de: V-N06-el_pit_no_cuenta_a_las_vigias_como_llamador
- `V-N06b-el_candado_de_la_puerta_trasera_conectado` [pendiente] Vigia primero: Se conecta el candado existente
- `N06b-el_candado_de_la_puerta_trasera_conectado` [pendiente] Se conecta el candado de la puerta trasera: Se conecta el candado existente — depende de: V-N06b-el_candado_de_la_puerta_trasera_conectado
- `V-N05-al_sellar_la_memoria_se_actualiza` [pendiente] Vigia primero: El programa que actualiza la memoria
- `N05-al_sellar_la_memoria_se_actualiza` [pendiente] Al sellar, la memoria se actualiza sola: El programa que actualiza la memoria — depende de: V-N05-al_sellar_la_memoria_se_actualiza
- `V-N05-el_bucle_llama_a_sellar` [pendiente] Vigia primero: El bucle la llama al marcar hecha
- `N05-el_bucle_llama_a_sellar` [pendiente] Al sellar, la memoria se actualiza sola: El bucle la llama al marcar hecha — depende de: V-N05-el_bucle_llama_a_sellar
- `V-N09-la_hora_de_apuntes` [pendiente] Vigia primero: El programa de la hora de apuntes
- `N09-la_hora_de_apuntes` [pendiente] La hora de apuntes: El programa de la hora de apuntes — depende de: V-N09-la_hora_de_apuntes
- `V-N09-el_paquete_trae_las_lecciones` [pendiente] Vigia primero: El paquete trae las lecciones
- `N09-el_paquete_trae_las_lecciones` [pendiente] La hora de apuntes: El paquete trae las lecciones — depende de: V-N09-el_paquete_trae_las_lecciones
- `V-N09-el_bucle_corre_la_hora_de_apuntes` [pendiente] Vigia primero: El bucle la corre al parar
- `N09-el_bucle_corre_la_hora_de_apuntes` [pendiente] La hora de apuntes: El bucle la corre al parar — depende de: V-N09-el_bucle_corre_la_hora_de_apuntes
- `V-N12-la_linea_base` [pendiente] Vigia primero: El programa de la linea base
- `N12-la_linea_base` [pendiente] Linea base, regresion y marcha atras: El programa de la linea base — depende de: V-N12-la_linea_base
- `V-N12-el_bucle_mide_antes_y_despues` [pendiente] Vigia primero: El bucle mide antes y despues
- `N12-el_bucle_mide_antes_y_despues` [pendiente] Linea base, regresion y marcha atras: El bucle mide antes y despues — depende de: V-N12-el_bucle_mide_antes_y_despues
- `V-N07-el_traductor_de_deseo` [pendiente] Vigia primero: El traductor de deseo
- `N07-el_traductor_de_deseo` [pendiente] El Ingeniero traduce lo que Julio quiere: El traductor de deseo — depende de: V-N07-el_traductor_de_deseo
- `V-N07-el_comando_entiende` [pendiente] Vigia primero: El comando entiende
- `N07-el_comando_entiende` [pendiente] El Ingeniero traduce lo que Julio quiere: El comando entiende — depende de: V-N07-el_comando_entiende
- `V-N08-el_verificador_de_resultado` [pendiente] Vigia primero: El verificador de resultado
- `N08-el_verificador_de_resultado` [pendiente] Se sella solo si coincide con lo esperado: El verificador de resultado — depende de: V-N08-el_verificador_de_resultado
- `V-N08-el_bucle_verifica_antes_de_sellar` [pendiente] Vigia primero: El bucle verifica antes de sellar
- `N08-el_bucle_verifica_antes_de_sellar` [pendiente] Se sella solo si coincide con lo esperado: El bucle verifica antes de sellar — depende de: V-N08-el_bucle_verifica_antes_de_sellar
- `V-N10-el_canal_conoce_a_todas_las_ia` [pendiente] Vigia primero: El canal conoce a todas las IA
- `N10-el_canal_conoce_a_todas_las_ia` [pendiente] Codex, Big Pickle y Grok 4.7 trabajan por el canal: El canal conoce a todas las IA — depende de: V-N10-el_canal_conoce_a_todas_las_ia
- `V-N10-el_capataz_elige_quien_escribe_y_revisa` [pendiente] Vigia primero: Cada orden elige su equipo
- `N10-el_capataz_elige_quien_escribe_y_revisa` [pendiente] Codex, Big Pickle y Grok 4.7 trabajan por el canal: Cada orden elige su equipo — depende de: V-N10-el_capataz_elige_quien_escribe_y_revisa
- `V-N10-el_reparto_asigna_a_las_nuevas_ia` [pendiente] Vigia primero: El reparto las asigna
- `N10-el_reparto_asigna_a_las_nuevas_ia` [pendiente] Codex, Big Pickle y Grok 4.7 trabajan por el canal: El reparto las asigna — depende de: V-N10-el_reparto_asigna_a_las_nuevas_ia
- `V-N11-programa_antes_que_ia` [pendiente] Vigia primero: El que decide si basta un programa
- `N11-programa_antes_que_ia` [pendiente] Programa antes que IA, por regla: El que decide si basta un programa
- `V-N11-modo_ia_exige_por_que` [pendiente] Vigia primero: Modo IA exige explicar por que
- `N11-modo_ia_exige_por_que` [pendiente] Programa antes que IA, por regla: Modo IA exige explicar por que — depende de: V-N11-modo_ia_exige_por_que

### Paso 10 Velocidad sin repetir
- `V-R4c` [pendiente] Vigia primero: El capataz tampoco repite la corrida de la vigia de la orden
- `R4c` [pendiente] El capataz tampoco repite la corrida de la vigia de la orden — depende de: V-R4c
- `V-R3` [pendiente] Vigia primero: Preguntar a los lentos a la vez, no en fila
- `R3` [pendiente] Preguntar a los lentos a la vez, no en fila — depende de: V-R3
- `V-N22-la_espera_de_big_pickle_es_400` [pendiente] Vigia primero: La espera por defecto de Big Pickle es 400
- `N22-la_espera_de_big_pickle_es_400` [pendiente] La espera maxima es 400 segundos: La espera por defecto de Big Pickle es 400 — depende de: V-N22-la_espera_de_big_pickle_es_400
- `N22-la_vigia_vieja_de_big_pickle_pide_400` [pendiente] La espera maxima es 400 segundos: La vigia vieja pide 400
- `N22-la_vigia_de_nadie_mas_de_lo_medido_pide_400` [pendiente] La espera maxima es 400 segundos: Los dos casos de Big Pickle piden 400
- `132` [pendiente] El revisor no llama a Big Pickle mientras descansa y cuenta sus fallos
- `53` [pendiente] Si Big Pickle falla, revisa Codex

### Paso 11 La llave por partes
- `V-R7` [pendiente] Vigia primero: La llave abre solo lo que la tarea necesita
- `R7` [pendiente] La llave abre solo lo que la tarea necesita — depende de: V-R7

### Paso 12 Automatizar
- `167` [pendiente] El comando director del Ingeniero
- `184` [pendiente] La orden corta del director: la IA solo piensa, el programa redacta
- `185` [pendiente] El comando director corta
- `V-R8` [pendiente] Vigia primero: Un comando que arma el plan de trabajo solo
- `R8` [pendiente] Un comando que arma el plan de trabajo solo — depende de: V-R8
- `V-N13-el_arquitecto` [pendiente] Vigia primero: El arquitecto
- `N13-el_arquitecto` [pendiente] El arquitecto propone la estructura: El arquitecto — depende de: V-N13-el_arquitecto
- `V-N13-el_comando_plan_usa_al_arquitecto` [pendiente] Vigia primero: El comando plan usa al arquitecto
- `N13-el_comando_plan_usa_al_arquitecto` [pendiente] El arquitecto propone la estructura: El comando plan usa al arquitecto — depende de: V-N13-el_comando_plan_usa_al_arquitecto

### Paso 12b La prueba real del informe
- `V-N23-la_prueba_real_del_informe` [pendiente] Vigia primero: El programa de la prueba real del informe
- `N23-la_prueba_real_del_informe` [pendiente] La medida unica: Julio pudo hacer su informe hoy: El programa de la prueba real del inform — depende de: V-N23-la_prueba_real_del_informe

### Paso 13 Lo que quedaba pendiente sin vigia
- `V-H4-el-candado-de-memoria-avisa-sin-cobrar-peaje` [pendiente] Vigia primero: El aviso de la memoria avisa una vez y deja pasar, en vez de obligar a repe
- `H4-el-candado-de-memoria-avisa-sin-cobrar-peaje` [pendiente] El aviso de la memoria avisa una vez y deja pasar, en vez de obligar a repetir cada accion — depende de: V-H4-el-candado-de-memoria-avisa-sin-cobrar-peaje
- `V-H6-que-no-se-muerda-la-cola` [pendiente] Vigia primero: Que la reparacion de frenos no se muerda la cola: se consulta el camino que
- `H6-que-no-se-muerda-la-cola` [pendiente] Que la reparacion de frenos no se muerda la cola: se consulta el camino que ya fallo, tamb — depende de: V-H6-que-no-se-muerda-la-cola
- `V-H1-el-tiempo-de-reparacion-se-mide` [pendiente] Vigia primero: La senal de que la herramienta mejora: el tiempo de reparacion, medido solo
- `H1-el-tiempo-de-reparacion-se-mide` [pendiente] La senal de que la herramienta mejora: el tiempo de reparacion, medido solo — depende de: V-H1-el-tiempo-de-reparacion-se-mide
- `V-R25-el-guardado-compara-el-color-no-exige-verde` [pendiente] Vigia primero: El guardado compara con el color de antes, en vez de exigir verde absoluto
- `R25-el-guardado-compara-el-color-no-exige-verde` [pendiente] El guardado compara con el color de antes, en vez de exigir verde absoluto — depende de: V-R25-el-guardado-compara-el-color-no-exige-verde
- `V-R23-codex-no-hace-el-papeleo` [pendiente] Vigia primero: A Codex no se le frena por papeleo que el no puede hacer
- `R23-codex-no-hace-el-papeleo` [pendiente] A Codex no se le frena por papeleo que el no puede hacer — depende de: V-R23-codex-no-hace-el-papeleo
- `V-95-F001329` [pendiente] Vigia primero: 95-F001329
- `95-F001329` [pendiente]  — depende de: V-95-F001329
- `V-95-F012213` [pendiente] Vigia primero: 95-F012213
- `95-F012213` [pendiente]  — depende de: V-95-F012213


## Decisiones y definiciones de Julio (copiadas textuales del plan anterior)

# QUÉ SIGNIFICA "ECONÓMICO" — DEFINICIÓN DE JULIO (2026-09-27)

> **No se vuelve a preguntar el precio del token: eso NO es lo que lo hace económico.**
> Palabras de Julio, sin retocar:
>
> *"Lo barato no es para que me preguntes cuánto cuesta el token, no, barato es que todo lo que no
> necesita de IA, absolutamente todo, se haga por programa, eso es lo que lo hace económico.
> Además, que no repita procesos innecesarios, que sea preciso y no se pierdan vueltas en esto, que
> no se pierda trabajo bajo ninguna circunstancia. Que sea rápido, que se automaticen todas las
> tareas que necesiten programa, que todo esté conectado, que las respuestas tengan disparadores,
> para que se tomen acciones instantáneas. Esto es lo que lo hace económico. También que lo que
> puedan hacer las IA gratis, lo hagan, esto lo hace económico. Que tú no uses sino los recursos
> estrictamente necesarios, eso lo hace económico, y las IA pagas, Claude, DeepSeek."*

**Esta es ahora la vara de medir de todo el plan.** Las tres palabras no son tres bloques
separados: rápido, preciso y económico son la misma cosa vista desde tres lados.

## Los siete puntos y dónde se cumple cada uno

| Lo que dijo Julio | Quién lo cumple | Estado |
|---|---|---|
| 1. Todo lo que no necesita IA, lo hace un programa | `arnes/revisor_de_programa.py` (revisa gratis, sin IA), `R2b` (no se paga una pregunta imposible), `R9` (crear no es inventar: que lo compruebe un programa) | R2b hecha · **R9 pendiente** · falta una regla general |
| 2. No repetir procesos innecesarios | `R4a`+`R4b` (la misma prueba no se corre dos veces), `R4`, `R4c` | R4a/R4b hechas · **R4, R4c pendientes** |
| 3. Preciso, sin perder vueltas | `R13` (el paquete trae el archivo que se le nombra), `R14` (una ronda declara y usa), `R10` | **las tres pendientes — son las que más vueltas costaron** |
| 4. No perder trabajo bajo ninguna circunstancia | `R1` y su familia `R1b`/`R1c`/`R1d` (el trabajo aprobado llega al disco) | R1b/R1c/R1d hechas · **R1 pendiente** |
| 5. Automatizar y que todo esté conectado, con disparadores para acciones instantáneas | `R8` (el comando que arma el plan solo), `R3c` (disparador automático de los dos puestos de pago), `R5` (ningún proceso colgado) | R5 hecha · R3c en espera por orden suya · **R8 pendiente** · **falta la regla general de disparadores** |
| 6. Lo que puedan hacer las IA gratis, que lo hagan | la fila de cerebros pone lo gratis primero (`cuotas.ORDEN`), `R3` (preguntarles a la vez, no en fila) | funciona · **R3 pendiente** |
| 7. Claude no usa sino los recursos estrictamente necesarios; las de pago son Claude y DeepSeek | la ley del paquete mínimo, `arnes/read_gate.py`, `R7` (la llave abre solo lo que la tarea necesita) | funciona · **R7 pendiente** |

## Lo que esta definición cambia en el plan

1. **Ya no hace falta el dato del precio del millón de unidades.** Queda descartado como bloqueo.
2. **Los tres objetivos dejan de ir por separado.** El bloque de precisión (`R13`, `R14`, `R1`,
   `R9`, `R10`) es también el bloque económico: cada vuelta perdida es una llamada pagada de más.
   Por eso el orden de ataque **no cambia**: `R13` y `R14` primero, porque son las que hacen que
   todo lo demás no se repita.
3. **Dos huecos que la definición deja al descubierto y que no tienen orden todavía:**
   - **Una regla general de "programa antes que IA"**: hoy se cumple caso por caso, no hay nada que
     lo obligue en cada vuelta.
   - **Los disparadores**: hoy solo hay uno pensado así (el de los dos puestos de pago). No existe
     una forma común de que una respuesta dispare la acción siguiente sin que alguien se acuerde.

   Estos dos se apuntan como órdenes nuevas **antes** de seguir, para que no vivan en el chat.

### DECIDIDO POR JULIO EL 2026-09-27 — la espera máxima es 400 s

Palabras de Julio: *"Que tenga un disparador la respuesta, para que cuando haya respuesta no tenga
que esperar tiempo innecesario. Disminuir el tiempo de espera a 400 s, pero el criterio es: si se
activa el disparador, se atiende el requerimiento y máximo se espera 400 s; si no responde en ese
momento, se le pasa el encargo a otro."*

Medición que lo respalda (2026-09-27, `memoria/CUADERNO_DE_LLAMADAS.jsonl`): de las **163 respuestas
buenas** de Big Pickle, la más lenta tardó **314 s**, así que con 400 s **no se pierde ninguna** y el
peor caso baja de 600 a 400. grok47: 27 buenas, todas antes de 240 s.

Estado de esta decisión:
- **HECHO:** `TECHO_ESPERA = 400` declarada en `cuerpo/cuotas.py` y respetada por `cuanto_esperarle`.
- **HECHO (ya era así):** el disparador ya es la respuesta — `bigpickle.preguntar` devuelve en cuanto

- **DECIDIDO POR JULIO EL 2026-09-27 (opción b): sin trabajo doble.** R7 cambia la forma en que los
  **21 candados** piden permiso; si se hiciera "a lo bruto" habría que volver a tocar cada candado ya
  reparado. Julio eligió que el cambio sea **compatible con la forma vieja**: `autorizada()` sin
  argumentos sigue funcionando igual, y el nombre del candado se le pasa **solo cuando le toque a ese
  candado por otro motivo**. Así R7 se queda donde está en la fila y **ninguna reparación anterior se
  rehace**.

# R8 · El comando que arma el plan solo (para Foto Informe y cualquier repo)

`python ingeniero.py plan <proyecto> "<el problema>"`, encadenando piezas que **ya existen**:

| Hace falta | Pieza que ya lo hace |
|---|---|
| confirmar carpeta y rama buenas | `via` ([ingeniero.py:253](ingeniero.py#L253)) + `arnes/via_canonica.py`; Foto Informe en [proyectos.config:18](proyectos.config#L18) |