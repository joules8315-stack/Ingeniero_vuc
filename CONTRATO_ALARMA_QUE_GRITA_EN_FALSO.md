# CONTRATO — UNA ALARMA QUE GRITA EN FALSO SE ARREGLA O SE APAGA

**Julio, 2026-08-25:** "no vamos a ver los candados mensual, sino semanal, cada 8 dias los
evaluamos."

**Claude, el mismo dia:** "una alarma que suena sin motivo ensena a ignorarla, y el dia que suene
de verdad nadie va a mirar."

---

## 0. El caso que la trae (medido, no supuesto)

`rv3_prueba_4_roles.py`, paso 3, llevaba **desde el 2026-07-16** diciendo:

> "Tras borrar el rol de evidencia, el servidor lo sigue teniendo."

**Era mentira.** Borraba llamando a `updateTemplateRoleColumn('evidence','0')` creyendo que el
cero borra. `app_web.html:944` hace `Math.max(1, Number(columnIndex)||1)`: el cero **pasa a 1**,
asi que no borraba, **movia** evidencia a la columna 1 y de paso descolocaba a lectura.

Lo peor no es el fallo. Lo peor es esto: **ya estaba investigado y escrito** en la cabecera de
`rv3_prueba_4_1_borrar_rol.py`, con fecha y explicacion. Alguien lo entendio, lo dejo por escrito
**y no toco la alarma**. Cuarenta dias gritando.

Tras la cura (pulsar el boton real): **0 hallazgos**, y encima confirma que borrar un rol
funciona bien, se ve en Revisar y sobrevive a reabrir la sesion.

## 1. La regla

Cuando se descubre que una alarma señala algo que **no es cierto**:

- **Se arregla ese mismo dia**, o
- **se apaga ese mismo dia**, diciendo por que.

**No hay tercera opcion.** Dejarla gritando "porque ya sabemos que es falso" es la peor de las
tres: el que lo sabe se va, y el que llega se lo cree — o peor, aprende a no creerse ninguna.

## 2. Escribirlo NO cuenta como arreglarlo

Dejar una nota que diga "ojo, esta alarma miente" es exactamente lo que se hizo el 2026-07-16, y
no sirvio de nada. La nota la lee quien ya lo sabe. **La alarma la lee todo el mundo.**

## 3. Por que importa mas de lo que parece

Un aviso falso no es ruido inofensivo: **entrena a ignorar los avisos**. Y ese habito no
distingue: se contagia a los que si sirven. Cuando alguien dice "esa alarma siempre esta roja, no
le hagas caso", el sistema de alarmas entero ya esta muerto, aunque el tablero se vea lleno.

## 4. Como se sabe cual grita en falso: SE CUENTA

Cada candado y cada alarma lleva dos cuentas (`arnes/candados_medicion.py`):

| Cuenta | Que dice |
|--------|----------|
| **cazadas** | freno algo que de verdad estaba mal |
| **frenos en falso** | freno algo que resulto legitimo |

**Se revisan CADA 8 DIAS** (decision de Julio, 2026-08-25):

- **Caza y no estorba** -> se queda.
- **No ha cazado nada** -> o su señal esta mal puesta, o sobra. Se decide; no se deja.
- **Caza poco y frena mucho en falso** -> el peor. Se arregla la señal o se apaga.

**Primera entrada real de esa cuenta (2026-08-25):** la pregunta de criterio freno una causa
diciendo que comparaba dos cosas. Era UNA sola, dicha con una coma; el detector cuenta comas.
Se apunto como freno en falso. Ese numero es el que hace que la revision de los 8 dias sea un
dato y no una opinion.

## 5. Y al reves: una alarma que nunca se pone roja tampoco vale

Ya legislado y demostrado tres veces este mismo dia: una comprobacion que pasa igual con el fallo
delante es adorno. **Se sabotea la cura y se comprueba que se pone ROJA.** Si no muerde, no
protege: solo da falsa calma.

---

## Quien lo hace cumplir

| Que | Donde |
|-----|-------|
| Las dos cuentas por candado | `arnes/candados_medicion.py` |
| La revision cada 8 dias | `CONTRATO_DOS_TRABAJANDO.md` y este contrato |
| Que ninguna alarma quede sin vigia | `vigias/test_vigia_legislar_todo.py` |
