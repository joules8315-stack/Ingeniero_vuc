# CONTRATO — ANTES DE PREGUNTARLE A JULIO, SE BUSCA EN LO QUE YA DIJO

**Fecha:** 2026-09-12
**Lo dijo Julio, molesto y con razon:**

> "Repite las tres preguntas, solo si no existe la respuesta dentro de las leyes, objetivos,
> tablas, matrices. Si no lo encuentras, hazlas de nuevo."

---

## EL FALLO QUE LO ORIGINA (medido, esa misma noche)

Se le hicieron a Julio **tres preguntas**. De las tres, **dos ya las habia contestado el mismo**,
y estaban escritas, con fecha, en sus propias leyes:

| La pregunta que se le hizo | Donde estaba ya la respuesta |
|---|---|
| "¿Enciendo las imagenes o espero?" | `CONTRATO_FLUJO_DMM.md`: *"Cuota FREE (real): 3-5 imagenes/dia"*. **Decidido.** |
| "¿Que hacemos con la entrada por contraseña?" | `CONTRATO_ACCESO_Y_GOOGLE.md`, 2026-07-24: *"DECISION — el login se hace con Supabase Auth"*. **Decidido.** |
| "¿Que buzon usamos para el captador?" | `CONTRATO_CAPTADOR_POLITICAS.md`: *"PENDIENTE: conectar el buzon real"*. **Esta si.** |

**Dos de cada tres preguntas eran ruido.** Y Julio lleva dias diciendo *"sigo repitiendo cosas"*:
preguntarle lo que ya contesto **es hacerle repetir**. Es el mismo dano que perder sus ordenes,
solo que por el otro lado.

## LA LEY

**Antes de preguntarle NADA a Julio, se busca en lo que ya dijo.** En este orden:

1. **Los contratos** (`CONTRATO_*.md`) del proyecto que toca y de la herramienta.
2. **Los planes** (`PLAN_*.md`) y el mapa del proyecto.
3. **El registro de lo que Julio ya dijo** (`memoria/LO_QUE_JULIO_YA_DIJO.json`).
4. **Las tablas y matrices** de decision que existan.

Solo si **no aparece en ninguno de los cuatro**, se pregunta.

Y cuando se pregunta, se pregunta **diciendo donde se busco**. Asi Julio sabe que no es pereza:

> "Busque en las leyes del negocio, en los planes y en el registro de lo que ya dijiste, y esto
> no esta decidido en ninguno. Por eso te lo pregunto."

## LO QUE ESTA PROHIBIDO

- Preguntar sin haber buscado. Cada pregunta evitable es una repeticion que se le impone a Julio.
- Preguntar por una credencial dentro del chat. Lo prohibe `CONTRATO_CREDENCIALES.md`: se le dice
  **donde escribirla el mismo**, y nunca pasa por la conversacion.
- Amontonar preguntas "por si acaso". Si tres preguntas se pueden reducir a una buscando, se
  reducen a una.

## Y AL REVES, QUE TAMBIEN CUENTA

Si al buscar se encuentra la respuesta, **se actua con ella**, no se pide confirmacion de algo ya
decidido. Una decision escrita de Julio es una decision, no un borrador. Volver a consultarla es
otra forma de hacerle repetir.

## LOS PERMISOS SE BUSCAN ANTES DE PEDIRSE (Julio, 2026-09-12)

> "No tanto que no pida permisos: **debe primero buscar en los archivos si eso es permitido**,
> porque no hacemos nada que este pidiendo permisos que no estan autorizados. **Lo mismo para ti.**
> Ya sobre esto hemos legislado; ahora **haz que el ayudante lo cumpla siempre**."

**El caso que lo origina, y es instructivo porque salio medio bien:** el ayudante buscó en los
archivos antes de pedir permiso, citó el contrato que manda y el encargo vigente, y **aun asi
pidio permiso** para mandar un reporte que el mismo acababa de demostrar que estaba permitido.

Hizo la primera mitad y le falto la segunda. **Buscar sirve para DECIDIR, no para acompanar la
pregunta.**

### Los cuatro pasos, en orden

1. **Se busca** en los contratos, los planes y lo que Julio ya dijo.
2. **Si dice que si** → se hace. **No se pregunta.** Preguntar por algo ya autorizado le hace
   perder el tiempo igual que preguntarle lo que ya contesto.
3. **Si dice que no** → no se hace, y se dice **que ley lo prohibe**.
4. **Solo si no aparece en ninguno** → se pregunta **a la direccion**, diciendo donde se busco.
   Nunca a Julio ([[CONTRATO_A_JULIO_NO_SE_LE_PIDE_FIRMAR_LO_QUE_NO_PUEDE_JUZGAR]]).

### Lo que YA esta permitido y no se vuelve a preguntar nunca

Esta lista es corta y cerrada a proposito, para que se lea entera de un vistazo y nadie tenga que
recordarla: todo lo de aqui es **medir**, y medir no toca nada ni puede romper nada.

- leer cualquier archivo de los dos proyectos,
- correr las suites de pruebas,
- escribir en la carpeta temporal,
- mandar lo que sea por el canal,
- usar cualquier contador o medida que ya exista.

### Lo que sigue necesitando el si de la direccion

- tocar cualquier archivo de los proyectos,
- borrar cualquier cosa,
- cambiar cualquier configuracion.

Y se pide **diciendo que archivo, que cambia y a quien puede danar**. Sin esas tres cosas, no es
una peticion: es un cheque en blanco.

## COMO SE COMPRUEBA QUE SE CUMPLE, SIN QUE NADIE SE ACUERDE

NO con un contador que haya que subir a mano: asi murio el contador de repeticiones de Julio, y
asi mueren todos. Se comprueba leyendo lo que el propio texto deja escrito por si mismo, que esta
ahi lo mire alguien o no.

Cada vez que se le formula a Julio una pregunta marcada como tal (`PREGUNTA_REQUERIDA`), en ese
mismo texto tiene que constar donde se busco antes. El guardian lo cuenta solo: o la constancia
esta escrita, o no esta. Una pregunta sin ella es una pregunta sin buscar, y queda senalada.

**Guardian:** `vigias/test_vigia_antes_de_preguntar_se_busca.py`

## RELACION CON LAS OTRAS LEYES

- **Ley 1 de Julio, "nunca asumir"**: sigue intacta. Esta ley no dice que se adivine; dice que se
  BUSQUE. Si tras buscar no esta, se pregunta, exactamente como manda la ley 1.
- [[CONTRATO_APUNTA_Y_REPARA]]: misma raiz. Encontrar sin cerrar, y preguntar sin buscar, son las
  dos formas de parecer que se trabaja sin avanzar.
