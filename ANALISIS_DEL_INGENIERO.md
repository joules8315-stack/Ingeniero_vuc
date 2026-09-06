# Análisis del Ingeniero

> **ESTE ES EL ÚNICO ARCHIVO DE DIAGNÓSTICO.** Julio, 2026-09-05: *"Unifica, crea un solo archivo,
> ya existen por lo menos dos que hablan de esto."* Lo que haya en otros documentos sobre qué
> falla, qué se reparó y qué falta, **se trae aquí**. No se abre otro.

---

# ESTADO AL 2026-09-05 — MEDIDO, NO OPINADO

## Los cuatro números que mandan

| Qué se midió | Resultado |
|---|---|
| Frenadas de los candados (desde el 20-ago) | **13.375** |
| Trabajos del equipo que **SIRVIERON** | **2 de 70** (3%) |
| Esfuerzo de 30 días que fue a la **herramienta** | **85%** (182 guardados) |
| Esfuerzo que fue a los **productos que dan dinero** | **15%** (32 guardados) |
| Vigías en verde | **560** — y el producto de Julio no genera un informe |

**Trece mil frenadas para dos resultados útiles.**

## Reparto de los 70 trabajos del equipo

| Cómo acabó | Cuántos |
|---|---|
| Sin llegar a juzgarse | 60 |
| No concluyente | 5 |
| **Sirvió** | **2** |
| Se quedó corto (faltó material) | 2 |
| Esperando que Julio decidiera | 1 |

---

# LAS TRES CAUSAS, CADA UNA CON SU PRUEBA

## Causa 1 — El sistema mide sus aciertos solo y sus errores a mano

```
frenadas cazadas : 13.375   <- se suma sola
frenos en falso  :      2   <- hay que apuntarlos a mano
```

Julio recibió **al menos seis** frenadas falsas en pocos días. **Ninguna está contada.**

**Consecuencia:** el termómetro solo sube. El sistema siempre parece que va bien, así que **nunca
se entera de que va mal**. Esa es la respuesta medida a *"por qué no aprende de sus fallos"*.

**Agravante:** esto ya estaba escrito como lección —*"no medir algo importante con un contador que
hay que subir a mano"*— y se repitió igual.

## Causa 2 — Una lección solo avisa; avisar no detiene a quien ya decidió

De las **66 lecciones** guardadas, **51 son de dos días** (20 y 21 de agosto). Después, casi nada.
**Dejó de aprender hace dos semanas y siguió funcionando igual.**

**Prueba del mismo día:** la lección *"no des por bueno un anuncio sin comprobarlo"* estaba escrita,
y el sistema anunció **APLICADO** sin comprobar nada.

## Causa 3 — Todo mide la herramienta; nada mide si Julio puede trabajar

**560 vigías en verde y el programa no genera un informe.** Las vigías comprueban que la
herramienta se porta bien. **Ninguna comprueba que Julio pudo hacer su informe.**

Por eso se puede tener el sistema entero en verde y el negocio parado. **Es la causa de fondo.**

---

# LA RUTA: EN QUÉ FASE VAMOS

| Fase | Qué es | Estado |
|---|---|---|
| **0** | Medir de verdad qué falla | **HECHO** (2026-09-05, los números de arriba) |
| **1** | Que no se escriba en el proyecto equivocado | **HECHO** (ver abajo) |
| **2** | Que los frenos falsos se cuenten solos | pendiente |
| **3** | Que una lección repetida pase a candado | pendiente |
| **4** | **La medida única: ¿Julio pudo hacer su informe hoy?** | pendiente — *lo más importante* |
| **5** | Cerrar las 7 puertas del candado de equipo | a medias: vigía escrita y roja, apartada |
| **6** | Que el entregador traiga la función completa | pendiente |
| **7** | El vigilante que autoriza desde el plan aprobado | legislado, no construido |
| **8** | **Volver a Foto Informe y terminarlo** | **parado en el paso 6 de 8** |

---

# LO REPARADO (con prueba, no de palabra)

| Qué | Cuándo | Prueba |
|---|---|---|
| El filtro de datos destrozaba el código que se manda a los cerebros | 28-ago | Vigía nació roja, verde ahora, sabotaje comprobado |
| El auditor rechazaba por contar renglones | 28-ago | Ídem |
| Los enlaces del Word no saltaban (dos marcadores con el mismo número) | 28-ago | Ídem |
| **Anunciaba APLICADO habiendo escrito en la carpeta equivocada** | **05-sep** | **Vigía nació roja 2 de 6, verde ahora, sabotaje comprobado** |

## Detalle del último, porque es el que más daño hacía

Cuando la propuesta era un **cambio** sobre un archivo existente y ese archivo no estaba en la ruta
resuelta, **lo creaba** con solo el trozo nuevo dentro y devolvía éxito. Así nació un archivo de
Foto Informe **dentro de la carpeta del Ingeniero**, mientras arriba se anunciaba *"APLICADO"*.

**La ruta mal resuelta convertía un error en un éxito silencioso** — la peor clase de error, porque
quien viene detrás trabaja sobre algo que no existe y la ronda se paga igual.

---

# LO QUE FALTA, POR ORDEN DE DAÑO

1. **Nadie mide si el producto sirve.** (Fase 4)
2. **Los frenos falsos no se cuentan.** (Fase 2)
3. **El entregador entrega material incompleto.** Es lo que tumba la mayoría de las rondas. (Fase 6)
4. **Siete puertas por las que se puede escribir sin equipo**, una de ellas un accidente: si no se
   puede leer la petición, deja pasar. (Fase 5)
5. **La vía canónica solo se comprueba al arrancar**, no al escribir. Parcialmente cerrado hoy.

---

# PARA CONSULTAR CON OTRA IA — TODO LO QUE HACE FALTA SABER

Julio, 2026-09-05: *"dame todos los datos, para consultar con otra IA."* Aquí está, completo y sin
adornos.

## Qué es esto

Una herramienta que ayuda a construir y reparar dos productos, escrita en Python, en Windows.
Trabaja así: ante un problema se pide un **paquete mínimo** (los trozos de código relevantes), dos
IA distintas trabajan (una propone, otra audita), y unos **candados** (hooks) frenan las acciones
que rompen las reglas.

## Las piezas

- **El entregador**: elige qué trozos de código se le enseñan a las IA.
- **El equipo**: una IA propone un cambio en JSON (archivo, texto viejo, texto nuevo), otra lo
  audita y da un veredicto.
- **El aplicador**: escribe en disco el cambio aprobado.
- **Los candados**: 14 piezas enganchadas a los eventos de la herramienta; salir con código 2 frena.
- **Las vigías**: 560 pruebas automáticas.
- **La memoria**: 66 lecciones de fallos pasados, que se muestran antes de repetir una acción.

## Los síntomas medidos

1. 3% de éxito del equipo (2 de 70).
2. 13.375 frenadas, con solo 2 frenos falsos registrados (se apuntan a mano).
3. 85% del esfuerzo en la herramienta, 15% en los productos.
4. 560 vigías verdes con el producto sin funcionar.
5. Los rechazos del auditor se concentran en cosas que no son la reparación: números de línea que
   no cuadran, material incompleto, respuestas ilegibles.

## Las preguntas concretas para esa IA

1. Con un 3% de éxito del equipo, **¿el fallo está en el entregador, en el formato de la propuesta,
   o en el criterio del auditor?** ¿Qué medición lo decide?
2. **¿Cómo se hace que un sistema de este tipo cuente sus propios errores sin depender de que
   alguien los apunte?**
3. **¿Cómo se evita que 560 pruebas en verde convivan con un producto que no funciona?** ¿Qué
   medida única lo impediría?
4. Con 13.375 frenadas, **¿cómo se distingue el candado que protege del que solo estorba**, sin
   aflojar ninguno a ciegas?
5. **¿Cómo se sale de un sistema que gasta el 85% de su esfuerzo en sí mismo?**

---

# LA LEY QUE MANDA SOBRE TODAS LAS DEMÁS

**Julio, 2026-09-05**, respondiendo a dos preguntas mías mal planteadas (yo le preguntaba si
*parar* o *seguir*):

> *"Se debe hacer siempre analizar la información y determinar qué está mal: la herramienta, o el
> razonamiento, o la información recibida, o quien reparte. Se debe ver qué está fallando. Si no,
> ¿qué caso tiene?"*

**La pregunta nunca es "¿paro o sigo?". La pregunta es "¿QUIÉN FALLÓ?".**

## Los cuatro sospechosos, siempre los mismos

Ante **cualquier** freno, aviso, rechazo o resultado raro, se determina cuál de los cuatro falló:

| # | Quién | Cómo se reconoce | Qué se repara |
|---|---|---|---|
| 1 | **La herramienta** | El candado frenó algo que estaba bien | El candado |
| 2 | **El razonamiento** | Se midió bien y se concluyó mal | Quien concluyó |
| 3 | **La información recibida** | El material no traía lo necesario | La memoria |
| 4 | **Quien reparte** | Trajo lo que no era, o incompleto | El entregador |

**Y se repara al que falló.** No se rodea el freno, no se pide permiso para saltarlo, no se
"sigue igual". Eso es lo que convierte cada tropiezo en una mejora en vez de en un obstáculo.

## Por qué esto lo cambia todo (medido)

Hoy hay **13.375 frenadas** y **2 frenos falsos apuntados**. Esa diferencia no es que el sistema
acierte el 99,98% de las veces: es que **nadie preguntó nunca quién falló**. Las frenadas se
trataban como obstáculos que superar, no como información.

Si de cada frenada se hubiera determinado el culpable:
- las falsas habrían reparado **el candado**,
- las de material incompleto habrían reparado **el entregador**,
- las de conclusión equivocada habrían reparado **el razonamiento**.

**El sistema tenía 13.375 oportunidades de aprender y aprovechó dos.**

## Lo que esto obliga a construir

Cada freno tiene que acabar en una de estas cuatro respuestas, **escrita y contada sola**. Un
freno sin culpable identificado es un freno desperdiciado.

---

# EL PLAN: LA MEMORIA COMO RED, NO COMO LISTA

**Julio, 2026-09-05:** *"No has entendido lo de la memoria. La idea es que crees una red neuronal,
y esa red esté disponible, para que cuando te pida hacer algo tengas la información veraz, completa,
pertinente."*

## Qué hay hoy (medido) y por qué no sirve

| Pieza | Qué guarda | Por qué no sirve |
|---|---|---|
| Las lecciones | 66 textos de fallos pasados | Son una **lista**, no una red. Se muestran por parecido de palabras, no por relación |
| El mapa | Qué archivo hace qué | **El entregador no lo usa** para decidir qué traer |
| Los hilos | Quién llama a quién | Existen, pero **no se consultan al reparar** |
| El entregador | Trozos por parecido de palabras | Las palabras **no saben** dónde empieza una pieza ni a quién daña tocarla |

**El fallo de fondo:** cada pieza guarda algo suelto y **nada las relaciona**. Por eso hay
información y aun así se repara a ciegas.

## Lo que debe ser: una red que responda cinco preguntas

Antes de tocar nada, la red tiene que poder contestar **sin que nadie lo escriba a mano**:

| # | Pregunta | Hoy |
|---|---|---|
| 1 | **¿Qué pieza hace de verdad lo que se pide?** | Se adivina por palabras |
| 2 | **¿A quién daño si la toco?** | Existe la lista, no se consulta |
| 3 | **¿Esto ya se intentó antes y falló?** | 66 lecciones sueltas, por parecido |
| 4 | **¿Falta legislar, candado, tabla, matriz, vigía, arnés o skill?** | Nadie lo comprueba |
| 5 | **¿Esta reparación resuelve lo pedido, o crea otro problema?** | **Nadie lo comprueba** |

## Las siete comprobaciones antes de reparar (punto 4.3 de Julio)

Ante cualquier orden, la red responde **sí/no/no aplica** a cada una, y **si falta alguna, se
construye antes de tocar código**:

| # | Qué | Para qué sirve |
|---|---|---|
| 1 | **Legislación** | Que la regla quede escrita, no en la cabeza de nadie |
| 2 | **Candado** | Que la regla frene de verdad, porque escrita no es cumplida |
| 3 | **Tabla de la verdad** | Qué debe pasar en cada caso, incluidos los raros |
| 4 | **Matriz** | Qué se toca y **a quién daña** |
| 5 | **Vigía** | Que si se rompe, se sepa |
| 6 | **Arnés** | Que el candado esté enchufado de verdad y no sea adorno |
| 7 | **Skill** | Que el paso a paso quede guardado y no se reinvente |

## Las dos leyes que Julio subrayó

**No reparar a ciegas.** Si no se sabe **qué** hay que reparar, no se toca: se mide primero. Una
reparación sobre una sospecha es una avería nueva con permiso.

**No romper otra cosa.** Antes de tocar, la red dice **a quién daña**; después de tocar, se
comprueba que esos siguen sanos. Sin las dos mitades, no está reparado.

## Cómo se construye, por fases y en este orden

| Fase | Qué se construye | Por qué en ese orden |
|---|---|---|
| **A** | **La red se arma sola** desde lo que ya existe (mapa, hilos, lecciones, flujos) | Sin red no hay nada que consultar. **No se pide a nadie que la escriba a mano** |
| **B** | **Consulta obligatoria antes de reparar**: las cinco preguntas | Es lo que evita reparar a ciegas |
| **C** | **Las siete comprobaciones** como candado | Si falta una, se para y se dice cuál |
| **D** | **¿Daña a alguien?** antes y después | Es la mitad que falta de "no romper otra cosa" |
| **E** | **La red aprende sola**: cada fallo entra sin que nadie lo apunte | Hoy los aciertos se cuentan solos y los errores a mano: 13.375 contra 2 |
| **F** | **¿Resuelve lo pedido?** Se comprueba contra lo que Julio pidió, no contra las vigías | Es la única medida que manda |

## Lo que hace falta para que esto no sea otro humo

Cada fase nace con **su vigía en rojo primero**, y **no se da por hecha** hasta que:

1. La vigía pasa de roja a verde.
2. Se **rompe la cura a propósito** y la vigía vuelve a ponerse roja.
3. **Ninguna de las otras se rompe**.
4. Queda escrito **qué se midió**, no qué se cree.

---

# PARA QUIEN EVALÚE ESTE PLAN

Lo que hay que juzgar, con los números de arriba delante:

1. **¿La red resuelve el 3%?** El 97% de las rondas se cae por material incompleto o por
   respuestas ilegibles. ¿Una red de relaciones ataca eso, o hace falta otra cosa?
2. **¿El orden de las fases es el correcto?** ¿O hay una que daría más resultado antes?
3. **¿Falta alguna fase?** En especial: ¿cómo se comprueba **de verdad** que una reparación
   resuelve lo pedido y no crea otro problema?
4. **¿Se puede armar la red sola desde lo que ya existe**, o hace falta escribir algo a mano —y
   entonces se pudre igual que el contador que hay que subir a mano?
5. **¿Cómo se evita que esta red acabe siendo otra pieza más que existe y nadie usa**, como el mapa
   y los hilos de hoy?

---

# EL MAPA: QUÉ HAY, MEDIDO HOY

## El inventario

| Parte | Piezas | Renglones | Qué hace |
|---|---|---|---|
| La memoria y el entregador | 8 | 1.669 | Decide qué código se le enseña a las IA |
| El equipo y el trabajo | 15 | 3.157 | Las IA que proponen y auditan, y quien aplica |
| Los candados | 39 | 6.368 | Frenan lo que rompe las reglas |
| Las vigías | 96 archivos | 566 pruebas | Comprueban que la herramienta se porta bien |

**Los candados ocupan más que la memoria y el equipo juntos.** Eso es el retrato del problema: la
mayor parte del sistema existe para impedir cosas, no para hacerlas.

## La memoria y el entregador, pieza por pieza

| Pieza | Qué hace | Estado medido |
|---|---|---|
| Los hilos | Quién llama a quién | Existe. **No se consulta al reparar** |
| Los flujos | Los asuntos del proyecto | Existe |
| El grafo | Junta las capas | Existe |
| Las piezas | Un nodo por archivo, y traer una función por su nombre | **Reparado hoy**: ahora también sabe qué función contiene un trozo |
| El protocolo | Cómo se trabaja | Existe |
| El repartidor | Entrega el material | **Reparado hoy**: ya trae la función entera |
| El semántico | Buscar por significado | Existe. Sin medir si se usa |
| Los trozos | Parte el archivo en pedazos | Ventanas de 40 renglones |

## Los candados: cuántas veces frenó cada uno

| Candado | Frenadas | Frenos falsos apuntados |
|---|---|---|
| Terminal | 4.983 | 0 |
| Equipo | 3.760 | 0 |
| Prueba real | 1.144 | 0 |
| Cierre | 957 | 0 |
| Memoria | 797 | 0 |
| Por nombre | 540 | 0 |
| Buzón | 322 | 0 |
| Archivo del veredicto | 293 | 0 |
| Legislar | 289 | 0 |
| Compañero | 193 | 0 |
| Commit | 96 | 0 |
| Preguntar | 1 | 0 |
| Diagnóstico | 0 | 1 |
| Supervisor | 0 | 1 |

**Ninguno tiene un solo freno falso apuntado**, salvo dos que solo tienen eso. Y hubo al menos
seis reales en pocos días. **Los frenos falsos se apuntan a mano, así que no se apuntan.**

---

## Parte 1 - Qué hay de cada punto

### Punto 1: Ayudar a construir proyectos rápido, confiable, económico y en equipo
**A MEDIAS.**

*Prueba:* El Ingeniero lleva días reparándose a sí mismo y no ha construido ni una línea de las aplicaciones de Julio. Su producto de fotos sigue parado en el paso 6 de 8. Existen piezas que trabajan (consejeros, obrero, etc.) y un equipo que aprende, pero el resultado no llega a los proyectos de Julio.

### Punto 1.1: El equipo debe trabajar como un reloj suizo, enfocado
**A MEDIAS.**

*Prueba:* El equipo solo sabía hacer un tipo de trabajo (cambiar código) y acaba de aprender el segundo (analizar). Tres intentos de análisis fueron rechazados antes. No hay evidencia de que el equipo esté enfocado en una tarea sin distraerse.

### Punto 1.1.1: Dividir el trabajo en partes con bloques completos
**NO EXISTE.**

*Prueba:* No se menciona ningún mecanismo que divida el trabajo en bloques completos. El encargo se reescribía a ojo hasta ocho veces antes de aprobarse, lo que indica que no hay una división clara.

### Punto 1.1.2: Tener todo el proyecto planeado, un mapa claro
**A MEDIAS.**

*Prueba:* Existen piezas que piensan (enlaces, flujos, grafo, piezas, protocolo, router, semántico, trozos) y leyes escritas, pero no hay un mapa único y claro que Julio pueda ver. El punto 1.1.2.5 pide una memoria tipo Obsidian con mapa, matriz y tabla de verdad, y eso no existe como tal.

#### Punto 1.1.2.1: Entender la idea, ver el flujo de trabajo
**A MEDIAS.**

*Prueba:* Existen piezas llamadas "flujos" y "grafo", pero no se evidencia que se haya tomado una idea de Julio y se haya convertido en un flujo claro. El producto de fotos está parado, lo que sugiere que el flujo no se entendió o no se ejecutó.

#### Punto 1.1.2.2: Legislar
**HECHO.**

*Prueba:* Hay 25 leyes escritas, incluyendo dos de legislación y una matriz de legislación.

#### Punto 1.1.2.3: Candados en áreas clave, permitiendo bucles sin pedir permiso
**A MEDIAS.**

*Prueba:* Existen 18 candados, pero dos llegaron a contradecirse: uno exigía lo que el otro prohibía. Además, un aviso del sistema obliga a repetir cada orden dos veces, lo que va en contra de "trabajar en bucle sin pedir permiso".

#### Punto 1.1.2.4: Vigilantes para que no se rompa lo que sirve
**A MEDIAS.**

*Prueba:* Existen candados y un revisor, pero el revisor rechazaba trabajo bueno por motivos falsos (llamaba inventar a lo que el encargo pedía y rechazaba por una coma). Eso se reparó ayer, pero no hay garantía de que otros vigilantes funcionen bien.

#### Punto 1.1.2.5: Memoria que sepa para qué sirve cada pieza, por función, tipo Obsidian, con mapa, matriz y tabla de verdad
**NO EXISTE.**

*Prueba:* No hay ninguna pieza que haga esto. Existen "piezas" y "trozos", pero no una memoria central que organice por función y que sea legible para todos los agentes.

#### Punto 1.1.2.6: Agente que sepa qué agente usar según capacidad, cuándo, por qué, cómo y para qué
**NO EXISTE.**

*Prueba:* Existe un "router" (repartidor) y un "semántico", pero no se menciona que sepa elegir según capacidad de memoria. La medición de cerebros mide una prueba de marketing, no la capacidad real de reparar código.

### Punto 2: Trabajar en bucle hasta construir lo pedido
**NO EXISTE.**

*Prueba:* No hay evidencia de que el Ingeniero trabaje en bucle. El encargo se reescribía ocho veces, el trabajo aprobado se tiraba, y el producto de fotos está parado. No hay un mecanismo que haga que el trabajo continúe hasta terminar.

### Punto 3: Medir las capacidades reales de cada miembro
**A MEDIAS.**

*Prueba:* Existe un "medidor" y una tabla que dice lo bueno que es cada cerebro, pero mide una prueba de marketing, NO la de reparar código. Un cerebro con 100% en esa tabla alucinó tres veces seguidas reparando.

### Punto 4: Arnés fuerte pero sin pedir permiso a cada instante
**A MEDIAS.**

*Prueba:* Existen 18 candados, pero se contradicen y obligan a repetir órdenes. Eso es un arnés que frena, no que guía. No hay un equilibrio entre control y libertad.

### Punto 5: Autoevaluación y autoreparación
**A MEDIAS.**

*Prueba:* Existen piezas como "fallos", "lecciones" y "memoria de fallos", y el Ingeniero se repara a sí mismo. Pero lo hace de forma descontrolada: lleva días reparándose y no construye para Julio. No hay un método claro de autoevaluación.

### Punto 6: Director que vigile, pida informes JSON, y repartidor inteligente con red de conocimiento
**A MEDIAS.**

*Prueba:* Existe un "router" (repartidor) y piezas de red (enlaces, grafo), pero no se evidencia que pida informes JSON ni que tenga una red de conocimiento fuerte, sana y actualizada. El revisor rechazaba trabajo bueno, lo que indica que la supervisión no es perfecta.

### Punto 7: Incluir toda la información documentada que no esté en la lista
**NO EXISTE.**

*Prueba:* No hay un inventario de toda la información documentada. Existen 25 leyes y muchas piezas, pero no un índice que las relacione con los puntos de Julio.

## Parte 2 - La causa raíz de cada hueco

### Punto 1 y 1.1: No se construye para Julio
*Causa raíz:* El Ingeniero se ha convertido en su propio proyecto. No hay una prioridad clara que ponga las aplicaciones de Julio primero. Las piezas existen, pero no están orientadas a producir resultados para el dueño del negocio.

### Punto 1.1.1: No hay división en bloques
*Causa raíz:* No hay un plan de trabajo que divida las tareas. Se trabaja "a ojo", reescribiendo el encargo hasta que alguien lo aprueba. Falta una metodología de descomposición.

### Punto 1.1.2: No hay mapa claro
*Causa raíz:* La información está dispersa en muchas piezas y leyes, pero no hay un lugar único que las organice. La memoria tipo Obsidian que pide Julio no existe, así que nadie sabe qué hay y dónde.

#### Punto 1.1.2.1: Flujo no entendido
*Causa raíz:* No hay un proceso que tome la idea de Julio y la convierta en un flujo. Las piezas "flujos" y "grafo" existen, pero no se usan para esto.

#### Punto 1.1.2.3: Candados que contradicen
*Causa raíz:* Los candados se crearon sin una revisión central. Cada uno se hizo para un problema, pero nadie verificó que no se pisaran. La falta de un mapa de candados es la causa.

#### Punto 1.1.2.4: Vigilantes que fallan
*Causa raíz:* El revisor fue programado con reglas equivocadas (rechazar por coma, llamar inventar a lo que el encargo pedía). No hay una prueba real de que el revisor entienda el encargo.

#### Punto 1.1.2.5: Memoria por función no existe
*Causa raíz:* Nunca se construyó. Las piezas se fueron creando sin un registro central de para qué sirve cada una. Es un problema de organización, no de falta de piezas.

#### Punto 1.1.2.6: No hay agente selector
*Causa raíz:* No hay medición real de capacidades, así que no se puede elegir bien. El router reparte, pero no sabe qué cerebro es mejor para cada tarea.

### Punto 2: No hay bucle
*Causa raíz:* No hay un mecanismo que haga que el trabajo continúe hasta terminar. El sistema actual permite que el trabajo se detenga, se reescriba o se descarte. Falta un "empujón" automático.

### Punto 3: Medición equivocada
*Causa raíz:* Se eligió una prueba de marketing porque era fácil de pasar, no porque midiera lo que importa. No se pensó en qué significa "bueno" para reparar código.

### Punto 4: Arnés que frena
*Causa raíz:* Los candados se crearon para proteger, pero sin pensar en la eficiencia. El resultado es que piden permiso constantemente (repetir órdenes) y se contradicen.

### Punto 5: Autoreparación sin control
*Causa raíz:* No hay un método que diga cuándo parar de reparar y empezar a construir. El Ingeniero se repara a sí mismo sin límite, descuidando a Julio.

### Punto 6: Director sin informes
*Causa raíz:* No hay un formato de informe JSON ni una obligación de reportar. El router reparte, pero no supervisa el resultado final.

### Punto 7: Información no inventariada
*Causa raíz:* No se ha hecho un inventario de toda la documentación existente. Hay muchas piezas, pero nadie las ha relacionado con los puntos de Julio.

## Parte 3 - El plan, por orden

| Qué se repara | Dónde | Cómo | Cuándo | Por qué en este orden |
|---|---|---|---|---|
| 1. Medición real de cerebros | En el medidor | Cambiar la prueba de marketing por una prueba real de reparación de código | Primero | Sin saber qué cerebro es bueno, no se puede elegir bien. Todo lo demás depende de elegir bien. |
| 2. Mapa de piezas y leyes | En la memoria (crear o completar) | Organizar toda la información existente en un mapa por función, tipo Obsidian | Segundo | Con un mapa, se sabe qué hay y qué falta. Evita crear duplicados y permite reparar lo que existe. |
| 3. Candados que no se contradigan | En los 18 candados | Revisar cada candado y eliminar contradicciones. Probar que no se piden permisos innecesarios | Tercero | Con un mapa, se ven las contradicciones. Un arnés que no frena es base para trabajar en bucle. |
| 4. Bucle de trabajo | En el sistema de órdenes | Crear un mecanismo que repita la tarea hasta que esté aprobada, sin reescribir a ojo | Cuarto | Con candados coherentes, se puede permitir el bucle sin miedo a que se rompa algo. |
| 5. Repartidor inteligente | En el router | Usar la medición real para elegir el cerebro adecuado. Que sepa qué pieza usar y dónde está | Quinto | Con medición y mapa, el repartidor puede decidir bien. |
| 6. Director que pide informes JSON | En el director | Crear un formato de informe JSON y obligar a que cada tarea terminada lo envíe | Sexto | Con el bucle funcionando, se necesita saber qué se ha hecho. El informe JSON da visibilidad. |
| 7. Autoevaluación y autoreparación con método | En el Ingeniero | Definir un método que diga cuándo reparar y cuándo construir. Limitar el tiempo de reparación | Séptimo | Con todo lo anterior, el Ingeniero puede evaluarse y repararse sin descuidar a Julio. |
| 8. Prioridad a los proyectos de Julio | En el equipo | Establecer que el primer objetivo es construir las aplicaciones de Julio. El Ingeniero no se repara a sí mismo más de lo necesario | Octavo | Con el sistema estable, se puede poner el foco en el dueño del negocio. |

## Parte 4 - Las reglas del método

Para que estas reglas se cumplan solas, se pondrán candados que frenen el sistema si no se cumplen. No dependerán de que alguien se acuerde.

1. **Regla de medición real**: Si un cerebro no ha pasado la prueba de reparación de código, no se puede usar para reparar. El sistema lo bloqueará.
2. **Regla del mapa**: Si una pieza no está en el mapa, no se puede usar. El sistema la ignorará.
3. **Regla de candados coherentes**: Si dos candados se contradicen, el sistema se detiene y avisa. No se puede trabajar con contradicciones.
4. **Regla del bucle**: Si una tarea no está aprobada, el sistema la repite automáticamente. No se puede pasar a otra tarea.
5. **Regla del informe JSON**: Si una tarea no tiene informe JSON, no se considera terminada. El sistema no la cuenta como avance.
6. **Regla de prioridad**: Si el Ingeniero lleva más de un día reparándose sin construir para Julio, el sistema lo detiene y avisa.

## Parte 5 - Lo que añadirías tú

Añadiría una **regla de gasto máximo por tarea**. Hoy la IA cara se lleva el 80% del gasto y una mañana entera consumió el 90% de la sesión. Pondría un candado que avise cuando el gasto de una tarea supere un límite, para que Julio decida si vale la pena. Esto no está en la lista de Julio, pero es esencial para que el proyecto sea económico.

También añadiría un **informe semanal para Julio**, en lenguaje claro, que diga qué se ha construido, qué se ha reparado y cuánto ha costado. Así Julio no necesita ser técnico para saber si el Ingeniero está trabajando bien.

## PARTE 6 - LO QUE YA HAY EN LA CASA

Esto es un inventario de todo lo que ya está documentado y legislado, explicado para que se entienda para qué sirve cada grupo, no por nombres raros. Cada grupo dice qué problema resuelve y en cuál de los 8 pasos del plan se apoya. Si algo ya cubre un paso, se dice claramente: ese paso se COMPLETA, no se empieza de cero.

### Grupo 1: Las reglas del juego (las leyes)
- **Qué es**: Son 25 documentos escritos que dicen cómo hay que comportarse. Por ejemplo, hay leyes que dicen que nunca se debe inventar, que siempre hay que trabajar en equipo, que no se puede romper lo que ya funciona, y que hay que hablarle simple a Julio.
- **Qué resuelve**: Evita que cada uno haga lo que le parezca. Pone orden y obliga a todos a seguir las mismas reglas.
- **En qué paso del plan se apoya**: En el paso 2 (mapa de piezas y leyes) y en el paso 3 (candados coherentes). Estas leyes ya existen, así que el paso 2 se COMPLETA en parte: ya hay leyes, solo falta organizarlas en un mapa claro.

### Grupo 2: Los candados (los frenos que protegen)
- **Qué es**: Son 18 candados que frenan al sistema cuando algo va mal. Por ejemplo, hay un candado que impide que se escriba código desde la línea de comandos, y otro que obliga a leer una nota antes de seguir si se pierde el hilo.
- **Qué resuelve**: Protegen lo que ya funciona. Evitan que se rompan archivos, que se gaste de más, o que se trabaje sin contexto.
- **En qué paso del plan se apoya**: En el paso 3 (candados que no se contradigan). Ya hay candados, pero algunos se contradicen o frenan cosas que no deben, así que este paso se REPARA, no se empieza de cero.

### Grupo 3: Las pruebas (las comprobaciones)
- **Qué es**: Son 87 archivos con 524 comprobaciones, todas en verde hoy. Sirven para verificar que las cosas funcionan.
- **Qué resuelve**: Da confianza de que lo que se hace no rompe lo que ya estaba bien.
- **En qué paso del plan se apoya**: En el paso 1 (medición real de cerebros) y en el paso 4 (bucle de trabajo). Las pruebas ya existen, pero hay que asegurarse de que midan lo que importa, no solo lo fácil.

### Grupo 4: La memoria escrita (lo que se ha aprendido)
- **Qué es**: Son documentos que guardan dónde íbamos, los grafos, el rescate, el registro de lo que cada candado frenó y por qué, el registro de los trabajos del equipo, lo que Julio ya dijo, las decisiones tomadas, el diagnóstico, la medición de los candados, las respuestas y los significados.
- **Qué resuelve**: Que nadie empiece de cero. Todo lo que se ha hecho y aprendido queda guardado para no repetir errores.
- **En qué paso del plan se apoya**: En el paso 2 (mapa de piezas y leyes) y en el paso 7 (autoevaluación y autoreparación). Esta memoria ya existe, pero no está organizada como un mapa único y claro, así que el paso 2 se COMPLETA en parte: ya hay memoria, falta convertirla en un mapa por función.

### Grupo 5: Las leyes de Julio (las reglas sagradas)
- **Qué es**: Son 5 leyes que Julio ha dicho y que son innegociables: nunca asumir, nunca inventar, el vigilante en verde NO es prueba (la prueba es que Julio lo vea con sus ojos), no romper a los vecinos, y hablarle simple. Además hay otras reglas como siempre en equipo sin salto, probar de verdad antes de pedírselo a Julio, la memoria no miente ni olvida, las 5 preguntas antes de tocar nada (qué, dónde, por qué, cuándo y cómo), y la llave única que abre solo los candados que la tarea necesita y avisa cuáles abre y por qué.
- **Qué resuelve**: Son la base de todo. Sin estas leyes, el equipo podría desviarse y hacer lo que no debe.
- **En qué paso del plan se apoya**: En todos los pasos, pero especialmente en el paso 8 (prioridad a los proyectos de Julio). Estas leyes ya existen y se deben respetar siempre.

### Resumen de lo que ya hay y qué se completa
- **Paso 1 (medición real)**: Ya hay un medidor y una tabla, pero mide lo que no importa. Se REPARA.
- **Paso 2 (mapa)**: Ya hay leyes y memoria, pero no un mapa único. Se COMPLETA.
- **Paso 3 (candados coherentes)**: Ya hay 18 candados, pero algunos se contradicen. Se REPARA.
- **Paso 4 (bucle)**: No hay un mecanismo de bucle. Se CREA.
- **Paso 5 (repartidor inteligente)**: Ya hay un router, pero no usa medición real. Se REPARA.
- **Paso 6 (director con informes)**: No hay informes JSON. Se CREA.
- **Paso 7 (autoevaluación)**: Ya hay memoria de fallos y lecciones, pero no un método. Se COMPLETA.
- **Paso 8 (prioridad a Julio)**: No hay una regla que obligue a construir para Julio. Se CREA.

## PARTE 7 - LA TABLA DE FRENADOS

Esta tabla muestra cada frenado que ha pasado, por qué frenó (la causa de fondo, no el síntoma), qué sirve de ese frenado (lo que hay que conservar), qué fue inútil (lo que hay que quitar), y qué se repara exactamente. Si dos frenados tienen la misma causa de fondo, se dice, porque entonces una sola reparación arregla los dos.

| Qué frenó | Por qué frenó (causa de fondo) | Qué SIRVE de ese frenado | Qué fue INÚTIL | Qué se repara exactamente |
|---|---|---|---|---|
| A - El aviso que obliga a repetir cada orden | El candado se creó para confirmar lo grave, pero se dispara con todo, sin distinguir lo importante de lo trivial | Obliga a confirmar antes de algo grave | Se dispara con TODO, hasta con lo trivial | Se repara el candado para que solo pida confirmación en lo grave, no en lo trivial |
| B - El encargo se reescribía hasta 8 veces | No se comprobaba que el material llegara dentro del encargo antes de mandarlo | Nadie trabaja a ciegas | Se pagaba 8 veces lo mismo por no comprobar antes | Se repara el proceso de envío: comprobar que el material está dentro antes de mandar |
| C - El trabajo aprobado se tiraba | No había un registro de lo aprobado, así que se perdía | Nada | Pérdida pura | Se repara el registro de lo aprobado para que no se pierda |
| D - El revisor rechazaba trabajo bueno | El revisor juzgaba la forma (comas, palabras) en vez del fondo (si el trabajo cumple lo pedido) | Cuatro ojos: uno escribe y otro juzga | Juzgar la forma en vez del fondo | Se repara el revisor para que juzgue el fondo, no la forma |
| E - Dos candados se contradecían | No había una revisión central de los candados, así que uno exigía lo que el otro prohibía | Nada | El trabajo no podía avanzar | Se repara la revisión central de candados para que no se contradigan |
| F - Alarma de cuota agotada en falso | La alarma se basaba en un dato equivocado (creía que no había cuota cuando sí la había) | Avisa cuando la cuota se agota | Gritaba en falso y bloqueaba el día | Se repara la alarma para que use datos reales |
| G - El candado de la terminal frena cosas que solo miran | El candado se creó para impedir que se rompan archivos, pero también frena lo que solo lee | Impide que se rompan archivos | Frena lo que solo lee, como pedir las últimas líneas de un registro | Se repara el candado para que distinga entre escribir (peligroso) y leer (seguro) |
| H - El compañero reportó 3 veces que había terminado sin hacerlo | No se comprobaba el trabajo del compañero antes de creerle | Tener quien ayude | Creerle sin comprobar | Se repara el proceso de verificación: comprobar siempre lo que reporta el compañero |
| I - La tabla de cerebros mide lo que no importa | Se eligió una prueba de marketing porque era fácil, no porque midiera la capacidad real de reparar código | La idea de medir | Medir lo que no importa | Se repara la prueba para que mida la capacidad real de reparar código |
| J - Se reportaba todo en verde sin avance real | No había una definición clara de qué es un avance para Julio | Nada | Verde no significa que Julio termine su aplicación | Se repara el informe para que muestre avance real en los proyectos de Julio |
| K - La IA cara se mete en todo y gasta el 80% | No hay un límite de gasto ni una ubicación estratégica para la IA cara | Nada | Gasto excesivo sin beneficio claro | Se repara la ubicación de la IA cara: solo para supervisar e instruir, no para escribir código |
| L - La nota para recuperar el hilo apunta a un asunto viejo | La nota no se actualiza cuando cambia el trabajo, así que no orienta | No continuar inventando lo que se cree recordar | La nota apunta a un asunto viejo que ya no es el actual | Se repara la nota para que siempre apunte al asunto actual |

**Causas de fondo que se repiten**: Los frenados B, C y J tienen la misma causa de fondo: no hay un registro claro de lo que se ha aprobado y de lo que es un avance real. Una sola reparación (crear un registro de aprobaciones y avances) arregla los tres. Los frenados D y H también comparten causa: no se comprueba el trabajo antes de darlo por bueno. Una sola reparación (obligar a comprobar siempre) arregla los dos.

## PARTE 8 - EL PROTOCOLO DE REPARACIÓN

Este es el método que el equipo debe seguir siempre ante cualquier fallo. Está escrito como protocolo, en pasos numerados, para que todos lo hagan igual. Cada paso tiene un candado que impide saltárselo y un vigilante que comprueba que el candado sigue puesto. Recuerda la lección de esta casa: lo escrito se ignora, solo lo que FRENA se cumple.

### Paso 1: Anotar el fallo
- **Qué se hace**: Cuando algo falla, se escribe en el registro de fallos. Se anota qué pasó, cuándo pasó, y qué se estaba haciendo.
- **Candado**: No se puede seguir al siguiente paso si el fallo no está anotado.
- **Vigilante**: El registro de fallos comprueba que la anotación existe.

### Paso 2: Buscar la causa de fondo
- **Qué se hace**: Se investiga por qué falló de verdad, no solo el síntoma. Se usan las 5 preguntas: qué, dónde, por qué, cuándo y cómo.
- **Candado**: No se puede proponer una reparación si no se ha encontrado la causa de fondo.
- **Vigilante**: El equipo revisa que la causa de fondo esté bien identificada.

### Paso 3: Decidir si se repara o se completa lo que ya hay
- **Qué se hace**: Se mira si ya existe una pieza que haga lo que se necesita. Si existe, se repara o se completa. Si no existe, se crea una nueva, pero solo si de verdad no hay nada parecido.
- **Candado**: No se puede crear algo nuevo si ya hay una pieza que sirve.
- **Vigilante**: El mapa de piezas comprueba que no hay duplicados.

### Paso 4: Comprobar antes de mandar el encargo
- **Qué se hace**: Antes de enviar el trabajo a Julio, se comprueba que todo el material necesario está dentro del encargo. Así no se paga ocho veces lo mismo.
- **Candado**: No se puede enviar el encargo si no se ha comprobado que está completo.
- **Vigilante**: El revisor comprueba que el encargo está completo y que el trabajo cumple lo pedido.

### Paso 5: Revisión final
- **Qué se hace**: Un revisor (que no sea el que escribió) revisa el trabajo. Debe juzgar el fondo, no la forma. Si el trabajo cumple lo pedido, se aprueba. Si no, se devuelve con explicación clara.
- **Candado**: No se puede dar por terminado un trabajo sin la aprobación del revisor.
- **Vigilante**: El revisor comprueba que el trabajo cumple lo pedido.

### Paso 6: Cierre
- **Qué se hace**: Se registra lo que se hizo, cuánto costó, y se informa a Julio en lenguaje claro. Si el trabajo es para un proyecto de Julio, se marca como avance real.
- **Candado**: No se puede cerrar un trabajo sin informe.
- **Vigilante**: El registro de trabajos comprueba que el informe existe.

## PARTE 9 - EL SITIO DE LA IA CARA

La IA cara se coloca en un lugar estratégico: solo para supervisar e instruir, nunca para escribir código. Julio fue tajante: la IA cara no vuelve a escribir código; solo lee el resultado del equipo y se lo cuenta a Julio.

### Qué SÍ puede hacer la IA cara
- Leer el resultado del equipo (el código, los informes, los avances).
- Explicarle a Julio en lenguaje claro qué se ha hecho, qué falta y cuánto ha costado.
- Instruir al equipo barato: decirle qué hacer, pero sin hacerlo ella.
- Supervisar que el equipo no se desvíe y que los candados se cumplan.

### Qué NO puede hacer nunca la IA cara
- Escribir código.
- Reparar código directamente.
- Tomar decisiones por su cuenta.
- Gastar más de un límite sin avisar a Julio.

### Qué candado lo impide
- Un candado de gasto que frena a la IA cara si intenta escribir código o si su gasto supera el límite. Este candado ya existe (el candado del gasto) y se refuerza para que la IA cara solo pueda leer y explicar.
- Un candado de terminal que impide que la IA cara escriba código desde la línea de comandos. Este candado ya existe y se mantiene.

## PARTE 10 - LO QUE AÑADES TÚ

Sí, añado una mejora sustancial que no está nombrada: **un informe semanal para Julio en lenguaje claro**. Este informe dirá, cada semana, qué se ha construido, qué se ha reparado, cuánto ha costado y qué falta para terminar los proyectos de Julio. Así Julio no necesita ser técnico para saber si el equipo está trabajando bien. Esta mejora no está en el plan original y es esencial para que Julio tenga visibilidad sin tener que preguntar.

Además, añado una **regla de gasto máximo por tarea**: si una tarea supera un límite de gasto, el sistema avisa a Julio para que decida si vale la pena seguir. Esto ya se mencionó en el plan original, pero aquí se concreta como un candado más.

---
---

# ESTADO AL 2026-09-06 — LO QUE SE MIDIÓ Y LO QUE SE REPARÓ

Todo lo de aquí abajo está **comprobado en el código o contado del registro**, no opinado.

## Los cinco números nuevos

| Qué se midió | Resultado | Qué significa |
|---|---|---|
| Frenos de los candados | **15.034** | y **CERO** acabaron diciendo quién falló (0,000%) |
| El candado que más frena | **el de la terminal: 5.577 (37%)** | frenaba órdenes que **solo miran**. YA REPARADO |
| Leyes escritas | **25**, y **13 sin vigía (52%)** | más de la mitad de las leyes son papel |
| Trabajos del equipo | **900**, de los que **72** son reales | 828 fueron ensayos en archivos que no existen |
| Quién escribió código real | **solo el de pago: 72. Los gratis: 0** | nunca se les pidió: el mando no deja elegir |

## Las mediciones que se tomaron y NO se usan (lo que Julio sospechaba)

Julio preguntó: *"se han hecho varias pruebas y no son tomadas en cuenta, se pierden,
verifica por qué"*. **Tenía razón. Comprobado:**

| Medición | Quién la lee | ¿Sirve para decidir? |
|---|---|---|
| **Tabla de precisión** (quién es bueno) | solo quien la escribe, y su vigía | **NO. Se toma y se tira** |
| **Mediciones de paquetes** | solo quien las escribe, y vigías | **NO** |
| Tabla de capacidades | el repartidor de cerebros | SÍ |
| Pruebas reales | dos candados | SÍ |

**La más grave es la primera:** la tabla que dice *quién es bueno* (donde uno de los gratis
saca 100%) **no la consulta nadie al repartir trabajo**. Se mide y no se usa. Por eso el
reparto nunca mejora: la información existe y está desconectada.

**Y hay un agravante ya conocido:** esa tabla mide una prueba de **marketing**, no de reparar
código. Así que aunque se conectara, hoy diría una mentira útil.

## Lo reparado el 5 y 6 de septiembre (con prueba)

| Qué | Prueba |
|---|---|
| El repartidor se guiaba por las palabras **"que"** y **"solo"** | ahora dice NO_ENCONTRADO en vez de inventar un tema. Es la causa del 3% |
| El candado de la terminal frenaba lo que solo mira | probado con la misma orden que frenó seis veces: ya pasa |
| El revisor acusaba de inventar a quien decía "no lo encuentro" | reparado y aplicado por el equipo |
| El freno anti-invento impedía crear **cualquier** pieza nueva | reparado: lo que la tarea pide crear ya no es invento |
| El que aplica los cambios aceptaba **humo** | ahora rechaza el cambio que solo toca comentarios |
| Había una segunda copia completa del Ingeniero | retirada: una carpeta y una rama |

## Las siete habilidades que ya no gastan IA

medir al equipo · una sola vía · frenos con culpable · cazar el humo ·
falta en el material · orden o texto pegado · **leyes sin vigía**

---

# EL PLAN NUEVO — CON LAS CINCO RESPUESTAS DE JULIO

Manda [CONTRATO_ANALISIS_DE_FONDO.md](CONTRATO_ANALISIS_DE_FONDO.md): sin las cinco
respuestas no se toca nada. Van por orden: **cada una desbloquea la siguiente**.

## PIEZA 1 — Poder elegir quién escribe

- **QUÉ:** que el mando del equipo acepte a quién se le pide escribir y a quién revisar.
- **DÓNDE:** en el mando `equipo`, donde llama al obrero. El obrero **ya** respeta esos dos
  datos; lo único que falta es que se los pasen.
- **CÓMO:** dos datos más en la llamada. Es fontanería, no juicio: **cuenta, no cerebro**.
- **POR QUÉ ASÍ Y NO DE OTRO MODO:** se descartó (a) medir a los gratis con una prueba
  aparte — no mide trabajo real, es el error que ya se cometió con la tabla de marketing; y
  (b) turnarlos al azar — no se puede repetir ni comparar. Ésta es la única que da un número
  comparable. **Número que lo justifica: los gratis llevan 0 de 72 trabajos reales escritos,
  no por malos sino porque nunca se les pudo pedir.**
- **CUÁNDO:** **la primera**. Sin esto, las piezas 2, 3 y 4 son imposibles de medir.

## PIEZA 2 — Que el medidor mida por TIPO de trabajo

- **QUÉ:** medir a cada cerebro en buscar, resumir, escribir y revisar, con trabajo real de
  código, y guardarlo junto a lo que ya se mide.
- **DÓNDE:** en el medidor de capacidad y en la tabla que ya existe. **No se crea otra tabla.**
- **CÓMO:** se le da a cada uno un encargo real pequeño de cada tipo y **la vigía dice si
  sirvió**, no otro cerebro. Es cuenta, no juicio.
- **POR QUÉ ASÍ:** se descartó seguir con la prueba de marketing (ya está medido que un 100%
  ahí alucinó tres veces reparando) y se descartó preguntarle a un cerebro si el otro lo hizo
  bien (el revisor gratis aprobó dos reparaciones falsas el mismo día).
- **CUÁNDO:** después de la 1.

## PIEZA 3 — Que el repartidor USE lo medido

- **QUÉ:** que el reparto ordene por (tipo de trabajo × capacidad medida × tamaño × coste).
- **DÓNDE:** en la función que ya ordena a los cerebros. **Se amplía, no se duplica.**
- **CÓMO:** leer la tabla nueva antes de elegir. Y **conectar la tabla de precisión, que hoy
  se escribe y nadie lee**.
- **POR QUÉ ASÍ:** es el fallo medido hoy — la información existe y está desconectada.
  Construir un repartidor nuevo sería duplicar una pieza que ya funciona.
- **CUÁNDO:** después de la 2.

## PIEZA 4 — Que un cerebro gratis no pueda firmar un veredicto

- **QUÉ:** una vigía que impida que el "quedó bien" de un cerebro abra la puerta de escribir.
  Verificar = correr la vigía.
- **DÓNDE:** en las vigías, junto al candado del equipo.
- **CÓMO:** se simula un veredicto firmado por un gratis y se comprueba que **no** abre.
- **POR QUÉ ASÍ:** medido el 5 de septiembre — el revisor gratis aprobó **dos veces** una
  reparación que solo cambiaba comentarios.
- **CUÁNDO:** puede ir en paralelo con la 2.

## PIEZA 5 — Vigía para las 13 leyes que son papel

- **QUÉ:** una vigía por cada ley sin vigía, empezando por las cuatro de estos dos días.
- **DÓNDE:** en las vigías. La habilidad **leyes sin vigía** dice cuáles faltan.
- **CÓMO:** cada contrato ya trae escrito su apartado "cómo se comprueba". Se convierte en
  vigía tal cual.
- **POR QUÉ ASÍ:** una ley sin vigía depende de que la IA se acuerde, y eso ya está medido
  que no funciona.
- **CUÁNDO:** en cuanto la 1 permita repartir este trabajo a los gratis: es trabajo
  secundario, real y comprobable por máquina — exactamente lo que la ley manda darles.

## PIEZA 6 — Que el material traiga la pieza que el problema nombra

- **QUÉ:** que el repartidor meta siempre en el material la pieza cuyo nombre aparece en el
  problema.
- **DÓNDE:** en el armado del paquete.
- **CÓMO:** ya existe un bloque que mete lo que el problema nombra **por ruta exacta**; se
  amplía a nombres sueltos. **Se avisa antes de gastar** con la habilidad ya hecha.
- **POR QUÉ ASÍ:** un intento anterior se rechazó **con razón** porque citaba mal una ley. La
  ley de buscar por nombre habla de funciones, no de archivos: esto es una ampliación nueva y
  se justifica sola con el número (dos vueltas perdidas en un día).
- **CUÁNDO:** después de la 3.

---

# LO QUE FALTA Y JULIO NO HA VISTO

1. **El guardián escribe en sus propios cuadernos** mientras comprueba, así que cada guardado
   deja rastro nuevo sin guardar. Es un bucle: nunca queda limpio.
2. **El guardián corre las 566 vigías en cada guardado** (4 minutos y medio). Debería correr
   solo las que tocan lo que cambió. Eso es una cuenta: **habilidad**.
3. **El candado del equipo miente**: su aviso dice que las piezas nuevas se pueden tocar
   siempre, y las frena.
4. **El diccionario tiene 35 palabras y no conoce "skill" ni "habilidad"** — la palabra que
   Julio llevaba repitiendo y no se entendió hasta que la dijo una IA de fuera.
5. **No hay ninguna medida de si Julio pudo trabajar hoy.** Todo mide la herramienta.
6. **Foto Informe tiene 10 ramas de junio** con trabajo que la buena no tiene. Julio dijo:
   para después.

