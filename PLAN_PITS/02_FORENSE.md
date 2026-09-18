# ANÁLISIS FORENSE — 2026-09-18 (medido con programas, sin IA)
Fuentes: los registros del ingeniero en `memoria/` (llamadas, decisiones del candado, fallos, rondas del equipo, cuotas, guardia) + el informe forense de Big Pickle del 2026-09-14 (nunca se aplicó).

## Las tres raíces
1. **Se construyó reaccionando, nunca diseñando.** Cada fallo trajo un candado y nunca hubo plano. Hoy hay 21 candados, 143 vigías y 66 leyes, y el ingeniero nunca se construyó con su propio método.
2. **Se mira en el espejo.** Se repara con el equipo roto, sus marcadores se califican solos ("400 aciertos, 0 frenos falsos") y 83 rondas las revisó la misma IA que las escribió.
3. **Aprende de datos sucios.** 14.838 de 20.388 decisiones vienen de pruebas automáticas, y hay texto del sistema guardado como si fueran órdenes de Julio.

## Datos
| Qué | Dato |
|---|---|
| Fallos guardados | 68: **54 del propio ingeniero**, 9 de Foto Informe, 5 de DMM |
| Candado de escritura (sin contar pruebas) | **3.724 frenos contra 1.826 pases**. Los frenos: 1.358 porque el candado no entendió la petición, 990 por "documento libre", 583 por diferencia de nombre, ~340 que protegían de verdad |
| Rondas del equipo | 1.645 en total: 956 aprobadas (58%), 335 rechazadas, 270 sin revisar, 64 rechazadas por el programa, 83 **autorrevisadas** |
| **Big Pickle** | **0 rondas automáticas.** El código solo "la deja archivada para que revise después". Hoy trabaja a mano por el canal. OpenCode está instalado, pero **nunca se conectó para que un programa la llame** |
| Guardar | 780 pruebas, 3 a 4,5 minutos cada vez. Los últimos intentos terminaron frenados (3 a 5 vigías en rojo) |
| Trabajo sin guardar | **101 cambios sin commit** en la carpeta del ingeniero. Choca con "commit de todo" |
| Planes de DMM | **7 documentos de "lo que falta"**: 3 marcados como jubilados pero todavía en la carpeta. El vigente es "lo que falta para terminar el DMM" (2026-09-12) |
| Informe de Big Pickle del 14-09 | 7 causas, 5 pares de leyes que se contradicen. **No se aplicó** |

## Las IA, con datos de todo el tiempo registrado
| IA | Llamadas | Fallan | Aguanta (tamaño del encargo) | Descanso cuando se agota | Veredicto |
|---|---|---|---|---|---|
| DeepSeek (paga) | 966 | **1%** | hasta ~230.000 | no se agota | Obrero principal |
| Groq 120b (gratis) | 638 | 64% | ~19.000; más no cabe | 3-4 min normal, a veces 19-35 min | Solo tareas pequeñas y revisión (100% bien revisando en la última semana) |
| Gemini 4 (gratis) | 796 | 65% | ~190.000 | 3-4 min | Revisor de reserva, tareas pequeñas |
| Gemini 2 (gratis) | 620 | 76% | ~190.000 | 3-4 min | Reserva de la reserva |
| Groq 20b (gratis) | 603 | 67% (49% en trabajo real) | ~20.000 | 3-35 min | **Eliminar** |
| Gemini 1 y 3 (gratis) | 460 / 408 | 92% / 94% | — | 3-4 min | **Eliminar** |
| LM Studio local | 259 | 97% | — | — | **Eliminar** |
| OpenRouter (3 cuentas) | 54 c/u | **100%** | — | — | **Eliminar** (muertas) |
| Big Pickle (paga) | 0 automáticas | — | — | — | **Conectar y medir** |

**Qué NO se puede medir hoy:** cuánto tarda cada tarea. El registro no anota el tiempo y solo guarda las últimas 1.000 llamadas.
**Hallazgo:** con los números de todo el tiempo, **el equipo depende en la práctica de DeepSeek**. Las gratis fallan 2 de cada 3 veces. Casi siempre es por tamaño (se les manda más de lo que aguantan) o por cupo por minuto. Si se les asignan **solo tareas pequeñas y con pausas**, pueden servir; hoy se les manda a ciegas.

## Los fallos, uno por uno
| # | Fallo | Dónde vive | Flujo afectado | Raíz |
|---|---|---|---|---|
| 1 | No se autorrepara | Reparación del ingeniero | Todos | 2 |
| 2 | Los candados frenan de más | Candado de escritura (equipo) | Construir | 1 |
| 3 | Bucle al cerrar | Candados de cierre y de legislar | Terminar | 3 |
| 4 | Avisos que no vienen al caso | Candado de memoria | Todos (gasto) | 2 y 3 |
| 5 | La IA se revisa sola (83 veces) | Reparto del equipo | Construir | 1 |
| 6 | Claude suelta al equipo | Sesión de Claude | Construir | 1 (una regla escrita no es un mecanismo) |
| 7 | Respuestas en blanco / relevo en cadena | Reparto de IA (cuotas) | Construir | Se manda sin medir tamaño ni cupo |
| 8 | Guardar lento y frenado | Guardia + candado de commit | Guardar | 1 (prueba todo, no lo tocado) |
| 9 | Leyes que se contradicen | 66 leyes + planes de DMM repetidos | Todos | 1 |
| 10 | Información cortada o con sobras | Repartidor (pedazos) | Construir | Falta un filtro de salida |
| 11 | Dos ingenieros | VUC + Asesor Marketing | Todos | 1 |
| 12 | Los informes no se aplican | Forense de Big Pickle | Mejora | Nadie es dueño del siguiente paso |
| 13 | Big Pickle nunca automatizado | Obrero | Revisión | Se diseñó sin comprobar cómo llamarla |
| 14 | 101 cambios sin guardar | Ingeniero | Todos | Guardar es lento y se frena (fallo 8) |
