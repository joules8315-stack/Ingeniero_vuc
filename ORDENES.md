# ÓRDENES DE JULIO — la lista viva (candado del punto 7)

> "Verifica de esto que existe, que falta... Nunca asumas, crea candado para esto." (2026-08-20)

Aquí queda **cada orden de Julio, textual**, con la prueba de que está hecha o no.
El estado **no se escribe a mano**: lo calcula `verificar.py` mirando el disco.
Así nadie puede decir "ya está" sin que sea verdad.

Formato de cada línea:

    ID | orden textual de Julio | COMPROBACION

`COMPROBACION` es lo que se mira en el disco. Tipos:
- `archivo:<ruta>` — existe ese archivo
- `funcion:<modulo>:<nombre>` — ese módulo tiene esa función
- `vigia:<archivo>` — existe esa vigía Y está verde
- `texto:<archivo>:<palabra>` — ese archivo contiene esa palabra
- `manual:<que tiene que ver Julio>` — SOLO Julio puede darlo por bueno (ley 5)
- `hooks_puestos` — los hooks del Ingeniero estan de verdad en el settings de Julio

---

## TANDA 1 (los 6 puntos del plan del Ingeniero)

T1.1 | No dañar lo otro al reparar (cross-flow) | funcion:cerebro.grafo:vecinos
T1.2 | Sin perder contexto entre sesiones | archivo:cuerpo/estado.py
T1.3 | Sin gastar tokens a lo pendejo | vigia:test_vigia_paquete_no_lee_repo_entero.py
T1.4 | Sin que Julio repita instrucciones | archivo:arnes/modo_ingeniero.py
T1.5 | Sin alucinar | vigia:test_vigia_no_inventa.py
T1.6 | Cuerpo dotado de grafo de capas tipo Obsidian | archivo:cerebro/grafo.py
T1.7 | Mapa de todo lo que ya existe | archivo:mapa/MAPA_INGENIERO.md
T1.8 | Rescatar lo útil de C:\vigias y desechar el resto | archivo:memoria/rescate/RESCATE__test_vigia_cerebro_gemini.py

## TANDA 2 (candados, 4 ojos, JSON, skills, modo ingeniero)

T2.1 | Candado en cada instrucción, en cualquier proyecto | funcion:arnes.modo_ingeniero:prompt
T2.2 | Que nunca asuma y siempre pregunte | texto:cerebro/router.py:PREGUNTA_REQUERIDA
T2.3 | Que no pueda desatender ni irse por otro lado | texto:arnes/modo_ingeniero.py:NO IRSE POR OTRO LADO
T2.4 | Que al perder contexto NO continúe, sino que instruya cómo seguir | funcion:arnes.modo_ingeniero:compactar
T2.5 | Apoyo de otras IA gratis, vigilancia de 4 ojos | archivo:cuerpo/obrero.py
T2.6 | Pedir JSON en vez de todo el contexto | funcion:cuerpo.obrero:veredicto_corto
T2.7 | Usar subagentes para eso | archivo:cuerpo/subagentes.py
T2.8 | Buscador y creador de skills | archivo:cuerpo/skills.py
T2.9 | Que busque en las librerías respectivas | texto:cuerpo/skills.py:CONOCIDAS
T2.10 | Y si no existe, que cree las propias | funcion:cuerpo.skills:crear
T2.11 | Siempre modo ingeniero, nunca IA suelta | hooks_puestos
T2.12 | Gastar Qwen, luego Gemini, y VOLVER a Qwen al reponer | vigia:test_vigia_relevo_cuotas.py

## TANDA 3 (vigía cruzada y calidad del trabajo)

T3.1 | Un agente repara mientras OTRO crea la vigía (no autovalidarse) | funcion:cuerpo.cruzado:resolver
T3.2 | Que no rompa nada más | vigia:test_vigia_cross_flow.py
T3.3 | Que no repita instrucciones | funcion:cuerpo.estado:apuntar
T3.4 | Que no reescriba lo ya escrito | vigia:test_vigia_no_repetidera.py
T3.5 | Que ningún proceso sea lento | vigia:test_vigia_nada_lento.py
T3.6 | Que los proyectos funcionen con las mismas reglas (cerebro central, grafo, memoria, vigías, arnés) | funcion:arnes.instalar:instalar
T3.7 | Que entienda, analice y busque la CAUSA RAÍZ | texto:cuerpo/cruzado.py:ataca_la_causa_raiz
T3.8 | Que corrobore con otra IA hasta la solución real | texto:cuerpo/cruzado.py:RONDAS_MAX
T3.9 | Que busque las piezas dentro de los repositorios | funcion:cerebro.router:armar
T3.10 | Memoria de fallos que se actualice constantemente | archivo:cuerpo/fallos.py
T3.11 | Verificar qué existe y qué falta, sin asumir | archivo:verificar.py

T3.12 | Otros modelos como CONSEJEROS que me revisen a mi | funcion:cuerpo.consejeros:consultar
T3.13 | El consejo nunca puede decir lo contrario de lo que votaron | vigia:test_vigia_consejeros.py

T3.14 | Buscar en los repositorios ANTES de preguntar | funcion:cuerpo.dudas:resolver
T3.15 | Pero preguntar SIEMPRE lo que no este escrito | vigia:test_vigia_dudas.py
T3.16 | La pregunta no se puede olvidar (bloquea el cierre) | funcion:cuerpo.dudas:apuntar_pregunta

## TANDA 4 (medir para mejorar)

T4.1 | Medir el acierto, no solo el ahorro | funcion:cuerpo.medidor:juzgar
T4.2 | Aprender de los aciertos y los errores | funcion:cuerpo.medidor:lo_que_falto
T4.3 | Que el router se corrija solo | texto:cerebro/router.py:lo_que_falto
T4.4 | Buscar por significado, no solo por letras | archivo:cerebro/semantico.py
T4.5 | Que el medidor no se automienta | vigia:test_vigia_medidor.py
T4.6 | Que el significado no deje al Ingeniero sin buscador | vigia:test_vigia_semantico.py

T4.7 | Evaluar si la respuesta de Julio fue correcta | funcion:cuerpo.respuestas:evaluar
T4.8 | Si Julio repite, la respuesta anterior no sirvio | vigia:test_vigia_respuestas.py
T4.9 | Poder cerrar una pregunta ya respondida | funcion:cuerpo.estado:respondida

T4.10 | Distinguir "hay que aclararlo" de "no sirvio" | funcion:cuerpo.respuestas:evaluar
T4.11 | Medir aparte cuando el Ingeniero se explica mal | vigia:test_vigia_respuestas.py

## TANDA 5 (que el protocolo se cumpla solo)

T5.1 | Actuar SIEMPRE segun los protocolos ya escritos | archivo:arnes/candado_protocolo.py
T5.2 | Darse cuenta SOLO de que Julio esta repitiendo | funcion:arnes.candado_protocolo:repite
T5.3 | Nada de jerga tecnica con Julio (ley dura) | funcion:arnes.candado_protocolo:salida
T5.4 | Confirmar el objetivo antes de construir (ley dura) | funcion:arnes.candado_protocolo:construir
T5.5 | No preguntarle lo que ya dejo escrito | archivo:arnes/candado_preguntar.py
T5.6 | Que los disparadores muerdan y no atrapen | vigia:test_vigia_protocolo.py

T5.7 | Un solo protocolo unificado (DMM + MVP + rv2) | archivo:PROTOCOLO_UNICO.md
T5.8 | Causa raiz probada antes de reparar (lo inferido no se repara) | archivo:arnes/candado_diagnostico.py
T5.9 | Cada paso del protocolo con su candado | funcion:cuerpo.estado:leer

T5.10 | Siempre el paquete minimo, por todas las vias | archivo:arnes/candado_terminal.py
T5.11 | Ninguna rendija para leer sin control (7 vias) | vigia:test_vigia_sin_rendijas.py
T5.12 | La llave NECESITO_EDITAR existe de verdad | archivo:arnes/permiso_editar.py

## LO QUE SOLO JULIO PUEDE DAR POR BUENO (ley 5: vigía verde NO es prueba)

M.1 | Julio probó el Ingeniero con sus ojos y le sirve | manual:que Julio corra `python ingeniero.py trabaja` y diga si el paquete le sirve
M.2 | Julio autorizó el candado global en todas sus sesiones | manual:que Julio corra el instalador global
M.3 | Julio autorizó enchufar el candado a DMM y Foto Informe | manual:que Julio diga que sí
