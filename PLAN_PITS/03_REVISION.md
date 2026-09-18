# REVISIÓN: cada acuerdo contra el plan v3 (2026-09-18)
✅ cubierto · ⚠ a medias · ❌ faltaba. Todo lo que no era ✅ se corrige en el plan v4.

| Acuerdo | En v3 | Qué faltaba o estaba mal | Corrección en v4 |
|---|---|---|---|
| A-1 preguntar antes de construir | ✅ | — | — |
| A-2 programa primero; crear matrices y tablas de verdad | ⚠ | Marcaba programa o IA por tarea, pero **no creaba las matrices ni las tablas de verdad** de DMM, y **no hacía primero la lista de "qué IA se reemplaza por programa"** que Julio ya había ordenado | Paso 2 del loop: inventario "cuenta o juicio" y reemplazo; la ficha genera matriz y tabla de verdad |
| A-3 repartidor por nombre y función | ⚠ | Se perdió el orden de búsqueda (nombre → función → significado → "no existe") | Restaurado en el puesto Bibliotecario |
| A-4 mapa de flujos, nada desconectado | ⚠ | Había mapa del código, pero **no de flujos entre sí**, ni revisión de piezas sueltas | Mapa de flujos + vigía de piezas huérfanas antes de cada commit |
| A-5 papeles | ⚠ | **Big Pickle nunca se ha llamado de forma automática (0 rondas).** Todo el pit dependía de algo que no existe | Paso 1: conectar Big Pickle por OpenCode y medirla; si no se puede, se dice y se usa el reemplazo medido |
| A-6 legislar, vigías, nace conectado | ❌ | **v3 no decía qué pasa con los 21 candados existentes.** Tampoco cómo un fallo se convierte en ley ni el "nace conectado" | Los candados se reparan como tareas del pit (ninguno se quita). El forense produce la ley y su vigía. Vigía de "nace conectado" |
| A-7 aciertos nunca autovalidados | ⚠ | Si Julio prueba solo al final, no quedaba claro quién da por bueno lo intermedio | Tres estados: *pasa pruebas* → *revisado por otra familia* → *HECHO solo con la prueba de Julio* |
| A-8 vía y rama canónica | ⚠ | **Hay 101 cambios sin guardar en el ingeniero** y 7 planes de DMM (3 jubilados todavía en la carpeta) | Paso 0: el portero no arranca con trabajo sin guardar. Se resuelve con commit en la rama canónica. Los planes jubilados pasan a "reciclado" |
| A-9 medir y eliminar IA | ⚠ | Faltaban los datos de todo el tiempo | Hecho en el forense: se eliminan Groq 20b, Gemini 1 y 3, local y OpenRouter. Se agrega reloj al registro |
| A-10 filtros | ✅ | — | — |
| A-11 ingeniero de Marketing | ❌ | **v3 lo había olvidado** | Tarea del loop. Hay una duda sin resolver (Q2) |
| A-14 ningún candado se quita | ⚠ | v3 no nombraba los candados existentes | Ver A-6 |
| A-14 garantía de trabajar con el equipo | ⚠ | Para "Claude sin manos" dependía de la lista de permisos. **Esos candados son para Claude; los programas del pit no pasan por ellos.** El pit necesita sus propias reglas escritas en su código | Reglas del pit dentro del propio pit, con vigías de sabotaje |
| A-15 rapidez | ⚠ | **El candado de guardar corre 780 pruebas (3 a 4,5 min) en cada commit.** Con 3 commits por tarea, el pit sería lentísimo | En cada commit, solo la pieza y sus vecinas. Batería completa al final del loop |
| A-16 aprobar una vez, loop, informe | ⚠ | Faltaba **cuándo se detiene el loop** y un **tope de gasto** | Paradas: DMM terminado, frente parado por 3 fallos del mismo tipo, o tope de gasto |
| A-17 Claude solo donde aporta | ⚠ | Recomendé Claude en "el alma"; Julio solo nombró la reparación | Pregunta Q1. Además: Claude llamado por el programa **gasta del plan de Julio** |
| A-18 Big Pickle en JSON | ✅ | — | — |
| A-19 ahorro | ✅ | — | — |
| A-20 nada en memoria | ⚠ | Estaba en el plan, pero no se había guardado nada | Hecho: esta carpeta. Se sube con commit en el paso 0 |
| A-21 tareas, disparadores, multitarea | ⚠ | **Varias tareas a la vez + commits en una sola rama pueden chocar** | Fila de commits: las tareas corren en paralelo, pero guardan de a una |
| A-22 forense, no repetir | ✅ | — | — |
| A-23 commit de todo, sin versiones | ⚠ | Mismo choque de velocidad que A-15 | Igual que A-15 |
| A-24 antialucinación | ✅ | — | — |
| Orden: "que el flujo no se vuelva ley contradictoria" | ❌ | No estaba | Revisor de contradicciones en el libro de acuerdos y leyes (programa + Big Pickle en JSON) |
| Orden: "la memoria grafo es parte del equipo" | ⚠ | Implícito | Explícito: el bibliotecario ES la memoria grafo; toda IA pide la información ahí |

## Lo que no sé y no está en los archivos
- **Q1.** ¿Claude participa en "entender el alma" una vez por proyecto, o **solo** en la reparación (forense), como sugeriste? En los dos casos Claude es llamado por un programa, en solo-lectura, y gasta de tu plan de Claude.
- **Q2.** Dijiste: *"el de Marketing es el que debe usarse para construir marketing, o si sobra…"*. Esas piezas (director, analista, roles, constructor, bucle, auditor, motor) viven **dentro de DMM**, y DMM podría estar usándolas. **¿Se quedan dentro de DMM como parte del producto, o se mueven al ingeniero y se borran de DMM?** Antes de tocarlas, un programa comprobará si DMM las usa.
- **Q3.** Big Pickle es de pago por OpenCode. **¿Tiene tope de gasto o de uso** que la máquina deba respetar?
- **Q4.** Los **101 cambios sin guardar** del ingeniero: ¿se guardan todos tal cual (commit), o el equipo los revisa primero?
## Respuestas de Julio (2026-09-18)
- Q2 → A-26 · Q3 → A-27 · Q4 → A-28. Q1 → A-29 (los dos trabajos). Plan v4 aprobado → A-30.

## Políticas de OpenCode y Big Pickle (revisadas en la documentación oficial, 2026-09-18)
- En OpenCode Zen, **Big Pickle es gratis "por tiempo limitado"**. No cobra por uso.
- **Privacidad:** mientras sea gratis, *"los datos recogidos pueden usarse para mejorar el modelo"*. Es el mismo riesgo que Gemini gratis: **nunca mandarle llaves, credenciales ni datos de clientes.** El filtro de pedazos debe bloquearlo.
- **Recarga automática:** la cuenta de Zen **recarga 20 USD sola cuando el saldo baja de 5 USD**, salvo que se desactive. Para que el tope de 5 USD sea real, **Julio debe desactivar la recarga automática y poner un límite mensual** en su cuenta de OpenCode. Es un ajuste de su cuenta y lo hace él.
- **Límite de uso:** una fuente no oficial dice 200 pedidos cada 5 horas. **Sin confirmar:** la máquina lo medirá.
- **Cómo lo llama un programa:** OpenCode trae una orden sin ventana para correr un pedido, con elección de modelo y respuesta en formato de datos, y puede quedar conectada a un servidor ya abierto para no demorar al arrancar. La configuración local de OpenCode ya le **prohíbe editar**: Big Pickle ya está "sin manos".

- "DMM terminado" **no hace falta preguntarlo**: está en el plan vigente de DMM, "Lo que falta para terminar el DMM" (2026-09-12), con el norte en el contrato "Objetivo: Marketing Manager".
