# PRIORIDAD UNO — Reparar el Ingeniero: que termine, que acierte, rápido y barato

> **APROBADO POR JULIO el 2026-09-25. Es la PRIORIDAD NUMERO UNO.**
> **No se pasa a ninguna otra prioridad hasta que esto esté terminado.**
>
> El estado NO vive en el chat: vive aquí, en `memoria/ORDENES.json` y en `memoria/ESTADO.json`.
> Si una sesión nueva no sabe dónde íbamos, lee este documento y la lista de órdenes.
> Orden de trabajo: R0 → (R1 + R2 a la vez) → 1b → (R3 + R4 + R5) → (R6 + R7) → R8.

## ESTADO AL 2026-09-27 (lo primero que hay que leer al volver)

**Hechas y selladas hoy, cada una con su vigía nacida ROJA y ahora verde:**

| Orden | Qué quedó arreglado |
|---|---|
| R1b + R1c | El guardia ya **no frena por pruebas que estaban rojas de antes**. La pieza `rojas_que_frenan` quedó enganchada dentro de `_vigias`; el fallo estaba en que las declaradas se le pasaban como conjunto y él solo acepta listas, así que las anulaba. El aviso ya nombra la tercera razón. |
| R1d | **La batería corre en paralelo**: pieza nueva `arnes/bateria_en_paralelo.py`, enganchada en el guardia. En fila, las 257 pruebas pasaban de 12 min y se perdió un trabajo aprobado; en 4 grupos termina en un par de minutos. Ya ha dejado guardar varias veces. |
| R5 | **Ningún proceso del capataz sin tope**: los cuatro `subprocess.run` que salían sin tope ya lo llevan, y un cuelgue cuenta como fallo, nunca como aprobado. |
| R4a + R4b | **La misma prueba no se corre dos veces**: pieza `arnes/memoria_de_pruebas.py` y el juez ya la usa. Un apunte rojo nunca se vuelve verde. |
| R3a (a medias) | Techo de espera declarado y respetado por `cuanto_esperarle`. Lo de Big Pickle, ver la decisión de Julio en R3. |

**Cómo funciona ahora el guardado, en corto:** las rojas que ya estaban rojas antes viven en
`memoria/.rojas_conocidas.json` (no se sube al repositorio); el guardia las tolera, y cuando deja
pasar **une** las de ahora con las que ya conocía en vez de borrarlas. Si hoy hay 21 rojas
declaradas, son de antes y están apuntadas.

**Apuntado para después (órdenes nuevas de hoy):** `R4c` (el capataz tampoco repita la corrida),
`R6a` (la roja de `test_vigia_el_loop_del_pit.py` espera R6), `R13` (el paquete no trae el archivo
que se le nombra si la frase es larga: costó tres rondas hoy) y `R14` (una ronda no puede declarar
una constante y usarla a la vez: dejó la herramienta parada un rato).

---

Investigado el 2026-09-25: tres agentes en paralelo + verificación línea por línea hecha por Claude.
**Dos conclusiones mías anteriores resultaron falsas y están corregidas abajo** (marcadas CORRECCIÓN).

---

## Los números que mandan (de la memoria de la herramienta, no de una opinión)

| Qué | Número real | De dónde |
|---|---|---|
| "El guardia no dejó guardar lo que el equipo aplicó" | **82 veces** | `memoria/FALLOS.json` id 69 (el 2º más repetido tiene 5) |
| Trabajos aprobados frenados, aún en el disco | **14** | `memoria/trabajos_sin_revisar/*.FRENADO_POR_EL_GUARDIA` |
| Expedientes con veredicto `no_aprobo` | **40 de 82 (48.8%)** | `memoria/EXPEDIENTES/` |
| Minutos por orden (promedio) | **90.1 min** | `memoria/CUADERNO_DE_LLAMADAS.jsonl` |
| Llamadas a IA por orden | **4.78** (máx 27) | ídem, 165 órdenes |
| Llamadas que acabaron en nada | **20.6%** (206 de 1000) | ídem |
| Big Pickle | **25.9 h quemadas**, 167 s de media, **40.6% falla**, 22.8% timeout | `memoria/BIGPICKLE.log`, 715 llamadas |
| DeepSeek (el de pago) | **5.06 s** de media, **USD 2.79 de 5.00** al mes | `memoria/GASTO_USD.jsonl` |
| Órdenes fallidas | **37 de 197 (18.8%)**; 44 con `fallos_seguidos>0` | `memoria/ORDENES.json` |

**Lo que grita:** lo "gratis" es lo más caro. El de pago contesta en 5 segundos por centavos; el gratis
se comió 26 horas fallando 4 de cada 10 veces — y se le espera **en fila**, uno tras otro
([obrero.py:891](cuerpo/obrero.py#L891)), hasta 600 s cada uno.

---

# R0 · EL CIERRE ATASCADO — se repara PRIMERO

- **QUÉ pasa:** el guardia del cierre reclama "instrucciones de Julio sin asentar" que **no son de
  Julio**: hoy reclama el texto interno de cómo ponerle título corto a una tarea (*"Generate a concise,
  single-line task title…"*, en inglés). Mientras no se asiente, no deja cerrar. Nunca.
- **POR QUÉ pasa (causa exacta, verificada):** el filtro que distingue "lo que pide el programa" de "lo
  que dice Julio" **no lee el texto: confía en una marca de entorno**
  ([candado_legislar.py:194](arnes/candado_legislar.py#L194)): si quien llama no pone
  `INGENIERO_LLAMADA_DEL_PROGRAMA=1`, **todo lo que entra se apunta como orden de Julio**. El texto del
  título llegó sin la marca. Un filtro que depende de que el llamador se acuerde, falla siempre.
- **DÓNDE:** `arnes/candado_legislar.py`, la parte que apunta ([líneas 141-200](arnes/candado_legislar.py#L141-L200)).
- **CUÁNDO:** antes que todo lo demás. Cada cierre bloqueado cuesta vueltas todos los días.
- **CÓMO:** **la ley ya existe y la vigía también** — no se duplica nada:
  `vigias/test_vigia_lo_que_pide_el_programa_no_es_de_julio.py` (Julio, 2026-09-21) ya exige que lo del
  programa no se apunte. Lo que falta es que **no dependa de una marca**: el candado decide por el propio
  texto (idioma, forma de plantilla del sistema, que no venga del chat de Julio).
  1. Ampliar esa vigía con el caso REAL de hoy: el texto del título en inglés, **sin ninguna marca** →
     no se apunta. Nace roja.
  2. El equipo repara el candado hasta ponerla verde.
  3. Limpiar las 5 líneas falsas que hoy están en la lista de pendientes, marcadas "no aplica".

---

# R1 · El trabajo aprobado SIEMPRE llega al disco (la causa nº1: 82 veces)

**CORRECCIÓN de mi diagnóstico anterior:** dije que los apuntes de `memoria/` disparaban la batería
completa. **Es falso**: `_vecinas_por_stem` ignora lo que no es código
([vecinas.py:234](arnes/vecinas.py#L234)). La causa real es otra, y es más simple:

- **QUÉ pasa:** cuando se guarda, se corre una batería de vigías con tope de **15 minutos**; si no
  termina, **no se guarda** ([guardia_de_guardado.py:291-296](arnes/guardia_de_guardado.py#L291-L296)).
  Y hay **245 archivos de vigías, 28.355 líneas**.
- **POR QUÉ se corre todo (dos disparadores verificados):**
  1. **Un archivo de código cambiado que no se menciona en ninguna vigía → se corre TODA la batería**
     ([vecinas.py:244-247](arnes/vecinas.py#L244-L247)). Es prudente, pero con 245 vigías es una
     sentencia de muerte al guardado.
  2. Si cambia `conftest.py` (o `pytest.ini`, `setup.cfg`, `pyproject.toml`) → **toda la batería**
     ([vecinas.py:54-59](arnes/vecinas.py#L54-L59)). Y `conftest.py` **está entre los 14 trabajos
     frenados**: se quiso tocar y el guardado se atascó.
- **DÓNDE:** `arnes/vecinas.py` (a quién se le manda correr) y
  `arnes/guardia_de_guardado.py` (el tope de tiempo).
- **CUÁNDO:** inmediatamente después de R0.
- **CÓMO (sin aflojar el guardia — esto es clave):** el guardia sigue frenando igual las contraseñas y
  las vigías rojas. Solo cambia **a quién se le manda correr y con qué tiempo**:
  1. Batería completa **en paralelo** (varios procesos de prueba a la vez): 28.355 líneas no se corren
     en fila. Mismo rigor, minutos en vez de horas.
  2. El tope de 15 minutos se mide **por lo que se manda correr**, no fijo, y si se agota **el trabajo
     no se pierde**: queda apartado con el motivo exacto y una orden para retomarlo.
  3. Vigía nueva primero (nace roja): `test_vigia_el_guardado_no_muere_por_la_bateria_completa.py`.
- **Extra del mismo paso:** recoger los **14 trabajos aprobados** que llevan días esperando. Es trabajo
  ya pagado. `conftest.py` primero, porque él mismo dispara el atasco.

---

# R2 · Nunca más pagar por una pregunta imposible (el caso del expediente 173)

- **QUÉ:** un guardia de programa que compruebe, **antes de llamar a ninguna IA**, que el material
  lleva el archivo y la función que el encargo nombra.
- **DÓNDE:** `cuerpo/obrero.py`, tres averías verificadas:
  - [obrero.py:1195](cuerpo/obrero.py#L1195): acepta un `.py` suelto de la frase como si fuera un
    archivo → el filtro deja de filtrar.
  - [obrero.py:399-413](cuerpo/obrero.py#L399-L413): el recortador borra bloques desde el final **a
    ciegas** y se lleva justo la función pedida.
  - [obrero.py:300](cuerpo/obrero.py#L300) + [obrero.py:1222-1227](cuerpo/obrero.py#L1222-L1227):
    "falta material" se confunde con "la IA trabajó a medias" → reintenta y escala al de pago.
- **POR QUÉ:** `no_aprobo` es el 48.8% de los expedientes. En el 173 se preguntó 3 veces por
  `_prompt_obrero` sin mandar nunca el código; la función existe en [obrero.py:73](cuerpo/obrero.py#L73).
- **CUÁNDO:** a la vez que R1 (archivos distintos, no se pisan).
- **CÓMO:** vigías primero: `test_vigia_el_material_trae_la_pieza_pedida.py`,
  `test_vigia_el_punto_py_suelto_no_es_un_archivo.py`,
  `test_vigia_falta_material_no_llama_al_de_pago.py`.

---

# R3 · Velocidad: preguntar a la vez, no en fila

- **QUÉ:** (a) a los cerebros lentos se les pregunta **al mismo tiempo** y gana el primero que
  contesta; (b) a quien falla 4 de cada 10 veces no se le espera 600 s.
- **DÓNDE:** [obrero.py:891](cuerpo/obrero.py#L891) (`for quien in turnos` → en paralelo),
  [bigpickle.py:41](cuerpo/bigpickle.py#L41) (`TIMEOUT_POR_DEFECTO=600`),
  [cuotas.py:52](cuerpo/cuotas.py#L52) (el orden de la fila).
- **POR QUÉ:** 90 min por orden; 26 horas esperando a un gratis que falla el 40%.
- **CUÁNDO:** tras R1 y R2.
- **CÓMO:** vigía `test_vigia_se_pregunta_a_los_lentos_a_la_vez.py`; se mide con los segundos que ya
  guarda `memoria/CUADERNO_DE_LLAMADAS.jsonl`.

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
  el proceso contesta, y el tope solo es el máximo; al agotarse, el turno pasa al siguiente cerebro.
- **FALTA:** que `espera_de_bigpickle` respete `TECHO_ESPERA`, y bajar `TIMEOUT_POR_DEFECTO` de
  `cuerpo/bigpickle.py` de 600 a 400.
- **FALTA, y ahora SÍ está permitido:** reescribir `vigias/test_vigia_a_big_pickle_se_le_espera_lo_que_tarda.py`
  (orden A-47, 2026-09-21), cuyo caso "sin filas se espera el valor por defecto" exige 600. Se
  reescribe **con esta decisión de Julio anotada como razón**, no por conveniencia.
- **FALTA:** en `vigias/test_vigia_a_nadie_se_le_espera_mas_de_lo_medido.py`, los dos casos de Big
  Pickle piden 300 y tienen que pedir 400.

# R4 · La misma prueba no se corre cuatro veces

- **DÓNDE:** hoy corre en `arnes/juez_de_la_prueba.py` (desde [obrero.py:1268](cuerpo/obrero.py#L1268),
  hasta 3 corridas × 3 vecinas), otra vez en [capataz.py:973](cuerpo/capataz.py#L973), y otra en
  [capataz.py:548-553](cuerpo/capataz.py#L548-L553). Tope 300 s cada una.
- **CÓMO:** guardar el resultado con la huella del archivo probado y reusarlo mientras no cambie.

# R5 · Dos cuelgues sin tope (la causa de los fallos "tiempo")

- **DÓNDE:** [capataz.py:973](cuerpo/capataz.py#L973) y [capataz.py:1018](cuerpo/capataz.py#L1018):
  dos subprocesos **sin `timeout`**, contra la regla que el propio archivo declara
  ([capataz.py:9-13](cuerpo/capataz.py#L9-L13)). Un guardado ya se colgó 5 h 30
  ([guardia_de_guardado.py:272-274](arnes/guardia_de_guardado.py#L272-L274)).

# R6 · Varias órdenes a la vez, cada una en su copia

- **DÓNDE:** el motor ya está listo ([capataz.py:334](cuerpo/capataz.py#L334)); está frenado en
  [capataz.py:303](cuerpo/capataz.py#L303) (`en_paralelo=1`) y en [ingeniero.py:560](ingeniero.py#L560).
- **POR QUÉ frena hoy:** medido el 2026-09-21
  ([test_vigia_el_pit_corre_una_tarea_a_la_vez.py:9-17](vigias/test_vigia_el_pit_corre_una_tarea_a_la_vez.py#L9-L17)):
  dos tareas comparten carpeta y "el guardia de una ve el trabajo a medias de la otra".
- **CÓMO:** copia temporal por orden (`git worktree`), borrada al terminar — nunca copias sueltas en el
  disco. Dos permisos que se piden, no se rodean: reescribir esa vigía con su razón, y legislar la
  excepción a `CONTRATO_UNA_SOLA_VIA.md`. Sigue prohibido dos órdenes de la misma pieza a la vez.

# R7 · Que la llave abra solo lo que hace falta (la ley de la llave única, hoy incumplida)

- **QUÉ pasa:** `autorizada()` **no recibe ningún argumento**
  ([autorizacion.py:80-87](arnes/autorizacion.py#L80-L87)): es un interruptor **todo-o-nada**. Girar la
  llave apaga **los 27 guardias de golpe**, incluido el que obliga a trabajar con el equipo.
- **POR QUÉ importa:** la ley de la llave única (2026-08-27) dice que se abren **solo** los candados que
  la tarea necesita. Hoy el código no puede cumplirla.
- **CÓMO:** que la autorización diga **qué** se abre y por cuánto; cada guardia pregunta por su nombre.
  Vigía: `test_vigia_la_llave_abre_solo_lo_pedido.py`.
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
| material mínimo | `trabaja` |
| causa de fondo | `causa` |
| qué herramienta falta / crearla | `skills.buscar` ([skills.py:118](cuerpo/skills.py#L118)), `skills.crear` ([skills.py:167](cuerpo/skills.py#L167)) |
| plan → órdenes | `director.orden_nueva` ([director.py:215](cuerpo/director.py#L215)) |
| correrlas solas | `capataz.bucle` ([capataz.py:303](cuerpo/capataz.py#L303)) |
| aprender del fallo | `capataz.forense` ([capataz.py:803](cuerpo/capataz.py#L803)) |

---

## ¿La herramienta deja hacer estas reparaciones? (verificado, no supuesto)

| Riesgo | ¿Bloquea? | Prueba |
|---|---|---|
| Los archivos a tocar disparan la batería completa | **No** | La lista que obliga todas es solo `conftest.py`, `pytest.ini`, `setup.cfg`, `pyproject.toml` ([vecinas.py:54-59](arnes/vecinas.py#L54-L59)) |
| Quedan sin vigía vecina (→ batería completa) | **No** | Ya existen `test_vigia_vecinas.py`, `…el_obrero_…`, `…el_capataz_…`, `…el_guardia_…` |
| El equipo no puede escribir en los candados | **No** | Entre los trabajos aprobados hay `candado_equipo.py`, `candado_legislar.py`, `guardia_de_guardado.py` |
| **Huevo y gallina en R2** | **SÍ, riesgo real** | Para arreglar el filtro del material hay que mandarle al equipo la función **pegada dentro del encargo** (`piezas.funcion_completa`), o fallará igual que el 173 |
| `cuerpo/obrero.py` es el archivo más grande (76 KB) | **SÍ, riesgo real** | Encargos **por función**, nunca por archivo entero |
| Tocar `conftest.py` (uno de los 14 frenados) | **SÍ** | Dispara batería completa: va **después** de R1, nunca antes |

## Permisos: qué se abre, cuándo y por qué

Estado real: la última autorización es del **2026-09-18 12:43** y dura **24 horas**
([autorizacion.py:27](arnes/autorizacion.py#L27)) → **caducada; los guardias están cerrados hoy**.
La llave de Julio existe (`~/.ingeniero_julio_llave`) y solo él la gira.

**Este plan está hecho para NO necesitar la llave** en R0-R5: se trabaja con paquete mínimo y con el
equipo, que es el camino legal. La llave solo hace falta en dos momentos, y se pide en el momento:
1. recoger algunos de los 14 trabajos frenados, si el guardado los vuelve a frenar;
2. reescribir la vigía que prohíbe el paralelo (R6).

**Advertencia que hay que decirle a Julio antes de que la gire:** hoy la llave **abre los 27 guardias
de golpe**, incluido el que obliga a trabajar con el equipo. O sea, girarla abre la puerta de atrás que
él mismo prohibió. Por eso R7 está en el plan, y por eso no se gira "por si acaso".

Comando (PowerShell), cuando de verdad haga falta:
```
cd C:\Ingeniero_VUC; python ingeniero.py autorizar-off "<motivo en una frase>" "<su llave>"
```

## Siempre con el equipo, sin puerta trasera (garantizado por máquina, no por promesa)

- Cualquier escritura de código sin veredicto de equipo la frena `arnes/candado_equipo.py`
  ([líneas 463-478](arnes/candado_equipo.py#L463-L478)), y el interruptor viejo **ya no basta**: queda
  anotado como intento y sigue frenando.
- La IA que dirige **no escribe código**, ni con permiso (`CONTRATO_LA_IA_CARA_NUNCA_ESCRIBE.md`).
- Ninguna reparación de este plan afloja eso. R1 no toca lo que el guardia frena (contraseñas, vigías
  rojas): solo cambia **a quién manda correr** y **cuánto espera**.
- Único hueco conocido: girar la llave (ver arriba) lo abriría. Se repara en R7.

## Orden de trabajo

| Ronda | Qué | ¿A la vez? |
|---|---|---|
| 0 | R0 el cierre atascado | primero, solo |
| 1 | R1 el trabajo se queda **+** R2 el material completo | **sí** (piezas distintas) |
| 1b | Recoger los 14 trabajos frenados (`conftest.py` incluido) | tras R1 |
| 2 | R3 preguntar a la vez + R4 una sola prueba + R5 los dos topes | sí |
| 3 | R6 varias órdenes a la vez + R7 la llave por partes | después |
| 4 | R8 el comando que arma el plan | último |

## Cómo se ejecuta cada ronda (siempre igual, sin excepción)

1. `python ingeniero.py trabaja ingeniero "<la avería>"` — el paquete mínimo.
2. `python ingeniero.py vigias ingeniero antes` — de qué color están antes.
3. **La vigía primero, y tiene que nacer ROJA** (`.claude/rules/vigias.md`).
4. **El equipo escribe el código.** El encargo lleva la función **pegada dentro**.
5. `python ingeniero.py vigias ingeniero despues` — no romper vecinos.
6. Legislar y sellar con `git commit`.
7. Julio lo ve con sus ojos.

## Por qué esta vez no falla

1. Cada reparación nace de un número de la propia herramienta: 82, 14, 90 min, 40.6%, 48.8%.
2. Cada una tiene su vigía escrita antes, y roja. Si nace verde, no probó nada.
3. Cada una tiene medición antes y después, con los archivos que ya llevan la cuenta.
4. Se repara primero lo que hacía fracasar a todo lo demás: el cierre atascado y el guardado que tira
   el trabajo aprobado.
5. Dos conclusiones mías ya se cayeron al verificarlas en el código (los apuntes de `memoria/` y la
   causa de la batería completa). Están corregidas arriba. Se verifica antes de afirmar.
6. El plan no vive en el chat: queda como documento en la carpeta, apuntado en la hoja de leyes, y
   convertido en órdenes con dependencias.

## Cómo se sabrá que sirvió

| Medida | Hoy | Meta |
|---|---|---|
| Cierres bloqueados por "instrucciones que no son de Julio" | todos los días | **0** |
| "El guardia no dejó guardar" | 82 veces | **0 nuevas** |
| Trabajos aprobados sin llegar al disco | 14 | **0** |
| Minutos por orden | 90.1 | **menos de 20** |
| Llamadas a IA por orden | 4.78 | **menos de 2.5** |
| Llamadas que acaban en nada | 20.6% | **menos de 5%** |
| Órdenes a la vez | 1 | **3-4** |
| Orden 173-F064924 | muere sin veredicto | **cerrada en 1 ronda** |

---

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
