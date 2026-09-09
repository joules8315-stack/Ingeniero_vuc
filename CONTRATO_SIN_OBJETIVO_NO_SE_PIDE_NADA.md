# CONTRATO — SIN OBJETIVO NO SE LE PIDE NADA A NADIE

**Julio, 2026-09-08**, y dice que lo ha repetido muchas veces:

> *"Debes darle un objetivo. Si no tiene un objetivo claro, ¿cómo va a comparar si sirve o no
> sirve, si funciona o no funciona? Esa es la idea de buscar un fallo: **compararlo con el
> resultado esperado**, para ver qué tan cerca está de lograrlo, o no."*

Y:

> *"Lo que falta decirle es **qué hacer en cada caso**, porque si no sabe qué hacer, claro que
> se romperá."*

---

## POR QUE ESTA LEY NO EXISTIA (se busco antes de escribirla)

Existe la ley de **confirmar el objetivo CON JULIO** antes de construir
(`arnes/candado_protocolo.py construir`). **Eso es otra cosa:** es pedirle permiso a él.

Faltaba la de **darle el objetivo A QUIEN HACE EL TRABAJO** — el obrero, el auditor, el
programa. Nadie puede juzgar si algo sirve si no sabe para qué tenia que servir.

---

## LA LEY

**A nadie se le pide un trabajo sin decirle TRES cosas: qué tiene que conseguir, qué hay ahora,
y qué se espera de él en ese caso concreto. Un encargo sin objetivo se RECHAZA antes de
mandarlo.**

### Regla 1 — Buscar un fallo es COMPARAR
No se busca un fallo "a ver qué encuentras". Se compara **lo que hay** con **lo que tenía que
pasar**. Sin resultado esperado no hay comparación posible, y lo que sale es una opinión.

### Regla 2 — Las tres cosas que van SIEMPRE en el encargo

| | Qué es | Sin ello pasa esto |
|---|---|---|
| **EL OBJETIVO** | Qué tiene que conseguirse, en una frase, medible | No hay contra qué comparar: se opina |
| **LO QUE HAY** | Cómo está ahora, con el texto de verdad | Juzga a ciegas, o se lo inventa |
| **QUÉ SE ESPERA DE ÉL** | Si tiene que reparar, crear, o juzgar algo ya hecho | Hace lo que cree, y se rompe |

### Regla 3 — El caso se dice, no se adivina
Reparar, crear y juzgar algo ya aplicado **son tres oficios distintos**. Si no se le dice en
cuál está, contesta al que se imagina. **Y contestar bien a la pregunta equivocada es fallar.**

### Regla 4 — Un encargo vacío es culpa de quien lo manda
Si al que trabaja se le manda un hueco donde debía ir el texto, **el fallo NO es suyo**. Se
apunta contra quien redactó el encargo.

### Regla 5 — EL QUE ASIGNA COMPRUEBA ANTES DE GASTAR (Julio, 2026-09-08)

> *"Para que asignen la IA, ya el que asigna debe tener la información pertinente completa, lo
> en verdad necesario: **saber si la IA tiene la capacidad, si no está dormida**, diciéndole
> claramente este es el resultado que queremos, se hizo esto y no sirvió por esto, repáralo."*

**Antes de llamar a nadie se comprueba, en este orden, y son todas cuentas:**

| | Qué se mira | Si no |
|---|---|---|
| 1 | **Cuánto pesa** el encargo, en letras | — |
| 2 | **Quién tiene llave** | se descarta |
| 3 | **Quién NO está dormido** | se descarta |
| 4 | **A quién le cabe** ese peso | se descarta |
| 5 | **Si alguien ya lo tiene asignado** | no se pide dos veces |

**Y si no queda nadie, SE DICE Y NO SE GASTA.** Callarse y mandarlo igual es lo que hacía el
sistema viejo: se saltaba a todos los gratis en silencio y acababa escribiendo y revisando el
mismo cerebro de pago. **Medido: dos o tres rondas por cada cambio, una noche entera.**

**Y el material va DEPURADO:** *"no solo que quepa, sino que venga lo necesario, y no con peso
innecesario"*. Recortar por lo bruto es trampa: si al recortar se cae el trozo que hay que
reparar, **el encargo cabe y no sirve para nada**. Primero se guarda lo necesario; lo que se
recorta es el relleno.

### Regla 6 — UNA VIGÍA RECIÉN NACIDA NO LLAMA A NADIE (Julio, 2026-09-08)

> *"Si nace roja, lo va a mandar para una IA, y no es así; **debe ser en la segunda vuelta**,
> porque si nace roja lo manda enseguida para la IA, y es lo que no queremos. Estaríamos dando
> una orden contradictoria."*

**Lo cazó antes de que se construyera, y tenía toda la razón.** El método de esta casa dice que
**la vigía nace roja a propósito**. Si el criterio fuera *"rojo = llamar a una IA"*, cada vez
que se escribe una prueba nueva se dispararía una IA a reparar **algo que todavía no existe**:
se estaría pagando por el paso 1 del propio método, y encima la IA no encontraría nada.

**El criterio, y la casa YA sabe distinguirlo** (`arnes/guardia_de_guardado.py::_vigias` le
pregunta al guardado si esa vigía es nueva o si ya estaba):

| Tipo de rojo | Qué es | Quién entra |
|---|---|---|
| **Recién nacida** (la pieza aún no existe) | El método, no un fallo | **Nadie. Cero gasto** |
| **Estaba verde y se puso roja** | Algo se rompió de verdad | La IA |
| **Sigue roja tras un intento** | El arreglo no lo consiguió | La IA, con el mensaje nuevo |

**Regla que se suma:** un rojo que no se repite **es ruido, no un fallo**. Ya está medido en
esta casa que el guardia llegó a probar archivos a medio escribir. Antes de dar un rojo por
bueno, **se repite**.

---

## EL FALLO REAL QUE LA HACE NACER (2026-09-08, y lo cazó Julio)

Se le pidió al auditor que juzgara un enchufe **ya aplicado**. Se le mandó:

- **objetivo:** *"juzga si está bien puesto"* → **eso no es un objetivo, es un deseo**
- **lo que hay:** el hueco del "antes" y del "después" **EN BLANCO**
- **qué se espera de él:** nada; su encargo empieza diciendo *"otro modelo propuso una
  reparación"*, así que se puso a buscar un cambio que no le habían enseñado

**Resultado, dos veces seguidas, con sus palabras textuales:**
> *"la propuesta no realiza ningún cambio: el texto nuevo es idéntico al texto viejo"*
> *"solo afirma que el trabajo ya está hecho, por lo que no se puede auditar ni aprobar"*

**Julio lo vio al instante:** *"¿le estás pidiendo a un auditor que audite algo que no cambió?
Es estúpido."* Y tenía razón: **el cambio existía, en el disco. Simplemente no se lo enseñé.**

**El auditor no falló. Contestó bien a la pregunta equivocada.** Y la pregunta la escribí yo.

**Lo que casi hago mal, y es lo grave:** iba a proponer **cambiar el encargo del auditor**, es
decir, tocar la pieza que funcionaba, para arreglar un fallo que estaba en el encargo. Habría
sido reparar al sano.

---

## LO QUE CAMBIA

Un encargo, para cualquiera —obrero, auditor o programa— lleva SIEMPRE:

```
OBJETIVO : que tiene que conseguirse, medible
LO QUE HAY: el texto de verdad, no un resumen
TU PAPEL : reparar | crear | juzgar algo ya hecho
```

Y para el caso de **juzgar algo ya aplicado**, que era el que se rompía, se le manda el código
de antes y el de ahora, y se le dice: *"esto YA está aplicado; dime si cumple el objetivo y si
rompe a algún vecino"*. **No hace falta tocarle el encargo: hace falta llenárselo.**

## CÓMO SE COMPRUEBA QUE SE CUMPLE

Una vigía que:
1. manda un encargo **sin objetivo** y comprueba que **se frena antes de gastar**;
2. manda uno **sin el texto de lo que hay** y comprueba que **se frena**;
3. manda uno **completo** y comprueba que **pasa**.

**Vigía verde no es prueba.** La prueba es que Julio no vuelva a tener que decir "es estúpido".
