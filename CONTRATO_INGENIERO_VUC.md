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
