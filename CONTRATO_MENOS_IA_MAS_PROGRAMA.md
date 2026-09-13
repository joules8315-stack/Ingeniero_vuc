# CONTRATO — MENOS IA, MAS PROGRAMA

**Julio, 2026-09-05:**

> *"Cuando una tarea no necesite de una IA para analizar, que sea trabajo rutinario, se crea un
> script, no mas usar IA en cosas estupidas, o un skill, lo que se necesite. Menos IA, mas
> programa, para estas cosas rutinarias y que requieran el mismo resultado."*

**Julio lo llevaba diciendo hace rato con la palabra "habilidades" (skills) y no se entendio.**
Cuando una IA de fuera dijo lo mismo con otras palabras ("si un script puede hacerlo, no se le
pide a una IA") si se entendio. Eso es un fallo de escucha, y por eso queda escrito aqui.

---

## LA LEY

**Si la tarea es rutinaria y siempre da el mismo resultado, la hace un PROGRAMA. No una IA.**

Una IA solo entra donde hace falta **juicio**: decidir, diseñar, entender un problema nuevo.
Contar, buscar, comparar, listar y comprobar **no son juicio: son cuentas**.

### Regla 1 — La pregunta antes de gastar
Antes de mandarle nada a un cerebro se responde: **¿esto siempre da el mismo resultado?**
Si la respuesta es SI, no se manda: se escribe una habilidad.

### Regla 2 — Lo que ya se sabe que debe ser programa
Sacado de lo que costo tiempo o dinero de verdad (medido el 2026-09-05):

| Habilidad | Por que |
|---|---|
| **Cazar el humo**: comparar el cambio sin comentarios | el equipo entrego 2 reparaciones falsas en un dia y el revisor las aprobo |
| **Medir al equipo**: quien escribe, quien revisa, que llego al codigo | se hizo a mano con seis ordenes de terminal |
| **Comprobar la via unica**: ramas y copias sueltas | se hizo a mano; aparecieron dos copias fantasma |
| **Avisar si el material no trae la pieza del problema** | se gastaron dos vueltas del equipo por eso |
| **Contar frenos y decir cuantos acabaron con culpable** | hoy: 2 de 13.375 |
| **Distinguir una orden de Julio de un texto pegado** | la maquina confundio 32 frases de otra IA con ordenes suyas |

### Regla 3 — Una habilidad no opina
Una habilidad **cuenta, compara o lista**. Si hace falta interpretar, no es una habilidad: es
trabajo de cerebro. No se disfraza una cosa de la otra.

### Regla 4 — Antes de crear, se busca
No se crea una habilidad que ya existe. Primero se mira el mapa. Duplicar es el mismo fallo de
siempre con ropa nueva.

### Regla 5 — Lo repetido se convierte
Si una misma cuenta se hace **dos veces a mano**, la tercera ya no: se convierte en habilidad.

---

## EL CANDADO

Antes de mandar un encargo a un cerebro, el candado mira el encargo. Si lo que pide es
**contar, listar, comparar, medir o comprobar** y no pide interpretar nada, **frena** y dice:
*"esto es una cuenta: se hace con una habilidad, no gastando un cerebro"*.

No frena a ciegas: si Julio dice que se mande igual, se manda. Pero no pasa en silencio.

---

## A QUIEN PUEDE DANAR

- Al mando que llama al equipo: ahora tiene un paso antes.
- Al buscador de habilidades: hay que mirarlo antes de crear ninguna, para no duplicar.

---

## COMO SE COMPRUEBA QUE SE CUMPLE

Una vigia que:
1. manda un encargo de contar ("cuantas veces freno cada candado") y comprueba que **se frena**
   con el aviso de que eso es una habilidad;
2. manda un encargo de juicio ("decide si esta reparacion rompe al vecino") y comprueba que
   **pasa** sin frenarse;
3. comprueba que el aviso nombra la habilidad que ya existe, si existe.

**Vigia verde no es prueba.** La prueba es que Julio vea bajar el gasto en cosas que son cuentas.

---

## INVENTARIO DE LO QUE SE HACE A MANO — 2026-09-13

> Julio: *"Mira todos los procesos que se hacen manual, incluidos los que claude hace manual y
> verifica: que se puede programar, que aun no haya sido programado, que no necesite cerebro; que
> necesita cerebro."*

Medido por el ayudante (tareas B y C) y por la dirección contando sus propios registros. **Cada
fila comprobada en el código**; lo que el ayudante dijo y no se sostenía se corrigió o se tiró.

**Lo que Claude hizo a mano en UNA sesión (2026-09-12):** 163 órdenes y encargos escritos, 103
guardados, 95 corridas de pruebas, 89 aplicaciones con el copista, 67 frenazos de candado.
**Registros:** 54 guardados a mano contra 26 del equipo; 14.651 frenazos de candado.

### SIN CEREBRO Y SIN PROGRAMAR TODAVÍA (se programan, con el equipo y su vigía)
| proceso | quién lo hace hoy | por qué es una cuenta |
|---|---|---|
| armar la orden del ayudante: pegar `memoria/LEYES_DEL_AYUDANTE.md` + comprobar que no nombra carpetas de fuera (ley 9) | Claude | copiar un archivo y buscar rutas |
| lanzar al ayudante (`opencode run`), de uno en uno, y recoger su informe | Claude | encolar y guardar la salida |
| comparar vigías ANTES y DESPUÉS y decir si algo se rompió | Claude | restar dos números y comparar nombres |
| tras aplicar un cambio del equipo, correr la vigía que nombra el encargo; si sigue roja, NO está aprobado | nadie (el auditor aprueba sin correrla) | ejecutar y leer el resultado |
| decidir si un aviso de "fotocopia" es de verdad (hoy salta por nombrar las palabras) | programa que se equivoca | mirar si las marcas están al principio del renglón |
| no apuntar como "orden de Julio" los avisos automáticos y los recados entre IAs | Claude marcándolas a mano | mirar de dónde viene el texto |
| el aplicador toma la marca `NO_ENCONTRADO` como texto y no crea el archivo nuevo aprobado | nadie (se pierde la ronda) | comparar con una palabra fija |
| el comando del equipo aplica aunque el revisor de programa frene, y dice "LLAVE GUARDADA" | nadie | leer el veredicto final en vez del del auditor |
| el guardia del guardado DEJA PASAR cuando no alcanza a correr las vigías (se le acaba el tiempo) | nadie | si no se pudo comprobar, se frena |
| mover a un cliente por el embudo (`crm.mover`, negocio) | Julio, sin pantalla | cambiar un estado con su motivo |
| retirar `vigias/correr_todas.py` del negocio, que da verdes falsos | — | borrar y corregir 3 documentos |

### NECESITA CEREBRO (juicio)
redactar el mensaje al cliente dormido · escribir código nuevo · decidir la causa raíz de un fallo ·
redactar la ley de una orden nueva de Julio (el apuntarla ya es automático).

### DE LOS OJOS DE JULIO (no se programa, ley 3)
probar cada pantalla · autorizar el respaldo a GitHub · escribir sus llaves (`.env`) · copiar números
de Marketplace, que no tiene API.

### YA PROGRAMADO (comprobado)
cambiar el compañero activo (`arnes/companero.py`) · no aplicar si escribió y revisó el mismo
(`arnes/candado_equipo.py`) · el mecanismo del canal (`arnes/canal.py`) · compilar el mapa del
negocio al sellar (`arnes/compilar_mapa.py`).
