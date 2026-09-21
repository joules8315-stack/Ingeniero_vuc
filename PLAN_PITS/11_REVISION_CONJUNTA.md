# Revisión conjunta A-41 — Claude + Codex (2026-09-21)

> Cruce de la hoja 10 (Claude) con la revisión de Codex (solo lectura, 41 citas comprobadas contra
> los documentos: 40 exactas y 1 con otro formato, A-36 va en tabla). Cada una se hizo por
> separado. Nada de esto cambia el plan v4 sin el sí de Julio (A-30).

## 1. En qué coincidimos (las dos miradas llegaron solas a lo mismo)

| Punto | Lo que hay que hacer | Quién | Órdenes |
|---|---|---|---|
| 1.0 | Antes de pagar una consulta, un **programa comprueba que va todo**: la pieza, el encargo, sus relaciones y la prueba. Un archivo corto va entero. | PROGRAMA | 29, nuevas A |
| 1.1 | **Conectar lo que ya existe y nadie usa**: arreglar varios trozos en una sola ronda. | PROGRAMA | 55-60 |
| 1.2 | **No anunciar que terminó** con trabajo fallido o en espera; recuperar solo copias comprobadas; relevo de Claude y Big Pickle hacia Codex. | PROGRAMA | 37, 50-51, 61-62 |
| 1.2 | Distinguir una prueba que **descubre el fallo** de una que **ni siquiera arrancó**. | PROGRAMA | 38-45 |
| 1.5 | **Guardador**: cada directriz entera, quién, cuándo y a qué acuerdo pertenece; la IA solo cuando haya duda de significado. | PROGRAMA | nueva B |
| 1.6 | **El método ya está definido** (los 8 pasos). Falta que un programa **exija la prueba** de cada paso, no que esté escrito. | PROGRAMA | nueva C |
| 1.7 | **No está demostrado** que todas las IA estén obligadas por mecanismo en todas sus entradas. Se comprueba entrada por entrada. | PROGRAMA | 54, nueva D |

## 2. Lo que vio solo Codex (a medir antes de actuar)

1. **La máquina toma su lista de tareas del Ingeniero aunque se le nombre otro proyecto.** Si es
   cierto, **bloquea el punto 5 (DMM)**: trabajaría sobre el proyecto equivocado. Primero en la cola.
2. **La entrada directa de Big Pickle** no tiene completa la protección de datos. Es de
   **seguridad**: se mide y se cierra antes de mandarle nada más.
3. Las entregas entre programas se reconocen **buscando una frase** en el mensaje. Propuesta: cada
   entrega lleva su número de tarea, su resultado y la prueba de que se guardó.
4. Una **repetición** de Julio puede volver a abrir una orden ya resuelta. Debe contar la
   repetición y respetar lo resuelto.
5. Algunas IA reciben instrucciones con un **reparto antiguo** del equipo.
6. La entrega al revisor **todavía permite recortes**.
7. **No hay un paso propio de revisión final** de la tarea terminada en el cierre.

## 3. Lo que vio solo Claude

1. **Groq nunca cabe**: los paquetes pesan 26.000-40.000 letras y aguanta 19.000. Se deja de
   ofrecerle trabajo sin medirlo antes.
2. **Dos programas escriben la lista de tareas a la vez** (error medido): escritura segura.
3. El cierre corre la batería entera (4-5 min) y **para en falso** por las pruebas que esperan su
   arreglo (medido hoy otra vez).
4. **Clasificar por programa** la causa de los avisos conocidos y llamar al perito solo para lo nuevo.
5. **Índice de leyes** generado por programa: una línea por ley, dónde vive y qué candado la cumple.

## 4. Diferencias
Ninguna de fondo: lo que cada uno vio solo **se suma**, no se contradice.

## 5. Contradicciones en los documentos
- El plan v4 §4 conserva «si no está disponible, la tarea espera (sin relevo)», pero A-40 aprobó el
  relevo con Codex. Manda lo más reciente; **cambiar el texto del plan necesita el sí de Julio**.
- **Los 5 USD al mes**: A-27 los pone solo a Big Pickle; la ficha P3-8 los suma con DeepSeek.

## 6. Preguntas para Julio
1. ~~Los 5 dólares~~ RESPONDIDA: "son ambas pagas" → tope a las dos juntas (A-27).
2. RESPONDIDA: sí, corregido el plan v4 §4 (entra la otra).

## 7. Orden de trabajo que sale de aquí
1. Medir y cerrar la **protección de datos de Big Pickle** (seguridad primero).
2. Medir si la máquina **confunde el proyecto** (bloquea DMM).
3. El **cierre no para en falso** y **no anuncia terminado** con pendientes (61-62 + revisión final).
4. **Todo completo antes de pagar**; sin recortes al revisor (29 + nueva A).
5. **Varios trozos en una ronda** (55-60).
6. **Relevo con Codex** (48-53).
7. **Guardador** + memoria indexada (nueva B).
8. **Hoja única del método** con su candado por paso (nueva C) e **inventario de entradas** de
   cada IA (nueva D).
