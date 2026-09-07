# CONTRATO — EL EQUIPO GRATIS ESCRIBE, EL DE PAGO ES EL ÚLTIMO RECURSO

**Julio, 2026-09-07:**

> *"Si se comprueba que el equipo sí puede escribir — antes no lo hacía porque lo hacía mal,
> pero si se corrige el fallo de por qué lo hacía mal, ahora sí puede escribir — y que lo
> copie un programa. **Esa es la petición desde el principio.** Pasé a realizar todo con
> DeepSeek porque el equipo no servía; una vez reparado esto, que siga el equipo gratis y
> DeepSeek se deje para cuando el equipo falle, pasando a ser la última instancia. Luego de
> una hora se verifica si el equipo se recuperó y vuelve el equipo a trabajar. Esto se debe
> medir ahora cuando se comience a crear DMM: cuánto demora el equipo en recuperarse, cada
> IA, para delegar así, rotarlos de modo que tengan el tiempo suficiente de respuesta y de
> recuperación."*

---

## LA LEY, Y SU CONDICIÓN

**El equipo gratis vuelve a escribir. El de pago pasa a ser el último recurso.**

**PERO la orden es CONDICIONAL, y así se cumple:** *"si se comprueba que el equipo sí puede
escribir"*. Primero se reparan los fallos, después **se mide**, y **solo si la medida dice que
sí**, se invierte el reparto. La prohibición del 2026-08-24 no se levanta por decreto: se
levanta con datos.

### Regla 1 — ÚLTIMO RECURSO NO SIGNIFICA QUE NO SE LE LLAME

**Confirmado por Julio el 2026-09-07.** Es un fallo ya cometido: se dio por cerrado un *"no hay
quien audite"* **sin haber llamado al de pago**, estando disponible y documentado justo para
eso. Al invertir el reparto, **DeepSeek sigue entrando SIEMPRE que el equipo falle**. No se
convierte en un adorno.

**Si un trabajo se queda sin hacer y no se le llamó, eso es un fallo, no un ahorro.**

### Regla 2 — La hora de gracia
Si el equipo falla y el de pago toma el relevo, **a la hora se vuelve a probar al equipo con
una tarea corta**. Si contesta bien, recupera el trabajo. No se le entierra por un mal rato.

### Regla 3 — Se rota, no se amontona
El trabajo se reparte **espaciando las llamadas**, para no volver a tocar el límite por minuto
de cada uno. Cada IA tiene su tiempo de respuesta y su tiempo de recuperación, **medidos**, y
se delega según eso.

### Regla 4 — Se mide con trabajo de verdad
La medición de cuánto tarda cada IA en recuperarse **se hace construyendo DMM**, no con
pruebas de laboratorio. Lo pidió Julio así.

### Regla 5 — Lo que NO cambia
- El bloqueo **F2** (nunca trabajar solo) sigue en pie.
- Quien revisa es **siempre otro distinto** del que escribió.
- Los **tiempos de espera por llamada** se quedan como estaban (Julio, 2026-09-07).

---

## LA TABLA DE VERDAD — las tres razones de la prohibición, y su estado

Julio anotó el 2026-08-24, con la medida delante:

> *"Medido tres veces el mismo día, con encargos POR DEBAJO del tope, los gratis devolvieron
> **propuesta vacía**, un **error de tamaño**, y **texto ilegible**. Se rendían igual."*

Son **tres causas distintas que nunca se aislaron**. La ley se levanta cuando estén las tres
resueltas y medidas:

| Razón | Cómo se quita | Estado |
|---|---|---|
| **Texto ilegible** | El traductor: rescata la respuesta rota y, si no puede, pide lo mismo en texto normal | pendiente |
| **Error de tamaño** | Rotación y espaciado: no volver a tocar el límite por minuto | pendiente |
| **Propuesta vacía** | El cuaderno de llamadas dirá si sigue pasando y cuándo | pendiente |

**Mientras quede una viva, la prohibición se queda, y se dice CUÁL sigue viva.**

---

## LA MATRIZ — qué hay que tener antes de invertir

| Hace falta | Para qué | Estado |
|---|---|---|
| `arnes/copista.py` | Que lo mecánico no lo escriba ningún cerebro | **HECHO y probado (2026-09-07)** |
| `vigias/test_vigia_copista.py` | Que el copista no deje de frenar nunca | en marcha |
| El traductor de respuestas rotas | Quitar la 3ª razón | pendiente |
| El cuaderno de llamadas | Saber POR QUÉ falla cada una. **Sin esto no se puede decidir nada** | pendiente |
| La rotación medida | Dejar de llamar cada minuto y medio | pendiente |

---

## LO QUE SE MIDIÓ Y OBLIGA A ESTO (fechas incluidas)

- **2026-09-06:** de 8 rondas pagadas, en **5** el encargo ya llevaba el texto de antes y el de
  después exactos. El cerebro de pago solo copió.
- **2026-09-06 / 07, 15 horas:** **40 siestas, 35 de tipo "minuto"**. Un cerebro que toca su
  límite duerme 90 segundos y vuelve a la fila; se le llama otra vez y vuelve a caer. **Cada
  vuelta de esa noria le cuenta como un fallo suyo.** Por eso Gemini figura con 96 % de fallos:
  no es que sea malo, es que se le llama a la puerta cada minuto y medio.

---

## A QUIÉN PUEDE DAÑAR

- A `cuerpo/obrero.py` (el orden de la fila) y a `cuerpo/cuotas.py` (las siestas y el reparto).
- A `CONTRATO_MAESTRO_AHORRO`, que se actualiza cuando la inversión ocurra.
- **A nadie más**: mientras la medida no lo permita, todo sigue exactamente como hoy.

## CÓMO SE COMPRUEBA

**La prueba no es una vigía verde. Es esta:** que en el veredicto de un trabajo real aparezca
**un cerebro GRATIS como obrero, no DeepSeek** — y que cuando ese gratis falle, **el de pago
entre igual** y el trabajo salga.

Su vigía comprueba lo que sí es determinista: que el de pago **siga estando en la fila** aunque
vaya el último, y que nunca se devuelva "no se pudo hacer" sin haberle llamado.
