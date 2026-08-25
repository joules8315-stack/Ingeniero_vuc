# CONTRATO — EL EQUIPO QUE AGUANTA EL TAMAÑO

**Ley dictada por Julio el 2026-08-24:**

> "Usa la version paga para Foto Informe, que aguante el tamaño, incluido Claude. Trabajen los 3
> en Foto Informe, de manera por defecto."

> "Investiga, legisla, repara, para que no vuelva a fallar Cline."

---

## 0. De donde sale esta ley (el fallo real, medido)

Cline entrego a Julio la prueba de las 10 vueltas **diciendo que el equipo ya la habia
auditado**. Tenia cinco fallos, y uno le habria borrado a Julio siete textos escritos a mano.

No fue descuido de Cline. Fue esto, medido el mismo dia:

- Los dos obreros gratis (GPT-OSS 20B y 120B) devolvieron **413 Payload Too Large en TODAS las
  llamadas** sobre Foto Informe. Ni una vez llegaron a ver el codigo.
- Un cerebro agoto su cuota; otro devolvio servicio no disponible.
- Y aun asi se les seguia eligiendo en cada intento.

**Causa raiz (declarada y medida):** el techo de cada cerebro **solo sube, nunca baja**.
`CAPACIDAD` cree lo que dicen los proveedores (Groq: 500.000 letras; Gemini: 4.000.000),
`_capacidad` se queda con el MAXIMO entre esa promesa y lo medido, y `apuntar_uso` solo apunta
tamaño cuando el cerebro ACIERTA. Cuando revienta por tamaño no apunta nada.

Resultado: se le manda trabajo a quien ya demostro cien veces que no puede, y **"auditado" acaba
significando "alguien dijo que si sin haber visto nada"**.

## 1. Quien no cupo, no se le vuelve a pedir lo mismo

Cuando un cerebro falla **porque no le cabe el material** (413, payload too large, context
length, request too large), se le apunta un **TECHO**: a partir de ahi, no se le vuelve a
elegir para encargos de ese tamaño o mayores.

- El techo **baja** con la evidencia. Es el unico numero del sistema que puede bajar, y debe
  poder bajar: es la leccion.
- No se le castiga para siempre: sigue entrando en encargos que SI le caben.
- La promesa del proveedor **deja de mandar** en cuanto hay una medida que la desmiente.
  Julio, 2026-08-21: *"legislar con datos, no con suposiciones"*.

## 2. Foto Informe va con los que aguantan, por defecto

Foto Informe es el proyecto grande (mas de 430.000 lineas). Por orden de Julio, **por defecto**
trabajan ahi los que aguantan el tamaño:

| Quien | Papel |
|-------|-------|
| **Claude** | dirige, lee el veredicto y responde a Julio |
| **Cline** | trabaja el codigo bajo las mismas reglas (`.clinerules/modo_ingeniero.md`) |
| **DeepSeek** (de pago) | el obrero pesado: genera |

Los gratis pequeños **no se eligen** para generar en Foto Informe. Pueden auditar si el material
que se les pasa les cabe; si no les cabe, tampoco auditan.

## 3. "Auditado" hay que poder demostrarlo

Un encargo **no cuenta como auditado** si el auditor no llego a ver el material.

- Si el auditor fallo por tamaño, cuota o servicio caido, el veredicto es **SIN_AUDITAR**, nunca
  APROBADO.
- Un SIN_AUDITAR **no es una aprobacion**. No se le dice a Julio "el equipo lo aprobo".
- Esto es lo que fallo con la prueba de las 10 vueltas, y es lo que esta ley existe para evitar.

## 4. Y si no queda nadie que aguante

Se **para y se le dice a Julio**, con esta frase o parecida:

> "Nadie del equipo aguanta este encargo: el material es demasiado grande para los que hay."

No se reparte a ciegas, no se recorta el material para que quepa (eso ya se apunto como fallo:
*"no se acelera recortando el material"*), y **no se da por auditado**.

---

## Quien lo hace cumplir

| Que | Donde |
|-----|-------|
| El techo que baja | `cuerpo/cuotas.py` -> `apuntar_uso`, `_capacidad` |
| Quien elige a quien | `cuerpo/obrero.py` -> reparto de turnos |
| Vigia | `vigias/test_vigia_equipo_que_aguanta.py` |

**Estado al legislarlo (2026-08-24):** el punto 1 esta REPARADO y su vigia nacio ROJA. Los
puntos 2, 3 y 4 quedan escritos; lo que ya se cumple y lo que no, lo dice la vigia.
