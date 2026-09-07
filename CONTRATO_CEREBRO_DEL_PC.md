# CONTRATO — EL CEREBRO DEL PC DE JULIO: SIEMPRE EL 3B

**Julio, 2026-09-07:**

> *"La IA de mi pc, debes ver por qué no sirve, si no sirve para eliminarla, dado que en todos
> los informes nunca sirve. Además, quedamos que se pasaría de 1,5B a 3B, mira si esto ya
> ocurre."*

Y después, con la medida delante:

> *"Legisla que siempre se use el cerebro de 3B, del pc."*

---

## LA LEY

**El cerebro local es SIEMPRE el de 3B. Se busca POR SU NOMBRE Y, SI NO APARECE, POR LO QUE
ES. Nunca por su posición en una lista.**

No se elimina: **sí sirve, y está medido.** Lo que no servía era cómo se elegía.

Es la misma regla que ya mandó Julio el 2026-08-31 para las funciones (*"se busca por nombre,
nunca por un número"*), aplicada aquí: **una posición en una lista se corre sola, igual que un
número de renglón. Un nombre no se mueve.**

### DOS CAMINOS, NUNCA UNO (Julio, 2026-09-07)

> *"Hablas mucho de nombrar, y muchos de los fallos pasados fue por ello: no encontraba el
> nombre. Debes agregar 'por nombre o por función', para que si no la encuentra de una forma
> la encuentre por otra y no frene el trabajo por un fallo falso."*

**El origen ya está localizado y medido, no supuesto:** el nombre que anuncia el programa
(`qwen2.5-3b-instruct`) **no es el mismo que el del archivo en el disco**
(`qwen2.5-3b-instruct-q4_k_m.gguf`). Buscar solo por nombre exacto habría fallado en cuanto
cambiara una letra, y habría parado todo por nada.

**El orden de búsqueda, siempre los dos caminos:**

1. **Por NOMBRE exacto:** `qwen2.5-3b-instruct`.
2. **Si no aparece, por LO QUE ES:** el que sea de 3B y sirva para conversar (su nombre lleva
   `3b`, y no es de búsqueda ni de embeddings).
3. **Si tampoco, por lo que HACE:** cualquiera de los que hay que responda de verdad,
   **excepto el 7B** (está medido que se estrella). Y **se dice cuál se usó y por qué**.
4. **Solo si ninguno responde** se avisa de que no hay cerebro local.

**Nunca se frena por no encontrar un nombre.** Un nombre que no aparece no es una avería: es
otra forma de escribirlo. Es la Regla 1 de `CONTRATO_CREAR_PIEZA_NUEVA` (*"primero se busca
POR FUNCIÓN, no por nombre"*) aplicada a los cerebros.

---

## LO QUE SE MIDIÓ (2026-09-07, prueba real, no opinión)

LM Studio **encendido — comprobado PROBANDO EL PUERTO, no supuesto ni leído de una variable de
entorno** (cura del fallo del 2026-08-20, en que estaba encendido y el Ingeniero no lo veía).
La misma tarea a cada modelo:

| Modelo | Tamaño | Tiempo | Resultado |
|---|---|---|---|
| **`qwen2.5-3b-instruct`** | 2,0 GB | **38,4 s** | **Respuesta correcta y bien formada** |
| `qwen2.5-7b-instruct` | 4,4 GB | 35,8 s | **SE ESTRELLA al cargar** (no cabe) |
| `qwen2.5-coder-1.5b-instruct` | 0,9 GB | 18,6 s | Correcta esta vez, pero **tiene fallo anotado por alucinar** |

**El equipo de Julio: 7,8 GB de memoria total, 3,6 GB libres. Gráfica integrada con 1 GB.**
El 7B pesa 4,4 GB: **no cabe en 3,6 GB libres**. No es configuración, es tamaño. Error exacto
de LM Studio: *"Failed to load model qwen2.5-7b-instruct... exited before becoming healthy.
exitCode=3221226505"* (desbordamiento de memoria de Windows).

---

## LOS DOS FALLOS QUE PROVOCAN ESTA LEY

**Fallo 1 — se elegía por POSICIÓN, no por nombre.** `cuerpo/obrero.py::_modelo_local` coge
**el primero de la lista** que no sea de búsqueda. Hoy ese primero es el 3B **de casualidad**.
Si LM Studio reordena, vuelve solo al 1.5B, que ya tiene fallo anotado por decir que una
función no existía cuando sí estaba (línea 202). **Elegir por posición es no elegir.**

**Fallo 2 — el respaldo escrito a mano era el malo.** Si la consulta al puerto falla, el
código cae en `qwen2.5-coder-1.5b-instruct`. El respaldo debe ser el bueno, no el peor.

---

## LA TABLA DE VERDAD

| Situación | Qué debe pasar |
|---|---|
| El 3B está con su nombre exacto y responde | **Se usa el 3B** |
| El nombre exacto no está, pero hay uno de 3B escrito de otra forma | **Se usa ese**, y se dice con qué nombre apareció. NO se frena |
| No hay ninguno de 3B, pero hay otro que responde | Se usa ese (menos el 7B) y **se dice cuál y por qué**. NO se frena |
| El 3B está en la lista pero no responde | Se pasa al siguiente camino. **No se cae al 1.5B en silencio**: se dice |
| Ninguno responde | Recién entonces se avisa de que no hay cerebro local |
| Alguien pide el 7B | **No se intenta.** Está medido que se estrella, y cada intento cuesta 36 segundos tirados |
| La consulta al puerto falla | El respaldo es el **3B**, nunca el 1.5B |

---

## LA MATRIZ — qué se cambia

| Qué | Dónde | Cómo |
|---|---|---|
| Elegir por nombre, no por posición | `cuerpo/obrero.py::_modelo_local` | Buscar `qwen2.5-3b-instruct` en la lista y devolverlo |
| El respaldo deja de ser el 1.5B | misma función | El valor por defecto pasa a ser el 3B |
| No intentar el 7B | misma función | Nunca se devuelve: está medido que no arranca |

---

## LO QUE NO CAMBIA (y está escrito para que nadie lo "arregle")

- **El local sigue siendo la RED DE SEGURIDAD, NUNCA el juez.** Va SIEMPRE el último y **nunca
  se acepta su palabra sin que otro cerebro la audite.** Que ahora sea el 3B y no el 1.5B **no
  lo asciende a juez**: sigue necesitando auditor.
- **Se detecta PROBANDO EL PUERTO** (`localhost:1234/models`), nunca por una variable de
  entorno, y por la vía directa propia (`obrero.preguntar_local`), nunca dependiendo del
  cerebro prestado de DMM.
- **Se le manda trabajo CORTO.** Midió 38 s en una pregunta de dos líneas: con un encargo
  grande tardaría minutos. Es su sitio (`CONTRATO_CUENTA_O_JUICIO`).
- **Los tiempos de espera no se tocan** (Julio, 2026-09-07).

---

## LO QUE LE TOCA A JULIO (se le guía, no se hace por él)

- Si quiere un cerebro local más listo, **el 7B necesita más memoria**: con 16 GB iría cómodo.
  Con los 7,8 GB de hoy, no.
- Alternativa sin gastar: una versión más comprimida del 7B (unos 3 GB). Cabría justo, pero
  iría lento.
- **Consejo honesto: no gastar en eso todavía.** Los cerebros gratis de internet aguantan
  194.000 letras y son mucho más capaces que cualquier cosa que quepa en este equipo. Su
  problema no es la potencia: es que se les llama demasiado seguido.

---

## A QUIÉN PUEDE DAÑAR

- A `cuerpo/obrero.py::preguntar_local` y a `disponible()`, que preguntan qué modelo hay.
  Ninguno se rompe: reciben un nombre igual que antes, solo que elegido y no tropezado.
- A los proyectos: **a ninguno**. El local es red de seguridad en todos por igual
  (`CONTRATO_UNA_LEY_PARA_TODOS`).

## CÓMO SE COMPRUEBA

`vigias/test_vigia_cerebro_del_pc.py`, determinista y **sin llamar a ningún cerebro** (se le da
una lista de mentira, que es como se prueba algo que no contesta siempre igual):
1. lista con 3B, 7B y 1.5B → devuelve **el 3B**;
2. lista sin el 3B → **no devuelve el 1.5B en silencio**: avisa;
3. la consulta al puerto falla → el respaldo es **el 3B**;
4. **nunca** devuelve el 7B.

**Vigía verde no es prueba.** La prueba es que Julio vea en su pantalla el nombre del modelo
que se está usando, y que ponga `qwen2.5-3b-instruct`.
