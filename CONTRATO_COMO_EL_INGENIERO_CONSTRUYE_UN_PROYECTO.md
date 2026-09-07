# CONTRATO — COMO EL INGENIERO CONSTRUYE UN PROYECTO (los 4 pasos, en orden)

**Julio, 2026-09-07:**

> *"El ingeniero tiene todo para construir DMM, si es capaz de verse, y de determinar que tiene
> el ingeniero que le sirva al proyecto, en este caso DMM, asi debe ser con todos los proyectos."*

Esto **no es solo para DMM**: es el metodo para **cualquier** proyecto que el Ingeniero atienda.

---

## POR QUE NACE

Hoy el Ingeniero se enchufa a un proyecto dejandole un aviso, y ya. Nunca se pregunta **que de
lo suyo le sirve** a ese proyecto, ni **que le falta**, ni **que de lo que hace ese proyecto no
necesita IA**. Construye a ciegas o no construye.

Y se acaba de ver en vivo, medido en la ronda del 2026-09-07: se le encargo al equipo instalar un
candado **sin decirle como debia ser por dentro**, y el obrero **se lo invento**; el auditor lo
rechazo, y al mirarlo tenia razon. Construir sin haber mirado antes es el fallo que este contrato
cierra.

---

## LOS 4 PASOS, EN ESTE ORDEN Y SIN SALTARSE NINGUNO

### Paso 1 — El Ingeniero se mira a si mismo: ¿que de mi le sirve a este proyecto?

Antes de tocar nada, el Ingeniero hace **su propio inventario** y lo cruza con el del proyecto.
Sale una lista de **dos columnas, las dos obligatorias**:

| LE SIRVE | NO LE SIRVE |
|---|---|
| lo que el proyecto necesita y el Ingeniero ya tiene resuelto | lo que es del taller y no del producto |

**La columna de lo que NO le sirve es tan importante como la otra.** Sin ella se acaba metiendole
al producto los guardias del taller, que es lo que Julio prohibio: *"quiero que DMM la construya
el ingeniero, mas NO que funcione con el"*.

Y **le sirve** no quiere decir **se le presta**: quiere decir que el Ingeniero **sabe como se
hace** y se lo **construye al proyecto, suyo y dentro de su carpeta**.

### Paso 2 — Que habilidades le FALTAN al proyecto

Con su **arquitectura** y su **mapa** delante —no de memoria— se lista lo que el proyecto
necesita y no tiene. Lo que ya tiene **no se vuelve a construir**: se engancha o se completa.

### Paso 3 — El mapa de IA contra PROGRAMACION (antes de construir nada)

Se recorren las funciones del proyecto y se parte en dos:

| Necesita IA | Necesita programacion |
|---|---|
| escribir con criterio, decidir con matices | contar, sumar, fechas, reglas fijas, repetir siempre igual |

De ahi salen **las habilidades y los scripts** que hay que tener. Lo rutinario **no se le pide a
la IA**: se programa. Este paso va **antes** de construir, porque decide **que** se construye.

### Paso 4 — Recien ahora se construye

Con el mapa claro, se le construye al proyecto lo suyo y **completo**:

- **arnes suficiente** — el que ese proyecto necesita, ni mas ni menos
- **legislacion** — sus contratos, escritos antes que el codigo
- **vigias** — las pruebas que protegen cada pieza
- **candados** — enganchados de verdad; escrito y sin disparar **no cuenta**
- **memorias** — su estado y sus fallos, para que no repita
- **indexaciones** — para que se busque barato y no se lea entero
- **ontologia** — como se llaman las cosas en ese negocio
- **habilidades y scripts** — lo del paso 3

---

## LAS REGLAS QUE HACEN CUMPLIR LOS 4 PASOS

### Regla 1 — El orden no se negocia
No se construye (paso 4) sin el mapa de IA contra programacion (paso 3). No se hace ese mapa sin
saber que falta (paso 2). No se sabe que falta sin haberse mirado a si mismo (paso 1).
**Saltarse un paso es construir a ciegas**, y a ciegas se inventa.

### Regla 2 — Lo construido es del proyecto
Todo vive dentro del proyecto y le pertenece. **El proyecto tiene que seguir funcionando aunque
la carpeta del Ingeniero desaparezca del disco.** El Ingeniero construye; el proyecto no depende
de el para funcionar.

### Regla 3 — Nada se inventa, y por eso se dan plantillas
Cuando se manda construir una pieza, se entrega **como debe ser por dentro**, sacada de una que
ya funciona. Un encargo que dice "hazme un candado" sin decir cual **se contesta inventando**.

### Regla 4 — No se duplica: primero se busca en su mapa
Si el proyecto ya tiene la pieza, **no se le escribe otra encima**. Y no se busca por el nombre
del archivo: se busca por **lo que hace**. Contar candados por el nombre ya dio un numero falso
el 2026-09-07 (se dijo que DMM tenia cero, y tiene los suyos, apagados).

### Regla 5 — Enganchado o no cuenta
Una pieza escrita que no se dispara **no esta instalada**. Al terminar se dice **cuantas quedaron
funcionando**, no cuantas quedaron escritas.

### Regla 6 — Lo que diga un cerebro sobre el codigo se comprueba en el codigo
Un veredicto, del obrero o del auditor, **no es un hecho**. Antes de darlo por bueno o de
repetirselo a Julio, se mira el archivo. Ya paso que dos cerebros avisaron de un peligro FALSO y
casi se le cuenta como cierto.

---

## A QUIEN PUEDE DANAR

- `arnes/instalar.py` — pasa de dejar un aviso a seguir estos 4 pasos.
- `mapa/auditoria_proyecto.py` — ya inventaria un proyecto; el paso 1 necesita ademas que el
  Ingeniero se inventarie **a si mismo** y cruce las dos listas. **No se duplica: se reusa.**
- Todo proyecto ya declarado: al pasarle este metodo le apareceran piezas nuevas. Se le dice
  antes, no despues.

## COMO SE COMPRUEBA QUE SE CUMPLE

Una vigia que, sobre un proyecto de mentira:
1. comprueba que el paso 1 entrega **las dos columnas** (le sirve / no le sirve), no una;
2. comprueba que el paso 3 entrega el reparto **IA / programacion** de sus funciones;
3. comprueba que **no se construye nada** si faltan los pasos 1, 2 o 3 (Regla 1);
4. comprueba que lo construido **no nombra al Ingeniero** por ningun lado (Regla 2);
5. comprueba que una pieza que el proyecto ya tiene **no se pisa** (Regla 4);
6. comprueba que el informe final cuenta **enganchadas**, no escritas (Regla 5).

**Vigia verde no es prueba.** La prueba es que Julio toque DMM y le salte un candado de DMM.
