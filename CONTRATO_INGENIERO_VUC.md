# CONTRATO — INGENIERO VUC (la constitucion de esta herramienta)
> Julio (2026-08-20): "necesito una red neuronal tipo Obsidian que solo le de lo necesario del codigo
> a la IA, para no volver a leerlo todo y no gastar token a lo pendejo". Este contrato es la ley de
> esa herramienta. Nace de `CONTRATO_MAESTRO_AHORRO.md` y `CONTRATO_AHORRO_DE_TOKENS.md` de DMM.

## LEY 0 — QUE ES Y DONDE VIVE
- El Ingeniero vive en `C:\Ingeniero_VUC`. **No pertenece a ningun proyecto.**
- Atiende a los proyectos declarados en `proyectos.config`. Para atender uno nuevo: una linea mas.
- Se enchufa a un proyecto con `python arnes/instalar.py <apodo>` y se desenchufa con `--quitar`.

## LEY 1 — NO SE LEE EL PROYECTO, SE LEE EL PAQUETE
- Todo trabajo empieza con `python ingeniero.py trabaja <proy> "<problema>"`.
- El paquete es TODO el material permitido. Lo que falte se PIDE con `NECESITO_LEER`.
- **Candado:** `arnes/read_gate.py` (hook PreToolUse). Bloquea abrir entero cualquier archivo de mas
  de 300 lineas que el paquete no declare. La documentacion oficial es clara: el CLAUDE.md es
  contexto, **el hook es lo que obliga**.
- **Vigia:** `vigias/test_vigia_paquete_no_lee_repo_entero.py` (tope 400 lineas, ahorro minimo 90%).

## LEY 2 — LAS 4 CAPAS DEL CEREBRO (ninguna se elimina)
| Capa | Pieza | Que aporta |
|---|---|---|
| 1 FLUJOS | `cerebro/flujos.py` | junta por ASUNTO lo que el texto no enlaza |
| 2 PIEZAS | `cerebro/piezas.py` | la ficha de cada archivo (que es, que boca tiene) |
| 3 TROZOS | `cerebro/trozos.py` | el pedazo exacto `archivo:desde-hasta` (el "chunk") |
| + HILOS | `cerebro/enlaces.py` | quien toca a quien, CON FUERZA |
| = GRAFO | `cerebro/grafo.py` | las junta y se acuerda (cache por huella) |
| = BOCA | `cerebro/router.py` | entrega el paquete minimo |
- Regla dura: **ninguna capa se elimina** sin actualizar este contrato y su vigia.

## LEY 3 — NUNCA ASUMIR, NUNCA INVENTAR
- Lo que el contrato no decide: `PREGUNTA_REQUERIDA:` y se le pregunta a Julio. No se adivina.
- Lo que no existe en disco: `NO_ENCONTRADO`. Jamas se rellena con algo verosimil.
- **Vigia:** `vigias/test_vigia_no_inventa.py` (todo lo que el paquete nombra debe existir; las
  lineas de los trozos deben caber en el archivo real).

## LEY 4 — NO REPARAR ALGO Y DANAR LO OTRO
- Todo paquete lleva la seccion "A QUIEN PUEDE DANAR" (los vecinos del grafo por IMPORTA/VIGILA).
- Antes de sellar se declara cual de esos vecinos se reviso.
- **Vigia:** `vigias/test_vigia_cross_flow.py`.

## LEY 5 — VIGIA VERDE NO ES PRUEBA
- La prueba es que **Julio lo vea funcionar con sus ojos**. `ESTADO.json` guarda `prueba_humana`
  y solo Julio la pone en HECHA. Ninguna IA la marca por su cuenta.
- **Meta-prueba (leccion de DMM LEY 5):** al tocar un candado hay que **sabotearlo a proposito** y
  comprobar que la vigia se pone ROJA. Un candado fantasma es peor que ninguno.

## LEY 6 — NO REPETIDERA
- Antes de crear una pieza se busca en `mapa/MAPA_INGENIERO.json` si ya existe.
- Antecedente real: `C:\vigias` tenia 52 vigias duplicadas; se comprobo una por una, se rescataron
  las 2 pruebas unicas a `memoria/rescate/` y el resto se desecho el 2026-08-20.
- **Vigia:** `vigias/test_vigia_no_repetidera.py`.

## LEY 7 — QUE JULIO NO REPITA
- El estado NO vive en el chat: vive en `memoria/ESTADO.json`. `python ingeniero.py arranca` dice
  donde ibamos y cual es el siguiente paso, aunque se cierre la sesion o se acabe el saldo.
- A Julio se le habla simple, sin jerga, y el comando siempre listo para PowerShell (`;`, no `&&`).

## ESTADO HONESTO (2026-08-20)
- Hecho y probado: mapa, las 4 capas, router, candado de lectura, instalador, ESTADO, 7 vigias.
- Probado contra si mismo y contra DMM/Foto Informe: ahorro 99.0% y 99.4%.
- **Falta la prueba de Julio.** Hasta que el lo vea, esto NO esta certificado.

---

# AMPLIACION (Julio, 2026-08-20, segunda tanda de ordenes)

## LEY 8 — NADIE SE AUTOVALIDA (vigia cruzada)
- El que REPARA no escribe la prueba. Otro cerebro escribe la vigia **a ciegas**, sin ver la
  reparacion, y un tercero juzga si la reparacion pasa esa vigia.
- Motivo: si el mismo repara y prueba, escribe la prueba que su reparacion pasa. Verde de mentira.
- **Pieza:** `cuerpo/cruzado.py`. **Vigia:** el propio ciclo deja constancia de quien hizo que.
- El juez pregunta siempre: ¿invento algo? ¿pasa la vigia de verdad? ¿ataca la CAUSA RAIZ o tapa
  el sintoma? Si rechaza, se reintenta con lo aprendido, hasta 3 rondas.

## LEY 9 — NADA LENTO
- Ningun proceso hace esperar a Julio. Topes: **120s por llamada**, **300s el ciclo entero**.
- Medido el 2026-08-20 con un paquete de 388 lineas:
  `qwen3.6-27b` >300s TIMEOUT · `llama-3.3-70b-versatile` 30s · `gemini-2.0-flash` 40s.
- **Pieza:** `arnes/velocidad.config`. **Vigia:** `test_vigia_nada_lento.py`, que se pone ROJA si
  alguien vuelve a poner un modelo de los lentos.
- Lo que no depende uno de otro va EN PARALELO (reparador y vigilante a la vez).

## LEY 10 — EL RELEVO DE CEREBROS (critico)
- Orden textual de Julio: "gaste los token gratis de Qwen y despues los de gemini, cuando se
  repongan los de Qwen continue con el".
- Lo critico no es cambiar de cerebro: es **VOLVER** al primero cuando repone.
- **Pieza:** `cuerpo/cuotas.py`. **Vigia:** `test_vigia_relevo_cuotas.py`.
- "Lento" NO es lo mismo que "agotado": tardar una vez no manda a nadie a dormir una hora.
- En el trabajo cruzado los cerebros SE REPARTEN: si compiten por el mismo, se bloquean entre si.

## LEY 11 — MEMORIA DE FALLOS
- Todo fallo real se apunta con: que paso · causa raiz · como se curo · **QUE NO VOLVER A HACER**.
- Antes de reparar, el paquete avisa si ya se tropezo con esa piedra.
- **Pieza:** `cuerpo/fallos.py` -> `memoria/FALLOS.json`. No se borra nada: lo viejo sigue enseñando.

## LEY 12 — NADA SE DA POR HECHO SIN MIRAR EL DISCO
- Cada orden de Julio vive en `ORDENES.md`, textual, con su comprobacion.
- `verificar.py` la comprueba una por una contra el disco. Nadie puede decir "ya esta" sin prueba.
- Lo que solo Julio puede dar por bueno sale marcado `[JULIO]` y **ninguna IA lo marca jamas**.
- **Comando:** `python ingeniero.py verificar`

## LEY 13 — EL VOLUMEN NO ENTRA EN LA VENTANA DE CLAUDE
- El trabajo pesado corre en proceso APARTE (`cuerpo/subagentes.py`): se traga las 20.000 letras
  del paquete y devuelve ~600 de veredicto. Claude decide igual de bien viendo el 3%.
- Si el proceso aparte se cuelga, NO se lleva por delante la sesion de Julio.

## LEY 14 — LA VIA CANONICA ES LO PRIMERO (Julio, 2026-08-20)
> "que todas las rutas, ramas, vias canonicas, siempre se cumplan, que sea lo primero que
>  verifique el ingeniero, que este trabajando donde debe, no en una version equivoca,
>  y que guarde alli sus commit"

- **Antes de tocar nada** se comprueba: la ruta declarada existe · esta en la RAMA declarada ·
  no hay copias mas nuevas del mismo proyecto por el disco · no quedan cambios sin guardar.
- **Una ruta y una rama por proyecto**, declaradas en `proyectos.config`. Sin rama declarada,
  no se trabaja: los commits acabarian en cualquier parte.
- **Si la copia declarada es mas VIEJA que otra que hay en el disco -> BLOQUEO.** Reparar en la
  copia equivocada es tirar el trabajo a la basura.
- **Pieza:** `arnes/via_canonica.py` · **Vigia:** `test_vigia_via_canonica.py` (meta-probada:
  al apuntar a la copia vieja se pone ROJA).
- **Donde actua:** en el mando (antes de `trabaja`, `resolver`, `cruzado`, `vigias`, skills),
  en `ingeniero.py arranca`, y en el hook que se mete en CADA mensaje de Julio.
- **Comando:** `python ingeniero.py via`
- **Los commits se guardan en la rama canonica**, y `sellar.sh` lo hace cumplir.

### FALLO REAL que la motiva (2026-08-20)
El propio Ingeniero apuntaba a `C:\MVP\Foto_informe--main` (rama `main`, ultimo commit
**28 de mayo**, 57 archivos) habiendo en `C:\Users\USER\dev\Foto_info_repo\Foto_informe--main`
la version del **23 de julio** con 253 archivos. **Todas las pruebas del router se hicieron
contra una copia dos meses vieja.** Nadie se dio cuenta hasta que Julio pidio esta ley.

## LEY 15 — LO QUE NO SE PUEDE COMPROBAR, NO ESTA GARANTIZADO (Julio, 2026-08-20)
> "Como hacemos para que lo que no se garantiza ahora, sea una garantia?"

**El principio:** una regla escrita se ignora; una comprobacion que BLOQUEA, no. Para convertir
una promesa en garantia hay que encontrarle una comprobacion mecanica que la haga cumplir.
Si no se le encuentra, **se dice que NO esta garantizada**. No se promete.

### Las garantias, y donde vive cada una
| Promesa | Candado que la hace cumplir | Puesto |
|---|---|---|
| No leer archivos grandes | `arnes/read_gate.py` | PreToolUse:Read |
| No tocar codigo a ciegas, en NINGUN proyecto | `arnes/edit_gate_universal.py` | PreToolUse:Edit\|Write |
| No terminar con pasos saltados | `arnes/candado_cierre.py` | **Stop** |
| No seguir a ciegas tras perder el hilo | `arnes/candado_contexto.py` | **PostCompact** |
| No trabajar en la copia o rama equivocada | `arnes/via_canonica.py` | mando + cada mensaje |
| No sellar con una vigia roja | `sellar.sh` | al sellar |

### Reglas de todo candado (sin excepcion)
1. **Tiene que morder:** se sabotea a proposito y se comprueba que se pone ROJO.
2. **No puede dejar atrapado a Julio:** todo candado que bloquea lleva salida (tope de bloqueos
   seguidos) y el interruptor `INGENIERO_OFF=1`.
3. **No estorba lo que debe fluir:** documentos, contratos y vigias se escriben siempre libres.
4. **Comprueba el HECHO, no la palabra:** se mira el disco, no se cree lo que alguien diga.

### LO QUE SIGUE SIN GARANTIA (y se dice, no se disimula)
- **Rapidez de los cerebros gratis:** es de servidores ajenos (5 a 305 s medidos). Lo unico
  garantizable es que **no hagan esperar a Julio** (proceso aparte, `subagentes.lanzar_al_fondo`).
- **Entender al 100%:** ninguna IA puede garantizarlo. Lo que si se hace: preguntar cuando el
  contrato no decide, y que el candado de cierre no deje terminar con la pregunta sin hacer.
- **Que la reparacion sea la correcta:** por eso existen los 4 ojos, el juez y la Ley 5
  (vigia verde NO es prueba; la prueba es que Julio lo vea).

## LEY 16 — BUSCAR PRIMERO, PREGUNTAR SIEMPRE (Julio, 2026-08-20)
> "No me puedes entender al 100%, pero si puedes hacer preguntas que te lleven a esa
>  comprension. Legisla que siempre las hagas, pero que primero busque en los repositorios
>  la respuesta; solo cuando no la halle, pregunte. Siempre debe hacerlas, aun mas si pierde
>  el contexto."

**El orden no se salta:**
1. **Contratos** — ¿ya esta legislado? Si lo dice la ley, no se pregunta.
2. **Memoria de fallos** — ¿ya tropezamos aqui? Lo aprendido vale mas que una opinion nueva.
3. **Codigo** — ¿lo responde una pieza que ya existe?
4. **Estado** — ¿lo decidimos hace un rato y se olvido?
5. **Y SOLO ENTONCES** — se le pregunta a Julio, en palabras simples, diciendole **donde se
   busco ya**. Preguntar sin haber buscado le hace perder el tiempo; callarse la duda es peor,
   porque ahi es donde se asume.

**El ultimo filtro es un JUEZ, no un buscador.** Un buscador por palabras no puede saber si un
texto RESPONDE una pregunta: solo sabe si las palabras aparecen. Por eso, tras encontrar
candidatos, un cerebro GRATIS dice cual responde de verdad (~3 s, cero dinero, poco material).
**Si no hay cerebro disponible, se elige el lado seguro: preguntarle a Julio.**

- **Pieza:** `cuerpo/dudas.py` · **Comando:** `python ingeniero.py duda "<lo que no se>"`
- **Vigia:** `test_vigia_dudas.py` — prueba sobre todo que **NO de por resuelta** una duda que
  no esta escrita. Dar por buena una respuesta que no lo es es peor que preguntar de mas.
- **Candado:** la pregunta se apunta en `ESTADO.json` y `arnes/candado_cierre.py` **no deja
  terminar el turno** mientras siga sin hacerse. Asi no se pierde ni "se olvida".
- **Tras perder el contexto se pregunta mas, no menos** (Ley 15 + esta).

### El error que se cometio TRES veces el mismo dia
Buscador de habilidades, buscador de trozos y buscador de dudas: los tres dijeron "ya existe"
sobre algo que no existia. **Causa unica: cualquier texto "se parece" si no se exige la palabra
que de verdad distingue.** Cura unica y ya compartida: `Buscador.buscar_estricto()`.

## LEY 17 — MEDIR EL ACIERTO, NO SOLO EL AHORRO (Julio, 2026-08-20)

Se podia decir "ahorra el 99%" porque se conto. **No se podia decir "acierta el X%" porque nunca
se midio.** Y el paquete FALLABA: traia el motor y no la pantalla, y lo cazaron dos modelos
gratis, no las 26 vigias verdes. Sin medir, todo lo demas es fe.

### 1. Medir el acierto — `cuerpo/medidor.py`
Cada paquete queda apuntado con lo que trajo. Despues se deduce si SIRVIO, **sin molestar a
Julio**, por las señales que deja el propio trabajo:
| Señal | Veredicto |
|---|---|
| el obrero pidio `NECESITO_LEER` | **CORTO** (el paquete no traia lo necesario) |
| el obrero contesto `NO_ENCONTRADO` | **CORTO** |
| el juez APROBO | **SIRVIO** |
| el obrero se invento algo | **SOSPECHOSO** |
| falto que Julio decidiera | **FALTO_DECISION** (no es culpa del paquete: no cuenta) |
| Julio marco la prueba humana | **el unico acierto que vale** (Ley 5) |
- Comando: `python ingeniero.py medir` · Solo Julio: `python ingeniero.py probado <proy> "<problema>"`
- **Vigia:** `test_vigia_medidor.py`, meta-probada: al hacer que un paquete CORTO se apunte como
  que SIRVIO, se pone ROJA. Un medidor que siempre dice "bien" da tranquilidad falsa.

### 2. Aprender — el medidor apunta **QUE** falto, no solo que fallo
### 3. El router se corrige solo — `cerebro/router.py` lee `medidor.lo_que_falto()` y mete esa
pieza en los paquetes del mismo flujo. **Medir sin corregir no sirve de nada.**

### 4. Buscar por SIGNIFICADO — `cerebro/semantico.py`
Contar palabras no entiende sinonimos: el contrato dice "perfil" y el codigo "onboarding".
Medido con dos frases que dicen lo mismo con otras palabras, contra una que no viene al caso:
- LM Studio (nomic-embed local): **0.022** de diferencia -> NO distingue. **Descartado.**
- `gemini-embedding-001`: **0.202** de diferencia -> SI distingue. **Elegido.**
No se indexa el proyecto entero (600 llamadas): se **re-ordenan** los candidatos que ya trajo el
buscador de palabras (1 llamada). Con cache: un texto se paga UNA vez.
- Apagarlo sin tocar codigo: `$env:INGENIERO_SIN_SIGNIFICADO=1`
- **Vigia:** `test_vigia_semantico.py` — vigila sobre todo que **sin llave, sin cuota o sin
  internet el Ingeniero siga funcionando**. Una mejora que puede dejarlo sin buscador no es mejora.

### 5. Cobertura — ya estaba hecha
El candado global cubre TODOS los proyectos declarados. Comprobado el 2026-08-20: DMM y Foto
Informe protegidos para editar; los archivos de mas de 300 lineas, tambien para leer.

## LEY 18 — NO BASTA CON RESPONDER: HAY QUE EVALUAR SI LA RESPUESTA SIRVIO
> Julio, 2026-08-20: "No solo que se respondio, despues falta evaluar si fue correcta la
>  respuesta, de lo contrario de nada sirve"

Es el error de siempre con otra cara: dar por buena una respuesta **solo porque existe** es lo
mismo que dar por probada una reparacion **solo porque la vigia esta verde**.

**LA SEÑAL OBJETIVA** (la que Julio lleva repitiendo desde el primer dia):
> **Si Julio tiene que repetir la instruccion, la respuesta NO sirvio.**

Eso se mide sin opinar. Cada pregunta se guarda con su respuesta y nace `PENDIENTE`. Si vuelve
a aparecer una pregunta parecida, la anterior queda marcada `NO_SIRVIO` **sola**.

| Forma de evaluar | Fiabilidad |
|---|---|
| Automatica: la pregunta vuelve -> NO_SIRVIO | objetiva |
| Por el trabajo: se hizo y las vigias quedaron verdes | probable |
| **De Julio**: `respuesta-ok` / `respuesta-mal` | **la unica que zanja** (Ley 5) |

- **Pieza:** `cuerpo/respuestas.py` -> `memoria/RESPUESTAS.json`
- **Comandos:** `python ingeniero.py respondio "<pregunta>" :: "<lo que dijo Julio>"` ·
  `respuesta-ok` / `respuesta-mal` · se ve todo con `python ingeniero.py medir`
- **Vigia:** `test_vigia_respuestas.py`, meta-probada (al desactivar la deteccion de
  repeticion se pone ROJA).
- **EL NUMERO QUE IMPORTA:** *"veces que Julio repitio"*. **Si ese numero sube, el sistema esta
  fallando**, por muchas vigias verdes que haya.

### Y el hueco que lo destapo
El candado de cierre bloqueaba por preguntas YA respondidas, y no habia forma honrada de
cerrarlas salvo apagar el candado entero. **Un candado sin manera legitima de satisfacerlo
empuja a saltarselo, y eso es peor que no tenerlo.** Cura: `cuerpo/estado.respondida()`.

### LEY 18-bis — "HAY QUE ACLARARLO" NO ES "NO SIRVIO" (Julio, 2026-08-20)
> "No lo marques como una respuesta que no sirvio, sino como una que debe ser aclarada, que es
>  muy diferente: se trata solo de argumentar de manera diferente, no que no sirva."

Son **tres cosas distintas** y se arreglan de forma distinta:

| Estado | Que paso | Que hay que cambiar |
|---|---|---|
| `SIRVIO` | correcta y entendida | nada |
| `ACLARAR` | **correcta, pero mal explicada** | la EXPLICACION, no el fondo |
| `NO_SIRVIO` | equivocada o no resolvia | la RESPUESTA |

**Confundir ACLARAR con NO_SIRVIO hace que el sistema aprenda al reves:** daria por erroneo algo
que era correcto, y se acabaria cambiando lo que ya estaba bien.

Por eso el informe separa dos numeros que antes iban juntos:
- **CONTENIDO acertado** — las de `ACLARAR` cuentan como acertadas: el fondo era bueno.
- **ME EXPLIQUE MAL** — mide solo la forma. **Este numero es del Ingeniero, no de Julio.**

- **Comando:** `python ingeniero.py respuesta-aclarar "<la pregunta>"`
- **Vigia:** `test_vigia_respuestas.py` — comprueba que `ACLARAR` no baja el acierto y que
  `NO_SIRVIO` si lo baja.

## LEY 19 — EL PROTOCOLO DE JULIO SE CUMPLE SOLO, NO DE MEMORIA (2026-08-20)
> "Falta que actues segun protocolos, ya eso lo he dicho miles de veces... crea los putos
>  disparadores, lo que tengas que hacer."

**El protocolo YA existia** (`PROTOCOLO_DEL_CHAT.md`, Julio 2026-07-28) y aun asi se incumplio
todo el dia. El fallo no era que faltara la ley: era que **nada obligaba a cumplirla**.

### La leccion del dia, en una linea
**Lo que se ejecuta solo, se cumple. Lo que depende de que alguien se acuerde, no se cumple.**
Quedo demostrado con las dos mitades del mismo dia:
| Se ejecuta solo (disparadores) | Depende de acordarse |
|---|---|
| lectura, edicion, contexto, via canonica | buscar en el contrato antes de preguntar |
| **frenaron 4 veces, funcionaron** | **se incumplio 3 veces** |

### Los disparadores del protocolo (`arnes/candado_protocolo.py`)
1. **¿Julio esta repitiendo?** — en cada mensaje suyo se compara con lo que ya habia dicho. Si
   repite, avisa EN EL MOMENTO y lo cuenta solo. Antes el contador marcaba **CERO habiendo
   repetido cuatro veces el mismo dia**, porque habia que subirlo a mano.
2. **Jerga prohibida** — se revisa la respuesta ANTES de que le llegue a Julio. Si lleva nombres
   de archivos o palabras de informatica, no se puede terminar. (LEY DURA de lenguaje simple:
   Julio no es tecnico y lo ha repetido muchas veces, con enojo.)
3. **Confirmar el objetivo antes de construir** — no se crea nada nuevo sin haberle repetido con
   palabras propias el RESULTADO que quiere y haber esperado su "si".
4. **No preguntarle lo que ya escribio** (`arnes/candado_preguntar.py`) — antes de que le llegue
   una pregunta, se busca en sus contratos. Si esta escrito, bloquea y manda a leerlo.

- **Vigia:** `test_vigia_protocolo.py` (11 pruebas). Comprueba que muerden Y que no atrapan:
  ninguno bloquea mas de dos veces seguidas y todos se apagan con `INGENIERO_OFF=1`.
- **Regla dura:** toda ley nueva nace con su disparador. **Una ley sin disparador no es una ley,
  es un deseo.**

## LEY 20 — HAY UN SOLO PROTOCOLO, Y CADA PASO LLEVA CANDADO (Julio, 2026-08-20)
> "Busca en DMM el metodo de trabajo completo... ahora lo del protocolo del MVP, comparalos y
>  haz uno solo unificado, mapa de la forma de trabajo, legislala y pon los candados, de manera
>  que en tu vida los vuelvas a violar."

El documento es `PROTOCOLO_UNICO.md`. Une lo que ya estaba escrito y disperso:
| Fuente | Aporta |
|---|---|
| `PROTOCOLO_DEL_CHAT.md` (DMM, 2026-07-28) | como se responde |
| `PROTOCOLO_MVP.md` (= "protocolo rv3:") | como se repara |
| `CLAUDE.md` § "protocolo rv2:" | el NORTE: consolidar a una sola version |
| `CLAUDE.md` § punto de retomada | donde ibamos |
**RV1 no existe escrito** (se busco el 2026-08-20). No se inventa: si Julio se referia a algo
anterior, se le pregunta.

### Los 8 pasos y su candado (ninguno se salta)
| Paso | Candado |
|---|---|
| 1 ¿Estoy donde debo? | `arnes/via_canonica.py` |
| 2 Buscar solo lo necesario, en orden | `arnes/read_gate.py` |
| 3 Causa raiz, nunca sintoma | `arnes/candado_diagnostico.py` |
| 4 Agotar las fuentes antes de preguntar | `arnes/candado_preguntar.py` |
| 5 Confirmar el objetivo antes de construir | `arnes/candado_protocolo.py construir` |
| 6 Plan cerrado y reparacion minima | `arnes/edit_gate_universal.py` |
| 7 La prueba la manda la realidad | `arnes/candado_cierre.py` + `cuerpo/cruzado.py` |
| 8 Legislar, sellar y aprender | `sellar.sh` |

### El paso 3 es el que faltaba y el que mas dolio
Del PROTOCOLO_MVP § 6, escrito hace tiempo: *"Causa declarada exige archivo, funcion, linea,
flujo reproducido y evidencia. Sin eso = INFERIDO, y lo inferido NO SE REPARA."*
El 2026-08-20 se iba a **indexar el MVP entero sin saber donde estaba lento**. La regla existia
y no la hacia cumplir nadie. Ahora: `python ingeniero.py causa <proyecto> --archivo ... --funcion
... --linea ... --evidencia "lo que se midio"`. Sin eso, el candado no deja tocar codigo.

### Comprobarlo
`python ingeniero.py protocolo` — dice paso por paso cual tiene candado.
**Regla dura: una ley sin candado es un deseo.** Quedo demostrado el 2026-08-20, con los dos
protocolos escritos, delante, y violados los dos.

## LEY 21 — SIEMPRE EL PAQUETE MINIMO, POR TODAS LAS VIAS (Julio, 2026-08-20)
> "No solo tapa la ventana, sino cada rendija por donde te puedas colar; no sirve de nada gastar
>  mi tiempo en una IA que no me va a ayudar, por el contrario me hace perder tiempo."
> "pon el arnes para que siempre pida el paquete minimo y sea inviolable, no lo vuelvas a pasar
>  por alto, crea vigia."

### EL AGUJERO, medido
La auditoria del trabajo sobre el MVP dio esto: **CERO paquetes minimos pedidos**. Todo el
diagnostico se hizo con busquedas sueltas sobre un archivo de 16.845 lineas. **El arnes vigilaba
TRES puertas y habia SIETE formas de leer sin control.** Vigilaba la puerta principal mientras
se entraba por la ventana.

### LA REGLA, sin excepciones
**SIEMPRE el paquete primero. CERO lecturas de cortesia.** No hace falta buscar antes: el paquete
se pide solo con el problema en palabras normales. Si se queda corto, se pide otro mas concreto
o se justifica con `NECESITO_LEER`.

### Las siete vias, todas vigiladas (`arnes/candado_terminal.py`)
| Via | Antes | Ahora |
|---|---|---|
| terminal: grep, sed, head, tail, cat, awk | libre | vigilada |
| python suelto: `python -c "open(...)"` | libre | vigilada |
| PowerShell: Get-Content, Select-String | libre | vigilada |
| buscar dentro del codigo | libre | vigilada |
| listar archivos | libre | vigilada |
| mandar a otro agente a leer | libre | vigilada |
| abrir el archivo entero | vigilada | vigilada |

- **Vigia:** `test_vigia_sin_rendijas.py` (12 pruebas, una por via).
- **INVIOLABLE** no es que no haya salida: es que **no se pueda usar a escondidas**. Cada apagon
  queda apuntado en `memoria/APAGONES.log`, con fecha y que se leyo.

### LA LLAVE QUE FALTABA (`arnes/permiso_editar.py`)
El candado de edicion ofrecia la salida `NECESITO_EDITAR` **y esa salida no existia**. Un candado
que ofrece una llave inexistente obliga a apagar el arnes entero. Ahora existe:
`python ingeniero.py necesito-editar <archivo> --motivo "..." --vigia "..." --dana "..."`
Permite UN archivo, 30 minutos, con la justificacion por escrito y apuntada.
**Regla nueva: un mensaje de bloqueo NUNCA ofrece una salida que no este implementada.**

## LEY 22 — GUARDAR UN FALLO NO ES APRENDER (Julio, 2026-08-21)
> "Verifica que se esten guardando los errores y que estes aprendiendo de ellos, no veo que te
>  llegue ningun paquete recordandote el error... otra vez estas confiando de tu memoria y es
>  justo lo que debemos combatir."

### LO QUE SE DESCUBRIO
Habia **31 fallos guardados y NINGUNO avisaba jamas**. La memoria solo se consultaba al pedir un
paquete, y solo si las palabras del problema coincidian. Pero hay fallos que no son "un problema
con nombre" sino **una accion** —escribir codigo desde la terminal, por ejemplo—. Ese no coincidia
con nada y **se repitio SEIS veces el mismo dia**.

**La prueba definitiva:** el apunte de ese fallo decia *"NO VOLVER A: meter codigo con \n o rutas
con \a dentro de un heredoc"* y **el propio apunte estaba corrompido por el fallo que describia**.

### LA REGLA
**Aprender no es guardar el fallo: es que el fallo te FRENE la proxima vez.** Por eso cada fallo
lleva un **DISPARADOR**, y el candado `arnes/candado_memoria.py` lo revisa ANTES de cada accion.

### EL DISPARADOR SE ESCRIBE POR LO QUE LA ACCION *HACE*, NO POR SU NOMBRE
Regla de Julio, que ya estaba en su protocolo del MVP y volvio a recordar:
> "en vez de buscar por nombre, se busca por funcion, por lo que hace, asi es mas dificil
>  equivocarse."

Nada de nombres de herramientas ni de archivos —eso cambia y envejece—: la huella de lo que la
accion hace. Asi el aviso salta aunque manana se use otro programa para lo mismo.

- **Pieza:** `arnes/candado_memoria.py` · **Vigia:** `test_vigia_memoria_avisa.py` (7 pruebas)
- **No estorba:** solo avisa de lo que viene al caso. Si avisara de todo se volveria ruido y se
  ignoraria, que es exactamente como estaba antes.
- **Siempre dice QUE HACER en su lugar**, no solo que esta mal.

## LEY 23 — UNA COMPROBACION QUE FALLA A VECES ES PEOR QUE NINGUNA (2026-08-21)

El guardia de cierre dio ROJO y, segundos despues, las mismas 144 salieron VERDES **doce veces
seguidas** sin tocar nada. Un rojo que no se repite no es un fallo: es ruido. Y una comprobacion
que a veces falla se acaba ignorando, que es la peor forma de perderlas todas.

### La causa raiz, reproducida a proposito
Se lanzaron DOS corridas a la vez: **2 y 3 rojas de 144**. Solas, siempre verdes.
Varias comprobaciones escribian en los MISMOS archivos de memoria (el estado, los errores, el
contador de bloqueos) y se pisaban entre ellas. El guardia de cierre las lanzaba **aunque el
sellado ya las estuviera corriendo**.

### La cura, en dos partes
1. **No se lanzan dos corridas a la vez.** El guardia pone un cerrojo mientras corre; si ya hay
   otra en marcha, no lanza la suya.
2. **Cada comprobacion usa SU copia** de la memoria, del estado y del contador. Ninguna toca los
   archivos de verdad.

### Reglas que quedan
- **Un rojo se repite antes de darlo por bueno.** Si no se repite, es ruido.
- **Ninguna comprobacion escribe en los archivos de memoria reales.** Se desvia su ruta.
- **Antes de dar por arreglada una intermitencia, se reproduce a proposito.** Aqui se lanzaron
  dos corridas simultaneas hasta verlas fallar, y luego hasta verlas pasar las dos.

---

## LEY 24 — LO YA REPARADO NO SE VUELVE A ROMPER: TECHO Y PISO (Julio, 2026-08-21)

> "crea el guardia de lo ya reparado, fuerte, con candado, ultra blindado, que siempre este
> pendiente, de extremo a extremo, y que sirva de techo y piso, que nada se le escape, que tenga
> siempre presente los fallos pasados para que no los cometa, y que siempre tenga el grafo del
> pedazo, para que tambien sea eficiente."

**EL PROBLEMA DE SIEMPRE:** arreglar una cosa y tumbar otra que YA funcionaba. Es el dano que mas
caro sale, porque lo que se cae es justo lo que ya se habia dado por bueno y nadie vuelve a mirar.
El guardia de dano cruzado mira a los VECINOS de ahora; este mira al PASADO.

**TECHO** — antes de tocar: se avisa que reparaciones pasadas puede afectar lo que se va a tocar,
con su causa, su cura y su "no volver a".

**PISO** — antes de guardar: se corren las pruebas de ESAS reparaciones. Si una cae, NO SE GUARDA.

**EFICIENTE POR EL GRAFO:** se corren SOLO las pruebas de lo que se toco y sus vecinos, no las 150.
Medido: tocar una pieza son 5 pruebas, no 150. El guardia hace el trabajo MAS rapido, no mas lento.

**LO QUE SE DESCUBRIO AL PONERLO (y es la mitad de la ley):** al sabotear a proposito reparaciones
para comprobar que el piso mordia, **dos de ellas siguieron verdes**: 31 comprobaciones en verde
con el arreglo de tildes eliminado, y 6 en verde con el filtro de asunto anulado. La memoria decia
"protegido" y no lo estaba. De ahi sale la parte dura de esta ley:

> **Una reparacion solo esta protegida si su vigia NACE ROJA al sabotear la cura.**
> Apuntar un nombre de vigia en la memoria no protege nada. Se comprueba rompiendo, no leyendo.

**POR QUE NO LO COMPRUEBAN VARIOS AYUDANTES** (opinion de ingeniero dada a Julio ese dia): lo ya
reparado no se comprueba opinando, se comprueba PROBANDO. La prueba es instantanea, gratis y
siempre da el mismo resultado; un ayudante tarda entre 3 y 300 segundos (medido) y puede
equivocarse. Los ayudantes entran DESPUES, solo cuando algo se pone rojo, para explicar que se
rompio: ahi si hace falta juicio, no comprobacion.

**CANDADO:** `arnes/guard_pasado.py`, enganchado al cierre en `arnes/candado_cierre.py`.
**VIGIAS:** `test_vigia_lo_ya_reparado.py` (10), `test_vigia_el_trozo_habla_del_asunto.py` (4),
`test_vigia_las_tildes_no_rompen_la_busqueda.py` (10). Las tres comprobadas por sabotaje.
