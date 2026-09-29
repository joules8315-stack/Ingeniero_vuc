# EL METODO ANTE UN PROBLEMA — ley de Julio, 2026-09-29

**Quien la dicta:** Julio, el 2026-09-29, despues de repetirla "infinidad de veces".
**A quien obliga:** a TODAS las IA que trabajen en cualquier proyecto suyo. Sin excepcion y sin salto.
**Por que existe:** porque sin ella las IA **especulan**, y especular cuesta tiempo y dinero.
**Como se hace cumplir:** con un PROGRAMA, no con este documento. Un documento es memoria, y la
evidencia de hoy es que la memoria no sirve. La orden es `H5`.

---

## LOS CUATRO PASOS DE JULIO (el original, no se toca)

1. **¿Cual es el problema?** Generalmente lo muestra el usuario o lo muestran los vigilantes.
2. **¿Que causa el problema?** Aqui se investiga la CAUSA RAIZ. ¿Ya se presento antes? ¿Ya se
   hicieron reparaciones? ¿Que necesito para repararlo? ¿Lo tengo?
3. **¿Donde esta el problema?** Se AISLA: que archivos toca, el flujo, que podria danar, como
   interactua con otros flujos.
4. **¿Cuando lo ejecuto?** Solo si se reconocio TODO en absoluto: se legisla, se pone el candado, se
   crean las vigias, se mira si lo puede hacer un programa, y se ejecuta. Preciso, quirurgico.

---

# LA LEY QUE EVITA MORDERSE LA COLA (Julio, 2026-09-29)

Cuando un freno para una reparacion, la IA repara el freno con este mismo metodo. **Eso puede girar
para siempre.** Julio lo pidio expreso, y asi se evita:

## Regla 1 — CADA INTENTO DEJA ESCRITO EL CAMINO Y POR QUE FALLO

Se apunta la huella del camino (la pieza y el modo de arreglarla), el motivo del fallo y la fecha.

**Esto YA EXISTE** en la herramienta: `cuerpo/capataz.py`, funciones `huella_de`,
`anotar_huella_fallida` y `ya_fallo`, sobre `memoria/HUELLAS_QUE_FALLARON.jsonl`. No se duplica.

> **MEDIDO el 2026-09-29, y es el fallo que esta ley repara:** ese registro tiene 40 caminos escritos,
> y **el ultimo es del 2026-09-28. Hoy no se apunto ni uno**, porque solo escribe el ciclo automatico y
> hoy todas las rondas se lanzaron a mano. **El freno del bucle existia y estuvo ciego todo el dia.**
> Por eso se repitio DOS veces el mismo camino equivocado y se perdieron seis vueltas.

## Regla 2 — UN CAMINO QUE YA FALLO NO SE VUELVE A INTENTAR

Antes de lanzar, se consulta ese registro. **Tambien en las rondas lanzadas a mano**, que es donde hoy
no se consultaba nada.

Y la huella no puede enganarse cambiando las palabras: se calcula sobre **la pieza y el modo de
arreglarla** (el renglon que se cambia), no sobre el texto del encargo. Si no, basta reescribir la
frase para que el mismo error pase por nuevo.

## Regla 3 — EL AVANCE SE MIDE EN HECHOS NUEVOS, NO EN INTENTOS

Un intento que falla **tiene que dejar un hecho nuevo**: una medicion, el nombre de una prueba roja, un
motivo. **Si un intento falla sin dejar ningun hecho nuevo, eso es morderse la cola: se para.**

Es el unico limite que no se puede burlar, porque no cuenta vueltas: cuenta si se aprendio algo.

## Regla 4 — TRES FRENOS ENCADENADOS: SE SUBE, NO SE BAJA

Reparar un freno que produce otro freno es profundidad dos. **En el tercero se para de bajar y se
sube**: una cadena de tres frenos esta diciendo que la causa esta mas arriba, no mas abajo.

## Regla 5 — TRES CAMINOS DISTINTOS FALLIDOS: EL DIAGNOSTICO ESTA MAL

Si tres caminos distintos fallan sobre el mismo problema, **no se prueba un cuarto**: se vuelve al
paso 2 y se MIDE otra vez, porque lo que esta equivocado es la causa, no el arreglo.

**Esto tambien existe ya**: `cuerpo/capataz.py`, funcion `bucle`, para con
`PARADO: 3 FALLOS DEL MISMO TIPO`. Lo que falta es que valga tambien fuera del ciclo automatico.

## Regla 6 — UN FRENO SIN VOZ ES EL PRIMER DEFECTO A REPARAR

Si un freno no dice **por que** freno, no se adivina: **lo primero que se repara es darle voz.**

> **Ejemplo medido hoy:** el guardado devolvia *"4 grupos, 4 rojos"*. Se le dio voz y ahora dice **el
> nombre** de la prueba que lo frena. Eso convirtio nueve minutos de medicion en un renglon, y en
> cuanto hablo **revelo que el equivocado era yo**. Sin voz, habria seguido dando vueltas.

---

## LOS CUATRO ANADIDOS AL METODO, cada uno de un fallo MEDIDO el 2026-09-29

### Al paso 2 — LOS CAMINOS CERRADOS
Antes de proponer nada: **¿esto ya se intento y NO funciono?** No es lo mismo que "¿ya se presento
antes?". Un problema conocido puede tener caminos ya probados y fallidos.

> Se intento DOS veces subir el tope del recorte. Las dos veces se aprobo y las dos se devolvio. Al
> tercer intento se supo por que: rompia tres leyes del reparto. **Seis vueltas.**

### Al paso 2 — LA CAUSA SE MIDE, NO SE LEE
El paso 2 termina con **una medicion que podia salir al contrario**. Leer produce una hipotesis; medir
produce una causa. Si la comprobacion no podia fallar, era una opinion con formato de dato.

> La causa real la encontro preguntarle a la pieza en vivo que conservaria: contesto que solo el nombre
> del archivo, y que la funcion pedida NO estaba en su lista.

### Al paso 4 — LA VIGIA SOLO CUENTA CON SABOTAJE PROBADO
**Roja antes** (y por su motivo), **verde despues**, y **roja otra vez al deshacer el arreglo**. Sin la
tercera no se sabe si mira la reparacion o mira a otro lado.

> Una vigia nacio roja por mal montaje: dos vueltas. Otra vez, 31 comprobaciones siguieron verdes con
> el arreglo **eliminado**. **Y al contrario:** una ronda donde el programa demostro las tres cosas
> **no pago revision de IA**. El sabotaje probado es mas barato que la opinion comprada.

### Al paso 4 — LA MANO MAS BARATA QUE PUEDA HACERLO
Orden fijo, y se baja un escalon solo cuando el de arriba **no puede**:
**1)** un programa que comprueba solo · **2)** el cerebro barato, para volumen y lectura ·
**3)** el de pago, cuando la precision decide o el barato ya fallo · **4)** la IA que dirige, solo para
decidir y hablar con Julio.

> El revisor gratis se llevo el **82% del reloj** (55,7 s por llamada contra 5,1 s del de pago).

---

## EL PASO 5, QUE FALTABA: ¿CUANTO COSTO?

Cada reparacion apunta **vueltas gastadas** y **minutos de reloj**. Sin numero, "el metodo funciona" es
una creencia. Es la senal que pidio Julio.

---

## LO QUE SE DECLARA FUERA — la frase que evita la mitad de los rechazos

El encargo dice tambien **lo que NO se va a tocar**: un arreglo, un archivo, y la lista de lo que se
queda igual.

> Tres rechazos seguidos hoy por pedir cosas de mas. Al declarar lo que quedaba fuera, la misma
> reparacion salio aprobada.

---

## LAS SIETE COSAS QUE EL PROGRAMA EXIGE ANTES DE DEJAR ARRANCAR

| Lo que exige | Paso |
|---|---|
| El problema, con las palabras de quien lo reporto | 1 |
| La EVIDENCIA medida: que se midio, con que, y que contesto | 2 |
| Que no repita un CAMINO CERRADO ni una huella que ya fallo | 2 |
| A quien puede danar, y el flujo | 3 |
| Su vigia declarada, y la promesa de sabotaje | 4 |
| Lo que NO se toca | 4 |
| Quien es la mano mas barata que puede hacerlo | 4 |

Si falta alguna, **no se llama a ningun cerebro**: ahi es donde se quema el dinero.

Va **dentro del comando con que se pide una reparacion**, que es la unica puerta por la que pasan todas
las IA. Un candado de Claude solo obliga a Claude: Codex y las demas no pasan por ahi.

---

**Y la ley que manda sobre todas, que no cambia:** vigia verde NO es prueba. La prueba es que Julio lo
vea funcionar con sus ojos.
