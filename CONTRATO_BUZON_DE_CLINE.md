# CONTRATO — EL BUZON DE CLINE SE VE SIEMPRE, CON CANDADO

**Julio, 2026-08-31:** *"Cuando trabaje contigo, debes estar mirando el buzón... crea un mecanismo
que te active cuando Claude esté trabajando, legislalo, pon candado y crea vigía. No debe depender
de que te acuerdes."*

## LEY — CLINE NO TRABAJA SIN VER EL BUZÓN

**El fallo medido:** el canal (`canal.py`) deja los mensajes de Claude para Cline en disco, pero
Cline no los veía salvo que Julio le dijera *"mira el buzón"*. Eso dependía de que Cline se
acordara, y ya está apuntado que **depender de que la IA se acuerde no funciona**.

**La ley:** antes de trabajar, y al terminar, Cline **mira el buzón**. Si hay un mensaje de otro
agente para Cline **sin leer**, **no se trabaja** hasta verlo y responderlo.

**Quién lo hace cumplir — un candado, no la memoria:**
`arnes/candado_buzon.py`, enchufado a:
- `UserPromptSubmit` (cuando arranca el turno): si hay encargos para Cline sin leer, **bloquea** y
  los muestra.
- `Stop` (cuando termina): si quedó algo sin ver, no se puede cerrar el turno.

**Qué cuenta como "sin leer":** un mensaje en el canal dirigido a `cline`/`4ojos`/`todos` que no
esté marcado `leido` y que venga de otro agente (no del propio Cline). Al leer el buzón con
`canal.py leer`, se marca `leido` y el candado suelta.

**Lo que NO se hace (para que el candado no se vuelva ruido):**
- **No bloquea a Claude** por los mensajes que él mismo le manda a Cline.
- **No bloquea** si el buzón está vacío (un candado que grita siempre se acaba apagando).
- Tiene tope de bloqueos seguidos y salida por la autorización de Julio, como todos los candados.

**Quién lo vigila:** `vigias/test_vigia_buzon_de_cline.py` (nació roja en el cableado y quedó verde):
que bloquee con un mensaje de claude→cline sin leer, que no bloquee sin mensajes, que no bloquee a
Claude por sus propios mensajes, y que esté enchufado a `UserPromptSubmit` y a `Stop`.
