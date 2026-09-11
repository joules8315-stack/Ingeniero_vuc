# DÓNDE QUEDAMOS — 2026-09-11

**Para retomar sin releer nada.**

---

## EL HALLAZGO DE HOY: FALLÓ EL ARNÉS, Y SE SABE POR QUÉ

Julio preguntó: *"mira además por qué lo borró, está faltando a la regla de que construya pero
sin dañar algo. Falló el arnés."* **Tenía razón, y está comprobado.**

### El agujero, medido

El revisor automático comprueba **cinco cosas**:
1. que no sea humo · 2. que no quede roto · 3. que no use nombres inventados ·
4. que haga lo que se pidió · 5. que se pueda leer

**Y no comprueba ni una sola vez si el cambio BORRA algo que ya estaba.**

| Guardia | ¿Vigila los borrados? |
|---|---|
| El revisor automático | **NO** |
| El que aplica los cambios | **NO** |
| El copista | **NO** |
| El guardia de guardado | solo de refilón |

**Por eso pasó:** la otra IA reescribió el jefe que coordina, **la puerta desapareció**, y
**ningún guardia dijo nada**. Las 526 pruebas siguieron verdes.

> **El arnés vigila que lo nuevo esté bien. No vigila que lo viejo siga ahí.**

---

## LO QUE PASÓ CON EL JEFE QUE COORDINA

La otra IA hizo algo **bien**: repartió el trabajo en vez de duplicarlo — le pregunta el
presupuesto al plan y la aprobación a la pieza de aprobación. **Eso se respeta.**

Pero al hacerlo **se perdieron tres cosas**:

| Lo que había | Lo que quedó |
|---|---|
| **Una puerta** que juntaba permiso + presupuesto y decía sí o no con su motivo | Dos piezas sueltas. **Nadie las junta** |
| Saber si el permiso **ya se dio** | Solo dice si **hace falta** |
| **Descontar** lo gastado | Nadie descuenta: el combustible nunca baja |

**Y un cambio de criterio:** antes publicar pedía permiso siempre; después, **un texto salía solo**.

---

## LA DECISIÓN DE JULIO, YA TOMADA

> *"Tiene que pedir mi permiso, sin él nunca sale nada."*

**Legislado** en `CONTRATO_SIN_SU_PERMISO_NO_SALE_NADA.md` (en la aplicación). Sin excepciones
por formato, precio ni prisa. **El formato no decide.**

---

## LO QUE SIGUE, EN ORDEN

### 1 · La vigía de la puerta — **ya escrita, falta guardarla**
`vigias/test_vigia_sin_su_permiso_no_sale_nada.py` (en la aplicación). Nace **roja**. Exige:
un texto sin permiso **no sale** · ningún formato se libra · con el permiso **sí sale** ·
sin presupuesto tampoco · y el que publica no saca nada sin aprobar.

### 2 · La puerta única — **es lo que falta construir**
En el jefe que coordina: **`puede_salir(empresa, formato, aprobado)`** → devuelve **sí/no y el
motivo**, mirando **las dos cosas**: ¿tiene el permiso?, ¿queda combustible?

**Es una CUENTA, no un juicio: lo hace un programa, gratis.** Todo lo que necesita ya existe
(el plan sabe del combustible, la pieza de aprobación guarda los síes).

### 3 · TAPAR EL AGUJERO DEL ARNÉS ← **lo más importante**
Que el revisor automático **cuente si el cambio borra algo**: si el texto nuevo tiene **menos
funciones** que el viejo, **frena y dice cuáles desaparecen**.

**Sin esto, volverá a pasar con cualquier otra pieza.**

### 4 · Avisado a la otra IA
Ya se le mandó por el canal el encargo entero y la decisión de Julio. **No se tocó nada de su
trabajo.**

---

## EL MÉTODO, QUE NO SE SALTA
1. **La vigía primero, y nace roja.**
2. **De enchufe, con espía: se ejecuta el camino real**, nunca se busca la palabra en el archivo.
3. Si es una cuenta, **la aplica el copista, gratis**. La IA solo para lo que es juicio.
4. **Correr todas las vigías**, no solo la nueva.
5. Guardar contando **también lo que salió mal**.

## CÓMO SE COMPRUEBA QUE QUEDÓ BIEN
- Se intenta sacar **un texto sin permiso** → **no sale**.
- Se da el permiso → **sale**.
- Se ejecuta con coste → **el combustible baja**.
- **Se borra a mano la puerta → alguna vigía se pone roja.**

**Y la prueba de verdad: que Julio intente publicar algo sin dar su sí, y no salga.**
