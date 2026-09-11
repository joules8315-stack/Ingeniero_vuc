# EXPEDIENTE DE FALLOS RECURRENTES — POR QUÉ NADA FUNCIONA

**Lo pidió Julio, 2026-09-09.** "Mostrar todos los fallos recurrentes, qué se ha descubierto,
qué se ha hecho para repararlo, y por qué una y otra vez vuelve a salir. Trae todo: dividir el
paquete, que no sea corte arbitrario, que se asigne por capacidad a las IA... y mira por qué
nada funciona."

Todo lo de abajo está sacado del propio sistema (commits, memoria/FALLOS.json, contratos,
vigías). Nada de memoria ni de opinión.

---

## 1. LA RESPUESTA CORTA (la raíz)

> Hay **un solo pasillo** por donde todo paquete va a un cerebro, y **nadie lo vigila**.
> Los arreglos se han hecho **abriendo puertas nuevas**, no poniendo el filtro en el pasillo.
> Y las pruebas dan **verde de mentira** porque miran **el papel escrito, no lo que de verdad
> le llega al cerebro**. Por eso se repara, sale verde, y a los días vuelve por otra puerta.

---

## 2. EL MISMO PROBLEMA "RESUELTO" CINCO VECES

| Día | Commit | Qué se anunció | Qué se hizo | Por qué no aguantó |
|---|---|---|---|---|
| 07-sep | `8673f49` | "EL PAQUETE ADELGAZA: de 24.916 a 19.951 letras, y vuelve a caber" | En `router.armar`: si la tarea nombra archivos, se queda solo con esos trozos | Solo cubre el caso de "nombra archivos". El paquete general siguió gordo |
| 07-sep | `8fd6c04` | "EL RECORTE DEL PAQUETE YA FUNCIONA" | Arreglar un `continue` que dejaba la lista vacía y el recorte **no se aplicaba nunca** | Recorta en el repartidor, no en la salida; otra puerta lo salta |
| 07-sep | `6ba46e3` | "EL PAQUETE YA MANDA LOS RECUERDOS QUE IMPORTAN" | Pesar recuerdos por rareza de palabra | No toca el tamaño ni el pasillo |
| 08-sep | `f4956a0` | "MEDIDO: los gratis no fallan, es que NO LES CABE EL PAQUETE" | Se descubre que `a_texto` corta la ley a **400 LÍNEAS** y no mira las **LETRAS** | **No se aplicó el tope de 6.000.** El encargo siguió en 41.022 |
| 09-sep | `564a05b` | "LA CAUSA RAIZ DEL MATERIAL DE MAS: se le pedía buscar a un encargo que ya lo traía dentro" | `juzga` deja de buscar material; tope 19.000 → 15.000; nada viaja dos veces | Se aplicó **solo** en `resolver` y `juzga`. `equipo` y el bucle cruzado siguen mandando el bulto entero |

**Cinco "ya está resuelto".** Y hoy, 2026-09-09 18:27, la última ronda del equipo volvió a salir
**RECHAZADA** — y además **se revisó a sí misma** (`escribió deepseek · revisó deepseek`).

---

## 3. LOS FALLOS QUE SE REPITEN (memoria/FALLOS.json)

| ID | Veces | Qué pasó | Causa raíz | ¿Sigue vivo? |
|---|---|---|---|---|
| 64 | **5** | `trabajar` acepta "generador" y "auditor" pero **no los usa** | Los parámetros no llegan al relevo: se pide un cerebro y contesta otro, sin avisar | Parcheado en parte; el relevo sigue mandando generación al de pago |
| 67 | **5** | Encargo "enchufar traductor y aprobación al chat" **nunca se puede hacer** | El material **no trae** el archivo del chat: el cerebro responde `NO_ENCONTRADO` | **Vivo** |
| 52 | **5** | Crear `experimentos.py` no sale | Módulo no existe + firmas incompatibles + material insuficiente | **Vivo** |
| 46 | 1 | "Se le mandó al equipo un encargo SIN el pedazo de código, y el obrero se rindió" | El paquete midió **598.377 letras**: no le cabía a nadie | **Vivo** (es el mismo de hoy) |
| 65 | 1 | "El único cerebro vivo se revisa a sí mismo y se contradice" | No son cuatro ojos: es el mismo cerebro con dos sombreros | **Vivo** (última ronda) |
| 1 | 1 | El paquete traía el motor pero **no la cara** | El flujo se armaba solo por el **nombre** del archivo | Parcheado |
| 16 | 1 | El buscador decía `NO_ENCONTRADO` sobre `medidor.py` | Tildes: el índice guarda "económico", la consulta va sin tilde | Parcheado |

Los de **veces = 5** son la firma del problema: el mismo fallo contado cinco veces.

---

## 4. QUÉ SE HA HECHO PARA REPARARLO (todo el arsenal)

**Leyes (contratos):**
- `CONTRATO_AL_CEREBRO_SOLO_LO_SUYO` — al cerebro solo lo suyo.
- `CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA` — lo que ya trae texto viejo/nuevo lo hace un programa.
- `CONTRATO_MEDIR_A_LOS_GRATIS` — a los gratis se les mide con trabajo real.
- `CONTRATO_SIN_OBJETIVO_NO_SE_PIDE_NADA` — sin objetivo no se llama a nadie.
- `CONTRATO_CREAR_PIEZA_NUEVA` — crear no es arbitrario; y **nace conectada o no nace**.
- `CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO` — lo enchufado se prueba ejecutándolo.
- `CONTRATO_MENOS_IA_MAS_PROGRAMA`, `CONTRATO_SE_BUSCA_POR_NOMBRE`, `CONTRATO_SE_BUSCA_POR_FUNCION`.

**Repartidor por capacidad (ley de Julio 2026-08-21):** *"es estúpido darle una tarea a una IA
que sabes que no va a soportar"*. Hecho: `cuotas.rankear` salta al que no aguanta el tamaño.
Medido hoy: groq 19.042 · groq20b 20.169 · gemini3 30.314 · local 26.000 · deepseek 230.668.

**Lo pesado siempre a DeepSeek (orden de Julio 2026-08-21):** hecho en `trabajar` con
`pesado = not generador`. **Pero esto es justo lo que manda a generar al de pago casi siempre.**

**Vigías del tema:** `al_cerebro_solo_llega_lo_suyo`, `la_fotocopia_no_se_paga`,
`repartidor_por_capacidad`, `lo_pesado_a_deepseek`, `el_asignador`, `no_se_juzga_lo_que_ya_esta_verde`.

**Cura construida:** `arnes/asignador.py` (`armar_encargo`), que recorta y elige cerebro.

---

## 5. POR QUÉ NADA DE ESO LO HA CURADO (las 6 causas de fondo)

1. **El filtro no está en el pasillo.** Todo paquete pasa por `obrero._preguntar_con_relevo`.
   Ahí **no hay recorte**. Se puso en 2 puertas de 6. Las otras 4 lo saltan.
2. **La prueba mide el papel, no el hecho.** `test_vigia_al_cerebro_solo_llega_lo_suyo` busca la
   **palabra** `armar_encargo` dentro de `resolver`. No mide lo que llega al cerebro.
   (Su propio texto afirma *"el mando equipo también usa el asignador"* — **es falso**.)
3. **El recorte que existe recorta mal.** `armar_encargo` tira **el final**, suponiendo que el
   relleno está al principio. En el paquete real el código va **en medio**: medido, **9 funciones → 0**.
   Cabe, pero no sirve.
4. **Generar va al de pago por diseño** (`pesado = not generador`). Los gratis no "se saltan":
   para escribir **ni se les pregunta**. Y si el de pago también recibe un bulto inútil, contesta.
5. **Nadie llama a la cura.** `armar_encargo` está construido, con vigía verde, y **casi nadie lo usa**.
   Es la enfermedad de las "22 piezas dormidas" del proyecto de marketing.
6. **Verde falso propio, ya cazado antes:** `ecf26cc` ("se caza un VERDE FALSO propio") y `fd7b14a`
   ("dos cerebros aprobaron código que revienta en la primera línea"). El segundo par de ojos
   **de IA no cubre lo mecánico**.

---

## 6. LA RESPUESTA MECÁNICA (por qué no es una respuesta "de verdad")

En `cuerpo/obrero.py`, el encargo al cerebro dice **literalmente**:

> "**1. NO inventes archivos, funciones ni líneas. Si algo no está en el material, escribe
> NO_ENCONTRADO.**"

Cuando el material (recortado o gordo) **no trae la pieza**, el cerebro no falla: **obedece y
escribe `NO_ENCONTRADO`**. La plantilla no es una respuesta del cerebro; es **una instrucción
nuestra que se cumple**. El sistema le enseña a contestar eso cuando llega sin lo suyo.

Y no es solo `NO_ENCONTRADO`: el mismo texto de relleno produce respuestas **idénticas entre
modelos distintos** (por eso "la misma plantilla"). Un cerebro ahogado en relleno **no juzga:
adivina**.

---

## 7. ¿ES EL FLUJO DE TRABAJO O QUÉ? (lo que dicen los datos)

- **No es (solo) el tamaño.** Ya se adelgazó (24.916 → 19.951) y hay encargos que caben y aun así
  fallan, porque **el recorte tira la pieza**. Tamaño y contenido son dos cosas.
- **No es (solo) la capacidad.** Ya se reparte por capacidad y se salta al que no aguanta.
- **No es que los gratis sirvan o no:** medido, **nunca se les ha dado la oportunidad de escribir**
  (0 de 72). Y por orden de Julio, generar va al de pago.
- **SÍ es de flujo y de prueba.** El flujo tiene **6 puertas** y el filtro en **2**. Y la prueba
  mide el **código fuente** en vez de lo que **llega**. Mientras la prueba mire el papel, cada
  parche sale verde y el fallo reaparece por otra puerta.

**Conclusión:** es, sobre todo, **de dónde está el filtro** y **qué mide la prueba**. No de las
piezas que faltan: las piezas existen; es el **enchufe**.

---

## 8. LO QUE HAY QUE DECIDIR CON JULIO

1. Poner **el filtro en el pasillo** (una vez, para las 6 puertas) — no en cada puerta.
2. **Recortar por partes, no por el final**: conservar siempre lo que el problema **nombra**
   y la ley que aplica; tirar la ley repetida y las plantillas de cola.
3. **Reescribir la cura** (`armar_encargo`) para que no deje fuera el código, o sustituirla.
4. **Vigía que mide el hecho**: intercepta el pasillo en las **6 puertas** y comprueba que lo que
   llega **no pasa del tope** y que **la pieza que hay que reparar sigue dentro**. Nada de "la
   palabra está en el archivo".
5. Decidir el caso **crear** (analista): cuánto material necesita sin romper la creación.
6. Y **usar la cura de verdad** una vez, en una corrida real, para ver un gratis contestando algo
   útil en vez de la plantilla.

---

## 9. MEDIDO EN VIVO HOY (2026-09-09)

- Paquete dmm: **7.610 letras** → al convertirlo en encargo del obrero: **10.300 letras**.
- Tope real de los gratis: **19.042** (groq), **20.169** (groq20b), **26.000** (local),
  **30.314** (gemini3). DeepSeek: **230.668**.
- Paquete `equipo` medido en una corrida real: **34.460 letras** → **no le cabe a ninguno de los
  cuatro gratis**.
- Última ronda del equipo (18:27): veredicto **RECHAZADO**, y `escribió deepseek · revisó deepseek`
  (el fallo se materializó dentro de su propio intento de repararse).

---

## 10. COMPROBACIÓN DE RESPALDO (Julio dudó de estos datos: "es siempre el mismo mensaje")

Julio, textual: *"los datos suministrados son datos que no tienen respaldo, dado que es siempre el
mismo mensaje, no existe variación en todos los paquetes, lo cual es sospechoso, que parece una
memoria vieja, recurrente."*

Se fue a comprobar con números. Resultado — **mitad y mitad**:

**Lo que NO es cierto (la memoria no está copiada):**

| Qué se comprobó | Resultado |
|---|---|
| Textos de los 67 fallos | **67 distintos de 67** (0 repetidos) en `que_paso`, `causa_raiz`, `cura` y `no_volver_a` |
| Los 121 paquetes guardados | **121 distintos** de 121 (por sus primeras 500 letras) |
| ¿Se perdió memoria? | No: **0 fallos** del respaldo de git faltan hoy en disco |

**Lo que SÍ es cierto (y es lo que Julio olía):**

| Qué se comprobó | Resultado |
|---|---|
| La memoria vieja va pegada en los paquetes | El bloque **"LO QUE YA NOS PASÓ AQUÍ"** viaja en **112 de 121 paquetes** |
| Cuánto pesa ese bloque | **3.292 letras de media = el 14% del paquete entero** |
| Peso medio de un paquete | **23.294 letras** → **por encima del tope de todos los gratis** (19.042 el más pequeño) |
| Los paquetes más gordos | Hasta **157.272 letras** (los 5 mayores son de `foto_informe`) |
| Fechas de nacimiento | El mismo día se generan paquetes a montones: 31-ago x14, 21-ago x13, 08-sep x13, 27-ago x12, 20-ago x12, 05-sep x11, 09-sep x7 |
| La memoria de fallos, en git | **66 fallos, TODOS de agosto**. Del 06-sep al 09-sep (9 commits del mismo fallo) **solo se apuntó 1** |

**Conclusión de la comprobación:** **no es un texto viejo copiado literalmente** (cada fallo y cada
paquete son únicos). **Sí es un mensaje recurrente**: la **misma memoria de fallos** se pega en
casi todos los paquetes (3.292 letras, 14%), y el paquete medio (**23.294**) ya nace **por encima
del tope de todos los gratis**. Por eso el resultado que sale es **siempre el mismo**: no cabe →
se salta a los gratis → contesta el de pago → contesta la plantilla. **El mismo mensaje de salida
no es memoria vieja: es el único resultado posible de un paquete que siempre nace grande.**

**Y una advertencia honesta, que va antes de seguir:** las cifras de los avisos de capacidad de
`ULTIMO_TRABAJO_DEL_EQUIPO.json` (34.460, 37.644, 34.766, 36.619...) **no llevan fecha ni número
de ronda**, y ese archivo se sobrescribe en cada corrida. Son **un solo momento**, no una serie.
Lo que sí está respaldado en git: los commits, los 66 fallos de agosto y el `FALLOS.json` actual.

---

## 11. EL PASILLO, MEDIDO HOY (esto sí se puede reproducir)

**El pasillo único es `cuerpo/obrero.py::_preguntar_con_relevo` (línea 427).** Ahí confluyen
**9 sitios** que construyen un prompt y lo mandan a un cerebro — **ninguno recorta**:

| # | Dónde | Qué manda |
|---|---|---|
| 1 | `cuerpo/obrero.py:742` | **GENERAR** (el trabajo de verdad) |
| 2 | `cuerpo/obrero.py:664` | auditar (reintento 1) |
| 3 | `cuerpo/obrero.py:689` | auditar con el de pago (último recurso) |
| 4 | `cuerpo/cruzado.py:149` | los dos ojos del ciclo cruzado |
| 5 | `cuerpo/cruzado.py:195` | el reparador, con el intento anterior dentro |
| 6 | `cuerpo/cruzado.py:208` | el juez |
| 7 | `cuerpo/consejeros.py:95` | los consejeros |
| 8 | `cuerpo/dudas.py:140` | responder dudas |
| 9 | `cuerpo/skills.py:194` | buscar/crear habilidad |

**La medición (reproducible con `python medir_el_pasillo.py`):**

| Escalón | Letras | ¿Cabe en un gratis? |
|---|---|---|
| Lo que Julio manda (paquete) | **7.575** | — |
| Lo que sale del recorte (`armar_encargo`) | **14.858** | ✅ **cumple el tope de 15.000** |
| **Lo que DE VERDAD llega al cerebro** (`_prompt_obrero`) | **25.122** | ❌ **no le cabe a groq (19.042) ni a groq20b (20.169)** |

**El encargo se recorta bien y aun así se pasa: el prompt final es ×1,69 más grande que el encargo
y ×3,32 más grande que lo que se mandó.** Dos motivos, los dos en el código:

1. **`_prompt_obrero` añade su plantilla fija** (las 5 reglas duras, ~2.400 letras) **encima** del
   material, y **vuelve a meter la tarea**, que ya viaja dentro del encargo como "OBJETIVO".
2. **`trabajar` reintenta 3 veces y EN CADA RECHAZO PEGA LOS MOTIVOS AL ENCARGO** (`obrero.py:735-741`).
   El paquete **crece en cada vuelta**: eso explica los 34.460 → 37.644 → 36.619 de la última ronda.

**Y el golpe final, la razón de fondo:** el tamaño **se mira dentro del pasillo** (`obrero.py:480`,
`cuotas.rankear(turnos, len(prompt))`), **después** de construir el prompt. Ahí ya no se puede
recortar: la única jugada posible es **saltar** al cerebro. Saltar a todos = paga el de pago =
**se juzga a sí mismo**. **Ese es el punto exacto donde nace el fallo cada vez**, y es el único
punto donde nunca se ha puesto una cura.

---

## 12. POR QUÉ LA MEMORIA DE FALLOS NO HA FRENADO NADA

La ley existe y es buena (`CONTRATO_MEMORIA_DE_FALLOS`, 2026-08-21): *"Guardar un fallo NO es
aprenderlo"*, y exige 4 cosas (qué pasó, causa raíz, no volver a, **disparador**).
Pero se comprobó lo que pasa de verdad:

1. **La memoria no cuenta la repetición.** El campo `veces` se lleva **por encargo**, no por causa:
   de 67 fallos, **64 tienen `veces = 1`**. Cuando el mismo fallo vuelve, **nace con id nuevo**.
   Por eso el contador dice que casi nada se repite mientras todo se repite.
2. **Los 4 días que más ha dolido no están apuntados.** En git hay **66 fallos, todos de agosto**.
   Los **9 commits del mismo fallo** entre el 06-sep y el 09-sep dejaron **1 solo apunte** (el ID 67).
3. **La ley tiene un efecto perverso escrito en ella misma:** *"no se apunta un fallo sin disparador;
   antes no apuntarlo que apuntarlo mudo"*. Si el que apunta no encuentra la señal corta, **no
   apunta**. Y un fallo no apuntado **no puede avisar**.
4. **Cuando se legisló, era peor:** de 51 fallos, **24 mudos** y **7 con el disparador escrito como
   frase** (una frase no coincide con nada, nunca).
5. **El sistema confiesa que deja pasar la repetición.** `memoria/.repeticiones.log` tiene
   **964 líneas**, casi todas *"BLOQUEO: respuesta repetida, se frena"* y *"AVISO: se deja pasar
   para no atascar a Julio, pero repite lo ya contado"*.
6. **Hueco conocido y escrito en el propio contrato:** el aviso de fallos **no distingue** entre
   cometer el fallo y trabajar sobre el registro de fallos. Al escribir esa misma ley **frenó
   cuatro veces**.

---

## 13. LAS 14 REPARACIONES, UNA POR UNA (cronología completa)

| # | Día | Commit | Dónde se puso el parche | Por qué no aguantó |
|---|---|---|---|---|
| 1 | 20-ago | `18768dc` | Nace el "router de paquete mínimo" | Nace midiendo **líneas**, no letras |
| 2 | 21-ago | `ea78d43` | LEY 21: paquete mínimo por las 7 vías | Ley escrita, sin candado que muerda |
| 3 | 21-ago | `c3f65a8` | "lo pesado a DeepSeek" | Crea `pesado`: mandar a generar al de pago **siempre** |
| 4 | 01-sep | `75081d2` | Avisar cuando no le cabe a nadie | **Avisa, no arregla** (`obrero.py:492`) |
| 5 | 01-sep | `356a4cb` | Apartar al cerebro roto | Aparta también al sano que no aguanta |
| 6 | 07-sep | `8673f49` | `router.armar`: quedarse con los trozos nombrados | Solo el caso "nombra archivos" |
| 7 | 07-sep | `6ba46e3` | Pesar recuerdos por rareza | No toca el tamaño |
| 8 | 07-sep | `ecf26cc` | Memoria en la puerta de DMM | Se caza 1 verde falso; quedan los del pasillo |
| 9 | 07-sep | `8fd6c04` | Un `continue` que anulaba el recorte | Recorta en el repartidor, no en la salida |
| 10 | 08-sep | `f4956a0` | Descubrir que `a_texto` corta a 400 líneas | **El tope de 6.000 no se aplicó**: 41.022 |
| 11 | 08-sep | `b813846` `4d975d3` `c607219` | El copista: la fotocopia no se paga | Reparación **lateral** al bulto |
| 12 | 08-sep | `cac2611` | El asignador decide a quién pedir | Decide **a quién saltar**, no recorta |
| 13 | 09-sep | `564a05b` | Tope 19.000 → 15.000; nada viaja dos veces | Solo en `resolver` y `juzga` |
| 14 | 09-sep | `f0d6ada` | Enchufar `armar_encargo` en `ingeniero.py:205-210` | **El propio commit da la cifra del fracaso: 7.575 mandadas, 35.845 llegadas** |

**Ninguna de las 14 se puso en el sitio donde nace el fallo** (`_preguntar_con_relevo`, línea 480).
Esa es, literalmente, la respuesta a "por qué nada funciona".

---

## 14. LO QUE AÚN FALTA (dicho claro, para no vender humo)

1. **No existe una vigía que mida el tamaño DENTRO del pasillo** (`len(prompt)` en la línea 480).
   Es la única medición que decide de verdad, y no la vigila nadie.
2. **Solo está medido el prompt de la puerta 1** (generar). Las **otras 8 puertas** no se han medido
   una por una con el paquete real.
3. **El caso "crear" (analista) sigue sin decidir**: cuánto material necesita sin romper la creación.
4. **Los avisos de capacidad guardados no llevan fecha ni número de ronda** y el archivo se
   sobrescribe: no se puede reconstruir una serie histórica con ellos.
5. **No consta una corrida real vista por Julio** donde un cerebro gratis escriba algo útil.
   Mientras eso no pase, todo lo demás es verde de laboratorio.

---

*Expediente escrito el 2026-09-09. Fuente: git log, memoria/FALLOS.json, memoria/LECCIONES.json,
contratos, vigías y medición propia reproducible. Nada aquí es opinión: cada línea tiene su archivo,
su commit o su medición. La sección 10 responde a la duda de Julio sobre el respaldo de los datos.*
