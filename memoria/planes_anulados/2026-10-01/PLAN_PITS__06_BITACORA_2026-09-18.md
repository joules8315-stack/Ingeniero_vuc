# BITÁCORA — pasos 0 y 1 del plan v4 (2026-09-18). Solo datos; no modifica el plan (A-30).

## Hecho (escribió DeepSeek, revisó otra familia; copias literales con arnes/copista.py)
- Canal NUEVO con Big Pickle: `cuerpo/bigpickle.py` (encargo por entrada estándar; como argumento Windows lo rompe; con -f se cuelga). Costo 0, 7-190 s. `obrero.auditar(..., auditor="bigpickle")` la usa como revisora; si no contesta, SIN_AUDITAR sin relevo. Vigía `test_vigia_bigpickle_enchufe.py` (6, sin red, saboteada: se pone roja).
- Filtro de llaves del enchufe: detecta la FORMA de la llave (sk-/gsk_/AIza + filtro de la casa), no la palabra.
- Canal VIEJO (recados a la ventana de OpenCode) reparado: `canal.py leer --sin-marcar` / `canal.py marcar`; complemento con id `prt_`, messageID real `msg...`, entrega y DESPUÉS marca. Prueba viva: Big Pickle respondió la palabra del recado (GIRASOL). Raíz del "error severo" del 15-sep: OpenCode exige id `prt...` y messageID `msg...` (registro de OpenCode).
- Revisor de programa: ya no lee JavaScript como Python (usa node --check).
- opencode.json: el permiso de editar obrero.py fue RECHAZADO por el revisor y su vigía salía roja → se restauró; la versión rechazada queda en memoria/trabajos_sin_revisar/.

## Datos medidos
- Big Pickle cazó errores graves que Groq/Gemini aprobaron (variable inexistente, llamada antes del material, llaves sk-ant- que escapaban, JS roto por pedazos).
- Groq 120b/Gemini 4 rechazan en falso seguido porque les llega el archivo RECORTADO (dicen que `os`, `sys`, `Path`, `re` "no existen").
- Si Groq 120b no tiene espacio, el motor cae en Groq 20b (eliminado por el forense): falta limpiar el reparto (paso 1).

## Frenos en falso anotados (para el paso 4, reparar candados)
1. revisor_de_programa: "USA SIMULADOR" por la palabra en un comentario ("SIN Mock").
2. revisor_de_programa: exige en el código las palabras de CONTEXTO del encargo.
3. El buscador no entrega archivos de carpetas ocultas (.opencode) → DeepSeek contesta NO_ENCONTRADO.
4. DeepSeek hace 1 de N cambios cuando el encargo trae varios: conviene un cambio por encargo.

## Pendiente de decisión de Julio
- Vigía nueva "Claude audita si las gratis duermen" (exige que Claude REVISE): choca con A-29 (Claude solo arquitecto y perito). Apartada sin borrar en memoria/trabajos_sin_revisar/*.PENDIENTE_JULIO_2026-09-18.

## Paso 1, limpiar el reparto de IA: DETENIDO, consulta a Julio
- Sacar groq20b, gemini (Gemini 1), gemini3 y local de cuotas.ORDEN pone rojos 3 candados de leyes viejas de Julio:
  test_vigia_relevo_cuotas (orden Qwen→Gemini→local; "si se agota la nube queda el local") y
  test_vigia_se_reparte_por_capacidad::test_C. Choque A-9 (eliminar por datos) contra esas leyes. Revertido.
## Paso 0, planes jubilados de DMM: DETENIDO, consulta a Julio
- Jubilados: PENDIENTES.md, PLAN_DE_ATAQUE.md, PLAN_SIGUIENTE_IA.md (este último lo lee el candado
  vigias/test_vigia_plan_completo.py → no se mueve sin reparar el candado).
- DMM prohíbe carpetas no declaradas (sellar.sh) y sellar guarda TODO: hay 4 cambios sin revisar en DMM.

## A-31/A-32/A-33 (decisiones de Julio, 2026-09-18)
- A-31 hecho: cuotas.ORDEN = groq, gemini4, gemini2, deepseek (copista). 3 candados ACTUALIZADOS por el equipo (revisó Big Pickle), no quitados.
- A-32: vigía "Claude audita" descartada → memoria/trabajos_sin_revisar/*.DESCARTADA_A-32. PENDIENTE (tarea del pit): el código de obrero.auditar y 2 vigías guardadas aún hacen revisar a Claude cuando las gratis duermen.
- Freno en falso nº5: revisor_de_programa pide "decirlo por escrito" para un borrado querido, pero no existe forma de decirlo (no lee el encargo). Se esquivó conservando el nombre de la pieza.
- Nota: la vigía de capacidad no distingue gemini4 de gemini2 (misma puerta).

## A-33 hecho (DMM 7f896a7)
- Planes jubilados → PLAN_PITS/reciclado/dmm. Candado test_vigia_plan_completo lee su nueva ruta (DeepSeek + Big Pickle). PROTOCOLO_DEL_CHAT apunta al plan vigente.
- Big Pickle revisó los cambios sin guardar de DMM: RECHAZADOS y archivados en memoria/trabajos_sin_revisar/dmm/ → permisos de escritura de OpenCode; vigía "DMM se construye a sí mismo" (9 de 18 pasos no pueden fallar: devuelven bool y se toma como OK). APROBADO pero no guardado: .github/copilot-instructions.md (DMM prohíbe carpetas no declaradas → decisión de Julio).
- Bomba de calendario reparada: test_vigia_la_cara_de_la_agenda usaba FECHA fija 2026-09-14 (ya pasada) → próximo lunes.

## Hallazgos (datos)
- sellar.sh de DMM imprime "SELLADO" aunque el guardia de git rechace el commit (el commit no ocurre). Freno/aviso falso nº6: anuncia éxito sin guardar.
- El guardia de DMM rechazó con razón un cambio dictado por Claude al copista (sin revisión del equipo). En el Ingeniero, 5 ediciones dictadas al copista entraron sin ese control → Big Pickle las revisó TARDE: APROBADAS (y corrió la batería: 792 verdes).
- Big Pickle, al revisar, EJECUTA comandos en el proyecto (corrió pytest). Para el paso 4: fijar en su configuración que como revisora solo lea y pruebe, nunca escriba.
- La batería completa tarda 3,5-11 min por guardado (plan §5: prueba de pieza y vecinas al guardar).

## A-34/A-35/A-36 (órdenes de Julio, 2026-09-18)
- **A-34 HECHO**: candado_equipo.anotar_huella + ingeniero.py la llama tras aplicar lo APROBADO + guardia exige que el sha256 (sin ) de lo preparado en git coincida con una huella aprobada en 24 h. Vigía test_vigia_el_guardia_se_acuerda_y_frena actualizada (11/11) con SABOTAJE: cambio a mano tras aprobar → no entra. Transición: candado_equipo.py e ingeniero.py (aprobados por Big Pickle antes de existir la huella) recibieron huella SOLO tras comprobar por programa que su contenido = HEAD + el cambio aprobado archivado. Escribió DeepSeek, revisó Big Pickle.
- (lo que sigue es el diagnóstico original)
- A-34, HUECO del guardián (arnes/guardia_de_guardado.py `_cubierto_por_equipo`): da por "revisado" CUALQUIER cambio a un archivo si el equipo aprobó ALGO en ese nombre de archivo en las últimas 24 h. Peor: cada aprobación anota en memoria/.veredictos_recientes.jsonl (lo escribe arnes/candado_equipo.py:138) TODOS los archivos del paquete, no solo el tocado. Por eso entraron las 5 ediciones dictadas al copista.
  CURA a encargar al equipo (DeepSeek escribe, Big Pickle revisa, un cambio por encargo):
  (a) candado_equipo.py: en cada aprobación anotar "huellas": {archivo_tocado: sha256 del contenido tras aplicar, sin \r}, solo del archivo que se tocó;
  (b) guardia: un archivo de código está cubierto SOLO si el sha256 (sin \r) de su versión preparada (`git show :ruta`) coincide con una huella aprobada en 24 h; si no, "escrito a solas";
  (c) vigía con sabotaje: aprobar, luego editar a mano → el guardián frena.
  El Ingeniero ya usa ese mismo guardián (hooks/pre-commit); la cura sirve a los dos proyectos.
- A-35 pendiente: sellar.sh de DMM debe decir SELLADO solo si `git commit` salió bien.
- A-36 pendiente: declarar `.github` en PERMITIDAS de sellar.sh de DMM y devolver la carpeta desde memoria/trabajos_sin_revisar/dmm/github_APROBADO_BP_carpeta_no_declarada/.
- **A-35 HECHO** (DMM d46904c): sellar.sh no dice SELLADO si quedaron cambios preparados (el guardia rechazó). Sabotaje pendiente de repetir: el primer intento lo frenó antes otro candado (cobertura).
- **A-36 HECHO** (DMM 5d0a881): .github permitida en sellar.sh y devuelta a DMM.
- revisor_de_programa: ya no lee con el analizador de Python archivos que no son .py (bash frenaba en falso); _piezas protegido ante arbol=None.
- **A-37 HECHO**: arnes/vecinas.py elige solo las vigías de la pieza tocada y sus vecinas (TODAS si toca infraestructura de pruebas o una pieza sin vecinas; nada si solo documentos; INGENIERO_BATERIA_COMPLETA=1 para el cierre). Lo usan el guardia y sellar.sh. Vigía test_vigia_vecinas 6/6 + sabotaje (5 rojas).
- A-37 medido: guardado del Ingeniero 15 s (antes 3-11 min); sellado de DMM 3-38 s (antes ~20 min: la batería corría DOS veces). Fallo real cazado por el sabotaje: en Windows python deja \r al final de cada renglón y bash lo pegaba a las rutas → sellar.sh ahora pasa la selección por tr -d '\r'.
- **A-35 PROBADO con sabotaje** (DMM): archivo tocado a solas → vecinas verdes → GUARDIA "escrito A SOLAS" → sellar.sh "NO SE SELLO", exit 1. DMM c106e34: .github devuelta.
- RIESGO CONOCIDO del modo selectivo: una rotura en una pieza que ninguna vigía vecina mira se ve recién al CIERRE. Cierre = correr con INGENIERO_BATERIA_COMPLETA=1.
- SIGUIENTE: paso 2 del plan v4 (inventario "cuenta o juicio").

## Paso 1 terminado: el RELOJ (2026-09-18, noche)
- cuaderno.apuntar acepta segundos (cbfcade); el relevo mide cada llamada (obrero); Big Pickle también anota en el cuaderno común con sus segundos (bigpickle._anotar). Vigía test_el_reloj_anota_los_segundos (1356be5) + SABOTAJE: sin la línea del reloj → roja.
- FALLO REAL cazado al guardar: el guardia corría las vigías heredando GIT_INDEX_FILE del commit; con `git commit -- rutas` (el guardado automático del equipo) una vigía que crea un repo de prueba y hace `git add -A` PISABA el índice del commit → el guardia veía otro contenido y frenaba como "escrito a solas" lo aprobado (y podía colar archivos ajenos). Cura del equipo (ac9ad56): pytest corre sin las variables GIT_*. Vigía test_las_vigias_no_heredan_el_indice_del_commit (776bbb3) + SABOTAJE: con el entorno heredado → roja.
- Frenos/fallos vistos: DeepSeek hace 1 de 2 cambios (nº4, otra vez); el buscador no entrega archivos NUEVOS (cuerpo/bigpickle.py) → hay que pegar el código (nº3); DeepSeek pegó una prueba en medio de otra función porque no vio el final del archivo y Big Pickle lo aprobó → el guardia lo frenó (vigías rojas) y se deshizo a mano: el pit debe VOLVER ATRÁS solo (plan §5). Big Pickle dudó con razón 2 veces por falta de material (import faltante; código del guardia no incluido).

## Paso 2 (2026-09-19, madrugada)
- Inventario: PLAN_PITS/07_INVENTARIO_CUENTA_O_JUICIO.md. Big Pickle lo RECHAZÓ con 3 errores y 3 faltantes, todos con cita del código → corregido.
- Hechos: P2-1 (volver atrás solo), P2-3, P2-4, A-32 en código. Detalle en el inventario.
- Método nuevo que salió de P2-1: cuando un cambio de código y su vigía solo pueden entrar juntos, se aprueban por separado (quedan apartados con su huella), se devuelven los dos y se guardan en un commit; el guardia comprueba que sean exactamente lo aprobado.
- Error del arquitecto (Claude): el encargo afirmó que bigpickle estaba importado en obrero.py y no lo estaba; DeepSeek y Big Pickle lo creyeron. Lo cazaron las vigías antes de guardar. Lección: el encargo no afirma lo que no se comprobó.
- Frenos en falso de esta noche: nº2 (palabras del encargo) 7 veces; nº4 (1 de 2 cambios) 2 veces; nº5 (renombrar = "desaparece") 1; NUEVO nº7: un arreglo que solo toca un comentario se rechaza como HUMO (quedó un comentario viejo en cerebro/router.py: "respetando el tope TOPE_FUNCION_ENTERA").

## Paso 3 (2026-09-19, mañana): P3-1..P3-6 hechos
Todo escrito por DeepSeek y revisado por Big Pickle; cada regla con vigía y SABOTAJE (roja al romperla, verde al devolverla).
- P3-1 `capataz.marcar_estado` reparada (vigía test_vigia_el_capataz_marca_estado). Queda una copia muerta tras el último return de comprobar_pasos (inofensiva: nunca corre); 4 intentos de borrarla chocaron con frenos → paso 4.
- P3-2 etiqueta: `CAMPOS_ETIQUETA`, `validar_etiqueta`; `siguiente_pendiente` salta lo que no tiene etiqueta (test_vigia_sin_etiqueta_no_se_corre, 3 sabotajes).
- P3-3 huella que ya falló: `huella_de`, `anotar_huella_fallida`, `ya_fallo` → memoria/HUELLAS_QUE_FALLARON.jsonl (test_vigia_huella_que_ya_fallo).
- P3-4 despachador: `listas_para_correr` (pendiente + etiqueta + no fallada + dependencias hechas + una por pieza) (test_vigia_el_despachador, 5 sabotajes).
- P3-5 `lanzar_al_equipo(proyecto, orden, tope_segundos)` con deepseek/bigpickle, --crear, tope de tiempo, GUARDADO leído del texto (el comando equipo sale con 0 aunque no apruebe, ingeniero.py:451) (test_vigia_el_capataz_lanza_al_equipo).
- P3-6 fila de commits: `candado_equipo.fila_de_commits` (candado en la carpeta temporal, uno por proyecto, abandonado a las 2 h) y `guardar_en_la_historia` guarda dentro de la fila (test_vigia_fila_de_commits, 3 sabotajes).
- FALLO REAL 1 (mío, cazado por las vigías): volver_atras (P2-1) apuntaba el fallo SIN disparador → test_ningun_fallo_es_MUDO roja. Cura del equipo: disparador `ingeniero\.py\s+equipo`.
- FALLO REAL 2 (grave): un encargo mío dejó arnes/candado_equipo.py sin cargar (decorador con contextlib importado dentro de la función) y el GUARDIA LO DEJÓ GUARDAR. Causa: una vigía que no carga sale como 'ERROR vigias/x.py - NameError...', el guardia tomaba todo eso como nombre de archivo, git no lo conocía → "vigía nueva sin su pieza, se deja pasar". Se deshizo con git revert (a840d4e). Cura del equipo (f492764): cortar por ' - '. Vigía test_vigia_una_vigia_vieja_que_no_carga_frena + sabotaje.
- Big Pickle aprobó 2 veces algo incorrecto (dijo que se había borrado la copia muerta y no; aprobó un texto viejo que no existía literal). El programa lo frenó las dos.
- Frenos en falso nuevos: nº8 un encargo que solo BORRA se rechaza ("no trae texto nuevo"); nº9 nombrar las palabras "texto viejo"/"texto nuevo" en el encargo lo convierte en fotocopia. nº2 otra vez 2 veces; nº4 otra vez 2 veces (imports olvidados).
- Errores del arquitecto (Claude): 2 encargos con datos sin comprobar (dónde se importa contextlib; que candado_equipo importa subprocess arriba). Lección repetida: comprobar antes de afirmar en el encargo.

## Paso 3 (2026-09-19, mediodía): P3-7..P3-10
- P3-7 etiqueta en el cuaderno: `cuaderno.apuntar` anota `etiqueta` si existe INGENIERO_ETIQUETA; `lanzar_al_equipo` la pone con el id de la orden (test_vigia_la_etiqueta_llega_al_cuaderno, 3 sabotajes).
- P3-8 tope de gasto: DeepSeek no dejaba registro del gasto. Ahora `obrero._deepseek_directo` anota modelo y tokens en memoria/GASTO_USD.jsonl; `capataz.costo_deepseek / gastado_del_mes / se_paso_del_tope` (5 USD, precios de hora PICO copiados de api-docs.deepseek.com el 2026-09-19; modelo desconocido = el caro). Big Pickle suma su costo= de BIGPICKLE.log (hoy 0). Dato real: DeepSeek contesta como "deepseek-flash", ~0,5 centavos por llamada. Lo gastado antes de hoy no quedó registrado. (test_vigia_tope_de_gasto, 7 sabotajes).
- P3-9 el loop: `capataz.tipo_de_fallo` y `capataz.bucle` (paralelo por piezas distintas, en fila la misma pieza, para por tope de gasto / todo hecho o nada que correr / 3 fallos del mismo tipo en una pieza) (test_vigia_el_loop_del_pit, 6 sabotajes; prueba de "a la vez" con barrera y de "en fila" con contador).
- P3-10 forense: `armar_expediente` (memoria/EXPEDIENTES), `citas_que_no_existen` (P2-2, programa), `pedir_al_perito` (Claude con `--tools Read,Grep,Glob --permission-mode plan`: probado en vivo que lee y NO escribe), `juzgar_citas` (Big Pickle), `agregar_orden`, `forense` (cadena completa, libro de fallos con disparador) y `bucle` lo llama tras cada fallo. Vigía de expediente y citas con sabotaje; la del forense completo PENDIENTE: Big Pickle se cayó (OpenCode cuelga o sale con código 1 desde las 10:48).
- Frenos: nº2 dos veces más; Big Pickle timeout en encargos de vigías grandes (300 s) → partir vigías grandes.

## A-38 cerrado (2026-09-19, noche)
- Big Pickle volvió: 16 s en una pregunta corta. Pero en revisiones de trabajo se pasa de los 300 s (tres veces esta noche) y entra el relevo (Groq), que es justo lo que A-38 mandó.
- **E-5** (un cambio que solo borra vale) y **E-7** (texto repetido: se busca dentro de la función que el obrero dice tocar, por nodo de ast) hechos con vigía y sabotaje.
- **E-3b**: `no_carga` conectado en `revisar` como cuenta NO CARGA, antes del corte por "es un pedazo"; solo frena si el archivo cargaba antes. Su vigía volvió de `.ESPERA_SU_PIEZA`.
- **E-4 apartado con la medición en contra**: el freno nº2 ya no dispara en los cambios por trozo y no hubo ni un rechazo suyo en ~120 trabajos del día. Invertir la condición rompe dos vigías legítimas. Quien decide si el cambio hace lo pedido es el juez de la prueba.
- **E-8b**: `arnes/juez_de_la_prueba.py`. Roja antes, verde con el cambio, roja al deshacer; deja el cambio puesto. Tres casos en su vigía, incluido "ya estaba verde" (si no, un cambio inútil cuela). Dos de las tres cuentas se sabotean; la tercera no tiene escenario honrado y así quedó escrito.
- **E-9**: `arnes/medidor_de_rondas.py`, conectado al candado de cierre. **Primera medición: 136 rondas, 103 aprobadas, 81 guardadas = 0,60 por ronda.**
- **Freno en falso nº13, cazado en vivo**: un cambio dentro de un texto entre comillas triples se leía como código ("usa un nombre que no existe", "desaparece lo que ya estaba"). Reparado con su vigía.
- Aislamiento de `test_vigia_vecinas.py` arreglado: ya no sale roja en falso con la batería completa.
- Lo que de verdad pierde rondas, medido: de 11 rechazos, la mitad son "el texto viejo no aparece en el material original" (el obrero adivina más allá del recorte, o el revisor no ve en su material lo que sí está en el archivo). El resto: hace 1 de 2 cosas, e imports olvidados.
