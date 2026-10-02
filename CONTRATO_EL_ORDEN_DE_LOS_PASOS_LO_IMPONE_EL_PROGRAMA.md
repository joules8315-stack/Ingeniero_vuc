# CONTRATO — EL ORDEN DE LOS PASOS LO IMPONE EL PROGRAMA

**Fecha:** 2026-10-02
**Lo dijo Julio, textual:**

> "que cada paso abra el otro, porque si no seguimos tirando trabajo a la basura"
>
> "que nada dependa de tu memoria"

---

## EL FALLO QUE LO ORIGINA

Hoy el plan de trabajo es una lista de ordenes que nadie encadena. Cada orden se puede
empezar cuando a alguien le parece, sin que importe si lo que tenia que estar hecho antes
lo esta. El resultado es trabajo tirado a la basura: se construye encima de algo que aun no
existe, o se espera a que alguien se acuerde del orden correcto.

Medido el 2026-10-01: el campo `depende` estaba **vacio en las 56 ordenes abiertas**. Y una
orden archivada o sin vigia **detiene en silencio** a todas las que vienen detras, sin que
nadie se entere.

## LA LEY (es un orden, no una sugerencia)

1. **Un plan se ejecuta en pasos, y cada paso abre el siguiente.** No hay pasos sueltos.
2. **El orden lo impone el programa.** Nunca la memoria de una persona ni la de una IA.
3. **Cada orden lleva escrito de que depende.** Ese campo no puede quedar vacio.
4. **Una orden no corre hasta que las ordenes de las que depende esten hechas.**
5. **La tabla del plan vive en un solo archivo:** `memoria/PLAN_DE_PASOS.json`.
   No hay copias, no hay listas paralelas, no hay nombres escritos a mano en otros sitios.

## QUE ES UNA FALLA DEL PLAN

Una dependencia es una falla cuando apunta a:

- una orden **archivada**,
- una orden **inexistente**,
- una dependencia **circular** (A depende de B y B depende de A),
- una orden **cuya vigia no se ha escrito**.

Cuando pasa cualquiera de estas cuatro cosas, **el programa lo detecta y lo dice con nombre**:
no un aviso generico, sino el nombre de la orden que falla y el motivo.

## TABLA DE VERDAD

| Caso | Dependencia apunta a | La orden corre? | Que hace el programa |
|---|---|---|---|
| 1 | Orden existente y hecha | SI | La deja correr |
| 2 | Orden existente y NO hecha | NO | La detiene y dice de cual espera |
| 3 | Orden archivada | NO | Falla del plan: dice el nombre de la archivada |
| 4 | Orden inexistente | NO | Falla del plan: dice el nombre que no existe |
| 5 | Dependencia circular | NO | Falla del plan: dice el ciclo con nombres |
| 6 | Orden sin vigia escrita | NO | Falla del plan: dice el nombre de la orden sin vigia |
| 7 | Campo `depende` vacio | NO | Falla del plan: dice el nombre de la orden sin depende |

## LO QUE ESTA PROHIBIDO

- Empezar una orden sin que sus dependencias esten hechas.
- Dejar el campo `depende` vacio.
- Guardar la tabla del plan en mas de un sitio.
- Escribir a mano el nombre de una orden dentro de otra pieza: se lee del plan.
- Confiar en que alguien se acuerde del orden.

## COMO SE COMPRUEBA QUE SE CUMPLE, SIN QUE NADIE SE ACUERDE

Esto NO se mide con un contador que alguien tenga que subir a mano. Se mide solo, mirando
lo que ya queda escrito por si mismo:

- El campo `depende` de cada orden esta o no esta: se cuenta solo.
- Cada dependencia apunta a una orden que existe o no existe: se mira solo.
- Cada orden tiene su vigia escrita o no la tiene: se mira solo.
- El plan vive en un solo archivo o en varios: se mira solo.

**Programa que lo hace cumplir:** NO_ENCONTRADO
**Vigia que lo hace cumplir:** NO_ENCONTRADO

## PREGUNTA_REQUERIDA

Para poder cerrar este contrato sin inventar nada, hace falta saber:

1. **Cual es el nombre exacto del programa** que va a leer `memoria/PLAN_DE_PASOS.json`,
   comprobar las dependencias y decir con nombre las fallas del plan.
2. **Cual es el nombre exacto de la vigia** que va a comprobar, sola, que ese programa
   sigue haciendo su trabajo.
3. **Cual es el texto del contrato `CONTRATO_EL_PLAN_SE_SIGUE`** que este documento
   completa, para no repetirlo ni contradecirlo.

Sin esas tres respuestas, este contrato queda escrito pero sin guardian, y una ley sin
un disparador que la haga cumplir no se cumple.

## NECESITO_LEER

- `CONTRATO_EL_PLAN_SE_SIGUE.md` / es el contrato que este documento completa y no debe
  repetir / decide que partes de la ley ya estan dichas alli / riesgo: escribir dos veces lo
  mismo o contradecir la ley vigente.
- `memoria/PLAN_DE_PASOS.json` / es la tabla del plan que este contrato manda usar / decide
  si el archivo existe, que forma tiene y si el campo `depende` esta o no / riesgo: escribir
  una ley sobre un archivo que no existe o con otra forma.
- `CONTRATO_RUTA_DE_ACCESO.md` / es la ley que dice que el plan decide que se toca y nada
  mas / decide si este contrato nuevo encaja con esa ley o la contradice / riesgo: dos leyes
  que se pisan.
- `CONTRATO_COMO_EL_INGENIERO_CONSTRUYE_UN_PROYECTO.md` / describe los 4 pasos en orden /
  decide si el orden de los pasos ya esta definido alli / riesgo: repetir o contradecir el
  orden ya escrito.
