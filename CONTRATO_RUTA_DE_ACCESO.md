# CONTRATO — LA RUTA DE ACCESO: EL PLAN DICE QUE SE TOCA, Y NADA MAS

**Julio, 2026-09-06:**

> *"Cuando pidas permiso, eso ya lo habiamos hablado y pedi sea legislado: debe haber una ruta
> clara de lo que se va a tocar, para que no toque nada mas, y esto lo define el plan. Una vez
> aprobado el plan, este debe tener todo lo que necesita acceso, y pedir acceso para eso
> unicamente. Esto debe estar legislado fuerte, con candado, blindado y con super vigia."*

---

## EL NUMERO QUE LO JUSTIFICA

El permiso que Julio dio el 2026-09-05 **abre los DOCE candados a la vez, durante 24 horas, y
no dice ni una palabra sobre QUE se puede tocar**. Con ese permiso abierto, cualquier pieza de
las 101.000 lineas del proyecto quedaba a mano.

Eso choca de frente con la propia ley de la llave unica del 2026-08-27:
*"no se abren los 12 candados de golpe; se abren solo los que la tarea necesita, ni mas ni
menos, y antes de abrir se dice exactamente cuales y por que"*.

**Hasta hoy esa ley estaba escrita y no la hacia cumplir nadie.** Ahora la hace cumplir un
candado.

---

## LAS CINCO RESPUESTAS (obligatorias desde CONTRATO_ANALISIS_DE_FONDO.md)

| | |
|---|---|
| **QUE** | Un candado que frena **escribir** en cualquier pieza que el plan aprobado no haya declarado. |
| **DONDE** | `arnes/candado_ruta_de_acceso.py`, enganchado antes de escribir o editar. La lista vive en `memoria/RUTA_DE_ACCESO.json`. El rastro, en `memoria/RUTA_DE_ACCESO.log`. |
| **COMO** | Se compara la ruta del archivo contra la lista del plan. **Es una cuenta, no un juicio**: no opina si el cambio es bueno; solo si estaba permitido tocarlo. |
| **POR QUE ASI Y NO DE OTRO MODO** | Se descarto **(a)** deducir la lista sola, segun lo que se va tocando: eso no es una ruta, es un parte de daños escrito despues; y **(b)** frenar todo cuando no hay plan: dejaria la herramienta inservible para el trabajo del dia a dia. La unica forma que cumple la ley sin romper el uso normal es: **manda solo cuando hay un plan aprobado vigente**. |
| **CUANDO** | **La primera de todas.** Las otras ocho piezas del plan se ejecutan ya bajo esta ruta. Hacerla despues seria trabajar sin ella justo cuando mas se toca. |

---

## LA LEY

### Regla 1 — Sin ruta declarada no se pide permiso
Antes de pedirle a Julio que abra nada, se escribe **la lista exacta de piezas** que se van a
tocar. Pedir permiso "para trabajar" sin decir en que, esta prohibido.

### Regla 2 — El plan aprobado ES la ruta
La lista no se inventa aparte: sale del plan que Julio aprobo. Si una pieza no esta en el
plan, no esta en la ruta.

### Regla 3 — EL BLINDAJE: la autorizacion no es barra libre
Aunque Julio haya apagado los candados, **si el archivo no esta en la ruta, se frena igual**.
La autorizacion de Julio pasa a significar *"permiso para lo que el plan dijo"*, no
*"permiso para todo"*.

### Regla 4 — Si el plan se quedo corto, no se rodea: se dice
Cuando hace falta tocar algo que no esta en la ruta, **no se busca la vuelta**. Se le dice a
Julio que el plan se quedo corto y **el** decide si se amplia. Ese aviso es informacion: dice
que el analisis de fondo fallo en la pregunta *donde*.

### Regla 5 — Toda ruta se cierra, y ninguna manda para siempre
Terminado el plan, la ruta se cierra y vuelve el regimen normal. Y si nadie la cierra,
**caduca sola a las 48 horas**: un plan olvidado no puede bloquear la casa.

### Regla 6 — Frenar en silencio esta prohibido
Cada freno y cada paso queda apuntado en el cuaderno de la ruta. Un candado que frena sin
dejar rastro no se puede medir, y lo que no se mide no se repara.

---

## ALCANCE — LO QUE ESTE CANDADO NO HACE

- **No juzga si el cambio es bueno.** De eso van las vigias.
- **No sustituye a ningun otro candado.** Se suma a los que ya estan.
- **No frena leer.** Solo escribir.
- **No manda cuando no hay plan aprobado.** Ahi gobiernan los demas, como siempre.

---

## A QUIEN PUEDE DANAR

- A la autorizacion de Julio: deja de abrir todo y pasa a abrir **lo declarado**. Es el efecto
  buscado, pero hay que saberlo.
- Al trabajo del dia a dia: **ninguno**, mientras no haya un plan abierto.

---

## COMO SE COMPRUEBA QUE SE CUMPLE

La super vigia `vigias/test_vigia_ruta_de_acceso.py` comprueba las ocho cosas que importan:

1. sin plan, no estorba;
2. lo que el plan declaro, pasa;
3. lo que no declaro, se frena;
4. **se frena tambien con los candados apagados** (el blindaje);
5. no se cuela un archivo por tener el mismo nombre en otra carpeta;
6. una ruta cerrada deja de mandar;
7. una ruta caducada deja de mandar;
8. cada freno deja rastro.

**Vigia verde no es prueba.** La prueba es que Julio pida abrir y **vea escrita, antes de dar
la llave, la lista exacta de lo que se va a tocar**.
