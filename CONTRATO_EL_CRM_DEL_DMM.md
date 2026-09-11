# CONTRATO — EL CRM DENTRO DEL DMM

**Julio, 2026-09-11 (punto 5):**

> *"Que todas las skills del CRM estén; encárgate de planificar, crear la arquitectura, trazar el
> mapa, legislar fuerte, poner candado, crear vigías, programas, para que esto sea un CRM dentro
> del DMM, que sea muy fácil de usar, que cree automatizaciones."*

---

## EL PUNTO DE PARTIDA, MEDIDO (2026-09-11)

**Lo que ya existe y está enchufado:** la libreta de contactos con su embudo
(prospecto → contactado → cotizado → vendido), el registro de ventas y el perfilador de clientes.

**Lo que sabe hacer hoy la libreta: CUATRO cosas.** Apuntar un contacto, marcarlo como vendido,
abrirlo y listar. **El estado lo mueve Julio a mano.**

**Lo que NO existe, comprobado buscándolo:**
- **Ni una sola regla del tipo *"si pasa esto, haz aquello"*.** El motor de automatizaciones no
  existe. Lo que hoy se llama automatización es **un calendario para programar publicaciones**.
- **Ni citas ni agenda de clientes.** No hay disponibilidad, ni reserva, ni confirmación.
- **Ni carpeta de habilidades en el negocio.** Cero.
- **Ni motor de seguimiento.** Hay una pantalla, pero nada que diga *"este lleva 5 días callado"*.

---

## LA ARQUITECTURA — CUATRO CAPAS

| Capa | Qué guarda | Su regla dura |
|---|---|---|
| **1. La libreta** | quién es cada cliente, de dónde salió, en qué punto está, su historia entera | **Un cliente, UNA ficha.** Nunca dos |
| **2. El embudo** | los puntos por los que pasa | Se mueve **por un hecho**, nunca por una opinión, y queda la fecha y el motivo |
| **3. Las automatizaciones** | las reglas *"si pasa esto, haz aquello"* | Todo lo que **salga a un cliente** pide el permiso de Julio. Sin excepción de formato |
| **4. La cara** | lista, ficha, embudo y un botón por acción | **Si hay que explicársela a Julio, está mal hecha** |

---

## LAS HABILIDADES QUE FALTAN — CADA UNA CON SU GUARDIÁN

| # | La habilidad | ¿Cuenta o juicio? |
|---|---|---|
| 1 | Meter un cliente **sin duplicarlo** (casa por correo y teléfono antes de crear) | **cuenta** |
| 2 | **Moverlo de punto** en el embudo, con el hecho que lo justifica | **cuenta** |
| 3 | **Contar el embudo**: cuántos hay en cada punto y cuánto llevan parados | **cuenta** |
| 4 | **Cazar al dormido**: quién lleva más de X días sin moverse | **cuenta** |
| 5 | **Escribir el mensaje** de seguimiento con el contexto del cliente | **juicio: equipo** |
| 6 | **Disparar la automatización**: la regla que une el hecho con la acción | **cuenta** |
| 7 | **La ficha completa**: todo el historial de un cliente en una pantalla | **cuenta** |
| 8 | **Importar de una hoja** sin duplicar, diciendo qué descartó y por qué | **cuenta** |

**Siete de ocho son CUENTAS: las hace un programa, gratis.** Solo una necesita una IA. Eso es lo
que manda `CONTRATO_MENOS_IA_MAS_PROGRAMA.md`, y aquí se cumple desde el diseño, no después.

---

## LAS LEYES DEL CRM (cada una con su candado)

### Ley 1 — Un cliente, una ficha
Duplicar es el fallo número uno de todo CRM del mundo. **El candado:** meter un contacto que ya
existe (por correo o por teléfono) **no crea otro**: actualiza el que hay y lo dice.

### Ley 2 — Un movimiento sin motivo no es un movimiento
Nadie pasa de "contactado" a "cotizado" porque sí. **El candado:** mover sin el hecho que lo
justifica se rechaza.

### Ley 3 — Nada sale al cliente sin el sí de Julio
Ni un texto. Es `CONTRATO_SIN_SU_PERMISO_NO_SALE_NADA.md`, aplicado también aquí. **El formato no
decide.** Una automatización que manda mensajes sin permiso es la forma más rápida de quemarle la
marca.

### Ley 4 — Lo que entra, entra validado
Correo y teléfono se comprueban al entrar. **Y no se escribe un validador nuevo:** el del negocio
**ya existe y está dormido**. Se enchufa aquí. Duplicarlo sería el mismo fallo que perseguimos.

### Ley 5 — Si Julio no sabe usarlo solo, no está terminado
No es una frase bonita: es el criterio de aceptación. **La prueba es que Julio lo use sin que
nadie le explique nada.**

---

## A QUIÉN PUEDE DAÑAR

- **A la libreta de hoy:** sus cuatro funciones se quedan, pero dejan de ser la puerta principal.
  **No se borra nada**: se construye encima.
- **A quien meta contactos a mano en bruto:** ya no podrá duplicar.
- **A las prisas:** ninguna automatización sale sin permiso, aunque sea "solo un texto".

## CÓMO SE COMPRUEBA QUE SE CUMPLE

- Se mete el mismo cliente dos veces → **hay una sola ficha**.
- Se intenta mover a un cliente sin motivo → **no se mueve**.
- Se deja a un cliente quieto los días del tope → **aparece en la lista de dormidos**.
- Se dispara una automatización que manda algo → **pide permiso y, sin él, no sale**.
- Se importa una hoja con repetidos → **dice cuántos descartó y por qué**.

**Y la prueba de verdad:** que Julio meta un cliente, lo mueva por el embudo y lo vea aparecer
solo en la lista de dormidos, **sin que nadie le enseñe cómo**.
