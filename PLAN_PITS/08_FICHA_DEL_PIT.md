# Paso 3 del plan v4 — Ficha del pit (Claude arquitecto, A-29)

## Qué es
Un programa que corre una lista de tareas etiquetadas, en loop, hasta terminar: cada tarea va al equipo (DeepSeek escribe, Big Pickle revisa), se monta, se prueba (la pieza y sus vecinas), se guarda en la fila de commits, y si falla vuelve atrás, deja expediente y se anota. Se lanza con `python ingeniero.py pit <proyecto>`.

## Qué no es
- No escribe código por su cuenta ni decide qué hay que hacer: eso viene de la ficha del proyecto (Alma) y del equipo.
- No reemplaza a los candados ni al guardia: pasa por ellos.
- No usa a Claude para escribir ni revisar (A-5, A-32). Claude solo es perito cuando algo falla (A-29).

## Lo que no se puede romper
- El comando `equipo` sigue funcionando igual (el pit lo usa, no lo copia).
- El guardia de guardado, las huellas (A-34), volver atrás (P2-1).
- Ningún candado se quita (A-14).

## Cómo se sabe que está listo (plan v4 §7)
1. Una lista de 3 tareas de prueba corre sola hasta el final, cada commit trae su etiqueta.
2. Dos tareas de archivos distintos corren a la vez sin mezclarse; dos del mismo archivo, en fila.
3. Se sabotea cada regla (sin etiqueta, huella que ya falló, se revisa a sí mismo) y el pit frena.
4. Un fallo forzado deja expediente y una tarea nueva distinta.
5. Se para solo: todo hecho, 3 fallos del mismo tipo en un frente, o tope de gasto.

## Pieza base: `cuerpo/capataz.py` (existe, nadie la llama, `marcar_estado` quedó partida)
Lista de tareas: `memoria/ORDENES.json` (del proyecto que corre el pit).

## Tareas (una por encargo; DeepSeek escribe, Big Pickle revisa; cada regla con vigía y sabotaje)
| Nº | Qué | Pieza | Depende | Modo |
|---|---|---|---|---|
| P3-1 | Reparar `marcar_estado` (su cuerpo quedó pegado al final de `comprobar_pasos`) + vigía | capataz.py | — | IA (reparar) |
| P3-2 | ETIQUETA: cada orden trae id, origen, repara, pieza, depende, modo (PROGRAMA/IA), razon, encargo; `validar_etiqueta` dice qué falta; sin etiqueta no se corre | capataz.py | P3-1 | IA |
| P3-3 | HUELLA QUE YA FALLÓ: sha del encargo+pieza; si ya falló no se vuelve a mandar igual (plan §2) | capataz.py | P3-2 | IA |
| P3-4 | DESPACHADOR: `listas_para_correr` = pendientes con sus dependencias hechas, sin dos de la misma pieza | capataz.py | P3-2 | IA |
| P3-5 | CORRER: `lanzar_al_equipo(proyecto, orden)` llama `equipo` con `--escribe deepseek --revisa bigpickle`, con tope de tiempo, y lee si quedó GUARDADO | capataz.py | P3-2 | IA |
| P3-6 | FILA DE COMMITS: `guardar_en_la_historia` espera su turno (candado de archivo) para que dos tareas no guarden a la vez | candado_equipo.py | — | IA |
| P3-7 | ETIQUETA EN EL REGISTRO: el cuaderno anota la etiqueta de la tarea (variable de entorno que pone el capataz) | cuaderno.py | P3-5 | IA |
| P3-8 | TOPE DE GASTO: suma lo gastado del mes (DeepSeek + Big Pickle ≤ 5 USD, A-27) y para | capataz.py | — | IA |
| P3-9 | EL LOOP: `bucle(proyecto)` corre en paralelo lo que se puede y se para solo por las 3 causas del plan §1 | capataz.py | P3-3..P3-8 | IA |
| P3-10 | FORENSE: expediente del fallo (programa) + P2-2 (citas verificadas por programa) + tarea nueva distinta | capataz.py / pieza nueva | P3-9 | IA |
| P3-11 | Comando `python ingeniero.py pit <proyecto>` | ingeniero.py | P3-9 | IA |
| P3-12 | Vigía "nace conectado": una pieza nueva que nadie llama no cuenta como hecha (reusar `skills/nace_conectada.py`) | capataz.py | P3-5 | IA |
| P3-14 | CRUZADO en el pit (plan §6 paso 3 lo nombra): una tarea sin vigía la recibe escrita a ciegas por el vigilante de cruzado; el código 2 del juez ("¿pasa la prueba?") lo decide la prueba CORRIDA en una copia, no la IA (P2-5) | cruzado.py + capataz.py | P3-9 | IA |
| P3-13 | Prueba de aceptación: 3 tareas reales corren solas (criterio 1-5 de arriba) | — | todo | programa |


**Claude sin manos (plan §2)**: la lista de permisos de solo lectura la activa Julio con su llave; se le prepara el comando al llegar al paso 4.
