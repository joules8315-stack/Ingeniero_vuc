# Paso 2 del plan v4 — Inventario "¿cuenta o juicio?" de cada paso del pit
> Ley: CONTRATO_CUENTA_O_JUICIO.md. **CUENTA** = con reglas fijas sale siempre lo mismo → programa, gratis.
> **JUICIO** = hay que decidir algo que no está escrito → IA. Regla 0: una pieza que existe y nadie llama cuenta como NO HECHA.
> Hecho por Claude (arquitecto, A-29) el 2026-09-18 leyendo el código; lo revisa Big Pickle.

## A. Los puestos del pit (plan v4 §3)
| Puesto | Paso | Qué es | Hoy lo hace | Estado |
|---|---|---|---|---|
| 0 Portero | carpeta y rama canónicas, nada sin guardar | CUENTA | `arnes/via_canonica.py`, `arnes/portero.py` (lo llama `equipo`) | ✅ |
| A Recepción | guardar la instrucción textual + commit | CUENTA | `memoria/LO_QUE_JULIO_YA_DIJO.json` (candados); commit a mano | ⚠ sin commit automático → paso 3 |
| B Alma | ficha, matriz, tabla de verdad | JUICIO | Claude arquitecto, una vez (A-29) | ✅ correcto |
| C Planificador | partir la ficha en tareas con el mapa de flujos | CUENTA (el reparto) | el libro del reparto existe (`arnes/reparto.py`, estados y dueño, lo usa el portero) y el mapa también (`cerebro/flujos.py`); falta el programa que PARTE la ficha | ❌ paso 3 |
| C Planificador | etiqueta PROGRAMA o IA de cada tarea | CUENTA si el cambio ya viene decidido (fotocopia: `candado_terminal.es_una_fotocopia`); JUICIO si no | la fotocopia sí; el resto no existe | ❌ paso 3 |
| D Despachador | archivos distintos en paralelo, mismo archivo en fila | CUENTA | `cuerpo/subagentes.py` (paralelo), sin fila por archivo | ⚠ paso 3 |
| D Despachador | elegir la IA antes, según datos | CUENTA | `cuotas.fila/rankear` + orden A-31 | ✅ |
| E Pit | escribir el cambio cuando hay que decidir CÓMO | JUICIO | DeepSeek | ✅ |
| E Pit | escribir cuando el cambio ya está decidido | CUENTA | `arnes/copista.py` (técnicamente sirve para cualquier archivo; por política, Claude solo le dicta docs: dictarle código sería que Claude escriba código) + ley de la fotocopia en `equipo` | ✅ |
| E Pit | revisar si el cambio es correcto y no rompe vecinos | JUICIO | Big Pickle (A-32) | ✅ (queda el respaldo a Claude en `obrero.auditar` → A-32 en código) |
| E Pit | revisión de forma (nombres que no existen, texto viejo literal, inventos) | CUENTA | `arnes/revisor_de_programa.py`, `obrero._validar_en_paquete` | ✅ |
| E Pit | montar el cambio en disco | CUENTA | `cuerpo/aplicador.py` | ✅ |
| E Pit | probar pieza y vecinas | CUENTA | `arnes/vecinas.py` + guardia (A-37) | ✅ |
| E Pit | **si la prueba falla, volver atrás** (plan §5) | CUENTA | **nadie**: el cambio roto queda en disco y preparado; hoy lo deshace Claude a mano | ❌ **P2-1** |
| E Pit | vigía "nace conectado" | CUENTA | no existe | ❌ paso 3 |
| E Pit | fila de commits | CUENTA | `candado_equipo.guardar_en_la_historia` (uno por tarea) | ⚠ sin fila entre tareas paralelas → paso 3 |
| F Forense | expediente del fallo | CUENTA | no existe | ❌ paso 3 |
| F Forense | análisis de la causa, con citas | JUICIO | (Claude perito, A-29) | paso 3 |
| F Forense | **comprobar que cada cita existe literal** en el archivo | CUENTA | el plan se lo da a Big Pickle | ❌ **P2-2**: primero programa (cita literal sí/no), después Big Pickle juzga si la cita prueba la causa |
| F Forense | volver atrás, libro de fallos, tarea nueva | CUENTA | `cuerpo/fallos.py` apunta; lo demás no existe | ❌ paso 3 |
| G Cierre | batería completa + commit + informe | CUENTA | `INGENIERO_BATERIA_COMPLETA=1` + guardia | ✅ (informe → paso 7) |
| Bibliotecario | buscar nombre → función → significado | CUENTA | `cerebro/router.py`, `cerebro/piezas.py` | ⚠ **P2-3** (corregido por Big Pickle): el grafo sí indexa archivos nuevos y carpetas ocultas salvo las excluidas (`cerebro/grafo.py`, `cerebro/piezas.py`); lo que falla es que el router **no elige** el archivo que el encargo nombra (medido hoy: `cuerpo/bigpickle.py` nombrado en el encargo → NO_ENCONTRADO). Hoy Claude pega el código a mano |
| Bibliotecario | entregar la función ENTERA que se toca, también al revisor | CUENTA | `obrero._filtrar_paquete` recorta | ⚠ **P2-4** (corregido por Big Pickle): el router entrega funciones ENTERAS hasta 120 líneas (`cerebro/router.py::completar_funciones`); las más largas llegan en pedazos (medido hoy: `obrero._preguntar_con_relevo` ≈220 líneas → NO_ENCONTRADO). Y al revisor no le llega el código de la pieza que la tarea NOMBRA si no es la tocada (dudas de Big Pickle hoy) |
| Bibliotecario | buscar por significado (`cerebro/semantico.py`, embedding de Gemini por consulta) | CUENTA con ayuda de un modelo de embedding (no escribe ni juzga) | `cerebro/router.py` | ✅ (ojo: Gemini gratis lee lo que se manda → solo nombres/código, nunca llaves ni clientes) |
| Bibliotecario | mapa de flujos | CUENTA | `cerebro/flujos.py` (lo usa el grafo y el router) | ✅ |
| Registro | tiempo y etiqueta de cada llamada | CUENTA | `cuerpo/cuaderno.py` (reloj hecho hoy); etiqueta de tarea no existe | ⚠ etiqueta → paso 3 |

## B. Otras llamadas a IA del Ingeniero (fuera del pit)
| Pieza | Qué pide a la IA | Qué es | Veredicto |
|---|---|---|---|
| `cuerpo/cruzado.py` vigilante | escribir la prueba a ciegas | JUICIO | queda |
| `cuerpo/cruzado.py` juez, código 1 "inventa" | ¿usa algo que no está en el material? | CUENTA | ya lo cubre `_validar_en_paquete` / revisor_de_programa si se le pasa → **P2-5** |
| `cuerpo/cruzado.py` juez, código 2 "no pasa la prueba" | ¿la reparación pasaría la prueba? | **CUENTA: se corre la prueba** | ❌ **P2-5**: hoy lo adivina una IA; debe correrse la prueba en una copia |
| `cuerpo/cruzado.py` juez, códigos 3-5 | atajo, rompe vecino, tapa síntoma | JUICIO | queda |
| `cuerpo/dudas.py::_responde_de_verdad` | ¿este texto responde la duda? | JUICIO | queda |
| `cuerpo/consejeros.py` | consejo | JUICIO | queda |
| `cuerpo/skills.py::crear` | escribir una habilidad | JUICIO | queda |
| `arnes/medir_capacidad.py`, `medir_precision.py` | usan el cerebro local (eliminado por el forense) | — | no se usan en el pit; se dejan |

## C. Lo que el paso 2 convierte a programa (una tarea por encargo, DeepSeek escribe, Big Pickle revisa, con vigía y sabotaje)
- **P2-1** Volver atrás solo: si el guardia no deja guardar lo aplicado, `equipo` devuelve el archivo a su versión guardada y lo anota en el libro de fallos.
- **P2-3** Bibliotecario: si el encargo NOMBRA un archivo que existe en el proyecto y el router no lo eligió, el programa lo agrega por ruta al material (Regla 4: dos caminos).
- **P2-4** Funciones de más de 120 líneas: al obrero y al revisor les llega la función nombrada entera (o el tramo pedido), no un pedazo.
- **P2-5** Juez de cruzado: el código 2 lo decide la prueba corrida, no la IA.
- **P2-2** Citas del forense: nace con el forense en el paso 3 (no existe aún); queda escrito aquí para que nazca como programa.

## Revisión de Big Pickle (2026-09-18)
RECHAZADO con 3 errores y 3 faltantes, todos con cita del código; corregidos arriba (copista, P2-3, P2-4; semántico, reparto, flujos). Las fallas P2-1..P2-5 se sostienen en el código.
