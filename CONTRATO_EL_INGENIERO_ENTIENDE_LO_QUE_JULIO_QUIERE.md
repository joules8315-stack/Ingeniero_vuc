# CONTRATO — EL INGENIERO ENTIENDE LO QUE JULIO QUIERE

**Julio, 2026-10-01:**

> *"El objetivo máximo es que cuando yo le diga al ingeniero que deseo, él lo traduzca, sepa en realidad qué quiero."*
>
> *"Nada dependa de tu memoria, ni de la de ninguna IA."*

---

## LA LEY

**Cuando Julio dice lo que desea, el Ingeniero no construye todavía. Primero traduce. Después construye. Después verifica. Después se repara solo.**

Y todo eso ocurre **por programa**, no por la memoria de ninguna IA. La IA solo entra donde un programa no alcanza.

---

## LOS ONCE PASOS DE JULIO (textuales, en este orden)

Cada paso nombra **su programa** (quién lo hace sin pensar) y **su vigía** (quién lo comprueba). Si un paso no tiene programa ni vigía, el paso no existe.

### Paso 1 — Verifica si sabe lo que se desea, y si existe material o toca crearlo
- **Qué hace:** antes de tocar nada, el Ingeniero comprueba dos cosas: (a) ¿entiendo de verdad qué quiere Julio?, (b) ¿ya existe la pieza, o hay que crearla?
- **Programa:** `ingeniero.py buscar-skill` + `cerebro/piezas.py::funcion_completa` (búsqueda por nombre y por lo que hace).
- **Vigía:** `vigias/test_vigia_antes_de_construir_se_busca.py`.
- **Ley que completa:** `CONTRATO_ANTES_DE_CONSTRUIR_SE_BUSCA`.

### Paso 2 — Analiza el problema
- **Qué hace:** descompone el deseo en problema concreto, con sus partes y sus límites.
- **Programa:** NO_ENCONTRADO (no hay programa declarado en el material para este paso).
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_COMO_EL_INGENIERO_CONSTRUYE_UN_PROYECTO`.
- **PREGUNTA_REQUERIDA:** ¿Con qué programa se analiza el problema, y con qué vigía se comprueba que el análisis es correcto?

### Paso 3 — Propone la arquitectura
- **Qué hace:** dice cómo va a quedar armado, antes de escribir una línea.
- **Programa:** NO_ENCONTRADO.
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_COMO_EL_INGENIERO_CONSTRUYE_UN_PROYECTO`.
- **PREGUNTA_REQUERIDA:** ¿Qué programa propone la arquitectura y qué vigía comprueba que la arquitectura respeta las leyes ya existentes?

### Paso 4 — Busca todos los recursos
- **Qué hace:** recorre el mapa y el disco y junta todo lo que ya sirve antes de crear nada.
- **Programa:** `mapa/inventario.py` + `cerebro/piezas.py`.
- **Vigía:** `vigias/test_vigia_antes_de_construir_se_busca.py`.
- **Ley que completa:** `CONTRATO_ANTES_DE_CONSTRUIR_SE_BUSCA`.

### Paso 5 — Organiza las tareas
- **Qué hace:** parte el trabajo en tareas, una a la vez, un encargo por archivo.
- **Programa:** NO_ENCONTRADO.
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_COMO_EL_INGENIERO_CONSTRUYE_UN_PROYECTO`.
- **PREGUNTA_REQUERIDA:** ¿Qué programa organiza las tareas y qué vigía impide que un encargo toque dos archivos a la vez?

### Paso 6 — Las delega al equipo diciendo el objetivo
- **Qué hace:** reparte el trabajo al equipo, pero diciéndole **el objetivo**, no los pasos sueltos.
- **Programa:** `cuerpo/obrero.py::trabajar` (con los parámetros `generador` y `auditor` usados de verdad).
- **Vigía:** `vigias/test_vigia_el_cerebro_es_el_que_pido.py` y `vigias/test_vigia_equipo_sirve.py`.
- **Ley que completa:** `CONTRATO_LOS_CUATRO_OBJETIVOS_ORQUESTADOS`.
- **Memoria de fallos que respeta:** no se quema una ronda si el auditor contesta roto (se le vuelve a preguntar); no se deja que el mismo cerebro se revise a sí mismo.

### Paso 7 — Antes establece candados y vigilantes
- **Qué hace:** antes de que el equipo empiece, ya están puestos los candados (lo que no se puede tocar) y los vigilantes (quién avisa si algo se rompe).
- **Programa:** NO_ENCONTRADO (no hay programa declarado que instale candados y vigías automáticamente al crear una pieza).
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_TODO_ENCHUFADO_NADA_DORMIDO`.
- **PREGUNTA_REQUERIDA:** ¿Qué programa instala el candado y el vigía en el momento en que nace una pieza, y qué vigía comprueba que ninguna pieza nace sin ellos?

### Paso 8 — Hay una hora de apuntes que recoge lo que no sirvió y replantea
- **Qué hace:** después de cada vuelta, se apunta lo que no sirvió y se replantea. Esa hora es obligatoria, no opcional.
- **Programa:** NO_ENCONTRADO.
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_MEMORIA_DE_FALLOS`.
- **PREGUNTA_REQUERIDA:** ¿Dónde vive el registro de "lo que no sirvió" y qué programa lo lee para replantear la siguiente vuelta?

### Paso 9 — En caso de acierto se verifica contra el resultado esperado (ontología) y se sella
- **Qué hace:** cuando algo sale bien, no se canta victoria: se compara contra el **resultado esperado** escrito de antemano (la ontología) y, si coincide, se sella.
- **Programa:** NO_ENCONTRADO — **medido: no existe campo de resultado esperado ni ontología en el código.**
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_MEMORIA_DE_FALLOS`.
- **PREGUNTA_REQUERIDA:** ¿Dónde se escribe el resultado esperado antes de construir, y qué programa lo compara con lo que salió para poder sellar?

### Paso 10 — Verifica que cada paso no dañe lo que ya sirve
- **Qué hace:** antes de dar por bueno un paso, se comprueba que no rompió nada de lo que ya funcionaba.
- **Programa:** NO_ENCONTRADO.
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_TODO_ENCHUFADO_NADA_DORMIDO`.
- **PREGUNTA_REQUERIDA:** ¿Qué programa comprueba, paso a paso, que no se dañó lo que ya servía, y qué vigía lo vigila?

### Paso 11 — Todo por programa y la IA solo donde un programa no alcanza
- **Qué hace:** por defecto, programa. La IA entra solo cuando un programa no puede. Cada vez que se usa IA donde podía haber programa, es un fallo.
- **Programa:** `skills/quien_sirve_de_verdad.py` (decide sin gastar ni una llamada a IA).
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_MENOS_IA_MAS_PROGRAMA`.
- **PREGUNTA_REQUERIDA:** ¿Qué vigía comprueba que no se gastó IA donde un programa bastaba?

---

## LO QUE SE SUMA A LOS ONCE PASOS

### Suma 1 — Toda pieza nace conectada, con candado y con vigía, y lo comprueba un programa
- **Programa:** NO_ENCONTRADO.
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_TODO_ENCHUFADO_NADA_DORMIDO`.
- **PREGUNTA_REQUERIDA:** ¿Qué programa comprueba que ninguna pieza nace dormida, sin candado o sin vigía?

### Suma 2 — Al sellar, la memoria se actualiza sola
- **Programa:** NO_ENCONTRADO.
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_MEMORIA_DE_FALLOS`.
- **PREGUNTA_REQUERIDA:** ¿Qué programa escribe en la memoria de fallos en el mismo acto de sellar, sin que nadie se acuerde de hacerlo a mano?

### Suma 3 — El creador de skills YA existe y no se vuelve a crear
- **Programa:** el creador de skills existente (NO_ENCONTRADO su nombre exacto en el material).
- **Vigía:** NO_ENCONTRADO.
- **Ley que completa:** `CONTRATO_EL_FABRICANTE_DE_HABILIDADES`.
- **PREGUNTA_REQUERIDA:** ¿Cuál es el nombre exacto del creador de skills que ya existe, para citarlo aquí y prohibir que se vuelva a crear?

---

## LO QUE ESTÁ MEDIDO HOY (por qué nace esta ley)

- **No existe campo de resultado esperado ni ontología en el código.** Sin eso, el paso 9 no se puede cumplir: no hay contra qué comparar el acierto.
- **Hay 11 piezas dormidas.** Piezas que existen pero no están enchufadas. Esta ley las obliga a nacer conectadas, con candado y con vigía.
- **Julio, 2026-10-01:** *"nada dependa de tu memoria, ni de la de ninguna IA"*. Por eso cada paso nombra su programa: si el programa no está, se pide, no se improvisa.

---

## A QUIÉN PUEDE DAÑAR TOCAR ESTO

Antes de sellar hay que declarar cuál de estos se revisó:

- `arnes/mostrador.py` — lo importa desde `cerebro/piezas.py`.
- `cerebro/piezas.py` — lo importa desde `mapa/inventario.py`.
- `mapa/inventario.py` — lo importa desde `cerebro/piezas.py`.

**Estado de la revisión:** NO_ENCONTRADO en el material. No se declara revisado nada que no se haya mirado.

---

## CÓMO SE COMPRUEBA ESTA LEY

- **Vigía principal:** NO_ENCONTRADO. Hay que crearlo.
- **PREGUNTA_REQUERIDA:** ¿Cuál es el vigía que comprueba que los once pasos se cumplen en orden, y que ninguna pieza nace sin candado, sin vigía y sin resultado esperado escrito?

**Vigía verde no es prueba.** La prueba es que Julio diga un deseo y el Ingeniero le devuelva, sin que Julio tenga que explicarlo dos veces, exactamente lo que quería.

---

## LEYES QUE ESTA COMPLETA

- `CONTRATO_TODO_ENCHUFADO_NADA_DORMIDO`
- `CONTRATO_MENOS_IA_MAS_PROGRAMA`
- `CONTRATO_LOS_CUATRO_OBJETIVOS_ORQUESTADOS`
- `CONTRATO_MEMORIA_DE_FALLOS`
- `CONTRATO_EL_FABRICANTE_DE_HABILIDADES`
- `CONTRATO_ANTES_DE_CONSTRUIR_SE_BUSCA`
- `CONTRATO_ANTES_DE_PREGUNTAR_SE_BUSCA`
- `CONTRATO_ANTES_DE_REPARAR_SE_BUSCA_LA_CURA`
- `CONTRATO_COMO_EL_INGENIERO_CONSTRUYE_UN_PROYECTO`

---

## LO QUE FALTA PARA QUE ESTA LEY SE PUEDA CUMPLIR

Los pasos 2, 3, 5, 7, 8, 9, 10, 11 (vigía) y las tres sumas no tienen programa ni vigía declarados en el material. Sin ellos, esta ley es papel. **El papel escrito envejece; el mapa y el disco no mienten.**

Antes de dar esta ley por buena, hay que responder cada PREGUNTA_REQUERIDA de arriba y escribir el nombre del programa y del vigía en su sitio.
