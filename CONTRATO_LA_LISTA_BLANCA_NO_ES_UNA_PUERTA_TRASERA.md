# CONTRATO — LA LISTA BLANCA NO ES UNA PUERTA TRASERA. NUNCA

**Julio, 2026-09-11:**

> *"Sí, que la lista blanca solo sirva para esa pieza que dijiste, lo demás no. Legíslalo, pon
> candado, vigílalo y que se cumpla, que nada se cuele por allí, **nunca**, que no sea una puerta
> trasera, **nunca**. Mira si se puede programar, para no introducir IA."*

---

## POR QUÉ SE ABRIÓ, Y LO QUE COSTÓ NO TENERLA

El contador de piezas dormidas necesita poder perdonar a las **herramientas de mano**: las que se
lanzan a propósito y por eso no las llama nadie desde el código. Sin ese permiso, su lista **nunca
llega a cero**.

**Costó siete horas y media.** Opencode se quedó parado esperando esta decisión, y **hizo bien**:
prefirió parar antes que inventar, que es exactamente lo que mandan las leyes de esta casa.

## POR QUÉ ES PELIGROSA

Una lista blanca es, por naturaleza, **una puerta trasera**. Lo que entra ahí deja de contarse, y
**lo que deja de contarse no lo enchufa nadie nunca**.

Sería la enfermedad de este día entero —algo que se pierde en silencio— pero **entrando por detrás
y con permiso**. Por eso la decisión de Julio fue abrirla **del ancho de una sola pieza**.

## LO MEDIDO ANTES DE ABRIRLA

| | |
|---|---|
| Piezas dormidas del negocio | **9** |
| De ésas, **se pueden lanzar a mano** | **1** (el compilador del mapa) |
| Las otras ocho | **no tienen ni forma de arrancarse** |

**Las ocho no son herramientas: son trabajo sin terminar.** La lista resuelve 1 de 9, no 9.

---

## LA LEY

### Regla 1 — Solo entra lo que DE VERDAD se puede lanzar
Lo comprueba **una máquina mirando el archivo**, no la palabra de nadie. Una pieza sin forma de
arrancarse **no es una herramienta de mano**, por mucho que alguien lo diga: es trabajo sin
terminar, y si entra aquí **deja de contarse y no la enchufa nadie nunca**.

### Regla 2 — Cada una escribe POR QUÉ está y QUIÉN la lanza
Sin las dos cosas, **no entra**. Sin motivo escrito, mañana nadie sabrá por qué se perdona a esa
pieza. *Una herramienta que no lanza nadie no es una herramienta.*

### Regla 3 — El motivo del rechazo SIEMPRE se dice
Frenar en silencio es peor que no frenar: si no se explica, nadie sabe qué hacer y **se acaba
apagando el candado**.

### Regla 4 — Es una CUENTA, no un juicio: NO entra ninguna IA
Julio lo pidió expresamente. Mirar si un archivo se puede lanzar es **leer, no opinar**. Por eso
la misma pregunta da **siempre la misma respuesta** — y eso se comprueba ejecutándolo cinco veces.

### Regla 5 — Salir es fácil; entrar es difícil
Sacar una pieza de la lista se puede siempre. **Meterla, solo pasando los cuatro candados.**

---

## A QUIÉN PUEDE DAÑAR

- **A quien quiera que su número baje sin trabajar:** ya no puede. Meter una pieza dormida en la
  lista es imposible por máquina.
- **A nadie más.** La lista solo deja de contar; no cambia ni una línea de código.

## CÓMO SE COMPRUEBA QUE SE CUMPLE

`vigias/test_vigia_la_lista_blanca_no_es_una_puerta_trasera.py`, con cinco guardianes que
**ejecutan el camino real**:

1. Una pieza que se puede lanzar **y trae su motivo** → entra.
2. Una que **no se puede lanzar** → **NO entra jamás**, diga lo que diga el motivo.
3. **Sin motivo escrito o sin decir quién la lanza** → no entra.
4. **La lista de verdad está limpia**: si una listada deja de poder lanzarse, **ROJA**. Ésta es la
   que muerde con el tiempo — hoy una pieza se lanza a mano, mañana alguien le quita esa puerta, y
   la lista la seguiría perdonando en silencio.
5. **La misma pregunta cinco veces da la misma respuesta** → es un programa, no un juicio.

**Y la prueba de verdad:** que Julio intente meter en la lista una pieza que no se puede lanzar, y
**no lo consiga**.

---

## LO QUE HAY HOY EN LA LISTA

**Una sola pieza**, la del negocio:

| Pieza | Por qué | Quién la lanza |
|---|---|---|
| El compilador del mapa | Regenera el mapa antes de sellar; por eso no la llama nadie desde el código | `sellar.sh` y quien va a sellar |

**Las otras ocho dormidas del negocio siguen contando como dormidas, y hay que enchufarlas.**
