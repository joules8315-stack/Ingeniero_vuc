# PLAN DE RAÍZ — DMM Y HERRAMIENTA — 2026-09-13

**Estado: APROBADO ENTERO POR JULIO el 2026-09-13** (respuesta a la pregunta de aprobación en la
sesión de Claude: "Apruebo todo"). Antes: "trabaja en loop hasta terminar". Se ejecuta con el ciclo de
`CONTRATO_EL_AYUDANTE_DE_LA_CARGA_PESADA.md`, "EL CICLO DEL PLAN".

**De dónde sale:** diagnósticos del ayudante (tareas A, B, D, G-ING y su plan R1–R7), la prueba
real con Playwright del DMM (18 pasos, S1→S4) y lo que encontró la dirección trabajando.
**Cada punto se comprobó en el código, ejecutándolo o viéndolo en una captura.** Los hallazgos que
resultaron falsos están abajo, con la prueba.

---

## LA PRUEBA REAL (Playwright, navegador de verdad, DMM dado de alta como su propio cliente)

**13 pasos funcionan y 5 se cuelgan.** Funcionan: entrar, perfil del DMM, voz de marca, entorno,
parrilla, programación, web de ventas, precios, contestadora, chat, seguimiento, clientes, agenda.
Se cuelgan (más de 20 s sin cargar): **crear campaña, medir campaña, aprobar campaña, resultados,
buscar competencia.** Son justo las pantallas que llaman a un cerebro o a internet.

*Límite de esta corrida:* se hizo sin llaves de nube (así aíslan las vigías los datos de Julio), así que
prueba que las pantallas y el orden funcionan, **no la calidad de lo que escribe la IA**. Esa va en la
corrida con llaves del paso N6.

---

## A · LO QUE FRENA LA ENTREGA DEL DMM (repara el ayudante; la dirección revisa, prueba y sella)

| # | fallo de raíz | cómo se comprobó | lo que se hace |
|---|---|---|---|
| N1 | **Las pantallas se quedan en blanco hasta 2–5 minutos esperando a un cerebro.** El cerebro de la nube espera hasta 120 s y el del PC hasta 300 s, sin avisar nada en pantalla | prueba real: 5 pasos colgados · `cuerpo/cerebro.py:89` (300 s) y `:149` (120 s) | tope corto de espera en las pantallas y, si no contesta, el aviso honesto de "borrador" que ya usa la parrilla |
| N2 | **Programa publicaciones en una fecha que ya pasó**: aprobada hoy (13), sale con fecha 2026-09-07 | captura de /parrilla y /programacion | la semana de la parrilla empieza desde hoy, nunca atrás |
| N3 | **El mensaje al cliente dormido existe y nadie lo usa** | `cuerpo/seguimiento.py` sin ningún llamador | conectarlo: se redacta → Julio lo ve en /clientes → solo sale con su sí |
| N4 | **Las imágenes no llegan a las publicaciones reales** | `cuerpo/estudio.py` sin ningún llamador | conectar `estudio` a quien crea las publicaciones, con la cuota y la marca de agua de la ley |
| N5 | **No hay forma de mover a un cliente por el embudo** | `crm.mover` (`cuerpo/crm.py:151`) solo lo llaman las vigías | botón en /clientes con el motivo obligatorio |
| N6 | **La prueba real con llaves de verdad** (calidad de la IA), con el almacén aislado para no tocar los datos de Julio | — | después de N1–N5, antes de pedirle a Julio que pruebe |
| N7 | La vigía del chat depende del cerebro del PC (sola falla, en la suite pasa) | informe D del ayudante, coherente con `cerebro.py:89` | que no dependa de un cerebro de verdad |
| N8 | `vigias/correr_todas.py` da verdes falsos | medido: 52 archivos que no ejecuta | retirarlo y corregir los 3 documentos que lo nombran |
| N9 | `.salud_almacen.json` (un latido automático) está guardado en el repositorio | `git status` lo marca en cada vuelta | sacarlo del repositorio (la ley de carpetas prohíbe guardar datos de funcionamiento) |
| N10 | En la prueba real hay datos del DMM **inventados** ("1 año en el mercado") y "1 años" mal escrito en la pantalla | captura de /empresa | la prueba solo usa lo que dicen los documentos; corregir el plural |

## B · LO QUE HACE FALLAR O ENCARECE AL EQUIPO (repara la dirección con el equipo)

| # | fallo de raíz | cómo se comprobó | lo que se hace |
|---|---|---|---|
| H1 | **El comando del equipo aplica aunque el revisor de programa frene**, y el aviso "LLAVE GUARDADA" mira al auditor, no el veredicto final | `ingeniero.py:379-433`; visto hoy: "código roto" y aun así "APLICADO" | usar el veredicto final para aplicar y para el aviso |
| H2 | **El aplicador no crea un archivo nuevo aprobado** si el obrero pone la marca NO_ENCONTRADO | `cuerpo/aplicador.py:45-53`; hoy no se escribió la vigía del guardia ya aprobada | la marca no cuenta como texto |
| H3 | **El auditor aprueba sin correr la vigía que el encargo nombra** | hoy: aprobó una reparación que no reparaba y una vigía con 1 de 6 pruebas | tras aplicar, correr esa vigía; si sigue roja, no está aprobado |
| H4 | **El guardia del guardado no frena el trabajo a solas** y solo recuerda el último veredicto | `arnes/guardia_de_guardado.py:130-148` y `main()` | cuaderno de 24 h y conectar el freno (ya escrito y aprobado ayer) |
| H5 | **El guardia (900 s) y el candado de cierre (300 s) dejan pasar cuando no alcanzan a correr las pruebas**; la suite ya tarda 22 min y hubo guardados de 3 horas | `guardia_de_guardado.py:215-218`, `candado_cierre.py:132,174`, `memoria/GUARDIA.log` | si no se pudo comprobar, se frena; y que las pruebas no corran dos veces a la vez |
| H6 | **El registro apunta como órdenes de Julio los avisos automáticos** y los recados entre IAs | hoy: 40 entradas falsas marcadas a mano | mirar de dónde viene el texto |
| H7 | **El detector de "fotocopias" salta con solo nombrar las palabras**, y el de "humo" frenó una propuesta que añadía 2 pruebas | hoy, dos rondas frenadas sin razón | las marcas cuentan solo al principio del renglón; buscar la causa del humo |
| H8 | **Se pide un revisor y revisa otro sin avisarlo claro** | hoy: pedido DeepSeek, revisó GPT-OSS 20B | decirlo en la salida |
| H9 | El comentario sobre el patrón de correo en `cuerpo/privacidad.py` explica un motivo falso | leído en el archivo | corregirlo para que nadie "arregle" mal |
| H10 | **El reparto de cerebros no sale de la medición**: los gratis fallan mucho (flash-lite 251 de 451, Gemini 3 211 de 323) | `ingeniero.py cuotas` | ordenar a los gratis por lo medido, solo; **el de pago nunca primero** (ley de la IA cara) |
| H11 | **Armar y lanzar las órdenes del ayudante es a mano** (163 en una sesión) | informe C + registros de Claude | un programa que pega sus leyes, revisa la ley 9 y lanza de uno en uno |
| H12 | **La aprobación de Julio no tiene candado** | legislado hoy, sin programar | un comando que solo corre Julio; sin él no se arma una orden de reparación |

## HALLAZGOS QUE RESULTARON FALSOS (no se quita nada del producto; solo no entran al plan)

- **R1/F2 del ayudante** ("el permiso de edición solo guarda un archivo"): ese permiso ya no existe
  desde el 2026-08-26 (`arnes/permiso_editar.py`) y la llave actual ya cubre varios archivos.
- **R3 del ayudante** ("poner a DeepSeek primero"): va contra la ley de que la IA de pago no escribe.
  En su lugar va H10.
- **G-ING #3 y #7**: el ayudante los reformuló mal. El detector de fotocopias sí mira las dos marcas,
  pero **salta por nombrarlas** (H7). Y el "--revisa" no siempre se respeta (H8).
- **G-ING #10** ("privacidad ya curada"): el patrón sí está curado; el comentario no (H9).
- **Informe C, línea final** ("124 soleados... SEA/SAR/SPA"): no tiene sentido; no se usa.
- **"Comparar vigías antes/después es de los ojos de Julio"** (informe C): es una cuenta; va en H11.

## SUBPLAN URGENTE: EL TRABAJO PAGADO NO SE TIRA (Julio: "Repara primero la herramienta que hace desechar trabajo pago")

Investigó el ayudante (tarea P), verificó y corrigió la dirección. Medido: en 7 días, 46 de 96 rondas
aprobadas no llegaron al disco; de 102 aprobadas reales, 40 las revisó el mismo cerebro que las escribió.

**Reparado el 2026-09-13 (commit 76b9327), cada uno con vigía roja primero:** la marca NO_ENCONTRADO
ya no impide crear archivos · añadir al final ya no es "humo" · la marca BOM de `ingeniero.py` ya no
tira todo cambio · cada ronda se archiva con su nombre y `aplicar-guardado` acepta cuál aplicar.

**APROBADO POR JULIO (2026-09-13, "Apruebo A a F"):**
- **A.** Nadie revisa su propio trabajo: sin otro revisor, queda archivado "pendiente de revisión".
- **B.** Tras aplicar se corre la vigía del encargo; si sigue roja, no cuenta como aprobado.
- **C.** No se aplica lo que el revisor de programa frenó; el aviso de llave dice la verdad.
- **D.** Si el trozo de antes no coincide, el trabajo no se tira: se archiva y se pide solo el trozo exacto.
- **E.** Medir cada semana qué cerebro gratis contesta vacío y no darle trabajos grandes.
- **F.** Corregir la vigía del guardia (`test_vigia_el_guardia_se_acuerda_y_frena.py`, rota por NameError).

## ORDEN DE EJECUCIÓN PROPUESTO

**Fase 1 — entregar el DMM (ayudante, una reparación por orden):**
N1 → N2 → **se repite la prueba real: tienen que pasar los 18 pasos** → N3 → N4 → N5 → N10 →
**N6: prueba real con llaves** → la lista de pruebas de Julio, pantalla por pantalla.

**Fase 2 — a la vez, en la herramienta (dirección con el equipo):**
H1 → H2 → H3 (que el equipo deje de aprobar mal y de tirar trabajo pagado) → H12 (candado de la
aprobación) → H4 → H5 → H6, H7, H8, H9 → H10 → H11.

**Fase 3 — limpieza (ayudante):** N7 → N8 → N9.

**Cada paso:** vigía primero y roja · lo escribe uno y lo revisa otro · nace conectado · suite entera
verde · se guarda. **Nada se da por hecho sin verlo en el disco o en la prueba.**
