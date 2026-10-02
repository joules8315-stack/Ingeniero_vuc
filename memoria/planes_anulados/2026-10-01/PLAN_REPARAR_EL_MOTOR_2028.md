# PLAN — QUE EL INGENIERO TRABAJE BIEN (eje: desatascar el motor de reparación)

Julio, 2026-08-31. Prioridad que Julio ordenó: "lo más importante es reparar que el ingeniero
trabaje bien. Averigua cuáles son las cosas a reparar, cuáles faltan y cuáles está ejecutando
Claude, para crear un plan, dárselo a Claude, que lo apruebe y que yo [Continue] lo ejecute."

## Por qué esto es lo primero

El motor de reparación está atascado y quema rondas sin cerrar nada. La cadena de `ESTADO.json`
y el `loop.log` de hoy lo prueban: `[LOOP r1..r5]` sobre `obrero.py`, cinco rechazos del juez
consecutivos. Mientras el motor no pueda cerrar UNA reparación de verdad, todo lo demás (el
candado del buzón, el compañero, las 7 puertas, Foto Informe) no se puede guardar, porque el
guardián exige vigía verde. Reparar el motor destraba el resto.

## LO QUE ESTÁ EJECUTANDO CLAUDE AHORA (vía el loop automático)

El encargo del 2026-08-31 11:04 de Julio está corriendo en el bucle, sobre `cuerpo/obrero.py`:

> "la función `trabajar` acepta los parámetros `generador` y `auditor` pero no los usa en
> ningún sitio del cuerpo"

El juez lo rechazó 5 veces. Causa de fondo encontrada leyendo el código: `trabajar()` llama
`_preguntar_con_relevo(_prompt_obrero(...), 0.2, pesado=True)` para GENERAR (que por "lo pesado
va a DeepSeek" siempre manda a DeepSeek e IGUALA el parámetro `generador`) y después llama
`_preguntar_con_relevo(_prompt_auditor(...), 0.1, evitar=quien_gen)` para AUDITAR (nunca usa el
parámetro `auditor`). Los parámetros se aceptan pero se tiran.

## LO QUE FALTA Y ES DE JULIO / DE CLAUDE (confirmado en DONDE_QUEDAMOS.md y ORDENES.md)

1. **El tramo de líneas / texto-vs-número** → a medias (el auditor ya juzga por texto; falta
   que el OBRERO entregue texto y que el motor se cierre con esa pieza).
2. **El vigilante que autoriza desde el plan aprobado** → legislado, NO construido.
3. **Que no le pida permiso a cada instante** → falta construir el vigilante + lista de
   permitidos de Windows (Julio ya la entregó).
4. **Pruebas reales con navegador del Ingeniero** → NO EMPEZADO.
5. **Que Julio pruebe `python ingeniero.py trabaja` con sus ojos** → pendiente de Julio (M.1).
6. **La vigía de las 7 puertas** → escrita y roja, apartada; hay que devolverla y verificar verde.
7. **Foto Informe** (botón títulos + enlaces Word) → sin guardar, requiere el portero encendido.

## QUÉ HACE ESTA SESIÓN (lo que me asigné, bajo aprobación de Claude)

Solo el punto que destranca el motor: **hacer que `trabajar()` respete los parámetros
`generador` / `auditor` que recibe, y que si no puede respetarlos, lo avise.** No tocar nada más
sin aprobación.

### El cambio concreto (en `cuerpo/obrero.py`, función `trabajar`)

1. **GENERAR**: pasar `generador` a `_preguntar_con_relevo` como `primero=` (respetándolo sin
   por eso forzar que deba ser DeepSeek: el `pesado=True` ya lo manda a DeepSeek igual, pero si
   Julio pidió un generador concreto, se intenta él primero). Si el generador pedido NO está
   disponible, se deja que el relevo elija y se agrega un AVISO.
2. **AUDITAR**: pasar `auditor` como `primero=` a la llamada del auditor, **sabiendo que el
   auditor nunca puede ser el que generó** (si `auditor == quien_gen`, se lo descarta como
   auditor y se elige a otro). Si el auditor pedido no está disponible, aviso.
3. Ningún cerebro se paga dos veces por el mismo rol; el `evitar=quien_gen` sigue valiendo.

### Qué NO se hace en esta sesión (queda listado para después, con su aprobación)

- terminar la reparación del buzón (ya quedó a medias, espera aprobación aparte)
- construir el vigilante de autorización
- la vigía de las 7 puertas
- pruebas con navegador
- Foto Informe

## EVIDENCIA de que el bug existe (para que el revisor la mire)

`cuerpo/obrero.py`, al final de `trabajar()`: el resultado guarda `"obrero": quien_gen` y
`"auditor": quien_aud`, pero `generador` y `auditor` (los parámetros) se aceptan y no se
consultan en ningún `_preguntar_con_relevo` de GENERAR ni de AUDITAR.

## APRUEBA / RECHAZA

Deja aquí el visto bueno de Claude por el canal. Si aprueba, ejecuto exactamente esto, pongo
vigía que nace roja, corro, y le cuento a Claude qué/dónde/por qué/cuándo.
