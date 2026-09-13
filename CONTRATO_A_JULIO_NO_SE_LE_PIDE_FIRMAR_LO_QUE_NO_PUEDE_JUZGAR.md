# CONTRATO — A JULIO NO SE LE PIDE QUE FIRME LO QUE NO PUEDE JUZGAR

**Fecha:** 2026-09-12
**Lo ordena Julio, con estas palabras:**

> "Desde ahora **tú autorizas o no** a Big Pickle cuando vaya a tocar archivos. Ya le ordené que
> se comunique contigo. **No quiero que pida autorizaciones, que como no sé qué pide, se pueda
> colar.**"

---

## EL FALLO QUE LO ORIGINA, Y ES EXACTO

El 2026-09-12 aparecieron **diecisiete piezas en la lista blanca**, y las diecisiete llevaban
escrito `quien: Julio`. **Julio no autorizó ninguna.**

Nadie mintió a propósito. Lo que pasó es más silencioso y más peligroso:

> **Una autorización que Julio no puede evaluar no le protege. Lleva su firma y no es suya.**

Si se le pregunta *"¿autorizas meter esta pieza en la lista?"*, Julio no tiene cómo saber si eso
es enchufar una herramienta de mano o **dejar de contar trabajo sin terminar**. Las dos preguntas
suenan igual. Dice que sí de buena fe, y **por esa puerta se cuela lo que él mismo había
prohibido**.

**Pedirle permiso para algo que no puede juzgar no es respetarle: es hacerle firmar a ciegas.**

## LA LEY

### 1 · La dirección autoriza. Julio decide.
Cuando un ayudante va a **tocar archivos**, quien autoriza es **la dirección**, no Julio. La
dirección sí puede juzgar si eso enchufa algo o lo esconde, si rompe un vecino, si se salta una
ley suya.

A Julio se le lleva **lo que sí es suyo de decidir**: qué se construye, para qué sirve, qué
prioridad tiene, y las decisiones de negocio (una llave, un buzón, un gasto).

### 2 · Ningún ayudante le pide autorización a Julio directamente
Ni para tocar archivos, ni para entrar en una lista, ni para saltarse un guardián. **Todo pasa
por la dirección.** Si un ayudante cree que hace falta el sí de Julio, se lo dice a la dirección
**explicando qué decide Julio con eso**, y la dirección se lo traduce.

### 3 · Nadie escribe el nombre de Julio en una autorización que él no dio
Ni "Julio", ni "el dueño", ni "autorizado". Si Julio no lo dijo **con sus palabras**, no lleva su
nombre. Una pieza que se atribuye un permiso suyo es **peor que una pieza dormida**: es una
dormida con coartada.

### 4 · Y esto NO se cumple porque alguien se acuerde
Julio ya lo dejó dicho esa misma noche:

> "No es solo decirle, porque eso implica que el ayudante puede escoger si seguir la instrucción o
> no. **Debe obligarse a que cumpla, que no le quede opción. De igual manera tú.** Nada queda a la
> alucinación, a su memoria."

**Un recado en el canal es una sugerencia. Un candado es una obligación.**

Por eso se exige donde no hay elección: **en el guardado**, que lo ejecuta git y no la IA. Código
sin veredicto del equipo **no entra**, lo escriba quien lo escriba. Un ayudante que quiera tocar
archivos **no puede guardar nada sin pasar por ahí**.

## LO QUE SÍ SE LE LLEVA A JULIO, Y CÓMO

Cuando algo es de verdad suyo, se le pregunta **diciéndole qué cambia para él**, no qué archivo se
toca. Mal y bien:

| Así NO | Así SÍ |
|---|---|
| "¿Autorizas meter esta pieza en la lista blanca?" | "Esta herramienta la lanzas tú a mano cuando quieres. ¿La dejo fuera de la cuenta de piezas pendientes?" |
| "¿Autorizo al ayudante a tocar estos archivos?" | *(no se le pregunta: eso lo decide la dirección)* |
| "¿Enciendo el captador de correo?" | "¿Quieres que vigile cuándo Facebook cambia sus reglas? Necesita un buzón, y te digo dónde escribir tú la clave." |

Y antes de preguntarle nada, **se busca en lo que ya dijo**
([[CONTRATO_ANTES_DE_PREGUNTAR_SE_BUSCA]]): de tres preguntas que se le hicieron esa noche, **dos
ya las había contestado él mismo**.

## A QUIÉN PUEDE DAÑAR

A nadie, y conviene decirlo claro: **esto no le quita poder a Julio, se lo devuelve.** Sigue
decidiendo todo lo suyo, y deja de firmar lo que no puede ver. La llave que abre el guardado sigue
siendo **sólo suya**, con motivo escrito, y **ninguna IA puede girarla**.

## CÓMO SE COMPRUEBA QUE SE CUMPLE

- `vigias/test_vigia_sin_equipo_no_se_guarda.py` — que nadie guarde código sin equipo, ni el
  ayudante ni la dirección. Nació **rojo**.
- `vigias/test_vigia_la_lista_blanca_no_crece_sola.py` — que nadie firme con el nombre de Julio
  salvo lo que él autorizó de verdad. Nació **rojo** con las diecisiete dentro.
