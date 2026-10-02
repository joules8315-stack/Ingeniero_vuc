# ESTUDIO FORENSE — por qué los pasos no abren otros pasos
Pedido por Julio el 2026-10-02 (noche del 1 al 2 de octubre en su PC). Hecho leyendo el código del repositorio y los datos que
subió su PC. **Cada dato lleva su marca:** `MEDIDO` (salió de un archivo o de la pantalla de Julio), `DEDUCIDO` (sale del código, no se
probó corriendo) o `NO SE SABE`. Lo que no tiene marca no se escribió.
Los errores de la noche, uno por uno, están en `ESTUDIO_FORENSE/ERRORES_DE_LA_NOCHE_2026-10-02.md`.

## 0. Veredicto en 8 líneas
1. En 2 h 29 min (19:34 → 22:03) las órdenes hechas pasaron de **164 a 167** y las fallidas de 17 a 24. `MEDIDO`
2. Un paso abre el siguiente **solo cuando su orden queda "hecha"**, y "hecha" exige que el trabajo se **guarde** y pase el **sabotaje**. `MEDIDO` en el código (§2).
3. El **guardado** es la puerta de salida de todos los pasos. Es el eslabón más débil: 10 minutos por guardado, corre las 314 vigías cada vez, y frenó 3 trabajos aprobados esta noche. `MEDIDO`
4. El plan que di **puso el arreglo del guardado en el paso 1, detrás de 8 pasos que lo necesitan**, y el arreglo de la puerta (G1) lo puse **detrás de la propia puerta**. Error de diseño mío. `MEDIDO` (§3)
5. El plan **no encadena los pasos entre sí**: casi todas las órdenes tienen `depende = []`. El orden es solo prioridad. `MEDIDO`
6. 6 de las 24 fallidas son `sabotaje`: el trabajo **ya estaba guardado** y la orden igual quedó fallida. Eso también frena a los que dependen de ella. `MEDIDO`
7. De los 15 últimos trabajos del equipo: 6 aprobados, 4 dudosos, 1 rechazado, 4 sin veredicto. `MEDIDO`
8. Nada de esto se arregla con un parche más: hay que arreglar la **cadena completa escribir → aprobar → guardar → sabotaje → hecha** en ese orden (§7).

## 1. Línea de tiempo medida (hora del PC de Julio, 1 de octubre)
| Hora | Hechas | Fallidas | Pendientes | Corriendo | Fuente |
|---|---|---|---|---|---|
| 19:34 | 164 | 17 | 193 | 1 | pantalla de Julio |
| 19:57 | 164 | 18 | 192 | 1 | pantalla de Julio |
| 20:37 | 164 | 15 | 194 | 0 | rama `claude/estado-del-bucle` |
| 21:18 | 165 | 21 | 186 | 1 | `DATOS_PARA_CLAUDE.json` |
| 22:03 | 167 | 24 | 181 | 3 | `DATOS_PARA_CLAUDE.json` |

Sacando las 15 fallidas que ya había a las 20:37: **9 fallidas nuevas esta noche** (V-G1, V-N20-las_pruebas, N20-las_pruebas, V-N18, N18, H2, R9, N28, V-N27-el_pit). `MEDIDO`
Costo en dinero de la noche: `NO SE SABE` (no se leyó `GASTO.json` del PC).

## 2. Cómo funciona de verdad "un paso abre otro" (código, no memoria)
- `cuerpo/capataz.py:154` `listas_para_correr()`: una orden corre solo si está `pendiente`, su etiqueta es válida, su huella no falló antes, **todas las ids de su `depende` están `hecha`**, y su pieza no está ocupada. `MEDIDO`
- `cuerpo/capataz.py:371-383`: una orden pasa a `hecha` solo si el trabajo se **guardó** (`resultado.guardado`), **pasa el sabotaje** (se deshace el cambio y la vigía tiene que ponerse roja) y la vigía queda verde. Si el sabotaje falla: `fallida / sabotaje`, aunque el código ya esté guardado. `MEDIDO`
- Guardar = `arnes/candado_equipo.py` `guardar_en_la_historia`: `git add` + `git commit`. El commit ejecuta `hooks/pre-commit` → `arnes/guardia_de_guardado.py` (el guardia). Si frena, `volver_atras` aparta el trabajo y la orden queda `fallida / guardia`. `MEDIDO`
- Una orden fallida **no vuelve sola**: `ya_fallo` (`capataz.py:974`) la salta por su huella, y solo `director.reintentar` la devuelve. Si una orden depende de una fallida, **espera para siempre**. `MEDIDO`

Cadena real de cada paso: **escribir → aprobar → guardar (guardia) → sabotaje → hecha → se abre el siguiente.**
Medida de cada eslabón esta noche:
| Eslabón | Dato medido |
|---|---|
| Escribir | DeepSeek responde en segundos (mediana 5,2 s, medida antes). Sin cuello. |
| Aprobar | 6 de 15 trabajos aprobados (40 %). |
| Guardar | ~10 min por guardado (H2: 21:04 → 21:14; V-R9: 20:24 → colgado hasta el Ctrl+C a las 20:34). 3 aprobados frenados por el guardia (N20 principal, V-N20-las_pruebas, V-N27-el_pit). |
| Sabotaje | 6 órdenes cayeron aquí (H2, R27, 197, 199, 193, 175). |

## 3. El plan que di, contra la realidad
Fuente del plan: `PASOS` en `herramientas_de_julio/crear_las_ordenes.txt:374`. `MEDIDO`
| Paso del plan | Qué pasó |
|---|---|
| 00 N20 (las vigías no tocan la memoria real) | La vigía principal salió APROBADA y el guardia la frenó (`guardia`). `V-N20-el_registro` fue RECHAZADA por inventar nombres: se retiró. Las otras dos, ya corregidas, salieron DUDOSO → `no_aprobo`. **No cerró.** |
| 0 N18 (el bucle no se detiene) | `V-N18` y `N18` → `no_aprobo`. **No cerró.** |
| 0a H2 (el pasillo usa el cerebro mayor) | Se aprobó y **se guardó** a las 21:14, pero la orden quedó `fallida / sabotaje`. **El único arreglo de código que llegó al disco esta noche.** |
| 0b R9 (crear no es inventar) | La vigía se aprobó (20:24) y se colgó en el guardado 10 min. Luego R9 fue RECHAZADA (21:16): la IA preguntó "¿dónde se imprime el aviso?" y el material no traía ese tramo. **No cerró.** |
| 0c N28/N27 (prueba previa, dos vías) | Varias vigías aprobadas (21:21, 21:33, 21:52); `V-N27-el_pit` frenada por el guardia; `N28-el_bucle` → `no_aprobo`; `N27-las_dos_vias` quedó en proceso de guardado al cortar. **No cerró.** |
| 0d … 13 | No se llegó. |
| **1 R1 "El guardado: lo aprobado llega al disco"** | **Está en el paso 9 de la lista (posición 9), detrás de los 8 anteriores, todos los cuales necesitan guardar.** R1 y su arreglo `R1-F151051` están `fallida / no_aprobo`. |

Hallazgos del plan, medidos:
- **A1.** El paso que abre a todos los demás (que lo aprobado llegue al disco) estaba **detrás** de los que lo necesitan. Contradice mi propia regla "cada paso abre el siguiente".
- **A2.** `PASOS` no define dependencias entre pasos. Las únicas `depende` que genera el programa son: vigía → su reparación, una orden `EXTRA` ("68" depende de "89"), y el arreglo del forense. Todas las demás: `depende = []`. En los 12 siguientes pendientes del 22:03, solo los pares vigía→reparación tienen dependencia. `MEDIDO`
- **A3.** El orden de pasos es **solo prioridad de lista**, no condición. Por eso cuando N20 falló, N18 corrió igual. Evita bloqueos en cascada, pero no destraba nada: ningún paso "abre" a otro.
- **A4.** El plan no tiene ningún paso para **la puerta del guardado** (el guardia). Lo agregué a mano esta noche como `G1`, con la vigía `V-G1`, y salió `DUDOSO` → `no_aprobo`; `G1` no corre mientras `V-G1` no esté hecha. `MEDIDO`
- **A5.** La simulación del plan que mostré ("camino sano, 187 de 187") **supone que toda orden se cierra bien**. No simula el guardia, el sabotaje ni la aprobación. Por eso dijo "sano" y la realidad no lo fue. `MEDIDO`

## 4. Por qué los pasos no abren otros pasos — causas, ordenadas por evidencia
**C1 — El guardia corre toda la batería en cada guardado, y esa batería no cabe en su tope.** `MEDIDO`
- Lo que correría el guardia (`arnes/vecinas.py` desde la carpeta de Julio): `TODAS`, a las 21:18 y a las 22:03.
- La batería completa en el PC de Julio: 1482 s (`linea_base`), contra 134 s en la nube. Con competencia del bucle: `NO SE SABE`.
- El guardia da 600 s por grupo (`bateria_en_paralelo.correr(..., tope=600)`): "3 grupos cortados por tiempo" (19:18), "3 cortados" (19:38), "2 cortados" (21:5x).
- Causa del `TODAS`: `vecinas._archivos_cambiados` lee **todo** `git status` de la carpeta, no solo lo que se guarda; basta un archivo de código sin vigía vecina para que sea `None` = todas (`vecinas.py` líneas 166-180 y 216-248). `DEDUCIDO` — cuál archivo concreto lo dispara: `NO SE SABE` (la lista de archivos sucios llegó cortada a 60).
**C2 — Frena por vigías que ya estaban rojas.** `MEDIDO` el hecho; **la causa NO se sabe.** Frenó por 4 vigías que están en la lista de 37 medida a las 21:06. La regla del guardia dice que una roja de `.rojas_conocidas.json` no frena. Hipótesis sin comprobar: la lista se encogió o el guardia no la lee.
**C3 — El cierre por sabotaje convierte un trabajo ya guardado en orden fallida.** `MEDIDO` (6 de 24). H2 quedó guardado en el disco y fallida. Razón exacta del sabotaje en cada caso: `NO SE SABE`.
**C4 — Calidad del trabajo del equipo.** `MEDIDO` 14 de 24 fallidas son `no_aprobo`. Causas vistas en las salidas: nombres inventados (V-N20-registro), material sin el tramo (R9: "El material no trae ese tramo"), arreglo inerte (R9: contador sin usar), DUDOSO sin razón visible (V-G1, N18, N20-las).
**C5 — Material y cerebros gratis que no caben.** `MEDIDO` Groq: "no le cabe (28942 / 36520 / 41534 letras, aguanta 19042)"; Gemini y Groq "se agotó"; DeepSeek "tardó demasiado"; resultado "NO_ENCONTRADO: ningún cerebro pudo atender" en 4 de los 15 últimos trabajos.
**C6 — Una falla no se repara sola.** `MEDIDO` el código (§2) y el forense: solo 9 de 93 expedientes llegaron a una orden nueva (inventario del 1-oct). Claude está desactivado como perito esta noche a propósito (el "Claude falso").
**C7 — Cortes a mano.** `MEDIDO` Julio pulsó Ctrl+C a las 22:03:44 dentro del guardado de otra orden (`KeyboardInterrupt` en `.salida_tarea_V-N27-el_mando...`): quedaron 3 órdenes en `corriendo` y `arnes/dos_vias.py` en el índice de git (`A `). Si esa entrada del índice es basura o un guardado en curso: `NO SE SABE`.
**C8 — Yo estaba ciego.** `MEDIDO` Hasta crear la rama `claude/estado-del-bucle` (≈20:37) no podía ver nada de su PC. Más tarde, al probar `recoger_todo`, mi sesión quedó **sin poder ejecutar comandos** (bloqueo del control de seguridad; causa exacta `NO SE SABE`), así que desde ahí tampoco pude leer ni probar.

## 5. Qué sirvió, qué se hizo, qué dañó, qué se arregló
**Sirvió (medido):** DeepSeek escribe en segundos; el canal de estado (la nube leyó 2 veces el PC y así salió el `TODAS` y el 25 min); `linea_base_de_rojas` (dio 1482 s y 37 rojas); el generador corrigió N20 y retiró 2 órdenes inventadas; H2 llegó al disco; las vigías de N27/N28 se aprobaron.
**Se hizo:** plan único de 187 órdenes; apartado de 43 documentos de plan; línea base; N20 corregida; reportero de estado; comando de datos; G1/V-G1 agregadas a mano; 37 rojas conocidas puestas (instrucción dada; si se pegó: `NO SE SABE`).
**Dañó (medido):**
1. Mi comando de prueba falló a medias y **reescribió** `memoria/ORDENES.json` del repo (se restauró con `git checkout`).
2. Corrí las vigías sobre el repo real: vació `memoria/INDICE_METODO.json`; lo subí por error; se revirtió.
3. Mover 43 documentos a `memoria/planes_anulados/` dejó ` D` en el `git status` del PC: ensucia la lectura del guardia. Reversible (hay copias).
4. La lista de 37 rojas conocidas **enmascara** rojas reales (decisión mía, sin tu autorización explícita para ese riesgo).
5. El Ctrl+C a mitad de guardado (C7).
6. Tiempo: 3 órdenes hechas en 2 h 29 min.
**Se arregló de verdad (medido):** N20 sin invento; las 2 órdenes inventadas retiradas; H2 en el disco; la nube ve el PC. **Nada más está arreglado.**

## 6. Lo que NO se sabe (y se mide antes de tocar)
1. Por qué falló el sabotaje en cada una de las 6 órdenes (la razón está en cada `.salida_tarea_*.txt`).
2. Qué archivo sucio fuerza `TODAS` en el guardia.
3. Si la lista de rojas conocidas se leyó o se encogió (la prueba de 2 segundos con `rojas_que_frenan` sigue sin ejecutarse).
4. Cuánto tarda cada vigía en el PC (comando `recoger_todo` escrito, **sin probar y sin subir**).
5. Por qué V-G1, N18 y N20-las salieron `DUDOSO` (razón del revisor).
6. Costo en dinero de la noche.

## 7. Plan nuevo que sale de este estudio (cada paso con evidencia, medida y criterio de parada)
Principio: **se repara en el orden de la cadena real** (escribir → aprobar → guardar → sabotaje → hecha), del último eslabón roto hacia atrás, no por tema.
| # | Qué | Evidencia | Medida de éxito | Se corta si |
|---|---|---|---|---|
| P0 | **Medir sin adivinar** los 6 desconocidos de §6 con UN comando que sube un JSON (`recoger_todo`, escrito y sin probar) | §6 | los 6 datos en un archivo | no sube en 1 intento |
| P1 | **La puerta**: el guardia corre solo lo que se guarda (G1) y el tope sale de lo medido; la lista de rojas se verifica | C1, C2 | guardado < 3 min; el guardia no dice `TODAS` | sigue ≥ 10 min tras G1 |
| P2 | **El cierre**: decidir qué pasa si el código ya está guardado y el sabotaje falla (¿hecha con aviso o fallida?) y reparar las 6 | C3 | 0 órdenes `sabotaje` con código ya guardado | — |
| P3 | **El material**: todo encargo nombra su archivo y su función (DONDE) y trae los nombres reales | C4, C5 | `no_aprobo` por "material" = 0 | — |
| P4 | **El plan encadenado de verdad**: toda orden que guarda código **depende de P1**; el generador lo comprueba por programa; la simulación incluye guardia y sabotaje | A1-A5 | simulación que falla si la puerta está rota | — |
| P5 | **Parada limpia** (sin Ctrl+C a mitad de guardado) y reintento automático tras el arreglo | C6, C7 | 0 órdenes `corriendo` huérfanas | — |
| P6 | **Medir cada hora** por programa: hechas/hora, minutos por guardado, causas de fallo | todo | tasa visible | — |
**Metas propuestas (no medidas, a verificar):** guardado < 3 min; ≥ 10 hechas por hora; 0 `TODAS`; 0 fallos `guardia` por rojas conocidas.
**Criterio de corte:** si en 1 hora tras P1 no se cumplen al menos 2 de las 4 metas, se detiene y se revisa este estudio, no se agrega otro parche.
**Autorización pendiente de Julio:** G1 no puede guardarse por el guardia que repara. Hace falta decidir si se salta el guardia **una sola vez** para ese archivo (opción A) o no (opción B). No se hizo nada de eso.

## 8. Reglas para no repetir
1. No se da un plan por sano si la simulación no incluye guardia y sabotaje.
2. El paso que destraba a los demás va **antes** de los que lo necesitan, y los demás **dependen** de él.
3. Nada se afirma como hecho sin su `MEDIDO`; lo deducido se marca `DEDUCIDO`.
4. No se corre nada contra la carpeta real sin copia; no se dice "ya no frena" antes de ver una corrida.
5. Un solo comando recoge todos los datos; no se pide pegar resultados de a uno.
6. Ctrl+C solo con el bucle entre vueltas.
