# DONDE VAMOS — 2026-09-13 noche (Julio limpia la conversación)

**Plan que manda:** `PLAN_DE_RAIZ_2026-09-13.md` (APROBADO ENTERO por Julio) + su subplan "EL TRABAJO PAGADO NO SE TIRA" (A–F aprobados).
**Leyes nuevas de hoy:** `CONTRATO_EL_AYUDANTE_DE_LA_CARGA_PESADA.md` (también repara; ciclo del plan; canal cada 5 min una hora;
puerta trasera cerrada con candado de opencode) · `CONTRATO_CREAR_PIEZA_NUEVA.md` regla 7 (código nuevo siempre con plan aprobado por Julio) ·
`memoria/LEYES_DEL_AYUDANTE.md` leyes 9 y 10.

## ORDEN DE JULIO QUE MANDA AHORA
1. **Reparar lo que nos frena, antes que nada** ("hasta que lo que nos frena no se repare, seguimos perdiendo tiempo y dinero").
2. **Después, SOLO DMM** hasta entregarlo, con Big Pickle haciendo los arreglos y la dirección verificando con la prueba real;
   avisar a Julio al terminar cada punto, con la hora. **No dar estimaciones de horas sin descontar lo que se pierde.**
3. **Coordinar con Big Pickle** (Julio lo tiene corriendo en su ventana): que no ensucie el trabajo de la dirección.

## LISTADO MEDIDO DE LO QUE RETRASA (2026-09-14, pedido por Julio; registros del 13-14 sep)
1. Lo aprobado no se guarda al momento: 30 rondas aprobadas, ninguna guardada al aprobarse → REPARANDOSE (guardar_en_la_historia + llamada en equipo y aplicar-guardado).
2. candado_memoria frena la 1a vez casi cada accion ("repite la misma accion"): ~1.480 veces en 2 sesiones → SIGUIENTE a reparar (el mayor desperdicio).
3. Candados de cierre: F8 guardar 199 (bucle YA reparado 0f4db7b) · ordenes sin legislar 161 (captura textos del sistema como ordenes de Julio) · comunicacion F4 57 · jerga 40 → sin reparar.
4. Revisor de programa: 18 de 55 rondas frenadas (3 motivos en falso ya reparados); medir cuantos siguen en falso.
5. Un solo cambio por ronda → sin reparar.
6. Big Pickle: 27 cortes por carpeta externa (resuelto con candados), 9 errores de servidor, 3 cupo.
7. Guardado corre toda la bateria (3-5 min herramienta, ~12 negocio): con tope de 15 min el negocio podria quedar frenado → riesgo abierto.
8. Nadie mide solo las rondas aprobadas que llegan al disco → sin reparar.
9. Clasificador de seguridad de Claude: 11 bloqueos.
Alcance de las 3 IA corregido: SOLO crear codigo nuevo (CONTRATO_CREAR_PIEZA_NUEVA regla 8). Cada freno: frena → causa raiz → que se dano → se repara de una vez.

## ACTUALIZACION 2026-09-14 04:50 (lo hecho en la noche)
- ✅ H4: el guardia se acuerda de TODAS las aprobaciones de 24 h y FRENA el codigo sin equipo (c36b28e, llave de Julio; probado en vivo: 4 archivos con 4 aprobaciones distintas pasaron).
- ✅ Big Pickle obligado: candado global cerrado por defecto (Foto Informe y cualquier carpeta), herramienta cerrada, negocio repara pero no guarda/deshace/borra; ventana de Julio recargada SIN cerrarla (`/global/dispose` + `/instance/dispose`, comprobado con `/config`). Probado en real. Ley en CONTRATO_EL_AYUDANTE (TODAS LAS PUERTAS Y VENTANAS CERRADAS). Vigia 5/5 saboteada. (adb7153, 3bfb09c)
- ✅ El guardia se colgaba (5 h 30 min) y dejaba guardar sin probar: entrada cerrada + si no terminan NO se guarda (3c1a243; guardado real en 2 min 41 s).
- ✅ Revisor de programa frenaba en falso al crear archivos nuevos (3c1a243).
- ✅ via_canonica ya no grita por las notas de los candados (c36b28e).
- ⏳ SIGUE: el candado de cierre sigue viendo como "sin guardar" las notas que los candados escriben solos (bucle al terminar). · El aplicador acepta UN cambio por ronda. · Medicion automatica de rondas aprobadas que llegan al disco. · Recuperar trabajo archivado (`aplicar-guardado`) no deja aprobacion: el guardia no lo deja guardar.
- ⏳ DESPUES: DMM (N1c pantallas colgadas: medir donde esperan; N2 fechas pasadas; N3–N6).

## LO QUE NOS FRENA (estado)
- ✅ Marca NO_ENCONTRADO no dejaba crear archivos · ✅ "añadir al final" tomado por humo · ✅ marca BOM de ingeniero.py tiraba todo cambio
- ✅ Trabajo aprobado pisado → se archiva en `memoria/trabajos_del_equipo/` y `aplicar-guardado <proy> <ruta>` lo recupera
- ✅ Autorrevisión (40 de 102 aprobadas) · ✅ se aplicaba lo que el revisor de programa frenaba
- ✅ Revisor frenaba por palabras de contexto · ✅ revisor acusaba de "no existe" nombres importados más arriba (11/11)
- ✅ Puerta trasera de opencode: `opencode.json` en herramienta, negocio y global, probado. **Julio debe cerrar y reabrir su ventana de Big Pickle.**
- ⏳ `guardar_trabajo_pagado` está definida DOS veces en `arnes/candado_equipo.py` (renglones 260 y 296): dejar una sola, con el equipo.
- ⏳ Falta la prueba del CAMINO COMPLETO de crear código (el equipo crea una pieza nueva y queda en el disco), en carpeta temporal de la prueba, NUNCA una pieza de juguete dentro de `cuerpo/`.
- ⏳ **El aplicador solo acepta UN cambio por ronda** (un arreglo de 4 cambios = 4 rondas pagadas). SIGUIENTE a reparar.
- ⏳ Los cerebros gratis contestan vacío: escribir con `--escribe deepseek --revisa gemini4`.
- ⏳ Medir siempre cuántas rondas aprobadas llegan al disco y que muerda (punto E). Hoy desde las curas: 14 de 17.
- ⏳ H4: memoria de veredictos 24 h — el cuaderno YA se escribe; faltan LEER el cuaderno en `_cubierto_por_equipo` y CONECTAR el freno en `main()`.
  Su vigía `vigias/test_vigia_el_guardia_se_acuerda_y_frena.py` está en el disco SIN GUARDAR a propósito (3 rojas reales: guardarla bloquearía todo).
- ⏳ El guardia (900 s) y el candado de cierre (300 s) dejan pasar cuando no alcanzan a probar (H5).
- ⏳ Candado del consentimiento de Julio con firma y frase secreta: **PROPUESTO, NO APROBADO, NO construir** sin su sí.

## DMM (negocio)
- Prueba real con navegador: `vigias/test_vigia_dmm_se_construye_a_si_mismo.py` (en el disco SIN GUARDAR a propósito: 5 pantallas rojas).
  13 funcionan; se cuelgan crear/medir/aprobar campaña, resultados, competencia.
- N1: LM Studio encendido pero el modelo pedido (qwen2.5-coder-3b-instruct) NO está cargado; el pedido espera 300 s.
  Big Pickle hizo N1 (comprueba el puerto) y **N1b (comprobar que el modelo esté cargado): TERMINADO, SIN REVISAR** por la dirección.
- Faltan: N2 fechas pasadas en la parrilla (`web/servidor.py:476`), N3 mensaje al cliente dormido (Big Pickle investiga, solo leer),
  N4 imágenes, N5 botón para mover clientes, N6 prueba con llaves reales, lista de pruebas de Julio.

## LO QUE ESCRIBIÓ BIG PICKLE SIN PERMISO EN LA HERRAMIENTA (15:08)
Ley "atento al canal": contrato, candado, vigía (9/9 con sabotaje), renglones en leyes, matriz y protocolo. Julio pidió guardar TODO:
se guardó en el commit de esta nota. Pendiente: que el equipo lo revise.
