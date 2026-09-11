# DONDE QUEDO — 2026-09-09 (noche). Julio apago el equipo.

> **ACTUALIZADO (2026-09-09, madrugada / sesion de reparacion):** el punto 1 **YA ENTRO y esta
> VERDE**. Lo de abajo es la historia de como se llego hasta ahi; el estado de hoy esta al final,
> en **"REPARACION 1: HECHA Y PROBADA"**.

## Que SI esta hecho y sirve

1. **La ley escrita**: `CONTRATO_EL_PASILLO_SE_REPARTA_POR_CAPACIDAD.md`
   El encargo se manda al cerebro de pago SOLO cuando no le cabe a ningun gratis, **medido**.
   Hoy se decide a ciegas por el tope declarado `TOPE_PESADO = 15000`.
2. **La prueba que destapa el fallo**: `vigias/test_vigia_se_reparte_por_capacidad.py`
   Corre en **0,28 s**, no gasta cuota (espia que solo apunta a quien se le pide).
   Resultado de hoy: **ROJA en 3 casos, VERDE en 2**.
   - ROJO A/B: un encargo de 19.500 letras, que los gratis SI aguantan, **lo contesta deepseek (de pago)**.
   - ROJO C: no se le pide al gratis que aguanta.
   - ROJO 5: la ley vieja sigue escrita en el codigo.
   - VERDE D: lo que no le cabe a nadie sigue yendo al de pago (la orden de Julio no se tira).
   - VERDE G: sin de pago y sin gratis que aguante, se PARA (nunca a solas, F2).
   (Estar roja es lo correcto: es la prueba del fallo, no el arreglo.)

## Que NO entro

El arreglo del codigo. Es **una sola linea**: `cuerpo/obrero.py:473`
    hoy:      if len(prompt) > TOPE_PESADO or pesado:
    debe ser: if pesado or not cuotas.rankear(turnos, len(prompt)):
(`turnos`, linea 466, ya son los gratis disponibles sin los de pago → sin filtro de mas.)

Dos rondas del equipo, **rechazadas las dos** (escribio deepseek, audito gemini2):
- Razon buena que dio el auditor: el filtro que yo pedia sobraba (turnos ya viene limpio). **Acertó.**
- Razon falsa: dijo que la variable `hay` no existia. **Si existe (linea 435).** No se cazo el invento.
- El segundo intento se corto antes de arrancar: no llego a correr.

## Para retomar (comando listo, un solo paso)

    cd C:\Ingeniero_VUC; python ingeniero.py equipo ingeniero "<el encargo de la ronda 2, ya afinado: usar `turnos`>" --escribe gemini4 --revisa gemini2

Despues: correr `python -m pytest vigias/test_vigia_se_reparte_por_capacidad.py -q` (debe pasar a VERDE)
y actualizar `vigias/test_vigia_lo_pesado_a_deepseek.py`, que vigila la ley vieja.

## Pendiente de apuntar

El auditor rechazo dando por falso un dato verdadero (`hay` existe) y el cazador de inventos
(`invento_algo: false`) no lo cazo. Eso es una vigia a reparar: un rechazo en falso frena trabajo bueno.

## Puntos 2 a 6 de Julio

NO empezados, como pidio: primero que Julio vea el punto 1 funcionando con sus ojos.

---

# REPARACION 1: HECHA Y PROBADA (2026-09-09, madrugada)

## Como entro (ruta de acceso declarada, y nada mas)

Julio dio **libertad controlada**: no barra libre. Se abrio la **ruta de acceso** del proyecto
(`memoria/RUTA_DE_ACCESO.json`, ley `CONTRATO_RUTA_DE_ACCESO.md`) con la lista exacta:

    cuerpo/obrero.py
    cuerpo/cuotas.py                (solo si la evidencia lo pide: NO hizo falta tocar)
    vigias/test_vigia_se_reparte_por_capacidad.py
    vigias/test_vigia_lo_pesado_a_deepseek.py
    CONTRATO_EL_PASILLO_SE_REPARTA_POR_CAPACIDAD.md
    PLAN_DE_REPARACION_CONTROLADA.md
    DONDE_QUEDO_2026-09-09.md

Fuera de esa lista, el candado frena (y quedo rastro en `memoria/RUTA_DE_ACCESO.log`).

## El arreglo: 4 cambios, ni uno mas

| # | Archivo | Que se hizo |
|---|---|---|
| 1 | `cuerpo/obrero.py` (linea 482) | `if pesado or not cuotas.rankear(turnos, len(prompt)):` — el de pago entra si **ningun gratis aguanta** (medido), no por un tope escrito a mano. Antes: `if len(prompt) > TOPE_PESADO or pesado:` |
| 2 | `cuerpo/obrero.py` (linea 745) | `pesado_ahora = bool(generador) and generador in cuotas.DE_PAGO` — el pesado **se mide, no se supone**. Antes: `pesado_ahora = not generador` (que era el 0 de 72 y metia el bloqueo F2 en el caso normal) |
| 3 | `cuerpo/obrero.py` (linea 230) | `TOPE_PESADO` queda **informativo**: ya no decide nada. NO se borra porque `medir_las_nueve_puertas.py` lo lee (vecino que solo lo mira) |
| 4 | las 2 vigias | la del punto 1 se endurecio (vigila tambien que el tope no vuelva) y `test_vigia_lo_pesado_a_deepseek.py` se **actualizo a la ley nueva** (no se borro) |

## Prueba (hecha, no contada)

- **`vigias/test_vigia_se_reparte_por_capacidad.py`: ROJA en 3 -> 5 passed en 0,30 s.** No gasta cuota.
- **Vecinos del cross-flow: 52 passed, 0 failed** (repartidor por capacidad, respeta generador/auditor,
  el cerebro que pido, relevo de cuotas, nada lento, revisor roto, ruta de acceso, lo pesado a deepseek).
- **Juego completo de vigias: 642 passed, 6 failed** — y esas 6 **ya estaban rojas antes** de tocar
  nada: se comprobo apartando el arreglo con `git stash` y corriendo las mismas 6 con el codigo viejo
  (6 failed / 14 passed). Son: `test_vigia_el_espia.py` (4), `test_vigia_fallos_de_verdad_avisan.py` (1)
  y `test_vigia_memoria_completa.py` (1). Ninguna toca el reparto.
- **Evidencia con los numeros REALES del proyecto** (capacidades medidas hoy):
  `groq 19.042 · groq20b 20.169 · gemini 107.349 · gemini2 194.297 · gemini3 30.314 · gemini4 193.689 ·
  local 26.000 · deepseek 230.668`
  - encargo de **19.500 letras** -> lo aguantan **6 gratis** (antes: iba a DeepSeek de pago).
  - encargo de **60.000 letras** -> lo aguantan gemini4, gemini2 y gemini (antes: DeepSeek de pago).

## Lo que FALTA (y por que)

**Falta la prueba de Julio con sus ojos** (ley: vigia verde no es prueba). Y **no se toca** el punto 2
ni nada mas hasta que el punto 1 quede certificado por el.

Dos cosas que se aprendieron y quedan apuntadas:
1. **El candado de la ruta no tenia puerta**: `abrir()`/`cerrar()` existen, pero ningun comando de
   `ingeniero.py` los llamaba. Se abrio con una orden directa. Merece su propia reparacion.
2. **Un comentario que cita la ley vieja pone roja la vigia**: los detectores buscan el texto en el
   codigo, y el comentario que explica el fallo lo contiene. Se escribe la ley nueva sin copiar la
   linea vieja literal.

---

# PRUEBA REAL DEL 2026-09-10 (lo que pidio Julio: "que no vuelva a salir el fallo")

Julio: *"La prueba real es que no vuelva a salir el fallo... sigue reparando DMM; si sale el fallo,
para; esa es la verdadera prueba real."*

**Se lanzo una ronda REAL del equipo** (no un simulacro y no una vigia), con un trabajo real que
estaba pendiente y con su vigia nacida ROJA pidiendolo: crear `vigias/_espia.py` (punto A1 del plan
de DMM, `PLAN_LAS_15_QUE_FALTAN.md`, "EMPIEZA AQUI").

    cd C:\Ingeniero_VUC; python ingeniero.py equipo ingeniero "<crear vigias/_espia.py>" --crear

**Quien escribio: `gemini4` (GRATIS). Quien reviso: `gemini` (GRATIS, y DISTINTO).**
Registro: `memoria/TRABAJOS_DEL_EQUIPO.log` -> `2026-09-10 12:04 | escribio gemini4 | reviso gemini`.

Antes del arreglo, TODAS las rondas del log iban `escribio deepseek | reviso deepseek`: el de pago
escribia siempre, y a veces se revisaba a si mismo. **El fallo del punto 1 NO volvio:** ningun gratis
quedo de brazos cruzados, no hubo aviso falso de "no le cabe" y no salto el bloqueo F2 en un caso
normal. Ficheros de la ronda: `memoria/_ronda_espia.txt` y `memoria/ULTIMO_TRABAJO_DEL_EQUIPO.json`.

## Lo que SI salio (y NO es el fallo del reparto)

El veredicto fue **RECHAZADO**, por una causa distinta y demostrada:

- Con la marca `--crear`, el obrero recibe el encargo de **ANALISTA** (`cuerpo/obrero.py`,
  `_prompt_obrero`): *"NO vas a cambiar codigo... el documento ENTERO y completo, escrito en markdown"*.
- El gratis hizo EXACTAMENTE lo que se le pidio: entrego un documento en markdown.
- El auditor lo rechazo con razon: un `.py` con markdown revienta al importarlo.
- **Causa raiz medida:** el encargo de crear NO distingue "crear un informe" de "crear una pieza de
  codigo". Sin eso, A1 y A2 del plan quedan atascados.

**No se toca nada de eso**: es el punto 2/3 y espera a que Julio certifique el punto 1 (regla 6 del
plan). Queda apuntado y dicho, no tapado.

## Colores de hoy (corridos de verdad, no leidos)

- `vigias/test_vigia_se_reparte_por_capacidad.py` + `test_vigia_lo_pesado_a_deepseek.py`: **10 passed**.
- Vecinos del cross-flow (8 vigias): **50 passed, 0 failed**.
- `vigias/test_vigia_el_espia.py`: **4 failed** - es correcto: nace ROJA pidiendo su pieza.

## Una pregunta del sistema que YA tiene respuesta (fallo 67 de dmm)

El fallo 67 pedia: *"¿cual es el archivo del chat real que atiende al dueno y cual es la funcion que
procesa los mensajes?"*. **Buscado por nombre, no adivinado:**

- `web/panel_chat.py` -> `armar_respuesta(perfil, mensaje, preguntar=None)` (procesa el mensaje).
- Se llama desde `web/servidor.py` (la ruta del POST del chat).
- La ventana es `web/bloque_chat.py` -> `html_chat(historial=None)`.
- En DMM ese enchufe **ya se hizo** (commit `ca30e7b`); `cuerpo/traductor.py` y `cuerpo/aprobacion.py` existen.


---

# PARADA ORDENADA POR JULIO (2026-09-10) — REAPARECIO EL FALLO RECURRENTE

**Orden de Julio:** *"La prueba real de que la reparacion de los fallos recurrentes funciono es que
se siga construyendo el DMM sin que aparezcan los fallos recurrentes ya documentados. Si esto
sucede, la reparacion es un fracaso total: debes PARAR y AVISAR."*

**Resultado medido: SE PARA.** La construccion de DMM **no avanzo** y el fallo que lo impide esta
ya documentado en esta casa.

## Lo que se intento (continuar por donde Julio interrumpio)

Crear la pieza **A1** que DMM tiene mandada y que su vigia esta pidiendo a gritos:
`vigias/_espia.py` (ley: `CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO.md`, Regla 4: el espia es UNO
para toda la casa). Ronda real del equipo, 2026-09-10 12:04.

## El fallo recurrente que reaparecio (documentado, con numero)

`CONTRATO_CREAR_PIEZA_NUEVA.md`, escrito el **2026-09-05**, lo dice literal:

> *"Resultado medido el 2026-09-05: **cinco encargos seguidos de crear una habilidad fueron
> rechazados, y no se pudo crear ni una.**"*

Hoy es **el sexto**. La ronda de hoy salio **RECHAZADA** y la pieza **NO se creo** (`vigias/_espia.py`
no existe; el registro lo dice: `2026-09-10 12:04 | escribio gemini4 | reviso gemini | RECHAZADO`).
Se intento **construir DMM** y DMM no se construyo. Ese es el sintoma recurrente: **no se puede
crear la pieza nueva**. La ley lo persiguio en 2026-09-05 abriendo la puerta del anti-invento; y
hoy vuelve **por otra puerta** — el patron exacto que denuncia `EXPEDIENTE_FALLOS_RECURRENTES.md`
("se repara, sale verde, y a los dias vuelve por otra puerta").

## La causa, medida (no supuesta)

La **ley** (`CONTRATO_CREAR_PIEZA_NUEVA.md`) trata la creacion como **PIEZA DE CODIGO** (cinco
respuestas, alcance, quien la llama). El **mando**, en cambio, manda el encargo de **ANALISTA**
(`cuerpo/obrero.py`, `_prompt_obrero`, linea 92):

> *"texto_nuevo": "el documento ENTERO y completo, escrito en **markdown**"*

**Ley y mando se contradicen.** El cerebro gratis hizo EXACTAMENTE lo que se le mando (un documento
en markdown); el auditor lo rechazo con razon (un `.py` con markdown revienta al importar). No fallo
ni el reparto ni el auditor: **falla el encargo, que no distingue "crear un informe" de "crear una
pieza de codigo"**. El propio expediente ya lo tenia apuntado como pendiente (seccion 14.3: *"el
caso crear (analista) sigue sin decidir"*).

## Lo que SI quedo comprobado hoy (para que conste)

| Comprobacion | Resultado |
|---|---|
| Reparto por capacidad (punto 1) | **OK**: escribio `gemini4` (GRATIS), reviso `gemini` (GRATIS y DISTINTO) |
| Fallo 65 (el unico vivo se revisa a si mismo) | **NO reaparecio** |
| Fallo 52 (`experimentos.py` no sale) | **CURADO de hecho**: `cuerpo/experimentos.py` existe y su vigia real (ejecuta la pieza, no lee palabra) da **6 passed** |
| Fallo 64 (trabajar ignora generador/auditor) | No medido en esta ronda |
| Fallo 67 (el material no trae el chat real) | No aplicaba; **pendiente de medir** antes de seguir con el chat |
| Punto 1 + lo-pesado | **10 passed** |
| Vecinos del cross-flow (8 vigias) | **50 passed / 0 failed** |
| `vigias/test_vigia_el_espia.py` | **4 failed** — correcto: nace roja pidiendo su pieza |

## Lo que la ley pide para desbloquearlo (y NO se hace sin Julio)

1. **Autorizacion**: `CONTRATO_CREAR_PIEZA_NUEVA.md`, Regla 5 — se crea *"con autorizacion de Julio"*.
2. **El encargo debe pedir CODIGO, no markdown**: es el punto 2 de la reparacion (no autorizado aun).
3. Es el trabajo **A1** del plan de DMM (`PLAN_LAS_15_QUE_FALTAN.md`), que ya tiene su vigia escrita
   y roja: la pieza solo tiene que hacer `mirando(objeto, "nombre")` con `la_llamaron` y `veces`,
   y el molde ya existe en `vigias/test_vigia_no_se_paga_dos_veces_por_lo_mismo.py`.

**NO se ha tocado codigo.** La ruta de acceso sigue abierta (7 piezas), sin usar. Nada se cierra.


---

# DESBLOQUEO DEL FALLO RECURRENTE (2026-09-10, el mismo dia)

**Autorizacion de Julio:** *"si, autorizo crear una pieza nueva"* — se cumple la Regla 5 de
`CONTRATO_CREAR_PIEZA_NUEVA.md`. La ruta de acceso se amplia **solo** con lo que la pieza necesita
(`vigias/_espia.py`), y queda escrito en `memoria/RUTA_DE_ACCESO.json` con su motivo.

## Paso 1 — El encargo de `--crear` ya pide CODIGO (punto 2, reparado)

`cuerpo/obrero.py` (`_prompt_obrero`, pieza que YA estaba en la ruta abierta): dentro de la rama de
crear, si la tarea pide un archivo `.py` se devuelve un encargo NUEVO de **ANALISTA DE CODIGO**; si
pide un documento, el encargo de siempre **queda intacto**. Comprobado ejecutando:

| Caso | Antes | Ahora |
|---|---|---|
| la tarea pide `vigias/_espia.py` | pedia *el documento entero, en markdown* | pide **codigo Python entero y ejecutable** |
| la tarea pide un documento/guia | documento en markdown | **igual que antes** |
| la tarea de reparar | encargo de obrero | **igual que antes** |

**NO se pago por esto** (ley `CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md`). El primer intento se mando al
equipo y **fue el propio equipo el que lo freno**:

> `FRENADO: ESO ES UNA FOTOCOPIA, Y LA FOTOCOPIA NO SE PAGA. (...) lo aplica arnes/copista.py`

Los dos textos ya estaban decididos, asi que lo aplico el **copista** (programa, gratis, 1 segundo),
con su encargo en `memoria/_encargo_copista.txt`. Antes de aplicar se comprobo en seco que el
`TEXTO_VIEJO` aparecia **exactamente 1 vez**, y despues que el archivo **compila**.

## Paso 2 — La pieza nueva se creo, y es la primera vez

Ronda real, `--crear`, 2026-09-10 12:26:

| | |
|---|---|
| Quien ESCRIBIO | **`gemini4` (GRATIS)** |
| Quien REVISA | **`gemini3` (GRATIS y DISTINTO)** |
| Veredicto | **APROBADO** |
| Pieza | `vigias/_espia.py` creada, **3.654 bytes** |
| Registro | `memoria/TRABAJOS_DEL_EQUIPO.log`, `memoria/_ronda_crear.txt` |

**Es el sexto encargo de crear una pieza nueva y el PRIMERO que se aprueba.** Ese fallo recurrente
queda **curado de hecho**: la pieza existe y su vigia lo demuestra ejecutando.

## Paso 3 — Prueba fisica (correr, no leer)

| Prueba | Antes | Ahora |
|---|---|---|
| `vigias/test_vigia_el_espia.py` | **4 failed** | **4 passed** |
| Vecinos del cross-flow + vigias del obrero (12 ficheros) | verde | **67 passed / 0 failed** |
| Juego completo | 642 passed + 6 rojas | **646 passed / 2 rojas** |

Las **2 rojas que quedan son ajenas** y ya estaban antes (comprobado en `memoria/FALLOS.json`):
`test_vigia_fallos_de_verdad_avisan` (el fallo 67, del 2026-09-09, sin disparador) y
`test_vigia_memoria_completa` (legislacion pendiente). Las 4 de `_espia` son justo las que han virado
a verde: 642 + 4 = 646. **No ha nacido ninguna roja nueva.**

Fallo 65 (el unico vivo se revisa a si mismo): **NO reaparecio** (escribio `gemini4`, reviso `gemini3`).

### Como verlo con tus ojos (comando listo para PowerShell)

    cd C:\Ingeniero_VUC; python -m pytest vigias/test_vigia_el_espia.py -q

## Lo que sigue pendiente, dicho claro

1. **Certificacion de Julio** (etapa 8 del plan): que vea la pieza funcionar con sus ojos. Hasta
   entonces la ruta sigue **abierta**.
2. `EXPEDIENTE_FALLOS_RECURRENTES.md` **quedo desactualizado** (da el 52 y este como vivos). No se
   toca porque no esta en la ruta declarada: lo amplia Julio, o dice que se amplie.
3. `ingeniero.py` imprime *"Al obrero le llega el encargo de ANALISTA: escribe el documento entero"*
   al crear **aunque la tarea pida codigo**. Es solo el mensaje (la pieza esta bien), pero es un
   aviso que no dice la verdad; `ingeniero.py` tampoco esta en la ruta.
4. **Fallo 67** (*el material no trae el chat real*): sigue **sin medir**, y hay que medirlo antes de
   seguir con el chat de DMM.
5. `vigias/_espia.py` funciona (su vigia pasa), pero trae **codigo de mas**: un `import contextlib`
   que no usa y una heuristica (`_es_modulo`) que decide lo mismo por los dos caminos. No estorba:
   queda apuntado como limpieza, no como urgencia.
6. El **molde que cita el plan de DMM** (`vigias/test_vigia_no_se_paga_dos_veces_por_lo_mismo.py`)
   **no esta en el Ingeniero: esta en DMM** (`...\Asesor Marketing\vigias\`). El plan lo da por
   existente aqui y no lo esta: dato para corregir el plan.
7. **Queda abierto A2** (el candado que caza el veneno) y **A3/A4** del plan de DMM. No se empieza
   nada de eso hasta que Julio certifique este paso.

