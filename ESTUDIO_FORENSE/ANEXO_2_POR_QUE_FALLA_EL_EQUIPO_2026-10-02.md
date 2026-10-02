# ANEXO 2 — Por qué falla el equipo (evidencia leída de la rama `claude/evidencia-20261001_233703`)
Fuente: `EVIDENCIA_20261001_233703/RESULTADOS.json` (E1 a E6, subido por el PC de Julio). Cada orden se clasificó leyendo las líneas de su salida.
`MEDIDO` = está en el archivo. `DEDUCIDO` = lo concluyo yo de lo medido.

## 1. Lista de rojas conocidas (hipótesis anterior: CONFIRMADA)
- `.rojas_conocidas.json` tenía **13** entradas, no 37. De mis 37 solo estaban 10. Las 4 vigías que frenaron a las 22:03 **no estaban**. `MEDIDO`
- Causa `DEDUCIDO` del código (`guardia_de_guardado.py`): con la selección `TODAS`, si el guardia pasa, **reescribe la lista con las rojas que vio**, que eran 13 porque algunos grupos se cortaron. La lista se encoge cada vez que el guardia pasa con la batería completa.
- Con la selección de 61 vigías (sin `TODAS`) esa reescritura es una unión y no encoge. `DEDUCIDO`

## 2. Las 33 fallidas: 15 viejas y 18 de esta noche
De las 18 de esta noche, clasificadas por lo que dice su salida:
| Clase | Cuántas | Órdenes | Evidencia |
|---|---|---|---|
| A. El escritor no recibe el código que necesita | **8** | V-N18, N18, R9, N28-el_bucle, N29, R6a, R6, N20-las_pruebas | "El material no trae ese tramo"; "no tengo el codigo de listas_para_correr"; `NO_ENCONTRADO`; "Necesito el contenido literal de … / el texto completo de CONTRATO_UNA_SOLA_VIA.md" |
| B. Vigías con nombres inventados (la pieza nueva aún no existe y el encargo no fija sus nombres) | **4** | V-N28, V-N17, V-N15, V-N27-el_mando | "INVENTO: centinela SIN_LEER"; "8 nombres de módulo y 6 de función" adivinados; `CANDIDATOS_MODULO_PERITO` |
| C. El revisor pide más de lo que dice el encargo (DUDOSO) | **3** | V-G1, V-N20-las_pruebas, V-L4 | "añade 4 pruebas distintas"; separador POSIX/win32; `gpgsign`; limpieza de `tempfile` |
| D. Fallan **después** de aprobarse | **2** | V-N27-el_pit (guardia), H2 (sabotaje) | `APROBADO` y luego guardia / sabotaje |
| E. Sin revisor disponible | **1** | N27-las_dos_vias | Groq no cabe (22.930 > 19.042) y Gemini "se agotó" → `SIN_AUDITAR` |
**16 de 18 (89 %) fallan antes de aprobarse. Solo 2 después.** `MEDIDO`
Veredictos en las 33 salidas: DUDOSO 9, APROBADO 9, RECHAZADO 8, SIN_AUDITAR 1, sin veredicto 5. Las 9 APROBADAS son las 9 que fallaron después (guardia 3 + sabotaje 6).

## 3. Los cerebros gratis no caben
- Los pedidos miden entre 20.525 y 41.534 letras; Groq aguanta 19.042: "se le salta" en al menos 18 avisos de estas salidas. `MEDIDO`
- Es el mismo material "grande pero sin la pieza": 20-40 mil letras y aun así falta la función que hay que cambiar (A). `DEDUCIDO`: el paquete se arma por palabras del encargo, no por la estructura del código.

## 4. Sabotaje: las 6 órdenes (E4)
- 4 de 6 (H2, 197, 199, 193): el texto a deshacer aparece 1 vez en la pieza y la vigía existe. El sabotaje sí se puede aplicar; **la vigía no se puso roja** (o `sabotaje.py` salió con otro código). Razón exacta: `NO SE SABE` (no queda escrita).
- R27: **la vigía no existe** (`test_vigia_el_aplicador_no_tira_por_la_marca_invisible.py`). 
- 175: de dos textos a deshacer, **uno ya no aparece** en `cerebro/router.py` (0 veces): sabotaje vencido.
- 5 de las 6 son órdenes de septiembre; solo H2 es de esta noche.

## 5. Correcciones que salen de los datos (en orden)
| # | Corrección | Arregla | Cómo se verifica |
|---|---|---|---|
| C1 | Restaurar las 37 rojas (unión) y que el guardia nunca reescriba la lista con una corrida parcial | frenos por rojas conocidas | `deja_guardar: True` en E8 |
| C2 | **Material por función**: un programa extrae el cuerpo exacto de las funciones nombradas en el encargo y sus llamadores; y cuando el escritor pide archivos o funciones (`NECESITO_LEER`, `PREGUNTA_REQUERIDA`), un programa los adjunta y repite una vez antes de contar fallo | clase A (8 de 18) y la clase E (pedidos más chicos caben en Groq) | 0 fallos por "el material no trae" en 10 corridas seguidas |
| C3 | **Nombres decididos por el arquitecto**: cada orden de pieza nueva fija módulo, función, firma y retorno en su encargo | clase B (4 de 18) | 0 rechazos por INVENTO en vigías nuevas |
| C4 | El revisor juzga **solo lo que pide el encargo**; si el veredicto es DUDOSO sin invento ni falta de material, sus líneas vuelven al escritor una vez | clase C (3 de 18) | DUDOSO baja de 9 a ≤ 3 |
| C5 | El sabotaje deja su razón escrita en `nota`; regenerar el sabotaje vencido (175) y escribir la vigía que falta (R27) | clase D (sabotaje) | 0 `sabotaje` sin razón |
**Recomendación medida:** no relanzar el bucle completo hasta C2 y C3. Esta noche hubo 18 fallos nuevos y 3 hechas (≈ 14 % de acierto) y cada fallo gasta pago.
