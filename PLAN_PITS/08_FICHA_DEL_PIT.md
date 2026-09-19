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

## ANTES de seguir el paso 3: tareas de la orden A-38 (Julio, 2026-09-19)
En este orden; cada una con vigía y sabotaje; DeepSeek escribe; revisa Big Pickle o, si está caído, otra IA con solo lo necesario.
| Nº | Qué | Pieza | Cómo se hace cumplir |
|---|---|---|---|
| E-1 | El revisor recibe solo lo necesario: tope único y chico del material del revisor (sin la excepción de 40.000 letras para Big Pickle) | cuerpo/obrero.py | vigía: el material del revisor nunca pasa el tope |
| E-2 | Si el revisor pedido está caído, revisa el siguiente de la fila que no sea quien escribió | cuerpo/obrero.py, cuerpo/cuotas.py | vigía con revisor caído |
| E-3 | Antes de revisar, un programa comprueba que el archivo cambiado CARGA (se importa en una copia) | cuerpo/obrero.py o arnes/revisor_de_programa.py | vigía: import olvidado frena antes de gastar revisión |
| E-4 | Freno nº2 corregido: solo exige las palabras que el encargo manda cambiar | arnes/revisor_de_programa.py | vigía con los encargos reales que frenó en falso |
| E-5 | Freno nº8: un cambio que solo borra es válido | arnes/revisor_de_programa.py | vigía |
| E-6 | Freno nº9: fotocopia solo con marcas TEXTO_VIEJO:/TEXTO_NUEVO: al inicio de línea | arnes/candado_terminal.py | vigía |
| E-7 | Texto viejo repetido: se busca dentro de la función que el obrero dice tocar | cuerpo/aplicador.py | vigía |
| E-8 | Juez de la prueba (programa): vigía roja con lo viejo, verde con lo nuevo, vecinas verdes, sabotaje automático | cuerpo/capataz.py (reusa vecinas, guardar_en_la_historia, volver_atras) | vigía + sabotaje |
| E-9 | Medidor: rondas por guardado y segundos de revisión por día; meta ≥ 0,9 guardados por ronda | programa conectado al cierre | vigía |
| E-10 | Claude no responde dos veces: regla en la memoria y, si es medible, candado de cierre | memoria, arnes | — |
| E-11 | El candado de memoria no hace repetir acciones: lecciones con disparador del PELIGRO (no de palabras comunes) y cuenta por lección | arnes/candado_memoria.py, memoria/FALLOS.json | test_vigia_los_avisos_no_hacen_repetir |

### Estado E-1..E-11 (2026-09-19, 15:00)
- HECHO con vigía y sabotaje por programa: E-1 (tope del revisor), E-2 (si Big Pickle cae revisa otro; reemplaza la ley del 15-09), E-3a (el programa revisa ANTES que la IA; si frena no se paga), E-6 (fotocopia solo con marcas), nº10 y nº12 (humo con cadenas), E-8a (`arnes/sabotaje.py`: el sabotaje lo hace un programa; listas en memoria/sabotajes/), E-11 (5 lecciones con disparador del peligro + cuenta por lección), guardia: "nueva" = no está en HEAD, revisor ve el trozo tocado (del paquete o del DISCO, ventana de 40 líneas si la función es larga) y sabe lo que ya comprobó el programa.
- A MEDIAS: E-3b `no_carga` existe (4 falsos de 318 archivos, por eso solo frena si antes cargaba); su conexión en `revisar` (regla 4b) quedó sin revisor. Su vigía está APARTADA en memoria/trabajos_sin_revisar/test_vigia_revisar_frena_si_deja_de_cargar.py.ESPERA_SU_PIEZA (el candado de cierre no deja la batería roja); se devuelve a vigias/ junto con la pieza, en el mismo commit.
- FALTA: E-4 (freno nº2), E-5 (borrar), E-7 (texto repetido), E-8b (juez de la prueba completo), E-9 (medidor); el relevo aún intenta Gemini 3 y LM Studio (A-31 los sacó); más lecciones con disparador de palabra común (LM Studio, memoria).
- FALLA DE PRUEBA encontrada al cierre: con `INGENIERO_BATERIA_COMPLETA=1` puesto, 3 pruebas de vigias/test_vigia_vecinas.py salen rojas porque no se aíslan de esa variable (vecinas elige todo). Cura: `monkeypatch.delenv("INGENIERO_BATERIA_COMPLETA", raising=False)` en esas pruebas. Sin eso, el cierre del paso 7 sale rojo en falso. Batería normal: 919 verdes.
- PARADO a las 15:00: Big Pickle caído desde las 10:48 y las gratis agotadas por hoy (Groq, Gemini flash-lite, Gemini 3). Sin revisor no se guarda nada (así debe ser).
