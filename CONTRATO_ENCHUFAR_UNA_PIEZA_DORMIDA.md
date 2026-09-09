# CONTRATO — CÓMO SE ENCHUFA UNA PIEZA DORMIDA

**Julio, 2026-09-09:**

> *"Continúa con las 6 gratis, en loop, usa el equipo, arnés, legisla lo que falte, pon candado,
> mira que todo esté conectado, sé económico, usa todo el protocolo de trabajo. Dota de
> habilidades de modo que sea un programa capaz, no humo."*

Esta ley recoge el método que salió de enchufar **doce piezas dormidas seguidas** en la
aplicación de marketing, sin gastar un céntimo. No es teoría: es lo que funcionó, y también lo
que falló.

---

## POR QUÉ NACE

De 82 piezas de esa aplicación, **22 estaban construidas, probadas y sin que nadie las llamara.**
El plan las daba por *"departamentos que faltan"*. **No faltaban: estaban desenchufadas.**

Enchufarlas a lo bruto habría sido humo. De ahí este método.

---

## LOS SEIS PASOS. NO SE SALTA NINGUNO

### 1 — Mirar qué hace de verdad, no lo que promete su nombre
Se lee **su boca** (qué funciones ofrece) y **qué datos pide**. Ahí aparecen las sorpresas:
*el departamento de publicidad no podía funcionar porque la aplicación nunca preguntaba cuánto
se había gastado.* Enchufarlo sin eso habría sido humo.

### 2 — ¿GUARDA lo que produce? Si no, se repara la raíz ANTES de enchufar
**Cuatro de las doce vivían solo en memoria** y se perdían al apagar: las metas, el historial,
el calendario y el grafo del negocio.

> **Enchufar una pieza que pierde lo que guarda es enchufar humo.**

Se repara reusando lo que ya guarda (`cuerpo/almacen.py`), **cada negocio con lo suyo**, y
**guardando solo** — sin que nadie tenga que acordarse.

### 3 — La vigía PRIMERO, y tiene que nacer roja
Y comprueba **las dos caras**:
- que **con datos reales sale el resultado**;
- que **sin datos NO SE INVENTA NADA**.

La segunda es la que evita el humo. *Un número de dinero inventado es peor que ninguno: el dueño
movería su dinero a ciegas.*

### 4 — Si es una CUENTA, la aplica el copista. Gratis
Copiar un texto ya decidido **no es juicio**. Las doce piezas se enchufaron así: **cero llamadas
a ninguna IA**. Lo que sí es juicio —si el sitio elegido es el correcto, si rompe un vecino— **se
le pide al equipo**, y eso no se salta.

### 5 — Correr TODAS las vigías, no solo la nueva
Un cable puede romper un vecino. Solo se sabe corriéndolas todas.

### 6 — Guardar, contando también lo que salió mal
El mensaje de guardado dice **qué se rompió y cómo se reparó**. Un guardado que solo cuenta lo
bueno enseña la mitad.

---

## LO QUE ESTÁ PROHIBIDO

1. **Enchufar una pieza que pierde lo que guarda.** Es humo.
2. **Enchufarla por datos que nadie rellena.** Pasó con los gustos: sabía agrupar por tema,
   formato y tono, y **nadie etiqueta los posts**. Se enchufó por canal, que sí existe, y lo
   otro quedó apuntado como lo que falta.
3. **Forzar a la pieza cuando se defiende.** El grafo rechazó un dominio inventado. **Se
   corrige el cable, nunca se afloja la pieza.**
4. **Poner algo lento en una pantalla del cliente.** Fallo real medido: dos consultas a internet
   dentro de una pantalla → **ocho minutos y medio de carga**. Se reparó mirando **una vez al
   día** y guardando: 1,8 segundos.
5. **Dejar dicho lo que se puede reparar.** Si se encuentra la raíz, se repara. Anotarla y
   seguir es escurrir el bulto.

---

## CÓMO SE COMPRUEBA QUE SE CUMPLE

`skills/nace_conectada.py` cuenta las piezas que nadie llama. **Una pieza que existe y nadie
llama cuenta como NO HECHA**, por muy verde que esté su vigía (`CONTRATO_CREAR_PIEZA_NUEVA`,
regla 6).

**Y la prueba de verdad no es una vigía verde: es que Julio lo vea funcionar.**

---

## LO MEDIDO CON ESTE MÉTODO (2026-09-09)

| | |
|---|---|
| Piezas despertadas | **12 de 22** |
| Coste | **cero** — todas con el copista |
| Vigías | **489 verdes** |
| Raíces reparadas antes de enchufar | **4** (no guardaban nada) |
| Fallos propios cazados por sus vigías | **2**, reparados en el mismo rato |
