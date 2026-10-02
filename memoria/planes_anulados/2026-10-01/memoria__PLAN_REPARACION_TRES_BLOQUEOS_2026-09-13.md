# PLAN DE REPARACION — LOS 3 BLOQUEOS (2026-09-13)

Remitente: opencode (big-pickle) -> canal a Claude. Diagnostico con paquete minimo
`memoria/paquetes/ingeniero__revisa__1__que_frena_el_trabajo_2__por_q.md` + evidencia viva.

## 1) QUE FRENA EL TRABAJO (medido)

- La ley manda: NO se escribe codigo a solas. Todo .py exige veredicto APROBADO del equipo
  (un cerebro escribe, OTRO distinto audita). Eso es ley 6 de Julio, no un bug.
- Lo que de verdad frena hoy:
  - `opencode.json` cerro la puerta trasera: edit=deny, external_directory=deny, terminal tildada
    (vigia test_vigia_opencode_no_escribe_en_la_herramienta.py, aprobada hoy 16:35). El asistente
    actual NO puede escribir archivos: solo lee, diagnostica y manda por el canal.
  - El cuello es el EQUIPO: depende de cerebros gratis vivos (deepseek/groq/gemini). Cuando se
    caen, o el unico vivo se revisa a si mismo (bloqueo, memoria 2026-08-31), o no hay voto.
  - El revisor de programa rechaza rondas hasta que sale bien (hoy 15:06, 15:08, 15:15
    RECHAZADO_POR_EL_PROGRAMA).
  - Candados del canal: despues de mandar a Claude hay que esperar 1 hora mirando cada 5 min,
    y los recados sin responder frenan el cierre del dia.

## 2) POR QUE NO PERMITE CREAR CODIGO Y REPARO DE RAIZ

- Dos puertas para crear codigo:
  a) El atajo (el asistente escribiendo a mano): CERRADO A PROPOSITO (opencode.json + vigia).
  b) La via legal (`python ingeniero.py equipo <proy> "<tarea .py>" --crear`): EXISTE.
- Causa raiz historica del bloqueo de crear (ya curada HOY, evidencia en APLICACIONES.log):
  - el encargo --crear pedia markdown aunque la tarea fuera .py -> codigo con SyntaxError
    (curado 2026-09-10: prompt especial ANALISTA DE CODIGO en cuerpo/obrero.py);
  - el aplicador no sabia crear archivo nuevo (curado 2026-09-05: cuerpo/aplicador.py crea);
  - trabajar no respetaba generador/auditor (curado: vigia test_vigia_trabajar_respeta_generador_auditor.py VERDE hoy).
- REPARO DE RAIZ:
  1) NO abrir la puerta trasera. Se mantiene edit=deny en opencode.json.
  2) Probar de verdad la via legal (ley 7): crear una pieza nueva de juguete con el equipo
     (`--crear --escribe deepseek --revisa groq`), comprobar que nace el archivo en disco,
     y dejar una vigia/PRUEBA REAL que lo demuestre. Si se prueba, "crear codigo" deja de ser
     un bloqueo y pasa a ser un derecho con plan aprobado (ley de 2026-09-08: regla 7).
  3) Si la prueba falla, responder las 5 preguntas (que/donde/por que/cuando/como) y reparar
     la causa, con la ronda archivada, sin excusas.

## 3) QUE NO PERMITE GUARDAR EL TRABAJO Y COMO SE PIERDE (causa raiz + reparo)

- HOY el trabajo YA se guarda en disco (memoria/trabajos_del_equipo/ + ULTIMO_TRABAJO, 26
  archivos de hoy, APLICACIONES.log todo OK). Se curo con: guardar ANTES de mostrar
  (ingeniero.py:358), guardar_trabajo_pagado que archiva cada ronda (antes se pisaba un unico
  archivo y el 2026-09-12 se perdieron 24 h de veredictos), freno al auto-auditado
  (40 de 102 rondas aprobadas se perdian), y el arreglo del BOM.
- CAUSA RAIZ VIVA (por que HOY se puede seguir perdiendo):
  1) NADA esta en git: git status muestra decenas de archivos sin commit. El respaldo depende
     de un commit que aun no se hizo.
  2) El guardia frena el commit si hay vigia ROJA o una llave (hoy 13:40 freno por 13 vigias
     rojas). Correcto, pero deja el trabajo sin respaldo mientras haya rojas.
  3) Los cuadernos que prueban el trabajo pagado (.veredicto_equipo.json, ULTIMO_TRABAJO,
     .veredictos_recientes, SIN_EQUIPO, DECISIONES_CANDADO, GUARDIA) estan en .gitignore:
     el rastro de lo aprobado NO viaja con el repo; si se borra la carpeta, se pierde la prueba
     de que se pago y aprobo.
  4) guardar_trabajo_pagado esta definido DOS VECES (arnes/candado_equipo.py:260 y 296):
     copia duplicada, hay que consolidar en una sola.
  5) recados firmados 'desconocido' (INGENIERO_QUIEN sin poner en alguna sesion): un recado sin
     firma no se cierra nunca.

## PLAN EN FASES (para el equipo)

FASE 1 - PROBAR LA VIA LEGAL DE CREAR CODIGO (ley 7):
  - Correr `python -m pytest -q vigias/test_vigia_trabajar_respeta_generador_auditor.py`
    (verde). Despues, encargo al equipo:
    `python ingeniero.py equipo ingeniero "crear cuerpo/_demo_2026.py: una funcion pieza_demo
     que devuelva 1" --crear --escribe deepseek --revisa groq`
  - Verificar que el archivo nace en disco y que `python -c "from cuerpo import _demo_2026"` importa.
  - Dejar vigia nueva (nace antes que la pieza) que pruebe el flujo crear completo.

FASE 2 - GUARDAR DE VERDAD (que no se pierda):
  - Correr la suite completa de vigias; cuando este toda verde, comitear HOY.
  - Preguntar a Julio (PREGUNTA_REQUERIDA): el rastro pagado (.veredictos_recientes,
    ULTIMO_TRABAJO, .veredicto_equipo) debe viajar con el repo, o replicarse a un respaldo que
    si viaje (memoria/rescate/ o respaldo diario). Sin esa decision, el trabajo queda solo en disco.
  - Consolidar la funcion duplicada guardar_trabajo_pagado (una sola, misma vigia).

FASE 3 - DESATASCAR EL EQUIPO:
  - Que el mando `equipo` SIEMPRE pida dos cerebros DISTINTOS (--escribe/--revisa); si el unico
    vivo queda solo, PARAR, avisar por el canal y dejar la ronda archivada, nunca descartada.

FASE 4 - CIERRE DEL DIA:
  - Responder los recados pendientes por el canal, poner INGENIERO_QUIEN en toda sesion,
    actualizar memoria/ESTADO.json.

PREGUNTAS_REQUERIDAS para Julio:
  1) El rastro del trabajo pagado, se sube al repo o se respalda aparte?
  2) La pieza de juguete de prueba (cuerpo/_demo_2026.py) se borra o se queda como ejemplo?
  3) Se autoriza el commit de hoy cuando las vigias esten verdes?