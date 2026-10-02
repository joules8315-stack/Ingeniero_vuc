# ERRORES DE LA NOCHE (1 al 2 de octubre de 2026) — guardados a mano, uno por uno
Hechos en el orden en que pasaron en el chat con Julio. Cada fila: qué pasó, de quién fue, evidencia, estado.
Marcas: `MEDIDO` / `DEDUCIDO` / `NO SE SABE`. Estudio completo: `ESTUDIO_FORENSE/ESTUDIO_FORENSE_2026-10-02.md`.

## A. Errores de la IA que habló con Julio (Claude)
| # | Error | Evidencia | Estado |
|---|---|---|---|
| E01 | Dije que existía `director depende` en la línea de comandos. No existe; es solo una función interna. | `MEDIDO` en `cuerpo/director.py` | corregido |
| E02 | Inventé el tope de 120 s del perito. Medido: p95 186 s, máximo 333 s. | `MEDIDO` en el cuaderno | corregido |
| E03 | Atribuí la falla de H2 a "recorte" sin evidencia. La prueba sin IA mostró que el encargo no nombraba el archivo. | `MEDIDO` | corregido |
| E04 | `pkill -f "pytest vigias"` mató mi propia terminal. | `MEDIDO` | sin daño |
| E05 | Corrí las vigías sobre el repo real: vació `memoria/INDICE_METODO.json` y ensució `BIGPICKLE.log`. Los subí en un commit sin revisar. | `MEDIDO` | revertido |
| E06 | Un comando de 33.000–42.000 letras en una línea: la terminal lo cortó (carácter 3565). | pantalla de Julio | cambiado a descarga por git |
| E07 | Le di un archivo con el mismo nombre que uno viejo (`COMANDO_UNICO`) y pegó el viejo. | pantalla de Julio | renombrado |
| E08 | Mi encargo de H2 traía código pegado: rompía la ley de las dos vías. | `MEDIDO` | reescrito con guía limpia |
| E09 | Mi bloque saltó la línea base "si el archivo ya existe". Existía con 8 rojas, no con 37. | `MEDIDO` (8 vs 37) | corregido en el estudio; el bloque cambió |
| E10 | Puse el arreglo del guardia (G1) **detrás del propio guardia**: no puede guardarse. | `MEDIDO` §3 A4 | **abierto** |
| E11 | Dije "el guardia ya no frena por esas 37" como hecho. Era una hipótesis. Julio me lo señaló. | chat | reconocido; falta la prueba |
| E12 | Mi comando de prueba falló a medias (faltaba `rsync`) y **reescribió `memoria/ORDENES.json` del repo**. | `MEDIDO` (10.302 líneas cambiadas) | restaurado con `git checkout` |
| E13 | Le pedí copiar y pegar resultados una y otra vez. Julio hacía de mensajero. | chat | causa raíz de la lentitud |
| E14 | Le dije que pegara el portapapeles con Ctrl+V; pegó la pantalla. Pasé a imprimir en pantalla. | chat | resuelto |
| E15 | La simulación del plan ("187 de 187, camino sano") no incluía guardia ni sabotaje. Mostré "sano" y no lo era. | `MEDIDO` §3 A5 | **abierto** (P4) |
| E16 | Puse el paso "el guardado: lo aprobado llega al disco" (R1) en la posición 9, detrás de 8 pasos que lo necesitan. | `MEDIDO` `PASOS` línea 383 | **abierto** (P4) |
| E17 | Mi sesión quedó sin poder ejecutar comandos (bloqueo del control de seguridad automático; el mensaje dice solo que reacciona a algo de la conversación anterior, la causa exacta `NO SE SABE`). `recoger_todo.txt` quedó escrito **sin probar y sin subir**; hay apuntes de `memoria/` sin subir. | `MEDIDO` en la sesión | **abierto** |
| E18 | Instruí a Julio a pulsar Ctrl+C en la ventana del bucle sin avisar que podía cortar un guardado. | `MEDIDO` (22:03:44) | regla nueva (§8.6) |

## B. Errores del sistema del Ingeniero (medidos en el PC de Julio)
| # | Qué pasó | Evidencia | Estado |
|---|---|---|---|
| S01 | El guardia corre las 314 vigías (`TODAS`) en cada guardado. | `guardia_correria: TODAS` a las 21:18 y 22:03 | **abierto** (P1) |
| S02 | La batería completa tarda 1482 s en el PC; el guardia da 600 s por grupo. "3 cortados por tiempo". | `linea_base` + salidas de N20 y V-N27 | **abierto** (P1) |
| S03 | El guardia frenó trabajos APROBADOS por vigías ya rojas, incluso 4 que estaban en la lista de 37. | `.salida_tarea_V-N27-el_pit_arma_las_dos_vias.txt` | **abierto** (causa `NO SE SABE`) |
| S04 | Un guardado tarda ~10 min (H2: 21:04→21:14). V-R9 se colgó 10 min hasta el Ctrl+C. | marcas de hora de archivos | **abierto** |
| S05 | 6 órdenes `fallida / sabotaje` con el código ya guardado (H2, R27, 197, 199, 193, 175). | lista de 22:03 + `capataz.py:371-376` | **abierto** (P2) |
| S06 | 14 de 24 fallidas son `no_aprobo`. Razones vistas: nombre inventado; material sin el tramo; arreglo inerte; DUDOSO sin razón visible. | salidas de V-N20-registro, R9 | **abierto** (P3) |
| S07 | Los cerebros gratis no caben: Groq aguanta 19.042 letras y los pedidos eran 28.942–41.534. Gemini y Groq "se agotó"; DeepSeek "tardó demasiado". | salidas de tareas | **abierto** |
| S08 | `NO_ENCONTRADO: ningún cerebro pudo atender` en 4 de los 15 últimos trabajos. | lista de trabajos 22:03 | **abierto** |
| S09 | La vigía `VIGIA-DOS-VIAS-1` falló porque `ingeniero.py` no existía en la carpeta temporal que armó la prueba. | `.salida_tarea_VIGIA-DOS-VIAS-1.txt` | **abierto** |
| S10 | Una orden fallida no vuelve sola; las que dependen de ella esperan para siempre. | `capataz.py:974`, `listas_para_correr` | **abierto** (P5) |
| S11 | `H2` quedó con el código en disco pero la orden `fallida`. | salida 21:14 vs lista 21:18 | **abierto** (P2) |
| S12 | El forense casi no produce órdenes (9 de 93). Claude está apagado como perito esta noche. | inventario del 1-oct | **abierto** |
| S13 | Las vigías tocan el estado real (BIGPICKLE.log, INDICE_METODO.json). | inventario del 1-oct | N20 (en curso, no cerró) |
| S14 | Líneas peligrosas en el PowerShell: pegado multilínea con `>>` y cascada de errores. | pantalla de Julio | evitado con archivos por git |

## C. Daños colaterales (todos reversibles, ninguno borra trabajo)
| # | Daño | Dónde | Cómo se revierte |
|---|---|---|---|
| D01 | 43 documentos de plan movidos a `memoria/planes_anulados/2026-10-01/`; salen como ` D` en el `git status`. | PC de Julio | copias en esa carpeta |
| D02 | La lista de 37 rojas conocidas esconde rojas reales. | `memoria/.rojas_conocidas.json` (si se aplicó) | borrar el archivo / volver a medir |
| D03 | 3 órdenes quedaron en `corriendo` y `arnes/dos_vias.py` en el índice tras el Ctrl+C. | PC de Julio | `director.reintentar` y `git restore --staged` |
| D04 | Apuntes automáticos de `memoria/` sin subir al repo. | repo (nube) | commit cuando se desbloquee la sesión |

## D. Lo que NO se sabe todavía
Razón de cada `sabotaje`; archivo que fuerza `TODAS`; si la lista de rojas se lee; tiempo por vigía en el PC; razón de los `DUDOSO`; costo en dinero de la noche.
