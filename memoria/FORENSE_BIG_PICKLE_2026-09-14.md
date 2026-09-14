> Hecho por Big Pickle (opencode) el 2026-09-14 por orden de la direccion (orden_bp_forense). Solo lectura. Copiado tal cual por la direccion para que no se pierda con el clear.

# INFORME FORENSE — C:\Ingeniero_VUC — 2026-09-14

Solo lectura y medición. Nada se tocó (`GUARDADO: SIN CAMBIOS`).

## PARTE 1 — Las 7 causas sospechadas (una por una, con prueba)

| Causa | Veredicto | Prueba |
|---|---|---|
| **C1 candado_memoria** | **CONFIRMADA — el mayor desperdicio** | Frenos medidos: `memoria/CANDADOS_MEDICION.json` → memoria **cazadas=342**. En 2 sesiones se contaron **~1.480 avisos** (`continuacion_2026-09-13.md:48`). Diseño: la 1ª vez frena y exige reenviar la misma acción para que pase (`arnes/candado_memoria.py:184-193`). |
| **C2 candado_legislar** | **CONFIRMADA (a medias)** | Captura como orden todo trozo de ≥20 letras (`candado_legislar.py:118-140,67`). El cierre bloqueó 18 veces (contador mel spring). En una ventana: **161** "órdenes sin legislar" que eran texto del sistema (`continuacion:49`). Registro: 255 órdenes, resueltas todas, pero **137 (69 `ya_existe` + 68 `no_aplica`) eran ruido** re-marcado a mano. Y `LO_QUE_JULIO_YA_DIJO.json` guarda texto del sistema como "lo que Julio dijo" (157 textos, **204 marcas `task-notification`**). |
| **C3 candado_comunicacion** | **CONFIRMADA (a medias)** | Medida: **57 frenos F4** en una ventana (`continuacion:49`); `buzon` cazadas=44 (contador). Hasta 2026-09-12 los recados quedaban pendientes para siempre porque nadie marcaba "respondido" (`candado_comunicacion.py:106-126`) → cierre en bucle. |
| **C4 candado_protocolo** | **CONFIRMADA (a medias)** | **40 frenos por jerga** en la ventana (`continuacion:49`). Reglas en `candado_protocolo.py:45-50,133-140`. Además el registro de "Julio repite" se contamina con texto del sistema (ver C2). |
| **C5 revisor_de_programa** | **A MEDIAS — el más delicado** | Contador: `revisor_de_programa cazadas=0, frenos_falsos=1` (`CANDADOS_MEDICION.json`). En 3 días frenó **34 de 91 rondas (37%)** (`TRABAJOS_DEL_EQUIPO.log`). Historia: 18 de 55 rondas frenadas, 3 motivos en falso ya reparados (`continuacion:50`). Los falsos viejos: pedazo suelto, import de más arriba, crear archivo nuevo (todos reparados: `revisor_de_programa.py:153-206,253-264`). |
| **C6 un solo cambio por ronda** | **CONFIRMADA** | `cuerpo/aplicador.py:151-157`: si el texto a cambiar aparece 2+ veces **rechaza**, y sustituye solo 1. `ingeniero.py:427` aplica una sola propuesta por llamada. **Un arreglo de 4 cambios = 4 rondas pagadas** (`continuacion:75`). |
| **C7 aprobado y no guardado** | **CONFIRMADA (ayer) → CURA EN VIVO** | Pasado: **30 rondas aprobadas, ninguna guardada al aprobarse** (`continuacion:47`; causa en `ingeniero.py:31-35`). 99 frenos del candado commit + **199 mordidas F8** en la ventana (`continuacion:49`). Cura nueva verificada en el código: `candado_equipo.guardar_en_la_historia` + "GUARDADO AL MOMENTO" (`ingeniero.py:433-438`), vigía `test_vigia_lo_aprobado_se_guarda_al_momento.py` (07:13/07:19). |

## PARTE 2 — Leyes que se pisan (cada par: dos citas)

1. **"NUNCA se escribe código sin el equipo… Ni una línea"** (`LEYES_DEL_AYUDANTE.md:39-42`) contra **"Desde el 2026-09-13 puede REPARAR… entregando lo cambiado"** (`LEYES_DEL_AYUDANTE.md:44-47`). Se arreglan por orden expresa, pero un mismo documento se lleva la contra.
2. **"La fotocopia NO se paga: la aplica un PROGRAMA"** (`CONTRATO_LA_FOTOCOPIA_NO_SE_PAGA.md:17-18,27-29`) contra **"el guardia FRENA todo código sin aprobación del equipo de las últimas 24h"** (`CONTRATO_EL_AYUDANTE_DE_LA_CARGA_PESADA.md:171-172`) y la ley 6. Resultado: lo que el programa aplica gratis no trae aprobación del equipo → acaba pagándose de nuevo al equipo (medido: 4 rondas por una copia, `CONTRATO_FOTOCOPIA:67-75`).
3. **"La vigía nace ROJA"** (`CONTRATO_EL_AYUDANTE:71`; método en `continuacion:24`) contra **"Sellar con una vigía roja" PROHIBIDO** (`CLAUDE.md:57`) y **"el guardia no deja guardar con una prueba roja"** (`CONTRATO_EL_AYUDANTE:159-161`). Atasco real: hay vigías **"en el disco SIN GUARDAR a propósito"** (`continuacion:79,84`), cosa que el candado de commit (F8) ataca por ser trabajo sin commitear.
4. **Jerga: "Nada de nombres de archivos"** (`candado_protocolo.py:133-134,159-160`) contra **el pedido que exige "qué archivo"** (`LEYES_DEL_AYUDANTE.md:35-37`) y el método `archivo:renglón` (`CONTRATO_EL_AYUDANTE:90`). Se salva por interlocutor, pero el hook corre también en ventanas de dirección.
5. **Ley 9 "NADA fuera de su carpeta: NI EL CANAL"** (`LEYES_DEL_AYUDANTE.md:68-74`) contra **ley 2 "mandar lo que sea por el canal"** (`LEYES_DEL_AYUDANTE.md:27`) — y el canal vive **dentro** de la carpeta prohibida (`memoria/canal/`). Medida: N1c "terminó sin informe" `(continuacion:31-35)` y 27 cortes por carpeta externa (`continuacion:52`).

## PARTE 3 — Cuellos de botella, últimos 3 días (09-12 · 09-13 · 09-14)

- **Rondas del equipo:** 30 (12) + 47 (13) + 14 (14) = **91 rondas** (`TRABAJOS_DEL_EQUIPO.log`). No hay reloj de inicio/fin por ronda (`NO_ENCONTRADO` para la duración exacta de ronda).
- **Guardados:** **94 corridas** en 3 días (`GUARDIA.log`). Con batería completa: entre **1m52s y 9m39s**, mediana ≈ 3 min. Pérdidas grandes: **3h07m, 3h05m** (guardia colgada, 09-13 04:15/04:17), **1h19m** (FRENADO 22:39), **44m** (08:33), **21m** — suman **≈6h30m de solo esperar pytest** en 3 días. El contrato confirma "12 min por sellado del negocio; más de 2 horas por noche esperando pruebas" (`CONTRATO_EL_AYUDANTE:31-33`).
- **Rondas pagadas dos veces:** el mayor agujero son **34 de 91 rondas rechazadas por el revisor de programa (37%)** → se repiten. Le sigue el **un-cambio-por-ronda** (multiplica cada arreglo por N). Histórico de trabajo pagado y no aplicado: **659 "el archivo no existe en esa ruta" + 341 "texto_viejo no encontrado"** (`APLICACIONES.log`) — hoy casi extinto (09-14: 11 aplicaciones, **0 fallos**).
- **Dónde se pierde el tiempo (orden):** 1) candado_memoria (342 frenos / 1.480 avisos) → 2) batería completa por guardado → 3) 37% de rondas rechazadas → 4) un cambio por ronda → 5) cierres (legislar/jerga/comunicación: 161+40+57) → 6) Big Pickle (27 cortes + 11 del clasificador, `continuacion:52,55`).

## PARTE 4 — Hallazgos nuevos

1. **El canal (única vía de informe del ayudante) está dentro de la carpeta prohibida** → la dirección pierde informes completos y lo descubre después. Explicaría el "estancamiento" más que cualquier candado.
2. **`LO_QUE_JULIO_YA_DIJO.json` guarda texto del sistema como palabras de Julio** (204 marcas `task-notification` en 157 textos): el termómetro de "Julio repite" compara contra ruido y el registro engaña.
3. **El 37% de rechazos del revisor está sin clasificar** (cuántos son falsos hoy): es la fuga de pago más barata de cerrar (medir antes de decidir).
4. Las vigías "a propósito sin guardar" viven en el árbol de trabajo; ya hay excepción en el guardia (`ingeniero.py:154-182`) pero no está legislada como estado formal.

## Reparaciones propuestas (ninguna quita un candado protector)

1. **C6 — la más barata y de mayor ahorro:** que una misma aprobación del equipo pueda aplicar **todos los trozos de un mismo archivo que cubra su veredicto** (pasar `aplicar_cambio` → `aplicar_cambios` sobre la misma llave de 90 min; revisor y 4 ojos intactos). Vigía: una reparación de 3 trozos = 1 ronda.
2. **Revisor (37%):** clasificar con el espía cada freno en falso/real ANTES de decidir; repetir el patrón que ya curó los 3 falsos (`revisor_de_programa.py:153-206`). El freno se queda.
3. **Guardado:** correr la batería **una vez por tanda de cambios**, no por cada cierre; o batería segmentada al arnés tocado. El guardia que no guarda con roja se mantiene.
4. **Registros:** filtrar el texto del sistema **antes** de entrar a `LO_QUE_JULIO_YA_DIJO.json` y a la legislación (mismo criterio ya existente en `candado_legislar.py:83-115`, aplicarlo también al protocolo).
5. **Ley 9/canal:** para las órdenes de medición darle al ayudante una carpeta de trabajo **dentro de su carpeta** (y dejarle ver el canal) — es una ley de cómo pedir, no un aflojo del candado.

---

TAREA: Confirmar/tumbar C1–C7, leyes contradictorias, cuellos de botella y hallazgos nuevos en C:\Ingeniero_VUC (solo lectura y medición).
RESULTADO: C1, C6 y C7 confirmadas (C7 ya con cura en vivo); C2, C3, C4 a medias; C5 en vía de mejora (37% de rechazos sin clasificar). 5 parejas de leyes que se pisan; 91 rondas y 94 guardados en 3 días, el de mayor costo es candado_memoria (342 frenos / ~1.480 avisos). 34 de 91 rondas rechazadas por el programa; guardado típico 2-6 min con 6h30 de esperas grandes.
GUARDADO: SIN CAMBIOS
