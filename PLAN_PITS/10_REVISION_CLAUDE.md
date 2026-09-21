# Revisión conjunta (A-41) — la mitad de Claude

> Hecha por separado de la de Codex, para que las dos miradas no se contagien. Solo lo **medido**
> estos días (2026-09-20 y 21), con su prueba. Lo supuesto va marcado. Se cruza con la de Codex en
> la hoja 11.

## 1.0 La información que llega a las IA

| Hallazgo (medido) | Evidencia | Propuesta | Programa o IA |
|---|---|---|---|
| El material se corta en trozos de 40 renglones elegidos por parecido de palabras; en archivos cortos gana la **portada** y no la función | 3 rondas pagadas perdidas; obrero: "el material solo trae las líneas 1-40" (archivo de 103) | Archivo de ≤600 renglones **entero** (orden 29, pieza ya diseñada) | PROGRAMA |
| Cuando el encargo **describe** la pieza en vez de nombrarla, el material no la trae | 8 rondas perdidas con `NO_ENCONTRADO` (órdenes 16-24, primera vuelta) | El revisor de programa frena gratis un encargo que no nombra ninguna función ni archivo que exista | PROGRAMA |
| Groq no cabe nunca: los paquetes pesan 26.000-40.000 letras y aguanta 19.000 | cada ronda: "GPT-OSS 120B no le cabe (…) → se le salta" | Dejar de ofrecerle trabajo que no cabe (se mide antes de mandar) | PROGRAMA |
| Las leyes están **dispersas**: 66 contratos + CLAUDE.md + leyes del ayudante + acuerdos; el método de operar está en 5 documentos | punto 1.6 | Un **índice de leyes** generado por programa: una línea por ley, con dónde vive y qué candado la hace cumplir | PROGRAMA |

## 1.1 Más rápida, precisa y económica

| Hallazgo (medido) | Evidencia | Propuesta |
|---|---|---|
| **El mayor desperdicio: un solo trozo por ronda.** La pieza que aplica varios existía y **nadie la llamaba** | cada arreglo de 2 sitios costó 2-4 rondas; `aplicar_cambios` sin llamadas | Ya hecha `aplicar_propuesta` (sabotaje 3/3); faltan enchufarla y avisar al obrero (órdenes 55-60) |
| Pruebas que **no pueden ponerse rojas** entraron como buenas: una devolvía en vez de afirmar, otra se saltaba, dos reventaban | órdenes 18, 20, 30, 46 | El revisor de programa las frena gratis antes de pagar (órdenes 40-45) |
| El vigilante de legislar recoge **renglones de máquina**: 26, 14, 53… por turno, resueltos a mano | medido cada turno | Regla de palabras de máquina (órdenes 30-31) y, de raíz, el guardador (1.5) |

## 1.2 Autorreparación

| Hallazgo (medido) | Propuesta |
|---|---|
| El perito (Claude) no contestó **3 de 3** veces de noche: sin cupo o sin ventana | Si Claude no contesta, entra Codex (órdenes 50-51) |
| La máquina ya recoge sola lo que frena el guardia y ya sigue sola el método de la prueba roja | Funciona; falta que recoger no pise trabajo más nuevo (orden 37, con la medida corregida) |
| Un fallo que se repite 3 veces con la misma causa para el frente, pero la causa la clasifica el perito | Clasificar la causa **por programa** cuando el aviso es conocido (`NO_ENCONTRADO`, `HUMO`, sintaxis, guardia) y solo pedir perito para lo nuevo |

## 1.3 Velocidad entre programas

| Hallazgo (medido) | Propuesta |
|---|---|
| El candado de cierre corre la **batería entera (4-5 min)** al final de cada turno y **para en falso** por las pruebas que esperan su arreglo | Misma regla que ya tiene el guardia (órdenes 61-62) |
| Dos programas escriben la **lista de tareas a la vez** sin candado: error de escritura medido (`Errno 22`) | Escritura atómica (temporal + reemplazo) en todo lo que se escribe en la memoria |
| La revisión de Big Pickle tarda 80-160 s; DeepSeek, 5 s | El juez de la prueba ya evita pagar revisión cuando la prueba lo demuestra (A-39); extenderlo a más casos |

## 1.4 Qué más se reemplaza por programas
- Sale el mismo patrón en todo lo medido: **lo que falló una vez por olvido humano o de IA, lo comprueba un programa** (marca de crear, nombre de la pieza, texto repetido en el sabotaje, prueba que no puede ponerse roja).
- DMM todavía no se ha revisado con esta mirada: **pendiente** para la segunda vuelta.

## 1.5 El guardador (medido que hoy no existe)
Hoy existe un vigilante que recoge lo que Julio escribe, pero: (a) recoge **ruido de máquina**, (b) no
distingue **repite / nueva / parte de una directriz principal**, (c) lo deja en una lista aparte y **no
en la memoria indexada**, y (d) el forense del 14-09 ya midió texto del sistema guardado como si fuera
de Julio. Propuesta de un **programa guardador**:
1. Toma **solo lo que Julio tecleó** (los ganchos de Claude y de Codex traen el mensaje; se quitan por
   marcas los avisos del sistema y lo citado de la máquina).
2. Lo compara, **por programa**, con los acuerdos y órdenes que ya existen: igual → *repite* (y se
   cuenta); muy parecido → *amplía el acuerdo A-x*; distinto → *nueva*.
3. Lo escribe **entero** donde toca (libro de acuerdos + nodo de la memoria indexada) y lo enlaza.
4. La IA solo entra cuando el programa no puede decidir si "es la misma directriz" (juicio).

## 1.6 El método de operar (ya definido, disperso)
Está en: acuerdo **A-1**, contrato de los **4 pasos** para construir un proyecto, contrato de las **5
preguntas** del análisis de fondo, contrato **cuenta o juicio**, y los **puestos** del plan v4 §3.
Propuesta: **una sola hoja del método**, corta, que los una en orden y enlace cada paso a su candado.

## 1.7 Modo ingeniero automático para todas las IA (inventario medido)

| IA | ¿Obligada por mecanismo? |
|---|---|
| Claude | **Sí**: ganchos al arrancar y en cada mensaje |
| Codex | **Sí cuando lo llama el programa** (configuración, reglas, ganchos por el puente; probado). **Falta**: en su ventana, los ganchos necesitan una confianza que hoy solo se da a mano |
| DeepSeek, Groq, Gemini | **Sí**: solo trabajan dentro de los encargos del Ingeniero |
| Big Pickle | Sí cuando la llama el programa; su ventana propia (OpenCode) tiene su plugin del canal: **sin medir** |
| Cursor, Copilot, Cline | **No**: están instalados o nombrados y **nada los obliga** (supuesto a confirmar midiendo) |
