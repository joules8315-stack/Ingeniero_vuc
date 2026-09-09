# CONTRATO — LA FOTOCOPIA NO SE PAGA

**Julio, 2026-09-08**, y no es la primera vez que lo dice:

> *"Quedó que lo que se podía hacer con programa, se hacía, así salía gratis. ¿Qué pasa, otra
> vez lo tengo que repetir? ¿Cuántas veces lo tengo que repetir para que lo tomes en serio?"*

Y al pillarlo:

> *"Legisla bien esa mierda, que no toque volver a repetirlo. Créala, ponle candado, vigía, y
> mira que se cumpla, que se conecte, que no se te olvide en la puta vida."*

---

## LA LEY

**Si el encargo ya lleva dentro el texto de ANTES y el texto de DESPUÉS exactos, eso NO es
trabajo de cerebro: es una fotocopia. La aplica un PROGRAMA. Mandarla a una IA es un FALLO.**

No es una recomendación ni una preferencia de estilo. **Es un fallo, y se cuenta como fallo.**

### Regla 1 — La pregunta, antes de llamar a nadie
Antes de mandar un encargo al equipo se responde una sola cosa:

> **¿Ya sé exactamente qué texto quito y qué texto pongo?**

Si la respuesta es **SÍ**, no se llama a ningún cerebro. Va al copista.
Si la respuesta es **NO** —hay que decidir QUÉ está mal o CÓMO se arregla— eso sí es juicio, y
ahí sí entra el equipo.

### Regla 2 — Quién decide sigue siendo el equipo
El copista **NO decide nada**. Aplica lo que ya está decidido. Lo que se ahorra es la
FOTOCOPIA, no la revisión. Si el cambio necesitaba juicio, ese juicio se pide antes, igual que
siempre. La ley 6 de Julio (siempre en equipo) sigue entera: cambia el oficio, no el equipo.

### Regla 3 — Se cuenta, y duele
Cada encargo mandado al equipo llevando ya el texto viejo y el nuevo exactos **se apunta como
fallo**. Una ley que no se mide no se cumple.

### Regla 4 — EL MAPA DE QUÉ ES PROGRAMA Y QUÉ ES IA (Julio, 2026-09-08)

> *"Mira todo, absolutamente todo, con cifras, y crea un mapa de todo lo que se puede hacer con
> programa y todo lo que en verdad necesita una IA, y comienza a conectar."*

**Después de cablear, y antes de seguir construyendo, se hace el barrido completo del proyecto,
pieza por pieza, con cifras**, y queda escrito en un mapa con tres columnas:

| Columna | Qué dice |
|---|---|
| **PROGRAMA** | Da siempre el mismo resultado. Cuenta, compara, lista, comprueba, copia. **Gratis** |
| **IA** | Hay que decidir algo que no está escrito en ninguna ley ni material. **Juicio** |
| **¿La llama alguien?** | Si nadie la llama, está **sin terminar** (regla 6 de `CONTRATO_CREAR_PIEZA_NUEVA`) |

**Con cifras, no con impresiones:** cuántas piezas hay, cuántas son programa, cuántas piden una
IA de verdad, y cuántas están dormidas. **Y entonces se conecta**, empezando por las que no
necesitan ninguna IA, porque esas salen gratis.

**Primer barrido, ya hecho en la aplicación de marketing (2026-09-08):** 82 piezas, **22
dormidas**, de las cuales **solo 3 dependen de credenciales de Julio**. Y de las dormidas
grandes, **cuatro no necesitan ninguna IA**: publicidad, las metas, el CRM y el jefe que
coordina. Son cuentas puras, ya programadas. Faltaba el cable.

---

## LO MEDIDO EL 2026-09-08 (por eso nace, y con números)

**El mismo cambio, hecho de las dos maneras:**

| | Con el equipo de IA | Con el programa |
|---|---|---|
| Intentos | **4 rondas** | **1** |
| ¿Entró? | **No** | **Sí, a la primera** |
| Tiempo | Toda la madrugada | **1 segundo** |
| Coste | Dinero de Julio | **Cero** |
| Fallos por el camino | Se comió las comillas · no encontró el texto por una raya larga · en dos rondas escribió y revisó el mismo cerebro | Ninguno |

**Y esa noche TODOS los encargos llevaban el texto viejo y el nuevo exactos.** Todos eran
fotocopias. Se pagaron todas.

## POR QUÉ NO SE USABA EL PROGRAMA QUE YA EXISTÍA

`arnes/copista.py` existe desde antes, hecho **justo para esto**. Su propia documentación lo
dice: *"de las 8 rondas pagadas, en 5 el encargo ya llevaba dentro el texto de antes y el de
después exactos: el cerebro solo los copió. Cinco vueltas pagadas por una fotocopia."*

**Y estaba ROTO.** Al lanzarlo como dice su propia documentación reventaba en el arranque
(`No module named cuerpo`), porque no sabe encontrar su casa. Construido, dormido **y
averiado**. Nadie lo usó nunca porque al primer intento se rompía.

**Lección que se suma a la regla 6 de `CONTRATO_CREAR_PIEZA_NUEVA` (nace conectada o no nace):
una pieza no está terminada hasta que se ha USADO una vez de verdad.** Verde en su vigía no
basta: hay que lanzarla como la va a lanzar quien la use.

---

## CÓMO SE HACE CUMPLIR (candado, no recordatorio)

1. **El copista se repara** para que arranque solo, sin que nadie tenga que saber ponerle el
   camino a mano.
2. **Candado en `arnes/candado_terminal.py`**: si se va a lanzar el equipo con un encargo que
   ya trae el texto de antes y el de después exactos, **se FRENA** y se dice que eso lo hace el
   copista, gratis.
3. **Vigía**: se comprueba que el candado muerde de verdad — que frena una fotocopia y que
   **deja pasar** un encargo de juicio. Un candado que frena lo legítimo enseña a ignorarlos
   todos.

## CÓMO SE COMPRUEBA QUE SE CUMPLE

Una vigía que:
1. lanza un encargo **con** texto viejo y nuevo exactos y comprueba que **se frena**;
2. lanza un encargo **sin** ellos (de juicio de verdad) y comprueba que **pasa**;
3. corre el copista **como lo lanzaría cualquiera** y comprueba que **no revienta al arrancar**.

**Vigía verde no es prueba.** La prueba es que Julio no vuelva a tener que preguntar por qué se
le pagó a una IA para hacer una fotocopia.
