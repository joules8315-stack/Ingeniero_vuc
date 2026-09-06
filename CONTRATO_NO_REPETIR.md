# CONTRATO — NO SE LE REPITE A JULIO LO QUE YA LEYO

**Julio, 2026-09-06:**

> *"Esto fue lo que acabamos de hacer, ¿por qué repites todo dos veces? ¿Qué pasa? Repara eso
> también."*

---

## EL NUMERO QUE LO JUSTIFICA

Julio pregunto **"¿que paso?"** y, en vez de contestarle lo NUEVO, se le solto el resumen
entero del dia por segunda vez. Dos respuestas seguidas con el mismo contenido.

Y no es un descuido suelto: **son dos causas distintas, y las dos se repiten.**

| Causa | Que hace |
|---|---|
| **1. Contestar de mas** | Se pregunta una cosa y se contesta esa mas todo lo anterior "por si acaso" |
| **2. Reescribir entero** | Cuando el candado del lenguaje frena una respuesta por una palabra tecnica, se reescribe **la respuesta completa**, asi que todo el contenido sale otra vez |

Existe un cuaderno de lo que Julio ha dicho. **No existe nada que frene a Claude cuando repite
lo que YA le conto.**

**Y ya hay un antecedente exacto de por que esto NO puede depender de acordarse:** el contador
de veces que Julio repetia algo marcaba CERO habiendo repetido cuatro veces el mismo dia,
porque solo subia si alguien lo apuntaba a mano. Se curo haciendo que se dispare solo. Este
candado nace ya asi: **se dispara solo, comparando con lo que ya se dijo.**

---

## LAS CINCO RESPUESTAS

| | |
|---|---|
| **QUE** | un candado que frena una respuesta cuando repite lo que ya se le dijo a Julio |
| **DONDE** | `arnes/candado_no_repetir.py`, enganchado al terminar la respuesta. El cuaderno en `memoria/.ya_le_dije.json`, el rastro en `memoria/.repeticiones.log` |
| **COMO** | se guarda la **huella** de cada frase larga que se le dijo (no el texto). Al terminar, si mas de la mitad de las frases largas ya estan en el cuaderno, se frena. Es comparar texto: **cuenta, no juicio**. Y se apunta **solo**, sin que nadie tenga que acordarse |
| **POR QUE ASI Y NO DE OTRO MODO** | se descarto **(a)** fiarlo a que Claude se acuerde — medido: un contador que hay que subir a mano marca cero aunque haya pasado cuatro veces; y **(b)** guardar el texto entero de cada respuesta, porque engorda la memoria sin falta: con la huella basta para saber si ya se dijo |
| **CUANDO** | ahora. Cada repeticion es tiempo de Julio leyendo lo que ya sabia |

---

## LA LEY

### Regla 1 — Se contesta lo que se pregunta
Si Julio pregunta una cosa, se contesta **esa**. El resumen completo solo cuando el lo pide.

### Regla 2 — Lo ya contado no se vuelve a contar
Un dato que ya se le dio no se repite, ni aunque venga a cuento. Si hace falta apoyarse en el,
se le nombra en una linea y se sigue.

### Regla 3 — Reescribir no es repetir
Cuando un candado obliga a rehacer una respuesta, **se cambia solo el trozo que sobra**. No se
vuelve a escribir la respuesta entera: eso es lo que la duplica.

### Regla 4 — El freno no puede atascar el trabajo
No frena mas de dos veces seguidas, igual que hace el candado del lenguaje, y se apaga con la
variable de siempre. Un candado que bloquea del todo se acaba saltando, y entonces no sirve.

---

## ALCANCE — LO QUE NO HACE

- No juzga si la respuesta es buena: solo si **ya se dijo**.
- No frena una palabra o una frase corta repetida: eso es hablar normal.
- No toca lo que Claude escribe en el codigo ni en las leyes: **solo lo que le dice a Julio**.

---

## A QUIEN PUEDE DANAR

- Al candado del lenguaje: ahora hay dos frenos sobre la misma respuesta. Por eso los dos
  tienen el mismo tope de dos veces seguidas.

---

## COMO SE COMPRUEBA QUE SE CUMPLE

Una vigia que:
1. le pasa una respuesta nueva y comprueba que **pasa**;
2. le pasa la MISMA respuesta otra vez y comprueba que **se frena**;
3. le pasa una respuesta que solo repite una frase corta y comprueba que **pasa**;
4. comprueba que no frena tres veces seguidas.

**Vigia verde no es prueba.** La prueba es que Julio deje de preguntar por que se le repite
todo dos veces.
