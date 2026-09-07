# CONTRATO — LO QUE SE ARREGLA VALE PARA TODOS LOS PROYECTOS

**Julio, 2026-09-07:**

> *"Que los cambios que se apliquen, se apliquen a todo, ya que son generalidades. Esto es
> importante: aquí estamos hablando de economizar, de optimizar. Todos los proyectos deben
> contar con eso."*

---

## LA LEY

**Una mejora de ahorro no es de un proyecto: es del Ingeniero, y el Ingeniero atiende a
todos.** Ningún proyecto de `proyectos.config` se queda sin ella.

### Regla 1 — Lo que vive en el Ingeniero, ya llega a todos
Las piezas del Ingeniero (`cerebro/`, `cuerpo/`, `arnes/`) trabajan sobre CUALQUIER proyecto
de la libreta. Repararlas ahí es repararlas para todos. **Se repara en el Ingeniero, nunca en
la copia de un proyecto**, o la mejora se queda encerrada en uno.

### Regla 2 — Lo que hay que dejar DENTRO de cada proyecto, se instala y se comprueba
Las reglas de ahorro que viven en el `CLAUDE.md` de cada proyecto se ponen con
`arnes/instalar.py`. **Una vigía comprueba que ningún apodo de la libreta se quede sin ellas.**
Instalar a mano y confiar en la memoria es como no instalar: pasó con DMM, que estuvo sin sus
reglas guardadas hasta el 2026-09-06.

### Regla 3 — Al terminar una mejora, se dice a quién alcanzó
No basta con "hecho". Se escribe **en qué proyectos queda activa** y **cuáles quedaron fuera y
por qué**. Un proyecto que se queda fuera en silencio paga de más sin que nadie lo sepa.

### Regla 4 — Lo medido en uno se aprovecha en todos
Los números de capacidad, fallos y tiempos (`memoria/CUOTAS.json`, `memoria/CAPACIDADES.json`)
son del Ingeniero, no de un proyecto. Lo aprendido reparando DMM sirve para Foto Informe sin
volver a medirlo.

### Regla 5 — Esta ley NO abre ninguna puerta a la vía canónica
Alcanzar a todos los proyectos **no** autoriza a tocar ninguno sin comprobar antes su ruta y
su rama con `arnes/via_canonica.py`, y **no autoriza a declarar ni cambiar ninguna ruta**: la
libreta `proyectos.config` aquí solo se LEE. Un proyecto cuya vía no esté limpia **se deja
fuera y se dice por escrito**, nunca se toca "de paso".

Esto está escrito porque ya pasó dos veces: había 3 copias de Foto Informe en el disco y se
trabajó media sesión sobre la de mayo habiendo una de julio con 253 archivos, por haber
llenado la libreta a ojo sin comprobar cuál era la viva. Julio confirmó la buena el
2026-08-20 y las otras dos se respaldaron y se borraron. **Aquí no se declara nada.**

---

## LA TABLA DE VERDAD — a quién alcanza cada mejora del 2026-09-06 / 07

| Mejora | Dónde vive | ¿Alcanza a todos? |
|---|---|---|
| El obrero ya puede crear algo nuevo (`clase`) | Ingeniero, `cuerpo/obrero.py` | **Sí**, automático |
| La marca `--crear` en el mando | Ingeniero, `ingeniero.py` | **Sí**, automático |
| El aplicador sabe en qué proyecto está (`raiz`) | Ingeniero, `cuerpo/aplicador.py` | **Sí** — antes solo acertaba con el Ingeniero |
| El mando `aplicar-guardado` | Ingeniero, `ingeniero.py` | **Sí**, recibe el proyecto por su apodo |
| El guardia deja de gritar en falso | Ingeniero, `arnes/guardia_de_guardado.py` | **Sí**, automático |
| El rastro del guardia no viaja con el código | En CADA proyecto (`.gitignore`) | **NO todavía**: hecho en Ingeniero y DMM; **falta Foto Informe** |
| Las reglas de ahorro en el `CLAUDE.md` | En CADA proyecto | **Comprobar uno por uno** |

---

## LA MATRIZ — qué falta para cumplir esta ley

| Falta | Cómo se cura |
|---|---|
| Foto Informe no tiene la cura del rastro del guardia | La misma línea, **con su vía canónica comprobada y limpia primero** |
| No hay quien vigile que todos tengan las reglas de ahorro | `vigias/test_vigia_todos_los_proyectos.py` |
| Nadie comprueba que una mejora llegó a todos | Regla 3: se escribe al terminar |

---

## A QUIÉN PUEDE DAÑAR

- A los proyectos de la libreta: **a ninguno**. Se les añade, no se les quita.
- A la **vía canónica**: **no se toca**, y la Regla 5 lo deja escrito.
- A los tiempos de espera: **no se tocan** (Julio, 2026-09-07).

## CÓMO SE COMPRUEBA

`vigias/test_vigia_todos_los_proyectos.py`, determinista y sin red:
1. LEE los apodos de `proyectos.config` (no los declara ni los cambia);
2. comprueba que **cada uno** tiene sus reglas de ahorro instaladas;
3. comprueba que **cada uno** tiene el rastro del guardia fuera del guardado;
4. si falta alguno, **lo nombra** — nunca dice solo "falla".

**Vigía verde no es prueba.** La prueba es que Julio no vea un proyecto pagando de más porque
se quedó sin una mejora que los otros sí tienen.
